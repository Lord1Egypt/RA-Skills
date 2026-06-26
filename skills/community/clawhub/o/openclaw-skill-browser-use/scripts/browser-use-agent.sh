#!/bin/bash
# browser-use-agent.sh — Standalone wrapper (same as installed /usr/local/bin/browser-use-agent)
# Can be run directly from the skill directory without global install.
# Usage: ./browser-use-agent.sh "task description" [--model MODEL] [--max-steps N]
set -euo pipefail

VENV_DIR="${BROWSER_USE_VENV:-/opt/browser-use}"
TASK="${1:?Usage: $0 \"task description\" [--model MODEL] [--max-steps N]}"
shift

MODEL="gpt-4o-mini"
MAX_STEPS=12

while [[ $# -gt 0 ]]; do
    case "$1" in
        --model) MODEL="$2"; shift 2 ;;
        --max-steps) MAX_STEPS="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

if [ -z "${OPENAI_API_KEY:-}" ] && [ -f "/root/.openclaw/openclaw.json" ]; then
    export OPENAI_API_KEY=$(python3 -c "import json; print(json.load(open('/root/.openclaw/openclaw.json'))['models']['providers']['openai']['apiKey'])" 2>/dev/null || true)
fi
if [ -z "${ANTHROPIC_API_KEY:-}" ] && [ -f "/root/.openclaw/openclaw.json" ]; then
    export ANTHROPIC_API_KEY=$(python3 -c "import json; print(json.load(open('/root/.openclaw/openclaw.json'))['models']['providers']['anthropic']['apiKey'])" 2>/dev/null || true)
fi

if [[ "$MODEL" == claude* ]] || [[ "$MODEL" == anthropic* ]]; then
    LLM_IMPORT="from langchain_anthropic import ChatAnthropic"
    LLM_INIT="ChatAnthropic(model='$MODEL', api_key=os.environ['ANTHROPIC_API_KEY'])"
else
    LLM_IMPORT="from langchain_openai import ChatOpenAI"
    LLM_INIT="ChatOpenAI(model='$MODEL', api_key=os.environ['OPENAI_API_KEY'])"
fi

cat > /tmp/_bu_task.py << PYEOF
import asyncio, os
$LLM_IMPORT
from browser_use import Agent

async def run():
    llm = $LLM_INIT
    agent = Agent(task="""$TASK""", llm=llm)
    result = await agent.run(max_steps=$MAX_STEPS)
    final = result.final_result()
    if final:
        print(final.extracted_content if hasattr(final, 'extracted_content') else str(final))
    else:
        for r in result.all_results:
            if r.extracted_content:
                print(r.extracted_content)

asyncio.run(run())
PYEOF

xvfb-run "$VENV_DIR/bin/python3" /tmp/_bu_task.py
