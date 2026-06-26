# OpenClaw Update Failure Patterns

Use this file after the main `SKILL.md` install/update workflow narrows a problem to update drift, plugin drift, service-manager disagreement, task ledger health, or post-update channel/runtime regressions.

These are symptom-matching patterns, not a command script. Keep the scope narrow, avoid destructive cleanup until the loaded paths and service owner are known, and verify after every repair.

**Before grepping these generic patterns**, check whether `local-install.md` records a "Rescue / Incident Workspace" path. Install-specific incident history often holds the exact prior occurrence and its fix; these generic patterns are the fallback when local history is silent.

Source note: this reference is adapted from the MIT-licensed `BKF-Gitty/openclaw-update-runbook` project and generalized for any OpenClaw install shape.

## 1. Update Channel Drift

Symptom:
- The host intentionally runs beta/dev or a newer stable build.
- `status --deep` says the local version is newer than the published "latest" version.
- Config metadata still shows a different update channel than the package that was installed.

Inspect:
- `openclaw --version`
- `openclaw status --deep`
- `openclaw config get update`

Why it matters:
- Update advice can be misleading when installed version and recorded channel disagree.
- Record the real version/channel before deciding whether to update, downgrade, or leave the host alone.

## 2. Stale Config After Upgrade

Symptom:
- `doctor` warns that a provider, plugin, model alias, or config key is unknown.
- Runtime falls back to auto-detect or legacy behavior.
- A helper command appears to fix the issue, but the warning remains.

Inspect:
- `openclaw doctor --non-interactive --no-workspace-suggestions`
- `openclaw config validate`
- Specific config keys named in the warning, often `tools.web.search.provider`, `plugins.allow`, `plugins.entries.*`, model aliases, and fallback chains.

Recovery:
- Remove or update only the stale key after backing up config.
- Re-run validation and doctor before restarting.

## 3. Bundled Plugin Shadowed By External Plugin

Symptom:
- A capability should be bundled with the host package, but the gateway loads an older global/npm/plugin-path copy.
- `plugins list` or `plugins inspect` shows a source path outside the host package.
- The loaded plugin version does not match the host package cohort.

Inspect:
- `openclaw plugins inspect <id>`
- `openclaw plugins list --json`
- The plugin source/origin/version fields and whether the source has compiled runtime output such as `dist/`.

Recovery:
- Decide which install should be canonical.
- Prefer reconciling the external install or install record over deleting directories blindly.
- Restart only after the loaded path and intended source are clear.

## 4. Plugin Install Records Drift From Disk

Symptom:
- Config or plugin registry says a plugin exists, but the recorded path is missing.
- Plugin warnings mention phantom installs or allowlist entries.
- `plugins doctor` points to a package path that is not on disk.

Inspect:
- `~/.openclaw/plugins/installs.json` or the equivalent profile-specific plugin install registry.
- `~/.openclaw/npm/node_modules/@openclaw/...`
- `~/.openclaw/npm/projects/<plugin>-<hash>/...` — per-plugin project directories used by newer updaters (observed in 2026.6.x); the older `npm/node_modules/@openclaw/*` layout can coexist with it.
- `~/.openclaw/extensions/...`
- `openclaw plugins registry --refresh`

Recovery:
- Refresh the registry first.
- Reinstall the single missing plugin when the install record is clearly stale.
- Avoid broad plugin reinstall until the registry and disk state are compared.

## 5. Third-Party Plugin Runtime Dependencies Removed

Symptom:
- A third-party plugin fails after update or cleanup with `Cannot find module ...`.
- The plugin root remains, but its local `node_modules` or bundled dependency directory is gone.

Inspect:
- Plugin package directory and `package.json`.
- Whether dependencies are declared as runtime dependencies, peer dependencies, optional peers, or externalized build inputs.
- Whether a cleanup command removed plugin-local runtime dependencies.

Recovery:
- Reinstall or roll back the specific third-party plugin.
- Preserve the broken directory if you need evidence for an upstream report.

## 6. Context Engine Not Registered After Restart

Symptom:
- Logs say the context engine falls back to legacy behavior.
- The plugin appears installed but is not registered or initialized.

Inspect:
- `openclaw plugins doctor`
- `openclaw plugins inspect <context-plugin-id>`
- Recent startup logs for dependency, contract, registry, or load-order errors.

Recovery:
- Fix the plugin load error first.
- Then re-run `plugins doctor` and restart if plugin loading is not hot-reloaded.

## 7. Event Loop Degradation After Update

