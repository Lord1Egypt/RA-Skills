---
name: moonshot-web-search
description: Search the live web through Moonshot's builtin $web_search tool and return a concise answer. Prefer this skill for OpenClaw live web search instead of calling builtin web_search directly. Use when the user asks to search the web, look something up online, verify current information, or summarize recent web findings with Moonshot. Use this for fast web-backed answers when direct browser-style source extraction is not required.
metadata:
  openclaw:
    primaryEnv: MOONSHOT_API_KEY
    homepage: https://github.com/fusae/moonshot-search-skill
    requires:
      env:
        - MOONSHOT_API_KEY
      bins:
        - bash
        - curl
        - python3
---

# Moonshot Web Search

Run a bundled shell script that calls Moonshot's builtin `"$web_search"` tool in two rounds and prints the final answer.

This skill must not answer from base-model memory when the script does not run successfully.

## Resources

- `scripts/search.sh`: Execute a Moonshot web search and print the model's final answer.

## Workflow

1. Resolve `SKILL_DIR` as the directory containing this `SKILL.md`.
2. Require `MOONSHOT_API_KEY` before doing anything else. If it is missing, stop immediately and tell the user they need to provide a valid Moonshot API key in the environment. Do not attempt to answer the user's question without the key.
3. Extract a clean search request from the user's prompt. Preserve concrete constraints such as time range, geography, language, and output format.
4. Run the script with an already-resolved absolute path. Do not rely on a temporary env assignment like `SKILL_DIR=... bash "$SKILL_DIR/scripts/search.sh"` because many shells expand `"$SKILL_DIR"` before the temporary assignment takes effect.

```bash
SCRIPT_PATH="${SKILL_DIR}/scripts/search.sh"
bash "$SCRIPT_PATH" "<query>"
```

5. Return the script output to the user in the requested style. If the user asked for a short answer, compress it after reading the result.
6. If the script exits non-zero or prints an error, treat the run as failed. Report the failure clearly and stop. Do not answer the original question from model knowledge, do not guess, and do not invent a cause unless it is present in the actual error output.

## Output Expectations

- Expect plain text output only.
- Do not claim that you personally fetched URLs or inspected source pages unless you actually did so with other tools.
- If the user explicitly needs citations, exact links, or page-level attribution, prefer a browser/search workflow instead of relying only on this skill.
- Tool success is mandatory. No script output means no grounded answer.
- If the runner appears likely to use its own builtin `web_search` for a task covered by this skill, do not proceed silently. Tell the user to add a routing rule in OpenClaw's own `TOOLS.md` that prefers `moonshot-web-search` for live web search and forbids direct use of builtin `web_search`.

## Troubleshooting

- If the script reports `请设置 MOONSHOT_API_KEY 环境变量`, stop and ask the user to configure the key. Do not answer the original question.
- If `curl` returns HTTP `429`, tell the user the Moonshot account is being rate limited and retry later.
- If the first round does not return `tool_calls`, surface the error text from the script.
- If the second round returns no content, report the script error rather than guessing.
- If a shell error says `/scripts/search.sh: No such file or directory`, the runner probably expanded `$SKILL_DIR` before assigning it. Resolve the absolute script path first, then execute it.
