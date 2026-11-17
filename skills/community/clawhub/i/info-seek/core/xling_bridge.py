#!/usr/bin/env python3
"""core/xling_bridge.py — GA10 跨语言别名桥接唯一真源（v1.9.0 / mod-v1.0.0）

治理动机（ROADMAP §8.11.1 D1 / §8.12.2 GA10）
----------------------------------------------
实测：中文主题 × 拉丁文正文的语义相似度（Jaccard/字符串包含）趋零，
`ualberta.ca` 官方一手权威源（唯一确证人物身份）仅得 9 分被判「❌噪声」——
英文源因中文 query 被**系统性低估**。两处闸门同病：

  1. `infoseek_core_v2.score_source` semantic_fallback 分支（评分侧，D1 实锤现场）
  2. `infoseek_pipeline._filter_relevant` 语义阈值 + 中文多字词硬门槛（召回侧）

本模块提供实体中介的跨语言桥接：subject 中的**人名拼音别名**（GA9 person_ner）
与**词典实体跨语言别名**（entities aliases 拉丁形态，如 比亚迪→BYD）构成别名组；
源文本词边界命中任一组 → 桥接分保底（单组 55 = 🟡潜力，多组递增至 70 封顶），
使英文一手源不再归零。**只在原口径低估时抬升（max 语义），不改变任何既有命中路径。**

消费方（统一经模块对象属性访问，禁 from-import —— §8.13.3 铁律）：
  - `scripts/infoseek_core_v2.py`  score_source fallback → max(jaccard, containment×0.8, bridge)
  - `scripts/infoseek_pipeline.py` _filter_relevant → 桥接命中豁免双门槛；_expand_query → ⑤ 拼音别名扩展

设计约束
--------
- 别名「区分度」守卫：单 token 拉丁别名须 ≥4 字符或全大写缩写（≥2），且不在
  常见英文词 blocklist（apple/meta/shell 类多义词禁止桥接，防假阳性抬分）；
  多 token 别名（'linjian xiang'）天然区分，直接放行。
- env 闸：INFOSEEK_XLING_BRIDGE（默认开）→ 关闭时 bridge_score 恒 0（零回归通道）。
- 缓存纪律（GA8 教训）：subject → 别名组走 lru_cache **不可变结构**（tuple），
  外层返回 copy 防调用方 mutate 污染；别名 → 正则 pattern 独立 lru_cache。
- 导入纪律：经顶层模块名导入（person_ner / entities），规避 core./顶层双模块分裂。
- 版本维度：mod-v1.0.0，非 skill 对外版本。
"""

from __future__ import annotations

import functools
import logging
import os
import re
import sys
from pathlib import Path

__all__ = ['MOD_VERSION', 'build_alias_groups', 'bridge_score',
           'expansion_aliases', 'BRIDGE_BASE', 'BRIDGE_STEP', 'BRIDGE_CAP']

MOD_VERSION = '1.0.0'

log = logging.getLogger(__name__)

_CORE_DIR = str(Path(__file__).parent)
if _CORE_DIR not in sys.path:
    sys.path.insert(0, _CORE_DIR)

import person_ner as _person_mod          # noqa: E402  模块对象导入（晚绑定纪律）
import entities as _entities_mod          # noqa: E402

# ── 口径常量（单源；调整此处即全局生效）─────────────────────────────
BRIDGE_BASE = 55        # 单组命中保底分（≥40 → 🟡潜力，脱离 ❌噪声）
BRIDGE_STEP = 5         # 每多命中一组的递增
BRIDGE_CAP = 70         # 封顶（= 🟢核心门槛，多组强命中可入核心）
_TEXT_SCAN_LIMIT = 4000 # 源文本扫描截断（性能护栏）
_MAX_GROUPS = 6         # subject 别名组上限
_MAX_LAT_PER_GROUP = 6  # 每组拉丁别名上限

# 常见英文多义词（禁止作为单 token 桥接别名——假阳性主源）
_COMMON_WORD_BLOCK = frozenset({
    'apple', 'meta', 'amazon', 'oracle', 'shell', 'visa', 'master', 'magic',
    'smart', 'future', 'open', 'deep', 'general', 'universal', 'unity',
    'origin', 'pioneer', 'summit', 'apex', 'titan', 'atlas', 'falcon',
    'eagle', 'dragon', 'tiger', 'panda', 'lotus', 'crown', 'arrow', 'spark',
    'flash', 'storm', 'cloud', 'river', 'ocean', 'mountain', 'forest',
    'python', 'java', 'ruby', 'swift', 'kotlin', 'golang', 'rust',
})

_LATIN_FULL_RE = re.compile(r'^[A-Za-z][A-Za-z0-9 .+\-]*$')
_CHN_RE = re.compile(r'[\u4e00-\u9fff]')


def _env_on(name: str, default: bool = True) -> bool:
    v = os.environ.get(name, '')
    if v == '':
        return default
    return v not in ('0', 'false', 'False', 'no', 'off')


# ── 别名区分度守卫 ──────────────────────────────────────────────────

def _alias_distinctive(alias: str, original: str = None) -> bool:
    """拉丁别名区分度判定（多 token 放行；单 token ≥4 字符或全大写缩写 ≥2）。"""
    a = (alias or '').strip().lower()
    if len(a) < 2:
        return False
    tokens = a.split()
    if len(tokens) >= 2:
        return all(len(t) >= 2 for t in tokens)
    if a in _COMMON_WORD_BLOCK:
        return False
    src = original or alias or ''
    if src.isupper() and len(a) >= 2:      # 词典原形全大写缩写（BYD/CATL/AWS）
        return True
    return len(a) >= 4


