## Memory Governance

This workspace follows `memory-governor`.

Route memory in two steps:

1. classify the information into a target class
2. let the current environment's adapter map that class to a concrete file

Do not let individual skills define their own global memory rules.

For the full contract, see `memory-governor/SKILL.md`.

If this host enables OpenClaw runtime memory features:

- let Active Memory handle ordinary pre-reply recall
- let Dreaming handle background daily-to-long-term consolidation
- treat Memory Wiki as a compiled knowledge surface, not canonical durable truth
- keep one-off corrections in `learning_candidates` until reviewed
- keep manual reads minimal unless recovering, auditing, or resolving conflicts
