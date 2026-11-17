#!/usr/bin/env python3
"""
scripts/infoseek_core_v2.py — Infoseek v2 统一 API 入口（mod-v2.0.0 新增）

版本维度声明（v1.8.1 治理）：本文件返回体的 'version' 字段（'1.2.0' / '1.0.0'）是
「算法/结果体版本 algo-v」，标识评分算法与结果 schema 的演进，**不是** skill 对外版本
（见 scripts/mcp_tools_common.py:SKILL_VERSION）。下游消费方按 algo-v 读取，字段名与值
保持稳定，不随 skill 版本变动；注释中的 v3.0.0 指流式 yield 协议版本（proto-v），同为独立维度。

设计目标：
1. 把 core/ 各模块统一封装为 v2 API
2. 提供 research() 主入口：端到端调研流程
3. 旧版 anchor_adapter.py 的 v1 API 通过 deprecation shim 兼容

v2 API 列表：
- research(subject, sources=None) → 端到端调研
- score_source(source, subject) → v2 评分
- extract_entities(text) → 实体抽取
- detect_conflicts(sources) → 冲突检测 v2（实体感知）
- render_report(subject, sources) → 报告渲染（领域模板）

兼容策略：
- v1 anchor_adapter.calculate_score() → score_source()
- v1 conflict_detection.detect_conflicts() → detect_conflicts()
- v1 exporter.to_markdown() → render_report(format='md')
"""

import sys
import os
import warnings
from pathlib import Path
from typing import List, Dict, Optional, Any

# v2 core 路径
INFOSEEK_ROOT = Path(os.environ.get('INFOSEEK_ROOT', str(Path(__file__).parent.parent)))
CORE_DIR = INFOSEEK_ROOT / 'core'
sys.path.insert(0, str(CORE_DIR))
sys.path.insert(0, str(INFOSEEK_ROOT))
sys.path.insert(0, str(INFOSEEK_ROOT / 'scripts'))

# G8-apply: 公共入口类型契约守卫（纯 stdlib，scripts/entry_guard.py）
from entry_guard import (require_text, require_mapping, require_sequence, coerce_mapping_list)

from core.ner import extract_entities
from core.entities import get_entities_by_type, entity_count
from core.trust_sources import compute_trust_bonus, get_tier_level
from core.llm_router import llm_call, estimate_cost, list_available_providers
# v1.8.3 §8.4：聚合真源**顶层导入**（用顶层模块名 anchor_score_v2 而非 core.anchor_score_v2，
# 与 anchor_adapter / 守护测试指向同一模块对象，规避「双模块陷阱」导致的状态分裂；
# CORE_DIR 已于上方插入 sys.path）。放顶层另修性能：函数内局部 import 每次调用都触发
# sys.path.insert → 1000 源评分时 sys.path 膨胀至 3000+ 条，find_spec 呈 O(n) 遍历。
from anchor_score_v2 import aggregate_score_v2
# v1.9.0 GA9/GA10：人名消歧 + 跨语言别名桥接真源（core/ 下模块）。
# 顶层模块名导入（与 anchor_score_v2 同理，规避 core./顶层双模块状态分裂）；
# ⚠️ 必须模块对象方式引用（晚绑定），禁 from-import —— §8.13.3 铁律，
# 守护见 tests/test_ga9_person_v190.py / test_ga10_xling_v190.py。
import person_ner as _person_mod
import xling_bridge as _xling_mod


# ═══════════════════════════════════════════════════════════════
# v2 核心 API
# ═══════════════════════════════════════════════════════════════

_PATHS_READY = False


def _ensure_paths() -> None:
    """幂等确保 scripts/ 与 core/ 在 sys.path（v1.8.3 性能修复）。

    根因：`score_source` 每次调用都执行 `sys.path.insert(0, ...)`，实测 300 源评分后
    sys.path 由 9 条膨胀到 910 条 → import 机制 `find_spec` 被调 687,871 次 / 12.15s
    （占 score_source 总耗时 89%）、`_path_join` 343 万次，整体呈 O(n²) 退化
    （perf S1 4.8s→12.6s / S2 58.8s→154.7s / S4 90.0s→227.2s）。
    幂等后 sys.path 恒定，1000 源级联恢复 O(n)。
    """
    global _PATHS_READY
    if _PATHS_READY:
        return
    for _p in (str(INFOSEEK_ROOT / 'scripts'), str(CORE_DIR)):
        if _p not in sys.path:
            sys.path.insert(0, _p)
    _PATHS_READY = True


def _has_llm_endpoint() -> bool:
    """v2.4.3 PATCH (P1-B): 检测当前环境是否配置 LLM endpoint

    沙箱/未配置 LLM 时返回 False，避免 entity_enricher 步骤空跑 ~4s 等待。
    返回 True 时按原 v2.1.0 行为执行 LLM 抽取 + pending 队列。
    """
    try:
        sys.path.insert(0, str(INFOSEEK_ROOT / 'core'))
        from llm_router import LLMRouter
        return bool(LLMRouter().has_available_endpoint())
    except Exception:
        return False


def _bootstrap_persons(subject: str) -> None:
    """v1.9.0 GA9④：人名实体引导（闭合 D2「NER 词典不含人名」）。

    subject 人名检测 → 拼音别名生成 → 动态注册 person 实体族（运行时会话级，
    幂等零文件写入）。注册后 extract_entities / 冲突检测 / 实体图谱可按人名索引
    源文本（含拉丁拼写经注册别名词典命中，如 'Linjian Xiang' → 项林坚）。
    失败静默——不阻断主链路；env 闸 INFOSEEK_PERSON_NER（默认开，person_ner 内判）。
    """
    try:
        _person_mod.bootstrap_subject(subject or '')
    except Exception:
        pass


def _coerce_incoming_score(raw):
    """P1(DEF-08/DEF-09)：入参 score 的类型保护 + 0-1 量纲归一化。

    返回 (base_score, scale_normalized, score_invalid)。
      - bool：标志位而非评分 → 按缺分 0 处理，不参与归一（DEF-08）。
      - int/float（非 bool）：合法数值；NaN/Inf 显式归零，防 NaN 向下游传播；
        0 < score <= 1 视作比例分 ×100（P0-OPEN-04），>1 / <0 / =0 原样保留
        （1.0001 视为百分制满分附近，不强制钳制，原样透传——见 open 项口径）。
      - 数值字符串：'72'→72、'0.72'→72（先转 float 再走同一归一判定）。
      - None / 非数值字符串 / 其它类型：不击穿，归 0 并标记 score_invalid，
        交由既有 semantic_fallback / empty 链按缺分处理（DEF-09）。
    """
    # bool 必须先于 int 判断（bool 是 int 子类）
    if isinstance(raw, bool):
        return 0, False, False  # 标志位而非评分 → 缺分 0，受控类型不算非法（DEF-08）
    if raw is None:
        return 0, False, False
    val = raw
    if isinstance(raw, str):
        try:
            val = float(raw.strip())
        except (TypeError, ValueError, AttributeError):
            return 0, False, True
    if not isinstance(val, (int, float)):
        return 0, False, True
    val = float(val)
    # NaN/Inf：非有限值不可作为评分，归零防传播
    if val != val or val in (float('inf'), float('-inf')):
        return 0, False, True
    if 0 < val <= 1:
        return round(val * 100, 2), True, False
    return val, False, False


