# Upgrading a hybrid setup

Order: Gateway first, then each node. A node may run the previous supported release (N-1) until it is upgraded.

1. **Stop, then check config.** 2026.9 refuses to start on an invalid config. With the Gateway stopped, run `openclaw doctor --fix`; it migrates renamed keys (`env.*` to `env.vars`, exec `security: ask` to `mode`).
2. **Service files.** `openclaw gateway install --force` refuses group-writable `~/.config`, `~/.config/systemd`, `~/.config/systemd/user`, and unit files. `chmod 755` the directories and `644` the unit first.
3. **Plugins.** Pinned plugin versions do not follow the core upgrade: `openclaw plugins install @openclaw/<plugin>@latest` for each.
4. **Proxy list.** Keep `gateway.trustedProxies` narrow (the same-host Serve proxy only). A wide list rejects nodes with `403 Proxy client attribution is required`.
5. **Node reapproval.** After the node upgrades it advertises new capabilities and files a reapproval request. `openclaw nodes describe --node <name>` lists current vs pending caps and commands; existing caps keep working. Approve with `openclaw nodes approve <request-id>` (needs `operator.admin`) only if the workflow needs the new surface.
6. **Verify.** `openclaw doctor`, `openclaw security audit --deep`, `openclaw nodes status`, and one `openclaw nodes invoke --node <name> --command system.which --params '{"bins":["node"]}' --json`.
