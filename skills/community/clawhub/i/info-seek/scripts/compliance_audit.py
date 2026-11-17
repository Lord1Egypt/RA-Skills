#!/usr/bin/env python3
"""Infoseek 合规审计自动化（D-8 / P3-9 立项落地，mod-v2.6.1）

四链合一自动化审计报告（P3-9 定义：抓取合规 / 版权 / 凭证审计的自动化报告）：
  ① 凭证链      复用 scripts/leak_scan.py（密钥字面量扫描）+ core/key_manager.py（脱敏状态）
  ② 抓取合规链  复用 core/capability_registry.py（consent 闸口 / 启用判定）+ ~/.infoseek/consent.log
  ③ 网络边界链  复用 scripts/boundary_gate.py（**静态声明校验，零网络请求**）
  ④ 版权来源链  复用 references/trusted-sources.json（可信源台账）

设计约束（对齐本仓零依赖 / 降级哲学）：
  - **只读**：不写状态、不建目录、不发网络请求；任一数据源缺失记「无记录」而非抛错
  - **真源复用**：不重复实现扫描 / 注册表 / 边界校验，全部 import 既有模块，避免口径分叉
  - **误报白名单**：仓库自检口径下，测试夹具 / 文档占位符不算可处置项（见 PLACEHOLDER_MARKERS）
  - **脱敏**：actionable 凭证只记「已脱敏」占位，明文不落报告；非敏感指纹（前4***后4）可保留
  - 输出 Markdown / JSON 报告；CLI: --path --out --json-out --json --strict

退出码: 0=无待处置项（默认）  1=--strict 且存在可处置项
"""
from __future__ import annotations

import argparse
import importlib
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# AUDIT_VERSION 动态引用唯一真源（2026-09-29：原写死 '2.2.0'，每次升版漂移）
sys.path.insert(0, str(ROOT / 'scripts'))
try:
    from mcp_tools_common import SKILL_VERSION as AUDIT_VERSION
except Exception:
    AUDIT_VERSION = '2.3.0'
DEFAULT_REPORT_REL = 'references/compliance-audit-report.md'
DEFAULT_JSON_REL = 'references/compliance-audit-report.json'
NETWORK_REPORT_REL = 'references/network-boundary-report.md'
SCAN_EXCLUDES = ('dist', 'node_modules', '.git', '.venv', '.mypy_cache', '__pycache__')
# 审计自身产物：禁止自扫描（否则报告里回显的命中会被二次判级，形成自污染回路）
SELF_OUTPUT_NAMES = ('compliance-audit-report.md', 'compliance-audit-report.json')
_FALLBACK_EXTS = {'.py', '.js', '.ts', '.tsx', '.json', '.yaml', '.yml', '.env',
                  '.toml', '.ini', '.sh', '.md', '.txt'}

# 仓库自检口径的误报白名单：测试夹具 / 文档示例 / 占位符
PLACEHOLDER_MARKERS = (
    'secret', 'redacted', 'example', 'sample', 'demo', 'dummy', 'fake', 'mock',
    'placeholder', 'your', 'changeme', 'none', 'null', 'xxx', '<', '${', 'not_set',
)
TEST_PATH_SEGMENTS = ('tests', 'test', '__tests__', 'examples', 'docs', 'fixtures')

for _p in (str(ROOT), str(ROOT / 'core'), str(ROOT / 'scripts')):
    if _p not in sys.path:
        sys.path.append(_p)


def _import_first(*names):
    """按序尝试导入，返回首个成功模块；全失败返回 None（降级不抛）。"""
    for name in names:
        try:
            return importlib.import_module(name)
        except Exception:
            continue
    return None


_LEAK = _import_first('leak_scan', 'scripts.leak_scan')
_KEYS = _import_first('core.key_manager', 'key_manager')
_CAPS = _import_first('core.capability_registry', 'capability_registry')
_BOUND = _import_first('boundary_gate', 'scripts.boundary_gate')


# ── 误报分级 ──────────────────────────────────────────────────────────────
def _classify(value: str, file_path: str) -> str:
    """把一条扫描命中分级：test_fixture / placeholder / actionable。"""
    path = str(file_path).replace('\\', '/').lower()
    if any(seg in TEST_PATH_SEGMENTS for seg in path.split('/') if seg):
        return 'test_fixture'
    low = str(value).lower()
    if any(m in low for m in PLACEHOLDER_MARKERS):
        return 'placeholder'
    return 'actionable'


