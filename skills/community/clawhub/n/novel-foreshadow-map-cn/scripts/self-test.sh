#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"
required=(SKILL.md manifest.yaml agents/openai.yaml README.md README.en.md LICENSE scripts/self-test.sh fixtures/success.md fixtures/failure.md assets/icon-512.png assets/promo-1600x900.png)
for path in "${required[@]}"; do
  [[ -f "$path" ]] || { echo "missing: $path" >&2; exit 1; }
done
python3 - <<'PY'
from pathlib import Path
import struct
def png_size(path):
    raw = Path(path).read_bytes()
    assert raw[:8] == b'\x89PNG\r\n\x1a\n', f'{path}: not a PNG'
    return struct.unpack('>II', raw[16:24])
assert png_size('assets/icon-512.png') == (512, 512), 'icon must be 512x512'
assert png_size('assets/promo-1600x900.png') == (1600, 900), 'promo must be 1600x900'
skill = Path('SKILL.md').read_text()
manifest = Path('manifest.yaml').read_text()
agent = Path('agents/openai.yaml').read_text()
assert 'name: novel-foreshadow-map-cn' in skill
assert 'name: novel-foreshadow-map-cn' in manifest and 'slug: novel-foreshadow-map-cn' in manifest
assert 'self_test: bash scripts/self-test.sh' in manifest
assert 'allow_implicit_invocation: true' in agent
assert 25 <= len('从章节材料提取伏笔并追踪埋点、兑现状态与建议回收位置') <= 64
for fixture in ('fixtures/success.md', 'fixtures/failure.md'):
    assert '| ID |' in Path(fixture).read_text(), f'{fixture}: missing delivery table'
allowed_statuses = {'已兑现', '待兑现', '待确认'}
for fixture in ('fixtures/success.md', 'fixtures/failure.md', 'fixtures/forward-success.md', 'fixtures/forward-failure.md', 'fixtures/forward-additional.md'):
    rows = [line for line in Path(fixture).read_text().splitlines() if line.strip().startswith('| F-')]
    assert rows, f'{fixture}: missing clue rows'
    for line in rows:
        cells = [cell.strip() for cell in line.strip().strip('|').split('|')]
        assert len(cells) == 7, f'{fixture}: invalid clue row'
        assert cells[4] in allowed_statuses, f'{fixture}: invalid status {cells[4]!r}'
failure_rows = [[c.strip() for c in line.strip().strip('|').split('|')] for line in Path('fixtures/failure.md').read_text().splitlines() if line.strip().startswith('| F-')]
warning = next(row for row in failure_rows if row[1] == '未署名纸条')
assert warning[4] == '待兑现', 'verifiable warning has no payoff in supplied scene'
assert '当前材料范围内' in warning[6], 'scope qualifier belongs in notes'
print('self-test passed: structure, fixtures, and image dimensions are valid')
PY