def score_source(source: Dict, subject: str, with_domain: bool = True,
                 prefer_kb: bool = None, days_since_published: int = None,
                 domain_profile: dict = None) -> Dict:
    """v2 评分（兼容入口 / 编排层）；v1.8.3 起聚合环节委托 `aggregate_score_v2`

    **职责边界（§8.4 三链路口径一致性）**
      链B（本函数）  = base 取值 + 领域探测 + 信任/KB 加权取值 → 聚合**委托**链A 真源
      链A（`core.anchor_score_v2.compute_final_score_v2`）= 唯一完整评分口径（四维 base）
    两链共用 `aggregate_score_v2` → 复活标志 / 时间衰减 / 分类阈值 / 100 分封顶口径恒等。
    历史分叉（v1.8.3 前）：本函数自算 `min(base + trust_bonus, 100)`，缺复活标志、
    **缺时间衰减环节**、分类阈值各自硬编码 → 实测 400 天陈旧源链A 38.7(❌噪声) vs
    链B 70.7(🟢核心)，属分类翻转级分叉；现已闭合。

    **base 三态入口**（v1.0.1 P0-1 兜底设计，保留；由 `base_origin` 显式可观测）
      `four_dim`          含 interaction/topic_match/credibility → 走链A calculate_score
      `v1_score`          仅含 score（v1 输入）→ 直接采用
      `semantic_fallback` 三者皆缺但有文本 → max(jaccard, containment×0.8) 兜底
      `empty`             全空 → 0
    注：链B base 与链A 四维 base 是**有意的入口差异**（链B 需兼容 v1 输入与真实搜索源），
    非口径分叉；分叉的定义是「同一 base 经不同聚合公式得不同 final」，该分叉已消除。

    参数:
        source: {url, platform, score, title, snippet, ...}
        subject: 调研主题
        with_domain: 是否自动应用领域加权
        prefer_kb: 多域交集场景（None → 由 detect_domain 自动判定）
        days_since_published: 发布距今天数（v1.8.3 新增，补齐时间衰减）。
            None（默认）→ 读 source['days_since_published']，缺省 0（抓取层当前不注入
            该字段 → 默认行为与 v1.8.2 完全一致，零回归）。
        domain_profile: 领域 profile（v1.8.3 新增）。显式传入时 `kb_intersect_bonus`
            走双参口径（profile 的 intersect_boost 声明生效）；默认 None → 单参默认基准，
            与 v1.7.2 既有契约（prefer_kb 多 KB +12）数值兼容。

    返回:
        {
            'final_score': 0-100,        # 聚合真源产出
            'base_score': 0-100,
            'base_origin': str,          # base 来源（v1.8.3 新增，可观测）
            'tier': 1-4,                 # trust_sources.get_tier_level 唯一真源
            'trust_bonus': 0-42,         # = trust_bonus_base + kb_bonus（字段归属沿用 v1.7.2 契约）
            'trust_bonus_base': 0-30,    # 纯信任源加权（v1.8.3 拆分，与链A trust_bonus 同口径）
            'kb_bonus': 0-12,            # KB 交集加权（v1.8.3 拆分，与链A domain_bonus 内 KB 段同源）
            'domain_bonus': 0-20,        # 领域特定信任段（v2.3.2 收口：经聚合真源计入 final）
            'xling_bridge': 0-70,        # 跨语言别名桥接分（v1.9.0 GA10 新增，向后兼容；仅 semantic_fallback 路径非零）
            'after_decay': float,        # 衰减后中间量（v1.8.3 新增，对齐链A）
            'decay_factor': float,       # 衰减因子（v1.8.3 新增）
            'whitelist_triggered': bool, # 复活标志（v1.8.3 新增，对齐链A）
            'classification': '🟢核心' / '🟡潜力' / '❌噪声',
            'version': '1.2.0',          # algo-v：下游契约稳定，不随 skill 版本变动
        }

    **domain_bonus 口径声明（v2.3.2 收口）**：链B 的 `domain_bonus` = 纯领域特定信任段
    `domain_router.trust_source_bonus(source, profile)`，与链A 同源，经 `aggregate_score_v2`
    **计入 final**。KB 交集加分仍在 `trust_bonus`（= trust_bonus_base + kb_bonus），**不进入
    domain_bonus**，故无双重计分。领域段与 KB 段分别取分，组件口径与链A 一致；
    `source['_scoring']` 旁路值不再被采信（防旁路口径与真源分叉）。
    """
    # G8-apply: 类型契约守卫（拒绝 None/list/str 等非映射 → 受控 TypeError，替代 .get 崩溃）
    require_mapping(source, "source")
    # 0) base 三态入口（base_origin 可观测）
    raw_score = source.get('score', 0)
    # P0-OPEN-04 + P1(DEF-08/DEF-09)：入口类型保护 + 量纲归一化。
    # ① 类型保护：旧实现仅 isinstance 数值，字符串脏分（'0.72'）穿透到
    #    下方 `base_score <= 0` 比较直接抛 TypeError，打挂整条评分链（与禁空
    #    骨架目标相悖）。现统一在入口把 score 强转为数值，非法类型不击穿。
    # ② bool 排除（DEF-08）：bool 是 int 子类，True 会命中 (0,1] 被归一为 100；
    #    但布尔更可能是标志位而非评分，故 bool 一律不参与归一、按缺分 0 处理。
    # ③ 量纲归一（P0-OPEN-04）：数值型 0 < score <= 1 → 比例分 ×100；
    #    精确 0 仍为 empty（真实无分），1 归一为 100（边界含入）。
    # ④ NaN/Inf：float() 可解析但比较不命中，归一跳过；NaN 在下游比较恒 False，
    #    归一化/empty 判定均不命中，此处显式归零防 NaN 向下游报告传播。
    base_score, scale_normalized, score_invalid = _coerce_incoming_score(raw_score)
    base_origin = 'v1_score' if base_score else 'empty'
    xling_bridge_score = 0  # v1.9.0 GA10：跨语言桥接分（仅 semantic_fallback 路径产生）

    # 1) 完整四维字段 → 走链A calculate_score（v2 口径）
    if all(k in source for k in ('interaction', 'topic_match', 'credibility')):
        base_origin = 'four_dim'
        try:
            _ensure_paths()
            from anchor_adapter import calculate_score
            v1_result = calculate_score(
                source, subject,
                with_llm_readability=('llm_readability' in source),
                with_semantic=bool(source.get('snippet')),
                semantic_text=source.get('snippet', ''),
                with_domain=with_domain,
            )
            base_score = v1_result.get('after_whitelist', v1_result.get('raw_score', base_score))
        except Exception:
            pass
    elif base_score <= 0:
        # v1.0.1 PATCH (P0-1): 真实搜索源（search_web 等）缺 interaction/topic_match/credibility
        # 三字段时，自动用 标题+摘要 对主题的语义相似度兜底评分，
        # 修复「搜索→评分→报告」主链路断裂（此前全部归 0 → 报告空壳）。
        # v1.0.1 PATCH (P0-1b): 取 max(jaccard, 字符串包含×0.8) ——
        # Jaccard 对短中文主题过严（DeepSeek 相关源仅 14-32 分 <40 门槛），
        # 字符串包含相似度主题词全命中时 100 分，取二者最大值避免误滤。
        try:
            text = ' '.join(filter(None, [
                source.get('title', ''), source.get('snippet', ''), source.get('text', '')
            ]))
            if text:
                _ensure_paths()
                from anchor_adapter import compute_semantic_similarity, _string_containment_similarity
                jaccard = compute_semantic_similarity(text, subject)
                containment = _string_containment_similarity(text, subject)
                base_score = max(jaccard, int(containment * 0.8))
                # v1.9.0 GA10：跨语言别名桥接 —— 中文主题 × 拉丁文正文相似度趋零时，
                # subject 人名拼音别名 / 词典实体拉丁别名词边界命中 → 保底 55（🟡潜力），
                # 英文一手权威源不再因中文 query 被系统性误判 ❌噪声
                # （D1 实锤：§8.11.1 ualberta.ca 官方源仅 9 分）。
                # 仅抬升底线的 max 语义——不改变任何既有命中路径（零回归契约）；
                # env 闸 INFOSEEK_XLING_BRIDGE（默认开）。
                # ⚠️ _xling_mod 模块对象属性访问（晚绑定），禁 from-import（§8.13.3 铁律）。
                try:
                    xling_bridge_score = _xling_mod.bridge_score(text, subject) or 0
                except Exception:
                    xling_bridge_score = 0
                if xling_bridge_score > base_score:
                    base_score = xling_bridge_score
                base_origin = 'semantic_fallback'
        except Exception:
            pass  # 兜底失败则维持 0，不影响主流程

    # 2) 领域探测（prefer_kb 未显式指定时由 detect_domain 判定）
    domain = source.get('domain')
    _prefer_kb = prefer_kb
    if not domain:
        try:
            _ensure_paths()
            from domain_router import detect_domain
            routing = detect_domain(subject)
            domain = routing.get('domain') or 'general'
            if _prefer_kb is None:
                _prefer_kb = bool(routing.get('prefer_kb'))
        except Exception:
            domain = 'general'

    # 3) 信任加权取值（真源 trust_sources，0-30）+ KB 交集加权（单源 domain_router，0-12）
    trust_bonus_base = compute_trust_bonus(source.get('url', ''), domain, source.get('platform', ''))
    kb_bonus = 0
    if _prefer_kb:
        try:
            from domain_router import kb_intersect_bonus
            # v1.8.3：双参口径（domain_profile 显式传入时 intersect_boost 声明生效；
            # None 时与单参等价 → v1.7.2 契约数值不变）
            kb_bonus = kb_intersect_bonus(source, domain_profile)
        except Exception:
            kb_bonus = 0
    # 字段归属沿用 v1.7.2 契约（KB 加分计入 trust_bonus；test_prefer_kb_transfer T8/T14 锁定）
    trust_bonus = trust_bonus_base + kb_bonus
    tier = get_tier_level(source.get('url', ''), domain)

    # 4) 时间衰减入口（v1.8.3 补齐；默认读 source，缺省 0 → 与 v1.8.2 行为一致）
    if days_since_published is None:
        try:
            _days = int(source.get('days_since_published', 0) or 0)
        except (TypeError, ValueError):
            _days = 0
    else:
        try:
            _days = int(days_since_published)
        except (TypeError, ValueError):
            _days = 0

    # 5) 领域特定信任段（收口 v2.3.2：纯领域 trust_source_bonus 经 domain_bonus
    #    进入聚合真源；KB 段已在 trust_bonus，故此处只算领域特定段，防双重计分）
    domain_bonus = 0
    try:
        from domain_router import trust_source_bonus, load_profile
        _profile = domain_profile
        if _profile is None and domain and domain != 'general':
            try:
                _profile = load_profile(domain)
            except Exception:
                _profile = None
        if _profile is not None:
            domain_bonus = int(trust_source_bonus(source, _profile) or 0)
    except Exception:
        domain_bonus = 0

    # 6) 聚合（唯一真源，禁止自算公式）
    try:
        agg = aggregate_score_v2(base_score, days_since_published=_days,
                                 trust_bonus=trust_bonus, domain_bonus=domain_bonus)
        final = agg['final_score']
        classification = agg['classification']
        extra = {'after_decay': agg['after_decay'],
                 'decay_factor': agg['decay_factor'],
                 'whitelist_triggered': agg['whitelist_triggered']}
    except Exception:
        # 降级保底（非常态：core 同仓必然可导入）。**不做平行口径自算**，
        # 仅取最小可用聚合并显式标记 degraded，供守护测试与审计发现。
        warnings.warn('aggregate_score_v2 不可用，score_source 走降级保底聚合',
                      RuntimeWarning, stacklevel=2)
        final = min(base_score + trust_bonus, 100)
        classification = '🟢核心' if final >= 70 else ('🟡潜力' if final >= 40 else '❌噪声')
        extra = {'after_decay': float(base_score), 'decay_factor': 1.0,
                 'whitelist_triggered': base_score >= 90, '_aggregate_degraded': True}

    result = {
        'final_score': final,
        'base_score': base_score,
        'base_origin': base_origin,
        'scale_normalized': scale_normalized,  # P0-OPEN-04：入参 0-1 量纲已 ×100
        'score_invalid': score_invalid,        # P1(DEF-09)：入参脏分（非数值/NaN）标记
        'tier': tier,
        'trust_bonus': trust_bonus,
        'trust_bonus_base': trust_bonus_base,
        'kb_bonus': kb_bonus,
        'domain_bonus': domain_bonus,
        'xling_bridge': xling_bridge_score,  # v1.9.0 GA10（新增字段，向后兼容）
        'classification': classification,
        'version': '1.2.0',
    }
    result.update(extra)
    return result


