#!/usr/bin/env python3
"""core/person_ner.py — GA9 人名消歧唯一真源（v1.9.0 / mod-v1.0.0）

治理动机（ROADMAP §8.11 / §8.12.2 GA9）
----------------------------------------
人物类调研三大实测缺陷中 D2「NER 词典不含人名」致融合链近乎空转：
95+ 实体以公司名为主，`extract_entities` 对人物语料仅命中 1 个实体，
`detect_conflicts_v3` 9 源仅产出 2 条 raw_claims。本模块按 §8.11.3 五步路线闭合：

  ① 多音字姓氏白名单     → `references/person-surnames.json`（数据真源，mtime 感知加载）
  ② 整词优先长匹配       → 复姓（欧阳/司马/爱新觉罗…≤4 字）先于单姓匹配，禁止逐字拆复姓
  ③ heteronym 全读音枚举 → `person_pinyin_aliases()` 输出多候选（姓氏多音字全枚举），
                            不在生成端硬判，交相关性门控 / 检索引擎自然收敛（§8.11.2 修正三件套）
  ④ person 实体族动态入库 → `register_person_runtime()` 运行时注册（默认，会话级零文件写入）；
                            `persist=True` 走 `entities.learn_entity` 持久化通道
  ⑤ 拼音别名接入 `_expand_query` → 由 `core/xling_bridge.py` 统一消费（GA10 联动）

多音字精度实锤（§8.11.2）：pypinyin 默认输出对姓氏误读率约 40%（单雄信→dan 应 shan、
查良镛→cha 应 zha、区楚良→qu 应 ou）→ 白名单 `preferred` 读音前置，`candidates`
仅作追加候选（heteronym 枚举），不做替换裁决。

两种检测模式（精度/召回分层）
------------------------------
- `mode='text'`（源文本扫描，保守）：仅 3-4 字候选 + 地名后缀守卫 + 虚词守卫 +
  blocklist + 叠字守卫 + 常用词守卫。精度优先——漏检由 subject 引导注册兜底
  （注册后走词典精确命中）。
- `mode='subject'`（调研主题/查询，宽松）：独立 CJK token 完整消费即可检（含 2 字名），
  blocklist + 地名后缀 + 虚词 + 叠字 + 常用词守卫（守卫两模式共用，防 bootstrap 注册污染）。
  subject 是用户声明的调研对象，召回优先于 text 模式。

设计约束
--------
- pypinyin / jieba 均为**可选依赖**（requirements.txt 已声明 pypinyin）：缺失时检测/注册
  仍工作，拼音别名降级为空、常用词守卫收窄 + 一次性告警（L3 降级哲学，
  同 text_tokenizer 的 jieba 模式）。
- 导入纪律：本模块经**顶层模块名**导入内部依赖（`entities`），规避 core./顶层
  双模块状态分裂；注册时同步失效所有已加载 entities 实例的缓存（见 _entities_modules）。
- 版本维度：mod-v1.0.0（模块内部版本），非 skill 对外版本
  （对外唯一真源见 `mcp_tools_common.SKILL_VERSION`）。
"""

from __future__ import annotations

import json
import logging
import os
import re
import sys
from pathlib import Path

__all__ = [
    'MOD_VERSION', 'load_surname_data', 'detect_person_names',
    'person_pinyin_aliases', 'register_person_runtime', 'bootstrap_subject',
    'process_text', 'surname_readings',
]

MOD_VERSION = '1.0.0'

log = logging.getLogger(__name__)

# ── 路径与幂等 sys.path 保障（模块导入期一次，GA8 纪律：禁止调用期 insert）──
_CORE_DIR = str(Path(__file__).parent)
if _CORE_DIR not in sys.path:
    sys.path.insert(0, _CORE_DIR)

_REF_PATH = Path(__file__).parent.parent / 'references' / 'person-surnames.json'

_CHN_RE = re.compile(r'[\u4e00-\u9fff]')
_CJK_RUN_RE = re.compile(r'[\u4e00-\u9fff]+')

# ── 数据加载（mtime 感知缓存）────────────────────────────────────────
_DATA = None
_DATA_MTIME = None
_DATA_WARNED = False