def _redact(value: str, klass: str) -> str:
    """命中一律不回显明文：actionable 给人工复核占位，其余给掩码预览（防误分级泄密）。"""
    if klass == 'actionable':
        return '***（已脱敏，需人工复核）'
    s = str(value)
    return (s[:3] + '***') if len(s) > 6 else '***'


# ── ① 凭证链 ──────────────────────────────────────────────────────────────
def _iter_files(root: Path, excludes=SCAN_EXCLUDES):
    exts = getattr(_LEAK, 'SCAN_EXTS', None) or _FALLBACK_EXTS
    for p in sorted(Path(root).rglob('*')):
        if not p.is_file():
            continue
        if any(part in excludes for part in p.parts):
            continue
        if p.name in SELF_OUTPUT_NAMES:
            continue
        if p.suffix.lower() not in exts:
            continue
        yield p


def _rel(path_str: str) -> str:
    try:
        return str(Path(path_str).resolve().relative_to(ROOT))
    except Exception:
        return str(path_str)


def audit_credentials(scan_root=None, excludes=SCAN_EXCLUDES, max_items=50) -> dict:
    root = Path(scan_root or ROOT)
    chain = {
        'chain': 'credentials',
        'scanner': {'module': 'scripts/leak_scan.py', 'available': _LEAK is not None,
                    'pattern_count': len(getattr(_LEAK, 'KEY_PATTERNS', []) or []),
                    'assign_pattern': bool(getattr(_LEAK, 'ASSIGN_PATTERN', None)),
                    'safe_values': len(getattr(_LEAK, 'SAFE_VALUES', ()) or ())},
        'scan': {'root': str(root), 'files_scanned': 0, 'raw_findings': 0,
                 'actionable': 0, 'whitelisted': 0, 'by_class': {}, 'items': []},
        'key_status': {'module': 'core/key_manager.py', 'available': _KEYS is not None,
                       'providers': 0, 'records': 0, 'by_status': {},
                       'open_circuits': [], 'fingerprints': [], 'thresholds': {}},
    }
    findings = []
    if _LEAK is not None and root.exists():
        for p in _iter_files(root, excludes):
            chain['scan']['files_scanned'] += 1
            _LEAK.scan_file(p, findings)
    chain['scan']['raw_findings'] = len(findings)
    by_class, items = Counter(), []
    for f in findings:
        klass = _classify(f.get('value', ''), f.get('file', ''))
        by_class[klass] += 1
        items.append({'file': _rel(f.get('file', '')), 'line': f.get('line'),
                      'pattern': f.get('pattern'), 'class': klass,
                      'value': _redact(f.get('value', ''), klass)})
    chain['scan']['by_class'] = dict(by_class)
    chain['scan']['actionable'] = by_class.get('actionable', 0)
    chain['scan']['whitelisted'] = chain['scan']['raw_findings'] - chain['scan']['actionable']
    items.sort(key=lambda x: (x['class'] != 'actionable', x['file'], x['line'] or 0))
    chain['scan']['items'] = items[:max_items]

    if _KEYS is not None:
        try:
            stats = _KEYS.KeyManager.instance().stats() or {}
            st = Counter()
            for provider, recs in sorted(stats.items()):
                for r in recs:
                    status = str(r.get('status', ''))
                    st[status] += 1
                    if status == getattr(_KEYS, 'S_CIRCUIT_OPEN', 'CIRCUIT_OPEN'):
                        chain['key_status']['open_circuits'].append(provider)
                    fp = str(r.get('key_fingerprint', ''))
                    if fp:
                        chain['key_status']['fingerprints'].append(f'{provider}: {fp}')
            chain['key_status']['providers'] = len(stats)
            chain['key_status']['records'] = sum(st.values())
            chain['key_status']['by_status'] = dict(st)
            chain['key_status']['thresholds'] = {
                'fail': getattr(_KEYS, 'FAIL_THRESHOLD', None),
                'circuit': getattr(_KEYS, 'CIRCUIT_THRESHOLD', None),
                'cooldown_s': getattr(_KEYS, 'CIRCUIT_COOLDOWN', None)}
        except Exception as e:
            chain['key_status']['error'] = type(e).__name__
    chain['verdict'] = 'fail' if chain['scan']['actionable'] else 'pass'
    return chain


