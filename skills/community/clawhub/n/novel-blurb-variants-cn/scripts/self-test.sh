#!/bin/sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
fail() { printf '%s\n' "SELF-TEST FAILED: $1" >&2; exit 1; }

for file in SKILL.md manifest.yaml agents/openai.yaml README.md README.en.md LICENSE fixtures/success.json fixtures/failure-missing-type.json assets/icon-512.png assets/promo-1600x900.png; do
  [ -f "$root/$file" ] || fail "missing $file"
done

command -v python3 >/dev/null 2>&1 || fail "python3 is required for structural checks"
ROOT="$root" python3 - <<'PY'
import json, os, struct
from pathlib import Path

root = Path(os.environ['ROOT'])
manifest = (root / 'manifest.yaml').read_text(encoding='utf-8')
for key in ('slug:', 'repository:', 'short_description:', 'self_test:', 'triggers:'):
    assert key in manifest, f'manifest missing {key}'
assert 'https://github.com/xxjrq/novel-blurb-variants-cn' in manifest
assert 'sh scripts/self-test.sh' in manifest
short_desc = next(line.split(':', 1)[1].strip().strip('"') for line in manifest.splitlines() if line.startswith('short_description:'))
assert 25 <= len(short_desc) <= 64, 'short_description must be 25–64 characters'
assert manifest.count('  - "') >= 7, 'manifest needs at least four tags and three triggers'
skill = (root / 'SKILL.md').read_text(encoding='utf-8')
assert skill.startswith('---\n') and 'name: novel-blurb-variants-cn' in skill
ui = (root / 'agents/openai.yaml').read_text(encoding='utf-8')
assert 'display_name: "小说简介与封底文案"' in ui
ok = json.loads((root / 'fixtures/success.json').read_text(encoding='utf-8'))
bad = json.loads((root / 'fixtures/failure-missing-type.json').read_text(encoding='utf-8'))
required = {'故事梗概', '类型', '禁剧透点'}
assert required <= set(ok), 'success fixture must contain all required inputs'
assert required - set(bad) == {'类型'}, 'failure fixture must isolate missing 类型'
assert '可公开的结局范围' in ok['故事梗概'], 'success synopsis must state its public ending range'
assert '可公开的结局范围' in bad['故事梗概'], 'failure synopsis must be complete except for 类型'

expected = ok.get('expected_output')
assert isinstance(expected, dict), 'success fixture needs expected_output'
sections = expected.get('required_sections')
assert sections == ['已知信息', '版本一｜情绪与人物', '版本二｜冲突与类型', '版本三｜主题与气质', '一句卖点'], 'success expected sections do not match SKILL.md'
variants = expected.get('variants')
assert isinstance(variants, list) and len(variants) == 3, 'success needs three expected variants'
assert [v.get('section') for v in variants] == sections[1:4], 'variant sections must match output format'
assert all(v.get('length_chars') == [120, 220] and v.get('focus') for v in variants), 'each variant needs focus and 120–220 character boundary'
assert expected.get('selling_point', {}).get('length_chars') == [18, 36], 'selling point must specify 18–36 characters'
assert expected.get('selling_point', {}).get('must_be_spoiler_safe') is True, 'selling point must be spoiler-safe'
assert expected.get('must_not_reveal') == ok['禁剧透点'], 'spoiler contract must mirror input boundaries'
assert expected.get('must_not_invent_story_facts') is True, 'success contract must prohibit invented facts'

error = bad.get('expected_error')
assert isinstance(error, dict), 'failure fixture needs expected_error'
assert error.get('missing_fields') == ['类型'], 'failure expected error must name only 类型'
assert error.get('must_not_request_fields') == ['故事梗概', '禁剧透点'], 'failure must not re-request supplied fields'
rules = error.get('response_rules')
assert isinstance(rules, list) and len(rules) >= 3, 'failure needs response behavior rules'
assert '只指出缺少的字段并请用户补充' in rules, 'failure must require a missing-field reply'
assert '不得编造故事事实' in rules, 'failure must prohibit invented facts'
for rel, expected in [('assets/icon-512.png', (512, 512)), ('assets/promo-1600x900.png', (1600, 900))]:
    raw = (root / rel).read_bytes()
    assert raw[:8] == b'\x89PNG\r\n\x1a\n', f'{rel} is not PNG'
    width, height = struct.unpack('>II', raw[16:24])
    assert (width, height) == expected, f'{rel} is {width}x{height}, expected {expected}'
print('Structure validation: PASS')
print('Fixture contract validation: PASS (success specifies three variants, selling point, and spoiler bounds; failure isolates 类型)')
print('Behavior validation: NOT AUTOMATED — model output must be reviewed against fixture contracts for factual fidelity and spoiler control.')
PY