# L3 应急最小集（数据文件缺失/损坏时兜底：宁缺勿错，仅收录实锤多音字 + 高频姓）
_FALLBACK_DATA = {
    'version': '0-fallback',
    'compound_surnames': {
        '欧阳': ['ou', 'yang'], '司马': ['si', 'ma'], '诸葛': ['zhu', 'ge'],
        '上官': ['shang', 'guan'], '皇甫': ['huang', 'fu'], '令狐': ['ling', 'hu'],
        '尉迟': ['yu', 'chi'], '长孙': ['zhang', 'sun'], '宇文': ['yu', 'wen'],
        '澹台': ['tan', 'tai'], '万俟': ['mo', 'qi'], '单于': ['chan', 'yu'],
    },
    'single_surnames': list('王李张刘陈杨黄赵吴周徐孙马朱胡郭何林罗高郑梁谢宋唐许韩冯邓曹彭曾'),
    'polyphonic_surnames': {
        '单': {'preferred': 'shan', 'candidates': ['dan', 'chan']},
        '查': {'preferred': 'zha', 'candidates': ['cha']},
        '区': {'preferred': 'ou', 'candidates': ['qu']},
        '曾': {'preferred': 'zeng', 'candidates': ['ceng']},
        '解': {'preferred': 'xie', 'candidates': ['jie']},
    },
    'blocklist_words': ['马上', '王朝', '方向', '方法', '万一', '高兴', '程序', '任务'],
    'blocklist_geo': ['王府井', '石家庄', '张家口', '张家港', '马鞍山'],
    'geo_suffix_chars': list('庄口堡店镇村县市区省街路巷站港湾屯营坊井峪岭沟坪坝窑铺集岗洲州岛渡桥楼苑园城关塞庙寺塔陵墓门池都阁峡渠库厂矿里弄'),
    'stop_given_chars': list('的是了和与及或在有没不为之以所把被让从到对于由此如虽然可能应该需问题事情系会说道上下内外前后时很更最太再又才将已经正着过给使令各每些这里儿头面边式型类种等级数量率度值价第初向方法规则性者所其'),
}


def load_surname_data(force: bool = False) -> dict:
    """加载姓氏数据真源（mtime 感知缓存；缺失/损坏 → L3 应急最小集 + 一次性告警）。"""
    global _DATA, _DATA_MTIME, _DATA_WARNED
    try:
        mtime = _REF_PATH.stat().st_mtime
    except OSError:
        mtime = None
    if not force and _DATA is not None and _DATA_MTIME == mtime:
        return _DATA
    if mtime is None:
        if not _DATA_WARNED:
            log.warning(f"[person_ner] 姓氏数据缺失 {_REF_PATH} → L3 应急最小集"
                        f"（检测覆盖收窄；恢复文件即自动生效）")
            _DATA_WARNED = True
        _DATA, _DATA_MTIME = _FALLBACK_DATA, None
        return _DATA
    try:
        raw = json.loads(_REF_PATH.read_text(encoding='utf-8'))
        if not isinstance(raw, dict) or 'single_surnames' not in raw:
            raise ValueError('schema 缺 single_surnames')
        _DATA, _DATA_MTIME = raw, mtime
        _DATA_WARNED = False
    except Exception as e:
        if not _DATA_WARNED:
            log.warning(f"[person_ner] 姓氏数据损坏（{e}）→ L3 应急最小集")
            _DATA_WARNED = True
        _DATA, _DATA_MTIME = _FALLBACK_DATA, mtime
    return _DATA


# ── pypinyin / jieba 统一经 jieba_bridge 探测（2026-09-29 六处裸 import 收敛）──
# 探测/初始化/告警全部收口到 core/jieba_bridge.py（进程内一次、降级永不抛错）；
# 本模块不再保留独立 try-import 与模块级探测状态，避免双套状态口径漂移。
import jieba_bridge as _jb  # 顶层模块名导入：与 core.jieba_bridge 经 sys.modules 双登记合一


def _probe_pypinyin():
    """委托 bridge 探测 pypinyin（保留名字以向后兼容既有调用点/测试）。"""
    return _jb.get_pypinyin()


def _warn_pinyin_once() -> None:
    """委托 bridge：pypinyin 缺失一次性告警。"""
    _jb.warn_pypinyin_once()


# ── 常用词守卫（jieba 词典词频；2026-09-14 实测标定）─────────────────
# 词频分离度实锤：常用词 研究35029/管理27191/发展68664 vs 真名组合
# 林坚0/雄信0/泽天0/志明0/建华342/溥仪305 → 阈值 20000 两侧零重叠带
# （建国3083/文化34860 为边界代价：文化类高频"名字词"text 模式拒判，
#   精度优先，漏检由 subject 引导注册 + 静态词典/learn 通道兜底）。
_COMMON_GIVEN_FREQ = 20000


