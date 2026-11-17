#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
novelty-validator · 向量召回精校 · Tier A 真向量实现
====================================================
在 CN `api_path` 召回候选池之后，对 claim 与每篇候选摘要做真实语义向量化 + 余弦相似度：
  1) 重排序（sim 降序）
  2) 捕获关键词漏检的「改写近邻 (paraphrase near-miss)」：sim>=0.6 但关键词命中率低
  3) 把 sim 喂给 ④ 五级碰撞分级做阈值校准

密钥读取顺序：环境变量 SILICONFLOW_API_KEY → 本目录 config.json。
模型：BAAI/bge-m3（1024 维，中英文混合友好，SiliconFlow 托管）。

用法（作为模块被主链路 ③.5 调用）：
    from vector_recall_impl import VectorRefiner
    ref = VectorRefiner()                 # 自动读 key；无 key 则 available=False
    if ref.available:
        ranked = ref.refine(claim_text, candidates)
        # candidates: [{"title":..,"desc":..,"year":..,"identifier":..}, ...]
        # 返回: [{"title","desc","sim","near_miss","keyword_hit_rate"}, ...] 按 sim 降序
依赖：仅标准库 urllib + json（无第三方依赖，便于嵌入自动化）。
"""
import json
import os
import math
import urllib.request
import urllib.error

_HERE = os.path.dirname(os.path.abspath(__file__))


def _load_key():
    env = os.environ.get("SILICONFLOW_API_KEY")
    if env:
        return env
    try:
        with open(os.path.join(_HERE, "..", "config.json"), encoding="utf-8") as f:
            cfg = json.load(f)
        return cfg.get("SILICONFLOW_API_KEY")
    except Exception:
        return None


class VectorRefiner:
    def __init__(self, model=None, url=None, key=None):
        self.key = key or _load_key()
        self.model = model or os.environ.get("SILICONFLOW_EMBED_MODEL") or "BAAI/bge-m3"
        self.url = url or os.environ.get("SILICONFLOW_EMBED_URL") or "https://api.siliconflow.cn/v1/embeddings"
        self.available = bool(self.key)
        self._cache = {}

    def _embed_one(self, text):
        text = (text or "").strip()
        if not text:
            return None
        if text in self._cache:
            return self._cache[text]
        body = json.dumps({"model": self.model, "input": [text]}).encode("utf-8")
        req = urllib.request.Request(
            self.url, data=body,
            headers={"Authorization": "Bearer " + self.key, "Content-Type": "application/json"},
            method="POST",
        )
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=30) as r:
                    d = json.loads(r.read().decode())
                vec = d["data"][0]["embedding"]
                self._cache[text] = vec
                return vec
            except urllib.error.HTTPError as e:
                if e.code == 429 or e.code == 433:
                    import time
                    time.sleep(1.2 * (attempt + 1))
                    continue
                raise
        return None

    @staticmethod
    def _cosine(a, b):
        if not a or not b:
            return 0.0
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(y * y for y in b))
        if na == 0 or nb == 0:
            return 0.0
        return dot / (na * nb)

    @staticmethod
    def _kw_hit_rate(claim_kw, cand_text):
        """claim 关键词在候选文本里的命中率（用于 near-miss 判定）。"""
        if not claim_kw:
            return 0.0
        hit = sum(1 for k in claim_kw if k in cand_text)
        return hit / len(claim_kw)

    def refine(self, claim_text, candidates, claim_kw=None, top_k=None):
        """
        claim_text : 结构化 claim 文本（用于向量化）
        candidates : [{title, desc, year, identifier, ...}]
        claim_kw   : claim 关键词列表（用于 near-miss 检测，可选）
        """
        if not self.available:
            return None  # 调用方须回退 Tier C
        qvec = self._embed_one(claim_text)
        if qvec is None:
            return None
        out = []
        for c in candidates:
            ctext = f"{c.get('title','')}。{c.get('desc','')}"
            cvec = self._embed_one(ctext)
            sim = self._cosine(qvec, cvec) if cvec else 0.0
            khr = self._kw_hit_rate(claim_kw or [], ctext)
            near_miss = (sim >= 0.6) and (khr < 0.34)  # 语义近但关键词没对上
            out.append({
                "title": c.get("title", ""),
                "year": c.get("year", ""),
                "identifier": c.get("identifier", ""),
                "sim": round(sim, 3),
                "kw_hit_rate": round(khr, 3),
                "near_miss": near_miss,
            })
        out.sort(key=lambda x: x["sim"], reverse=True)
        if top_k:
            out = out[:top_k]
        return out


# ============ 自测（直接运行可验证 key + 模型可用）============
if __name__ == "__main__":
    ref = VectorRefiner()
    print("available:", ref.available, "| model:", ref.model)
    if ref.available:
        demo = ref.refine(
            "用图神经网络做配电网故障定位",
            [{"title": "基于改进时空图神经网络的高渗透率有源配电网故障定位", "desc": "提出一种基于改进时空图神经网络的配电网故障区段定位方法", "year": 2025, "identifier": "2031589494977"},
             {"title": "Predicting Cancer Driver Genes via Contrastive Learning", "desc": "cancer gene prediction", "year": 2025, "identifier": "x1"}],
            claim_kw=["图神经网络", "配电网", "故障定位"],
        )
        for r in demo:
            print(round(r["sim"], 3), "near_miss=" + str(r["near_miss"]), "|", r["title"][:30])