# ── ② 抓取合规链 ──────────────────────────────────────────────────────────
def read_consent_log() -> dict:
    """读取 consent 台账；路径不可解析 / 目录不存在时降级返回空记录（不抛）。"""
    info = {'path': '', 'exists': False, 'lines': 0, 'grant': 0, 'revoke': 0,
            'malformed': 0, 'last': '', 'source': 'unavailable'}
    path = ''
    if _CAPS is not None:
        try:
            path = str(_CAPS.consent_log_path() or '')
        except Exception:
            path = ''
    if path:
        info['source'] = 'capability_registry'
    else:
        path = str(Path.home() / '.infoseek' / 'consent.log')
        info['source'] = 'home_fallback'
    info['path'] = path
    try:
        p = Path(path)
        if not p.exists():
            return info
        info['exists'] = True
        for raw in p.read_text(encoding='utf-8', errors='replace').splitlines():
            ln = raw.strip()
            if not ln:
                continue
            info['lines'] += 1
            parts = ln.split()
            if len(parts) >= 3 and parts[1] in ('grant', 'revoke'):
                info[parts[1]] += 1
                info['last'] = ln
            else:
                info['malformed'] += 1
    except Exception as e:
        info['read_error'] = type(e).__name__
    return info


def audit_crawl_compliance() -> dict:
    chain = {'chain': 'crawl_compliance',
             'registry': {'module': 'core/capability_registry.py', 'available': _CAPS is not None,
                          'declared': 'capabilities/registry.yaml', 'total': 0, 'by_kind': {},
                          'enabled_declared': 0, 'effective_enabled': 0},
             'consent': {'required': [], 'granted_runtime': [], 'unauthorized': [],
                         'declared_conflicts': []},
             'capabilities': [], 'consent_log': None}
    caps = []
    if _CAPS is not None:
        try:
            caps = list(_CAPS.list_capabilities())
        except Exception:
            caps = []

    def _flag(fn, name):
        if _CAPS is None or not hasattr(_CAPS, fn):
            return None
        try:
            return bool(getattr(_CAPS, fn)(name))
        except Exception:
            return None

    required, granted, unauthorized, conflicts = [], [], [], []
    for c in caps:
        name = str(c.get('name', ''))
        need = bool(c.get('requires_consent'))
        ok = _flag('consent_granted', name) if need else None
        eff = _flag('is_effective_enabled', name)
        chain['capabilities'].append({
            'name': name, 'kind': c.get('kind', ''), 'enabled': bool(c.get('enabled')),
            'requires_consent': need, 'consent_granted': ok,
            'effective_enabled': eff, 'network_boundary': c.get('network_boundary', ''),
            'env_override': _flag('_env_override', name)})
        if need:
            required.append(name)
            (granted if ok else unauthorized).append(name)
            if bool(c.get('enabled')):
                conflicts.append(name)
    chain['registry'].update({'total': len(caps),
                              'by_kind': dict(Counter(str(c.get('kind', '')) for c in caps)),
                              'enabled_declared': sum(1 for c in caps if c.get('enabled')),
                              'effective_enabled': sum(1 for c in chain['capabilities']
                                                       if c['effective_enabled'])})
    chain['consent'].update({'required': required, 'granted_runtime': granted,
                             'unauthorized': unauthorized, 'declared_conflicts': conflicts})
    chain['consent_log'] = read_consent_log()
    issues = len(conflicts) + chain['consent_log']['malformed']
    chain['verdict'] = 'pass' if issues == 0 else 'warn'
    return chain


