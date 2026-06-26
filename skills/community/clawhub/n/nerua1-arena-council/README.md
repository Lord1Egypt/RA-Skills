# arena-council

OpenClaw/Claude Code skill: Multi-Model Council — parallel execution of multiple local LLMs with voting/consensus for higher quality responses.

## What it does

Instead of asking one model, ask 3-5 models in parallel and combine answers via voting strategies (weighted, majority, best-of).

```python
from scripts.council import council_decide

result = council_decide(
    "Review this code for security issues",
    models=['huihui-qwen3.5-27b', 'hauhaucs-35b', 'qwen9b'],
    strategy="weighted"
)
```

Works with any models running on LM Studio (`http://127.0.0.1:1234/v1`).

## Install

```bash
npx clawhub install arena-council
# or
git clone https://github.com/nerua1/arena-council ~/.openclaw/workspace/skills/arena-council
```

See `SKILL.md` for full documentation.

---

If this saved you time: [☕ PayPal.me/nerudek](https://www.paypal.me/nerudek)
