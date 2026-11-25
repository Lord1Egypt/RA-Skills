# Model Selection

Default behavior: omit `models` and let mumo select the panel. mumo's defaults evolve as model quality and pricing change. Hardcoded model strategy in the skill will go stale.

## Family names

A family name works wherever a model ID does: `"claude"`, `"gpt"`, `"gemini"`, `"grok"`, and so on. It resolves to that family's default model on the user's plan. The ack names the model it chose and, when the plan has another model in that family, one alternative. Use a family name when the user names a lab but not a model.

## When to call `list_models`

`list_models` sorts models by what the caller can use: available on their plan, available on a higher plan, and unavailable right now, grouped by family, with each family's default marked.

- The user names one specific model.
- The user asks for a cheap gut-check or a premium panel.
- A previous call failed because a model was unavailable.
- The user asks what their plan includes.

## Selection principles

When selecting yourself:

- **Provider diversity over intra-family differences.** A panel with models from three different providers is more valuable than three variants from one.
- **Include your own family only when the user wants it** or the comparison specifically benefits from it. You're already in the conversation as moderator.
- **Avoid nano/fast variants for high-stakes decisions** unless the user explicitly prioritizes cost.
- **Don't present model choice as a leaderboard judgment.** You're picking for diversity, not ranking.

## Cost awareness

`wait_for_round`'s status line shows what the round cost and, when it could be read, the current balance (`get_session` shows cost only). `get_credit` is useful when balance is uncertain or the user asks about cost.

Don't make cost preflight a default ritual before every deliberation — it creates friction and can bias agents away from using mumo when the task genuinely warrants a panel.

If cost is part of the user's problem, translate it into problem context:

Good: "Assume this workflow can afford at most one additional model call per important decision."
Weak: "The previous mumo round cost $0.34."

Frontier panels typically cost $0.20-0.60 per round. Mid-tier panels are significantly cheaper.
