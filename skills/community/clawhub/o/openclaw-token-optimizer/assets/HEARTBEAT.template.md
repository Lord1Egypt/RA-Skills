# Heartbeat review checklist (not an installer)

- Respect the user's monitoring, quiet-hours, and delivery requirements.
- Return the runtime's quiet-success response when no actionable change exists.
- Avoid repeated full-workspace reads; load only what the task needs.
- Use deterministic command automations when inference is unnecessary.
- Do not wake the model merely to keep a cache warm without measured net savings.
- A cheaper model must still meet the required reliability, context, tools and modality.
- This template does not change runtime configuration or schedule any work.