def _q_hit(name: str, subject_lower: str) -> bool:
    """subject 命中判定（与 ner/_expand_query 同语义：拉丁词边界，中文子串）。"""
    nl = (name or '').lower()
    if not nl:
        return False
    if re.search(r'[a-z0-9]', nl):
        try:
            return re.search(r'(?<![a-z0-9_])' + re.escape(nl) + r'(?![a-z0-9_])',
                             subject_lower) is not None
        except Exception:
            return nl in subject_lower
    return nl in subject_lower


# ── 别名组构建（subject → 跨语言别名组；不可变缓存 + 外层 copy）──────

@functools.lru_cache(maxsize=512)
def _groups_cached(subject: str) -> tuple:
    """返回 tuple((zh, tuple(latin_aliases)), ...)（lru_cache 须不可变结构）。"""
    if not subject:
        return ()
    groups = []          # [[zh, [latin...]], ...]（末尾转 tuple 入缓存）
    seen_zh = {}         # zh → group（去重：bootstrap 注册后人名兼具词典实体身份）
    sl = subject.lower()

    # 1) 人名拼音别名（GA9 ⑤：subject 模式检测，含 2 字名）
    try:
        for p in _person_mod.detect_person_names(subject, mode='subject'):
            lats = list(dict.fromkeys(
                a for a in _person_mod.person_pinyin_aliases(p['name'])
                if _alias_distinctive(a)
            ))[:_MAX_LAT_PER_GROUP]
            if lats:
                g = [p['name'], lats]
                groups.append(g)
                seen_zh[p['name']] = g
    except Exception:
        pass

    # 2) 词典实体跨语言别名（比亚迪→BYD；商汤科技→SenseTime）
    try:
        for e in _entities_mod.get_all_entities():
            if len(groups) >= _MAX_GROUPS:
                break
            ename = e.get('name', '')
            names = [ename] + list(e.get('aliases', []) or [])
            if not any(_q_hit(n, sl) for n in names):
                continue
            lats = []
            for a in names:
                al = (a or '').strip().lower()
                if (al and al not in sl and _LATIN_FULL_RE.match(al)
                        and _alias_distinctive(al, original=a) and al not in lats):
                    lats.append(al)
                if len(lats) >= _MAX_LAT_PER_GROUP:
                    break
            if not lats:
                continue
            if ename in seen_zh:
                # 同名组（人名注册体）→ 合并拉丁别名，不重复建组
                g = seen_zh[ename]
                for a in lats:
                    if a not in g[1] and len(g[1]) < _MAX_LAT_PER_GROUP:
                        g[1].append(a)
            else:
                g = [ename, lats]
                groups.append(g)
                seen_zh[ename] = g
    except Exception:
        pass

    return tuple((zh, tuple(lats)) for zh, lats in groups[:_MAX_GROUPS])


def build_alias_groups(subject: str) -> list:
    """subject → 跨语言别名组 [{'zh', 'latin': [...]}]（缓存外层 copy，防污染）。"""
    try:
        cached = _groups_cached(subject or '')
    except Exception:
        return []
    return [{'zh': zh, 'latin': list(lats)} for zh, lats in cached]


# ── 桥接评分 ────────────────────────────────────────────────────────

@functools.lru_cache(maxsize=1024)
def _alias_pattern(alias: str):
    """别名 → 词边界正则（token 间允许空白/连字符；两端拉丁数字边界）。"""
    tokens = [re.escape(t) for t in alias.split() if t]
    body = r'[\s\-]+'.join(tokens)
    return re.compile(r'(?<![a-z0-9])' + body + r'(?![a-z0-9])')


def bridge_score(text: str, subject: str) -> int:
    """跨语言桥接分：0（未触发/未命中）或 55-70（命中组数递增）。

    触发前提：subject 存在人名拼音别名或实体拉丁别名组；text 前 4000 字符
    词边界命中 ≥1 组。env INFOSEEK_XLING_BRIDGE=off → 恒 0。
    """
    if not _env_on('INFOSEEK_XLING_BRIDGE', True):
        return 0
    if not text or not subject:
        return 0
    try:
        groups = _groups_cached(subject)
    except Exception:
        return 0
    if not groups:
        return 0
    tl = text[:_TEXT_SCAN_LIMIT].lower()
    hits = 0
    for _zh, lats in groups:
        for a in lats:
            try:
                if _alias_pattern(a).search(tl):
                    hits += 1
                    break
            except Exception:
                continue
    if not hits:
        return 0
    score = min(BRIDGE_CAP, BRIDGE_BASE + (hits - 1) * BRIDGE_STEP)
    log.info(f"[xling] 桥接命中 '{subject[:30]}' ×{hits} 组 → {score}")
    return score


# ── ⑤ 召回扩展（_expand_query 消费）─────────────────────────────────

def expansion_aliases(subject: str, cap: int = 3, exclude_lower: str = '',
                      exclude: set = None) -> list:
    """subject → 跨语言扩展别名（人名拼音优先 → 实体拉丁别名；≤cap）。

    exclude_lower: 原 query 小写（已含词不再扩展）；exclude: 已收集扩展词小写集
    （避免与实体别名扩展重复，如 BYD 已被词典通道扩出）。
    """
    if not _env_on('INFOSEEK_XLING_BRIDGE', True):
        return []
    exclude = {x.lower() for x in (exclude or set())}
    out = []
    for zh, lats in _groups_cached(subject or ''):
        for a in lats:
            if (a not in exclude and a not in (exclude_lower or '')
                    and a not in out):
                out.append(a)
            if len(out) >= cap:
                return out
    return out
