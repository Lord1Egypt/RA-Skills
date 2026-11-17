# Nous Model Deal Router

A shareable [Hermes Agent](https://github.com/NousResearch/hermes-agent) skill that recommends the best-value **Nous Portal** model for a task, including temporary Portal promotions—while requiring explicit approval before it changes anything.

## What it does

- Refreshes or inspects live Nous Portal pricing instead of relying on stale prices.
- Distinguishes a real promotion (visible discount / “was” price) from cache pricing.
- Chooses the least-expensive model that clears the task's capability floor.
- Explains one recommendation and one cheaper alternative.
- Requires affirmative approval before changing a default model or an active session.

## Install

```bash
hermes skills install https://raw.githubusercontent.com/sknewcomb/nous-model-deal-router/main/SKILL.md
```

Or copy `SKILL.md` into your Hermes skills directory:

```text
~/.hermes/skills/autonomous-ai-agents/nous-model-deal-router/SKILL.md
```

## Example

> Use the model deal router: check the current Nous sale pricing and recommend the best value for agentic coding. Don't switch until I approve.

The skill will inspect the current Portal evidence, recommend a suitable model and a lower-cost alternative, then ask before modifying your configuration.

## License

MIT. See [LICENSE](LICENSE).