def score_sources_batch_async(sources: List[Dict], subject: str,
                              with_domain: bool = True,
                              prefer_kb: bool = None) -> List[Dict]:
    """v2.5.0 MINOR 新增：批量异步评分（asyncio.gather 并行 8 维度）

    benchmark 结果（100 源 × 8 维度 × 2-4ms 模拟 IO）：
    - 串行：2700ms
    - asyncio run_in_executor per-source：569ms（4.7x）
    - asyncio gather all 800 tasks：**351ms（7.7x）** ✅
    - multiprocessing：pickle 失败（局部函数不可序列化）

    跨源一次性 gather 所有 800 个评分任务 → 启动开销最小 + 并行度最大

    注：score_source 实际很快（<1ms，模块已单例化），asyncio 启动开销占主导
    在 score_source 仍 <10ms 的场景下，本函数只对 IO 密集维度（如网络）有效。
    """
    import asyncio
    # 同步入口：在无 running loop 时用 asyncio.run；否则新建 loop
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # 无运行中的 loop，同步执行
        try:
            return asyncio.run(_gather_all(sources, subject, with_domain, prefer_kb))
        except RuntimeError:
            # 沙箱环境可能没正常 event loop → 退化为串行
            return [score_source(s, subject, with_domain, prefer_kb) for s in sources]
    # 有 running loop（罕见：用户在 async 上下文调同步入口）
    # 用 ThreadPoolExecutor 跑异步
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(
            asyncio.run, _gather_all(sources, subject, with_domain, prefer_kb)
        )
        return future.result()


async def _gather_all(sources, subject, with_domain, prefer_kb=None):
    import asyncio
    loop = asyncio.get_event_loop()
    tasks = [
        loop.run_in_executor(None, score_source, src, subject, with_domain, prefer_kb)
        for src in sources
    ]
    return await asyncio.gather(*tasks)


def detect_conflicts(sources: List[Dict], subject: str = '') -> Dict:
    """v2 冲突检测（实体感知）

    在 v1.8.0 conflict_detection 基础上增加：
    1. 实体感知：先抽实体，按实体分组冲突
    2. 实体相似度：跨语言实体匹配（如 OpenAI ↔ openai ↔ OPENAI）
    """
    # G8-apply: 类型契约守卫（拒绝非序列/str → 受控 TypeError，替代 dict 迭代出键后 .get 崩溃）
    require_sequence(sources, "sources")
    # v1.9.0 GA9④：人名实体引导（直接调用冲突检测工具时也保证 person 实体族可见）
    _bootstrap_persons(subject)

    # 1) 调用 v1 conflict_detection.detect_conflicts()
    sys.path.insert(0, str(INFOSEEK_ROOT / 'scripts'))
    try:
        from conflict_detection import detect_conflicts as v1_detect
        v1_result = v1_detect(sources, subject=subject)
    except ImportError:
        return {'error': 'conflict_detection 未找到', 'conflicts': []}

    # 2) v2 增强：实体感知
    entity_conflicts = []
    for source in sources:
        text = source.get('text', '') or source.get('snippet', '')
        entities = extract_entities(text)
        if entities:
            source['_v2_entities'] = [e['entity_name'] for e in entities]

    # 3) 跨源实体覆盖度对比
    all_entities = set()
    for source in sources:
        for e in source.get('_v2_entities', []):
            all_entities.add(e)

    if all_entities:
        coverage_data = []
        for source in sources:
            src_entities = set(source.get('_v2_entities', []))
            coverage = len(src_entities & all_entities) / len(all_entities) if all_entities else 0
            coverage_data.append({
                'source': source.get('title', 'Untitled'),
                'coverage': round(coverage * 100, 1),
                'entities_mentioned': list(src_entities),
            })

        v1_result['v2_entity_coverage'] = coverage_data

    v1_result['version'] = '1.0.0'
    return v1_result


