#!/usr/bin/env python3
"""
domain_router.py — Infoseek 领域 Profile 路由器（mod-v1.8.1）

版本维度声明（v1.8.1 治理）：本文件内所有 v1.8.x 标记均为「模块内部版本 mod-v」，仅描述
本模块自身演进，与 skill 对外版本（scripts/mcp_tools_common.py:SKILL_VERSION）不同维度，
不可比较大小、不可混用。

从 5 个领域 profile YAML 中根据关键词自动路由：
- tech-research（技术工艺）
- market-research（市场研究）
- finance-research（金融投资）
- policy-research（政策法规）
- competitor-intel（竞品情报）

返回选中的 profile 路径与权重，供 anchor_adapter.calculate_score() 使用。
"""

import os
import re
from pathlib import Path
from typing import Optional

import yaml

WORKSPACE = Path(os.environ.get('OPENCLAW_WORKSPACE', str(Path.home() / 'infoseek')))
DOMAINS_DIR = Path(__file__).parent.parent / 'domains'


# 各领域关键词触发词（内置兜底；唯一真源见 references/keyword.yaml，v1.7.5 外置）
_BUILTIN_TRIGGERS = {
    'tech-research': {
        'weight': 1.0,
        'keywords': [
            '工艺', '分切', '轧制', '退火', '热处理', '冷轧', '热轧', '模具',
            '圆盘刀', '重叠量', '压辊', '张力', '缺陷', '毛刺', '钢卷', '带钢',
            '不锈钢', '合金', '精度', '公差', '工艺参数', '设备', '工序',
            'process', 'rolling', 'annealing', 'tolerance', 'defect',
            'alloy', 'precision', 'manufacturing', 'slitting', 'coiling',
            # v1.0.1 PATCH (P0-3): 扩充通用技术触发词，修复技术主题
            # 检测返回 None（如"DeepSeek 开源模型 技术路线"）
            '模型', '开源', '技术', '算法', '软件', '代码', '芯片', '架构',
            '大模型', '人工智能', '深度学习', '机器学习', '训练', '推理',
            'framework', 'open source', 'software', 'algorithm', 'chip',
            'architecture', 'deep learning', 'machine learning', 'llm',
            'training', 'inference', 'api', '模型', '微调', '部署',
            # P0-OPEN-05：AI 产品/实体词（与 keyword.yaml 唯一真源保持一致）
            'gpt', 'gpt5', 'gpt-5', 'chatgpt', 'openai', 'claude', 'gemini',
            'agent', '智能体', 'aigc', '生成式',
        ],
    },
    'market-research': {
        'weight': 1.0,
        'keywords': [
            '市场', '行业', '规模', '增速', 'CAGR', '渗透率', '用户画像',
            '消费', '需求', '行业研究', '市场规模', '细分', '增长',
            'market', 'industry', 'segment', 'TAM', 'SAM', 'SOM', 'user persona',
            'consumer', 'demand', 'growth',
        ],
    },
    'finance-research': {
        'weight': 1.0,
        'keywords': [
            '股票', '基金', '债券', '期货', '外汇', '期权', '行情', 'K线',
            'MACD', 'KDJ', 'RSI', '布林带', '财报', '估值', 'PE', 'PB',
            '市净率', '市盈率', '回测', '策略', '持仓', '杠杆', '做空',
            'stock', 'equity', 'bond', 'futures', 'forex', 'technical analysis',
            'valuation', 'backtest', 'portfolio', 'leverage',
        ],
        # DEF-16（v2.1.1 P2）：中文无空格词边界，2 字短词「回测」裸子串会误嵌进
        # 常用多字词——铁证「工业来回测试平台」（零金融语义）因「来**回测**试」被判 finance。
        # strict_keywords 中的 2 字中文词命中时，额外校验每次出现是否都被 false_compounds
        # （含该词的非金融常用多字词）覆盖；全部被覆盖则不命中，至少一次干净出现才命中。
        # 仅收录经实证的高置信项，其余 2 字词无实证误例，保留子串匹配（零过杀）。
        'strict_keywords': ['回测'],
        'false_compounds': ['来回测试', '回测设备'],
    },
    'policy-research': {
        'weight': 1.0,
        'keywords': [
            '政策', '法规', '标准', '合规', '监管', '国标', 'GB ', 'ISO',
            '工信部', '发改委', '证监会', '银保监', '国务院', '指导意见',
            '通知', '办法', '条例', '规定',
            'policy', 'regulation', 'compliance', 'standard', 'governance',
            'regulatory', 'mandate', 'directive',
        ],
    },
    'competitor-intel': {
        'weight': 1.0,
        'keywords': [
            '竞品', '对比', '差异化', '竞争对手', '市场份额', '产品矩阵',
            '功能比较', 'vs ', ' versus', 'alternative', 'competitor',
            'comparison', 'feature parity', 'head-to-head',
        ],
    },
}


