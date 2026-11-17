#!/usr/bin/env python3
"""core/jieba_bridge.py — jieba / pypinyin 统一探测·初始化·降级桥（mod-v1.0.0）

治理动机（2026-09-29 六处裸 import 收敛）
----------------------------------------
收敛前同一组「可选中文 NLP 依赖」存在 **6 处裸 import、3 套独立探测/告警状态**：
  - `scripts/text_tokenizer.py`      —— jieba 探测 + 缺失一次性告警
  - `core/person_ner.py`             —— pypinyin 探测 + jieba.dt 探测/initialize（各一套）
  - `core/entity_aliases.py`         —— jieba.posseg，**热路径每次调用** try-import（无缓存）
  - `core/entity_profile.py`         —— jieba，每次 `_extract_topics` try-import（无缓存）
  - `scripts/infoseek_zerodep_nlp.py` —— jieba.analyse，每次调用 try-import

缺陷：①热路径重复 import（GA8 教训：import find_spec 可占 89% 耗时）；
②探测/告警状态三套，口径可能漂移；③降级行为散落各处。

本桥统一为唯一入口：
  - **探测进程内缓存一次**（get_jieba / get_dt / get_posseg / get_analyse / get_pypinyin）；
  - **初始化按需触发一次**（jieba.dt.initialize）；
  - **缺失告警一次性**（warn_jieba_once / warn_pypinyin_once，调用方按需启用）；
  - **降级永不抛错**：依赖缺失/运行期异常统一返回 None / 空集 / 0，由调用方走兜底。

mock 契约（晚绑定，§8.13.3 铁律）
----------------------------------
消费方必须以「模块对象 + 属性访问」方式使用本桥
（`import jieba_bridge as _jb` 或函数内 `from core import jieba_bridge`），
**禁止 from-import 本桥函数**——否则 mock.patch/monkey-patch 早绑定击穿。

双模块状态分裂防护
------------------
`core/` 既可作包导入（`from core import jieba_bridge`），其目录也在 sys.path
（顶层 `import jieba_bridge`）。模块加载尾部做 sys.modules 双向登记，
保证两条导入路径拿到**同一模块对象**、探测状态合一（同 capability_registry 模式）。

设计约束
--------
- 不 import 任何 infoseek 内部模块 → 天然无循环依赖；
- jieba / pypinyin 均为可选依赖（requirements.txt 已声明），缺失只降级不致命；
- 版本维度：mod-v1.0.0（模块内部版本），非 skill 对外版本
  （对外唯一真源见 `mcp_tools_common.SKILL_VERSION`）。
"""

from __future__ import annotations

import logging
from typing import List, Optional, Set

__all__ = [
    'MOD_VERSION',
    'get_jieba', 'lcut',
    'get_posseg', 'posseg_cut',
    'get_dt', 'word_freq',
    'textrank', 'extract_tags',
    'get_pypinyin', 'lazy_pinyin',
    'warn_jieba_once', 'warn_pypinyin_once',
    'reset',
]

MOD_VERSION = '1.0.0'

log = logging.getLogger(__name__)

# ── 进程内探测状态（每个依赖至多 try-import 一次）────────────────────
_JIEBA = None               # jieba 模块对象 / None
_JIEBA_PROBED = False
_JIEBA_DT = None            # jieba.dt（已 initialize）/ None
_JIEBA_DT_PROBED = False
_POSSEG = None              # jieba.posseg 模块 / None
_POSSEG_PROBED = False
_ANALYSE = None             # jieba.analyse 模块 / None
_ANALYSE_PROBED = False
_PYPINYIN = None            # pypinyin 模块 / None
_PYPINYIN_PROBED = False

# ── 一次性告警状态 ───────────────────────────────────────────────────
_JIEBA_WARNED = False
_PYPINYIN_WARNED = False


# ── 探测（永不抛错）─────────────────────────────────────────────────

def get_jieba():
    """探测 jieba 模块（进程内一次）；不可用返回 None。"""
    global _JIEBA, _JIEBA_PROBED
    if not _JIEBA_PROBED:
        try:
            import jieba
            _JIEBA = jieba
        except Exception:
            _JIEBA = None
        _JIEBA_PROBED = True
    return _JIEBA


def get_dt():
    """探测 jieba.dt 并按需 initialize（进程内一次）；不可用返回 None。

    jieba 首次 lcut 会隐式建词典；此处显式 initialize 供词频守卫
    （FREQ 查询）独立使用，初始化成本进程内一次性。
    """
    global _JIEBA_DT, _JIEBA_DT_PROBED
    if not _JIEBA_DT_PROBED:
        jb = get_jieba()
        if jb is not None:
            try:
                jb.dt.initialize()
                _JIEBA_DT = jb.dt
            except Exception:
                _JIEBA_DT = None
        _JIEBA_DT_PROBED = True
    return _JIEBA_DT


def get_posseg():
    """探测 jieba.posseg（进程内一次）；不可用返回 None。"""
    global _POSSEG, _POSSEG_PROBED
    if not _POSSEG_PROBED:
        jb = get_jieba()
        if jb is not None:
            try:
                import jieba.posseg as pseg
                _POSSEG = pseg
            except Exception:
                _POSSEG = None
        _POSSEG_PROBED = True
    return _POSSEG


