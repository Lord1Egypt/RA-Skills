#!/usr/bin/env python3
"""
Semantic Check — 语义检查引擎（v1.0）
基于 BAAI/bge-small-zh-v1.5 实现语义级别的内容审核。

定位：finalize-chapter 第5步（logic 之后）
有模型 → 执行主力HARD + 辅助SOFT 共5项检测
无模型 → 自动跳过，不影响现有流程

主力[HARD] 2项:
  1. overview-vs-content 语义对齐 <0.4 → 阻断
  2. 子结构间语义跳跃 <0.4 → 阻断

辅助[SOFT] 3项:
  3. 情绪实际 vs 规划偏离 → SOFT
  4. 同义冗余 >0.85 → SOFT
  5. 跨章主题延续 <0.25 → SOFT

依赖：
  - sentence-transformers (pip install)
  - BAAI/bge-small-zh-v1.5 (首次自动下载 33MB)
  - torch (CPU only ~200MB，作为 sentence-transformers 间接依赖)

镜像（安装/下载）：
  PyPI:
    pip install sentence-transformers -i https://mirrors.aliyun.com/pypi/simple/
    pip install sentence-transformers -i https://pypi.tuna.tsinghua.edu.cn/simple/
    pip install sentence-transformers -i https://mirrors.cloud.tencent.com/pypi/simple/
  Model:
    HF_ENDPOINT=https://hf-mirror.com python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-small-zh-v1.5')"
    pip install modelscope && python -c "from modelscope import snapshot_download; snapshot_download('BAAI/bge-small-zh-v1.5')"
  Torch (CPU only):
    pip install torch --index-url https://download.pytorch.org/whl/cpu -i https://mirrors.aliyun.com/pypi/simple/
"""
import json, sys, os, re
from pathlib import Path

_MODEL = None
_MODEL_NAME = "BAAI/bge-small-zh-v1.5"

# ── 情绪词参考表（用于情绪偏离检测） ──
EMOTION_KEYWORDS = {
    "紧张": ["脚步声", "围堵", "攥紧", "屏息", "逼近", "昏暗", "颤抖", "冷汗", "心跳",
             "身后", "不敢动", "停步", "围上来", "黑暗", "夜路", "短句", "压迫", "紧张"],
    "悲伤": ["沉默", "怀念", "叹息", "沉重", "别离", "往事", "难过", "哽咽", "遗物",
             "远方", "说不出口", "一个人", "伤心", "哭", "眼泪", "悲伤"],
    "愤怒": ["握拳", "砸桌", "低吼", "瞪", "质问", "凭什么", "混蛋", "找死",
             "忍不住", "怒", "愤怒", "火大"],
    "温馨": ["微笑", "轻声", "牵", "晚饭", "灯光", "肩膀", "晚安", "相依", "家",
             "温馨", "暖", "温柔"],
    "悬疑": ["为什么", "怎么回事", "痕迹", "不对劲", "暗自", "暗中", "视线",
             "余光", "奇怪", "疑问", "悬疑"],
    "平静": ["躺着", "闭眼", "呼吸", "均匀", "微风", "寂静", "枕头", "梦", "平静"],
    "恐惧": ["后退", "尖叫", "跑", "逃", "拼命", "僵硬", "屏住", "冷汗", "恐惧", "害怕"],
    "欢乐": ["笑出声", "哈哈", "得意", "轻松", "嬉笑", "乐", "欢乐", "开心"],
    "疑惑探索": ["好奇", "翻", "查看", "研究", "琢磨", "试验", "对比", "验证",
                 "想不通", "定睛", "端详", "疑惑", "探索"],
    "专注": ["专注", "凝视", "目不转睛", "仔细", "认真", "盯着", "埋头", "研读",
             "一字不漏", "专注"],
    "启发": ["原来如此", "明白了", "懂了", "灵感", "窍", "悟", "发现",
             "意识到", "突然明白", "启发"],
    "顿悟": ["豁然", "一下子", "灵光", "开窍", "通透", "醍醐", "秒懂", "顿悟"],
}