Symptom:
- `channels status --deep` reports degraded event-loop health.
- Logs mention lane wait thresholds, active-memory timeouts, long approval followups, or restart blocked by active tasks.

Inspect:
- `openclaw tasks audit`
- Recent gateway logs and error logs.
- Plugin load retry loops and long-running task runs.

Recovery:
- Clear or repair the specific stale task/ledger issue only when it is understood.
- Re-run channel status and task audit after the repair.

## 8. Task Ledger Blocks Clean Restart

Symptom:
- Gateway drain, restart, or status reports active task runs that should no longer be active.
- `tasks audit` reports stale running tasks, lost tasks, timestamp inconsistencies, or repeated delivery failures.

Inspect:
- `openclaw tasks audit`
- `openclaw tasks show <id>`
- Recent logs around the task IDs named by audit.

Recovery:
- Cancel or run maintenance only for tasks that are clearly stale or corrupt.
- Verify with `openclaw tasks audit` before treating runtime health as clean.

## 9. Command-Path Disagreement

Symptom:
- `doctor` or `status --deep` says a token, provider, or channel is unavailable from the command path.
- The live gateway's channel health says connected and ready.

Likely cause:
- The interactive shell and the service manager do not share the same environment, config path, profile, or user home.

Inspect:
- `openclaw config file`
- `openclaw gateway status`
- Service-manager environment source, without printing secret values.
- `openclaw channels status --deep`

Recovery:
- Treat shell-only warnings as evidence to investigate, not proof that the live gateway is down.
- Align the service and shell env/config only after confirming which runtime is authoritative.

## 10. Maintainer Handoff Bundle

When an issue looks like a package or plugin regression rather than local drift, collect:

- Version before and after.
- Install type and service manager.
- Plugin source path actually loaded.
- Whether the plugin is bundled, global/npm-installed, ClawHub-installed, or local-extension-installed.
- Exact doctor/plugins doctor warning text.
- Redacted startup log lines around the failure.
- Relevant non-secret config keys.

Do not include secrets, tokens, full env files, session bodies, or agent workspace contents.

## 11. Plugin Updater Follows Stale Install Records

Symptom:
- The host package is updated, but plugin install records still pin old specs.
- `openclaw plugins update --all` reinstalls or downgrades plugins to the old recorded versions.
- Disk versions briefly move forward, then update-all reverts them.

Inspect:
- Plugin install records and their `spec` fields.
- Actual package versions under the profile's npm plugin directory.
- `openclaw plugins inspect <id>` for source/origin/version.

Recovery:
- Update the specific plugin with an explicit desired spec when supported, for example `openclaw plugins update <id> <package>@latest`.
- Use `plugins update --all` only after install records already point at the desired specs.

## 12. Control UI Token Mismatch

Symptom:
- Gateway health is good and the dashboard loads.
- Control UI websocket auth fails with token mismatch or unauthorized logs.

Inspect:
- Recent websocket auth log lines.
- Whether `gateway.auth.token` or its SecretRef source changed.
- Whether the browser-side Control UI is holding an older token.

Recovery:
- Separate browser/UI auth cache problems from server-side startup failures.
- Refresh the UI-side token only after confirming the gateway token source is correct.

## 13. Channel SecretRef Resolves In Audit But Fails At Runtime

Symptom:
- `openclaw config validate` passes.
- `openclaw secrets audit` reports no unresolved secrets.
- A channel still reports token unavailable or fails to start.

Inspect:
- The channel token config field shape, without printing the secret value.
- The referenced secrets provider and whether the live gateway can resolve it.
- Gateway startup logs for plugin-side SecretRef errors.
- Whether another plugin using the same SecretRef provider resolves successfully.

Recovery:
- Prefer fixing provider/runtime resolution.
- If a temporary inline or env fallback is unavoidable, call out the security tradeoff, get user approval, and plan to revert after the plugin/runtime bug is fixed.

## 14. Gateway CLI Start Error But Service Manager Recovers

Symptom:
- `openclaw gateway start` prints an argument or invocation error.
- Service-manager state, listener checks, or health endpoint show the gateway is actually running.

Inspect:
- Native service-manager status.
- `openclaw gateway status`
- Listening port and process owner.
- Recent stdout/stderr logs.

Recovery:
- Verify service reality before reinstalling or retrying start commands.
- Treat the CLI error as one signal, not proof of outage.

## 15. Plugin Uninstall Removes More Than The Install Directory

Symptom:
- After `openclaw plugins uninstall <id> --force`, the plugin directory is gone.
- Config entries, allowlist rows, and exclusive slot assignments may also disappear.
- Re-enabling a sibling/local copy does not restore prior slot config automatically.

