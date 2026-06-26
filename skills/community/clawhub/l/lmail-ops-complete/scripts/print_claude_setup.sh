#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cat <<EOF2
Claude Code setup (manual, reliable):

1) Keep the skill at:
   $SKILL_DIR

2) In your Claude prompt, invoke it explicitly:
   Use \$lmail-ops-complete at $SKILL_DIR to operate LMail end-to-end.

3) Optional: add this snippet to your project-level CLAUDE.md:
   - Skill path: $SKILL_DIR
   - For LMail tasks, read SKILL.md then run scripts from scripts/.

4) Recommended start commands:
   python3 $SKILL_DIR/scripts/login_verify.py --base-url https://amiigzz.online
   python3 $SKILL_DIR/scripts/inbox_loop.py --base-url https://amiigzz.online --max-iterations 1
EOF2
