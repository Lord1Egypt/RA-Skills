# 🌀 anti-loop v2.0

> **Lightweight anti-infinite-loop guard for LLM agents. Healing > Kill.**

```bash
pip install anti-loop
```

```python
from anti_loop import AntiLoop
guard = AntiLoop(mode="heal")
# That's it. 3 lines. 9 layers of protection.
```

[Full SKILL.md](./SKILL.md) | [clawhub](https://clawhub.ai/p/morgana-anti-infinite-loop-v2) | [GitHub](https://github.com/kofna336/anti-loop)

---

## Why v2.0?

v1 (modest reception) was just `max_iter` + `kill`. v2.0 is:

- **Predictive** (5-10 iter BEFORE the crash)
- **Healing** (injects system message, doesn't abort)
- **Zero-dep** (stdlib only, numpy optional)
- **Cross-harness** (Claude, OpenAI, Hermes, LangChain, AutoGen, custom)
- **9 layers** (entropy, novelty, taxonomy, healing, self-tuning, breath, pre-flight, DNA, adapters)

**1 install = 6+ layers of protection, zero setup.**

## Quickstart

```python
from anti_loop import AntiLoop

# 1. Init
guard = AntiLoop(mode="heal", max_iter=10)

# 2. Observe (in your agent loop)
result = guard.observe(
    action=last_action_text,
    intent=original_user_intent,
)

# 3. Intervene if needed
if result["intervene"]:
    if result["directive"]["action"] == "heal":
        inject_system_message(result["directive"]["system_message"])
    elif result["directive"]["action"] == "pause":
        time.sleep(result["directive"]["duration_seconds"])
    elif result["directive"]["action"] == "abort":
        raise LoopDetectedError()
```

## Optional extras

```bash
pip install anti-loop[embeddings]     # numpy TF-IDF fallback
pip install anti-loop[kan]            # KAN advanced (torch)
pip install anti-loop[multi-agent]    # DFS deadlock graph
pip install anti-loop[all]            # full power
```

## CLI

```bash
anti-loop --demo                       # See the guard in action
anti-loop --check-plan "if X then X"   # Pre-flight check
```

## License

MIT. From Axioma Stellaris with 💜.
