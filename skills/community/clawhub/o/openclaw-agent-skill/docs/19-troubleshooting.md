# Help & Troubleshooting

> This file contains verbatim documentation from docs.openclaw.ai
> Total pages in this section: 8

---

<!-- SOURCE: https://docs.openclaw.ai/help/environment -->

# Environment Variables - OpenClaw

OpenClaw pulls environment variables from multiple sources. The rule is **never override existing values**.

## Precedence (highest → lowest)

1.  **Process environment** (what the Gateway process already has from the parent shell/daemon).
2.  **`.env` in the current working directory** (dotenv default; does not override).
3.  **Global `.env`** at `~/.openclaw/.env` (aka `$OPENCLAW_STATE_DIR/.env`; does not override).
4.  **Config `env` block** in `~/.openclaw/openclaw.json` (applied only if missing).
5.  **Optional login-shell import** (`env.shellEnv.enabled` or `OPENCLAW_LOAD_SHELL_ENV=1`), applied only for missing expected keys.

If the config file is missing entirely, step 4 is skipped; shell import still runs if enabled.

## Config `env` block

Two equivalent ways to set inline env vars (both are non-overriding):

```
{
  env: {
    OPENROUTER_API_KEY: "sk-or-...",
    vars: {
      GROQ_API_KEY: "gsk-...",
    },
  },
}
```

## Shell env import

`env.shellEnv` runs your login shell and imports only **missing** expected keys:

```
{
  env: {
    shellEnv: {
      enabled: true,
      timeoutMs: 15000,
    },
  },
}
```

Env var equivalents:

*   `OPENCLAW_LOAD_SHELL_ENV=1`
*   `OPENCLAW_SHELL_ENV_TIMEOUT_MS=15000`

## Runtime-injected env vars

OpenClaw also injects context markers into spawned child processes:

*   `OPENCLAW_SHELL=exec`: set for commands run through the `exec` tool.
*   `OPENCLAW_SHELL=acp`: set for ACP runtime backend process spawns (for example `acpx`).
*   `OPENCLAW_SHELL=acp-client`: set for `openclaw acp client` when it spawns the ACP bridge process.
*   `OPENCLAW_SHELL=tui-local`: set for local TUI `!` shell commands.

These are runtime markers (not required user config). They can be used in shell/profile logic to apply context-specific rules.

## UI env vars

*   `OPENCLAW_THEME=light`: force the light TUI palette when your terminal has a light background.
*   `OPENCLAW_THEME=dark`: force the dark TUI palette.
*   `COLORFGBG`: if your terminal exports it, OpenClaw uses the background color hint to auto-pick the TUI palette.

## Env var substitution in config

You can reference env vars directly in config string values using `${VAR_NAME}` syntax:

```
{
  models: {
    providers: {
      "vercel-gateway": {
        apiKey: "${VERCEL_GATEWAY_API_KEY}",
      },
    },
  },
}
```