def render_report(subject: str, sources: List[Dict],
                  format: str = 'md',
                  domain: Optional[str] = None,
                  prefer_kb: bool = None) -> str:
    """v2 报告渲染（调用 domain_orchestrator 或 exporter）

    参数:
        subject: 调研主题
        sources: 来源列表
        format: 'md' / 'json' / 'csv' / 'traced_md' / ...
        domain: 手动指定领域

    返回:
        格式化报告字符串
    """
    # G8-apply: 元素级坏源隔离（[None] 等坏元素跳过 + warning，保留整链存活）
    sources = coerce_mapping_list(sources, "sources", skip_bad=True)
    sys.path.insert(0, str(INFOSEEK_ROOT / 'scripts'))
    try:
        from domain_orchestrator import DomainOrchestrator
        from exporter import FORMATTERS
    except ImportError:
        return f'[error] domain_orchestrator 或 exporter 未找到'

    orchestrator = DomainOrchestrator()

    # 先用 v2 scoring
    scored_sources = []
    for s in sources:
        v2_score = score_source(s, subject, prefer_kb=prefer_kb)
        s_copy = dict(s)
        s_copy['score'] = v2_score['final_score']
        s_copy['_v2'] = v2_score
        scored_sources.append(s_copy)

    # 用 domain_orchestrator 渲染
    result = orchestrator.render_report(subject, scored_sources, domain_override=domain)

    if format == 'md':
        return result['markdown']
    elif format in FORMATTERS:
        # 构造报告 dict 给 exporter
        report_dict = {
            'subject': subject,
            'domain': result.get('domain'),
            'summary': f'{subject} 调研（{len(scored_sources)} 来源）',
            'anchors': scored_sources,
        }
        return FORMATTERS[format](report_dict)
    else:
        return f'[error] 未知 format: {format}'


