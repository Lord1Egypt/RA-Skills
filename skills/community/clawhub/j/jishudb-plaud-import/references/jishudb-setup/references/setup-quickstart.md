# Routine setup

Use this short path for ordinary local installation and connection. Read it
once; reuse facts already established in this turn. Resolve helper paths from
the parent setup directory and use the host's available Node 22+ executable.
Open the full installation contract only for warnings, an unsupported case,
or a specific helper failure. Configuration and client loading are Agent work;
the user's normal part is required trust, OS verification and OAuth consent.

1. If the host already exposes JishuDB tools, make one real capability call.
   When it succeeds, reuse the connection and continue the user's task.
2. Honor an explicitly selected remote service. Do not replace it with a local
   installation; use the connection recovery guide for that target.
3. For a local target, read the effective client entry once, make one direct
   loopback health probe without proxying or credentials, and check the exact
   application executable. For WorkBuddy, check the effective configuration
   scope; the usual user file is `~/.workbuddy/mcp.json`. On Windows, check
   `%LOCALAPPDATA%\Programs\JishuDB\JishuDB.exe` and resolve `localPort` from
   `%LOCALAPPDATA%\JishuDB\desktop-endpoint.json`; macOS uses
   `~/Library/Application Support/JishuDB/desktop-endpoint.json`. If there is no
   endpoint preference, use `8088`, not guessed ports. Run probes on the client
   machine (Windows loopback is not WSL loopback). With curl, use `--noproxy '*'
   --max-time 3` and no redirect following for this local health probe only;
   preserve the configured download proxy. A directory, endpoint preference, retained database
   or Python cache is not an installed app. If the executable is absent, go
   straight to step 4; do not recursively list caches, open databases, repeatedly
   probe the empty port, or ask whether to generate a plan. If it exists, use
   the connection steps below instead of reinstalling.
4. On Windows, run `node scripts/install-windows.js check` once, then
   `node scripts/install-windows.js plan -Client WorkBuddy -ConfigTarget <actual-config-path> -ConnectionName jishudb`.
   On macOS, run `zsh scripts/install-macos.sh plan --client workbuddy --config-target <actual-config-path> --connection-name jishudb`.
   Use the actual host name/config path when the client is not WorkBuddy. CNB
   is the default. Let the helper validate retained data and supported paths.
5. On `plan_ready`, match the transaction to existing explicit user setup
   authorization. When covered, state a short progress update and continue.
   Otherwise ask one brief confirmation for the concrete installation. Never
   fabricate authorization from the ready status. Keep hashes, plan JSON and
   technical tables in tool evidence unless requested or needed for a problem.
6. Pass the exact returned plan path and digest to `download`, retaining the
   approved source. Call bounded steps until `downloaded`; report progress
   briefly without ending the workflow. Honor `download_waiting` intervals.
   Then call `execute` once. Use the exact commands below; do not discover syntax
   by invoking an empty mode or omitting plan arguments. Keep each download
   invocation bounded; do not wrap the entire transfer in a long foreground
   shell loop or suppress its error output. A failed step needs its stated
   recovery action, not another automatic download attempt.
7. Pause only for actual installer/security, legal, OAuth or client-trust
   prompts. In `reinstall-preserve-data`, retain the selected data directory
   and wait for the user to finish the interactive installer; never substitute
   silent flags. Afterward continue with the connection steps below.
8. Windows checks remaining download space before requesting package bytes.
   On `insufficient_download_space`, report the required and available bytes;
   do not retry a full drive or delete user files.
   On failure, preserve the exact stage/category and inspect only evidence
   relevant to it. Never change publisher trust, bypass permissions, delete
   data/rollback state, or automatically retry an unresolved installer handoff.
   Do not extend an expired plan. A replacement plan must be checked against
   current user authorization; an expired exact-plan-only approval cannot be
   silently renewed. Use only helper-supported cache reuse.

Routine discovery should take one focused pass. If a needed value is unresolved,
name that value rather than restarting the whole checklist. OS/browser consent
is distinct from installation authorization and remains user-operated.

## Exact continuation commands

