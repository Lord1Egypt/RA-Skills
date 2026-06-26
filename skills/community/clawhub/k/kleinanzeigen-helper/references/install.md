## Prerequisites / Install

- Install [KleinClaw](https://clawhub.ai/plugins/kleinclaw), then enable it:

  ```bash
  openclaw plugins install clawhub:kleinclaw
  openclaw plugins enable kleinclaw
  openclaw gateway restart
  ```

- Configure KleinClaw under `plugins.entries.kleinclaw.config` with
  `configPath` or `workingDirectory` in the active OpenClaw config. Use
  `openclaw config file` to print that file path. `configPath` points at the
  local miniclaw `config.yaml`; `workingDirectory` makes miniclaw read
  `config.yaml` from that directory.
- The plugin bundles the `miniclaw` runtime and this helper skill, so no
  separate executable path is required. The standalone
  [`kleinanzeigen-helper`](https://clawhub.ai/ilyazar/kleinanzeigen-helper)
  skill from
  [`ilyaZar/kleinanzeigen-helper`](https://github.com/ilyaZar/kleinanzeigen-helper)
  is optional guidance only; the callable tools still come from the KleinClaw
  plugin.
- Keep Kleinanzeigen credentials, browser profiles, cookies, and full config
  files out of chat.
