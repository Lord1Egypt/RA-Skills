# Cross-platform editions

The canonical methodology is maintained once in this directory and packaged for three surfaces.

- ClawHub: https://clawhub.ai/mwclaw/hr-decision-packet
- ChatGPT: the tested private GPT configuration and public portable source are in `platforms/chatgpt/`; public GPT sharing was unavailable in the current creator UI at release time.
- Claude: installation instructions are in `platforms/claude/`; the uploadable ZIP is attached to the corresponding GitHub release.

Platform adapters may change packaging, field names, and conversation starters. They must not weaken the invariant, evidence distinctions, privacy boundaries, human-only decision boundary, stop condition, or adversarial evals in the canonical skill.
