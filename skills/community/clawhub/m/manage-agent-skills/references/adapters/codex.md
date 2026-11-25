# Codex

CLI platform: `codex`.

The [skills guide](https://learn.chatgpt.com/docs/build-skills) demonstrates a
`SKILL.md` path, while the
[configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
describes a containing folder path. The manager recognizes both when reading,
and writes `SKILL.md` paths by default. Both documents specify `enabled`;
neither establishes portable `name` selector support.

`--codex-selector name` preserves the previous optional stable-name workflow
for a host verified to support it. It uses `plugin:skill` identities for cached
plugin skills. `reconcile` migrates managed plugin paths only in this mode.
It does not migrate external rules, remove installed files, or prove prompt
metadata exclusion. The legacy `CODEX_SKILL_MANAGER` block remains recognized.
Malformed managed markers and unsupported manager-owned entries fail closed.

Plugin activation is inferred from the selected config; inherited policy and
host defaults may differ. Multiple cache versions and marketplace replacement
heuristics are reported as inventory evidence, not authoritative host selection.
Read `audit` warnings before treating reported `on/off` as effective host state.

## Operational notes

The default writes documented path rules. Existing name rules are
preserved. Use `--codex-selector name` only when the exact host build has been
verified to support name selectors. In that explicit mode, `reconcile`
converts managed plugin paths into stable names; default reconcile preserves
paths. Enabling cannot override a disable outside the manager's block.
Re-scan after a plugin update; path rules may refer to an old version.

Invocation policy is configured in agents/openai.yaml; keeping this manager discoverable does not prove host selection or zero metadata cost.
