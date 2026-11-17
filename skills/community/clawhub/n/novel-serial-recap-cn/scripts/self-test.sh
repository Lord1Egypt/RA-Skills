#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

fail() { printf 'SELF-TEST FAILED: %s\n' "$*" >&2; exit 1; }
need_file() { [[ -f "$1" ]] || fail "missing file: $1"; }

# Structural validation: packaging fields and the Bash-invoked self-test.
for path in SKILL.md manifest.yaml agents/openai.yaml README.md README.zh-CN.md LICENSE \
  fixtures/success-input.md fixtures/failure-missing-goal.md assets/icon-512.png assets/promo-1600x900.png; do
  need_file "$path"
done
[[ -f scripts/self-test.sh && -r scripts/self-test.sh ]] || fail "self-test must be readable and is invoked with bash"
bash -n scripts/self-test.sh || fail "self-test must be valid Bash"
rg -q '^name: novel-serial-recap-cn$' SKILL.md || fail "SKILL.md name mismatch"
rg -q '^slug: "novel-serial-recap-cn"$' manifest.yaml || fail "manifest slug mismatch"
rg -q '^display_name: "连载前情摘要"$' manifest.yaml || fail "manifest display name mismatch"
rg -q '^license: "MIT-0"$' manifest.yaml || fail "manifest license must be MIT-0"
rg -q 'MIT No Attribution' LICENSE || fail "LICENSE must declare MIT-0"
rg -q '\[MIT-0\]\(LICENSE\)' README.md || fail "README license label must match MIT-0"
rg -q '\[MIT-0\]\(LICENSE\)' README.en.md || fail "English README license label must match MIT-0"
rg -q '\[MIT-0\]\(LICENSE\)' README.zh-CN.md || fail "Chinese README license label must match MIT-0"
rg -q '^repository: "https://github.com/xxjrq/novel-serial-recap-cn"$' manifest.yaml || fail "manifest repository mismatch"
rg -q '^self_test: "bash scripts/self-test.sh"$' manifest.yaml || fail "manifest self_test mismatch"
rg -q '^  - "中文小说"$' manifest.yaml || fail "manifest tags missing"
rg -q '^  - "整理连载前情"$' manifest.yaml || fail "manifest triggers missing"
rg -q '^  display_name: "连载前情摘要"$' agents/openai.yaml || fail "agent display name mismatch"

python3 - <<'PY'
from pathlib import Path
import struct
for name, expected in [('assets/icon-512.png', (512, 512)), ('assets/promo-1600x900.png', (1600, 900))]:
    data = Path(name).read_bytes()
    if data[:8] != b'\x89PNG\r\n\x1a\n':
        raise SystemExit(f'{name}: not a PNG')
    width, height = struct.unpack('>II', data[16:24])
    if (width, height) != expected:
        raise SystemExit(f'{name}: expected {expected}, got {(width, height)}')
manifest = Path('manifest.yaml').read_text(encoding='utf-8')
short = next(line.split('"', 2)[1] for line in manifest.splitlines() if line.startswith('short_description:'))
if not 25 <= len(short) <= 64:
    raise SystemExit(f'short_description must be 25–64 characters, got {len(short)}')
PY

# Fixture behavior validation: the skill's input contract is demonstrable without
# pretending to implement text-generation logic in a test harness.
rg -q '^## 上几章材料$' fixtures/success-input.md || fail "success fixture lacks chapter material"
rg -q '^## 下一章目标$' fixtures/success-input.md || fail "success fixture lacks next-chapter goal"
rg -q '^## 预期处理$' fixtures/failure-missing-goal.md || fail "failure fixture lacks expected handling"
rg -q '缺少.*下一章目标' fixtures/failure-missing-goal.md || fail "failure fixture does not require a missing-field response"

printf 'SELF-TEST PASSED: structure and fixtures validated.\n'
printf 'NOTE: This test does not claim to verify generative quality; real behavior requires a model run using SKILL.md.\n'
