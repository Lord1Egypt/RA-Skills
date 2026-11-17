#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
layers_lm — 本地小模型层（Phase 4 实装, v3.2）。

supervised_layer: Qwen3-0.6B + LoRA 三分类(+编辑程度回归)检测器的 ONNX int8 推理。
  训练: 单卡 A5000 级 GPU, 两阶段(seed 43); 导出: LoRA merge→ONNX→fp16
  放置: ~/.cache/paper-polisher/qwen3-detector/model.int8.onnx + tokenizer.json
  依赖: pip install onnxruntime (可选; 未装/模型缺失自动返回 None, 引擎回退纯规则)
  tokenizer: 纯Python实现GPT-2式byte-level BPE(优先regex模块精确切分, 缺失时用
             unicodedata分类的等价实现), 不依赖transformers——skill保持stdlib核心。

L12 困惑度层 / L13 曲率层: 预留接口（当前监督层已覆盖其职责, 保持 None 降级）。
"""
import json
import os
import unicodedata

CACHE = os.path.join(os.path.expanduser("~"), ".cache", "paper-polisher")
DET_DIR = os.path.join(CACHE, "qwen3-detector")
MAXLEN = 1024  # 与训练时 tokenizer(truncation=True, max_length=1024) 一致

_sess = None
_tok = None


# ---------------------------------------------------------------------------
# 纯Python Qwen BPE tokenizer (byte-level, GPT-2式)
# ---------------------------------------------------------------------------

def _bytes_to_unicode():
    bs = list(range(ord("!"), ord("~") + 1)) + list(range(ord("¡"), ord("¬") + 1)) + \
        list(range(ord("®"), ord("ÿ") + 1))
    cs = bs[:]
    n = 0
    for b in range(256):
        if b not in bs:
            bs.append(b)
            cs.append(256 + n)
            n += 1
    return dict(zip(bs, map(chr, cs)))


class QwenBPE:
    """从 tokenizer.json 加载 vocab+merges, 实现与 HF Qwen 等价的 encode。

    切分用 tokenizer.json 里 Qwen 自带的 CLIP 变体 pattern(非GPT-2式:
    标点可前缀粘住字母串/数字单切/大小写不敏感缩写), 见 json pre_tokenizer。
    """

    QWEN_SPLIT = (
        r"(?i:'s|'t|'re|'ve|'m|'ll|'d)|[^\r\n\p{L}\p{N}]?\p{L}+|\p{N}"
        r"| ?[^\s\p{L}\p{N}]+[\r\n]*|\s*[\r\n]+|\s+(?!\S)|\s+"
    )

    def __init__(self, path):
        d = json.load(open(path, encoding="utf-8"))
        m = d["model"]
        self.vocab = m["vocab"]
        self.ranks = {}
        for i, pair in enumerate(m["merges"]):
            a, b = pair.split(" ") if isinstance(pair, str) else pair
            self.ranks[(a, b)] = i
        self.byte_enc = _bytes_to_unicode()
        try:
            import regex
            self._re = regex.compile(self.QWEN_SPLIT)
            self._exact = True
        except ImportError:
            self._re = None
            self._exact = False
        self._cache = {}

    def _split(self, text):
        if self._re is not None:
            return self._re.findall(text)
        # 无regex模块的近似实现(非完全等价, 建议pip install regex获取精确切分):
        # 可选非字母数字前缀 + 字母串 / 单数字 / 空格前缀标点串 / 换行串 / 空白
        out, i, n = [], 0, len(text)

        def cls(ch):
            if ch in "\r\n":
                return "R"
            if ch.isspace():
                return "s"
            cat = unicodedata.category(ch)[0]
            return "L" if cat == "L" else ("N" if cat == "N" else "O")

        while i < n:
            j = i
            if text[j] not in "\r\n" and not text[j].isspace() and cls(text[j]) == "O" \
                    and j + 1 < n and cls(text[j + 1]) == "L":
                j += 1  # [^\r\n\p{L}\p{N}]?\p{L}+ 的标点前缀
            c = cls(text[j]) if j < n else "O"
            if c == "L":
                while j < n and cls(text[j]) == "L":
                    j += 1
                out.append(text[i:j]); i = j
            elif c == "N":
                out.append(text[j]); i = j + 1  # \p{N} 单数字
            elif c == "O":
                k = j
                while k < n and cls(text[k]) == "O":
                    k += 1
                while k < n and text[k] in "\r\n":
                    k += 1  # [\r\n]*
                out.append(text[i:k]); i = k
            elif c == "s":
                k = j
                while k < n and text[k].isspace():
                    k += 1
                if k < n and k - i > 1 and text[k] not in "\r\n":
                    k -= 1  # \s+(?!\S): 末一个非换行空白留给下一段
                out.append(text[i:k]); i = k
            else:  # R 换行
                k = j
                while k < n and text[k].isspace():
                    k += 1
                out.append(text[i:k]); i = k
        return out

    def _bpe(self, piece):
        if piece in self._cache:
            return self._cache[piece]
        word = list(piece)
        while len(word) > 1:
            pairs = [(word[i], word[i + 1]) for i in range(len(word) - 1)]
            best = min(pairs, key=lambda p: self.ranks.get(p, 1 << 30))
            if best not in self.ranks:
                break
            a, b = best
            new, i = [], 0
            while i < len(word):
                if i < len(word) - 1 and word[i] == a and word[i + 1] == b:
                    new.append(a + b)
                    i += 2
                else:
                    new.append(word[i])
                    i += 1
            word = new
        self._cache[piece] = word
        return word

    def encode(self, text):
        ids = []
        for piece in self._split(text):
            b = piece.encode("utf-8")
            s = "".join(self.byte_enc[x] for x in b)
            for t in self._bpe(s):
                if t in self.vocab:
                    ids.append(self.vocab[t])
        return ids


# ---------------------------------------------------------------------------
# 监督层推理
# ---------------------------------------------------------------------------

def _load():
    global _sess, _tok
    if _sess is not None:
        return True
    mp = os.path.join(DET_DIR, "model.int8.onnx")
    tp = os.path.join(DET_DIR, "tokenizer.json")
    if not (os.path.isfile(mp) and os.path.isfile(tp)):
        return False
    try:
        import onnxruntime
        so = onnxruntime.SessionOptions()
        # PP_ORT_THREADS: 大核机器(≥32 vCPU)上默认吃满所有核会线程互踩,
        # 实测 56 vCPU 默认=24.9s/篇 vs 限 8 线程≈1-2s/篇; 0=自动(默认, 用户小核机不变)
        _t = int(os.environ.get("PP_ORT_THREADS", "0") or 0)
        if _t > 0:
            so.intra_op_num_threads = _t
            so.inter_op_num_threads = 1
        _sess = onnxruntime.InferenceSession(mp, so, providers=["CPUExecutionProvider"])
        _tok = QwenBPE(tp)
        return True
    except Exception:
        _sess = None
        return False


def supervised_available() -> bool:
    try:
        import onnxruntime  # noqa: F401
    except ImportError:
        return False
    return os.path.isfile(os.path.join(DET_DIR, "model.int8.onnx"))


def supervised_layer(text: str):
    """v3.2 监督层: 返回
    {p_human, p_ai, p_ai_assisted, p_ai_any, [edit_extent], n_tokens} 或 None。
    edit_extent: 第4维回归头输出(0-1), 估计文本被编辑改写的程度(仅v3.2模型有)。
    """
    if not _load():
        return None
    try:
        ids = _tok.encode(text)[:MAXLEN]
        if not ids:
            return None
        import numpy as np
        inp = np.array([ids], dtype=np.int64)
        mask = np.ones_like(inp)
        lg = _sess.run(None, {"input_ids": inp, "attention_mask": mask})[0][0]
        lg = [float(x) for x in lg]
        m = max(lg[:3])
        import math
        e = [math.exp(v - m) for v in lg[:3]]
        s = sum(e)
        p = [v / s for v in e]
        out = {"p_human": round(p[0], 5), "p_ai": round(p[1], 5),
               "p_ai_assisted": round(p[2], 5),
               "p_ai_any": round(min(p[1] + p[2], 1.0), 5), "n_tokens": len(ids)}
        if len(lg) >= 4:
            out["edit_extent"] = round(min(max(lg[3], 0.0), 1.0), 4)
        return out
    except Exception:
        return None


# ---------------------------------------------------------------------------
# L12 / L13 预留接口
# ---------------------------------------------------------------------------

def perplexity_layer(text: str):
    """L12 困惑度层: 监督层就位后职责已被覆盖, 保留接口返回 None。"""
    return None


def curvature_layer(text: str):
    """L13 曲率/双筒层: 预留。"""
    return None


def status() -> dict:
    ok = supervised_available() and _load()
    return {"supervised_available": ok,
            "model_dir": DET_DIR if ok else "",
            "tokenizer_engine": ("regex" if _tok and _tok._exact else "unicodedata") if ok else "",
            "hint": "" if ok else
                    "可选监督层未启用: pip install onnxruntime 并放置 model.int8.onnx + "
                    "tokenizer.json 到 ~/.cache/paper-polisher/qwen3-detector/ "
                    "(引擎自动回退纯规则融合, 不影响使用)"}


if __name__ == "__main__":
    import sys as _sys
    try:  # v3.5: 中文 Windows 默认 GBK 控制台会因 emoji/警示符崩溃 stdout——统一 UTF-8
        _sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        _sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    print(json.dumps(status(), ensure_ascii=False))
    demo = supervised_layer("在这个日新月异的时代，人工智能正在改变我们的生活。"
                            "它不仅提升了效率，更重塑了产业的形态。")
    print("demo:", json.dumps(demo, ensure_ascii=False))