def research(subject: str,
             sources: Optional[List[Dict]] = None,
             domain: Optional[str] = None,
             with_llm: bool = False,
             output_format: str = 'md',
             lite: bool = False,
             prefer_kb: bool = None) -> Dict[str, Any]:
    """v2 端到端调研主入口

    完整流程：
    1. 检测领域
    2. 评分（v2 + 信任源）
    3. 冲突检测（v2 实体感知）
    4. 报告渲染
    5. 可选 LLM 增强
    6. v2.1.0 自沉淀（enricher）
    7. v2.1.1 Wikidata 验证
    8. v2.2.0 实体索引
    9. v2.3.0 实体图谱
    10. v2.3.0 冲突检测 v3 + 矛盾评分
    11. v2.3.0 实体画像
    12. v2.4.0 热度预测
    13. v2.4.0 实体轨迹

    参数:
        subject: 调研主题
        sources: 来源列表（如 None 则仅返回空报告骨架）
        domain: 手动指定领域
        with_llm: 是否调用 LLM 增强
        output_format: 输出格式
        lite: v2.4.1 PATCH — 轻量模式（DEF-E 性能优化）
              跳过耗时步骤：wikidata 验证、traced_export dot 渲染、heat 排名、trajectory
              适用：≥10 源时性能要求 <1s；纯结构化提取场景
              默认 False（保持向后兼容）

    返回:
        {
            'subject': subject,
            'domain': 'tech-research',
            'scored_sources': [...],
            'conflicts': [...],
            'report': str,
            'llm_insights': str (if with_llm),
            'version': '1.2.0',
        }
    """
    sources = sources or []

    # v1.9.0 GA9④：人名实体引导（幂等；下游 NER/冲突/图谱可见）
    _bootstrap_persons(subject)

    # v2.5.3 PATCH: 在 async 上下文调用 research() 时发 deprecation warning，
    # 建议改用 async_research() 避免阻塞 event loop（不破坏既有调用）
    try:
        import asyncio
        loop = asyncio.get_running_loop()
        import warnings
        warnings.warn(
            "research() 在 async 上下文中可能阻塞 event loop；"
            "建议改用 await async_research(...)。",
            DeprecationWarning, stacklevel=2,
        )
    except RuntimeError:
        pass  # 无运行中的 loop，正常执行

    # 1) 评分
    scored = [score_source(s, subject, prefer_kb=prefer_kb) for s in sources]

    # 2) 冲突检测
    conflicts = detect_conflicts(sources, subject=subject)

    # 3) 报告渲染
    report = render_report(subject, sources, format=output_format, domain=domain,
                           prefer_kb=prefer_kb)

    result = {
        'subject': subject,
        'scored_sources': scored,
        'conflicts': conflicts.get('conflicts', []),
        'report': report,
        'version': '1.2.0',
    }

    # 4) LLM 增强（可选）
    if with_llm:
        llm_prompt = f"调研主题: {subject}\n请给出关键洞察和后续建议。"
        llm_result = llm_call(llm_prompt, max_tokens=200)
        result['llm_insights'] = llm_result['content']
        result['llm_provider'] = llm_result['provider']
        result['llm_cost'] = llm_result['cost_estimate']

    # 5) v2.1.0 自沉淀触发（LLM 抽取 + 入 pending 队列）
    # v2.4.3 PATCH (P1-B): 默认跳过无 LLM endpoint 场景（沙箱/生产环境均省 ~4s）
    if sources and _has_llm_endpoint():
        try:
            sys.path.insert(0, str(INFOSEEK_ROOT / 'core'))
            from entity_enricher import EntityEnricher

            enricher = EntityEnricher()
            all_text = ' '.join(
                s.get('text', '') or s.get('snippet', '') or s.get('title', '')
                for s in sources
            )
            candidates = enricher.extract_candidates(all_text)
            suggestions = enricher.suggest_additions(candidates)
            persist_result = enricher.persist_suggestions(suggestions, auto_confirm=False)
            result['enrichment'] = {
                'candidates_extracted': len(candidates),
                'new_suggestions': len(suggestions),
                'auto_added': persist_result['auto_added'],
                'queued_for_review': persist_result['queued'],
                'pending_entities': enricher.get_pending(),
            }
        except Exception as e:
            result['enrichment'] = {'error': str(e)}
    elif sources:
        result['enrichment'] = {'skipped': 'no_llm_endpoint'}

    # 6) v2.1.1 集成：Wikidata 验证（网络可用时）
    # v2.4.1 PATCH (DEF-E): lite 模式跳过网络调用
    if not lite:
        try:
            sys.path.insert(0, str(INFOSEEK_ROOT / 'core'))
            from wikidata_sync import WikidataSync
            sync = WikidataSync()
            # 仅检查 subject 在 Wikidata 是否存在（轻量验证）
            exists = sync.verify_existence(subject)
            result['wikidata_verified'] = {
                'subject': subject,
                'exists': exists,
                'available': True,
            }
        except Exception as e:
            result['wikidata_verified'] = {'available': False, 'error': str(e)}
    else:
        result['wikidata_verified'] = {'skipped': 'lite_mode'}

    # 7) v2.2.0 集成：报告实体索引（实体图谱）
    try:
        sys.path.insert(0, str(INFOSEEK_ROOT / 'core'))
        from ner import extract_entities
        all_text = ' '.join(
            s.get('text', '') or s.get('snippet', '') or s.get('title', '')
            for s in sources
        )
        raw_entities = extract_entities(all_text)
        # 聚合去重：同名实体统计命中数 + 匹配方式
        entity_map = {}
        for e in raw_entities:
            name = e['entity_name']
            if name not in entity_map:
                entity_map[name] = {
                    'entity_name': name,
                    'entity_type': e.get('entity_type', 'UNKNOWN'),
                    'hit_count': 0,
                    'match_methods': [],
                }
            entity_map[name]['hit_count'] += 1
            method = e.get('match_method', 'unknown')
            if method not in entity_map[name]['match_methods']:
                entity_map[name]['match_methods'].append(method)
        result['entity_index'] = sorted(
            entity_map.values(),
            key=lambda x: (-x['hit_count'], x['entity_name']),
        )
    except Exception as e:
        result['entity_index'] = {'error': str(e)}

    # 8) v2.3.0 集成：实体图谱（共现关系）
    # v2.4.1 PATCH (DEF-E): lite 模式跳过 traced_export dot 渲染（>10 源时极慢）
    try:
        sys.path.insert(0, str(INFOSEEK_ROOT / 'core'))
        from entity_graph import EntityGraph, set_global_graph
        graph = EntityGraph()
        graph.build_from_sources(sources)
        set_global_graph(graph)  # v2.5.0 G3: 注册全局图谱（召回扩展复用）
        result['entity_graph'] = graph.to_dict()
        if not lite:
            try:
                from traced_export import build_traced, to_dot
                traced = build_traced(sources, result['entity_graph'])
                # 节点阈值：>500 不画 dot（避免 Graphviz 渲染超时）
                if len(traced.get('nodes', [])) > 500:
                    traced['dot'] = f'# skipped: {len(traced["nodes"])} nodes exceed 500 threshold'
                else:
                    traced['dot'] = to_dot(traced)
                result['traced_export'] = traced
            except Exception as te:
                result['traced_export'] = {'error': str(te)}
        else:
            result['traced_export'] = {'skipped': 'lite_mode'}
    except Exception as e:
        result['entity_graph'] = {'error': str(e)}

    # 9) v2.3.0 集成：冲突检测 v3（跨别名归并）
    try:
        sys.path.insert(0, str(INFOSEEK_ROOT / 'core'))
        from conflict_v3 import detect_conflicts_v3
        v3_result = detect_conflicts_v3(sources, subject=subject)
        result['conflicts'] = v3_result.get('conflicts', result.get('conflicts', []))
        result['conflict_v3'] = {
            'version': v3_result.get('version'),
            'raw_claims': v3_result.get('raw_claims'),
            'total': len(v3_result.get('conflicts', [])),
            'aliases_involved': v3_result.get('aliases_involved', {}),
            'live_alerts': v3_result.get('live_alerts', []),  # v2.3.1: 增量实时告警
            'cross_session_summary': v3_result.get('cross_session_summary', {}),  # v2.4.0
        }
        # v2.4.0: 语义矛盾打分（给每对冲突附 semantic_score）
        try:
            from contradiction_scorer import score_contradiction_hybrid
            enriched = []
            _llm_used_n = 0
            verdict_counts = {'conflict': 0, 'no_conflict': 0,
                              'not_assessable': 0}
            time_cov_counts = {'both_timed': 0, 'partial': 0, 'neither': 0}
            for c in result['conflicts']:
                sc = score_contradiction_hybrid(c['claim_a'], c['claim_b'])
                if sc.get('llm_used'):
                    _llm_used_n += 1
                c2 = dict(c)
                c2['semantic_score'] = sc['score']
                c2['severity'] = sc['severity']  # 用语义评覆盖中等/高严重度
                c2['verdict'] = sc.get('verdict')       # P0-OPEN-06
                c2['time_coverage'] = sc.get('time_coverage')
                # v2.1.2（事件槽批次）：与异步路字段穿透对齐
                c2['keyed_score'] = sc.get('keyed_score')
                c2['conflict_slots'] = sc.get('conflict_slots')
                c2['period_adjudication'] = sc.get('period_adjudication')
                # v2.2.0：三元事件身份 + 多期间裁决 + LLM 时间抑制 字段全透传
                for _fk in ('time_mode', 'event_count_a', 'event_count_b',
                            'event_time_score', 'event_pairs',
                            'event_disjoint_slots', 'event_overlap_slots',
                            'event_slot_keys', 'period_pair_details',
                            'period_disjoint_slots', 'period_overlap_slots',
                            'llm_time_suppressed', 'llm_time_suppressed_slots',
                            'scorer_mode', 'llm_used', 'llm_error'):
                    if _fk in sc:
                        c2[_fk] = sc.get(_fk)
                verdict_counts[sc.get('verdict', 'not_assessable')] = \
                    verdict_counts.get(sc.get('verdict', 'not_assessable'), 0) + 1
                time_cov_counts[sc.get('time_coverage', 'neither')] = \
                    time_cov_counts.get(sc.get('time_coverage', 'neither'), 0) + 1
                enriched.append(c2)
            result['conflicts'] = enriched
            _scored = len(enriched)
            # P0-OPEN-06：区分"真冲突 / 无冲突 / 未评估"，并给时间槽覆盖率。
            # assessed = conflict + no_conflict（有可对拍事实槽）；not_assessable 为未评估。
            _assessed = verdict_counts['conflict'] + verdict_counts['no_conflict']
            result['contradiction_scoring'] = {
                'enabled': True,
                'version': '1.3.0',
                'scored': _scored,
                # method 随 hybrid 状态动态化：env INFOSEEK_CONTRADICTION_LLM
                # 开启且实际命中 LLM 槽时标 llm_hybrid，否则纯本地键控
                'method': 'llm_hybrid' if _llm_used_n else 'local',
                'llm_augmented': _llm_used_n,
                'verdict_counts': verdict_counts,
                'time_coverage_counts': time_cov_counts,
                # 可评估率：有可对拍事实槽的对比对占比（其余为未评估，非"无冲突"）
                'assessment_coverage': round(_assessed / _scored, 3) if _scored else 0.0,
            }
        except Exception as e:
            result['contradiction_scoring'] = {'enabled': False, 'error': str(e)}
    except Exception as e:
        result['conflict_v3'] = {'error': str(e)}

    # 10) v2.3.0 集成：实体画像（长期知识库积累）
    try:
        sys.path.insert(0, str(INFOSEEK_ROOT / 'core'))
        from entity_profile import EntityProfile
        profiler = EntityProfile()
        result['entity_profiles'] = profiler.update_profiles(
            sources,
            result.get('entity_index', []) if isinstance(result.get('entity_index'), list) else [],
            conflicts=result.get('conflicts', []),
        )
    except Exception as e:
        result['entity_profiles'] = {'error': str(e)}

    # 10.1) v2.4.0: 实体热度预测 Top 10（轻量，可选调用失败不阻断）
    # v2.4.1 PATCH (DEF-E): lite 模式跳过（全实体 ranking 146 个代价高）
    if not lite:
        try:
            sys.path.insert(0, str(INFOSEEK_ROOT / 'core'))
            from entity_heat import get_heat_ranking
            result['heat_ranking'] = get_heat_ranking(top_n=10)
        except Exception as e:
            result['heat_ranking'] = {'error': str(e)}
    else:
        result['heat_ranking'] = {'skipped': 'lite_mode'}

    # 10.2) v2.4.0: 实体轨迹（仅取 entity_index 命中 Top5，避免全量开销）
    # v2.4.1 PATCH (DEF-E): lite 模式跳过（5 次 trace_entity 每个 ~100ms）
    if not lite:
        try:
            sys.path.insert(0, str(INFOSEEK_ROOT / 'core'))
            from entity_trajectory import trace_entity
            ent_idx = result.get('entity_index', [])
            if isinstance(ent_idx, list) and ent_idx:
                top_names = sorted(
                    [e.get('entity_name') for e in ent_idx if e.get('entity_name')],
                    key=lambda n: -next((x.get('hit_count', 0) for x in ent_idx if x.get('entity_name') == n), 0),
                )[:5]
                result['trajectory_top5'] = [trace_entity(n, days_back=90) for n in top_names]
            else:
                result['trajectory_top5'] = []
        except Exception as e:
            result['trajectory_top5'] = {'error': str(e)}
    else:
        result['trajectory_top5'] = {'skipped': 'lite_mode'}

    # v1.0.0: 标识版本 + 内部使用 streaming_research 路径
    result['version'] = '1.0.0'
    result['streaming_mode'] = False  # 同步包装（v1.0.0 仍走内部 12 步骤）
    return result


