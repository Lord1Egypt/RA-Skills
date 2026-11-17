#!/usr/bin/env python3
"""
tests/test_conflict_weight.py — 冲突检测多源加权回归（P1-2 G2 修复，v2.5.0）

覆盖：
- W1 domain_of URL 解析（协议/www/路径剥离）
- W2 load_credibility_map 白名单映射（trusted-sources.json ≥29 条）
- W3 source_credibility 命中/未命中（命中→credibility；未知→默认 50）
- W4 weight_conflict 高可信升档（max_cred≥80 → severity +1）
- W5 weight_conflict 低可信标记（min_cred<40 → low_evidence=True，不降级）
- W6 INFOSEEK_CONFLICT_WEIGHT=0 关闭（无加权字段）
- W7 端到端：ConflictMonitor finalize 输出含加权字段
"""

import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'core'))

os.environ['INFOSEEK_DATA_DIR'] = tempfile.mkdtemp(prefix='infoseek_confw_')
os.environ['INFOSEEK_CONFLICT_WEIGHT'] = '1'

from core.conflict_weight import (  # noqa: E402
    domain_of, enabled, load_credibility_map, source_credibility,
    weight_conflict, DEFAULT_CREDIBILITY, HIGH_CRED,
)
from core.conflict_v3 import ConflictMonitor  # noqa: E402

_fails = []


def _check(name, cond, detail=''):
    if cond:
        print(f"  [PASS] {name}")
    else:
        _fails.append(name)
        print(f"  [FAIL] {name} {detail}")


# 已知高可信域（trusted-sources.json 内含）
_HIGH_URL = 'https://ccia.xin/article/1'           # 中国复合材料工业协会 credibility=95


def _make_claim(entity, url, text):
    return {
        'entity_name': entity,
        'mention': entity,
        'source': url,
        'source_title': 'T',
        'text': text,
    }


