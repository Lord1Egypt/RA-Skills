#!/bin/bash
cd "$(dirname "$0")" || exit 1
set -e
echo "Starting Kit Deployment..."
bash deploy.sh --no-restart

for skill_deploy_script in skills/*/deploy.sh; do
    if [ -f "$skill_deploy_script" ]; then
        bash "$skill_deploy_script" --no-restart
    fi
done

if [ -z "$HOME_MOCK" ]; then
    echo "🔄 Restarting OpenClaw gateway for Kit..."
    openclaw gateway restart || echo "⚠️ Gateway restart failed or not available."
fi
echo "✅ Kit deployment complete."