# ── ③ 网络边界链 ──────────────────────────────────────────────────────────
def audit_network_boundary() -> dict:
    """仅做**声明校验**（check_all_declared，零网络）；不调用 available/preflight 探测。"""
    chain = {'chain': 'network_boundary', 'module': 'scripts/boundary_gate.py',
             'available': _BOUND is not None, 'mode': 'static_only', 'probe': False,
             'note': '只校验能力声明的边界/要求主机，不探测可达性（零网络）',
             'valid_boundaries': [], 'gate_enabled': None, 'checked': 0, 'ok': 0,
             'failed': 0, 'by_boundary': {}, 'issues': {},
             'report': NETWORK_REPORT_REL, 'report_exists': False, 'report_bytes': 0}
    res = []
    if _BOUND is not None:
        try:
            res = list(_BOUND.check_all_declared())
        except Exception:
            res = []
        chain['valid_boundaries'] = list(getattr(_BOUND, '_VALID_BOUNDARIES', ()) or ())
        try:
            chain['gate_enabled'] = bool(_BOUND.gate_enabled())
        except Exception:
            chain['gate_enabled'] = None
    chain['checked'] = len(res)
    chain['ok'] = sum(1 for r in res if r.get('ok'))
    chain['failed'] = chain['checked'] - chain['ok']
    chain['by_boundary'] = dict(Counter(str(r.get('boundary')) for r in res))
    chain['issues'] = {str(r.get('cap')): list(r.get('issues') or [])
                       for r in res if not r.get('ok')}
    rp = ROOT / NETWORK_REPORT_REL
    if rp.exists():
        chain['report_exists'] = True
        chain['report_bytes'] = rp.stat().st_size
    if not chain['checked']:
        chain['verdict'] = 'unknown'
    else:
        chain['verdict'] = 'pass' if chain['failed'] == 0 else 'warn'
    return chain


# ── ④ 版权来源链 ──────────────────────────────────────────────────────────
def audit_provenance() -> dict:
    p = ROOT / 'references' / 'trusted-sources.json'
    chain = {'chain': 'provenance', 'source': 'references/trusted-sources.json',
             'exists': p.exists(), 'version': '', 'schema': '', 'updated': '',
             'white_list': 0, 'kb_sources': 0, 'by_tier': {}, 'by_credibility': {},
             'by_type': {}, 'unverified': [], 'verdict': 'unknown'}
    data = {}
    if p.exists():
        try:
            data = json.loads(p.read_text(encoding='utf-8', errors='replace'))
        except Exception as e:
            chain['parse_error'] = type(e).__name__
    wl = data.get('white_list') or []
    kb = data.get('kb_sources') or []
    chain['version'] = str(data.get('version', ''))
    chain['schema'] = str(data.get('schema', data.get('dual_segment', '')))
    chain['updated'] = str(data.get('updated', ''))
    chain['white_list'] = len(wl)
    chain['kb_sources'] = len(kb)
    chain['by_tier'] = dict(Counter(str(x.get('tier')) for x in wl if isinstance(x, dict)))
    chain['by_credibility'] = dict(Counter(str(x.get('credibility')) for x in wl
                                           if isinstance(x, dict)))
    chain['by_type'] = dict(Counter(str(x.get('type')) for x in wl if isinstance(x, dict)))
    chain['unverified'] = [x.get('domain') for x in wl
                           if isinstance(x, dict) and not x.get('verified')][:20]
    ok = bool(p.exists() and wl and kb and chain['version'])
    chain['verdict'] = 'pass' if ok else 'warn'
    return chain


# ── 汇总与渲染 ────────────────────────────────────────────────────────────
def build_report(scan_root=None, excludes=SCAN_EXCLUDES) -> dict:
    report = {
        'tool': 'compliance_audit', 'version': AUDIT_VERSION,
        'generated_at': datetime.now().astimezone().isoformat(timespec='seconds'),
        'date': datetime.now().strftime('%Y-%m-%d'),
        'root': str(ROOT), 'chains': [],
    }
    report['chains'] = [
        audit_credentials(scan_root, excludes),
        audit_crawl_compliance(),
        audit_network_boundary(),
        audit_provenance(),
    ]
    verdicts = Counter(c['verdict'] for c in report['chains'])
    report['summary'] = dict(verdicts)
    report['actionable'] = next((c['scan']['actionable'] for c in report['chains']
                                 if c['chain'] == 'credentials'), 0)
    report['verdict'] = ('fail' if report['actionable'] or verdicts.get('fail')
                         else ('warn' if verdicts.get('warn') else 'pass'))
    return report


def _md_table(headers, rows) -> str:
    out = ['| ' + ' | '.join(headers) + ' |',
           '|' + '|'.join(['---'] * len(headers)) + '|']
    out += ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rows]
    return '\n'.join(out) + '\n'