def _freq_common(word: str) -> bool:
    """二字组合是否为 jieba 词典高频常用词（≥ _COMMON_GIVEN_FREQ）。

    jieba 缺失/未初始化 → False（守卫收窄，检测仍工作——降级不阻断）。
    词频查询委托 bridge：jieba.dt 探测 + initialize 进程内一次
    （懒初始化：仅首个候选触发建词典，~1s/进程一次性）。
    """
    try:
        return _jb.word_freq(word) >= _COMMON_GIVEN_FREQ
    except Exception:
        return False


# ── 姓氏读音（①②：白名单前置 + 复姓整词）──────────────────────────

def _compound_surnames_by_len() -> dict:
    """复姓表按长度分桶（长匹配优先：4→3→2）。"""
    data = load_surname_data()
    buckets = {}
    for cs in data.get('compound_surnames', {}):
        buckets.setdefault(len(cs), []).append(cs)
    return buckets


def surname_readings(surname: str) -> list:
    """姓氏 → 读音变体列表（每个变体 = 音节 list；preferred 在前，heteronym 候选在后）。

    复姓：白名单整词读音（②禁止逐字切分）；缺失 → lazy_pinyin 整词。
    单姓：多音字白名单 preferred + candidates（①③）；缺失 → lazy_pinyin。
    pypinyin 缺失且白名单无读音 → []（调用方降级）。
    """
    data = load_surname_data()
    compounds = data.get('compound_surnames', {})
    if surname in compounds:
        return [list(compounds[surname])]
    poly = data.get('polyphonic_surnames', {}).get(surname)
    if poly:
        variants = [[poly['preferred']]]
        for c in poly.get('candidates', []):
            if c and [c] not in variants:
                variants.append([c])
        return variants
    pp = _probe_pypinyin()
    if pp is None:
        return []
    _v = _jb.lazy_pinyin(surname)
    return [_v] if _v else []


def _given_syllables(given: str) -> list:
    """名（非姓部分）→ 音节 list（lazy_pinyin 主读音；多音字组合爆炸，不做全枚举——
    §8.11.2 ③ 的枚举范围是**姓氏**多音字；名多音字取主读音，误差由相关性门控收敛）。"""
    pp = _probe_pypinyin()
    if pp is None:
        _warn_pinyin_once()
        return []
    return _jb.lazy_pinyin(given) or []


# ── 人名检测（②：整词优先长匹配 + 分层守卫）─────────────────────────

def _blocked(name: str, data: dict) -> bool:
    return (name in data.get('blocklist_words', ())
            or name in data.get('blocklist_geo', ()))


def _split_surname(seg: str, pos: int):
    """在 CJK 段 seg 的 pos 位置尝试姓氏匹配：复姓长匹配优先（4→3→2），再单姓。

    返回 (surname, surname_kind) 或 (None, None)。
    """
    data = load_surname_data()
    for ln in (4, 3, 2):
        cand = seg[pos:pos + ln]
        if len(cand) == ln and cand in data.get('compound_surnames', {}):
            return cand, 'compound'
    ch = seg[pos:pos + 1]
    if ch and ch in data.get('single_surnames', ()):
        return ch, 'single'
    return None, None


def _guards_ok(surname: str, given: str, name: str, data: dict,
               mode: str) -> bool:
    """公共守卫：blocklist / 叠字（名含姓字）/ 地名后缀字 / 虚词 / 常用词。"""
    if not given:
        return False
    if _blocked(name, data):
        return False
    # 叠字守卫：谢谢 / 王王 / 李李 类
    if any(c in surname for c in given):
        return False
    # 地名后缀守卫（两种模式均启用：石家庄/张家口/成都/温州 类整词误报主源）
    if name[-1] in data.get('geo_suffix_chars', ()):
        return False
    # 虚词守卫（两种模式均启用，2026-09-14 设计裁决）：名首字为功能词 → 判非人名。
    # subject 模式同样启用——bootstrap 会对每个检索 query 跑检测，「关系人/方向感」类
    # token 一旦注册即污染实体库；代价是「王向明」类真名漏检（可由静态词典/learn 兜底）。
    if given[0] in data.get('stop_given_chars', ()):
        return False
    # 常用词守卫（两种模式均启用）：双字名为 jieba 高频常用词 → 判非人名
    # （「都研究/张管理」类姓氏字+动词组合误报主源；阈值标定见 _freq_common）
    if len(given) == 2 and _freq_common(given):
        return False
    return True


