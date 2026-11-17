#!/usr/bin/env bash
set -Eeuo pipefail
cd "$(dirname "$0")/.."
bash -n scripts/todo-read.sh
python3 - <<'PY'
from pathlib import Path
import yaml
text=Path('SKILL.md').read_text()
assert text.startswith('---\n')
fm=yaml.safe_load(text.split('---',2)[1])
assert fm['name']=='outlook-todo'
print('frontmatter ok')
PY
printf 'outlook-todo offline tests ok\n'
