---
name: instagram-media-links-and-post-insights
description: Return video/audio links or organize verified fields from user-provided public Instagram video posts and Reels. Also select this Skill for first-use Apify setup or when Apify MCP is unconnected or its authorization/readiness is unconfirmed; provide the host-specific guidance before stopping.
---

# Instagram Media Links & Post Insights

Get the video or audio links and post fields actually returned for public Instagram video posts or Reels you provide. Use **Media links** to retrieve Actor-supplied `videoUrl` and `audioUrl` values, or **Post insights** to organize and compare returned likes, comments, author, and publish-time fields. Results depend on the fields the Actor returns; this Skill does not download media files. Respond in the user's language while preserving returned field names and source values.

Installing this Skill and connecting Apify are separate steps. You can install the Skill before setting up Apify. To run it, you need an Apify account and an Apify MCP/plugin connection that your Agent host supports and has authorized; installing the Skill does not create an account or connect or authorize a plugin. See the [Instagram Video Scraper API Actor on Apify](https://apify.com/apple_yang/instagram-video-scraper-api) for Actor details, the [project PRD](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/instagram-media-links-and-post-insights-prd.md) for documented scope and requirements, and the [project home](https://github.com/apismith-labs/instagram-ai-agent-skills).

## Example requests

**Media links**

```text
Return the video and audio links actually provided for this public Instagram Reel. Keep the original URL with the result, and say if either field is missing.
[INSTAGRAM_URL]
```

**Post insights**

```text
Organize the author, publish time, likes, and comments actually returned for these public Instagram video posts or Reels. Compare only the returned raw counts. Do not calculate rates or infer trends, audience response, performance changes, or causes.
[INSTAGRAM_URLS]
```

If the user requests both, return both sets of fields from one Actor result where possible. For an unclear request, ask whether they want media links, post fields, or both. Read [the workflow reference](references/workflow.md) before processing a request.

## First use: check Apify readiness and follow host-specific setup

Installing this Skill and connecting Apify are separate steps. Before the first real task, inspect the Apify tools and live schemas actually exposed in the current session, along with any host-visible authorization or connection status. If a tool is unavailable, authorization is unconfirmed, or readiness cannot be established, stop first. Tell the user that no Actor was started and no results were received, then provide the instructions for the host you have identified below. Do not infer that a plugin is uninstalled, install anything, change host settings, start OAuth, or bypass the host with another Actor, HTTP/API, shell, token, or cookie. Do not repeat setup guidance once readiness is confirmed. After setup, proceed only when the current session exposes and confirms the required Actor call, schema, run-status, and result-reading capabilities; otherwise stop and explain the gap.

### OpenClaw

Install this Skill from ClawHub in the environment connected to your OpenClaw Gateway by running `openclaw skills install @apismith-labs/instagram-media-links-and-post-insights`. The CLI installs into the active workspace by default; add `--global` for the shared managed Skills directory. This installs the Skill only: an Apify account and a separately configured and authorized Apify plugin are required to run it, and Skill installation does not create, connect, or authorize either. OpenClaw 2026.1.0 or later and Node.js 22+ are required; see the [current Apify plugin requirements](https://docs.apify.com/integrations/openclaw). Run `openclaw skills check` to inspect the default Agent, open a new session, and use `$instagram-media-links-and-post-insights`. If you are unsure of your directory or Agent permissions, do not guess; see the [project's OpenClaw guide](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/openclaw.md) and the [OpenClaw Skills CLI documentation](https://docs.openclaw.ai/cli/skills). The Apify plugin uses OpenClaw's separate configuration flow, not OAuth. After completing the OpenClaw guidance below, confirm the `apify` tool is visible in a new session. Never send an API key in chat.

### OpenClaw first-use setup guidance

Only when the current host is explicitly identified as OpenClaw and Apify tools are unavailable, the host explicitly reports missing authorization, or readiness cannot be confirmed, present the OpenClaw setup block below verbatim. Stop the Actor call first and say no Actor was started and no results were received. Do not substitute OpenClaw commands for another host's setup; missing tools do not prove that a plugin is uninstalled.

> There's no confirmed usable Apify tool available to me in this OpenClaw session, so I can't start the analysis. This doesn't necessarily mean the plugin is uninstalled: it may be disabled, your Apify account may not be configured, or this Agent may not have permission. I have not started any Actor.
>
> If you don't have an Apify account, [create one in the Apify Console](https://console.apify.com/sign-up).
>
> Choose one way to install the Apify OpenClaw plugin:
> - Run `openclaw plugins install @apify/apify-openclaw-plugin`.
> - Or, if your OpenClaw Control UI shows the plugin catalog, open **Plugins**, search for **Apify**, and install the Apify listing from ClawHub. If it is not available there, use the CLI command above.
>
> Restart the OpenClaw Gateway after installation.
>
> First, prepare an Apify API Key. The [official plugin README](https://github.com/apify/apify-openclaw-plugin) explains how to create and configure it. Then run `openclaw apify setup` and follow the wizard to finish configuration. Never send your API Key in chat.
>
> After setup, open a new conversation and try your request again.
>
> For detailed steps, see the [OpenClaw setup guide](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/openclaw.md#set-up-the-apify-plugin).

Do not start an Actor until a usable Apify tool and required schema are visible and explicit host status does not report missing authorization. If readiness remains unclear, stop and direct the user to the corresponding setup guidance above. The Skill cannot install plugins or change host settings.

### ChatGPT: regular chat and work mode

Unless the user has explicitly said they already have an Apify account, show this separate registration note:

**If you don't have an Apify account, [sign up for Apify](https://console.apify.com/sign-up) before continuing.**

**Connect Apify** in this order:

1. Open **Plugins → + → Add custom MCP server**.
2. Set **Name** to `Apify MCP` and **Server URL** to `https://mcp.apify.com`.
3. Set **Authentication** to **OAuth**.
4. Read the risk notice, check the confirmation box, and select **Create as a plugin**.
5. Follow ChatGPT's prompts to sign in to Apify and authorize access.
6. After connecting, we recommend resubmitting the task in a new ChatGPT **work mode** chat. If continuing in the current chat, refresh the available tools before trying again. In this project's tests, regular chat did not reliably invoke the Skill, so prefer work mode.

If **Add custom MCP server** is unavailable, check account, workspace, or administrator permissions and consult the [OpenAI guide to connecting custom MCP servers](https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt). The Apify MCP connection and Skill installation are separate; one connection can be shared by multiple Skills. Never share an API key, token, or other credential in chat. Once ready, rely only on the Apify tools actually visible in the current session. For complete ChatGPT setup and usage steps, see the [project's ChatGPT guide](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/chatgpt.md#1-add-and-authorize-the-apify-mcp-connection).

### Codex desktop and CLI

Installing the Codex Skill and the Apify plugin are separate steps. Install this Skill's complete directory first. If `$skill-installer` is available in your Codex session, ask it to install from `https://github.com/apismith-labs/instagram-ai-agent-skills/tree/main/skills/instagram-media-links-and-post-insights` using Git to `~/.agents/skills/instagram-media-links-and-post-insights/`; stop without overwriting if that destination already exists. If you already have a local clone, copy the complete `skills/instagram-media-links-and-post-insights/` folder into the current project's `.agents/skills/` or your user-level `~/.agents/skills/` directory. OpenAI's [Codex Skill directory documentation](https://developers.openai.com/api/reference/cli#use-the-cli-from-a-coding-agent) lists these locations. Start a new session and explicitly invoke `$instagram-media-links-and-post-insights`. It is ready when the new session discovers the Skill and the required Apify tools and operations are available.

**Codex desktop:** In the ChatGPT desktop app, switch to **Codex** from the upper-left menu. In the sidebar, open **Plugins**, use the dropdown beside **+**, and select **Add marketplace**. Enter `apify/apify-codex-plugin` as the source and add it. Open the **Personal** page, then under Apify Plugin select **Add** → **Add to Codex** → **Install Apify**. When the browser opens Apify OAuth, review the permissions and select **Allow access**.

**Codex CLI:** In Codex CLI, enter `/plugins`, select **Add Marketplace**, enter `apify/apify-codex-plugin`, and confirm. Open the **Apify Plugin** page, select Apify → **Install plugin**. When an Apify tool requiring authorization is first called, the browser opens OAuth; review the permissions and select **Allow access**. The desktop app and CLI have separate setup entry points; do not use one set of steps for the other. Then invoke `$instagram-media-links-and-post-insights` in a new session and confirm the tools are available. See the [Codex guide](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/codex.md), [Apify Codex desktop guide](https://docs.apify.com/integrations/codex-app), and [Apify Codex CLI guide](https://docs.apify.com/integrations/codex-cli).

### Claude Web and Claude Desktop chat

**Install this Skill:** In Claude's left sidebar, open **Customize** (some accounts are transitioning to **Plugins**) → **Skills** → **+** → **Create skill** → **Upload a skill**. Upload a trusted Skill ZIP, complete the scan, and enable it. Enterprise administrators may restrict code execution, Skill creation, or uploads. If the entry is unavailable, see [Claude's official Skills guide](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

**Connect Apify:** In Claude's sidebar, open **Customize/Plugins → Connectors**, find the official Apify Plugin, and select **Add**. In the Apify plugin page, open **Connectors** and select **Connect** for the `apify` connection. In the dialog, select **Continue → Add**. In the Apify authorization page opened by your browser, verify the account and permissions, then select **Allow access**. Confirm the connection shows as connected. In a new chat, use the input **+** menu to enable the Apify Connector, then enter `/` to select this Skill if that selector is available; you can also name the Skill in your request. Claude Desktop chat uses the same settings as the regular chat for that Claude account. Do not use Claude Code CLI commands for Claude Desktop chat. Ask an enterprise administrator to configure connectors if the workspace restricts them. See the [Claude guide](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/claude-web.md), [Apify Claude.ai guide](https://docs.apify.com/integrations/claude-ai), and [Anthropic remote MCP guide](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp).

### Claude Code CLI

Claude Code CLI and Claude Desktop chat are separate products. First install and enable this Skill in your Claude Web/Desktop account using the steps above. In a local Claude Code CLI session signed in to the same `claude.ai` account, if your version supports Skills sync, run `/skills` in a new session, confirm the Skill appears under `claude.ai sync`, then use `/` to select its displayed command. Alternatively, place the complete Skill directory at `~/.claude/skills/instagram-media-links-and-post-insights/`. In Claude Code CLI, run `/plugin install apify` and choose the installation scope; then run `/mcp`, enable `plugin:apify:apify`, and select **Authenticate**. Sign in to Apify in the browser, review permissions, and select **Allow access**. Check the connection status in `/mcp` and verify the tools are actually exposed in the session; then invoke this Skill in a new session. Apify's current documentation confirms this Claude Code CLI path; do not generalize it to the Claude desktop app's Code tab or Web/remote code sessions. See [Claude Code Skills](https://code.claude.com/docs/en/skills), the [Apify Claude Code CLI guide](https://docs.apify.com/integrations/claude-code-cli), and the [project's Claude guide](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/claude-web.md).

### Manus

**Connect Apify:** Open **Settings → Connectors → + Add connectors → Custom MCP → + Add custom MCP → Direct configuration**. Set **Server name** to `Apify`, **Transport type** to `HTTP`, and **Server URL** to `https://mcp.apify.com`, then select **Save**. When you first call an Apify tool in chat, sign in and authorize through the OAuth prompt shown by Manus. Do not use an API token instead. Confirm the connection is saved and the tools are available in the current session.

**Install and invoke this Skill:** Open **Skills → + Add → Import from GitHub**, paste the public GitHub URL for this Skill folder, `https://github.com/apismith-labs/instagram-ai-agent-skills/tree/main/skills/instagram-media-links-and-post-insights`, and select **Import**. Confirm the Skill appears in your personal list and enable it. In a new task, enter `/` in the input box to select this Skill, and enable Apify with the connector button below the input area. Before proceeding, confirm the Skill is selectable and the Apify connection is enabled. Manus's official documentation says MCP is available on all plans, but account permissions, interface changes, and task outcomes may vary. See the [project's Manus guide](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/manus.md), [Apify Manus guide](https://docs.apify.com/integrations/manus), and [Manus Skills guide](https://help.manus.im/en/articles/14753565-how-to-share-and-use-skills-in-manus).

### Other or unrecognized hosts

If the host is unclear, ask the user which product surface they are using instead of guessing menus or commands. Show host-specific steps only after identifying that host. If an account or workspace lacks the relevant entry, point to the linked official platform documentation or suggest contacting an administrator. Do not treat MCP, Connectors, plugin catalogs, and CLI configuration as interchangeable.

## Actor preflight and input

Before telling the user that processing will begin, complete the internal preflight in [the workflow reference](references/workflow.md). Do not first say “I’ll process these” or imply a run has started. Use only `apple_yang/instagram-video-scraper-api`. A visible Apify connection or OAuth success does not by itself confirm that this Actor's tool, schema, or result-reading tools are exposed.

The preflight must establish a supported tool path, the current input/output contract, a way to submit the user URLs in the required `videoUrls` array, and a way to obtain actual result rows. For a dedicated tool, verify that its live description/schema identifies the exact target owner and Actor; similar names or an unclear identity are insufficient. If any required capability is absent or unclear, stop before an Actor call. Tell the user which tool or capability is missing, and state that no Actor was started and no results were received. If the host is ChatGPT, then display the complete ChatGPT first-use guidance above; do not replace it with generic settings/search wording or a link-only reply. Do not infer that a public Actor is callable, guess tool names/arguments/Actor identifier format/result envelopes, use another Actor, or bypass the host with HTTP, shell, tokens, or `sessionid`.

Preserve each input URL exactly as supplied and its original order. Use one call for a single request or one batch call when supported. For combined Media links and Post insights requests, use one input set and one Actor result where possible; do not repeat calls without a task need. Never use API tokens, `sessionid`, shell commands, or direct HTTP requests to bypass host tools. Do not call another Actor.

## Media type and links

- Do not infer media type from URL path. `/p/` identifies a post path, not a video. Use only the user's stated intent and evidence in the Actor result.
- If media type is unknown, or no video/audio direct link is returned, say that support for this content cannot be confirmed. Do not guess or promise a link.
- Do not claim photo or carousel posts are supported or unsupported; they remain unverified and outside the first-release commitment.
- A returned `videoUrl` or `audioUrl` means the Actor supplied a direct link. It does not mean the Skill downloaded a file or that the link will remain valid.

## Post insights boundaries

Organize or compare only raw fields actually returned and otherwise verified, such as `likeCount`, `commentCount`, author fields, `createTime`, and `timestamp`. Treat each run as a snapshot of that collection. Do not promise or infer `views`, play count, impressions, reach, follower counts, shares, saves, or other unverified fields. Do not calculate engagement rates or other derived metrics needing unverified inputs. Do not infer trends, audience response, performance changes, or causation, and do not present a simple count comparison as a validated business conclusion. Missing fields are not zero.

## Match and report every input

Follow [the workflow reference](references/workflow.md). Match a result to an input using a verifiable match on the returned `url`. Do not rely on `code`, `pk`, or `id` unless their matching behavior has been independently verified for the current contract. Do not match by output order. Preserve exact input strings; do not merge URLs using unverified normalization. Deduplicate only exact identical strings, and retain their input positions.

Report each input separately and distinguish:

1. A non-empty `errMsg`: quote/report the actual returned message without adding a cause.
2. Empty or missing `errMsg`: state that the field is empty or missing; do not infer success from it.
3. If no result row can be reliably matched, explain that no matching row was received and cite the available evidence in the user's language; do not say the Actor failed or the post does not exist.
4. If a matched row has a missing, empty, or unreturned field, explain that the field was not returned or is unavailable, in the user's language; do not interpret missing links as proof media does not exist or missing counts as zero.
5. If the returned `url` is missing, conflicting, or has multiple candidates, explain that the input-to-result mapping cannot be confirmed and cite the evidence in the user's language. Never guess by position.
6. Partial batch results: show each confirmed, errored, unmatched, and unresolved item; do not say the batch fully succeeded.

Do not assume top-level error formats, batch order guarantees, or that `errMsg` is always present. Report only the tool result actually visible to the host. If the result cannot establish media type, state that support cannot be confirmed.

## Scope and privacy

Handle only public video post and Reel URLs supplied by the user. Private accounts, Stories, and authentication-required content are outside the supported scope. Do not discover account posts, monitor on a schedule, extract transcripts, interpret visuals, or download/save media files. Do not ask for or expose passwords, API keys, cookies, or session IDs. Do not include fixed prices or estimates; if asked about usage, direct the user to their Apify Console. The user is responsible for following applicable service terms, copyright, and privacy requirements; do not give legal conclusions.