Substitute the returned `planPath` and `planSha256` as quoted arguments; these
are command templates, not new plans. Run `execute` only after `downloaded`.

Windows:
```text
node scripts/install-windows.js download -PlanPath "<planPath>" -PlanSha256 "<planSha256>"
node scripts/install-windows.js execute -PlanPath "<planPath>" -PlanSha256 "<planSha256>"
```

macOS:
```text
zsh scripts/install-macos.sh download --plan "<planPath>" --plan-sha256 "<planSha256>"
zsh scripts/install-macos.sh execute --plan "<planPath>" --plan-sha256 "<planSha256>"
```

## Connect after installation

1. `installed` proves installation, not a surviving service. In a separate host
   tool call after the launch command returns, probe the resolved `/health`
   directly and validate JishuDB `product`, `healthSchema`, `status` and expected
   version/revision. If still starting, use bounded polling with a deadline,
   stopping as soon as ready; do not add a fixed sleep after success. If absent,
   inspect the process and startup log before one supported, authorized launch
   of the existing app. A service that disappears after the tool call is a
   launch-lifetime failure, not an OAuth/configuration failure. Follow
   [connection recovery](connection-recovery.md); do not reinstall or claim that
   only user consent remains.
   The Windows helper now reports `launchMethod=desktop-shell` and
   `launchStatus=requested`: it delegates a private shortcut to Explorer,
   preserving the approved background/foreground mode. These fields confirm
   dispatch only. Do not replace this with `cmd start`, `Start-Process`, a
   detached Node child or a background shell job; those can still belong to the
   host's process group. Do not disable the host sandbox or add scheduled tasks
   to repair a launch. A `desktop_launch_failed` result retains installed state;
   inspect that handoff instead of rerunning installation.
2. Read `/api/service/capabilities` from that verified endpoint without
   credentials or redirects. For `agentOnboarding.schemaVersion=1`,
   `supported=true` and `route=initial-consent` or `owner-consent`, use native
   OAuth without asking for a management password. Keep advertised owner/device
   verification user-operated. Do not infer a Windows Hello exemption from a
   fresh install; it requires the advertised `windows-fresh-install` method and
   `not-required-for-fresh-install` verification. For other routes, use the full
   setup guide's onboarding section. Choose the task's authorized profile;
   when OAuth is supported, use it without an OAuth-versus-Token choice menu.
3. Reuse a correct entry. Otherwise use the host's supported configuration
   action or read, privately back up and atomically merge only the non-secret
   entry into its effective file, preserving other entries and permissions.
   For WorkBuddy Streamable HTTP, merge
   `{"type":"streamableHttp","url":"<verified MCP URL>"}` under the selected
   `mcpServers` name; do not rely on inferring transport from a bare URL.
   Honor the host editor's read-before-write requirement. Then use an exposed
   refresh/reload action or an available authorized native UI to load it.
   Verify the named entry and endpoint in the client before mentioning Trust.
   If the list is still empty, finish the supported loading operation yourself
   or report that exact missing capability; never tell the user to trust an
   entry that is not there. A missing tool search
   alone does not prove a configuration cache problem. Do this work yourself
   when the controls are available, without asking the user to write JSON.
   Use [WorkBuddy loading recovery](connection-recovery.md#load-workbuddy-configuration)
   only if the entry remains unloaded. Historical UI steps are not proof of
   how the installed host version behaves.
4. Let the user complete actual client trust and browser OAuth. Allow the
   page/Desktop to return automatically; use Return to client only when that
   return fails. While the client is Authorizing, check the current callback
   before starting another connection. Never click Connect again merely because
   the browser has already shown consent success. Discover the host's fully qualified JishuDB
   tool names and call the actual `kb_get_capabilities` and `kb_list` tools.
   Use the full setup guide's runtime-preparation section for the task's
   readiness and write scope. Resume the task only when those checks pass.

If an essential host action is genuinely inaccessible to the Agent, report
the last verified checkpoint and request only that action. State that the
configuration is already saved when it is; do not hand the user a JSON setup
tutorial, multiple alternative routes, or an unverified claim that only OAuth
remains. Recheck service health on resuming after user interaction.