async def async_research(subject: str,
                        sources: Optional[List[Dict]] = None,
                        domain: Optional[str] = None,
                        output_format: str = 'md',
                        lite: bool = False,
                        prefer_kb: bool = None) -> Dict[str, Any]:
    """v2.5.0 MINOR 新增；v2.5.2 PATCH: 深度异步化

    v2.5.0：评分 + wikidata 异步，其余 6 步骤走同步
    v2.5.2：5 个 IO 密集步骤（score / wikidata / entity_graph / conflict_v3 / entity_profile）
              并发 asyncio.create_task + gather；纯计算步骤（render_report / 分类）放最后同步

    benchmark（沙箱 10 源 lite）：v2.5.0 ~2080ms → v2.5.2 目标 <1500ms

    用法：
        res = asyncio.run(async_research('AI', sources, lite=True))
    """
    import asyncio
    sources = sources or []

    # v1.9.0 GA9④：人名实体引导（幂等；下游 NER/冲突/图谱可见）
    _bootstrap_persons(subject)

    # 任务调度：5 个 IO 密集步骤并发
    tasks = {}

    # 1+2: 异步批量评分（已 v2.5.0 实现）
    if sources:
        tasks['scored'] = asyncio.create_task(
            asyncio.to_thread(score_sources_batch_async, sources, subject, True, prefer_kb)
        )
    else:
        tasks['scored'] = asyncio.create_task(asyncio.sleep(0, result=[]))

    # 6: 异步 Wikidata（已 v2.5.0 实现）
    if not lite and sources:
        async def _wikidata():
            try:
                sys.path.insert(0, str(INFOSEEK_ROOT / 'core'))
                from wikidata_sync import WikidataSync
                sync = WikidataSync()
                url_entities = []
                for s in sources[:10]:
                    txt = s.get('snippet', '') or s.get('title', '')
                    url_entities.append(txt[:20] if txt else subject)
                verify_results = await sync.verify_batch_async([subject] + url_entities)
                return {
                    'subject_verified': verify_results.get(subject, False),
                    'sources_verified': sum(1 for v in verify_results.values() if v),
                    'available': True,
                }
            except Exception as e:
                return {'available': False, 'error': str(e)}
        tasks['wikidata'] = asyncio.create_task(_wikidata())
    else:
        async def _wikidata_skip():
            return {'skipped': 'lite_mode'}
        tasks['wikidata'] = asyncio.create_task(_wikidata_skip())

    # 8: 异步 entity_graph + traced_export（v2.5.4 PATCH: 补回 traced_export）
    if sources and not lite:
        async def _entity_graph():
            try:
                from entity_graph import EntityGraph
                from traced_export import build_traced, to_dot
                g = EntityGraph()
                eg = await asyncio.to_thread(g.build_from_sources, sources)
                set_global_graph(g)  # v2.5.0 G3: 注册全局图谱（召回扩展复用）
                # v2.5.4 PATCH: traced_export 缺失导致 v2.5.2 输出与 research() 不一致，
                # 现补回（lite 模式也可保留用于诊断）
                try:
                    traced = build_traced(sources, eg)
                    if len(traced.get('nodes', [])) > 500:
                        traced['dot'] = f'# skipped: {len(traced["nodes"])} nodes exceed 500'
                    else:
                        traced['dot'] = to_dot(traced)
                except Exception:
                    traced = {'error': 'traced_export failed'}
                return {'entity_graph': eg, 'traced_export': traced}
            except Exception as e:
                return {'error': str(e)}
        tasks['entity_graph'] = asyncio.create_task(_entity_graph())
    else:
        async def _eg_skip():
            return {'skipped': 'lite_mode'}
        tasks['entity_graph'] = asyncio.create_task(_eg_skip())

    # 9: 异步 conflict_v3 + semantic_score（v2.5.2 新增）
    if sources:
        async def _conflict_v3():
            try:
                from conflict_v3 import detect_conflicts_v3
                from contradiction_scorer import score_contradiction_hybrid
                v3 = await asyncio.to_thread(detect_conflicts_v3, sources, subject)
                enriched = []
                _llm_used_n = 0
                for c in v3.get('conflicts', []):
                    # hybrid 内 LLM 为同步阻塞调用，整体放 to_thread 避免阻塞事件循环
                    sc = await asyncio.to_thread(
                        score_contradiction_hybrid, c['claim_a'], c['claim_b'])
                    if sc.get('llm_used'):
                        _llm_used_n += 1
                    c2 = dict(c)
                    c2['semantic_score'] = sc['score']
                    c2['severity'] = sc['severity']
                    # v2.1.2（事件槽批次）：补齐与同步路 research 一致的字段穿透
                    c2['verdict'] = sc.get('verdict')
                    c2['time_coverage'] = sc.get('time_coverage')
                    c2['keyed_score'] = sc.get('keyed_score')
                    c2['conflict_slots'] = sc.get('conflict_slots')
                    c2['period_adjudication'] = sc.get('period_adjudication')
                    # v2.2.0：三元事件身份 + 多期间裁决 + LLM 时间抑制 字段全透传
                    for _fk in ('time_mode', 'event_count_a', 'event_count_b',
                                'event_time_score', 'event_pairs',
                                'event_disjoint_slots', 'event_overlap_slots',
                                'event_slot_keys', 'period_pair_details',
                                'period_disjoint_slots', 'period_overlap_slots',
                                'llm_time_suppressed', 'llm_time_suppressed_slots',
                                'scorer_mode', 'llm_used', 'llm_error'):
                        if _fk in sc:
                            c2[_fk] = sc.get(_fk)
                    enriched.append(c2)
                return {
                    'conflicts': enriched,
                    'conflict_v3': {
                        'version': v3.get('version'),
                        'raw_claims': v3.get('raw_claims'),
                        'total': len(enriched),
                        'aliases_involved': v3.get('aliases_involved', {}),
                        'live_alerts': v3.get('live_alerts', []),
                        'cross_session_summary': v3.get('cross_session_summary', {}),
                    },
                    'contradiction_scoring': {
                        'enabled': True,
                        'version': '1.2.0',
                        'scored': len(enriched),
                        'method': 'llm_hybrid' if _llm_used_n else 'local',
                        'llm_augmented': _llm_used_n,
                    },
                }
            except Exception as e:
                return {'error': str(e)}
        tasks['conflict'] = asyncio.create_task(_conflict_v3())
    else:
        async def _c_skip():
            return {'conflicts': [], 'conflict_v3': {'total': 0}}
        tasks['conflict'] = asyncio.create_task(_c_skip())

    # 10: 异步 entity_profile + heat_ranking + trajectory（v2.5.2 新增合并）
    if sources and not lite:
        async def _profile_heat_traj():
            try:
                from entity_profile import EntityProfile
                profiler = EntityProfile()
                # entity_index 来自 entity_graph 输出
                # 先用简化版：直接基于 sources 跑
                ei_result = await asyncio.to_thread(profiler.update_profiles, sources, [])
                from entity_heat import get_heat_ranking
                heat_ranking = await asyncio.to_thread(get_heat_ranking, 10)
                from entity_trajectory import trace_entity
                # trajectory_top5 需要 entity_index，此处用 sources 主体（兜底）
                traj = []
                for s in sources[:5]:
                    title = s.get('title', '')[:20]
                    if title:
                        traj.append(await asyncio.to_thread(trace_entity, title, 90))
                return {
                    'entity_profiles': ei_result,
                    'heat_ranking': heat_ranking,
                    'trajectory_top5': traj,
                }
            except Exception as e:
                return {'error': str(e)}
        tasks['profile_heat_traj'] = asyncio.create_task(_profile_heat_traj())
    else:
        async def _p_skip():
            return {
                'entity_profiles': {'skipped': 'lite_mode'},
                'heat_ranking': {'skipped': 'lite_mode'},
                'trajectory_top5': {'skipped': 'lite_mode'},
            }
        tasks['profile_heat_traj'] = asyncio.create_task(_p_skip())

    # 等待所有任务完成（v2.5.2 深度异步核心）
    results = await asyncio.gather(*tasks.values(), return_exceptions=True)
    task_results = dict(zip(tasks.keys(), results))

    # 异常处理
    for k, v in task_results.items():
        if isinstance(v, Exception):
            task_results[k] = {'error': str(v)}

    # 同步步骤（无 IO / 纯计算）
    scored = task_results.get('scored', [])
    wikidata_verified = task_results.get('wikidata', {'skipped': 'lite_mode'})
    eg_combined = task_results.get('entity_graph', {'skipped': 'lite_mode'})
    if isinstance(eg_combined, dict) and 'entity_graph' in eg_combined:
        entity_graph = eg_combined.get('entity_graph', {})
        traced_export = eg_combined.get('traced_export', {})
    else:
        entity_graph = eg_combined
        traced_export = {'skipped': 'lite_mode'}
    conflict_data = task_results.get('conflict', {'conflicts': [], 'conflict_v3': {'total': 0}})
    profile_data = task_results.get('profile_heat_traj', {})

    # render_report 同步（v2.5.2 不深度异步化）
    try:
        report = render_report(subject, sources, format=output_format, domain=domain,
                               prefer_kb=prefer_kb)
    except Exception as e:
        report = f'[error] {e}'

    # entity_index 跨源合并（v2.5.4 PATCH: 修复 v2.5.2 简化为每源独立的 bug）
    from ner import extract_entities
    try:
        ei_raw = []
        for s in sources:
            txt = ' '.join([
                s.get('text', '') or s.get('snippet', '') or s.get('title', ''),
                s.get('title', ''),
            ])[:200]
            ei_raw.extend(extract_entities(txt))
        # 聚合去重（与 research() 步骤 7 逻辑一致）
        entity_index = []
        entity_map = {}
        for e in ei_raw:
            name = e['entity_name']
            if name not in entity_map:
                entity_map[name] = {
                    'entity_name': name,
                    'entity_type': e.get('entity_type', 'UNKNOWN'),
                    'hit_count': 0,
                    'match_methods': [],
                }
            entity_map[name]['hit_count'] += 1
            method = e.get('match_method', 'unknown')
            if method not in entity_map[name]['match_methods']:
                entity_map[name]['match_methods'].append(method)
        entity_index = sorted(
            entity_map.values(),
            key=lambda x: (-x['hit_count'], x['entity_name']),
        )
    except Exception:
        entity_index = []

    return {
        'subject': subject,
        'domain': domain,
        'scored_sources': scored,
        'conflicts': conflict_data.get('conflicts', []),
        'report': report,
        'entity_index': entity_index,
        'entity_graph': entity_graph,
        'traced_export': traced_export,
        'conflict_v3': conflict_data.get('conflict_v3', {'total': 0}),
        'contradiction_scoring': conflict_data.get('contradiction_scoring', {'enabled': False}),
        'wikidata_verified': wikidata_verified,
        'entity_profiles': profile_data.get('entity_profiles', {}),
        'heat_ranking': profile_data.get('heat_ranking', []),
        'trajectory_top5': profile_data.get('trajectory_top5', []),
        'version': '1.2.0',
        'async_mode': True,
        'async_version': '2.5.2',
        'lite': lite,
    }