def main():
    # W1 domain_of
    print('--- W1 domain_of ---')
    _check('协议剥离', domain_of('https://ccia.xin/a/b') == 'ccia.xin')
    _check('www 剥离', domain_of('http://www.example.com/p') == 'example.com')
    _check('无协议', domain_of('example.com/x') == 'example.com')
    _check('空输入', domain_of('') == '')

    # W2 白名单映射
    print('--- W2 load_credibility_map ---')
    cm = load_credibility_map(force=True)
    _check('白名单非空(≥29)', len(cm) >= 29, f'len={len(cm)}')
    _check('ccia.xin→95', cm.get('ccia.xin') == 95, str(cm.get('ccia.xin')))

    # W3 source_credibility
    print('--- W3 source_credibility ---')
    _check('命中返回 credibility', source_credibility(_HIGH_URL) == 95)
    _check('未命中默认 50', source_credibility('https://unknown-xyz-abc.com/p') == DEFAULT_CREDIBILITY)

    # W4 高可信升档
    print('--- W4 高可信升档 ---')
    c1 = {
        'severity': 'low',
        'claim_a': {'source': _HIGH_URL},
        'claim_b': {'source': 'https://other.com/x'},
    }
    weight_conflict(c1)
    _check('low→medium 升档', c1['severity'] == 'medium', c1['severity'])
    _check('加权字段', c1.get('weighted') is True and c1.get('max_cred') == 95, str(c1.get('max_cred')))
    _check('sources_cred 结构', len(c1.get('sources_cred', [])) == 2)

    # W5 低可信标记
    print('--- W5 低可信标记 ---')
    c2 = {
        'severity': 'high',
        'claim_a': {'source': 'https://a-unknown-1.com/x'},
        'claim_b': {'source': 'https://b-unknown-2.com/y'},
    }
    weight_conflict(c2)
    _check('low_evidence=True', c2.get('low_evidence') is True)
    _check('high 不降级', c2['severity'] == 'high', c2['severity'])
    _check('双方未知 known=False',
           all(not s['known'] for s in c2.get('sources_cred', [])),
           str(c2.get('sources_cred')))

    # W6 关闭开关
    print('--- W6 开关关闭 ---')
    os.environ['INFOSEEK_CONFLICT_WEIGHT'] = '0'
    c3 = {'severity': 'medium',
          'claim_a': {'source': _HIGH_URL},
          'claim_b': {'source': 'https://other.com/x'}}
    weight_conflict(c3)
    _check('severity 不变', c3['severity'] == 'medium', c3['severity'])
    _check('无 weighted 字段', 'weighted' not in c3)
    os.environ['INFOSEEK_CONFLICT_WEIGHT'] = '1'

    # W7 端到端 finalize
    print('--- W7 端到端 finalize ---')
    mon = ConflictMonitor()
    mon.session_claims = [
        _make_claim('OpenAI', _HIGH_URL, 'OpenAI 模型推理成本下降 30%'),
        _make_claim('OpenAI', 'https://unknown-blog-9.com/x', 'OpenAI 模型推理成本上升 50%'),
    ]
    result = mon.finalize(subject='OpenAI')
    _check('冲突检出', len(result.get('conflicts', [])) >= 1, str(len(result.get('conflicts', []))))
    if result.get('conflicts'):
        cc = result['conflicts'][0]
        _check('输出含 weighted', cc.get('weighted') is True)
        _check('输出含 max_cred', cc.get('max_cred') == 95, str(cc.get('max_cred')))
        _check('输出含 sources_cred', len(cc.get('sources_cred', [])) == 2)

    # W7b 关闭开关端到端
    os.environ['INFOSEEK_CONFLICT_WEIGHT'] = '0'
    mon2 = ConflictMonitor()
    mon2.session_claims = [
        _make_claim('OpenAI', _HIGH_URL, '推理成本降 30%'),
        _make_claim('OpenAI', 'https://unknown-blog-9.com/x', '推理成本升 50%'),
    ]
    r2 = mon2.finalize(subject='OpenAI')
    _check('关闭时无加权', r2.get('conflicts') and 'weighted' not in r2['conflicts'][0])
    os.environ['INFOSEEK_CONFLICT_WEIGHT'] = '1'

    # W8 mtime 感知缓存（L1, v1.7.1 PATCH：消除与 trusted_kb 实时读文件的缓存不对称）
    print('--- W8 mtime 感知缓存 ---')
    import core.conflict_weight as cw_mod
    _orig_core_dir = cw_mod.CORE_DIR
    _tmp_root = Path(tempfile.mkdtemp(prefix='infoseek_mtime_'))
    (_tmp_root / 'references').mkdir(parents=True, exist_ok=True)
    _tmp_json = _tmp_root / 'references' / 'trusted-sources.json'

    def _write_tmp(srcs, mtime_sec):
        _tmp_json.write_text(json.dumps({'version': 't', 'sources': srcs}, ensure_ascii=False),
                             encoding='utf-8')
        os.utime(_tmp_json, (mtime_sec, mtime_sec))  # 显式 mtime，规避同秒精度

    cw_mod.CORE_DIR = _tmp_root / 'core'
    try:
        _write_tmp([{'domain': 'alpha.com', 'credibility': 60}], 1_000_000_000)
        m1 = cw_mod.load_credibility_map(force=True)
        _check('W8a 初始加载', m1.get('alpha.com') == 60, str(m1))
        _check('W8b 未改走缓存(同对象)', cw_mod.load_credibility_map() is m1)
        _write_tmp([{'domain': 'alpha.com', 'credibility': 90}], 1_000_000_100)
        m2 = cw_mod.load_credibility_map()
        _check('W8c 热改自动重载(新值+新对象)', m2.get('alpha.com') == 90 and m2 is not m1, str(m2))
        _check('W8d 重载后再走缓存', cw_mod.load_credibility_map() is m2)
        _write_tmp([{'domain': 'alpha.com', 'credibility': 70}], 1_000_000_200)
        _check('W8e force 强制重载', cw_mod.load_credibility_map(force=True).get('alpha.com') == 70)
        # 删除 → 空映射；重建 → mtime None→float 触发重载
        _tmp_json.unlink()
        _check('W8f 文件删除→空映射', cw_mod.load_credibility_map() == {})
        _write_tmp([{'domain': 'beta.com', 'credibility': 55}], 1_000_000_300)
        m4 = cw_mod.load_credibility_map()
        _check('W8g 重建文件触发重载', m4.get('beta.com') == 55 and 'alpha.com' not in m4, str(m4))
    finally:
        cw_mod.CORE_DIR = _orig_core_dir
        cw_mod._CRED_CACHE = None
        cw_mod._CRED_CACHE_MTIME = None

    print()
    if _fails:
        print(f"FAIL: {len(_fails)} 项失败 → {_fails}")
        sys.exit(1)
    print("ALL PASS (test_conflict_weight) ✅")
    sys.exit(0)


if __name__ == '__main__':
    main()