def detect_person_names(text: str, mode: str = 'text', max_names: int = 10) -> list:
    """检测中文人名（②整词优先长匹配；分层守卫见模块 docstring）。

    Args:
        text: 输入文本。
        mode: 'text'（源文本，保守：单姓仅 3 字名 + 全守卫）/ 'subject'（调研主题，
              宽松：独立 CJK token 完整消费，2-4 字）。
        max_names: 返回上限（防长文本爆炸）。

    Returns:
        [{'name', 'surname', 'given', 'surname_kind', 'span', 'confidence'}, ...]
        检测失败/无命中 → []（不抛异常）。
    """
    if not text or not _CHN_RE.search(text):
        return []
    data = load_surname_data()
    out = []
    seen = set()

    def _candidate_at(seg: str, pos: int, seg_offset: int, mode: str):
        """纯函数候选生成（不写 out——subject 模式须先过「token 完整消费」校验，
        否则「石家庄旅游」会漏进半消费的「石家」类误报）。返回 (候选|None, 消费长度)。"""
        surname, kind = _split_surname(seg, pos)
        if not surname:
            return None, 0
        slen = len(surname)
        for glen in (2, 1):
            given = seg[pos + slen: pos + slen + glen]
            if len(given) != glen or not all(_CHN_RE.match(c) for c in given):
                continue
            name = surname + given
            total = slen + glen
            if mode == 'text':
                # text 模式：单姓仅收 3 字名（2 字名误报率高）；复姓允许 3-4 字
                if kind == 'single' and total != 3:
                    continue
            if not _guards_ok(surname, given, name, data, mode):
                continue
            conf = {'compound': 0.8}.get(kind, 0.7 if total >= 3 else 0.5)
            return {
                'name': name, 'surname': surname, 'given': given,
                'surname_kind': kind,
                'span': (seg_offset + pos, seg_offset + pos + total),
                'confidence': conf,
            }, total
        return None, 0

    if mode == 'subject':
        # subject 模式：按独立 token 判定（非 CJK 字符切分），token 须被完整消费
        for m in _CJK_RUN_RE.finditer(text):
            tok = m.group(0)
            if not (2 <= len(tok) <= 6):
                continue
            cand, consumed = _candidate_at(tok, 0, m.start(), mode)
            if consumed != len(tok):
                continue  # token 未被完整消费（如「石家庄旅游」）→ 不判人名
            if cand and cand['name'] not in seen and len(out) < max_names:
                seen.add(cand['name'])
                out.append(cand)
    else:
        for m in _CJK_RUN_RE.finditer(text):
            seg = m.group(0)
            pos = 0
            while pos < len(seg) and len(out) < max_names:
                cand, consumed = _candidate_at(seg, pos, m.start(), mode)
                if cand and cand['name'] not in seen:
                    seen.add(cand['name'])
                    out.append(cand)
                pos += consumed if consumed else 1
    return out


# ── 拼音别名生成（③：姓氏 heteronym 全枚举，生成端不硬判）────────────

def person_pinyin_aliases(name: str, max_aliases: int = 6) -> list:
    """中文人名 → 拉丁拼音别名（preferred 读音在前，多音字候选在后）。

    输出形如 ['shan xiongxin', 'xiongxin shan', 'shanxiongxin',
              'shan xiong xin', 'xiong xin shan', 'dan xiongxin']（≤ max_aliases）。
    名部分按英文惯例连写（'linjian' 而非 'lin jian'），并附全空格变体。
    pypinyin 缺失且非白名单姓 → []（降级不抛错）。
    """
    if not name:
        return []
    surname, kind = _split_surname(name, 0)
    if not surname or len(surname) >= len(name):
        return []
    given = name[len(surname):]
    sur_variants = surname_readings(surname)
    if not sur_variants:
        _warn_pinyin_once()
        return []
    giv = _given_syllables(given)
    if not giv:
        # 白名单姓氏读音可用但 pypinyin 缺失 → 名部分无法转写，降级
        return []
    giv_cat = ''.join(giv)      # 英文名惯例：名整体连写（'linjian' → 'Linjian Xiang'）
    giv_sp = ' '.join(giv)      # 全空格变体（覆盖 'Lin jian Xiang' 类排版）
    out = []
    for sur in sur_variants:
        sur_join = ' '.join(sur)
        sur_cat = ''.join(sur)
        for a in (f"{sur_join} {giv_cat}", f"{giv_cat} {sur_join}",
                  f"{sur_cat}{giv_cat}", f"{sur_join} {giv_sp}",
                  f"{giv_sp} {sur_join}"):
            if a and a not in out:
                out.append(a)
        if len(out) >= max_aliases:
            break
    return out[:max_aliases]