def render_markdown(report: dict) -> str:
    ch = {c['chain']: c for c in report['chains']}
    cred, crawl, net, prov = (ch.get('credentials', {}), ch.get('crawl_compliance', {}),
                              ch.get('network_boundary', {}), ch.get('provenance', {}))
    scan = cred.get('scan', {})
    L = [f"# Infoseek 合规审计报告（v{report['version']}）\n",
         f"> 生成：{report['generated_at']} ｜ 根目录：`{report['root']}` ｜ "
         f"总判定：**{report['verdict']}**\n",
         "本报告由 `scripts/compliance_audit.py`（D-8 / P3-9 合规审计自动化）生成，"
         "四链均**只读复用**既有真源模块，不重复实现口径、不发网络请求。\n",
         '## 一、总览\n',
         _md_table(['链路', '真源模块', '判定', '要点'],
                   [['① 凭证审计', 'scripts/leak_scan.py + core/key_manager.py', cred.get('verdict', '?'),
                     f"扫描 {scan.get('files_scanned', 0)} 文件；可处置 {scan.get('actionable', 0)} / "
                     f"白名单 {scan.get('whitelisted', 0)}；key 记录 {cred.get('key_status', {}).get('records', 0)}"],
                    ['② 抓取合规', 'core/capability_registry.py + consent.log', crawl.get('verdict', '?'),
                     f"能力 {crawl.get('registry', {}).get('total', 0)} 项；需授权 "
                     f"{len(crawl.get('consent', {}).get('required', []))}；运行时已授权 "
                     f"{len(crawl.get('consent', {}).get('granted_runtime', []))}"],
                    ['③ 网络边界', 'scripts/boundary_gate.py（静态声明校验）', net.get('verdict', '?'),
                     f"校验 {net.get('checked', 0)} 能力；不通过 {net.get('failed', 0)}；"
                     f"分布 {net.get('by_boundary', {})}"],
                    ['④ 版权来源', 'references/trusted-sources.json', prov.get('verdict', '?'),
                     f"v{prov.get('version', '?')}；white_list {prov.get('white_list', 0)}；"
                     f"kb_sources {prov.get('kb_sources', 0)}"]]) + '\n',
         '## 二、① 凭证审计链\n',
         f"- 扫描器：`{cred.get('scanner', {}).get('module')}`（可用={cred.get('scanner', {}).get('available')}，"
         f"字面量模式 {cred.get('scanner', {}).get('pattern_count')} 条，白名单 "
         f"{cred.get('scanner', {}).get('safe_values')} 项）\n"
         f"- 扫描结果：{scan.get('files_scanned', 0)} 文件 / 命中 {scan.get('raw_findings', 0)}；"
         f"分级 {scan.get('by_class', {})}\n"
         f"- 可处置项：**{scan.get('actionable', 0)}**\n",
         _md_table(['文件', '行', '模式', '分级', '值'],
                   [[i['file'], i['line'], i['pattern'], i['class'], i['value']]
                    for i in scan.get('items', [])[:20]]) if scan.get('items')
         else '- 无扫描命中。\n',
         '\n- KeyManager 状态（脱敏指纹）：\n',
         _md_table(['项', '值'], [['可用', cred.get('key_status', {}).get('available')],
                                  ['providers', cred.get('key_status', {}).get('providers')],
                                  ['记录数', cred.get('key_status', {}).get('records')],
                                  ['状态分布', cred.get('key_status', {}).get('by_status', {})],
                                  ['熔断中', cred.get('key_status', {}).get('open_circuits', [])],
                                  ['阈值', cred.get('key_status', {}).get('thresholds', {})]]) + '\n',
         '## 三、② 抓取合规链\n',
         f"- 注册表：`{crawl.get('registry', {}).get('declared')}`（{crawl.get('registry', {}).get('total', 0)} 项，"
         f"声明启用 {crawl.get('registry', {}).get('enabled_declared', 0)}，"
         f"有效启用 {crawl.get('registry', {}).get('effective_enabled', 0)}）\n"
         f"- 需授权：{crawl.get('consent', {}).get('required', [])}\n"
         f"- 运行时已授权：{crawl.get('consent', {}).get('granted_runtime', [])}\n"
         f"- 未授权（默认关闭）：{crawl.get('consent', {}).get('unauthorized', [])}\n"
         f"- 声明冲突（启用∧需授权）：{crawl.get('consent', {}).get('declared_conflicts', [])}\n"
         f"- consent 台账：path=`{crawl.get('consent_log', {}).get('path')}` "
         f"存在={crawl.get('consent_log', {}).get('exists')} "
         f"grant={crawl.get('consent_log', {}).get('grant')} "
         f"revoke={crawl.get('consent_log', {}).get('revoke')} "
         f"格式异常={crawl.get('consent_log', {}).get('malformed')}\n",
         _md_table(['能力', '类别', '声明启用', '需授权', '已授权', '有效启用', '网络边界'],
                   [[c['name'], c['kind'], c['enabled'], c['requires_consent'],
                     c['consent_granted'], c['effective_enabled'], c['network_boundary']]
                    for c in crawl.get('capabilities', [])]) + '\n',
         '## 四、③ 网络边界链\n',
         f"- 模式：**{net.get('mode')}**（probe={net.get('probe')}）—— {net.get('note')}\n"
         f"- 校验结果：{net.get('checked', 0)} 项 / 通过 {net.get('ok', 0)} / 不通过 {net.get('failed', 0)}\n"
         f"- 边界分布：{net.get('by_boundary', {})}；合法值 {net.get('valid_boundaries', [])}\n"
         f"- 不通过明细：{net.get('issues', {})}\n"
         f"- 边界报告产物：`{net.get('report')}`（存在={net.get('report_exists')}，"
         f"{net.get('report_bytes', 0)} 字节）\n",
         '## 五、④ 版权来源链\n',
         f"- 台账：`{prov.get('source')}`（v{prov.get('version', '?')}，更新 {prov.get('updated')}）\n"
         f"- 规模：white_list {prov.get('white_list', 0)} / kb_sources {prov.get('kb_sources', 0)}\n"
         f"- 层级分布：{prov.get('by_tier', {})}\n"
         f"- 可信度分布：{prov.get('by_credibility', {})}\n"
         f"- 未验证条目：{prov.get('unverified', [])}\n",
         '## 六、结论\n',
         f"- 总判定 **{report['verdict']}**（各链：{report['summary']}）\n"
         f"- 可处置项：{report['actionable']}（actionable 凭证明文不落报告，仅记脱敏占位）\n"
         f"- 待办：可处置凭证需人工复核；consent 台账缺失属预期（默认关闭 + 无授权事件）\n"]
    return '\n'.join(L)