See [Configuration: Env var substitution](https://docs.openclaw.ai/gateway/configuration#env-var-substitution-in-config) for full details.

## Secret refs vs `${ENV}` strings

OpenClaw supports two env-driven patterns:

*   `${VAR}` string substitution in config values.
*   SecretRef objects (`{ source: "env", provider: "default", id: "VAR" }`) for fields that support secrets references.

Both resolve from process env at activation time. SecretRef details are documented in [Secrets Management](https://docs.openclaw.ai/gateway/secrets).

| Variable | Purpose |
| --- | --- |
| `OPENCLAW_HOME` | Override the home directory used for all internal path resolution (`~/.openclaw/`, agent dirs, sessions, credentials). Useful when running OpenClaw as a dedicated service user. |
| `OPENCLAW_STATE_DIR` | Override the state directory (default `~/.openclaw`). |
| `OPENCLAW_CONFIG_PATH` | Override the config file path (default `~/.openclaw/openclaw.json`). |

## Logging

| Variable | Purpose |
| --- | --- |
| `OPENCLAW_LOG_LEVEL` | Override log level for both file and console (e.g. `debug`, `trace`). Takes precedence over `logging.level` and `logging.consoleLevel` in config. Invalid values are ignored with a warning. |

### `OPENCLAW_HOME`

When set, `OPENCLAW_HOME` replaces the system home directory (`$HOME` / `os.homedir()`) for all internal path resolution. This enables full filesystem isolation for headless service accounts. **Precedence:** `OPENCLAW_HOME` > `$HOME` > `USERPROFILE` > `os.homedir()` **Example** (macOS LaunchDaemon):

```
<key>EnvironmentVariables</key>
<dict>
  <key>OPENCLAW_HOME</key>
  <string>/Users/kira</string>
</dict>
```

`OPENCLAW_HOME` can also be set to a tilde path (e.g. `~/svc`), which gets expanded using `$HOME` before use.

*   [Gateway configuration](https://docs.openclaw.ai/gateway/configuration)
*   [FAQ: env vars and .env loading](https://docs.openclaw.ai/help/faq#env-vars-and-env-loading)
*   [Models overview](https://docs.openclaw.ai/concepts/models)

---

<!-- SOURCE: https://docs.openclaw.ai/help/troubleshooting -->

# Troubleshooting - OpenClaw

If you only have 2 minutes, use this page as a triage front door.

## First 60 seconds

Run this exact ladder in order:

```
openclaw status
openclaw status --all
openclaw gateway probe
openclaw gateway status
openclaw doctor
openclaw channels status --probe
openclaw logs --follow
```

Good output in one line:

*   `openclaw status` → shows configured channels and no obvious auth errors.
*   `openclaw status --all` → full report is present and shareable.
*   `openclaw gateway probe` → expected gateway target is reachable.
*   `openclaw gateway status` → `Runtime: running` and `RPC probe: ok`.
*   `openclaw doctor` → no blocking config/service errors.
*   `openclaw channels status --probe` → channels report `connected` or `ready`.
*   `openclaw logs --follow` → steady activity, no repeating fatal errors.

## Anthropic long context 429

If you see: `HTTP 429: rate_limit_error: Extra usage is required for long context requests`, go to [/gateway/troubleshooting#anthropic-429-extra-usage-required-for-long-context](https://docs.openclaw.ai/gateway/troubleshooting#anthropic-429-extra-usage-required-for-long-context).

## Plugin install fails with missing openclaw extensions

If install fails with `package.json missing openclaw.extensions`, the plugin package is using an old shape that OpenClaw no longer accepts. Fix in the plugin package:

1.  Add `openclaw.extensions` to `package.json`.
2.  Point entries at built runtime files (usually `./dist/index.js`).
3.  Republish the plugin and run `openclaw plugins install <npm-spec>` again.

Example:

```
{
  "name": "@openclaw/my-plugin",
  "version": "1.2.3",
  "openclaw": {
    "extensions": ["./dist/index.js"]
  }
}
```

Reference: [/tools/plugin#distribution-npm](https://docs.openclaw.ai/tools/plugin#distribution-npm)

## Decision tree

---

<!-- SOURCE: https://docs.openclaw.ai/help/faq -->

# FAQ - OpenClaw

Quick answers plus deeper troubleshooting for real-world setups (local dev, VPS, multi-agent, OAuth/API keys, model failover). For runtime diagnostics, see [Troubleshooting](https://docs.openclaw.ai/gateway/troubleshooting). For the full config reference, see [Configuration](https://docs.openclaw.ai/gateway/configuration).

## Table of contents

*   \[Quick start and first-run setup\]
    *   [Im stuck what’s the fastest way to get unstuck?](https://docs.openclaw.ai/help/faq#im-stuck-whats-the-fastest-way-to-get-unstuck)
    *   [What’s the recommended way to install and set up OpenClaw?](https://docs.openclaw.ai/help/faq#whats-the-recommended-way-to-install-and-set-up-openclaw)
    *   [How do I open the dashboard after onboarding?](https://docs.openclaw.ai/help/faq#how-do-i-open-the-dashboard-after-onboarding)
    *   [How do I authenticate the dashboard (token) on localhost vs remote?](https://docs.openclaw.ai/help/faq#how-do-i-authenticate-the-dashboard-token-on-localhost-vs-remote)
    *   [What runtime do I need?](https://docs.openclaw.ai/help/faq#what-runtime-do-i-need)
    *   [Does it run on Raspberry Pi?](https://docs.openclaw.ai/help/faq#does-it-run-on-raspberry-pi)
    *   [Any tips for Raspberry Pi installs?](https://docs.openclaw.ai/help/faq#any-tips-for-raspberry-pi-installs)
    *   [It is stuck on “wake up my friend” / onboarding will not hatch. What now?](https://docs.openclaw.ai/help/faq#it-is-stuck-on-wake-up-my-friend-onboarding-will-not-hatch-what-now)
    *   [Can I migrate my setup to a new machine (Mac mini) without redoing onboarding?](https://docs.openclaw.ai/help/faq#can-i-migrate-my-setup-to-a-new-machine-mac-mini-without-redoing-onboarding)
    *   [Where do I see what is new in the latest version?](https://docs.openclaw.ai/help/faq#where-do-i-see-what-is-new-in-the-latest-version)
    *   [I can’t access docs.openclaw.ai (SSL error). What now?](https://docs.openclaw.ai/help/faq#i-cant-access-docsopenclawai-ssl-error-what-now)
    *   [What’s the difference between stable and beta?](https://docs.openclaw.ai/help/faq#whats-the-difference-between-stable-and-beta)
    *   [How do I install the beta version, and what’s the difference between beta and dev?](https://docs.openclaw.ai/help/faq#how-do-i-install-the-beta-version-and-whats-the-difference-between-beta-and-dev)
    *   [How do I try the latest bits?](https://docs.openclaw.ai/help/faq#how-do-i-try-the-latest-bits)
    *   [How long does install and onboarding usually take?](https://docs.openclaw.ai/help/faq#how-long-does-install-and-onboarding-usually-take)
    *   [Installer stuck? How do I get more feedback?](https://docs.openclaw.ai/help/faq#installer-stuck-how-do-i-get-more-feedback)
    *   [Windows install says git not found or openclaw not recognized](https://docs.openclaw.ai/help/faq#windows-install-says-git-not-found-or-openclaw-not-recognized)
    *   [Windows exec output shows garbled Chinese text what should I do](https://docs.openclaw.ai/help/faq#windows-exec-output-shows-garbled-chinese-text-what-should-i-do)
    *   [The docs didn’t answer my question - how do I get a better answer?](https://docs.openclaw.ai/help/faq#the-docs-didnt-answer-my-question-how-do-i-get-a-better-answer)
    *   [How do I install OpenClaw on Linux?](https://docs.openclaw.ai/help/faq#how-do-i-install-openclaw-on-linux)
    *   [How do I install OpenClaw on a VPS?](https://docs.openclaw.ai/help/faq#how-do-i-install-openclaw-on-a-vps)
    *   [Where are the cloud/VPS install guides?](https://docs.openclaw.ai/help/faq#where-are-the-cloudvps-install-guides)
    *   [Can I ask OpenClaw to update itself?](https://docs.openclaw.ai/help/faq#can-i-ask-openclaw-to-update-itself)
    *   [What does the onboarding wizard actually do?](https://docs.openclaw.ai/help/faq#what-does-the-onboarding-wizard-actually-do)
    *   [Do I need a Claude or OpenAI subscription to run this?](https://docs.openclaw.ai/help/faq#do-i-need-a-claude-or-openai-subscription-to-run-this)
    *   [Can I use Claude Max subscription without an API key](https://docs.openclaw.ai/help/faq#can-i-use-claude-max-subscription-without-an-api-key)
    *   [How does Anthropic “setup-token” auth work?](https://docs.openclaw.ai/help/faq#how-does-anthropic-setuptoken-auth-work)
    *   [Where do I find an Anthropic setup-token?](https://docs.openclaw.ai/help/faq#where-do-i-find-an-anthropic-setuptoken)
    *   [Do you support Claude subscription auth (Claude Pro or Max)?](https://docs.openclaw.ai/help/faq#do-you-support-claude-subscription-auth-claude-pro-or-max)
    *   [Why am I seeing `HTTP 429: rate_limit_error` from Anthropic?](https://docs.openclaw.ai/help/faq#why-am-i-seeing-http-429-ratelimiterror-from-anthropic)
    *   [Is AWS Bedrock supported?](https://docs.openclaw.ai/help/faq#is-aws-bedrock-supported)
    *   [How does Codex auth work?](https://docs.openclaw.ai/help/faq#how-does-codex-auth-work)
    *   [Do you support OpenAI subscription auth (Codex OAuth)?](https://docs.openclaw.ai/help/faq#do-you-support-openai-subscription-auth-codex-oauth)
    *   [How do I set up Gemini CLI OAuth](https://docs.openclaw.ai/help/faq#how-do-i-set-up-gemini-cli-oauth)
    *   [Is a local model OK for casual chats?](https://docs.openclaw.ai/help/faq#is-a-local-model-ok-for-casual-chats)
    *   [How do I keep hosted model traffic in a specific region?](https://docs.openclaw.ai/help/faq#how-do-i-keep-hosted-model-traffic-in-a-specific-region)
    *   [Do I have to buy a Mac Mini to install this?](https://docs.openclaw.ai/help/faq#do-i-have-to-buy-a-mac-mini-to-install-this)
    *   [Do I need a Mac mini for iMessage support?](https://docs.openclaw.ai/help/faq#do-i-need-a-mac-mini-for-imessage-support)
    *   [If I buy a Mac mini to run OpenClaw, can I connect it to my MacBook Pro?](https://docs.openclaw.ai/help/faq#if-i-buy-a-mac-mini-to-run-openclaw-can-i-connect-it-to-my-macbook-pro)
    *   [Can I use Bun?](https://docs.openclaw.ai/help/faq#can-i-use-bun)
    *   [Telegram: what goes in `allowFrom`?](https://docs.openclaw.ai/help/faq#telegram-what-goes-in-allowfrom)
    *   [Can multiple people use one WhatsApp number with different OpenClaw instances?](https://docs.openclaw.ai/help/faq#can-multiple-people-use-one-whatsapp-number-with-different-openclaw-instances)
    *   [Can I run a “fast chat” agent and an “Opus for coding” agent?](https://docs.openclaw.ai/help/faq#can-i-run-a-fast-chat-agent-and-an-opus-for-coding-agent)
    *   [Does Homebrew work on Linux?](https://docs.openclaw.ai/help/faq#does-homebrew-work-on-linux)
    *   [What’s the difference between the hackable (git) install and npm install?](https://docs.openclaw.ai/help/faq#whats-the-difference-between-the-hackable-git-install-and-npm-install)
    *   [Can I switch between npm and git installs later?](https://docs.openclaw.ai/help/faq#can-i-switch-between-npm-and-git-installs-later)
    *   [Should I run the Gateway on my laptop or a VPS?](https://docs.openclaw.ai/help/faq#should-i-run-the-gateway-on-my-laptop-or-a-vps)
    *   [How important is it to run OpenClaw on a dedicated machine?](https://docs.openclaw.ai/help/faq#how-important-is-it-to-run-openclaw-on-a-dedicated-machine)
    *   [What are the minimum VPS requirements and recommended OS?](https://docs.openclaw.ai/help/faq#what-are-the-minimum-vps-requirements-and-recommended-os)
    *   [Can I run OpenClaw in a VM and what are the requirements](https://docs.openclaw.ai/help/faq#can-i-run-openclaw-in-a-vm-and-what-are-the-requirements)
*   [What is OpenClaw?](https://docs.openclaw.ai/help/faq#what-is-openclaw)
    *   [What is OpenClaw, in one paragraph?](https://docs.openclaw.ai/help/faq#what-is-openclaw-in-one-paragraph)
    *   [What’s the value proposition?](https://docs.openclaw.ai/help/faq#whats-the-value-proposition)
    *   [I just set it up what should I do first](https://docs.openclaw.ai/help/faq#i-just-set-it-up-what-should-i-do-first)
    *   [What are the top five everyday use cases for OpenClaw](https://docs.openclaw.ai/help/faq#what-are-the-top-five-everyday-use-cases-for-openclaw)
    *   [Can OpenClaw help with lead gen outreach ads and blogs for a SaaS](https://docs.openclaw.ai/help/faq#can-openclaw-help-with-lead-gen-outreach-ads-and-blogs-for-a-saas)
    *   [What are the advantages vs Claude Code for web development?](https://docs.openclaw.ai/help/faq#what-are-the-advantages-vs-claude-code-for-web-development)
*   [Skills and automation](https://docs.openclaw.ai/help/faq#skills-and-automation)
    *   [How do I customize skills without keeping the repo dirty?](https://docs.openclaw.ai/help/faq#how-do-i-customize-skills-without-keeping-the-repo-dirty)
    *   [Can I load skills from a custom folder?](https://docs.openclaw.ai/help/faq#can-i-load-skills-from-a-custom-folder)
    *   [How can I use different models for different tasks?](https://docs.openclaw.ai/help/faq#how-can-i-use-different-models-for-different-tasks)
    *   [The bot freezes while doing heavy work. How do I offload that?](https://docs.openclaw.ai/help/faq#the-bot-freezes-while-doing-heavy-work-how-do-i-offload-that)
    *   [Cron or reminders do not fire. What should I check?](https://docs.openclaw.ai/help/faq#cron-or-reminders-do-not-fire-what-should-i-check)
    *   [How do I install skills on Linux?](https://docs.openclaw.ai/help/faq#how-do-i-install-skills-on-linux)
    *   [Can OpenClaw run tasks on a schedule or continuously in the background?](https://docs.openclaw.ai/help/faq#can-openclaw-run-tasks-on-a-schedule-or-continuously-in-the-background)
    *   [Can I run Apple macOS-only skills from Linux?](https://docs.openclaw.ai/help/faq#can-i-run-apple-macos-only-skills-from-linux)
    *   [Do you have a Notion or HeyGen integration?](https://docs.openclaw.ai/help/faq#do-you-have-a-notion-or-heygen-integration)
    *   [How do I install the Chrome extension for browser takeover?](https://docs.openclaw.ai/help/faq#how-do-i-install-the-chrome-extension-for-browser-takeover)
*   [Sandboxing and memory](https://docs.openclaw.ai/help/faq#sandboxing-and-memory)
    *   [Is there a dedicated sandboxing doc?](https://docs.openclaw.ai/help/faq#is-there-a-dedicated-sandboxing-doc)
    *   [How do I bind a host folder into the sandbox?](https://docs.openclaw.ai/help/faq#how-do-i-bind-a-host-folder-into-the-sandbox)
    *   [How does memory work?](https://docs.openclaw.ai/help/faq#how-does-memory-work)
    *   [Memory keeps forgetting things. How do I make it stick?](https://docs.openclaw.ai/help/faq#memory-keeps-forgetting-things-how-do-i-make-it-stick)
    *   [Does memory persist forever? What are the limits?](https://docs.openclaw.ai/help/faq#does-memory-persist-forever-what-are-the-limits)
    *   [Does semantic memory search require an OpenAI API key?](https://docs.openclaw.ai/help/faq#does-semantic-memory-search-require-an-openai-api-key)
*   [Where things live on disk](https://docs.openclaw.ai/help/faq#where-things-live-on-disk)
    *   [Is all data used with OpenClaw saved locally?](https://docs.openclaw.ai/help/faq#is-all-data-used-with-openclaw-saved-locally)
    *   [Where does OpenClaw store its data?](https://docs.openclaw.ai/help/faq#where-does-openclaw-store-its-data)
    *   [Where should AGENTS.md / SOUL.md / USER.md / MEMORY.md live?](https://docs.openclaw.ai/help/faq#where-should-agentsmd-soulmd-usermd-memorymd-live)
    *   [What’s the recommended backup strategy?](https://docs.openclaw.ai/help/faq#whats-the-recommended-backup-strategy)
    *   [How do I completely uninstall OpenClaw?](https://docs.openclaw.ai/help/faq#how-do-i-completely-uninstall-openclaw)
    *   [Can agents work outside the workspace?](https://docs.openclaw.ai/help/faq#can-agents-work-outside-the-workspace)
    *   [I’m in remote mode - where is the session store?](https://docs.openclaw.ai/help/faq#im-in-remote-mode-where-is-the-session-store)
*   [Config basics](https://docs.openclaw.ai/help/faq#config-basics)
    *   [What format is the config? Where is it?](https://docs.openclaw.ai/help/faq#what-format-is-the-config-where-is-it)
    *   [I set `gateway.bind: "lan"` (or `"tailnet"`) and now nothing listens / the UI says unauthorized](https://docs.openclaw.ai/help/faq#i-set-gatewaybind-lan-or-tailnet-and-now-nothing-listens-the-ui-says-unauthorized)
    *   [Why do I need a token on localhost now?](https://docs.openclaw.ai/help/faq#why-do-i-need-a-token-on-localhost-now)
    *   [Do I have to restart after changing config?](https://docs.openclaw.ai/help/faq#do-i-have-to-restart-after-changing-config)
    *   [How do I disable funny CLI taglines?](https://docs.openclaw.ai/help/faq#how-do-i-disable-funny-cli-taglines)
    *   [How do I enable web search (and web fetch)?](https://docs.openclaw.ai/help/faq#how-do-i-enable-web-search-and-web-fetch)
    *   [config.apply wiped my config. How do I recover and avoid this?](https://docs.openclaw.ai/help/faq#configapply-wiped-my-config-how-do-i-recover-and-avoid-this)
    *   [How do I run a central Gateway with specialized workers across devices?](https://docs.openclaw.ai/help/faq#how-do-i-run-a-central-gateway-with-specialized-workers-across-devices)
    *   [Can the OpenClaw browser run headless?](https://docs.openclaw.ai/help/faq#can-the-openclaw-browser-run-headless)
    *   [How do I use Brave for browser control?](https://docs.openclaw.ai/help/faq#how-do-i-use-brave-for-browser-control)
*   [Remote gateways and nodes](https://docs.openclaw.ai/help/faq#remote-gateways-and-nodes)
    *   [How do commands propagate between Telegram, the gateway, and nodes?](https://docs.openclaw.ai/help/faq#how-do-commands-propagate-between-telegram-the-gateway-and-nodes)
    *   [How can my agent access my computer if the Gateway is hosted remotely?](https://docs.openclaw.ai/help/faq#how-can-my-agent-access-my-computer-if-the-gateway-is-hosted-remotely)
    *   [Tailscale is connected but I get no replies. What now?](https://docs.openclaw.ai/help/faq#tailscale-is-connected-but-i-get-no-replies-what-now)
    *   [Can two OpenClaw instances talk to each other (local + VPS)?](https://docs.openclaw.ai/help/faq#can-two-openclaw-instances-talk-to-each-other-local-vps)
    *   [Do I need separate VPSes for multiple agents](https://docs.openclaw.ai/help/faq#do-i-need-separate-vpses-for-multiple-agents)
    *   [Is there a benefit to using a node on my personal laptop instead of SSH from a VPS?](https://docs.openclaw.ai/help/faq#is-there-a-benefit-to-using-a-node-on-my-personal-laptop-instead-of-ssh-from-a-vps)
    *   [Do nodes run a gateway service?](https://docs.openclaw.ai/help/faq#do-nodes-run-a-gateway-service)
    *   [Is there an API / RPC way to apply config?](https://docs.openclaw.ai/help/faq#is-there-an-api-rpc-way-to-apply-config)
    *   [What’s a minimal “sane” config for a first install?](https://docs.openclaw.ai/help/faq#whats-a-minimal-sane-config-for-a-first-install)
    *   [How do I set up Tailscale on a VPS and connect from my Mac?](https://docs.openclaw.ai/help/faq#how-do-i-set-up-tailscale-on-a-vps-and-connect-from-my-mac)
    *   [How do I connect a Mac node to a remote Gateway (Tailscale Serve)?](https://docs.openclaw.ai/help/faq#how-do-i-connect-a-mac-node-to-a-remote-gateway-tailscale-serve)
    *   [Should I install on a second laptop or just add a node?](https://docs.openclaw.ai/help/faq#should-i-install-on-a-second-laptop-or-just-add-a-node)
*   [Env vars and .env loading](https://docs.openclaw.ai/help/faq#env-vars-and-env-loading)
    *   [How does OpenClaw load environment variables?](https://docs.openclaw.ai/help/faq#how-does-openclaw-load-environment-variables)
    *   [“I started the Gateway via the service and my env vars disappeared.” What now?](https://docs.openclaw.ai/help/faq#i-started-the-gateway-via-the-service-and-my-env-vars-disappeared-what-now)
    *   [I set `COPILOT_GITHUB_TOKEN`, but models status shows “Shell env: off.” Why?](https://docs.openclaw.ai/help/faq#i-set-copilotgithubtoken-but-models-status-shows-shell-env-off-why)
*   [Sessions and multiple chats](https://docs.openclaw.ai/help/faq#sessions-and-multiple-chats)
    *   [How do I start a fresh conversation?](https://docs.openclaw.ai/help/faq#how-do-i-start-a-fresh-conversation)
    *   [Do sessions reset automatically if I never send `/new`?](https://docs.openclaw.ai/help/faq#do-sessions-reset-automatically-if-i-never-send-new)
    *   [Is there a way to make a team of OpenClaw instances one CEO and many agents](https://docs.openclaw.ai/help/faq#is-there-a-way-to-make-a-team-of-openclaw-instances-one-ceo-and-many-agents)
    *   [Why did context get truncated mid-task? How do I prevent it?](https://docs.openclaw.ai/help/faq#why-did-context-get-truncated-midtask-how-do-i-prevent-it)
    *   [How do I completely reset OpenClaw but keep it installed?](https://docs.openclaw.ai/help/faq#how-do-i-completely-reset-openclaw-but-keep-it-installed)
    *   [I’m getting “context too large” errors - how do I reset or compact?](https://docs.openclaw.ai/help/faq#im-getting-context-too-large-errors-how-do-i-reset-or-compact)
    *   [Why am I seeing “LLM request rejected: messages.content.tool\_use.input field required”?](https://docs.openclaw.ai/help/faq#why-am-i-seeing-llm-request-rejected-messagescontenttool_useinput-field-required)
    *   [Why am I getting heartbeat messages every 30 minutes?](https://docs.openclaw.ai/help/faq#why-am-i-getting-heartbeat-messages-every-30-minutes)
    *   [Do I need to add a “bot account” to a WhatsApp group?](https://docs.openclaw.ai/help/faq#do-i-need-to-add-a-bot-account-to-a-whatsapp-group)
    *   [How do I get the JID of a WhatsApp group?](https://docs.openclaw.ai/help/faq#how-do-i-get-the-jid-of-a-whatsapp-group)
    *   [Why doesn’t OpenClaw reply in a group?](https://docs.openclaw.ai/help/faq#why-doesnt-openclaw-reply-in-a-group)
    *   [Do groups/threads share context with DMs?](https://docs.openclaw.ai/help/faq#do-groupsthreads-share-context-with-dms)
    *   [How many workspaces and agents can I create?](https://docs.openclaw.ai/help/faq#how-many-workspaces-and-agents-can-i-create)
    *   [Can I run multiple bots or chats at the same time (Slack), and how should I set that up?](https://docs.openclaw.ai/help/faq#can-i-run-multiple-bots-or-chats-at-the-same-time-slack-and-how-should-i-set-that-up)
*   [Models: defaults, selection, aliases, switching](https://docs.openclaw.ai/help/faq#models-defaults-selection-aliases-switching)
    *   [What is the “default model”?](https://docs.openclaw.ai/help/faq#what-is-the-default-model)
    *   [What model do you recommend?](https://docs.openclaw.ai/help/faq#what-model-do-you-recommend)
    *   [How do I switch models without wiping my config?](https://docs.openclaw.ai/help/faq#how-do-i-switch-models-without-wiping-my-config)
    *   [Can I use self-hosted models (llama.cpp, vLLM, Ollama)?](https://docs.openclaw.ai/help/faq#can-i-use-selfhosted-models-llamacpp-vllm-ollama)
    *   [What do OpenClaw, Flawd, and Krill use for models?](https://docs.openclaw.ai/help/faq#what-do-openclaw-flawd-and-krill-use-for-models)
    *   [How do I switch models on the fly (without restarting)?](https://docs.openclaw.ai/help/faq#how-do-i-switch-models-on-the-fly-without-restarting)
    *   [Can I use GPT 5.2 for daily tasks and Codex 5.3 for coding](https://docs.openclaw.ai/help/faq#can-i-use-gpt-52-for-daily-tasks-and-codex-53-for-coding)
    *   [Why do I see “Model … is not allowed” and then no reply?](https://docs.openclaw.ai/help/faq#why-do-i-see-model-is-not-allowed-and-then-no-reply)
    *   [Why do I see “Unknown model: minimax/MiniMax-M2.5”?](https://docs.openclaw.ai/help/faq#why-do-i-see-unknown-model-minimaxminimaxm25)
    *   [Can I use MiniMax as my default and OpenAI for complex tasks?](https://docs.openclaw.ai/help/faq#can-i-use-minimax-as-my-default-and-openai-for-complex-tasks)
    *   [Are opus / sonnet / gpt built-in shortcuts?](https://docs.openclaw.ai/help/faq#are-opus-sonnet-gpt-builtin-shortcuts)
    *   [How do I define/override model shortcuts (aliases)?](https://docs.openclaw.ai/help/faq#how-do-i-defineoverride-model-shortcuts-aliases)
    *   [How do I add models from other providers like OpenRouter or Z.AI?](https://docs.openclaw.ai/help/faq#how-do-i-add-models-from-other-providers-like-openrouter-or-zai)
*   [Model failover and “All models failed”](https://docs.openclaw.ai/help/faq#model-failover-and-all-models-failed)
    *   [How does failover work?](https://docs.openclaw.ai/help/faq#how-does-failover-work)
    *   [What does this error mean?](https://docs.openclaw.ai/help/faq#what-does-this-error-mean)
    *   [Fix checklist for `No credentials found for profile "anthropic:default"`](https://docs.openclaw.ai/help/faq#fix-checklist-for-no-credentials-found-for-profile-anthropicdefault)
    *   [Why did it also try Google Gemini and fail?](https://docs.openclaw.ai/help/faq#why-did-it-also-try-google-gemini-and-fail)
*   [Auth profiles: what they are and how to manage them](https://docs.openclaw.ai/help/faq#auth-profiles-what-they-are-and-how-to-manage-them)
    *   [What is an auth profile?](https://docs.openclaw.ai/help/faq#what-is-an-auth-profile)
    *   [What are typical profile IDs?](https://docs.openclaw.ai/help/faq#what-are-typical-profile-ids)
    *   [Can I control which auth profile is tried first?](https://docs.openclaw.ai/help/faq#can-i-control-which-auth-profile-is-tried-first)
    *   [OAuth vs API key: what’s the difference?](https://docs.openclaw.ai/help/faq#oauth-vs-api-key-whats-the-difference)
*   [Gateway: ports, “already running”, and remote mode](https://docs.openclaw.ai/help/faq#gateway-ports-already-running-and-remote-mode)
    *   [What port does the Gateway use?](https://docs.openclaw.ai/help/faq#what-port-does-the-gateway-use)
    *   [Why does `openclaw gateway status` say `Runtime: running` but `RPC probe: failed`?](https://docs.openclaw.ai/help/faq#why-does-openclaw-gateway-status-say-runtime-running-but-rpc-probe-failed)
    *   [Why does `openclaw gateway status` show `Config (cli)` and `Config (service)` different?](https://docs.openclaw.ai/help/faq#why-does-openclaw-gateway-status-show-config-cli-and-config-service-different)
    *   [What does “another gateway instance is already listening” mean?](https://docs.openclaw.ai/help/faq#what-does-another-gateway-instance-is-already-listening-mean)
    *   [How do I run OpenClaw in remote mode (client connects to a Gateway elsewhere)?](https://docs.openclaw.ai/help/faq#how-do-i-run-openclaw-in-remote-mode-client-connects-to-a-gateway-elsewhere)
    *   [The Control UI says “unauthorized” (or keeps reconnecting). What now?](https://docs.openclaw.ai/help/faq#the-control-ui-says-unauthorized-or-keeps-reconnecting-what-now)
    *   [I set `gateway.bind: "tailnet"` but it can’t bind / nothing listens](https://docs.openclaw.ai/help/faq#i-set-gatewaybind-tailnet-but-it-cant-bind-nothing-listens)
    *   [Can I run multiple Gateways on the same host?](https://docs.openclaw.ai/help/faq#can-i-run-multiple-gateways-on-the-same-host)
    *   [What does “invalid handshake” / code 1008 mean?](https://docs.openclaw.ai/help/faq#what-does-invalid-handshake-code-1008-mean)
*   [Logging and debugging](https://docs.openclaw.ai/help/faq#logging-and-debugging)
    *   [Where are logs?](https://docs.openclaw.ai/help/faq#where-are-logs)
    *   [How do I start/stop/restart the Gateway service?](https://docs.openclaw.ai/help/faq#how-do-i-startstoprestart-the-gateway-service)
    *   [I closed my terminal on Windows - how do I restart OpenClaw?](https://docs.openclaw.ai/help/faq#i-closed-my-terminal-on-windows-how-do-i-restart-openclaw)
    *   [The Gateway is up but replies never arrive. What should I check?](https://docs.openclaw.ai/help/faq#the-gateway-is-up-but-replies-never-arrive-what-should-i-check)
    *   [“Disconnected from gateway: no reason” - what now?](https://docs.openclaw.ai/help/faq#disconnected-from-gateway-no-reason-what-now)
    *   [Telegram setMyCommands fails with network errors. What should I check?](https://docs.openclaw.ai/help/faq#telegram-setmycommands-fails-with-network-errors-what-should-i-check)
    *   [TUI shows no output. What should I check?](https://docs.openclaw.ai/help/faq#tui-shows-no-output-what-should-i-check)
    *   [How do I completely stop then start the Gateway?](https://docs.openclaw.ai/help/faq#how-do-i-completely-stop-then-start-the-gateway)
    *   [ELI5: `openclaw gateway restart` vs `openclaw gateway`](https://docs.openclaw.ai/help/faq#eli5-openclaw-gateway-restart-vs-openclaw-gateway)
    *   [What’s the fastest way to get more details when something fails?](https://docs.openclaw.ai/help/faq#whats-the-fastest-way-to-get-more-details-when-something-fails)
*   [Media and attachments](https://docs.openclaw.ai/help/faq#media-and-attachments)
    *   [My skill generated an image/PDF, but nothing was sent](https://docs.openclaw.ai/help/faq#my-skill-generated-an-imagepdf-but-nothing-was-sent)
*   [Security and access control](https://docs.openclaw.ai/help/faq#security-and-access-control)
    *   [Is it safe to expose OpenClaw to inbound DMs?](https://docs.openclaw.ai/help/faq#is-it-safe-to-expose-openclaw-to-inbound-dms)
    *   [Is prompt injection only a concern for public bots?](https://docs.openclaw.ai/help/faq#is-prompt-injection-only-a-concern-for-public-bots)
    *   [Should my bot have its own email GitHub account or phone number](https://docs.openclaw.ai/help/faq#should-my-bot-have-its-own-email-github-account-or-phone-number)
    *   [Can I give it autonomy over my text messages and is that safe](https://docs.openclaw.ai/help/faq#can-i-give-it-autonomy-over-my-text-messages-and-is-that-safe)
    *   [Can I use cheaper models for personal assistant tasks?](https://docs.openclaw.ai/help/faq#can-i-use-cheaper-models-for-personal-assistant-tasks)
    *   [I ran `/start` in Telegram but didn’t get a pairing code](https://docs.openclaw.ai/help/faq#i-ran-start-in-telegram-but-didnt-get-a-pairing-code)
    *   [WhatsApp: will it message my contacts? How does pairing work?](https://docs.openclaw.ai/help/faq#whatsapp-will-it-message-my-contacts-how-does-pairing-work)
*   [Chat commands, aborting tasks, and “it won’t stop”](https://docs.openclaw.ai/help/faq#chat-commands-aborting-tasks-and-it-wont-stop)
    *   [How do I stop internal system messages from showing in chat](https://docs.openclaw.ai/help/faq#how-do-i-stop-internal-system-messages-from-showing-in-chat)
    *   [How do I stop/cancel a running task?](https://docs.openclaw.ai/help/faq#how-do-i-stopcancel-a-running-task)
    *   [How do I send a Discord message from Telegram? (“Cross-context messaging denied”)](https://docs.openclaw.ai/help/faq#how-do-i-send-a-discord-message-from-telegram-crosscontext-messaging-denied)
    *   [Why does it feel like the bot “ignores” rapid-fire messages?](https://docs.openclaw.ai/help/faq#why-does-it-feel-like-the-bot-ignores-rapidfire-messages)

## First 60 seconds if something’s broken

1.  **Quick status (first check)** Fast local summary: OS + update, gateway/service reachability, agents/sessions, provider config + runtime issues (when gateway is reachable).
2.  **Pasteable report (safe to share)** Read-only diagnosis with log tail (tokens redacted).
3.  **Daemon + port state** Shows supervisor runtime vs RPC reachability, the probe target URL, and which config the service likely used.
4.  **Deep probes** Runs gateway health checks + provider probes (requires a reachable gateway). See [Health](https://docs.openclaw.ai/gateway/health).
5.  **Tail the latest log** If RPC is down, fall back to:
    
    ```
    tail -f "$(ls -t /tmp/openclaw/openclaw-*.log | head -1)"
    ```
    
    File logs are separate from service logs; see [Logging](https://docs.openclaw.ai/logging) and [Troubleshooting](https://docs.openclaw.ai/gateway/troubleshooting).
6.  **Run the doctor (repairs)** Repairs/migrates config/state + runs health checks. See [Doctor](https://docs.openclaw.ai/gateway/doctor).
7.  **Gateway snapshot**
    
    ```
    openclaw health --json
    openclaw health --verbose   # shows the target URL + config path on errors
    ```
    
    Asks the running gateway for a full snapshot (WS-only). See [Health](https://docs.openclaw.ai/gateway/health).

## Quick start and first-run setup

### Im stuck what’s the fastest way to get unstuck

Use a local AI agent that can **see your machine**. That is far more effective than asking in Discord, because most “I’m stuck” cases are **local config or environment issues** that remote helpers cannot inspect.

*   **Claude Code**: [https://www.anthropic.com/claude-code/](https://www.anthropic.com/claude-code/)
*   **OpenAI Codex**: [https://openai.com/codex/](https://openai.com/codex/)

These tools can read the repo, run commands, inspect logs, and help fix your machine-level setup (PATH, services, permissions, auth files). Give them the **full source checkout** via the hackable (git) install:

```
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git
```

This installs OpenClaw **from a git checkout**, so the agent can read the code + docs and reason about the exact version you are running. You can always switch back to stable later by re-running the installer without `--install-method git`. Tip: ask the agent to **plan and supervise** the fix (step-by-step), then execute only the necessary commands. That keeps changes small and easier to audit. If you discover a real bug or fix, please file a GitHub issue or send a PR: [https://github.com/openclaw/openclaw/issues](https://github.com/openclaw/openclaw/issues) [https://github.com/openclaw/openclaw/pulls](https://github.com/openclaw/openclaw/pulls) Start with these commands (share outputs when asking for help):

```
openclaw status
openclaw models status
openclaw doctor
```

What they do:

*   `openclaw status`: quick snapshot of gateway/agent health + basic config.
*   `openclaw models status`: checks provider auth + model availability.
*   `openclaw doctor`: validates and repairs common config/state issues.

Other useful CLI checks: `openclaw status --all`, `openclaw logs --follow`, `openclaw gateway status`, `openclaw health --verbose`. Quick debug loop: [First 60 seconds if something’s broken](https://docs.openclaw.ai/help/faq#first-60-seconds-if-somethings-broken). Install docs: [Install](https://docs.openclaw.ai/install), [Installer flags](https://docs.openclaw.ai/install/installer), [Updating](https://docs.openclaw.ai/install/updating).

### What’s the recommended way to install and set up OpenClaw

The repo recommends running from source and using the onboarding wizard:

```
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw onboard --install-daemon
```

The wizard can also build UI assets automatically. After onboarding, you typically run the Gateway on port **18789**. From source (contributors/dev):

```
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm build
pnpm ui:build # auto-installs UI deps on first run
openclaw onboard
```

If you don’t have a global install yet, run it via `pnpm openclaw onboard`.

### How do I open the dashboard after onboarding

The wizard opens your browser with a clean (non-tokenized) dashboard URL right after onboarding and also prints the link in the summary. Keep that tab open; if it didn’t launch, copy/paste the printed URL on the same machine.

### How do I authenticate the dashboard token on localhost vs remote

**Localhost (same machine):**

*   Open `http://127.0.0.1:18789/`.
*   If it asks for auth, paste the token from `gateway.auth.token` (or `OPENCLAW_GATEWAY_TOKEN`) into Control UI settings.
*   Retrieve it from the gateway host: `openclaw config get gateway.auth.token` (or generate one: `openclaw doctor --generate-gateway-token`).

**Not on localhost:**

*   **Tailscale Serve** (recommended): keep bind loopback, run `openclaw gateway --tailscale serve`, open `https://<magicdns>/`. If `gateway.auth.allowTailscale` is `true`, identity headers satisfy Control UI/WebSocket auth (no token, assumes trusted gateway host); HTTP APIs still require token/password.
*   **Tailnet bind**: run `openclaw gateway --bind tailnet --token "<token>"`, open `http://<tailscale-ip>:18789/`, paste token in dashboard settings.
*   **SSH tunnel**: `ssh -N -L 18789:127.0.0.1:18789 user@host` then open `http://127.0.0.1:18789/` and paste the token in Control UI settings.

See [Dashboard](https://docs.openclaw.ai/web/dashboard) and [Web surfaces](https://docs.openclaw.ai/web) for bind modes and auth details.

### What runtime do I need

Node **\>= 22** is required. `pnpm` is recommended. Bun is **not recommended** for the Gateway.

### Does it run on Raspberry Pi

Yes. The Gateway is lightweight - docs list **512MB-1GB RAM**, **1 core**, and about **500MB** disk as enough for personal use, and note that a **Raspberry Pi 4 can run it**. If you want extra headroom (logs, media, other services), **2GB is recommended**, but it’s not a hard minimum. Tip: a small Pi/VPS can host the Gateway, and you can pair **nodes** on your laptop/phone for local screen/camera/canvas or command execution. See [Nodes](https://docs.openclaw.ai/nodes).

### Any tips for Raspberry Pi installs

Short version: it works, but expect rough edges.

*   Use a **64-bit** OS and keep Node >= 22.
*   Prefer the **hackable (git) install** so you can see logs and update fast.
*   Start without channels/skills, then add them one by one.
*   If you hit weird binary issues, it is usually an **ARM compatibility** problem.

Docs: [Linux](https://docs.openclaw.ai/platforms/linux), [Install](https://docs.openclaw.ai/install).

### It is stuck on wake up my friend onboarding will not hatch What now

That screen depends on the Gateway being reachable and authenticated. The TUI also sends “Wake up, my friend!” automatically on first hatch. If you see that line with **no reply** and tokens stay at 0, the agent never ran.

1.  Restart the Gateway:

2.  Check status + auth:

```
openclaw status
openclaw models status
openclaw logs --follow
```

3.  If it still hangs, run:

If the Gateway is remote, ensure the tunnel/Tailscale connection is up and that the UI is pointed at the right Gateway. See [Remote access](https://docs.openclaw.ai/gateway/remote).

### Can I migrate my setup to a new machine Mac mini without redoing onboarding

Yes. Copy the **state directory** and **workspace**, then run Doctor once. This keeps your bot “exactly the same” (memory, session history, auth, and channel state) as long as you copy **both** locations:

1.  Install OpenClaw on the new machine.
2.  Copy `$OPENCLAW_STATE_DIR` (default: `~/.openclaw`) from the old machine.
3.  Copy your workspace (default: `~/.openclaw/workspace`).
4.  Run `openclaw doctor` and restart the Gateway service.

That preserves config, auth profiles, WhatsApp creds, sessions, and memory. If you’re in remote mode, remember the gateway host owns the session store and workspace. **Important:** if you only commit/push your workspace to GitHub, you’re backing up **memory + bootstrap files**, but **not** session history or auth. Those live under `~/.openclaw/` (for example `~/.openclaw/agents/<agentId>/sessions/`). Related: [Migrating](https://docs.openclaw.ai/install/migrating), [Where things live on disk](https://docs.openclaw.ai/help/faq#where-does-openclaw-store-its-data), [Agent workspace](https://docs.openclaw.ai/concepts/agent-workspace), [Doctor](https://docs.openclaw.ai/gateway/doctor), [Remote mode](https://docs.openclaw.ai/gateway/remote).

### Where do I see what is new in the latest version

Check the GitHub changelog: [https://github.com/openclaw/openclaw/blob/main/CHANGELOG.md](https://github.com/openclaw/openclaw/blob/main/CHANGELOG.md) Newest entries are at the top. If the top section is marked **Unreleased**, the next dated section is the latest shipped version. Entries are grouped by **Highlights**, **Changes**, and **Fixes** (plus docs/other sections when needed).

### I can’t access docs.openclaw.ai SSL error What now

Some Comcast/Xfinity connections incorrectly block `docs.openclaw.ai` via Xfinity Advanced Security. Disable it or allowlist `docs.openclaw.ai`, then retry. More detail: [Troubleshooting](https://docs.openclaw.ai/help/troubleshooting#docsopenclawai-shows-an-ssl-error-comcastxfinity). Please help us unblock it by reporting here: [https://spa.xfinity.com/check\_url\_status](https://spa.xfinity.com/check_url_status). If you still can’t reach the site, the docs are mirrored on GitHub: [https://github.com/openclaw/openclaw/tree/main/docs](https://github.com/openclaw/openclaw/tree/main/docs)

### What’s the difference between stable and beta

**Stable** and **beta** are **npm dist-tags**, not separate code lines:

*   `latest` = stable
*   `beta` = early build for testing

We ship builds to **beta**, test them, and once a build is solid we **promote that same version to `latest`**. That’s why beta and stable can point at the **same version**. See what changed: [https://github.com/openclaw/openclaw/blob/main/CHANGELOG.md](https://github.com/openclaw/openclaw/blob/main/CHANGELOG.md)

### How do I install the beta version and what’s the difference between beta and dev

**Beta** is the npm dist-tag `beta` (may match `latest`). **Dev** is the moving head of `main` (git); when published, it uses the npm dist-tag `dev`. One-liners (macOS/Linux):

```
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --beta
```

```
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --install-method git
```

Windows installer (PowerShell): [https://openclaw.ai/install.ps1](https://openclaw.ai/install.ps1) More detail: [Development channels](https://docs.openclaw.ai/install/development-channels) and [Installer flags](https://docs.openclaw.ai/install/installer).

### How long does install and onboarding usually take

Rough guide:

*   **Install:** 2-5 minutes
*   **Onboarding:** 5-15 minutes depending on how many channels/models you configure

If it hangs, use [Installer stuck](https://docs.openclaw.ai/help/faq#installer-stuck-how-do-i-get-more-feedback) and the fast debug loop in [Im stuck](https://docs.openclaw.ai/help/faq#im-stuck--whats-the-fastest-way-to-get-unstuck).

### How do I try the latest bits

Two options:

1.  **Dev channel (git checkout):**

```
openclaw update --channel dev
```

This switches to the `main` branch and updates from source.

2.  **Hackable install (from the installer site):**

```
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git
```

That gives you a local repo you can edit, then update via git. If you prefer a clean clone manually, use:

```
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm build
```

Docs: [Update](https://docs.openclaw.ai/cli/update), [Development channels](https://docs.openclaw.ai/install/development-channels), [Install](https://docs.openclaw.ai/install).

### Installer stuck How do I get more feedback

Re-run the installer with **verbose output**:

```
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --verbose
```

Beta install with verbose:

```
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --beta --verbose
```

For a hackable (git) install:

```
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git --verbose
```

Windows (PowerShell) equivalent:

```
# install.ps1 has no dedicated -Verbose flag yet.
Set-PSDebug -Trace 1
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard
Set-PSDebug -Trace 0
```

More options: [Installer flags](https://docs.openclaw.ai/install/installer).

### Windows install says git not found or openclaw not recognized

Two common Windows issues: **1) npm error spawn git / git not found**

*   Install **Git for Windows** and make sure `git` is on your PATH.
*   Close and reopen PowerShell, then re-run the installer.

**2) openclaw is not recognized after install**

*   Your npm global bin folder is not on PATH.
*   Check the path:
*   Add that directory to your user PATH (no `\bin` suffix needed on Windows; on most systems it is `%AppData%\npm`).
*   Close and reopen PowerShell after updating PATH.

If you want the smoothest Windows setup, use **WSL2** instead of native Windows. Docs: [Windows](https://docs.openclaw.ai/platforms/windows).

### Windows exec output shows garbled Chinese text what should I do

This is usually a console code page mismatch on native Windows shells. Symptoms:

*   `system.run`/`exec` output renders Chinese as mojibake
*   The same command looks fine in another terminal profile

Quick workaround in PowerShell:

```
chcp 65001
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
```

Then restart the Gateway and retry your command:

If you still reproduce this on latest OpenClaw, track/report it in:

*   [Issue #30640](https://github.com/openclaw/openclaw/issues/30640)

### The docs didn’t answer my question how do I get a better answer

Use the **hackable (git) install** so you have the full source and docs locally, then ask your bot (or Claude/Codex) _from that folder_ so it can read the repo and answer precisely.

```
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git
```

More detail: [Install](https://docs.openclaw.ai/install) and [Installer flags](https://docs.openclaw.ai/install/installer).

### How do I install OpenClaw on Linux

Short answer: follow the Linux guide, then run the onboarding wizard.

*   Linux quick path + service install: [Linux](https://docs.openclaw.ai/platforms/linux).
*   Full walkthrough: [Getting Started](https://docs.openclaw.ai/start/getting-started).
*   Installer + updates: [Install & updates](https://docs.openclaw.ai/install/updating).

### How do I install OpenClaw on a VPS

Any Linux VPS works. Install on the server, then use SSH/Tailscale to reach the Gateway. Guides: [exe.dev](https://docs.openclaw.ai/install/exe-dev), [Hetzner](https://docs.openclaw.ai/install/hetzner), [Fly.io](https://docs.openclaw.ai/install/fly). Remote access: [Gateway remote](https://docs.openclaw.ai/gateway/remote).

### Where are the cloudVPS install guides

We keep a **hosting hub** with the common providers. Pick one and follow the guide:

*   [VPS hosting](https://docs.openclaw.ai/vps) (all providers in one place)
*   [Fly.io](https://docs.openclaw.ai/install/fly)
*   [Hetzner](https://docs.openclaw.ai/install/hetzner)
*   [exe.dev](https://docs.openclaw.ai/install/exe-dev)

How it works in the cloud: the **Gateway runs on the server**, and you access it from your laptop/phone via the Control UI (or Tailscale/SSH). Your state + workspace live on the server, so treat the host as the source of truth and back it up. You can pair **nodes** (Mac/iOS/Android/headless) to that cloud Gateway to access local screen/camera/canvas or run commands on your laptop while keeping the Gateway in the cloud. Hub: [Platforms](https://docs.openclaw.ai/platforms). Remote access: [Gateway remote](https://docs.openclaw.ai/gateway/remote). Nodes: [Nodes](https://docs.openclaw.ai/nodes), [Nodes CLI](https://docs.openclaw.ai/cli/nodes).

### Can I ask OpenClaw to update itself

Short answer: **possible, not recommended**. The update flow can restart the Gateway (which drops the active session), may need a clean git checkout, and can prompt for confirmation. Safer: run updates from a shell as the operator. Use the CLI:

```
openclaw update
openclaw update status
openclaw update --channel stable|beta|dev
openclaw update --tag <dist-tag|version>
openclaw update --no-restart
```

If you must automate from an agent:

```
openclaw update --yes --no-restart
openclaw gateway restart
```

Docs: [Update](https://docs.openclaw.ai/cli/update), [Updating](https://docs.openclaw.ai/install/updating).

### What does the onboarding wizard actually do

`openclaw onboard` is the recommended setup path. In **local mode** it walks you through:

*   **Model/auth setup** (provider OAuth/setup-token flows and API keys supported, plus local model options such as LM Studio)
*   **Workspace** location + bootstrap files
*   **Gateway settings** (bind/port/auth/tailscale)
*   **Providers** (WhatsApp, Telegram, Discord, Mattermost (plugin), Signal, iMessage)
*   **Daemon install** (LaunchAgent on macOS; systemd user unit on Linux/WSL2)
*   **Health checks** and **skills** selection

It also warns if your configured model is unknown or missing auth.

### Do I need a Claude or OpenAI subscription to run this

No. You can run OpenClaw with **API keys** (Anthropic/OpenAI/others) or with **local-only models** so your data stays on your device. Subscriptions (Claude Pro/Max or OpenAI Codex) are optional ways to authenticate those providers. If you choose Anthropic subscription auth, decide for yourself whether to use it: Anthropic has blocked some subscription usage outside Claude Code in the past. OpenAI Codex OAuth is explicitly supported for external tools like OpenClaw. Docs: [Anthropic](https://docs.openclaw.ai/providers/anthropic), [OpenAI](https://docs.openclaw.ai/providers/openai), [Local models](https://docs.openclaw.ai/gateway/local-models), [Models](https://docs.openclaw.ai/concepts/models).

### Can I use Claude Max subscription without an API key

Yes. You can authenticate with a **setup-token** instead of an API key. This is the subscription path. Claude Pro/Max subscriptions **do not include an API key**, so this is the technical path for subscription accounts. But this is your decision: Anthropic has blocked some subscription usage outside Claude Code in the past. If you want the clearest and safest supported path for production, use an Anthropic API key.

### How does Anthropic setuptoken auth work

`claude setup-token` generates a **token string** via the Claude Code CLI (it is not available in the web console). You can run it on **any machine**. Choose **Anthropic token (paste setup-token)** in the wizard or paste it with `openclaw models auth paste-token --provider anthropic`. The token is stored as an auth profile for the **anthropic** provider and used like an API key (no auto-refresh). More detail: [OAuth](https://docs.openclaw.ai/concepts/oauth).

### Where do I find an Anthropic setuptoken

It is **not** in the Anthropic Console. The setup-token is generated by the **Claude Code CLI** on **any machine**:

Copy the token it prints, then choose **Anthropic token (paste setup-token)** in the wizard. If you want to run it on the gateway host, use `openclaw models auth setup-token --provider anthropic`. If you ran `claude setup-token` elsewhere, paste it on the gateway host with `openclaw models auth paste-token --provider anthropic`. See [Anthropic](https://docs.openclaw.ai/providers/anthropic).

### Do you support Claude subscription auth (Claude Pro or Max)

Yes - via **setup-token**. OpenClaw no longer reuses Claude Code CLI OAuth tokens; use a setup-token or an Anthropic API key. Generate the token anywhere and paste it on the gateway host. See [Anthropic](https://docs.openclaw.ai/providers/anthropic) and [OAuth](https://docs.openclaw.ai/concepts/oauth). Important: this is technical compatibility, not a policy guarantee. Anthropic has blocked some subscription usage outside Claude Code in the past. You need to decide whether to use it and verify Anthropic’s current terms. For production or multi-user workloads, Anthropic API key auth is the safer, recommended choice.

### Why am I seeing HTTP 429 ratelimiterror from Anthropic

That means your **Anthropic quota/rate limit** is exhausted for the current window. If you use a **Claude subscription** (setup-token), wait for the window to reset or upgrade your plan. If you use an **Anthropic API key**, check the Anthropic Console for usage/billing and raise limits as needed. If the message is specifically: `Extra usage is required for long context requests`, the request is trying to use Anthropic’s 1M context beta (`context1m: true`). That only works when your credential is eligible for long-context billing (API key billing or subscription with Extra Usage enabled). Tip: set a **fallback model** so OpenClaw can keep replying while a provider is rate-limited. See [Models](https://docs.openclaw.ai/cli/models), [OAuth](https://docs.openclaw.ai/concepts/oauth), and [/gateway/troubleshooting#anthropic-429-extra-usage-required-for-long-context](https://docs.openclaw.ai/gateway/troubleshooting#anthropic-429-extra-usage-required-for-long-context).

### Is AWS Bedrock supported

Yes - via pi-ai’s **Amazon Bedrock (Converse)** provider with **manual config**. You must supply AWS credentials/region on the gateway host and add a Bedrock provider entry in your models config. See [Amazon Bedrock](https://docs.openclaw.ai/providers/bedrock) and [Model providers](https://docs.openclaw.ai/providers/models). If you prefer a managed key flow, an OpenAI-compatible proxy in front of Bedrock is still a valid option.

### How does Codex auth work

OpenClaw supports **OpenAI Code (Codex)** via OAuth (ChatGPT sign-in). The wizard can run the OAuth flow and will set the default model to `openai-codex/gpt-5.4` when appropriate. See [Model providers](https://docs.openclaw.ai/concepts/model-providers) and [Wizard](https://docs.openclaw.ai/start/wizard).

### Do you support OpenAI subscription auth Codex OAuth

Yes. OpenClaw fully supports **OpenAI Code (Codex) subscription OAuth**. OpenAI explicitly allows subscription OAuth usage in external tools/workflows like OpenClaw. The onboarding wizard can run the OAuth flow for you. See [OAuth](https://docs.openclaw.ai/concepts/oauth), [Model providers](https://docs.openclaw.ai/concepts/model-providers), and [Wizard](https://docs.openclaw.ai/start/wizard).

### How do I set up Gemini CLI OAuth

Gemini CLI uses a **plugin auth flow**, not a client id or secret in `openclaw.json`. Steps:

1.  Enable the plugin: `openclaw plugins enable google-gemini-cli-auth`
2.  Login: `openclaw models auth login --provider google-gemini-cli --set-default`

This stores OAuth tokens in auth profiles on the gateway host. Details: [Model providers](https://docs.openclaw.ai/concepts/model-providers).

### Is a local model OK for casual chats

Usually no. OpenClaw needs large context + strong safety; small cards truncate and leak. If you must, run the **largest** MiniMax M2.5 build you can locally (LM Studio) and see [/gateway/local-models](https://docs.openclaw.ai/gateway/local-models). Smaller/quantized models increase prompt-injection risk - see [Security](https://docs.openclaw.ai/gateway/security).

### How do I keep hosted model traffic in a specific region

Pick region-pinned endpoints. OpenRouter exposes US-hosted options for MiniMax, Kimi, and GLM; choose the US-hosted variant to keep data in-region. You can still list Anthropic/OpenAI alongside these by using `models.mode: "merge"` so fallbacks stay available while respecting the regioned provider you select.

### Do I have to buy a Mac Mini to install this

No. OpenClaw runs on macOS or Linux (Windows via WSL2). A Mac mini is optional - some people buy one as an always-on host, but a small VPS, home server, or Raspberry Pi-class box works too. You only need a Mac **for macOS-only tools**. For iMessage, use [BlueBubbles](https://docs.openclaw.ai/channels/bluebubbles) (recommended) - the BlueBubbles server runs on any Mac, and the Gateway can run on Linux or elsewhere. If you want other macOS-only tools, run the Gateway on a Mac or pair a macOS node. Docs: [BlueBubbles](https://docs.openclaw.ai/channels/bluebubbles), [Nodes](https://docs.openclaw.ai/nodes), [Mac remote mode](https://docs.openclaw.ai/platforms/mac/remote).

### Do I need a Mac mini for iMessage support

You need **some macOS device** signed into Messages. It does **not** have to be a Mac mini - any Mac works. **Use [BlueBubbles](https://docs.openclaw.ai/channels/bluebubbles)** (recommended) for iMessage - the BlueBubbles server runs on macOS, while the Gateway can run on Linux or elsewhere. Common setups:

*   Run the Gateway on Linux/VPS, and run the BlueBubbles server on any Mac signed into Messages.
*   Run everything on the Mac if you want the simplest single‑machine setup.

Docs: [BlueBubbles](https://docs.openclaw.ai/channels/bluebubbles), [Nodes](https://docs.openclaw.ai/nodes), [Mac remote mode](https://docs.openclaw.ai/platforms/mac/remote).

### If I buy a Mac mini to run OpenClaw can I connect it to my MacBook Pro

Yes. The **Mac mini can run the Gateway**, and your MacBook Pro can connect as a **node** (companion device). Nodes don’t run the Gateway - they provide extra capabilities like screen/camera/canvas and `system.run` on that device. Common pattern:

*   Gateway on the Mac mini (always-on).
*   MacBook Pro runs the macOS app or a node host and pairs to the Gateway.
*   Use `openclaw nodes status` / `openclaw nodes list` to see it.

Docs: [Nodes](https://docs.openclaw.ai/nodes), [Nodes CLI](https://docs.openclaw.ai/cli/nodes).

### Can I use Bun

Bun is **not recommended**. We see runtime bugs, especially with WhatsApp and Telegram. Use **Node** for stable gateways. If you still want to experiment with Bun, do it on a non-production gateway without WhatsApp/Telegram.

### Telegram what goes in allowFrom

`channels.telegram.allowFrom` is **the human sender’s Telegram user ID** (numeric). It is not the bot username. The onboarding wizard accepts `@username` input and resolves it to a numeric ID, but OpenClaw authorization uses numeric IDs only. Safer (no third-party bot):

*   DM your bot, then run `openclaw logs --follow` and read `from.id`.

Official Bot API:

*   DM your bot, then call `https://api.telegram.org/bot<bot_token>/getUpdates` and read `message.from.id`.

Third-party (less private):

*   DM `@userinfobot` or `@getidsbot`.

See [/channels/telegram](https://docs.openclaw.ai/channels/telegram#access-control-dms--groups).

### Can multiple people use one WhatsApp number with different OpenClaw instances

Yes, via **multi-agent routing**. Bind each sender’s WhatsApp **DM** (peer `kind: "direct"`, sender E.164 like `+15551234567`) to a different `agentId`, so each person gets their own workspace and session store. Replies still come from the **same WhatsApp account**, and DM access control (`channels.whatsapp.dmPolicy` / `channels.whatsapp.allowFrom`) is global per WhatsApp account. See [Multi-Agent Routing](https://docs.openclaw.ai/concepts/multi-agent) and [WhatsApp](https://docs.openclaw.ai/channels/whatsapp).

### Can I run a fast chat agent and an Opus for coding agent

Yes. Use multi-agent routing: give each agent its own default model, then bind inbound routes (provider account or specific peers) to each agent. Example config lives in [Multi-Agent Routing](https://docs.openclaw.ai/concepts/multi-agent). See also [Models](https://docs.openclaw.ai/concepts/models) and [Configuration](https://docs.openclaw.ai/gateway/configuration).

### Does Homebrew work on Linux

Yes. Homebrew supports Linux (Linuxbrew). Quick setup:

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> ~/.profile
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
brew install <formula>
```

If you run OpenClaw via systemd, ensure the service PATH includes `/home/linuxbrew/.linuxbrew/bin` (or your brew prefix) so `brew`\-installed tools resolve in non-login shells. Recent builds also prepend common user bin dirs on Linux systemd services (for example `~/.local/bin`, `~/.npm-global/bin`, `~/.local/share/pnpm`, `~/.bun/bin`) and honor `PNPM_HOME`, `NPM_CONFIG_PREFIX`, `BUN_INSTALL`, `VOLTA_HOME`, `ASDF_DATA_DIR`, `NVM_DIR`, and `FNM_DIR` when set.

### What’s the difference between the hackable git install and npm install

*   **Hackable (git) install:** full source checkout, editable, best for contributors. You run builds locally and can patch code/docs.
*   **npm install:** global CLI install, no repo, best for “just run it.” Updates come from npm dist-tags.

Docs: [Getting started](https://docs.openclaw.ai/start/getting-started), [Updating](https://docs.openclaw.ai/install/updating).

### Can I switch between npm and git installs later

Yes. Install the other flavor, then run Doctor so the gateway service points at the new entrypoint. This **does not delete your data** - it only changes the OpenClaw code install. Your state (`~/.openclaw`) and workspace (`~/.openclaw/workspace`) stay untouched. From npm → git:

```
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm build
openclaw doctor
openclaw gateway restart
```

From git → npm:

```
npm install -g openclaw@latest
openclaw doctor
openclaw gateway restart
```

Doctor detects a gateway service entrypoint mismatch and offers to rewrite the service config to match the current install (use `--repair` in automation). Backup tips: see [Backup strategy](https://docs.openclaw.ai/help/faq#whats-the-recommended-backup-strategy).

### Should I run the Gateway on my laptop or a VPS

Short answer: **if you want 24/7 reliability, use a VPS**. If you want the lowest friction and you’re okay with sleep/restarts, run it locally. **Laptop (local Gateway)**

*   **Pros:** no server cost, direct access to local files, live browser window.
*   **Cons:** sleep/network drops = disconnects, OS updates/reboots interrupt, must stay awake.

**VPS / cloud**

*   **Pros:** always-on, stable network, no laptop sleep issues, easier to keep running.
*   **Cons:** often run headless (use screenshots), remote file access only, you must SSH for updates.

**OpenClaw-specific note:** WhatsApp/Telegram/Slack/Mattermost (plugin)/Discord all work fine from a VPS. The only real trade-off is **headless browser** vs a visible window. See [Browser](https://docs.openclaw.ai/tools/browser). **Recommended default:** VPS if you had gateway disconnects before. Local is great when you’re actively using the Mac and want local file access or UI automation with a visible browser.

### How important is it to run OpenClaw on a dedicated machine

Not required, but **recommended for reliability and isolation**.

*   **Dedicated host (VPS/Mac mini/Pi):** always-on, fewer sleep/reboot interruptions, cleaner permissions, easier to keep running.
*   **Shared laptop/desktop:** totally fine for testing and active use, but expect pauses when the machine sleeps or updates.

If you want the best of both worlds, keep the Gateway on a dedicated host and pair your laptop as a **node** for local screen/camera/exec tools. See [Nodes](https://docs.openclaw.ai/nodes). For security guidance, read [Security](https://docs.openclaw.ai/gateway/security).

### What are the minimum VPS requirements and recommended OS

OpenClaw is lightweight. For a basic Gateway + one chat channel:

*   **Absolute minimum:** 1 vCPU, 1GB RAM, ~500MB disk.
*   **Recommended:** 1-2 vCPU, 2GB RAM or more for headroom (logs, media, multiple channels). Node tools and browser automation can be resource hungry.

OS: use **Ubuntu LTS** (or any modern Debian/Ubuntu). The Linux install path is best tested there. Docs: [Linux](https://docs.openclaw.ai/platforms/linux), [VPS hosting](https://docs.openclaw.ai/vps).

### Can I run OpenClaw in a VM and what are the requirements

Yes. Treat a VM the same as a VPS: it needs to be always on, reachable, and have enough RAM for the Gateway and any channels you enable. Baseline guidance:

*   **Absolute minimum:** 1 vCPU, 1GB RAM.
*   **Recommended:** 2GB RAM or more if you run multiple channels, browser automation, or media tools.
*   **OS:** Ubuntu LTS or another modern Debian/Ubuntu.

If you are on Windows, **WSL2 is the easiest VM style setup** and has the best tooling compatibility. See [Windows](https://docs.openclaw.ai/platforms/windows), [VPS hosting](https://docs.openclaw.ai/vps). If you are running macOS in a VM, see [macOS VM](https://docs.openclaw.ai/install/macos-vm).

## What is OpenClaw?

### What is OpenClaw in one paragraph

OpenClaw is a personal AI assistant you run on your own devices. It replies on the messaging surfaces you already use (WhatsApp, Telegram, Slack, Mattermost (plugin), Discord, Google Chat, Signal, iMessage, WebChat) and can also do voice + a live Canvas on supported platforms. The **Gateway** is the always-on control plane; the assistant is the product.

### What’s the value proposition

OpenClaw is not “just a Claude wrapper.” It’s a **local-first control plane** that lets you run a capable assistant on **your own hardware**, reachable from the chat apps you already use, with stateful sessions, memory, and tools - without handing control of your workflows to a hosted SaaS. Highlights:

*   **Your devices, your data:** run the Gateway wherever you want (Mac, Linux, VPS) and keep the workspace + session history local.
*   **Real channels, not a web sandbox:** WhatsApp/Telegram/Slack/Discord/Signal/iMessage/etc, plus mobile voice and Canvas on supported platforms.
*   **Model-agnostic:** use Anthropic, OpenAI, MiniMax, OpenRouter, etc., with per-agent routing and failover.
*   **Local-only option:** run local models so **all data can stay on your device** if you want.
*   **Multi-agent routing:** separate agents per channel, account, or task, each with its own workspace and defaults.
*   **Open source and hackable:** inspect, extend, and self-host without vendor lock-in.

Docs: [Gateway](https://docs.openclaw.ai/gateway), [Channels](https://docs.openclaw.ai/channels), [Multi-agent](https://docs.openclaw.ai/concepts/multi-agent), [Memory](https://docs.openclaw.ai/concepts/memory).

### I just set it up what should I do first

Good first projects:

*   Build a website (WordPress, Shopify, or a simple static site).
*   Prototype a mobile app (outline, screens, API plan).
*   Organize files and folders (cleanup, naming, tagging).
*   Connect Gmail and automate summaries or follow ups.

It can handle large tasks, but it works best when you split them into phases and use sub agents for parallel work.

### What are the top five everyday use cases for OpenClaw

Everyday wins usually look like:

*   **Personal briefings:** summaries of inbox, calendar, and news you care about.
*   **Research and drafting:** quick research, summaries, and first drafts for emails or docs.
*   **Reminders and follow ups:** cron or heartbeat driven nudges and checklists.
*   **Browser automation:** filling forms, collecting data, and repeating web tasks.
*   **Cross device coordination:** send a task from your phone, let the Gateway run it on a server, and get the result back in chat.

### Can OpenClaw help with lead gen outreach ads and blogs for a SaaS

Yes for **research, qualification, and drafting**. It can scan sites, build shortlists, summarize prospects, and write outreach or ad copy drafts. For **outreach or ad runs**, keep a human in the loop. Avoid spam, follow local laws and platform policies, and review anything before it is sent. The safest pattern is to let OpenClaw draft and you approve. Docs: [Security](https://docs.openclaw.ai/gateway/security).

### What are the advantages vs Claude Code for web development

OpenClaw is a **personal assistant** and coordination layer, not an IDE replacement. Use Claude Code or Codex for the fastest direct coding loop inside a repo. Use OpenClaw when you want durable memory, cross-device access, and tool orchestration. Advantages:

*   **Persistent memory + workspace** across sessions
*   **Multi-platform access** (WhatsApp, Telegram, TUI, WebChat)
*   **Tool orchestration** (browser, files, scheduling, hooks)
*   **Always-on Gateway** (run on a VPS, interact from anywhere)
*   **Nodes** for local browser/screen/camera/exec

Showcase: [https://openclaw.ai/showcase](https://openclaw.ai/showcase)

## Skills and automation

### How do I customize skills without keeping the repo dirty

Use managed overrides instead of editing the repo copy. Put your changes in `~/.openclaw/skills/<name>/SKILL.md` (or add a folder via `skills.load.extraDirs` in `~/.openclaw/openclaw.json`). Precedence is `<workspace>/skills` > `~/.openclaw/skills` > bundled, so managed overrides win without touching git. Only upstream-worthy edits should live in the repo and go out as PRs.

### Can I load skills from a custom folder

Yes. Add extra directories via `skills.load.extraDirs` in `~/.openclaw/openclaw.json` (lowest precedence). Default precedence remains: `<workspace>/skills` → `~/.openclaw/skills` → bundled → `skills.load.extraDirs`. `clawhub` installs into `./skills` by default, which OpenClaw treats as `<workspace>/skills`.

### How can I use different models for different tasks

Today the supported patterns are:

*   **Cron jobs**: isolated jobs can set a `model` override per job.
*   **Sub-agents**: route tasks to separate agents with different default models.
*   **On-demand switch**: use `/model` to switch the current session model at any time.

See [Cron jobs](https://docs.openclaw.ai/automation/cron-jobs), [Multi-Agent Routing](https://docs.openclaw.ai/concepts/multi-agent), and [Slash commands](https://docs.openclaw.ai/tools/slash-commands).

### The bot freezes while doing heavy work How do I offload that

Use **sub-agents** for long or parallel tasks. Sub-agents run in their own session, return a summary, and keep your main chat responsive. Ask your bot to “spawn a sub-agent for this task” or use `/subagents`. Use `/status` in chat to see what the Gateway is doing right now (and whether it is busy). Token tip: long tasks and sub-agents both consume tokens. If cost is a concern, set a cheaper model for sub-agents via `agents.defaults.subagents.model`. Docs: [Sub-agents](https://docs.openclaw.ai/tools/subagents).

### How do thread-bound subagent sessions work on Discord

Use thread bindings. You can bind a Discord thread to a subagent or session target so follow-up messages in that thread stay on that bound session. Basic flow:

*   Spawn with `sessions_spawn` using `thread: true` (and optionally `mode: "session"` for persistent follow-up).
*   Or manually bind with `/focus <target>`.
*   Use `/agents` to inspect binding state.
*   Use `/session idle <duration|off>` and `/session max-age <duration|off>` to control auto-unfocus.
*   Use `/unfocus` to detach the thread.

Required config:

*   Global defaults: `session.threadBindings.enabled`, `session.threadBindings.idleHours`, `session.threadBindings.maxAgeHours`.
*   Discord overrides: `channels.discord.threadBindings.enabled`, `channels.discord.threadBindings.idleHours`, `channels.discord.threadBindings.maxAgeHours`.
*   Auto-bind on spawn: set `channels.discord.threadBindings.spawnSubagentSessions: true`.

Docs: [Sub-agents](https://docs.openclaw.ai/tools/subagents), [Discord](https://docs.openclaw.ai/channels/discord), [Configuration Reference](https://docs.openclaw.ai/gateway/configuration-reference), [Slash commands](https://docs.openclaw.ai/tools/slash-commands).

### Cron or reminders do not fire What should I check

Cron runs inside the Gateway process. If the Gateway is not running continuously, scheduled jobs will not run. Checklist:

*   Confirm cron is enabled (`cron.enabled`) and `OPENCLAW_SKIP_CRON` is not set.
*   Check the Gateway is running 24/7 (no sleep/restarts).
*   Verify timezone settings for the job (`--tz` vs host timezone).

Debug:

```
openclaw cron run <jobId> --force
openclaw cron runs --id <jobId> --limit 50
```

Docs: [Cron jobs](https://docs.openclaw.ai/automation/cron-jobs), [Cron vs Heartbeat](https://docs.openclaw.ai/automation/cron-vs-heartbeat).

### How do I install skills on Linux

Use **ClawHub** (CLI) or drop skills into your workspace. The macOS Skills UI isn’t available on Linux. Browse skills at [https://clawhub.com](https://clawhub.com/). Install the ClawHub CLI (pick one package manager):

### Can OpenClaw run tasks on a schedule or continuously in the background

Yes. Use the Gateway scheduler:

*   **Cron jobs** for scheduled or recurring tasks (persist across restarts).
*   **Heartbeat** for “main session” periodic checks.
*   **Isolated jobs** for autonomous agents that post summaries or deliver to chats.

Docs: [Cron jobs](https://docs.openclaw.ai/automation/cron-jobs), [Cron vs Heartbeat](https://docs.openclaw.ai/automation/cron-vs-heartbeat), [Heartbeat](https://docs.openclaw.ai/gateway/heartbeat).

### Can I run Apple macOS-only skills from Linux?

Not directly. macOS skills are gated by `metadata.openclaw.os` plus required binaries, and skills only appear in the system prompt when they are eligible on the **Gateway host**. On Linux, `darwin`\-only skills (like `apple-notes`, `apple-reminders`, `things-mac`) will not load unless you override the gating. You have three supported patterns: **Option A - run the Gateway on a Mac (simplest).** Run the Gateway where the macOS binaries exist, then connect from Linux in [remote mode](https://docs.openclaw.ai/help/faq#how-do-i-run-openclaw-in-remote-mode-client-connects-to-a-gateway-elsewhere) or over Tailscale. The skills load normally because the Gateway host is macOS. **Option B - use a macOS node (no SSH).** Run the Gateway on Linux, pair a macOS node (menubar app), and set **Node Run Commands** to “Always Ask” or “Always Allow” on the Mac. OpenClaw can treat macOS-only skills as eligible when the required binaries exist on the node. The agent runs those skills via the `nodes` tool. If you choose “Always Ask”, approving “Always Allow” in the prompt adds that command to the allowlist. **Option C - proxy macOS binaries over SSH (advanced).** Keep the Gateway on Linux, but make the required CLI binaries resolve to SSH wrappers that run on a Mac. Then override the skill to allow Linux so it stays eligible.

1.  Create an SSH wrapper for the binary (example: `memo` for Apple Notes):
    
    ```
    #!/usr/bin/env bash
    set -euo pipefail
    exec ssh -T user@mac-host /opt/homebrew/bin/memo "$@"
    ```
    
2.  Put the wrapper on `PATH` on the Linux host (for example `~/bin/memo`).
3.  Override the skill metadata (workspace or `~/.openclaw/skills`) to allow Linux:
    
    ```
    ---
    name: apple-notes
    description: Manage Apple Notes via the memo CLI on macOS.
    metadata: { "openclaw": { "os": ["darwin", "linux"], "requires": { "bins": ["memo"] } } }
    ---
    ```
    
4.  Start a new session so the skills snapshot refreshes.

### Do you have a Notion or HeyGen integration

Not built-in today. Options:

*   **Custom skill / plugin:** best for reliable API access (Notion/HeyGen both have APIs).
*   **Browser automation:** works without code but is slower and more fragile.

If you want to keep context per client (agency workflows), a simple pattern is:

*   One Notion page per client (context + preferences + active work).
*   Ask the agent to fetch that page at the start of a session.

If you want a native integration, open a feature request or build a skill targeting those APIs. Install skills:

```
clawhub install <skill-slug>
clawhub update --all
```

ClawHub installs into `./skills` under your current directory (or falls back to your configured OpenClaw workspace); OpenClaw treats that as `<workspace>/skills` on the next session. For shared skills across agents, place them in `~/.openclaw/skills/<name>/SKILL.md`. Some skills expect binaries installed via Homebrew; on Linux that means Linuxbrew (see the Homebrew Linux FAQ entry above). See [Skills](https://docs.openclaw.ai/tools/skills) and [ClawHub](https://docs.openclaw.ai/tools/clawhub).

### How do I install the Chrome extension for browser takeover

Use the built-in installer, then load the unpacked extension in Chrome:

```
openclaw browser extension install
openclaw browser extension path
```

Then Chrome → `chrome://extensions` → enable “Developer mode” → “Load unpacked” → pick that folder. Full guide (including remote Gateway + security notes): [Chrome extension](https://docs.openclaw.ai/tools/chrome-extension) If the Gateway runs on the same machine as Chrome (default setup), you usually **do not** need anything extra. If the Gateway runs elsewhere, run a node host on the browser machine so the Gateway can proxy browser actions. You still need to click the extension button on the tab you want to control (it doesn’t auto-attach).

## Sandboxing and memory

### Is there a dedicated sandboxing doc

Yes. See [Sandboxing](https://docs.openclaw.ai/gateway/sandboxing). For Docker-specific setup (full gateway in Docker or sandbox images), see [Docker](https://docs.openclaw.ai/install/docker).

### Docker feels limited How do I enable full features

The default image is security-first and runs as the `node` user, so it does not include system packages, Homebrew, or bundled browsers. For a fuller setup:

*   Persist `/home/node` with `OPENCLAW_HOME_VOLUME` so caches survive.
*   Bake system deps into the image with `OPENCLAW_DOCKER_APT_PACKAGES`.
*   Install Playwright browsers via the bundled CLI: `node /app/node_modules/playwright-core/cli.js install chromium`
*   Set `PLAYWRIGHT_BROWSERS_PATH` and ensure the path is persisted.

Docs: [Docker](https://docs.openclaw.ai/install/docker), [Browser](https://docs.openclaw.ai/tools/browser). **Can I keep DMs personal but make groups public sandboxed with one agent** Yes - if your private traffic is **DMs** and your public traffic is **groups**. Use `agents.defaults.sandbox.mode: "non-main"` so group/channel sessions (non-main keys) run in Docker, while the main DM session stays on-host. Then restrict what tools are available in sandboxed sessions via `tools.sandbox.tools`. Setup walkthrough + example config: [Groups: personal DMs + public groups](https://docs.openclaw.ai/channels/groups#pattern-personal-dms-public-groups-single-agent) Key config reference: [Gateway configuration](https://docs.openclaw.ai/gateway/configuration#agentsdefaultssandbox)

### How do I bind a host folder into the sandbox

Set `agents.defaults.sandbox.docker.binds` to `["host:path:mode"]` (e.g., `"/home/user/src:/src:ro"`). Global + per-agent binds merge; per-agent binds are ignored when `scope: "shared"`. Use `:ro` for anything sensitive and remember binds bypass the sandbox filesystem walls. See [Sandboxing](https://docs.openclaw.ai/gateway/sandboxing#custom-bind-mounts) and [Sandbox vs Tool Policy vs Elevated](https://docs.openclaw.ai/gateway/sandbox-vs-tool-policy-vs-elevated#bind-mounts-security-quick-check) for examples and safety notes.

### How does memory work

OpenClaw memory is just Markdown files in the agent workspace:

*   Daily notes in `memory/YYYY-MM-DD.md`
*   Curated long-term notes in `MEMORY.md` (main/private sessions only)

OpenClaw also runs a **silent pre-compaction memory flush** to remind the model to write durable notes before auto-compaction. This only runs when the workspace is writable (read-only sandboxes skip it). See [Memory](https://docs.openclaw.ai/concepts/memory).

### Memory keeps forgetting things How do I make it stick

Ask the bot to **write the fact to memory**. Long-term notes belong in `MEMORY.md`, short-term context goes into `memory/YYYY-MM-DD.md`. This is still an area we are improving. It helps to remind the model to store memories; it will know what to do. If it keeps forgetting, verify the Gateway is using the same workspace on every run. Docs: [Memory](https://docs.openclaw.ai/concepts/memory), [Agent workspace](https://docs.openclaw.ai/concepts/agent-workspace).

### Does semantic memory search require an OpenAI API key

Only if you use **OpenAI embeddings**. Codex OAuth covers chat/completions and does **not** grant embeddings access, so **signing in with Codex (OAuth or the Codex CLI login)** does not help for semantic memory search. OpenAI embeddings still need a real API key (`OPENAI_API_KEY` or `models.providers.openai.apiKey`). If you don’t set a provider explicitly, OpenClaw auto-selects a provider when it can resolve an API key (auth profiles, `models.providers.*.apiKey`, or env vars). It prefers OpenAI if an OpenAI key resolves, otherwise Gemini if a Gemini key resolves, then Voyage, then Mistral. If no remote key is available, memory search stays disabled until you configure it. If you have a local model path configured and present, OpenClaw prefers `local`. Ollama is supported when you explicitly set `memorySearch.provider = "ollama"`. If you’d rather stay local, set `memorySearch.provider = "local"` (and optionally `memorySearch.fallback = "none"`). If you want Gemini embeddings, set `memorySearch.provider = "gemini"` and provide `GEMINI_API_KEY` (or `memorySearch.remote.apiKey`). We support **OpenAI, Gemini, Voyage, Mistral, Ollama, or local** embedding models - see [Memory](https://docs.openclaw.ai/concepts/memory) for the setup details.

### Does memory persist forever What are the limits

Memory files live on disk and persist until you delete them. The limit is your storage, not the model. The **session context** is still limited by the model context window, so long conversations can compact or truncate. That is why memory search exists - it pulls only the relevant parts back into context. Docs: [Memory](https://docs.openclaw.ai/concepts/memory), [Context](https://docs.openclaw.ai/concepts/context).

## Where things live on disk

### Is all data used with OpenClaw saved locally

No - **OpenClaw’s state is local**, but **external services still see what you send them**.

*   **Local by default:** sessions, memory files, config, and workspace live on the Gateway host (`~/.openclaw` + your workspace directory).
*   **Remote by necessity:** messages you send to model providers (Anthropic/OpenAI/etc.) go to their APIs, and chat platforms (WhatsApp/Telegram/Slack/etc.) store message data on their servers.
*   **You control the footprint:** using local models keeps prompts on your machine, but channel traffic still goes through the channel’s servers.

Related: [Agent workspace](https://docs.openclaw.ai/concepts/agent-workspace), [Memory](https://docs.openclaw.ai/concepts/memory).

### Where does OpenClaw store its data

Everything lives under `$OPENCLAW_STATE_DIR` (default: `~/.openclaw`):

Path

Purpose

`$OPENCLAW_STATE_DIR/openclaw.json`

Main config (JSON5)

`$OPENCLAW_STATE_DIR/credentials/oauth.json`

Legacy OAuth import (copied into auth profiles on first use)

`$OPENCLAW_STATE_DIR/agents/<agentId>/agent/auth-profiles.json`

Auth profiles (OAuth, API keys, and optional `keyRef`/`tokenRef`)

`$OPENCLAW_STATE_DIR/secrets.json`

Optional file-backed secret payload for `file` SecretRef providers

`$OPENCLAW_STATE_DIR/agents/<agentId>/agent/auth.json`

Legacy compatibility file (static `api_key` entries scrubbed)

`$OPENCLAW_STATE_DIR/credentials/`

Provider state (e.g. `whatsapp/<accountId>/creds.json`)

`$OPENCLAW_STATE_DIR/agents/`

Per-agent state (agentDir + sessions)

`$OPENCLAW_STATE_DIR/agents/<agentId>/sessions/`

Conversation history & state (per agent)

`$OPENCLAW_STATE_DIR/agents/<agentId>/sessions/sessions.json`

Session metadata (per agent)

Legacy single-agent path: `~/.openclaw/agent/*` (migrated by `openclaw doctor`). Your **workspace** (AGENTS.md, memory files, skills, etc.) is separate and configured via `agents.defaults.workspace` (default: `~/.openclaw/workspace`).

### Where should AGENTSmd SOULmd USERmd MEMORYmd live

These files live in the **agent workspace**, not `~/.openclaw`.

*   **Workspace (per agent)**: `AGENTS.md`, `SOUL.md`, `IDENTITY.md`, `USER.md`, `MEMORY.md` (or `memory.md`), `memory/YYYY-MM-DD.md`, optional `HEARTBEAT.md`.
*   **State dir (`~/.openclaw`)**: config, credentials, auth profiles, sessions, logs, and shared skills (`~/.openclaw/skills`).

Default workspace is `~/.openclaw/workspace`, configurable via:

```
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
}
```

If the bot “forgets” after a restart, confirm the Gateway is using the same workspace on every launch (and remember: remote mode uses the **gateway host’s** workspace, not your local laptop). Tip: if you want a durable behavior or preference, ask the bot to **write it into AGENTS.md or MEMORY.md** rather than relying on chat history. See [Agent workspace](https://docs.openclaw.ai/concepts/agent-workspace) and [Memory](https://docs.openclaw.ai/concepts/memory).

### What’s the recommended backup strategy

Put your **agent workspace** in a **private** git repo and back it up somewhere private (for example GitHub private). This captures memory + AGENTS/SOUL/USER files, and lets you restore the assistant’s “mind” later. Do **not** commit anything under `~/.openclaw` (credentials, sessions, tokens, or encrypted secrets payloads). If you need a full restore, back up both the workspace and the state directory separately (see the migration question above). Docs: [Agent workspace](https://docs.openclaw.ai/concepts/agent-workspace).

### How do I completely uninstall OpenClaw

See the dedicated guide: [Uninstall](https://docs.openclaw.ai/install/uninstall).

### Can agents work outside the workspace

Yes. The workspace is the **default cwd** and memory anchor, not a hard sandbox. Relative paths resolve inside the workspace, but absolute paths can access other host locations unless sandboxing is enabled. If you need isolation, use [`agents.defaults.sandbox`](https://docs.openclaw.ai/gateway/sandboxing) or per-agent sandbox settings. If you want a repo to be the default working directory, point that agent’s `workspace` to the repo root. The OpenClaw repo is just source code; keep the workspace separate unless you intentionally want the agent to work inside it. Example (repo as default cwd):

```
{
  agents: {
    defaults: {
      workspace: "~/Projects/my-repo",
    },
  },
}
```

### Im in remote mode where is the session store

Session state is owned by the **gateway host**. If you’re in remote mode, the session store you care about is on the remote machine, not your local laptop. See [Session management](https://docs.openclaw.ai/concepts/session).

## Config basics

### What format is the config Where is it

OpenClaw reads an optional **JSON5** config from `$OPENCLAW_CONFIG_PATH` (default: `~/.openclaw/openclaw.json`):

If the file is missing, it uses safe-ish defaults (including a default workspace of `~/.openclaw/workspace`).

Non-loopback binds **require auth**. Configure `gateway.auth.mode` + `gateway.auth.token` (or use `OPENCLAW_GATEWAY_TOKEN`).

```
{
  gateway: {
    bind: "lan",
    auth: {
      mode: "token",
      token: "replace-me",
    },
  },
}
```

Notes:

*   `gateway.remote.token` / `.password` do **not** enable local gateway auth by themselves.
*   Local call paths can use `gateway.remote.*` as fallback when `gateway.auth.*` is unset.
*   The Control UI authenticates via `connect.params.auth.token` (stored in app/UI settings). Avoid putting tokens in URLs.

### Why do I need a token on localhost now

OpenClaw enforces token auth by default, including loopback. If no token is configured, gateway startup auto-generates one and saves it to `gateway.auth.token`, so **local WS clients must authenticate**. This blocks other local processes from calling the Gateway. If you **really** want open loopback, set `gateway.auth.mode: "none"` explicitly in your config. Doctor can generate a token for you any time: `openclaw doctor --generate-gateway-token`.

### Do I have to restart after changing config

The Gateway watches the config and supports hot-reload:

*   `gateway.reload.mode: "hybrid"` (default): hot-apply safe changes, restart for critical ones
*   `hot`, `restart`, `off` are also supported

### How do I disable funny CLI taglines

Set `cli.banner.taglineMode` in config:

```
{
  cli: {
    banner: {
      taglineMode: "off", // random | default | off
    },
  },
}
```

*   `off`: hides tagline text but keeps the banner title/version line.
*   `default`: uses `All your chats, one OpenClaw.` every time.
*   `random`: rotating funny/seasonal taglines (default behavior).
*   If you want no banner at all, set env `OPENCLAW_HIDE_BANNER=1`.

### How do I enable web search and web fetch

`web_fetch` works without an API key. `web_search` requires a Brave Search API key. **Recommended:** run `openclaw configure --section web` to store it in `tools.web.search.apiKey`. Environment alternative: set `BRAVE_API_KEY` for the Gateway process.

```
{
  tools: {
    web: {
      search: {
        enabled: true,
        apiKey: "BRAVE_API_KEY_HERE",
        maxResults: 5,
      },
      fetch: {
        enabled: true,
      },
    },
  },
}
```

Notes:

*   If you use allowlists, add `web_search`/`web_fetch` or `group:web`.
*   `web_fetch` is enabled by default (unless explicitly disabled).
*   Daemons read env vars from `~/.openclaw/.env` (or the service environment).

Docs: [Web tools](https://docs.openclaw.ai/tools/web).

### How do I run a central Gateway with specialized workers across devices

The common pattern is **one Gateway** (e.g. Raspberry Pi) plus **nodes** and **agents**:

*   **Gateway (central):** owns channels (Signal/WhatsApp), routing, and sessions.
*   **Nodes (devices):** Macs/iOS/Android connect as peripherals and expose local tools (`system.run`, `canvas`, `camera`).
*   **Agents (workers):** separate brains/workspaces for special roles (e.g. “Hetzner ops”, “Personal data”).
*   **Sub-agents:** spawn background work from a main agent when you want parallelism.
*   **TUI:** connect to the Gateway and switch agents/sessions.

Docs: [Nodes](https://docs.openclaw.ai/nodes), [Remote access](https://docs.openclaw.ai/gateway/remote), [Multi-Agent Routing](https://docs.openclaw.ai/concepts/multi-agent), [Sub-agents](https://docs.openclaw.ai/tools/subagents), [TUI](https://docs.openclaw.ai/web/tui).

### Can the OpenClaw browser run headless

Yes. It’s a config option:

```
{
  browser: { headless: true },
  agents: {
    defaults: {
      sandbox: { browser: { headless: true } },
    },
  },
}
```

Default is `false` (headful). Headless is more likely to trigger anti-bot checks on some sites. See [Browser](https://docs.openclaw.ai/tools/browser). Headless uses the **same Chromium engine** and works for most automation (forms, clicks, scraping, logins). The main differences:

*   No visible browser window (use screenshots if you need visuals).
*   Some sites are stricter about automation in headless mode (CAPTCHAs, anti-bot). For example, X/Twitter often blocks headless sessions.

### How do I use Brave for browser control

Set `browser.executablePath` to your Brave binary (or any Chromium-based browser) and restart the Gateway. See the full config examples in [Browser](https://docs.openclaw.ai/tools/browser#use-brave-or-another-chromium-based-browser).

## Remote gateways and nodes

### How do commands propagate between Telegram the gateway and nodes

Telegram messages are handled by the **gateway**. The gateway runs the agent and only then calls nodes over the **Gateway WebSocket** when a node tool is needed: Telegram → Gateway → Agent → `node.*` → Node → Gateway → Telegram Nodes don’t see inbound provider traffic; they only receive node RPC calls.

### How can my agent access my computer if the Gateway is hosted remotely

Short answer: **pair your computer as a node**. The Gateway runs elsewhere, but it can call `node.*` tools (screen, camera, system) on your local machine over the Gateway WebSocket. Typical setup:

1.  Run the Gateway on the always-on host (VPS/home server).
2.  Put the Gateway host + your computer on the same tailnet.
3.  Ensure the Gateway WS is reachable (tailnet bind or SSH tunnel).
4.  Open the macOS app locally and connect in **Remote over SSH** mode (or direct tailnet) so it can register as a node.
5.  Approve the node on the Gateway:
    
    ```
    openclaw devices list
    openclaw devices approve <requestId>
    ```
    

No separate TCP bridge is required; nodes connect over the Gateway WebSocket. Security reminder: pairing a macOS node allows `system.run` on that machine. Only pair devices you trust, and review [Security](https://docs.openclaw.ai/gateway/security). Docs: [Nodes](https://docs.openclaw.ai/nodes), [Gateway protocol](https://docs.openclaw.ai/gateway/protocol), [macOS remote mode](https://docs.openclaw.ai/platforms/mac/remote), [Security](https://docs.openclaw.ai/gateway/security).

Check the basics:

*   Gateway is running: `openclaw gateway status`
*   Gateway health: `openclaw status`
*   Channel health: `openclaw channels status`

Then verify auth and routing:

*   If you use Tailscale Serve, make sure `gateway.auth.allowTailscale` is set correctly.
*   If you connect via SSH tunnel, confirm the local tunnel is up and points at the right port.
*   Confirm your allowlists (DM or group) include your account.

Docs: [Tailscale](https://docs.openclaw.ai/gateway/tailscale), [Remote access](https://docs.openclaw.ai/gateway/remote), [Channels](https://docs.openclaw.ai/channels).

### Can two OpenClaw instances talk to each other local VPS

Yes. There is no built-in “bot-to-bot” bridge, but you can wire it up in a few reliable ways: **Simplest:** use a normal chat channel both bots can access (Telegram/Slack/WhatsApp). Have Bot A send a message to Bot B, then let Bot B reply as usual. **CLI bridge (generic):** run a script that calls the other Gateway with `openclaw agent --message ... --deliver`, targeting a chat where the other bot listens. If one bot is on a remote VPS, point your CLI at that remote Gateway via SSH/Tailscale (see [Remote access](https://docs.openclaw.ai/gateway/remote)). Example pattern (run from a machine that can reach the target Gateway):

```
openclaw agent --message "Hello from local bot" --deliver --channel telegram --reply-to <chat-id>
```

Tip: add a guardrail so the two bots do not loop endlessly (mention-only, channel allowlists, or a “do not reply to bot messages” rule). Docs: [Remote access](https://docs.openclaw.ai/gateway/remote), [Agent CLI](https://docs.openclaw.ai/cli/agent), [Agent send](https://docs.openclaw.ai/tools/agent-send).

### Do I need separate VPSes for multiple agents

No. One Gateway can host multiple agents, each with its own workspace, model defaults, and routing. That is the normal setup and it is much cheaper and simpler than running one VPS per agent. Use separate VPSes only when you need hard isolation (security boundaries) or very different configs that you do not want to share. Otherwise, keep one Gateway and use multiple agents or sub-agents.

### Is there a benefit to using a node on my personal laptop instead of SSH from a VPS

Yes - nodes are the first-class way to reach your laptop from a remote Gateway, and they unlock more than shell access. The Gateway runs on macOS/Linux (Windows via WSL2) and is lightweight (a small VPS or Raspberry Pi-class box is fine; 4 GB RAM is plenty), so a common setup is an always-on host plus your laptop as a node.

*   **No inbound SSH required.** Nodes connect out to the Gateway WebSocket and use device pairing.
*   **Safer execution controls.** `system.run` is gated by node allowlists/approvals on that laptop.
*   **More device tools.** Nodes expose `canvas`, `camera`, and `screen` in addition to `system.run`.
*   **Local browser automation.** Keep the Gateway on a VPS, but run Chrome locally and relay control with the Chrome extension + a node host on the laptop.

SSH is fine for ad-hoc shell access, but nodes are simpler for ongoing agent workflows and device automation. Docs: [Nodes](https://docs.openclaw.ai/nodes), [Nodes CLI](https://docs.openclaw.ai/cli/nodes), [Chrome extension](https://docs.openclaw.ai/tools/chrome-extension).

### Should I install on a second laptop or just add a node

If you only need **local tools** (screen/camera/exec) on the second laptop, add it as a **node**. That keeps a single Gateway and avoids duplicated config. Local node tools are currently macOS-only, but we plan to extend them to other OSes. Install a second Gateway only when you need **hard isolation** or two fully separate bots. Docs: [Nodes](https://docs.openclaw.ai/nodes), [Nodes CLI](https://docs.openclaw.ai/cli/nodes), [Multiple gateways](https://docs.openclaw.ai/gateway/multiple-gateways).

### Do nodes run a gateway service

No. Only **one gateway** should run per host unless you intentionally run isolated profiles (see [Multiple gateways](https://docs.openclaw.ai/gateway/multiple-gateways)). Nodes are peripherals that connect to the gateway (iOS/Android nodes, or macOS “node mode” in the menubar app). For headless node hosts and CLI control, see [Node host CLI](https://docs.openclaw.ai/cli/node). A full restart is required for `gateway`, `discovery`, and `canvasHost` changes.

### Is there an API RPC way to apply config

Yes. `config.apply` validates + writes the full config and restarts the Gateway as part of the operation.

### configapply wiped my config How do I recover and avoid this

`config.apply` replaces the **entire config**. If you send a partial object, everything else is removed. Recover:

*   Restore from backup (git or a copied `~/.openclaw/openclaw.json`).
*   If you have no backup, re-run `openclaw doctor` and reconfigure channels/models.
*   If this was unexpected, file a bug and include your last known config or any backup.
*   A local coding agent can often reconstruct a working config from logs or history.

Avoid it:

*   Use `openclaw config set` for small changes.
*   Use `openclaw configure` for interactive edits.

Docs: [Config](https://docs.openclaw.ai/cli/config), [Configure](https://docs.openclaw.ai/cli/configure), [Doctor](https://docs.openclaw.ai/gateway/doctor).

### What’s a minimal sane config for a first install

```
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
  channels: { whatsapp: { allowFrom: ["+15555550123"] } },
}
```

This sets your workspace and restricts who can trigger the bot.

### How do I set up Tailscale on a VPS and connect from my Mac

Minimal steps:

1.  **Install + login on the VPS**
    
    ```
    curl -fsSL https://tailscale.com/install.sh | sh
    sudo tailscale up
    ```
    
2.  **Install + login on your Mac**
    *   Use the Tailscale app and sign in to the same tailnet.
3.  **Enable MagicDNS (recommended)**
    *   In the Tailscale admin console, enable MagicDNS so the VPS has a stable name.
4.  **Use the tailnet hostname**
    *   SSH: `ssh user@your-vps.tailnet-xxxx.ts.net`
    *   Gateway WS: `ws://your-vps.tailnet-xxxx.ts.net:18789`

If you want the Control UI without SSH, use Tailscale Serve on the VPS:

```
openclaw gateway --tailscale serve
```

This keeps the gateway bound to loopback and exposes HTTPS via Tailscale. See [Tailscale](https://docs.openclaw.ai/gateway/tailscale).

### How do I connect a Mac node to a remote Gateway Tailscale Serve

Serve exposes the **Gateway Control UI + WS**. Nodes connect over the same Gateway WS endpoint. Recommended setup:

1.  **Make sure the VPS + Mac are on the same tailnet**.
2.  **Use the macOS app in Remote mode** (SSH target can be the tailnet hostname). The app will tunnel the Gateway port and connect as a node.
3.  **Approve the node** on the gateway:
    
    ```
    openclaw devices list
    openclaw devices approve <requestId>
    ```
    

Docs: [Gateway protocol](https://docs.openclaw.ai/gateway/protocol), [Discovery](https://docs.openclaw.ai/gateway/discovery), [macOS remote mode](https://docs.openclaw.ai/platforms/mac/remote).

## Env vars and .env loading

### How does OpenClaw load environment variables

OpenClaw reads env vars from the parent process (shell, launchd/systemd, CI, etc.) and additionally loads:

*   `.env` from the current working directory
*   a global fallback `.env` from `~/.openclaw/.env` (aka `$OPENCLAW_STATE_DIR/.env`)

Neither `.env` file overrides existing env vars. You can also define inline env vars in config (applied only if missing from the process env):

```
{
  env: {
    OPENROUTER_API_KEY: "sk-or-...",
    vars: { GROQ_API_KEY: "gsk-..." },
  },
}
```

See [/environment](https://docs.openclaw.ai/help/environment) for full precedence and sources.

### I started the Gateway via the service and my env vars disappeared What now

Two common fixes:

1.  Put the missing keys in `~/.openclaw/.env` so they’re picked up even when the service doesn’t inherit your shell env.
2.  Enable shell import (opt-in convenience):

```
{
  env: {
    shellEnv: {
      enabled: true,
      timeoutMs: 15000,
    },
  },
}
```

This runs your login shell and imports only missing expected keys (never overrides). Env var equivalents: `OPENCLAW_LOAD_SHELL_ENV=1`, `OPENCLAW_SHELL_ENV_TIMEOUT_MS=15000`.

### I set COPILOTGITHUBTOKEN but models status shows Shell env off Why

`openclaw models status` reports whether **shell env import** is enabled. “Shell env: off” does **not** mean your env vars are missing - it just means OpenClaw won’t load your login shell automatically. If the Gateway runs as a service (launchd/systemd), it won’t inherit your shell environment. Fix by doing one of these:

1.  Put the token in `~/.openclaw/.env`:
2.  Or enable shell import (`env.shellEnv.enabled: true`).
3.  Or add it to your config `env` block (applies only if missing).

Then restart the gateway and recheck:

Copilot tokens are read from `COPILOT_GITHUB_TOKEN` (also `GH_TOKEN` / `GITHUB_TOKEN`). See [/concepts/model-providers](https://docs.openclaw.ai/concepts/model-providers) and [/environment](https://docs.openclaw.ai/help/environment).

## Sessions and multiple chats

### How do I start a fresh conversation

Send `/new` or `/reset` as a standalone message. See [Session management](https://docs.openclaw.ai/concepts/session).

### Do sessions reset automatically if I never send new

Yes. Sessions expire after `session.idleMinutes` (default **60**). The **next** message starts a fresh session id for that chat key. This does not delete transcripts - it just starts a new session.

```
{
  session: {
    idleMinutes: 240,
  },
}
```

### Is there a way to make a team of OpenClaw instances one CEO and many agents

Yes, via **multi-agent routing** and **sub-agents**. You can create one coordinator agent and several worker agents with their own workspaces and models. That said, this is best seen as a **fun experiment**. It is token heavy and often less efficient than using one bot with separate sessions. The typical model we envision is one bot you talk to, with different sessions for parallel work. That bot can also spawn sub-agents when needed. Docs: [Multi-agent routing](https://docs.openclaw.ai/concepts/multi-agent), [Sub-agents](https://docs.openclaw.ai/tools/subagents), [Agents CLI](https://docs.openclaw.ai/cli/agents).

### Why did context get truncated midtask How do I prevent it

Session context is limited by the model window. Long chats, large tool outputs, or many files can trigger compaction or truncation. What helps:

*   Ask the bot to summarize the current state and write it to a file.
*   Use `/compact` before long tasks, and `/new` when switching topics.
*   Keep important context in the workspace and ask the bot to read it back.
*   Use sub-agents for long or parallel work so the main chat stays smaller.
*   Pick a model with a larger context window if this happens often.

### How do I completely reset OpenClaw but keep it installed

Use the reset command:

Non-interactive full reset:

```
openclaw reset --scope full --yes --non-interactive
```

Then re-run onboarding:

```
openclaw onboard --install-daemon
```

Notes:

*   The onboarding wizard also offers **Reset** if it sees an existing config. See [Wizard](https://docs.openclaw.ai/start/wizard).
*   If you used profiles (`--profile` / `OPENCLAW_PROFILE`), reset each state dir (defaults are `~/.openclaw-<profile>`).
*   Dev reset: `openclaw gateway --dev --reset` (dev-only; wipes dev config + credentials + sessions + workspace).

### Im getting context too large errors how do I reset or compact

Use one of these:

*   **Compact** (keeps the conversation but summarizes older turns): or `/compact <instructions>` to guide the summary.
*   **Reset** (fresh session ID for the same chat key):

If it keeps happening:

*   Enable or tune **session pruning** (`agents.defaults.contextPruning`) to trim old tool output.
*   Use a model with a larger context window.

Docs: [Compaction](https://docs.openclaw.ai/concepts/compaction), [Session pruning](https://docs.openclaw.ai/concepts/session-pruning), [Session management](https://docs.openclaw.ai/concepts/session).

### Why am I seeing “LLM request rejected: messages.content.tool\_use.input field required”?

This is a provider validation error: the model emitted a `tool_use` block without the required `input`. It usually means the session history is stale or corrupted (often after long threads or a tool/schema change). Fix: start a fresh session with `/new` (standalone message).

### Why am I getting heartbeat messages every 30 minutes

Heartbeats run every **30m** by default. Tune or disable them:

```
{
  agents: {
    defaults: {
      heartbeat: {
        every: "2h", // or "0m" to disable
      },
    },
  },
}
```

If `HEARTBEAT.md` exists but is effectively empty (only blank lines and markdown headers like `# Heading`), OpenClaw skips the heartbeat run to save API calls. If the file is missing, the heartbeat still runs and the model decides what to do. Per-agent overrides use `agents.list[].heartbeat`. Docs: [Heartbeat](https://docs.openclaw.ai/gateway/heartbeat).

### Do I need to add a bot account to a WhatsApp group

No. OpenClaw runs on **your own account**, so if you’re in the group, OpenClaw can see it. By default, group replies are blocked until you allow senders (`groupPolicy: "allowlist"`). If you want only **you** to be able to trigger group replies:

```
{
  channels: {
    whatsapp: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15551234567"],
    },
  },
}
```

### How do I get the JID of a WhatsApp group

Option 1 (fastest): tail logs and send a test message in the group:

```
openclaw logs --follow --json
```

Look for `chatId` (or `from`) ending in `@g.us`, like: `1234567890-1234567890@g.us`. Option 2 (if already configured/allowlisted): list groups from config:

```
openclaw directory groups list --channel whatsapp
```

Docs: [WhatsApp](https://docs.openclaw.ai/channels/whatsapp), [Directory](https://docs.openclaw.ai/cli/directory), [Logs](https://docs.openclaw.ai/cli/logs).

### Why doesn’t OpenClaw reply in a group

Two common causes:

*   Mention gating is on (default). You must @mention the bot (or match `mentionPatterns`).
*   You configured `channels.whatsapp.groups` without `"*"` and the group isn’t allowlisted.

See [Groups](https://docs.openclaw.ai/channels/groups) and [Group messages](https://docs.openclaw.ai/channels/group-messages).

Direct chats collapse to the main session by default. Groups/channels have their own session keys, and Telegram topics / Discord threads are separate sessions. See [Groups](https://docs.openclaw.ai/channels/groups) and [Group messages](https://docs.openclaw.ai/channels/group-messages).

### How many workspaces and agents can I create

No hard limits. Dozens (even hundreds) are fine, but watch for:

*   **Disk growth:** sessions + transcripts live under `~/.openclaw/agents/<agentId>/sessions/`.
*   **Token cost:** more agents means more concurrent model usage.
*   **Ops overhead:** per-agent auth profiles, workspaces, and channel routing.

Tips:

*   Keep one **active** workspace per agent (`agents.defaults.workspace`).
*   Prune old sessions (delete JSONL or store entries) if disk grows.
*   Use `openclaw doctor` to spot stray workspaces and profile mismatches.

### Can I run multiple bots or chats at the same time Slack and how should I set that up

Yes. Use **Multi-Agent Routing** to run multiple isolated agents and route inbound messages by channel/account/peer. Slack is supported as a channel and can be bound to specific agents. Browser access is powerful but not “do anything a human can” - anti-bot, CAPTCHAs, and MFA can still block automation. For the most reliable browser control, use the Chrome extension relay on the machine that runs the browser (and keep the Gateway anywhere). Best-practice setup:

*   Always-on Gateway host (VPS/Mac mini).
*   One agent per role (bindings).
*   Slack channel(s) bound to those agents.
*   Local browser via extension relay (or a node) when needed.

Docs: [Multi-Agent Routing](https://docs.openclaw.ai/concepts/multi-agent), [Slack](https://docs.openclaw.ai/channels/slack), [Browser](https://docs.openclaw.ai/tools/browser), [Chrome extension](https://docs.openclaw.ai/tools/chrome-extension), [Nodes](https://docs.openclaw.ai/nodes).

## Models: defaults, selection, aliases, switching

### What is the default model

OpenClaw’s default model is whatever you set as:

```
agents.defaults.model.primary
```

Models are referenced as `provider/model` (example: `anthropic/claude-opus-4-6`). If you omit the provider, OpenClaw currently assumes `anthropic` as a temporary deprecation fallback - but you should still **explicitly** set `provider/model`.

### What model do you recommend

**Recommended default:** use the strongest latest-generation model available in your provider stack. **For tool-enabled or untrusted-input agents:** prioritize model strength over cost. **For routine/low-stakes chat:** use cheaper fallback models and route by agent role. MiniMax M2.5 has its own docs: [MiniMax](https://docs.openclaw.ai/providers/minimax) and [Local models](https://docs.openclaw.ai/gateway/local-models). Rule of thumb: use the **best model you can afford** for high-stakes work, and a cheaper model for routine chat or summaries. You can route models per agent and use sub-agents to parallelize long tasks (each sub-agent consumes tokens). See [Models](https://docs.openclaw.ai/concepts/models) and [Sub-agents](https://docs.openclaw.ai/tools/subagents). Strong warning: weaker/over-quantized models are more vulnerable to prompt injection and unsafe behavior. See [Security](https://docs.openclaw.ai/gateway/security). More context: [Models](https://docs.openclaw.ai/concepts/models).

### Can I use selfhosted models llamacpp vLLM Ollama

Yes. If your local server exposes an OpenAI-compatible API, you can point a custom provider at it. Ollama is supported directly and is the easiest path. Security note: smaller or heavily quantized models are more vulnerable to prompt injection. We strongly recommend **large models** for any bot that can use tools. If you still want small models, enable sandboxing and strict tool allowlists. Docs: [Ollama](https://docs.openclaw.ai/providers/ollama), [Local models](https://docs.openclaw.ai/gateway/local-models), [Model providers](https://docs.openclaw.ai/concepts/model-providers), [Security](https://docs.openclaw.ai/gateway/security), [Sandboxing](https://docs.openclaw.ai/gateway/sandboxing).

### How do I switch models without wiping my config

Use **model commands** or edit only the **model** fields. Avoid full config replaces. Safe options:

*   `/model` in chat (quick, per-session)
*   `openclaw models set ...` (updates just model config)
*   `openclaw configure --section model` (interactive)
*   edit `agents.defaults.model` in `~/.openclaw/openclaw.json`

Avoid `config.apply` with a partial object unless you intend to replace the whole config. If you did overwrite config, restore from backup or re-run `openclaw doctor` to repair. Docs: [Models](https://docs.openclaw.ai/concepts/models), [Configure](https://docs.openclaw.ai/cli/configure), [Config](https://docs.openclaw.ai/cli/config), [Doctor](https://docs.openclaw.ai/gateway/doctor).

### What do OpenClaw, Flawd, and Krill use for models

*   These deployments can differ and may change over time; there is no fixed provider recommendation.
*   Check the current runtime setting on each gateway with `openclaw models status`.
*   For security-sensitive/tool-enabled agents, use the strongest latest-generation model available.

### How do I switch models on the fly without restarting

Use the `/model` command as a standalone message:

```
/model sonnet
/model haiku
/model opus
/model gpt
/model gpt-mini
/model gemini
/model gemini-flash
```

You can list available models with `/model`, `/model list`, or `/model status`. `/model` (and `/model list`) shows a compact, numbered picker. Select by number:

You can also force a specific auth profile for the provider (per session):

```
/model opus@anthropic:default
/model opus@anthropic:work
```

Tip: `/model status` shows which agent is active, which `auth-profiles.json` file is being used, and which auth profile will be tried next. It also shows the configured provider endpoint (`baseUrl`) and API mode (`api`) when available. **How do I unpin a profile I set with profile** Re-run `/model` **without** the `@profile` suffix:

```
/model anthropic/claude-opus-4-6
```

If you want to return to the default, pick it from `/model` (or send `/model <default provider/model>`). Use `/model status` to confirm which auth profile is active.

### Can I use GPT 5.2 for daily tasks and Codex 5.3 for coding

Yes. Set one as default and switch as needed:

*   **Quick switch (per session):** `/model gpt-5.2` for daily tasks, `/model openai-codex/gpt-5.4` for coding with Codex OAuth.
*   **Default + switch:** set `agents.defaults.model.primary` to `openai/gpt-5.2`, then switch to `openai-codex/gpt-5.4` when coding (or the other way around).
*   **Sub-agents:** route coding tasks to sub-agents with a different default model.

See [Models](https://docs.openclaw.ai/concepts/models) and [Slash commands](https://docs.openclaw.ai/tools/slash-commands).

### Why do I see Model is not allowed and then no reply

If `agents.defaults.models` is set, it becomes the **allowlist** for `/model` and any session overrides. Choosing a model that isn’t in that list returns:

```
Model "provider/model" is not allowed. Use /model to list available models.
```

That error is returned **instead of** a normal reply. Fix: add the model to `agents.defaults.models`, remove the allowlist, or pick a model from `/model list`.

### Why do I see Unknown model minimaxMiniMaxM25

This means the **provider isn’t configured** (no MiniMax provider config or auth profile was found), so the model can’t be resolved. A fix for this detection is in **2026.1.12** (unreleased at the time of writing). Fix checklist:

1.  Upgrade to **2026.1.12** (or run from source `main`), then restart the gateway.
2.  Make sure MiniMax is configured (wizard or JSON), or that a MiniMax API key exists in env/auth profiles so the provider can be injected.
3.  Use the exact model id (case-sensitive): `minimax/MiniMax-M2.5` or `minimax/MiniMax-M2.5-highspeed`.
4.  Run: and pick from the list (or `/model list` in chat).

See [MiniMax](https://docs.openclaw.ai/providers/minimax) and [Models](https://docs.openclaw.ai/concepts/models).

### Can I use MiniMax as my default and OpenAI for complex tasks

Yes. Use **MiniMax as the default** and switch models **per session** when needed. Fallbacks are for **errors**, not “hard tasks,” so use `/model` or a separate agent. **Option A: switch per session**

```
{
  env: { MINIMAX_API_KEY: "sk-...", OPENAI_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "minimax/MiniMax-M2.5" },
      models: {
        "minimax/MiniMax-M2.5": { alias: "minimax" },
        "openai/gpt-5.2": { alias: "gpt" },
      },
    },
  },
}
```

Then:

**Option B: separate agents**

*   Agent A default: MiniMax
*   Agent B default: OpenAI
*   Route by agent or use `/agent` to switch

Docs: [Models](https://docs.openclaw.ai/concepts/models), [Multi-Agent Routing](https://docs.openclaw.ai/concepts/multi-agent), [MiniMax](https://docs.openclaw.ai/providers/minimax), [OpenAI](https://docs.openclaw.ai/providers/openai).

### Are opus sonnet gpt builtin shortcuts

Yes. OpenClaw ships a few default shorthands (only applied when the model exists in `agents.defaults.models`):

*   `opus` → `anthropic/claude-opus-4-6`
*   `sonnet` → `anthropic/claude-sonnet-4-6`
*   `gpt` → `openai/gpt-5.4`
*   `gpt-mini` → `openai/gpt-5-mini`
*   `gemini` → `google/gemini-3.1-pro-preview`
*   `gemini-flash` → `google/gemini-3-flash-preview`
*   `gemini-flash-lite` → `google/gemini-3.1-flash-lite-preview`

If you set your own alias with the same name, your value wins.

### How do I defineoverride model shortcuts aliases

Aliases come from `agents.defaults.models.<modelId>.alias`. Example:

```
{
  agents: {
    defaults: {
      model: { primary: "anthropic/claude-opus-4-6" },
      models: {
        "anthropic/claude-opus-4-6": { alias: "opus" },
        "anthropic/claude-sonnet-4-5": { alias: "sonnet" },
        "anthropic/claude-haiku-4-5": { alias: "haiku" },
      },
    },
  },
}
```

Then `/model sonnet` (or `/<alias>` when supported) resolves to that model ID.

### How do I add models from other providers like OpenRouter or ZAI

OpenRouter (pay-per-token; many models):

```
{
  agents: {
    defaults: {
      model: { primary: "openrouter/anthropic/claude-sonnet-4-5" },
      models: { "openrouter/anthropic/claude-sonnet-4-5": {} },
    },
  },
  env: { OPENROUTER_API_KEY: "sk-or-..." },
}
```

Z.AI (GLM models):

```
{
  agents: {
    defaults: {
      model: { primary: "zai/glm-5" },
      models: { "zai/glm-5": {} },
    },
  },
  env: { ZAI_API_KEY: "..." },
}
```

If you reference a provider/model but the required provider key is missing, you’ll get a runtime auth error (e.g. `No API key found for provider "zai"`). **No API key found for provider after adding a new agent** This usually means the **new agent** has an empty auth store. Auth is per-agent and stored in:

```
~/.openclaw/agents/<agentId>/agent/auth-profiles.json
```

Fix options:

*   Run `openclaw agents add <id>` and configure auth during the wizard.
*   Or copy `auth-profiles.json` from the main agent’s `agentDir` into the new agent’s `agentDir`.

Do **not** reuse `agentDir` across agents; it causes auth/session collisions.

## Model failover and “All models failed”

### How does failover work

Failover happens in two stages:

1.  **Auth profile rotation** within the same provider.
2.  **Model fallback** to the next model in `agents.defaults.model.fallbacks`.

Cooldowns apply to failing profiles (exponential backoff), so OpenClaw can keep responding even when a provider is rate-limited or temporarily failing.

### What does this error mean

```
No credentials found for profile "anthropic:default"
```

It means the system attempted to use the auth profile ID `anthropic:default`, but could not find credentials for it in the expected auth store.

### Fix checklist for No credentials found for profile anthropicdefault

*   **Confirm where auth profiles live** (new vs legacy paths)
    *   Current: `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
    *   Legacy: `~/.openclaw/agent/*` (migrated by `openclaw doctor`)
*   **Confirm your env var is loaded by the Gateway**
    *   If you set `ANTHROPIC_API_KEY` in your shell but run the Gateway via systemd/launchd, it may not inherit it. Put it in `~/.openclaw/.env` or enable `env.shellEnv`.
*   **Make sure you’re editing the correct agent**
    *   Multi-agent setups mean there can be multiple `auth-profiles.json` files.
*   **Sanity-check model/auth status**
    *   Use `openclaw models status` to see configured models and whether providers are authenticated.

**Fix checklist for No credentials found for profile anthropic** This means the run is pinned to an Anthropic auth profile, but the Gateway can’t find it in its auth store.

*   **Use a setup-token**
    *   Run `claude setup-token`, then paste it with `openclaw models auth setup-token --provider anthropic`.
    *   If the token was created on another machine, use `openclaw models auth paste-token --provider anthropic`.
*   **If you want to use an API key instead**
    *   Put `ANTHROPIC_API_KEY` in `~/.openclaw/.env` on the **gateway host**.
    *   Clear any pinned order that forces a missing profile:
        
        ```
        openclaw models auth order clear --provider anthropic
        ```
        
*   **Confirm you’re running commands on the gateway host**
    *   In remote mode, auth profiles live on the gateway machine, not your laptop.

### Why did it also try Google Gemini and fail

If your model config includes Google Gemini as a fallback (or you switched to a Gemini shorthand), OpenClaw will try it during model fallback. If you haven’t configured Google credentials, you’ll see `No API key found for provider "google"`. Fix: either provide Google auth, or remove/avoid Google models in `agents.defaults.model.fallbacks` / aliases so fallback doesn’t route there. **LLM request rejected message thinking signature required google antigravity** Cause: the session history contains **thinking blocks without signatures** (often from an aborted/partial stream). Google Antigravity requires signatures for thinking blocks. Fix: OpenClaw now strips unsigned thinking blocks for Google Antigravity Claude. If it still appears, start a **new session** or set `/thinking off` for that agent.

## Auth profiles: what they are and how to manage them

Related: [/concepts/oauth](https://docs.openclaw.ai/concepts/oauth) (OAuth flows, token storage, multi-account patterns)

### What is an auth profile

An auth profile is a named credential record (OAuth or API key) tied to a provider. Profiles live in:

```
~/.openclaw/agents/<agentId>/agent/auth-profiles.json
```

### What are typical profile IDs

OpenClaw uses provider-prefixed IDs like:

*   `anthropic:default` (common when no email identity exists)
*   `anthropic:<email>` for OAuth identities
*   custom IDs you choose (e.g. `anthropic:work`)

### Can I control which auth profile is tried first

Yes. Config supports optional metadata for profiles and an ordering per provider (`auth.order.<provider>`). This does **not** store secrets; it maps IDs to provider/mode and sets rotation order. OpenClaw may temporarily skip a profile if it’s in a short **cooldown** (rate limits/timeouts/auth failures) or a longer **disabled** state (billing/insufficient credits). To inspect this, run `openclaw models status --json` and check `auth.unusableProfiles`. Tuning: `auth.cooldowns.billingBackoffHours*`. You can also set a **per-agent** order override (stored in that agent’s `auth-profiles.json`) via the CLI:

```
# Defaults to the configured default agent (omit --agent)
openclaw models auth order get --provider anthropic

# Lock rotation to a single profile (only try this one)
openclaw models auth order set --provider anthropic anthropic:default

# Or set an explicit order (fallback within provider)
openclaw models auth order set --provider anthropic anthropic:work anthropic:default

# Clear override (fall back to config auth.order / round-robin)
openclaw models auth order clear --provider anthropic
```

To target a specific agent:

```
openclaw models auth order set --provider anthropic --agent main anthropic:default
```

### OAuth vs API key what’s the difference

OpenClaw supports both:

*   **OAuth** often leverages subscription access (where applicable).
*   **API keys** use pay-per-token billing.

The wizard explicitly supports Anthropic setup-token and OpenAI Codex OAuth and can store API keys for you.

## Gateway: ports, “already running”, and remote mode

### What port does the Gateway use

`gateway.port` controls the single multiplexed port for WebSocket + HTTP (Control UI, hooks, etc.). Precedence:

```
--port > OPENCLAW_GATEWAY_PORT > gateway.port > default 18789
```

### Why does openclaw gateway status say Runtime running but RPC probe failed

Because “running” is the **supervisor’s** view (launchd/systemd/schtasks). The RPC probe is the CLI actually connecting to the gateway WebSocket and calling `status`. Use `openclaw gateway status` and trust these lines:

*   `Probe target:` (the URL the probe actually used)
*   `Listening:` (what’s actually bound on the port)
*   `Last gateway error:` (common root cause when the process is alive but the port isn’t listening)

### Why does openclaw gateway status show Config cli and Config service different

You’re editing one config file while the service is running another (often a `--profile` / `OPENCLAW_STATE_DIR` mismatch). Fix:

```
openclaw gateway install --force
```

Run that from the same `--profile` / environment you want the service to use.

### What does another gateway instance is already listening mean

OpenClaw enforces a runtime lock by binding the WebSocket listener immediately on startup (default `ws://127.0.0.1:18789`). If the bind fails with `EADDRINUSE`, it throws `GatewayLockError` indicating another instance is already listening. Fix: stop the other instance, free the port, or run with `openclaw gateway --port <port>`.

### How do I run OpenClaw in remote mode client connects to a Gateway elsewhere

Set `gateway.mode: "remote"` and point to a remote WebSocket URL, optionally with a token/password:

```
{
  gateway: {
    mode: "remote",
    remote: {
      url: "ws://gateway.tailnet:18789",
      token: "your-token",
      password: "your-password",
    },
  },
}
```

Notes:

*   `openclaw gateway` only starts when `gateway.mode` is `local` (or you pass the override flag).
*   The macOS app watches the config file and switches modes live when these values change.

### The Control UI says unauthorized or keeps reconnecting What now

Your gateway is running with auth enabled (`gateway.auth.*`), but the UI is not sending the matching token/password. Facts (from code):

*   The Control UI keeps the token in memory for the current tab; it no longer persists gateway tokens in browser localStorage.

Fix:

*   Fastest: `openclaw dashboard` (prints + copies the dashboard URL, tries to open; shows SSH hint if headless).
*   If you don’t have a token yet: `openclaw doctor --generate-gateway-token`.
*   If remote, tunnel first: `ssh -N -L 18789:127.0.0.1:18789 user@host` then open `http://127.0.0.1:18789/`.
*   Set `gateway.auth.token` (or `OPENCLAW_GATEWAY_TOKEN`) on the gateway host.
*   In the Control UI settings, paste the same token.
*   Still stuck? Run `openclaw status --all` and follow [Troubleshooting](https://docs.openclaw.ai/gateway/troubleshooting). See [Dashboard](https://docs.openclaw.ai/web/dashboard) for auth details.

### I set gatewaybind tailnet but it can’t bind nothing listens

`tailnet` bind picks a Tailscale IP from your network interfaces (100.64.0.0/10). If the machine isn’t on Tailscale (or the interface is down), there’s nothing to bind to. Fix:

*   Start Tailscale on that host (so it has a 100.x address), or
*   Switch to `gateway.bind: "loopback"` / `"lan"`.

Note: `tailnet` is explicit. `auto` prefers loopback; use `gateway.bind: "tailnet"` when you want a tailnet-only bind.

### Can I run multiple Gateways on the same host

Usually no - one Gateway can run multiple messaging channels and agents. Use multiple Gateways only when you need redundancy (ex: rescue bot) or hard isolation. Yes, but you must isolate:

*   `OPENCLAW_CONFIG_PATH` (per-instance config)
*   `OPENCLAW_STATE_DIR` (per-instance state)
*   `agents.defaults.workspace` (workspace isolation)
*   `gateway.port` (unique ports)

Quick setup (recommended):

*   Use `openclaw --profile <name> …` per instance (auto-creates `~/.openclaw-<name>`).
*   Set a unique `gateway.port` in each profile config (or pass `--port` for manual runs).
*   Install a per-profile service: `openclaw --profile <name> gateway install`.

Profiles also suffix service names (`ai.openclaw.<profile>`; legacy `com.openclaw.*`, `openclaw-gateway-<profile>.service`, `OpenClaw Gateway (<profile>)`). Full guide: [Multiple gateways](https://docs.openclaw.ai/gateway/multiple-gateways).

### What does invalid handshake code 1008 mean

The Gateway is a **WebSocket server**, and it expects the very first message to be a `connect` frame. If it receives anything else, it closes the connection with **code 1008** (policy violation). Common causes:

*   You opened the **HTTP** URL in a browser (`http://...`) instead of a WS client.
*   You used the wrong port or path.
*   A proxy or tunnel stripped auth headers or sent a non-Gateway request.

Quick fixes:

1.  Use the WS URL: `ws://<host>:18789` (or `wss://...` if HTTPS).
2.  Don’t open the WS port in a normal browser tab.
3.  If auth is on, include the token/password in the `connect` frame.

If you’re using the CLI or TUI, the URL should look like:

```
openclaw tui --url ws://<host>:18789 --token <token>
```

Protocol details: [Gateway protocol](https://docs.openclaw.ai/gateway/protocol).

## Logging and debugging

### Where are logs

File logs (structured):

```
/tmp/openclaw/openclaw-YYYY-MM-DD.log
```

You can set a stable path via `logging.file`. File log level is controlled by `logging.level`. Console verbosity is controlled by `--verbose` and `logging.consoleLevel`. Fastest log tail:

Service/supervisor logs (when the gateway runs via launchd/systemd):

*   macOS: `$OPENCLAW_STATE_DIR/logs/gateway.log` and `gateway.err.log` (default: `~/.openclaw/logs/...`; profiles use `~/.openclaw-<profile>/logs/...`)
*   Linux: `journalctl --user -u openclaw-gateway[-<profile>].service -n 200 --no-pager`
*   Windows: `schtasks /Query /TN "OpenClaw Gateway (<profile>)" /V /FO LIST`

See [Troubleshooting](https://docs.openclaw.ai/gateway/troubleshooting#log-locations) for more.

### How do I start/stop/restart the Gateway service

Use the gateway helpers:

```
openclaw gateway status
openclaw gateway restart
```

If you run the gateway manually, `openclaw gateway --force` can reclaim the port. See [Gateway](https://docs.openclaw.ai/gateway).

### I closed my terminal on Windows how do I restart OpenClaw

There are **two Windows install modes**: **1) WSL2 (recommended):** the Gateway runs inside Linux. Open PowerShell, enter WSL, then restart:

```
wsl
openclaw gateway status
openclaw gateway restart
```

If you never installed the service, start it in the foreground:

**2) Native Windows (not recommended):** the Gateway runs directly in Windows. Open PowerShell and run:

```
openclaw gateway status
openclaw gateway restart
```

If you run it manually (no service), use:

Docs: [Windows (WSL2)](https://docs.openclaw.ai/platforms/windows), [Gateway service runbook](https://docs.openclaw.ai/gateway).

Start with a quick health sweep:

```
openclaw status
openclaw models status
openclaw channels status
openclaw logs --follow
```

Common causes:

*   Model auth not loaded on the **gateway host** (check `models status`).
*   Channel pairing/allowlist blocking replies (check channel config + logs).
*   WebChat/Dashboard is open without the right token.

If you are remote, confirm the tunnel/Tailscale connection is up and that the Gateway WebSocket is reachable. Docs: [Channels](https://docs.openclaw.ai/channels), [Troubleshooting](https://docs.openclaw.ai/gateway/troubleshooting), [Remote access](https://docs.openclaw.ai/gateway/remote).

### Disconnected from gateway no reason what now

This usually means the UI lost the WebSocket connection. Check:

1.  Is the Gateway running? `openclaw gateway status`
2.  Is the Gateway healthy? `openclaw status`
3.  Does the UI have the right token? `openclaw dashboard`
4.  If remote, is the tunnel/Tailscale link up?

Then tail logs:

Docs: [Dashboard](https://docs.openclaw.ai/web/dashboard), [Remote access](https://docs.openclaw.ai/gateway/remote), [Troubleshooting](https://docs.openclaw.ai/gateway/troubleshooting).

### Telegram setMyCommands fails with network errors What should I check

Start with logs and channel status:

```
openclaw channels status
openclaw channels logs --channel telegram
```

If you are on a VPS or behind a proxy, confirm outbound HTTPS is allowed and DNS works. If the Gateway is remote, make sure you are looking at logs on the Gateway host. Docs: [Telegram](https://docs.openclaw.ai/channels/telegram), [Channel troubleshooting](https://docs.openclaw.ai/channels/troubleshooting).

### TUI shows no output What should I check

First confirm the Gateway is reachable and the agent can run:

```
openclaw status
openclaw models status
openclaw logs --follow
```

In the TUI, use `/status` to see the current state. If you expect replies in a chat channel, make sure delivery is enabled (`/deliver on`). Docs: [TUI](https://docs.openclaw.ai/web/tui), [Slash commands](https://docs.openclaw.ai/tools/slash-commands).

### How do I completely stop then start the Gateway

If you installed the service:

```
openclaw gateway stop
openclaw gateway start
```

This stops/starts the **supervised service** (launchd on macOS, systemd on Linux). Use this when the Gateway runs in the background as a daemon. If you’re running in the foreground, stop with Ctrl-C, then:

Docs: [Gateway service runbook](https://docs.openclaw.ai/gateway).

### ELI5 openclaw gateway restart vs openclaw gateway

*   `openclaw gateway restart`: restarts the **background service** (launchd/systemd).
*   `openclaw gateway`: runs the gateway **in the foreground** for this terminal session.

If you installed the service, use the gateway commands. Use `openclaw gateway` when you want a one-off, foreground run.

### What’s the fastest way to get more details when something fails

Start the Gateway with `--verbose` to get more console detail. Then inspect the log file for channel auth, model routing, and RPC errors.

### My skill generated an imagePDF but nothing was sent

Outbound attachments from the agent must include a `MEDIA:<path-or-url>` line (on its own line). See [OpenClaw assistant setup](https://docs.openclaw.ai/start/openclaw) and [Agent send](https://docs.openclaw.ai/tools/agent-send). CLI sending:

```
openclaw message send --target +15555550123 --message "Here you go" --media /path/to/file.png
```

Also check:

*   The target channel supports outbound media and isn’t blocked by allowlists.
*   The file is within the provider’s size limits (images are resized to max 2048px).

See [Images](https://docs.openclaw.ai/nodes/images).

## Security and access control

### Is it safe to expose OpenClaw to inbound DMs

Treat inbound DMs as untrusted input. Defaults are designed to reduce risk:

*   Default behavior on DM-capable channels is **pairing**:
    *   Unknown senders receive a pairing code; the bot does not process their message.
    *   Approve with: `openclaw pairing approve --channel <channel> [--account <id>] <code>`
    *   Pending requests are capped at **3 per channel**; check `openclaw pairing list --channel <channel> [--account <id>]` if a code didn’t arrive.
*   Opening DMs publicly requires explicit opt-in (`dmPolicy: "open"` and allowlist `"*"`).

Run `openclaw doctor` to surface risky DM policies.

### Is prompt injection only a concern for public bots

No. Prompt injection is about **untrusted content**, not just who can DM the bot. If your assistant reads external content (web search/fetch, browser pages, emails, docs, attachments, pasted logs), that content can include instructions that try to hijack the model. This can happen even if **you are the only sender**. The biggest risk is when tools are enabled: the model can be tricked into exfiltrating context or calling tools on your behalf. Reduce the blast radius by:

*   using a read-only or tool-disabled “reader” agent to summarize untrusted content
*   keeping `web_search` / `web_fetch` / `browser` off for tool-enabled agents
*   sandboxing and strict tool allowlists

Details: [Security](https://docs.openclaw.ai/gateway/security).

### Should my bot have its own email GitHub account or phone number

Yes, for most setups. Isolating the bot with separate accounts and phone numbers reduces the blast radius if something goes wrong. This also makes it easier to rotate credentials or revoke access without impacting your personal accounts. Start small. Give access only to the tools and accounts you actually need, and expand later if required. Docs: [Security](https://docs.openclaw.ai/gateway/security), [Pairing](https://docs.openclaw.ai/channels/pairing).

### Can I give it autonomy over my text messages and is that safe

We do **not** recommend full autonomy over your personal messages. The safest pattern is:

*   Keep DMs in **pairing mode** or a tight allowlist.
*   Use a **separate number or account** if you want it to message on your behalf.
*   Let it draft, then **approve before sending**.

If you want to experiment, do it on a dedicated account and keep it isolated. See [Security](https://docs.openclaw.ai/gateway/security).

### Can I use cheaper models for personal assistant tasks

Yes, **if** the agent is chat-only and the input is trusted. Smaller tiers are more susceptible to instruction hijacking, so avoid them for tool-enabled agents or when reading untrusted content. If you must use a smaller model, lock down tools and run inside a sandbox. See [Security](https://docs.openclaw.ai/gateway/security).

### I ran start in Telegram but didn’t get a pairing code

Pairing codes are sent **only** when an unknown sender messages the bot and `dmPolicy: "pairing"` is enabled. `/start` by itself doesn’t generate a code. Check pending requests:

```
openclaw pairing list telegram
```

If you want immediate access, allowlist your sender id or set `dmPolicy: "open"` for that account.

### WhatsApp will it message my contacts How does pairing work

No. Default WhatsApp DM policy is **pairing**. Unknown senders only get a pairing code and their message is **not processed**. OpenClaw only replies to chats it receives or to explicit sends you trigger. Approve pairing with:

```
openclaw pairing approve whatsapp <code>
```

List pending requests:

```
openclaw pairing list whatsapp
```

Wizard phone number prompt: it’s used to set your **allowlist/owner** so your own DMs are permitted. It’s not used for auto-sending. If you run on your personal WhatsApp number, use that number and enable `channels.whatsapp.selfChatMode`.

## Chat commands, aborting tasks, and “it won’t stop”

### How do I stop internal system messages from showing in chat

Most internal or tool messages only appear when **verbose** or **reasoning** is enabled for that session. Fix in the chat where you see it:

```
/verbose off
/reasoning off
```

If it is still noisy, check the session settings in the Control UI and set verbose to **inherit**. Also confirm you are not using a bot profile with `verboseDefault` set to `on` in config. Docs: [Thinking and verbose](https://docs.openclaw.ai/tools/thinking), [Security](https://docs.openclaw.ai/gateway/security#reasoning--verbose-output-in-groups).

### How do I stopcancel a running task

Send any of these **as a standalone message** (no slash):

```
stop
stop action
stop current action
stop run
stop current run
stop agent
stop the agent
stop openclaw
openclaw stop
stop don't do anything
stop do not do anything
stop doing anything
please stop
stop please
abort
esc
wait
exit
interrupt
```

These are abort triggers (not slash commands). For background processes (from the exec tool), you can ask the agent to run:

```
process action:kill sessionId:XXX
```

Slash commands overview: see [Slash commands](https://docs.openclaw.ai/tools/slash-commands). Most commands must be sent as a **standalone** message that starts with `/`, but a few shortcuts (like `/status`) also work inline for allowlisted senders.

### How do I send a Discord message from Telegram Crosscontext messaging denied

OpenClaw blocks **cross-provider** messaging by default. If a tool call is bound to Telegram, it won’t send to Discord unless you explicitly allow it. Enable cross-provider messaging for the agent:

```
{
  agents: {
    defaults: {
      tools: {
        message: {
          crossContext: {
            allowAcrossProviders: true,
            marker: { enabled: true, prefix: "[from {channel}] " },
          },
        },
      },
    },
  },
}
```

Restart the gateway after editing config. If you only want this for a single agent, set it under `agents.list[].tools.message` instead.

### Why does it feel like the bot ignores rapidfire messages

Queue mode controls how new messages interact with an in-flight run. Use `/queue` to change modes:

*   `steer` - new messages redirect the current task
*   `followup` - run messages one at a time
*   `collect` - batch messages and reply once (default)
*   `steer-backlog` - steer now, then process backlog
*   `interrupt` - abort current run and start fresh

You can add options like `debounce:2s cap:25 drop:summarize` for followup modes.

## Answer the exact question from the screenshot/chat log

**Q: “What’s the default model for Anthropic with an API key?”** **A:** In OpenClaw, credentials and model selection are separate. Setting `ANTHROPIC_API_KEY` (or storing an Anthropic API key in auth profiles) enables authentication, but the actual default model is whatever you configure in `agents.defaults.model.primary` (for example, `anthropic/claude-sonnet-4-5` or `anthropic/claude-opus-4-6`). If you see `No credentials found for profile "anthropic:default"`, it means the Gateway couldn’t find Anthropic credentials in the expected `auth-profiles.json` for the agent that’s running.

* * *

Still stuck? Ask in [Discord](https://discord.com/invite/clawd) or open a [GitHub discussion](https://github.com/openclaw/openclaw/discussions).

---

<!-- SOURCE: https://docs.openclaw.ai/help/debugging -->

# Debugging - OpenClaw

This page covers debugging helpers for streaming output, especially when a provider mixes reasoning into normal text.

## Runtime debug overrides

Use `/debug` in chat to set **runtime-only** config overrides (memory, not disk). `/debug` is disabled by default; enable with `commands.debug: true`. This is handy when you need to toggle obscure settings without editing `openclaw.json`. Examples:

```
/debug show
/debug set messages.responsePrefix="[openclaw]"
/debug unset messages.responsePrefix
/debug reset
```

`/debug reset` clears all overrides and returns to the on-disk config.

## Gateway watch mode

For fast iteration, run the gateway under the file watcher:

This maps to:

```
node --watch-path src --watch-path tsconfig.json --watch-path package.json --watch-preserve-output scripts/run-node.mjs gateway --force
```

Add any gateway CLI flags after `gateway:watch` and they will be passed through on each restart.

## Dev profile + dev gateway (—dev)

Use the dev profile to isolate state and spin up a safe, disposable setup for debugging. There are **two** `--dev` flags:

*   **Global `--dev` (profile):** isolates state under `~/.openclaw-dev` and defaults the gateway port to `19001` (derived ports shift with it).
*   **`gateway --dev`: tells the Gateway to auto-create a default config + workspace** when missing (and skip BOOTSTRAP.md).

Recommended flow (dev profile + dev bootstrap):

```
pnpm gateway:dev
OPENCLAW_PROFILE=dev openclaw tui
```

If you don’t have a global install yet, run the CLI via `pnpm openclaw ...`. What this does:

1.  **Profile isolation** (global `--dev`)
    *   `OPENCLAW_PROFILE=dev`
    *   `OPENCLAW_STATE_DIR=~/.openclaw-dev`
    *   `OPENCLAW_CONFIG_PATH=~/.openclaw-dev/openclaw.json`
    *   `OPENCLAW_GATEWAY_PORT=19001` (browser/canvas shift accordingly)
2.  **Dev bootstrap** (`gateway --dev`)
    *   Writes a minimal config if missing (`gateway.mode=local`, bind loopback).
    *   Sets `agent.workspace` to the dev workspace.
    *   Sets `agent.skipBootstrap=true` (no BOOTSTRAP.md).
    *   Seeds the workspace files if missing: `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`.
    *   Default identity: **C3‑PO** (protocol droid).
    *   Skips channel providers in dev mode (`OPENCLAW_SKIP_CHANNELS=1`).

Reset flow (fresh start):

Note: `--dev` is a **global** profile flag and gets eaten by some runners. If you need to spell it out, use the env var form:

```
OPENCLAW_PROFILE=dev openclaw gateway --dev --reset
```

`--reset` wipes config, credentials, sessions, and the dev workspace (using `trash`, not `rm`), then recreates the default dev setup. Tip: if a non‑dev gateway is already running (launchd/systemd), stop it first:

## Raw stream logging (OpenClaw)

OpenClaw can log the **raw assistant stream** before any filtering/formatting. This is the best way to see whether reasoning is arriving as plain text deltas (or as separate thinking blocks). Enable it via CLI:

```
pnpm gateway:watch --raw-stream
```

Optional path override:

```
pnpm gateway:watch --raw-stream --raw-stream-path ~/.openclaw/logs/raw-stream.jsonl
```

Equivalent env vars:

```
OPENCLAW_RAW_STREAM=1
OPENCLAW_RAW_STREAM_PATH=~/.openclaw/logs/raw-stream.jsonl
```

Default file: `~/.openclaw/logs/raw-stream.jsonl`

## Raw chunk logging (pi-mono)

To capture **raw OpenAI-compat chunks** before they are parsed into blocks, pi-mono exposes a separate logger:

Optional path:

```
PI_RAW_STREAM_PATH=~/.pi-mono/logs/raw-openai-completions.jsonl
```

Default file: `~/.pi-mono/logs/raw-openai-completions.jsonl`

> Note: this is only emitted by processes using pi-mono’s `openai-completions` provider.

## Safety notes

*   Raw stream logs can include full prompts, tool output, and user data.
*   Keep logs local and delete them after debugging.
*   If you share logs, scrub secrets and PII first.

---

<!-- SOURCE: https://docs.openclaw.ai/help/scripts -->

# Scripts - OpenClaw

The `scripts/` directory contains helper scripts for local workflows and ops tasks. Use these when a task is clearly tied to a script; otherwise prefer the CLI.

## Conventions

*   Scripts are **optional** unless referenced in docs or release checklists.
*   Prefer CLI surfaces when they exist (example: auth monitoring uses `openclaw models status --check`).
*   Assume scripts are host‑specific; read them before running on a new machine.

## Auth monitoring scripts

Auth monitoring scripts are documented here: [/automation/auth-monitoring](https://docs.openclaw.ai/automation/auth-monitoring)

## When adding scripts

*   Keep scripts focused and documented.
*   Add a short entry in the relevant doc (or create one if missing).

---

<!-- SOURCE: https://docs.openclaw.ai/diagnostics/flags -->

# Diagnostics Flags - OpenClaw

Diagnostics flags let you enable targeted debug logs without turning on verbose logging everywhere. Flags are opt-in and have no effect unless a subsystem checks them.

## How it works

*   Flags are strings (case-insensitive).
*   You can enable flags in config or via an env override.
*   Wildcards are supported:
    *   `telegram.*` matches `telegram.http`
    *   `*` enables all flags

## Enable via config

```
{
  "diagnostics": {
    "flags": ["telegram.http"]
  }
}
```

Multiple flags:

```
{
  "diagnostics": {
    "flags": ["telegram.http", "gateway.*"]
  }
}
```

Restart the gateway after changing flags.

## Env override (one-off)

```
OPENCLAW_DIAGNOSTICS=telegram.http,telegram.payload
```

Disable all flags:

## Where logs go

Flags emit logs into the standard diagnostics log file. By default:

```
/tmp/openclaw/openclaw-YYYY-MM-DD.log
```

If you set `logging.file`, use that path instead. Logs are JSONL (one JSON object per line). Redaction still applies based on `logging.redactSensitive`.

Pick the latest log file:

```
ls -t /tmp/openclaw/openclaw-*.log | head -n 1
```

Filter for Telegram HTTP diagnostics:

```
rg "telegram http error" /tmp/openclaw/openclaw-*.log
```

Or tail while reproducing:

```
tail -f /tmp/openclaw/openclaw-$(date +%F).log | rg "telegram http error"
```

For remote gateways, you can also use `openclaw logs --follow` (see [/cli/logs](https://docs.openclaw.ai/cli/logs)).

## Notes

*   If `logging.level` is set higher than `warn`, these logs may be suppressed. Default `info` is fine.
*   Flags are safe to leave enabled; they only affect log volume for the specific subsystem.
*   Use [/logging](https://docs.openclaw.ai/logging) to change log destinations, levels, and redaction.

---

<!-- SOURCE: https://docs.openclaw.ai/debug/node-issue -->

# Node + tsx Crash - OpenClaw

## Node + tsx “\_\_name is not a function” crash

## Summary

Running OpenClaw via Node with `tsx` fails at startup with:

```
[openclaw] Failed to start CLI: TypeError: __name is not a function
    at createSubsystemLogger (.../src/logging/subsystem.ts:203:25)
    at .../src/agents/auth-profiles/constants.ts:25:20
```

This began after switching dev scripts from Bun to `tsx` (commit `2871657e`, 2026-01-06). The same runtime path worked with Bun.

## Environment

*   Node: v25.x (observed on v25.3.0)
*   tsx: 4.21.0
*   OS: macOS (repro also likely on other platforms that run Node 25)

## Repro (Node-only)

```
# in repo root
node --version
pnpm install
node --import tsx src/entry.ts status
```

## Minimal repro in repo

```
node --import tsx scripts/repro/tsx-name-repro.ts
```

## Node version check

*   Node 25.3.0: fails
*   Node 22.22.0 (Homebrew `node@22`): fails
*   Node 24: not installed here yet; needs verification

## Notes / hypothesis

*   `tsx` uses esbuild to transform TS/ESM. esbuild’s `keepNames` emits a `__name` helper and wraps function definitions with `__name(...)`.
*   The crash indicates `__name` exists but is not a function at runtime, which implies the helper is missing or overwritten for this module in the Node 25 loader path.
*   Similar `__name` helper issues have been reported in other esbuild consumers when the helper is missing or rewritten.

## Regression history

*   `2871657e` (2026-01-06): scripts changed from Bun to tsx to make Bun optional.
*   Before that (Bun path), `openclaw status` and `gateway:watch` worked.

## Workarounds

*   Use Bun for dev scripts (current temporary revert).
*   Use Node + tsc watch, then run compiled output:
    
    ```
    pnpm exec tsc --watch --preserveWatchOutput
    node --watch openclaw.mjs status
    ```
    
*   Confirmed locally: `pnpm exec tsc -p tsconfig.json` + `node openclaw.mjs status` works on Node 25.
*   Disable esbuild keepNames in the TS loader if possible (prevents `__name` helper insertion); tsx does not currently expose this.
*   Test Node LTS (22/24) with `tsx` to see if the issue is Node 25–specific.

## References

*   [https://opennext.js.org/cloudflare/howtos/keep\_names](https://opennext.js.org/cloudflare/howtos/keep_names)
*   [https://esbuild.github.io/api/#keep-names](https://esbuild.github.io/api/#keep-names)
*   [https://github.com/evanw/esbuild/issues/1031](https://github.com/evanw/esbuild/issues/1031)

## Next steps

*   Repro on Node 22/24 to confirm Node 25 regression.
*   Test `tsx` nightly or pin to earlier version if a known regression exists.
*   If reproduces on Node LTS, file a minimal repro upstream with the `__name` stack trace.

---

<!-- SOURCE: https://docs.openclaw.ai/help/testing -->

# Testing - OpenClaw

OpenClaw has three Vitest suites (unit/integration, e2e, live) and a small set of Docker runners. This doc is a “how we test” guide:

*   What each suite covers (and what it deliberately does _not_ cover)
*   Which commands to run for common workflows (local, pre-push, debugging)
*   How live tests discover credentials and select models/providers
*   How to add regressions for real-world model/provider issues

## Quick start

Most days:

*   Full gate (expected before push): `pnpm build && pnpm check && pnpm test`

When you touch tests or want extra confidence:

*   Coverage gate: `pnpm test:coverage`
*   E2E suite: `pnpm test:e2e`

When debugging real providers/models (requires real creds):

*   Live suite (models + gateway tool/image probes): `pnpm test:live`

Tip: when you only need one failing case, prefer narrowing live tests via the allowlist env vars described below.

## Test suites (what runs where)

Think of the suites as “increasing realism” (and increasing flakiness/cost):

### Unit / integration (default)

*   Command: `pnpm test`
*   Config: `scripts/test-parallel.mjs` (runs `vitest.unit.config.ts`, `vitest.extensions.config.ts`, `vitest.gateway.config.ts`)
*   Files: `src/**/*.test.ts`, `extensions/**/*.test.ts`
*   Scope:
    *   Pure unit tests
    *   In-process integration tests (gateway auth, routing, tooling, parsing, config)
    *   Deterministic regressions for known bugs
*   Expectations:
    *   Runs in CI
    *   No real keys required
    *   Should be fast and stable
*   Pool note:
    *   OpenClaw uses Vitest `vmForks` on Node 22/23 for faster unit shards.
    *   On Node 24+, OpenClaw automatically falls back to regular `forks` to avoid Node VM linking errors (`ERR_VM_MODULE_LINK_FAILURE` / `module is already linked`).
    *   Override manually with `OPENCLAW_TEST_VM_FORKS=0` (force `forks`) or `OPENCLAW_TEST_VM_FORKS=1` (force `vmForks`).

### E2E (gateway smoke)

*   Command: `pnpm test:e2e`
*   Config: `vitest.e2e.config.ts`
*   Files: `src/**/*.e2e.test.ts`
*   Runtime defaults:
    *   Uses Vitest `vmForks` for faster file startup.
    *   Uses adaptive workers (CI: 2-4, local: 4-8).
    *   Runs in silent mode by default to reduce console I/O overhead.
*   Useful overrides:
    *   `OPENCLAW_E2E_WORKERS=<n>` to force worker count (capped at 16).
    *   `OPENCLAW_E2E_VERBOSE=1` to re-enable verbose console output.
*   Scope:
    *   Multi-instance gateway end-to-end behavior
    *   WebSocket/HTTP surfaces, node pairing, and heavier networking
*   Expectations:
    *   Runs in CI (when enabled in the pipeline)
    *   No real keys required
    *   More moving parts than unit tests (can be slower)

### Live (real providers + real models)

*   Command: `pnpm test:live`
*   Config: `vitest.live.config.ts`
*   Files: `src/**/*.live.test.ts`
*   Default: **enabled** by `pnpm test:live` (sets `OPENCLAW_LIVE_TEST=1`)
*   Scope:
    *   “Does this provider/model actually work _today_ with real creds?”
    *   Catch provider format changes, tool-calling quirks, auth issues, and rate limit behavior
*   Expectations:
    *   Not CI-stable by design (real networks, real provider policies, quotas, outages)
    *   Costs money / uses rate limits
    *   Prefer running narrowed subsets instead of “everything”
    *   Live runs will source `~/.profile` to pick up missing API keys
*   API key rotation (provider-specific): set `*_API_KEYS` with comma/semicolon format or `*_API_KEY_1`, `*_API_KEY_2` (for example `OPENAI_API_KEYS`, `ANTHROPIC_API_KEYS`, `GEMINI_API_KEYS`) or per-live override via `OPENCLAW_LIVE_*_KEY`; tests retry on rate limit responses.

## Which suite should I run?

Use this decision table:

*   Editing logic/tests: run `pnpm test` (and `pnpm test:coverage` if you changed a lot)
*   Touching gateway networking / WS protocol / pairing: add `pnpm test:e2e`
*   Debugging “my bot is down” / provider-specific failures / tool calling: run a narrowed `pnpm test:live`

## Live: Android node capability sweep

*   Test: `src/gateway/android-node.capabilities.live.test.ts`
*   Script: `pnpm android:test:integration`
*   Goal: invoke **every command currently advertised** by a connected Android node and assert command contract behavior.
*   Scope:
    *   Preconditioned/manual setup (the suite does not install/run/pair the app).
    *   Command-by-command gateway `node.invoke` validation for the selected Android node.
*   Required pre-setup:
    *   Android app already connected + paired to the gateway.
    *   App kept in foreground.
    *   Permissions/capture consent granted for capabilities you expect to pass.
*   Optional target overrides:
    *   `OPENCLAW_ANDROID_NODE_ID` or `OPENCLAW_ANDROID_NODE_NAME`.
    *   `OPENCLAW_ANDROID_GATEWAY_URL` / `OPENCLAW_ANDROID_GATEWAY_TOKEN` / `OPENCLAW_ANDROID_GATEWAY_PASSWORD`.
*   Full Android setup details: [Android App](https://docs.openclaw.ai/platforms/android)

## Live: model smoke (profile keys)

Live tests are split into two layers so we can isolate failures:

*   “Direct model” tells us the provider/model can answer at all with the given key.
*   “Gateway smoke” tells us the full gateway+agent pipeline works for that model (sessions, history, tools, sandbox policy, etc.).

### Layer 1: Direct model completion (no gateway)

*   Test: `src/agents/models.profiles.live.test.ts`
*   Goal:
    *   Enumerate discovered models
    *   Use `getApiKeyForModel` to select models you have creds for
    *   Run a small completion per model (and targeted regressions where needed)
*   How to enable:
    *   `pnpm test:live` (or `OPENCLAW_LIVE_TEST=1` if invoking Vitest directly)
*   Set `OPENCLAW_LIVE_MODELS=modern` (or `all`, alias for modern) to actually run this suite; otherwise it skips to keep `pnpm test:live` focused on gateway smoke
*   How to select models:
    *   `OPENCLAW_LIVE_MODELS=modern` to run the modern allowlist (Opus/Sonnet/Haiku 4.5, GPT-5.x + Codex, Gemini 3, GLM 4.7, MiniMax M2.5, Grok 4)
    *   `OPENCLAW_LIVE_MODELS=all` is an alias for the modern allowlist
    *   or `OPENCLAW_LIVE_MODELS="openai/gpt-5.2,anthropic/claude-opus-4-6,..."` (comma allowlist)
*   How to select providers:
    *   `OPENCLAW_LIVE_PROVIDERS="google,google-antigravity,google-gemini-cli"` (comma allowlist)
*   Where keys come from:
    *   By default: profile store and env fallbacks
    *   Set `OPENCLAW_LIVE_REQUIRE_PROFILE_KEYS=1` to enforce **profile store** only
*   Why this exists:
    *   Separates “provider API is broken / key is invalid” from “gateway agent pipeline is broken”
    *   Contains small, isolated regressions (example: OpenAI Responses/Codex Responses reasoning replay + tool-call flows)

### Layer 2: Gateway + dev agent smoke (what “@openclaw” actually does)

*   Test: `src/gateway/gateway-models.profiles.live.test.ts`
*   Goal:
    *   Spin up an in-process gateway
    *   Create/patch a `agent:dev:*` session (model override per run)
    *   Iterate models-with-keys and assert:
        *   “meaningful” response (no tools)
        *   a real tool invocation works (read probe)
        *   optional extra tool probes (exec+read probe)
        *   OpenAI regression paths (tool-call-only → follow-up) keep working
*   Probe details (so you can explain failures quickly):
    *   `read` probe: the test writes a nonce file in the workspace and asks the agent to `read` it and echo the nonce back.
    *   `exec+read` probe: the test asks the agent to `exec`\-write a nonce into a temp file, then `read` it back.
    *   image probe: the test attaches a generated PNG (cat + randomized code) and expects the model to return `cat <CODE>`.
    *   Implementation reference: `src/gateway/gateway-models.profiles.live.test.ts` and `src/gateway/live-image-probe.ts`.
*   How to enable:
    *   `pnpm test:live` (or `OPENCLAW_LIVE_TEST=1` if invoking Vitest directly)
*   How to select models:
    *   Default: modern allowlist (Opus/Sonnet/Haiku 4.5, GPT-5.x + Codex, Gemini 3, GLM 4.7, MiniMax M2.5, Grok 4)
    *   `OPENCLAW_LIVE_GATEWAY_MODELS=all` is an alias for the modern allowlist
    *   Or set `OPENCLAW_LIVE_GATEWAY_MODELS="provider/model"` (or comma list) to narrow
*   How to select providers (avoid “OpenRouter everything”):
    *   `OPENCLAW_LIVE_GATEWAY_PROVIDERS="google,google-antigravity,google-gemini-cli,openai,anthropic,zai,minimax"` (comma allowlist)
*   Tool + image probes are always on in this live test:
    *   `read` probe + `exec+read` probe (tool stress)
    *   image probe runs when the model advertises image input support
    *   Flow (high level):
        *   Test generates a tiny PNG with “CAT” + random code (`src/gateway/live-image-probe.ts`)
        *   Sends it via `agent` `attachments: [{ mimeType: "image/png", content: "<base64>" }]`
        *   Gateway parses attachments into `images[]` (`src/gateway/server-methods/agent.ts` + `src/gateway/chat-attachments.ts`)
        *   Embedded agent forwards a multimodal user message to the model
        *   Assertion: reply contains `cat` + the code (OCR tolerance: minor mistakes allowed)

Tip: to see what you can test on your machine (and the exact `provider/model` ids), run:

```
openclaw models list
openclaw models list --json
```

## Live: Anthropic setup-token smoke

*   Test: `src/agents/anthropic.setup-token.live.test.ts`
*   Goal: verify Claude Code CLI setup-token (or a pasted setup-token profile) can complete an Anthropic prompt.
*   Enable:
    *   `pnpm test:live` (or `OPENCLAW_LIVE_TEST=1` if invoking Vitest directly)
    *   `OPENCLAW_LIVE_SETUP_TOKEN=1`
*   Token sources (pick one):
    *   Profile: `OPENCLAW_LIVE_SETUP_TOKEN_PROFILE=anthropic:setup-token-test`
    *   Raw token: `OPENCLAW_LIVE_SETUP_TOKEN_VALUE=sk-ant-oat01-...`
*   Model override (optional):
    *   `OPENCLAW_LIVE_SETUP_TOKEN_MODEL=anthropic/claude-opus-4-6`

Setup example:

```
openclaw models auth paste-token --provider anthropic --profile-id anthropic:setup-token-test
OPENCLAW_LIVE_SETUP_TOKEN=1 OPENCLAW_LIVE_SETUP_TOKEN_PROFILE=anthropic:setup-token-test pnpm test:live src/agents/anthropic.setup-token.live.test.ts
```

## Live: CLI backend smoke (Claude Code CLI or other local CLIs)

*   Test: `src/gateway/gateway-cli-backend.live.test.ts`
*   Goal: validate the Gateway + agent pipeline using a local CLI backend, without touching your default config.
*   Enable:
    *   `pnpm test:live` (or `OPENCLAW_LIVE_TEST=1` if invoking Vitest directly)
    *   `OPENCLAW_LIVE_CLI_BACKEND=1`
*   Defaults:
    *   Model: `claude-cli/claude-sonnet-4-6`
    *   Command: `claude`
    *   Args: `["-p","--output-format","json","--permission-mode","bypassPermissions"]`
*   Overrides (optional):
    *   `OPENCLAW_LIVE_CLI_BACKEND_MODEL="claude-cli/claude-opus-4-6"`
    *   `OPENCLAW_LIVE_CLI_BACKEND_MODEL="codex-cli/gpt-5.4"`
    *   `OPENCLAW_LIVE_CLI_BACKEND_COMMAND="/full/path/to/claude"`
    *   `OPENCLAW_LIVE_CLI_BACKEND_ARGS='["-p","--output-format","json","--permission-mode","bypassPermissions"]'`
    *   `OPENCLAW_LIVE_CLI_BACKEND_CLEAR_ENV='["ANTHROPIC_API_KEY","ANTHROPIC_API_KEY_OLD"]'`
    *   `OPENCLAW_LIVE_CLI_BACKEND_IMAGE_PROBE=1` to send a real image attachment (paths are injected into the prompt).
    *   `OPENCLAW_LIVE_CLI_BACKEND_IMAGE_ARG="--image"` to pass image file paths as CLI args instead of prompt injection.
    *   `OPENCLAW_LIVE_CLI_BACKEND_IMAGE_MODE="repeat"` (or `"list"`) to control how image args are passed when `IMAGE_ARG` is set.
    *   `OPENCLAW_LIVE_CLI_BACKEND_RESUME_PROBE=1` to send a second turn and validate resume flow.
*   `OPENCLAW_LIVE_CLI_BACKEND_DISABLE_MCP_CONFIG=0` to keep Claude Code CLI MCP config enabled (default disables MCP config with a temporary empty file).

Example:

```
OPENCLAW_LIVE_CLI_BACKEND=1 \
  OPENCLAW_LIVE_CLI_BACKEND_MODEL="claude-cli/claude-sonnet-4-6" \
  pnpm test:live src/gateway/gateway-cli-backend.live.test.ts
```

### Recommended live recipes

Narrow, explicit allowlists are fastest and least flaky:

*   Single model, direct (no gateway):
    *   `OPENCLAW_LIVE_MODELS="openai/gpt-5.2" pnpm test:live src/agents/models.profiles.live.test.ts`
*   Single model, gateway smoke:
    *   `OPENCLAW_LIVE_GATEWAY_MODELS="openai/gpt-5.2" pnpm test:live src/gateway/gateway-models.profiles.live.test.ts`
*   Tool calling across several providers:
    *   `OPENCLAW_LIVE_GATEWAY_MODELS="openai/gpt-5.2,anthropic/claude-opus-4-6,google/gemini-3-flash-preview,zai/glm-4.7,minimax/minimax-m2.5" pnpm test:live src/gateway/gateway-models.profiles.live.test.ts`
*   Google focus (Gemini API key + Antigravity):
    *   Gemini (API key): `OPENCLAW_LIVE_GATEWAY_MODELS="google/gemini-3-flash-preview" pnpm test:live src/gateway/gateway-models.profiles.live.test.ts`
    *   Antigravity (OAuth): `OPENCLAW_LIVE_GATEWAY_MODELS="google-antigravity/claude-opus-4-6-thinking,google-antigravity/gemini-3-pro-high" pnpm test:live src/gateway/gateway-models.profiles.live.test.ts`

Notes:

*   `google/...` uses the Gemini API (API key).
*   `google-antigravity/...` uses the Antigravity OAuth bridge (Cloud Code Assist-style agent endpoint).
*   `google-gemini-cli/...` uses the local Gemini CLI on your machine (separate auth + tooling quirks).
*   Gemini API vs Gemini CLI:
    *   API: OpenClaw calls Google’s hosted Gemini API over HTTP (API key / profile auth); this is what most users mean by “Gemini”.
    *   CLI: OpenClaw shells out to a local `gemini` binary; it has its own auth and can behave differently (streaming/tool support/version skew).

## Live: model matrix (what we cover)

There is no fixed “CI model list” (live is opt-in), but these are the **recommended** models to cover regularly on a dev machine with keys.

### Modern smoke set (tool calling + image)

This is the “common models” run we expect to keep working:

*   OpenAI (non-Codex): `openai/gpt-5.2` (optional: `openai/gpt-5.1`)
*   OpenAI Codex: `openai-codex/gpt-5.4`
*   Anthropic: `anthropic/claude-opus-4-6` (or `anthropic/claude-sonnet-4-5`)
*   Google (Gemini API): `google/gemini-3.1-pro-preview` and `google/gemini-3-flash-preview` (avoid older Gemini 2.x models)
*   Google (Antigravity): `google-antigravity/claude-opus-4-6-thinking` and `google-antigravity/gemini-3-flash`
*   Z.AI (GLM): `zai/glm-4.7`
*   MiniMax: `minimax/minimax-m2.5`

Run gateway smoke with tools + image: `OPENCLAW_LIVE_GATEWAY_MODELS="openai/gpt-5.2,openai-codex/gpt-5.4,anthropic/claude-opus-4-6,google/gemini-3.1-pro-preview,google/gemini-3-flash-preview,google-antigravity/claude-opus-4-6-thinking,google-antigravity/gemini-3-flash,zai/glm-4.7,minimax/minimax-m2.5" pnpm test:live src/gateway/gateway-models.profiles.live.test.ts`

### Baseline: tool calling (Read + optional Exec)

Pick at least one per provider family:

*   OpenAI: `openai/gpt-5.2` (or `openai/gpt-5-mini`)
*   Anthropic: `anthropic/claude-opus-4-6` (or `anthropic/claude-sonnet-4-5`)
*   Google: `google/gemini-3-flash-preview` (or `google/gemini-3.1-pro-preview`)
*   Z.AI (GLM): `zai/glm-4.7`
*   MiniMax: `minimax/minimax-m2.5`

Optional additional coverage (nice to have):

*   xAI: `xai/grok-4` (or latest available)
*   Mistral: `mistral/`… (pick one “tools” capable model you have enabled)
*   Cerebras: `cerebras/`… (if you have access)
*   LM Studio: `lmstudio/`… (local; tool calling depends on API mode)

### Vision: image send (attachment → multimodal message)

Include at least one image-capable model in `OPENCLAW_LIVE_GATEWAY_MODELS` (Claude/Gemini/OpenAI vision-capable variants, etc.) to exercise the image probe.

### Aggregators / alternate gateways

If you have keys enabled, we also support testing via:

*   OpenRouter: `openrouter/...` (hundreds of models; use `openclaw models scan` to find tool+image capable candidates)
*   OpenCode Zen: `opencode/...` (auth via `OPENCODE_API_KEY` / `OPENCODE_ZEN_API_KEY`)

More providers you can include in the live matrix (if you have creds/config):

*   Built-in: `openai`, `openai-codex`, `anthropic`, `google`, `google-vertex`, `google-antigravity`, `google-gemini-cli`, `zai`, `openrouter`, `opencode`, `xai`, `groq`, `cerebras`, `mistral`, `github-copilot`
*   Via `models.providers` (custom endpoints): `minimax` (cloud/API), plus any OpenAI/Anthropic-compatible proxy (LM Studio, vLLM, LiteLLM, etc.)

Tip: don’t try to hardcode “all models” in docs. The authoritative list is whatever `discoverModels(...)` returns on your machine + whatever keys are available.

## Credentials (never commit)

Live tests discover credentials the same way the CLI does. Practical implications:

*   If the CLI works, live tests should find the same keys.
*   If a live test says “no creds”, debug the same way you’d debug `openclaw models list` / model selection.
*   Profile store: `~/.openclaw/credentials/` (preferred; what “profile keys” means in the tests)
*   Config: `~/.openclaw/openclaw.json` (or `OPENCLAW_CONFIG_PATH`)

If you want to rely on env keys (e.g. exported in your `~/.profile`), run local tests after `source ~/.profile`, or use the Docker runners below (they can mount `~/.profile` into the container).

## Deepgram live (audio transcription)

*   Test: `src/media-understanding/providers/deepgram/audio.live.test.ts`
*   Enable: `DEEPGRAM_API_KEY=... DEEPGRAM_LIVE_TEST=1 pnpm test:live src/media-understanding/providers/deepgram/audio.live.test.ts`

## BytePlus coding plan live

*   Test: `src/agents/byteplus.live.test.ts`
*   Enable: `BYTEPLUS_API_KEY=... BYTEPLUS_LIVE_TEST=1 pnpm test:live src/agents/byteplus.live.test.ts`
*   Optional model override: `BYTEPLUS_CODING_MODEL=ark-code-latest`

## Docker runners (optional “works in Linux” checks)

These run `pnpm test:live` inside the repo Docker image, mounting your local config dir and workspace (and sourcing `~/.profile` if mounted):

*   Direct models: `pnpm test:docker:live-models` (script: `scripts/test-live-models-docker.sh`)
*   Gateway + dev agent: `pnpm test:docker:live-gateway` (script: `scripts/test-live-gateway-models-docker.sh`)
*   Onboarding wizard (TTY, full scaffolding): `pnpm test:docker:onboard` (script: `scripts/e2e/onboard-docker.sh`)
*   Gateway networking (two containers, WS auth + health): `pnpm test:docker:gateway-network` (script: `scripts/e2e/gateway-network-docker.sh`)
*   Plugins (custom extension load + registry smoke): `pnpm test:docker:plugins` (script: `scripts/e2e/plugins-docker.sh`)

The live-model Docker runners also bind-mount the current checkout read-only and stage it into a temporary workdir inside the container. This keeps the runtime image slim while still running Vitest against your exact local source/config. Manual ACP plain-language thread smoke (not CI):

*   `bun scripts/dev/discord-acp-plain-language-smoke.ts --channel <discord-channel-id> ...`
*   Keep this script for regression/debug workflows. It may be needed again for ACP thread routing validation, so do not delete it.

Useful env vars:

*   `OPENCLAW_CONFIG_DIR=...` (default: `~/.openclaw`) mounted to `/home/node/.openclaw`
*   `OPENCLAW_WORKSPACE_DIR=...` (default: `~/.openclaw/workspace`) mounted to `/home/node/.openclaw/workspace`
*   `OPENCLAW_PROFILE_FILE=...` (default: `~/.profile`) mounted to `/home/node/.profile` and sourced before running tests
*   `OPENCLAW_LIVE_GATEWAY_MODELS=...` / `OPENCLAW_LIVE_MODELS=...` to narrow the run
*   `OPENCLAW_LIVE_REQUIRE_PROFILE_KEYS=1` to ensure creds come from the profile store (not env)

## Docs sanity

Run docs checks after doc edits: `pnpm docs:list`.

## Offline regression (CI-safe)

These are “real pipeline” regressions without real providers:

*   Gateway tool calling (mock OpenAI, real gateway + agent loop): `src/gateway/gateway.test.ts` (case: “runs a mock OpenAI tool call end-to-end via gateway agent loop”)
*   Gateway wizard (WS `wizard.start`/`wizard.next`, writes config + auth enforced): `src/gateway/gateway.test.ts` (case: “runs wizard over ws and writes auth token config”)

## Agent reliability evals (skills)

We already have a few CI-safe tests that behave like “agent reliability evals”:

*   Mock tool-calling through the real gateway + agent loop (`src/gateway/gateway.test.ts`).
*   End-to-end wizard flows that validate session wiring and config effects (`src/gateway/gateway.test.ts`).

What’s still missing for skills (see [Skills](https://docs.openclaw.ai/tools/skills)):

*   **Decisioning:** when skills are listed in the prompt, does the agent pick the right skill (or avoid irrelevant ones)?
*   **Compliance:** does the agent read `SKILL.md` before use and follow required steps/args?
*   **Workflow contracts:** multi-turn scenarios that assert tool order, session history carryover, and sandbox boundaries.

Future evals should stay deterministic first:

*   A scenario runner using mock providers to assert tool calls + order, skill file reads, and session wiring.
*   A small suite of skill-focused scenarios (use vs avoid, gating, prompt injection).
*   Optional live evals (opt-in, env-gated) only after the CI-safe suite is in place.

## Adding regressions (guidance)

When you fix a provider/model issue discovered in live:

*   Add a CI-safe regression if possible (mock/stub provider, or capture the exact request-shape transformation)
*   If it’s inherently live-only (rate limits, auth policies), keep the live test narrow and opt-in via env vars
*   Prefer targeting the smallest layer that catches the bug:
    *   provider request conversion/replay bug → direct models test
    *   gateway session/history/tool pipeline bug → gateway live smoke or CI-safe gateway mock test



---

<!-- SOURCE: https://docs.openclaw.ai/help -->

# Help - OpenClaw

If you want a quick “get unstuck” flow, start here:

*   **Troubleshooting:** [Start here](https://docs.openclaw.ai/help/troubleshooting)
*   **Install sanity (Node/npm/PATH):** [Install](https://docs.openclaw.ai/install#nodejs--npm-path-sanity)
*   **Gateway issues:** [Gateway troubleshooting](https://docs.openclaw.ai/gateway/troubleshooting)
*   **Logs:** [Logging](https://docs.openclaw.ai/logging) and [Gateway logging](https://docs.openclaw.ai/gateway/logging)
*   **Repairs:** [Doctor](https://docs.openclaw.ai/gateway/doctor)

If you’re looking for conceptual questions (not “something broke”):

*   [FAQ (concepts)](https://docs.openclaw.ai/help/faq)