def _load_model():
    """懒加载模型，失败则设为 None。只在本地已缓存时加载，永不联网尝试。"""
    global _MODEL
    if _MODEL is not None:
        return _MODEL
    try:
        import os as _os
        # 强制 CPU，避免与 LM Studio 抢夺 GPU 显存（在 sentence_transformers 导入前设置）
        _os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")
        # sentence_transformers 导入时需要 HF_ENDPOINT 指向镜像以避免挂死
        _os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

        # 查找本地模型缓存
        try:
            sys.path.insert(0, str(Path(__file__).parent))
            from _path_utils import MODELS_DIR
            model_cache = str(MODELS_DIR / "bge-small-zh")
        except Exception:
            model_cache = str(Path.home() / ".cache" / "huggingface" / "hub")

        model_id_safe = _MODEL_NAME.replace("/", "--")
        model_id_safe = "models--" + model_id_safe
        hub_path = Path(model_cache) / model_id_safe

        # 先检查 MODELS_DIR
        if hub_path.exists() and (hub_path / "snapshots").exists():
            snapshot_dir = sorted((hub_path / "snapshots").iterdir())[-1]
            model_path = str(snapshot_dir)
        else:
            # 再检查标准 HF 缓存
            default_hub = str(Path.home() / ".cache" / "huggingface" / "hub")
            default_path = Path(default_hub) / model_id_safe
            if default_path.exists() and (default_path / "snapshots").exists():
                snapshot_dir = sorted((default_path / "snapshots").iterdir())[-1]
                model_path = str(snapshot_dir)
            else:
                # 没本地模型 → 跳过，绝不联网
                print("[语义检查] 跳过：本地无模型缓存，用户需主动安装")
                print("[语义检查] 安装命令: pip install sentence-transformers && HF_ENDPOINT=https://hf-mirror.com python -c \"from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-small-zh-v1.5')\"")
                _MODEL = None
                return _MODEL

        from sentence_transformers import SentenceTransformer
        _MODEL = SentenceTransformer(model_path)
        print(f"[语义检查] 模型已加载 (本地): {model_path[:80]}")
        print(f"[语义检查] 缓存路径: {model_cache}")
    except ImportError:
        print("[语义检查] 模型不可用: 未安装 sentence-transformers")
        print("[语义检查] 安装: pip install sentence_transformers -i https://mirrors.aliyun.com/pypi/simple/")
        _MODEL = None
    except Exception as e:
        print(f"[语义检查] 模型加载失败: {e}")
        print("[语义检查] 模型将自动跳过，不影响现有流程")
        _MODEL = None
    return _MODEL


def _encode(texts):
    """编码文本为 embeddings"""
    model = _load_model()
    if model is None:
        return None
    return model.encode(texts, normalize_embeddings=True)


def _similarity(a, b):
    """cosine similarity (已 normalize 的向量点积)"""
    import numpy as np
    return float(np.dot(a, b))


def _read_sub_file(chapter_dir, sub_key):
    """读取子结构文件正文（跳过标题行和末行标记）"""
    p = Path(chapter_dir) / f"{sub_key}.txt"
    if not p.exists():
        return ""
    lines = p.read_text(encoding="utf-8-sig").strip().split("\n")
    # 跳过子结构标题行 L## · S##《...》
    lines = [l for l in lines if not re.match(r'L\d+ · S\d+《', l.strip())]
    # 跳过末行编号 L01S01
    if lines and re.match(r'L\d+S\d+', lines[-1].strip()):
        lines = lines[:-1]
    return "\n".join(lines)


def _read_sub_head_tail(chapter_dir, sub_key, n=3):
    """读取子结构头 n 行和尾 n 行（不含标题和标记行）"""
    text = _read_sub_file(chapter_dir, sub_key)
    if not text:
        return "", ""
    lines = text.strip().split("\n")
    head = "\n".join(lines[:n]) if len(lines) >= n else text
    tail = "\n".join(lines[-n:]) if len(lines) >= n else text
    return head, tail