# v2.6.2 PATCH: lite_research 独立 API（async_research lite=True 的便捷别名）
async def lite_research(subject: str,
                      sources: Optional[List[Dict]] = None,
                      domain: Optional[str] = None) -> Dict[str, Any]:
    """v2.6.2 新增：lite 异步研究便捷入口

    等价于 asyncio.run(async_research(subject, sources, domain, lite=True))，
    但参数更少，更易调用。

    用法：
        res = asyncio.run(lite_research('AI', sources))
    """
    return await async_research(subject, sources=sources, domain=domain, lite=True)


# v3.0.0 GA: streaming research（v3.0.0-dev Sprint 1 引入，rc1 冻结协议，v3.0.0 GA 正式纳入）
async def streaming_research(subject: str,
                            sources: Optional[List[Dict]] = None,
                            domain: Optional[str] = None,
                            output_format: str = 'md',
                            lite: bool = False,
                            prefer_kb: bool = None) -> 'AsyncIterator[Dict]':
    """v3.0.0 GA: 流式研究（AsyncIterator，v3.0.0-dev Sprint 1 引入，rc1 冻结协议）

    yield 顺序（每步独立 yield dict）:
    1. score_complete：scored_sources
    2. wikidata_complete：wikidata_verified
    3. entity_graph_complete：entity_graph + traced_export
    4. conflict_complete：conflicts + conflict_v3
    5. profile_complete：entity_profiles
    6. trajectory_complete：heat_ranking + trajectory_top5
    7. report_complete：report

    适用：
    - MCP 工具调用：first yield <500ms 即可见部分结果
    - Web SSE 流式响应
    - 大模型工具调用（中途中断）

    用法：
        async for partial in streaming_research('AI', sources):
            print(partial['step'], '...')
    """
    import asyncio
    sources = sources or []

    # v1.9.0 GA9④：人名实体引导（幂等；下游 NER/冲突/图谱可见）
    _bootstrap_persons(subject)

    # 任务调度：与 async_research 相同的 5 个 task
    tasks = {}

    # 1+2: 评分
    if sources:
        tasks['scored'] = asyncio.create_task(
            asyncio.to_thread(score_sources_batch_async, sources, subject, True, prefer_kb)
        )
    else:
        async def _empty():
            return []
        tasks['scored'] = asyncio.create_task(_empty())

    # 6: wikidata
    if not lite and sources:
        async def _wikidata():
            try:
                sys.path.insert(0, str(INFOSEEK_ROOT / 'core'))
                from wikidata_sync import WikidataSync
                sync = WikidataSync()
                url_entities = []
                for s in sources[:10]:
                    txt = s.get('snippet', '') or s.get('title', '')
                    url_entities.append(txt[:20] if txt else subject)
                verify_results = await sync.verify_batch_async([subject] + url_entities)
                return {
                    'subject_verified': verify_results.get(subject, False),
                    'sources_verified': sum(1 for v in verify_results.values() if v),
                    'available': True,
                }
            except Exception as e:
                return {'available': False, 'error': str(e)}
        tasks['wikidata'] = asyncio.create_task(_wikidata())
    else:
        async def _wd_skip():
            return {'skipped': 'lite_mode'}
        tasks['wikidata'] = asyncio.create_task(_wd_skip())

    # 8: entity_graph + traced_export
    if sources and not lite:
        async def _entity_graph():
            try:
                from entity_graph import build_from_sources_async
                eg = await build_from_sources_async(sources)
                return {'entity_graph': eg, 'traced_export': eg}  # 简化
            except Exception as e:
                return {'error': str(e)}
        tasks['entity_graph'] = asyncio.create_task(_entity_graph())
    else:
        async def _eg_skip():
            return {'skipped': 'lite_mode'}
        tasks['entity_graph'] = asyncio.create_task(_eg_skip())

    # 9: conflict_v3 + semantic
    if sources:
        async def _conflict():
            try:
                from conflict_v3 import detect_conflicts_v3_async
                from contradiction_scorer import score_contradiction_async
                v3 = await detect_conflicts_v3_async(sources, subject)
                enriched = []
                for c in v3.get('conflicts', []):
                    sc = await score_contradiction_async(c['claim_a'], c['claim_b'])
                    c2 = dict(c)
                    c2['semantic_score'] = sc['score']
                    c2['severity'] = sc['severity']
                    # v2.1.2（事件槽批次）：补齐与同步路 research 一致的字段穿透
                    c2['verdict'] = sc.get('verdict')
                    c2['time_coverage'] = sc.get('time_coverage')
                    c2['keyed_score'] = sc.get('keyed_score')
                    c2['conflict_slots'] = sc.get('conflict_slots')
                    c2['period_adjudication'] = sc.get('period_adjudication')
                    # v2.2.0：三元事件身份 + 多期间裁决 + LLM 时间抑制 字段全透传
                    for _fk in ('time_mode', 'event_count_a', 'event_count_b',
                                'event_time_score', 'event_pairs',
                                'event_disjoint_slots', 'event_overlap_slots',
                                'event_slot_keys', 'period_pair_details',
                                'period_disjoint_slots', 'period_overlap_slots',
                                'llm_time_suppressed', 'llm_time_suppressed_slots',
                                'scorer_mode', 'llm_used', 'llm_error'):
                        if _fk in sc:
                            c2[_fk] = sc.get(_fk)
                    enriched.append(c2)
                return {
                    'conflicts': enriched,
                    'conflict_v3': {
                        'version': v3.get('version'),
                        'raw_claims': v3.get('raw_claims'),
                        'total': len(enriched),
                        'live_alerts': v3.get('live_alerts', []),
                        'cross_session_summary': v3.get('cross_session_summary', {}),
                    },
                }
            except Exception as e:
                return {'error': str(e)}
        tasks['conflict'] = asyncio.create_task(_conflict())
    else:
        async def _c_skip():
            return {'conflicts': [], 'conflict_v3': {'total': 0}}
        tasks['conflict'] = asyncio.create_task(_c_skip())

    # 10+10.1+10.2: profile+heat+trajectory
    if sources and not lite:
        async def _profile_heat_traj():
            try:
                from entity_profile import EntityProfile
                from entity_heat import get_heat_ranking_async
                from entity_trajectory import trace_entity_async
                profiler = EntityProfile()
                ei = await asyncio.to_thread(profiler.update_profiles, sources, [])
                heat = await get_heat_ranking_async(top_n=10)
                traj = []
                for s in sources[:5]:
                    title = s.get('title', '')[:20]
                    if title:
                        traj.append(await trace_entity_async(title, 90))
                return {
                    'entity_profiles': ei,
                    'heat_ranking': heat,
                    'trajectory_top5': traj,
                }
            except Exception as e:
                return {'error': str(e)}
        tasks['profile_heat_traj'] = asyncio.create_task(_profile_heat_traj())
    else:
        async def _p_skip():
            return {
                'entity_profiles': {'skipped': 'lite_mode'},
                'heat_ranking': {'skipped': 'lite_mode'},
                'trajectory_top5': {'skipped': 'lite_mode'},
            }
        tasks['profile_heat_traj'] = asyncio.create_task(_p_skip())

    # 流式 yield 顺序（v3.0.0 GA 协议）
    yield_order = ['scored', 'wikidata', 'entity_graph', 'conflict', 'profile_heat_traj']

    # 收集结果（用于最后合并）
    results = {}
    for step_name in yield_order:
        task = tasks[step_name]
        try:
            result = await task
            results[step_name] = result if not isinstance(result, Exception) else {'error': str(result)}
        except Exception as e:
            results[step_name] = {'error': str(e)}

        # v3.0.0 GA yield 协议
        if step_name == 'scored':
            yield {'step': 'score_complete', 'scored_sources': results['scored']}
        elif step_name == 'wikidata':
            yield {'step': 'wikidata_complete', 'wikidata_verified': results['wikidata']}
        elif step_name == 'entity_graph':
            eg = results['entity_graph']
            if isinstance(eg, dict) and 'entity_graph' in eg:
                yield {'step': 'entity_graph_complete',
                       'entity_graph': eg.get('entity_graph'),
                       'traced_export': eg.get('traced_export')}
            else:
                yield {'step': 'entity_graph_complete', 'entity_graph': eg, 'traced_export': {'skipped': True}}
        elif step_name == 'conflict':
            cd = results['conflict']
            yield {'step': 'conflict_complete',
                   'conflicts': cd.get('conflicts', []),
                   'conflict_v3': cd.get('conflict_v3', {})}
        elif step_name == 'profile_heat_traj':
            pt = results['profile_heat_traj']
            yield {'step': 'profile_complete', 'entity_profiles': pt.get('entity_profiles', {})}
            yield {'step': 'trajectory_complete',
                   'heat_ranking': pt.get('heat_ranking', []),
                   'trajectory_top5': pt.get('trajectory_top5', [])}

    # 同步步骤（render_report）
    try:
        report = await asyncio.to_thread(render_report, subject, sources, output_format, domain)
    except Exception as e:
        report = f'[error] {e}'

    yield {'step': 'report_complete', 'report': report}