def write_report(out=None, json_out=None, report=None) -> dict:
    report = report or build_report()
    paths = {}
    if out:
        p = Path(out)
        if not p.is_absolute():
            p = ROOT / p
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(render_markdown(report), encoding='utf-8')
        paths['markdown'] = p
    if json_out:
        p = Path(json_out)
        if not p.is_absolute():
            p = ROOT / p
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        paths['json'] = p
    return paths


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description='Infoseek 合规审计自动化（四链只读审计）')
    ap.add_argument('--path', default=str(ROOT), help='凭证扫描根目录（默认仓库根）')
    ap.add_argument('--exclude', default=','.join(SCAN_EXCLUDES), help='排除目录（逗号分隔）')
    ap.add_argument('--out', default='', help=f'Markdown 报告输出（默认建议 {DEFAULT_REPORT_REL}）')
    ap.add_argument('--json-out', default='', help=f'JSON 报告输出（默认建议 {DEFAULT_JSON_REL}）')
    ap.add_argument('--json', action='store_true', help='stdout 输出 JSON')
    ap.add_argument('--strict', action='store_true', help='存在可处置项时退出码 1')
    args = ap.parse_args(argv)

    excludes = tuple(x.strip() for x in args.exclude.split(',') if x.strip())
    report = build_report(scan_root=args.path, excludes=excludes)
    if args.out or args.json_out:
        paths = write_report(args.out, args.json_out, report)
        for k, v in paths.items():
            print(f'{k} 报告已写入: {v}')
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"合规审计完成 | 判定 {report['verdict']} | 各链 {report['summary']} | "
              f"可处置 {report['actionable']}")
    if args.strict and (report['actionable'] or report.get('verdict') == 'fail'):
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())