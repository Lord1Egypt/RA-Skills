## Ad Authoring

- Use `kleinanzeigen_ad_schema` before creating or editing a local ad draft.
  The plugin exposes the supported `ad.yaml` fields, required values, limits,
  enum values, and a safe draft workflow.
- For a concrete shape reference, use the packaged inactive example
  `examples/sample-listing/ad.yaml`. Copy it into a configured `adRoots`
  directory before editing; never publish the example unchanged.
- Treat KleinClaw as the source of truth for the miniclaw ad schema. User chat,
  image filenames, and image observations provide field values; the schema
  shape must come from `kleinanzeigen_ad_schema` and
  `kleinanzeigen_draft_ad`.
- Use `kleinanzeigen_images_list` for candidate image filenames and runtime
  support checks. This tool lists files, relative globs, sizes, and basic
  dimensions when available; it does not inspect image pixels or describe what
  is visible.
- If the user wants an ad based on images, use only user-provided chat context,
  file names, existing non-secret ad examples, and any image-viewing capability
  already available to the agent. Do not claim image details came from
  KleinClaw unless a KleinClaw tool actually returned them.
- Use `kleinanzeigen_read_ad` for one existing ad config under configured
  `adRoots` when examples are useful. Contact fields are redacted by default.
- Use `kleinanzeigen_draft_ad` only after explicit user confirmation. It creates
  or replaces a miniclaw-shaped `ad.yaml` or `ad.yml` under configured
  `adRoots`; it does not publish. Prefer `active: false` for first drafts.
- After drafting, run scoped `kleinanzeigen_verify` against the new directory or
  config path. Ask the user to review the sanitized draft summary before making
  it active or publishing it.