def check_semantic(state_path, chapter, chapter_dir):
    """
    语义检查主入口。
    返回 issues list，格式同 finalize-chapter 标准：
    [{"file", "problem", "position", "severity", "suggestion"}]
    """
    issues = []

    # ── 加载 state ──
    sp = Path(state_path)
    if not sp.exists():
        print("[语义检查] state 文件不存在，跳过")
        return issues
    data = json.loads(sp.read_text(encoding="utf-8-sig"))

    # ── 尝试加载模型 ──
    model = _load_model()
    if model is None:
        print("\n  [语义检查] 跳过（无 bge-small-zh 模型）")
        return issues

    print(f"\n{'='*50}")
    print(f"[语义检查] 开始语义审核...")
    print(f"{'='*50}")

    # 加载 numpy（首次使用）
    import numpy as np

    # 查找当前章节
    ch_info = None
    for ch in data.get("chapters", []):
        if ch["id"] == chapter:
            ch_info = ch
            break
    if not ch_info:
        return issues

    subs = ch_info.get("sub_structures", {})
    if not subs:
        return issues

    sorted_keys = sorted(subs.keys())

    # ──────────────────────────────────────────────
    # 主力1: overview-vs-content 语义对齐 [HARD]
    # ──────────────────────────────────────────────
    overview = ch_info.get("overview", "")
    if overview:
        # 拼接本章所有子结构正文
        full_text_parts = []
        for sk in sorted_keys:
            text = _read_sub_file(chapter_dir, sk)
            if text.strip():
                full_text_parts.append(text)
        full_text = "\n".join(full_text_parts)

        if full_text.strip():
            ov_emb = _encode([overview])
            ct_emb = _encode([full_text])
            if ov_emb is not None and ct_emb is not None:
                score = _similarity(ov_emb[0], ct_emb[0])
                print(f"\n  [主力1] overview-vs-content 对齐度: {score:.3f}")
                if score < 0.4:
                    issues.append({
                        "file": chapter,
                        "problem": f"本章正文语义偏离概述（相似度 {score:.3f} < 0.4）",
                        "position": f"{chapter} overview-vs-content",
                        "severity": "HARD",
                        "suggestion": "正文内容与规划概述的主题不匹配，请检查是否写了正确的内容"
                    })
                    print(f"    → [HARD] 阻断：正文语义偏离概述")
                elif score < 0.6:
                    issues.append({
                        "file": chapter,
                        "problem": f"本章正文与概述语义部分偏离（相似度 {score:.3f}）",
                        "position": f"{chapter} overview-vs-content",
                        "severity": "SOFT",
                        "suggestion": "正文与概述主题部分匹配，建议检查是否有内容偏移"
                    })
                    print(f"    → [SOFT] 提示：轻微偏离")
                else:
                    print(f"    → [OK] 对齐")

    # ──────────────────────────────────────────────
    # 主力2: 子结构间语义跳跃 [HARD]
    # ──────────────────────────────────────────────
    jump_issues = []
    for i in range(len(sorted_keys) - 1):
        sk1, sk2 = sorted_keys[i], sorted_keys[i + 1]
        _, tail1 = _read_sub_head_tail(chapter_dir, sk1)
        head2, _ = _read_sub_head_tail(chapter_dir, sk2)
        if not tail1.strip() or not head2.strip():
            continue
        t1_emb = _encode([tail1])
        h2_emb = _encode([head2])
        if t1_emb is None or h2_emb is None:
            continue
        score = _similarity(t1_emb[0], h2_emb[0])
        print(f"\n  [主力2] {sk1}→{sk2} 语义跳跃: {score:.3f}")
        if score < 0.4:
            jump_issues.append({
                "file": f"{chapter}",
                "problem": f"{sk1}→{sk2} 语义断裂（相似度 {score:.3f} < 0.4）",
                "position": f"{chapter} {sk1}→{sk2}",
                "severity": "HARD",
                "suggestion": f"检查 {sk1} 结尾与 {sk2} 开头之间是否有内容断裂，需添加过渡"
            })
            print(f"    → [HARD] 阻断：语义跳断")
        elif score < 0.6:
            jump_issues.append({
                "file": f"{chapter}",
                "problem": f"{sk1}→{sk2} 话题过渡不够自然（相似度 {score:.3f}）",
                "position": f"{chapter} {sk1}→{sk2}",
                "severity": "SOFT",
                "suggestion": "建议在两段之间添加更平滑的过渡"
            })
            print(f"    → [SOFT] 提示：过渡偏弱")
        else:
            print(f"    → [OK] 连续")
    issues += jump_issues

    # ──────────────────────────────────────────────
    # 辅助3: 情绪实际 vs 规划偏离 [SOFT]
    # ──────────────────────────────────────────────
    for sk in sorted_keys:
        sv = subs[sk]
        tone = sv.get("tone", "")
        if not tone:
            continue
        text = _read_sub_file(chapter_dir, sk)
        if not text.strip():
            continue
        # 简单情绪词频匹配（非 BERT，纯词表）
        tone_words = EMOTION_KEYWORDS.get(tone, [])
        if not tone_words:
            continue
        text_lower = text.lower()
        hits = sum(1 for w in tone_words if w in text_lower)
        hit_rate = hits / len(tone_words) if tone_words else 0
        print(f"\n  [辅助3] {sk} 情绪命中率: {hit_rate:.2f}（规划={tone}）")
        if hit_rate < 0.05:
            issues.append({
                "file": f"{chapter}",
                "problem": f"{sk} 情绪偏离规划（规划{tone}，情绪词命中率 {hit_rate:.2f}）",
                "position": f"{chapter} {sk} tone",
                "severity": "SOFT",
                "suggestion": f"规划情绪为「{tone}」，当前正文情绪词很少，建议检查是否偏离规划基调"
            })
            print(f"    → [SOFT] 提示：情绪基调可能偏离")

    # ──────────────────────────────────────────────
    # 辅助4: 同义冗余检测 [SOFT]
    # ──────────────────────────────────────────────
    for i in range(len(sorted_keys) - 1):
        sk1, sk2 = sorted_keys[i], sorted_keys[i + 1]
        text1 = _read_sub_file(chapter_dir, sk1)
        text2 = _read_sub_file(chapter_dir, sk2)
        if not text1.strip() or not text2.strip():
            continue
        e1 = _encode([text1])
        e2 = _encode([text2])
        if e1 is None or e2 is None:
            continue
        score = _similarity(e1[0], e2[0])
        print(f"\n  [辅助4] {sk1}↔{sk2} 语义重复度: {score:.3f}")
        if score > 0.85:
            issues.append({
                "file": f"{chapter}",
                "problem": f"{sk1}↔{sk2} 语义高度接近（相似度 {score:.3f}），可能有冗余",
                "position": f"{chapter} {sk1}↔{sk2}",
                "severity": "SOFT",
                "suggestion": "两个子结构内容语义上很接近，检查是否是有意重复或需要精简"
            })
            print(f"    → [SOFT] 提示：可能冗余")

    # ──────────────────────────────────────────────
    # 辅助5: 跨章主题延续 [SOFT]
    # ──────────────────────────────────────────────
    chapters_list = data.get("chapters", [])
    ch_idx = -1
    for i, ch in enumerate(chapters_list):
        if ch["id"] == chapter:
            ch_idx = i
            break
    if ch_idx > 0:
        prev_ch = chapters_list[ch_idx - 1]
        prev_ch_dir = Path(chapter_dir).parent / prev_ch["id"]
        # 拼接上章全文
        prev_text_parts = []
        prev_subs = prev_ch.get("sub_structures", {})
        for pk in sorted(prev_subs.keys()):
            t = _read_sub_file(str(prev_ch_dir), pk)
            if t.strip():
                prev_text_parts.append(t)
        prev_text = "\n".join(prev_text_parts)
        if prev_text.strip() and full_text.strip():
            pe = _encode([prev_text])
            ce = _encode([full_text])
            if pe is not None and ce is not None:
                score = _similarity(pe[0], ce[0])
                print(f"\n  [辅助5] {prev_ch['id']}↔{chapter} 跨章主题延续: {score:.3f}")
                if score < 0.25:
                    issues.append({
                        "file": f"{chapter}",
                        "problem": f"与上一章（{prev_ch['id']}）主题延续弱（相似度 {score:.3f}）",
                        "position": f"{chapter} cross-chapter",
                        "severity": "SOFT",
                        "suggestion": "本章与上一章内容主题差距较大，检查是否有意为之或需要加强衔接"
                    })
                    print(f"    → [SOFT] 提示：主题延续弱")

    print(f"\n{'─'*50}")
    h_count = len([i for i in issues if i.get("severity") == "HARD"])
    s_count = len([i for i in issues if i.get("severity") == "SOFT"])
    print(f"[语义检查] 完成: {h_count} HARD + {s_count} SOFT")
    print(f"{'='*50}")

    return issues


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("用法: python novel_semantic_check.py <state_path> <chapter> <chapter_dir>")
        sys.exit(1)
    issues = check_semantic(sys.argv[1], sys.argv[2], sys.argv[3])
    if issues:
        print(f"\n发现 {len(issues)} 个问题:")
        for i in issues:
            print(f"  [{i.get('severity','?')}] {i.get('problem','?')}")
    else:
        print("\n语义检查全部通过。")
