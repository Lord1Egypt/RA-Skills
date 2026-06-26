## Draft Publish Preflight

- When the user asks to publish a drafted ad, do not call
  `kleinanzeigen_publish` immediately.
- First run `kleinanzeigen_read_ad` for the exact ad directory or config path.
  Check the sanitized summary and confirm that the intended ad, title, category,
  image globs, and `active` state match the user's request.
- If `active` is not `true`, tell the user that publishing requires activation,
  then use `kleinanzeigen_set_ad_active` with `active: true` only when the
  user's publish request or follow-up confirmation clearly authorizes that
  activation.
- Run scoped `kleinanzeigen_verify` after activation and before publishing.
- Publish only with `kleinanzeigen_publish` scoped to the same exact
  `adDirectories` or `adConfigPaths` used for the preflight. Never switch to a
  broad selector during this flow.
- If scoped publish returns `outcome.status: "preflight_failed"` for
  `active`, do not retry publish immediately. Activate, verify, then retry
  scoped publish.