# ── ④ person 实体族动态入库 ─────────────────────────────────────────

def _entities_modules() -> list:
    """返回所有可解析的 entities 模块实例（entities / core.entities 双路径）。

    双模块陷阱治理：注册须写入**所有已加载实例**并失效各自缓存，否则
    消费方（ner.extract_entities 顶层路径 vs _expand_query 包路径）看到的
    PERSON_ENTITIES 不一致。
    """
    mods = []
    for mn in ('entities', 'core.entities'):
        m = sys.modules.get(mn)
        if m is None:
            try:
                import importlib
                m = importlib.import_module(mn)
            except Exception:
                continue
        if m is not None and m not in mods:
            mods.append(m)
    return mods


def _name_known(mod, name: str) -> bool:
    try:
        for e in mod.get_all_entities():
            if e.get('name', '') == name:
                return True
            if any(a == name for a in e.get('aliases', []) or []):
                return True
    except Exception:
        pass
    return False


def register_person_runtime(name: str, aliases=None, confidence: float = 0.6,
                            persist: bool = False) -> bool:
    """④ 人名动态注册进 person 实体族（闭合 D2：NER/融合链可按人名索引）。

    默认**运行时会话级**注册（直接 append 进各 entities 实例的 PERSON_ENTITIES
    + 失效合并缓存；零文件写入 → 无跨会话噪声累积风险）。
    persist=True → 走 entities.learn_entity 持久化通道（INFOSEEK_DATA_DIR 治理）。

    幂等：同名（含别名命中）已存在 → 仅合并缺失别名，不重复建条。
    """
    if not name or len(name) < 2:
        return False
    aliases = [a for a in (aliases or []) if a and a != name]
    registered = False
    for mod in _entities_modules():
        try:
            known = _name_known(mod, name)
            if not known:
                entry = {
                    'name': name,
                    'aliases': list(dict.fromkeys(aliases)),
                    'category': 'PERSON',
                    'source': 'person_ner',
                    'confidence': float(confidence),
                }
                mod.PERSON_ENTITIES.append(entry)
                registered = True
            elif aliases:
                # 已存在 → 补齐缺失别名（静态词典条目别名不改动，仅 learned/动态条目）
                _pool = list(mod.PERSON_ENTITIES)
                if hasattr(mod, 'get_learned_entities'):
                    _pool += list(mod.get_learned_entities())
                for e in _pool:
                    if e.get('name') == name and e.get('source') in ('person_ner', 'learned'):
                        merged = list(dict.fromkeys(list(e.get('aliases', [])) + aliases))
                        if merged != e.get('aliases'):
                            e['aliases'] = merged
            mod._ALL_ENTITIES_CACHE = None  # 失效合并缓存（下次 NER 即见）
        except Exception:
            continue
    if persist:
        try:
            import entities as _ent
            _ent.learn_entity(name, aliases, category='PERSON',
                              confidence=confidence)
        except Exception:
            pass
    if registered:
        log.info(f"[person_ner] 注册人名实体 '{name}'"
                 f"{f' +{len(aliases)} 别名' if aliases else ''}")
    return registered


def bootstrap_subject(subject: str) -> list:
    """⑤ 调研主题人名引导：subject 检测 → 拼音别名 → 动态注册（幂等）。

    由 research / async_research / streaming_research / detect_conflicts /
    _expand_query 入口调用；失败静默（不阻断主链路）。
    env 闸：INFOSEEK_PERSON_NER（默认开）。

    Returns: [{'name', 'aliases', 'confidence'}, ...]
    """
    if os.environ.get('INFOSEEK_PERSON_NER', '1') in ('0', 'false', 'False', 'no', 'off'):
        return []
    try:
        persons = detect_person_names(subject or '', mode='subject')
        out = []
        for p in persons:
            aliases = person_pinyin_aliases(p['name'])
            register_person_runtime(p['name'], aliases,
                                    confidence=p.get('confidence', 0.6))
            out.append({'name': p['name'], 'aliases': aliases,
                        'confidence': p.get('confidence', 0.6)})
        return out
    except Exception:
        return []


def process_text(text: str, register: bool = False, max_names: int = 10) -> list:
    """源文本人名扫描（text 模式，保守守卫）。register=True 时同步入库。"""
    try:
        persons = detect_person_names(text or '', mode='text', max_names=max_names)
        if register:
            for p in persons:
                register_person_runtime(p['name'], person_pinyin_aliases(p['name']),
                                        confidence=p.get('confidence', 0.6))
        return persons
    except Exception:
        return []
