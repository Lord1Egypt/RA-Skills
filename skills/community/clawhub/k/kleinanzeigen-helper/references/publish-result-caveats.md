## Publish Result Caveats

- Check the structured `outcome` first. Success evidence can include `DONE:`
  counts, published or updated IDs, selected ad config changes observed after
  miniclaw exits, or another explicit success signal returned by KleinClaw.
- If the structured result is empty, times out, reports a noisy process exit, or
  stops after browser interaction, do not assume failure automatically.
- If the result is unclear, tell the user what happened and suggest checking the
  listing on Kleinanzeigen or rerunning a scoped list, verify, or download when
  appropriate.
- Treat `Approval timed out` as an OpenClaw/tool approval timing issue, not as a
  Kleinanzeigen runtime failure. Retry only after the user confirms again.