Inspect:
- `plugins.entries.<id>`
- `plugins.allow`
- `plugins.slots.*`
- Plugin install records and the remaining on-disk plugin copies.

Recovery:
- Use uninstall only when you intend to remove all traces.
- If the goal is to switch loaded paths, prefer registry refresh, explicit enable/disable, or a backed-up config edit.

## 16. Optional Peer Dependency Imported Unconditionally

Symptom:
- A third-party plugin declares a peer dependency as optional, but load fails with `ERR_MODULE_NOT_FOUND`.
- The compiled bundle imports the optional peer unconditionally.

Inspect:
- `package.json` `peerDependencies`, `peerDependenciesMeta`, `dependencies`, and `devDependencies`.
- Token-level import specifiers in compiled output without dumping minified bundles into the conversation.
- Whether another host only works because the dependency is hoisted elsewhere.

Recovery:
- Roll back to a known-good plugin build or wait for a fixed package.
- Avoid manually installing the missing peer into the plugin directory as a hidden local patch; future plugin updates will overwrite it.

## 17. Duplicate Plugin ID Warnings

Symptom:
- `plugins doctor` warns about duplicate plugin IDs.
- Warning text may wrap poorly and appear self-referential.
- There may be both an extensions copy and a managed npm/global copy.

Inspect:
- Every `openclaw.plugin.json` matching the plugin ID under the profile's plugin roots.
- `openclaw plugins inspect <id>` source path.
- `plugins.load.paths`.

Recovery:
- If two real manifests exist, pick the canonical one and archive the other with user approval.
- If the warning path is identical to the loaded source path and no second manifest exists, treat it as a false positive and avoid deleting the canonical install.

## 18. Bundled Provider Discovery Mode Drift

Symptom:
- After upgrade, doctor warns that a restrictive plugin allowlist is still using legacy bundled provider discovery behavior.
- A new or previously implicit config key controls whether bundled providers bypass or obey `plugins.allow`.

Inspect:
- `plugins.allow`
- `plugins.bundledDiscovery`
- Agent model primary/fallback provider prefixes.
- Whether required provider credentials are available to the service runtime.

Recovery:
- If preserving legacy behavior, explicitly pin the compatibility mode if supported.
- If strict allowlisting is desired, add required bundled provider IDs to `plugins.allow`, set allowlist mode, restart if required, and verify doctor plus model availability.

## 19. Non-Interactive Plugin Uninstall Prompt

Symptom:
- `openclaw plugins uninstall <id>` prompts for confirmation and no-ops in a non-interactive shell.
- A noisy top-level-await or prompt warning may obscure that no input was provided.

Recovery:
- Use the CLI's supported force flag when non-interactive uninstall is explicitly intended.
- Run a dry run first when available.
- Re-check `plugins list` before assuming the uninstall happened.

## 20. Multi-Step Remote Update Disconnects Mid-Run

Symptom:
- A long remote command stops returning output while the target host keeps running parts of the script.
- Reconnecting shows package updates, plugin reinstalls, or restarts partially or fully completed.

Likely cause:
- Restarting the service manager, replacing a wrapper, or changing the process tree detached the remote shell from the caller.

Inspect:
- Fresh remote process list.
- Gateway listener and health endpoint.
- Package and plugin versions on disk.
- A remote log file if the update command redirected output.

Recovery:
- Do not rerun the entire update blindly.
- Kill orphan wrapper processes only when identified and safe.
- Prefer separate phases for stop, package update, plugin reconcile, start, and verify.

## 21. Version Drift Between Operator Sessions

Symptom:
- A host has a different OpenClaw version than the last audited state, even though the current operator did not update it.
- Auto-update config appears disabled, but another scheduled process or agent updated the host.

Inspect:
- `openclaw --version`
- Cron/autopilot/scheduled jobs that can run package or plugin updates.
- Plugin disk versions.
- Recent package-manager or gateway logs.

Recovery:
- Treat every update/debug session as a fresh audit.
- Do not apply yesterday's workaround until the current state is re-snapshotted.

## 22. Cohort Version Snapshot Before Update

Practice:
- Before stopping or updating, snapshot host and plugin versions.
- After update, snapshot again and compare.

Generic commands:

```bash
openclaw --version
openclaw plugins list --json
```

If plugin package directories are available, also capture package names and versions from each `package.json` using a redacting/local-only command.

Why it matters:
- A package update can move the host but leave one plugin on the old cohort.
- The snapshot provides rollback evidence if a new plugin version has a packaging regression.

## 23. Service Environment Quote Corruption

