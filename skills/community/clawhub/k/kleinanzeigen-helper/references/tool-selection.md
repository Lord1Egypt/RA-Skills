## Tool Selection

- `kleinanzeigen_status`: check runtime availability, config wiring, workspace
  mode, version, and supported commands without reading the config contents.
- `kleinanzeigen_list_ads`: discover configured local ad folders and resolve
  titles, IDs, active state, config paths, and directories before scoped
  operations.
- `kleinanzeigen_ad_schema`: inspect the safe ad config schema and draft
  workflow exposed by KleinClaw.
- `kleinanzeigen_read_ad`: read one existing ad config under configured
  `adRoots`, with contact fields redacted by default.
- `kleinanzeigen_images_list`: list image files under one configured ad
  directory and return relative globs usable in an ad draft.
- `kleinanzeigen_browser_status`: inspect sanitized effective browser settings
  and detected local browsers.
- `kleinanzeigen_browser_check`: test current or proposed browser settings
  through miniclaw diagnostics without changing the real config.
- `kleinanzeigen_browser_configure`: change miniclaw browser settings only after
  explicit confirmation.
- `kleinanzeigen_draft_ad`: create or replace a local ad draft under configured
  `adRoots` only after explicit confirmation.
- `kleinanzeigen_set_ad_active`: set the top-level `active` flag for one YAML
  ad config before scoped verify/publish.
- `kleinanzeigen_verify`: validate the already configured miniclaw workspace.
- `kleinanzeigen_publish`: publish or republish due, new, changed, all, combined
  selectors, or explicitly selected ads.
- `kleinanzeigen_update`: update changed, all, or explicitly selected ads.
- `kleinanzeigen_delete`: delete only explicitly selected ad IDs.
- `kleinanzeigen_download`: download new, all, or explicitly selected ads.
- `kleinanzeigen_extend`: extend all eligible ads or explicitly selected IDs.

Do not mix explicit ad IDs with selectors. For publish combinations, use
`selectors`, for example `["changed", "due"]`.

If a tool is unavailable, tell the user that KleinClaw must be installed and
enabled in OpenClaw before that action can run.