def _load_domain_triggers() -> dict:
    """加载领域关键词触发词（唯一真源 references/keyword.yaml，v1.7.5 外置）。

    - 文件缺失 / 解析失败 / 结构为空 → 返回内置 _BUILTIN_TRIGGERS 副本（路由不塌）
    - env INFOSEEK_KEYWORD_YAML 可覆盖路径
    """
    path = os.environ.get('INFOSEEK_KEYWORD_YAML') or str(
        Path(__file__).parent.parent / 'references' / 'keyword.yaml')
    try:
        p = Path(path)
        if p.exists():
            data = yaml.safe_load(p.read_text(encoding='utf-8')) or {}
            doms = data.get('domains') or {}
            out = {}
            for k, v in doms.items():
                if isinstance(v, dict) and v.get('keywords'):
                    out[k] = {
                        'weight': v.get('weight', 1.0),
                        'keywords': list(v['keywords']),
                        # DEF-16：可选歧义短词边界配置（缺失回退内置/空集）
                        'strict_keywords': list(v.get('strict_keywords', [])),
                        'false_compounds': list(v.get('false_compounds', [])),
                    }
            if out:
                return out
    except Exception:
        pass
    return {k: {'weight': v['weight'],
                'keywords': list(v['keywords']),
                'strict_keywords': list(v.get('strict_keywords', [])),
                'false_compounds': list(v.get('false_compounds', []))}
            for k, v in _BUILTIN_TRIGGERS.items()}


DOMAIN_TRIGGERS = _load_domain_triggers()


# P0-OPEN-05：纯字母/数字的短缩写（≤4 字符，如 PE/PB/RSI/KDJ/GB）若用裸子串
# 匹配会误命中普通英文单词（实测 'PE' in 'openai' → 把「OpenAI Agent」误判金融）。
# 这类 token 必须走正则词边界；中文词与含空格/长英文短语保留子串匹配。
_ASCII_WORD_RE = re.compile(r'^[a-z0-9]{1,4}$')
# 产品前缀（纯字母、以字母结尾）：允许后接版本数字（GPT4/GPT-5），故后向只排除字母。
_PREFIX_WORDS = {'gpt'}


def _all_occurrences_embedded(kw: str, text: str, false_compounds) -> bool:
    """DEF-16：判断 kw 在 text 中的每次出现是否都被某个 false_compound（含 kw 的
    非金融常用多字词）覆盖。

    - 无出现 → False（由调用方先保证 kw in text）；
    - 任一次出现不落在任何误嵌词区间内 → False（存在干净命中，应真命中）；
    - 所有出现均被误嵌词区间覆盖 → True（整词只是常用多字词的片段，不命中）。
    """
    spans = []
    for fc in false_compounds:
        if kw in fc:
            start = 0
            while True:
                idx = text.find(fc, start)
                if idx < 0:
                    break
                spans.append((idx, idx + len(fc)))
                start = idx + 1
    if not spans:
        return False
    pos = 0
    while True:
        idx = text.find(kw, pos)
        if idx < 0:
            return True  # 所有出现已遍历完，未发现干净命中
        end = idx + len(kw)
        if not any(s <= idx and end <= e for s, e in spans):
            return False  # 该次出现不在任何误嵌词内 → 干净命中
        pos = idx + 1


def _keyword_hit(kw_lower: str, subject_lower: str,
                 strict: bool = False, false_compounds=()) -> bool:
    """关键词是否命中文本。

    - 短 ASCII token（≤4 位字母数字）走正则词边界（防 'PE' in 'openai'）；
    - DEF-16：strict 的 2 字中文短词，命中后校验是否仅作为 false_compounds 的
      片段出现（防「回测」误命中「来回测试」）；
    - 其余（长中文词/英文短语）保留子串匹配。
    """
    if _ASCII_WORD_RE.match(kw_lower):
        if kw_lower in _PREFIX_WORDS:
            tail = r'(?![a-z])'      # 后可接数字/连字符（版本号），不可接字母（防 openai 类）
        else:
            tail = r'(?![a-z0-9])'
        return re.search(r'(?<![a-z0-9])' + re.escape(kw_lower) + tail,
                         subject_lower) is not None
    if kw_lower not in subject_lower:
        return False
    if strict and false_compounds and \
            _all_occurrences_embedded(kw_lower, subject_lower, false_compounds):
        return False
    return True