Symptom:
- A channel starts returning upstream auth failures immediately after a host update or service-env regeneration.
- Channel status may still say the token came from env/config.
- The underlying secret source did not change.

Possible cause:
- The service environment writer wrapped a string secret with literal quote characters, so the service passes `"token"` instead of `token`.

Inspect safely:
- This requires explicit user approval because service env files can contain secrets.
- Use a local redacting check that prints only variable names and whether the value has suspicious leading/trailing quote characters. Do not print token substrings.
- Check every affected `*_TOKEN` and `*_API_KEY` line, not only one channel.

Recovery:
- Back up the service env file before editing.
- Rewrite only affected env lines from the canonical secret source without printing values.
- Restart through the appropriate service manager.
- Re-run `openclaw channels status --deep` and inspect auth logs for the affected channel.

Why it matters:
- Rotating the upstream credential is the wrong fix when the local service env value was corrupted.
- Treat any operation that regenerates service env files as a reason to re-verify channel auth.

## 24. Clean-Exit Supervisor Restart Treated As Final By Service Manager

Symptom:
- The gateway is dead, but the last log lines show a normal config-reload or supervisor-restart message, not an error.
- The service unit is `inactive (dead)` with last exit status 0.
- The outage began right after a config write — even a routine one such as a `plugins.installs.*` update.

Likely cause:
- OpenClaw's config-reload "full process restart (supervisor restart)" exits the process cleanly (status 0) and relies on the service manager to start it again. A systemd unit with `Restart=on-failure` (or an equivalent policy elsewhere) treats the clean exit as intentional and never restarts it.

Inspect:
- Native service-manager state and the unit's restart policy (`systemctl show <unit> --property=Restart`).
- The exit status and final log lines of the dead process.
- Which config write immediately preceded the exit.

Recovery:
- Start the unit to restore service, then change the restart policy to `Restart=always` (drop-in override or backed-up unit edit) so the supervisor-restart path works next time.
- Pair `Restart=always` with `StartLimitBurst`/`StartLimitIntervalSec` so an invalid config cannot turn the fix into an unbounded crash loop.
- Audit every gateway unit on the host, not just the one that died — sibling units often share the same policy.

## 25. Stale Secondary Unit Serves The Port (Impostor Gateway)

Symptom:
- The health endpoint returns OK, but agents dispatch nothing, channels misbehave, or plugin errors reference an install path that should no longer be in use.
- Service-manager state for the expected unit disagrees with the listener (expected unit dead, port still answering).

Likely cause:
- A superseded unit — commonly a disabled legacy user-level service resurrected by a watchdog, login session, or stray start — grabbed the gateway port and serves health from an old install. One real case answered health 200 for 8 days while dispatching zero agent sessions.

Inspect:
- Which PID owns the listener (`ss -ltnp`), and that PID's binary path (`readlink /proc/<pid>/exe`) and owning unit (`systemctl status <pid>` or cgroup).
- Whether the binary path matches the install the active unit is supposed to run.
- Both system-level and user-level unit files matching the gateway name, including disabled ones.

Recovery:
- Stop the impostor, start the intended unit, and verify the new PID/binary/port lineup.
- Remove or mask the superseded unit file once whatever starts it is identified, with user approval.
- Treat "health 200" as one signal among several; require PID/install agreement before declaring the gateway healthy.

## 26. Native Module Bindings Missing After Plugin Install Or Update

Symptom:
- The gateway starts and health passes, but hooks or plugin features fail with `Could not locate the bindings file. Tried: ...` (commonly `better-sqlite3`).
- The failure appears right after an updater or ClawHub install dropped a new extension version on disk.

Likely cause:
- The extension shipped without compiled native bindings for the host's Node ABI, and install-time compilation did not run.

Inspect:
- Whether the compiled artifact exists, e.g. `node_modules/better-sqlite3/build/Release/better_sqlite3.node` under the extension directory.
- The npm config for `ignore-scripts` (`npm config get ignore-scripts`) for the owning user.

Recovery:
- Run `npm rebuild <module>` in the extension directory as the owning user.
- **Verify the `.node` file exists afterward.** With `ignore-scripts=true`, npm prints "rebuilt dependencies successfully" while building nothing — rerun with `npm rebuild <module> --ignore-scripts=false --foreground-scripts`.
- Restart the gateway and confirm the hook errors are gone from the new process's logs (filter by the new PID; old-process errors linger in the same journal window).

## Attribution

Portions of this reference are adapted from `BKF-Gitty/openclaw-update-runbook`, MIT License, copyright (c) 2026.

MIT license notice from the source project:

```text
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
