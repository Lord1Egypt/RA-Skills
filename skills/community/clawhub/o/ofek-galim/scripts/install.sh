#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE_DEFAULT="$HOME/.openclaw/workspace/.env/webtop-galim.env"
CALENDAR_DEFAULT="primary"
GROUP_DEFAULT="YOUR_WHATSAPP_GROUP_ID"
SA_DEFAULT="$HOME/.openclaw/workspace/.secrets/google-sa.json"

mkdir -p "$(dirname "$ENV_FILE_DEFAULT")"

if [ ! -f "$ENV_FILE_DEFAULT" ]; then
  cat > "$ENV_FILE_DEFAULT" <<EOF
# Ofek / Galim local configuration
# Fill these values before running the skill in production.

GALIM_NAME_CHILD1="Child 1"
GALIM_USERNAME_CHILD1=
GALIM_PASSWORD_CHILD1=
GALIM_NAME_CHILD2="Child 2"
GALIM_USERNAME_CHILD2=
GALIM_PASSWORD_CHILD2=

OFEK_NAME_CHILD1="Child 1"
OFEK_USERNAME_CHILD1=
OFEK_PASSWORD_CHILD1=
OFEK_NAME_CHILD2="Child 2"
OFEK_USERNAME_CHILD2=
OFEK_PASSWORD_CHILD2=

OFEK_GALIM_CALENDAR_ID=$CALENDAR_DEFAULT
OFEK_GALIM_WHATSAPP_GROUP=$GROUP_DEFAULT
GOOGLE_SA_FILE=$SA_DEFAULT
EOF
  chmod 600 "$ENV_FILE_DEFAULT"
  echo "Created env template: $ENV_FILE_DEFAULT"
else
  echo "Env file already exists: $ENV_FILE_DEFAULT"
fi

cat <<EOF

Installation complete ✅

Next steps:
1. Edit the env file:
   $ENV_FILE_DEFAULT
2. Export child credentials for scripts that expect OFEK_KIDS_JSON, for example:
   export OFEK_KIDS_JSON='[
     {"name":"Child 1","username":"STUDENT_ID_1","password":"PASSWORD_1"},
     {"name":"Child 2","username":"STUDENT_ID_2","password":"PASSWORD_2"}
   ]'
3. Test the scripts:
   python3 "$SKILL_DIR/scripts/fetch_tasks.py"
   python3 "$SKILL_DIR/scripts/galim_fetch_tasks.py"
   python3 "$SKILL_DIR/scripts/unified_report.py"
4. Optional calendar sync:
   python3 "$SKILL_DIR/scripts/sync_galim_calendar.py" --days 30

Tip:
- Source your env file before use:
  set -a; . "$ENV_FILE_DEFAULT"; set +a
EOF