def detect_domain(subject: str) -> dict:
    """根据主题文本自动选择最匹配的领域 profile。

    参数:
        subject: 调研主题或描述

    返回:
        {
          "domain": 选中的领域名，
          "score": 匹配得分，
          "candidates": [所有候选及得分]，
          "profile_path": profile YAML 文件路径，
        }
    """
    # DEF-13（v2.1.1 P2）：公开函数入口类型守卫。None / 数字 / 其他非字符串
    # 旧代码直传 .lower() 抛 AttributeError 击穿任何直调方（MCP 工具/新调用点）。
    # None → ''，其余非字符串 → str()；空输入随后走既有「无触发词→is_default」分支。
    if not isinstance(subject, str):
        subject = '' if subject is None else str(subject)
    subject_lower = subject.lower()

    candidates = []
    for domain, cfg in DOMAIN_TRIGGERS.items():
        hit_count = 0
        strict_kw = set(k.lower() for k in cfg.get('strict_keywords', ()))
        false_compounds = [c.lower() for c in cfg.get('false_compounds', ())]
        for kw in cfg['keywords']:
            kwl = kw.lower()
            if _keyword_hit(kwl, subject_lower,
                            strict=kwl in strict_kw,
                            false_compounds=false_compounds):
                hit_count += 1
        score = hit_count * cfg['weight']
        candidates.append({
            'domain': domain,
            'score': score,
            'hit_count': hit_count,
        })

    # 按得分降序排序
    candidates.sort(key=lambda x: -x['score'])
    # v1.8.1 多域交集判定（A）：多域得分>0 且 top2 差距 < 阈值 → 判交集
    _gap = _intersect_gap()
    _positive = [c for c in candidates if c['score'] > 0]
    _is_intersect = bool(len(_positive) >= 2
                         and (_positive[0]['score'] - _positive[1]['score']) < _gap)
    _intersect_domains = [c['domain'] for c in _positive]

    best = candidates[0] if candidates else None
    if not best or best['score'] == 0:
        # 无触发词 → 默认通用研究（不强制领域）
        return {
            'domain': None,
            'score': 0,
            'candidates': candidates,
            'profile_path': None,
            'is_default': True,
            'intersect_domains': [],
            'is_intersect': False,
            'prefer_kb': False,
        }

    profile_path = DOMAINS_DIR / f"{best['domain']}.yaml"
    return {
        'domain': best['domain'],
        'score': best['score'],
        'candidates': candidates,
        'profile_path': str(profile_path) if profile_path.exists() else None,
        'is_default': False,
        'intersect_domains': _intersect_domains,
        'is_intersect': _is_intersect,
        'prefer_kb': _is_intersect,
    }