def get_analyse():
    """探测 jieba.analyse（进程内一次）；不可用返回 None。"""
    global _ANALYSE, _ANALYSE_PROBED
    if not _ANALYSE_PROBED:
        jb = get_jieba()
        if jb is not None:
            try:
                import jieba.analyse as analyse
                _ANALYSE = analyse
            except Exception:
                _ANALYSE = None
        _ANALYSE_PROBED = True
    return _ANALYSE


def get_pypinyin():
    """探测 pypinyin 模块（进程内一次）；不可用返回 None。"""
    global _PYPINYIN, _PYPINYIN_PROBED
    if not _PYPINYIN_PROBED:
        try:
            import pypinyin
            _PYPINYIN = pypinyin
        except Exception:
            _PYPINYIN = None
        _PYPINYIN_PROBED = True
    return _PYPINYIN


# ── 一次性告警 ─────────────────────────────────────────────────────

def warn_jieba_once(suffix: str = '') -> None:
    """jieba 缺失一次性 WARNING（调用方按需触发；重复调用不刷屏）。"""
    global _JIEBA_WARNED
    if get_jieba() is None and not _JIEBA_WARNED:
        log.warning("[jieba_bridge] jieba 未安装 → 中文分词/词频能力降级"
                    "（精度下降；建议 pip install jieba）%s", suffix)
        _JIEBA_WARNED = True


def warn_pypinyin_once(suffix: str = '') -> None:
    """pypinyin 缺失一次性 WARNING（调用方按需触发）。"""
    global _PYPINYIN_WARNED
    if get_pypinyin() is None and not _PYPINYIN_WARNED:
        log.warning("[jieba_bridge] pypinyin 未安装 → 拼音别名降级为空"
                    "（检测/注册不受影响；建议 pip install pypinyin）%s", suffix)
        _PYPINYIN_WARNED = True


# ── 薄能力封装（异常即降级，返回值语义见各 docstring）───────────────

def lcut(text: str) -> Optional[List[str]]:
    """jieba.lcut 全模式切词；jieba 缺失/异常 → None（调用方走回退分词）。"""
    jb = get_jieba()
    if jb is None:
        return None
    try:
        return jb.lcut(text)
    except Exception:
        return None


def posseg_cut(text: str):
    """jieba.posseg.cut 词性切词（返回 pair 迭代器）；不可用/异常 → None。"""
    pseg = get_posseg()
    if pseg is None:
        return None
    try:
        return pseg.cut(text)
    except Exception:
        return None


def word_freq(word: str) -> int:
    """jieba 词典内词频（FREQ）；jieba 缺失/异常 → 0（守卫收窄，不阻断）。"""
    dt = get_dt()
    if dt is None:
        return 0
    try:
        return int(dt.FREQ.get(word, 0))
    except Exception:
        return 0


def textrank(text: str, top: int) -> Set[str]:
    """jieba.analyse.textrank 关键词；不可用/异常 → 空集。"""
    analyse = get_analyse()
    if analyse is None:
        return set()
    try:
        return set(analyse.textrank(text, topK=top, withWeight=False) or [])
    except Exception:
        return set()


def extract_tags(text: str, top: int) -> List[str]:
    """jieba.analyse.extract_tags（TF-IDF 关键词，textrank 不可用时的降级）；
    不可用/异常 → 空列表。"""
    analyse = get_analyse()
    if analyse is None:
        return []
    try:
        return list(analyse.extract_tags(text, topK=top) or [])
    except Exception:
        return []


def lazy_pinyin(text: str) -> Optional[List[str]]:
    """pypinyin.lazy_pinyin 主读音；pypinyin 缺失/异常 → None（调用方降级）。"""
    pp = get_pypinyin()
    if pp is None:
        return None
    try:
        return pp.lazy_pinyin(text)
    except Exception:
        return None


# ── 测试钩子 ────────────────────────────────────────────────────────

def reset() -> None:
    """清空全部探测/告警缓存（测试用）：下次调用重新探测。

    同时屏蔽「已探测定格」语义——旧测试通过直接置私有属性模拟缺失依赖，
    统一入口后应优先使用本钩子（或配合 mock），避免依赖私有名字。
    """
    globals()['_JIEBA'] = None
    globals()['_JIEBA_PROBED'] = False
    globals()['_JIEBA_DT'] = None
    globals()['_JIEBA_DT_PROBED'] = False
    globals()['_POSSEG'] = None
    globals()['_POSSEG_PROBED'] = False
    globals()['_ANALYSE'] = None
    globals()['_ANALYSE_PROBED'] = False
    globals()['_PYPINYIN'] = None
    globals()['_PYPINYIN_PROBED'] = False
    globals()['_JIEBA_WARNED'] = False
    globals()['_PYPINYIN_WARNED'] = False


# ── 双模块状态分裂防护：core.jieba_bridge ↔ 顶层 jieba_bridge 合一 ────
import sys as _sys  # noqa: E402

_this = _sys.modules[__name__]
for _alias in ('jieba_bridge', 'core.jieba_bridge'):
    _prev = _sys.modules.get(_alias)
    if _prev is None or _prev is not _this:
        _sys.modules[_alias] = _this
del _sys, _this