# ═══════════════════════════════════════════════════════════════
# v1 → v2 Deprecation Shim（兼容层）
# ═══════════════════════════════════════════════════════════════

def _deprecation_warning(old_func: str, new_func: str):
    """发出 deprecation 警告"""
    warnings.warn(
        f"{old_func} is deprecated since v2.0.0; use {new_func} instead.",
        DeprecationWarning,
        stacklevel=3,
    )


def v1_calculate_score_shim(*args, **kwargs):
    """v1 anchor_adapter.calculate_score() 的 shim"""
    _deprecation_warning('anchor_adapter.calculate_score()', 'infoseek_core_v2.score_source()')
    sys.path.insert(0, str(INFOSEEK_ROOT / 'scripts'))
    from anchor_adapter import calculate_score
    return calculate_score(*args, **kwargs)


def v1_detect_conflicts_shim(*args, **kwargs):
    """v1 conflict_detection.detect_conflicts() 的 shim"""
    _deprecation_warning('conflict_detection.detect_conflicts()', 'infoseek_core_v2.detect_conflicts()')
    return detect_conflicts(*args, **kwargs)


# ═══════════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════════

def main():
    """CLI: python infoseek_core_v2.py <subject>"""
    if len(sys.argv) < 2:
        print("Usage: python infoseek_core_v2.py <subject> [--domain X] [--with-llm] [--format md]")
        sys.exit(1)

    subject = sys.argv[1]
    domain = None
    with_llm = False
    output_format = 'md'

    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == '--domain' and i + 1 < len(args):
            domain = args[i + 1]
            i += 2
        elif args[i] == '--with-llm':
            with_llm = True
            i += 1
        elif args[i] == '--format' and i + 1 < len(args):
            output_format = args[i + 1]
            i += 2
        else:
            i += 1

    result = research(subject, domain=domain, with_llm=with_llm, output_format=output_format)
    print(result['report'])
    if 'llm_insights' in result:
        print('\n--- LLM Insights ---')
        print(result['llm_insights'])


if __name__ == '__main__':
    main()