def load_profile(domain_name: str) -> dict:
    """加载指定领域的 profile YAML。

    参数:
        domain_name: 领域名（如 "tech-research"）

    返回:
        profile dict，包含 trust_sources / keywords_template / weights / output_format

    异常:
        FileNotFoundError: profile 文件不存在
    """
    profile_path = DOMAINS_DIR / f"{domain_name}.yaml"
    if not profile_path.exists():
        raise FileNotFoundError(f"Profile not found: {profile_path}")

    with open(profile_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 简单 YAML 解析（支持注释 + 嵌套）
    profile = {
        'name': domain_name,
        'raw': content,
    }

    # 提取信任源白名单（v1.8.0 简化版，只读 raw 文本）
    # 实际应用时建议用 PyYAML 或 ruamel.yaml 严格解析
    return profile


def apply_profile_to_score(source: dict, profile: dict, prefer_kb: bool = False) -> dict:
    """根据 profile 微调评分权重（v1.8.1：泛化信任源解析 + prefer_kb 加分分段）。

    参数:
        source: 来源 dict（含 url、platform、text 等；可带 _kb_domain / _kb_hit_count）
        profile: 领域 profile dict（含 raw 文本）
        prefer_kb: 是否处于多域交集场景（由 detect_domain 产出）。开启后对带 KB
                   域标记的 source 额外加分（分段边界见 _KB_INTERSECT_BONUS / _KB_MULTI_BONUS）

    返回:
        更新后的 source（含 domain_applied / domain_bonus 字段）
    """
    if not profile:
        return source

    # v1.8.1 单源委托：信任源加权（消除三份漂移）
    bonus = trust_source_bonus(source, profile)

    # v1.8.1 prefer_kb 加分分段（交集场景 KB 可信度更高；单源委托）
    if prefer_kb:
        bonus += kb_intersect_bonus(source, profile)

    source['domain_applied'] = profile.get('name', '')
    source['domain_bonus'] = min(bonus, domain_bonus_cap())  # v1.8.3 单源 cap
    return source


# ── v1.8.1 多域交集 / KB 优先 辅助常量与函数 ──
def _int_env(name: str, default: int) -> int:
    """整型 env 读取（非法值回落默认；v1.7.5 配置化）。"""
    try:
        return int(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


_DOMAIN_BONUS_CAP = _int_env('INFOSEEK_DOMAIN_BONUS_CAP', 20)      # 信任源加权总分上限（模块加载期快照）
_KB_INTERSECT_BONUS = _int_env('INFOSEEK_KB_INTERSECT_BONUS', 8)   # 交集场景：单 KB +8
_KB_MULTI_BONUS = _int_env('INFOSEEK_KB_MULTI_BONUS', 4)           # 交集场景：多 KB 额外 +4（合计 +12）


def domain_bonus_cap() -> int:
    """领域加权总分上限 —— 唯一 cap 真源（v1.8.3 · §8.4 去硬编码）。

    历史分叉：本模块用 `_DOMAIN_BONUS_CAP`（env 可配），而
    `core/anchor_score_v2.compute_domain_bonus_v2` 与
    `scripts/anchor_adapter._compute_domain_bonus` 各自硬编码 `min(bonus, 20)`
    → 调 `INFOSEEK_DOMAIN_BONUS_CAP` 后两处不跟随，声明化配置半失效。
    现三处统一委托本函数（**每次动态读 env**，故运行期改 env / 测试 monkeypatch 均生效；
    `_DOMAIN_BONUS_CAP` 常量保留仅为向后兼容引用，不再作为判分依据）。
    """
    return _int_env('INFOSEEK_DOMAIN_BONUS_CAP', 20)
_TRUST_HINTS = tuple(
    h.strip() for h in os.environ.get('INFOSEEK_TRUST_HINTS', '来源,Tier,白名单').split(',')
    if h.strip()
)


def trust_source_bonus(source: dict, profile: dict) -> int:
    """信任源加权（单源定义，v1.7.2）。

    从 profile raw 的「来源/Tier/白名单」行提取信任源实体词，
    命中 url 计 +5 / platform 计 +3，上限 domain_bonus_cap()（v1.8.3 动态 env）。
    收敛 anchor_adapter._compute_domain_bonus 与
    anchor_score_v2.compute_domain_bonus_v2 的重复实现（原 +4/+3 全行提取）。
    """
    if not profile:
        return 0
    url_lower = (source.get('url') or '').lower()
    platform = source.get('platform') or ''
    bonus = 0
    for kw in set(_extract_trust_sources(profile.get('raw', ''))):
        if kw.lower() in url_lower:
            bonus += 5
        if kw in platform:
            bonus += 3
    return min(bonus, domain_bonus_cap())  # v1.8.3 单源 cap


def parse_domain_params(profile: dict) -> dict:
    """从领域 profile（Markdown raw）解析「领域路由参数」块（v1.7.5 声明化）。

    识别行：
        intersect_boost: 8
        kb_priority: true
    解析失败/缺省 → 对应值为 None（消费方回落默认常量）。
    """
    raw = profile.get('raw', '') if isinstance(profile, dict) else ''
    out = {'intersect_boost': None, 'kb_priority': None}
    m = re.search(r'intersect_boost:\s*(\d+)', raw)
    if m:
        out['intersect_boost'] = int(m.group(1))
    m2 = re.search(r'kb_priority:\s*(true|false)', raw, re.IGNORECASE)
    if m2:
        out['kb_priority'] = m2.group(1).lower() == 'true'
    return out


def kb_intersect_bonus(source: dict, profile: dict = None) -> int:
    """prefer_kb 交集场景的 KB 源加分（单 KB +8 / 多 KB 额外 +4，**合计 +12**）。

    v1.8.3 文档勘误：原首行「多 KB +4」易被误读为多 KB 总分 4（低于单 KB），
    实际语义 = _KB_INTERSECT_BONUS(8) + _KB_MULTI_BONUS(4) = 12；
    `trusted_kb.kb_merge` 注释「单 KB +8 / 多 KB +12」为正确口径，现两处对齐。

    单源定义：供 anchor_adapter / anchor_score_v2 / infoseek_core_v2 /
    trusted_kb 等消费方复用，避免多份漂移。
    识别标记：source['_kb_domain']（kb_enrich/kb_merge 注入）
             + source['_kb_hit_count']（多 KB 命中数，>=2 触发额外加成）。
    v1.7.5 声明化：profile 提供 intersect_boost 时覆盖默认基准（多 KB 额外仍用常量）。
    """
    kb_domain = source.get('_kb_domain') or source.get('kb_domain')
    if not kb_domain:
        return 0
    try:
        hits = int(source.get('_kb_hit_count', 1) or 1)
    except (TypeError, ValueError):
        hits = 1
    base = _KB_INTERSECT_BONUS
    if profile:
        p = parse_domain_params(profile).get('intersect_boost')
        if p is not None:
            base = p
    bonus = base
    if hits >= 2:
        bonus += _KB_MULTI_BONUS
    return bonus


def _intersect_gap() -> float:
    """多域交集判定阈值（INFOSEEK_DOMAIN_INTERSECT_GAP，默认 2）。"""
    try:
        return max(0.0, float(os.environ.get('INFOSEEK_DOMAIN_INTERSECT_GAP', '2')))
    except (TypeError, ValueError):
        return 2.0


def _extract_trust_sources(raw: str) -> list:
    """从 profile raw 抽取信任源实体词（替代 v1.8.0 硬编码清单）。

    v2.3.2 修正：实体位于「来源/Tier/白名单」锚点下方的 **Markdown 表格数据行**
    （如 ``| 监管 | 证监会/上交所/SEC | +25 |``），而旧实现只扫描含 hint 的锚点行，
    仅能命中表头的「来源/类型」，致领域信任段长期为 0。现改为：
      1. 定位含 hint 的锚点行（表头/小节标题）；
      2. 向后收集连续表格行（``| ... |``），跳过分隔行（``|:--``）与表头行；
      3. 从数据行按 ``/ 、 · , 空白`` 切分抽取中英专有名词。
    """
    lines = (raw or '').split('\n')
    # 表格列的类型标签等噪声（非信任源实体）
    _COL_NOISE = {'权重', '类型', '来源', '适用场景', '监管', '数据', '研报',
                  '官方', '媒体', 'Tier', '白名单', '信任源白名单'}
    kws = []
    for i, line in enumerate(lines):
        if not any(h in line for h in _TRUST_HINTS):
            continue
        # 锚点命中：向后扫描连续表格块（最多 20 行）
        for tbl in lines[i + 1: i + 21]:
            s = tbl.strip()
            if not s:
                break                      # 空行 → 表格块结束
            if not s.startswith('|'):
                break                      # 非表格行 → 块结束
            cells = [c.strip() for c in s.strip('|').split('|')]
            if all(set(c) <= set(':- ') for c in cells):
                continue                   # 分隔行 |:---|
            for cell in cells:
                # 按常见分隔符切分单元格
                for part in re.split(r'[/、·,\s]+', cell):
                    part = part.strip()
                    if not part:
                        continue
                    for kw in re.findall(r'[\u4e00-\u9fff]{2,8}|[A-Za-z][A-Za-z0-9.]{1,}', part):
                        if kw not in _COL_NOISE and not kw.startswith('+'):
                            kws.append(kw)
    return kws


if __name__ == '__main__':
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python domain_router.py <subject>")
        sys.exit(1)

    subject = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else sys.argv[1]
    result = detect_domain(subject)

    print(f"主题: {subject}")
    if result.get('is_default'):
        print(f"匹配: 无触发词，使用默认通用研究")
    else:
        print(f"匹配领域: {result['domain']} (得分 {result['score']})")
        print(f"Profile: {result['profile_path']}")
    print("所有候选:")
    for cand in result['candidates'][:3]:
        print(f"  - {cand['domain']:20s} 得分={cand['score']:.0f} 命中={cand['hit_count']}")

