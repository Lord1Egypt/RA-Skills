# Proof Loop Guidance for Codex

Use `.agent/tasks/<TASK_ID>/spec.md` as the frozen source of truth. Builders do not verify their own work. Verifiers do not edit production code. Completion requires `proof-loop check <TASK_ID>` to pass.
