---
name: instagram-creator-reels-insights
description: Review public creators’ recent Instagram videos, including Reels and regular video posts, in source-linked daily or weekly reports. Also select this Skill for first-use Apify setup or when Apify MCP is unconnected or its authorization/readiness is unconfirmed; provide the host-specific guidance before stopping.
---

# Instagram Creator Video Insights

Turn recent public Instagram videos—including Reels and regular video posts—from one or more creators into a source-linked report. Name the public accounts, choose Daily Scan or Weekly Review, and the Skill finds recent posts, transcribes the videos it can, and summarizes what was actually said, with source links for each post cited in the report.

## What you get

- **Daily Scan** reviews the most recent 24 hours for each creator you name.
- **Weekly Review** reviews the most recent 7 days and highlights recurring topics, hooks, and calls to action.

Every report keeps each creator in a separate section, ties findings to source posts, and separates transcript evidence from interpretation. Cross-creator comparisons appear only when the available transcripts support them.

## Typical use cases

- Identify transcript-supported topics and hooks worth studying in a creator's recent videos.
- Compare how specified creators discuss similar subjects when their returned transcripts support the comparison.
- Turn recurring ideas in returned transcripts into source-linked angles for your own content planning.

## Copy-ready requests

Replace the placeholders with public accounts and your own brand.

**Daily Scan**

```text
Run a Daily Scan for [CREATOR_1], [CREATOR_2], and [CREATOR_3]. Review their recent public Instagram videos—including Reels and regular video posts—from the last 24 hours. Give each creator a separate section with links to source posts and transcript-based observations.
```

**Weekly Review**

```text
Run a Weekly Review for [CREATOR_1], [CREATOR_2], and [CREATOR_3] for the last 7 days. Review their public Instagram videos, including Reels and regular video posts. Summarize each creator separately, then compare themes only where the available transcripts support a comparison. Link each finding to its source post.
```

**Content ideas**

```text
Based on the available transcripts from [CREATOR_1], [CREATOR_2], and [CREATOR_3], suggest content angles for [MY_BRAND]. Link observations to source posts and distinguish transcript-supported observations from your suggestions.
```

## Before you start

This Skill needs an Apify connection exposed and authorized in your host; installing the Skill does not create that connection. If the current session cannot confirm usable Apify tools, authorization, or required run and result-reading conditions, the Skill stops before starting any Actor. It analyzes only posts and transcripts actually returned, so coverage can be partial or unknown. The per-creator video limit caps transcript processing, not discovery coverage or usage. Never provide credentials in chat.

## OpenClaw setup and first use

OpenClaw is the primary host for this ClawHub Skill. Installing the Skill and configuring the Apify plugin are separate steps; the Skill does not install, connect, or authorize Apify automatically.

Install the Skill from ClawHub with `openclaw skills install @apismith-labs/instagram-creator-reels-insights`. If you use a repository already cloned in the Gateway environment, run `openclaw skills install ./skills/instagram-creator-reels-insights --global` from the repository root; omit `--global` to install only in the active workspace. OpenClaw 2026.1.0 or later and Node.js 22+ are required. See the [Apify OpenClaw requirements](https://docs.apify.com/integrations/openclaw).

For the Apify plugin, use the OpenClaw-specific setup below. This plugin uses OpenClaw's separate configuration flow, not OAuth. The Skill must not install the plugin or change OpenClaw configuration.

At the first real task, inspect only the Apify tools, live schemas, authorization/connection status, run-status queries, and result-reading capabilities actually exposed in the current session. If a required condition is missing or cannot be confirmed, stop before calling an Actor, tell the user that no Actor was started and no results were received, and explain what could not be confirmed. Show the following setup guidance only when the host is explicitly identified as OpenClaw and readiness is unavailable or unconfirmed. Missing tools do not prove that the plugin is uninstalled.

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

Do not start an Actor until the user completes setup and a usable Apify tool is available. Never ask the user to send an API Key in chat. After setup, open a new OpenClaw conversation or refresh available tools before retrying. Check the default Agent with `openclaw skills check`; if needed, specify one with `openclaw skills check --agent YOUR_AGENT_ID`. In a new session, invoke `$instagram-creator-reels-insights`. For directory or Agent permission questions, follow the [project OpenClaw guide](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/openclaw.md).

## Readiness and usage safeguards

- **Connect Apify in your host.** The Skill uses Apify Actors to read public posts and transcripts. Installing the Skill and connecting Apify are separate steps, and both are needed. Use only tools actually exposed in the current session or explicit connection status from the host. At the first actual analysis request, if Apify is unavailable, the host reports missing authorization, or readiness cannot be confirmed from host-visible status, stop without starting an Actor. Tell the user that no Actor was started and no results were received; explain what readiness condition could not be confirmed. If the host cannot expose connection status, say it cannot be confirmed; do not infer it from Skill metadata. For OpenClaw, show the setup guidance above only when the host is identified as OpenClaw; for ChatGPT, show the complete ChatGPT first-use instructions in the host-specific section below when its condition applies; for other identified hosts, use only the matching platform-specific guidance, without showing OpenClaw commands. Do not install plugins, change host configuration, or use shell, direct REST/API, tokens, cookies, or session IDs to bypass missing tools or authorization. After the user configures Apify, ask them to start a new session or refresh available tools and retry the request.
- **Set a per-creator video limit.** It caps how many eligible videos are processed for transcripts in each report. It is a processing limit, not a full-account scan, and it does not cap usage or cost.
- **Check your Apify usage.** More creators or more videos can mean more usage on your own Apify account. Review current usage in the Apify Console; the Skill does not estimate a price or promise a fee cap.
- **Never paste credentials.** Do not share Instagram passwords, API tokens, cookies, or session values in chat. The Skill reads public accounts only.

For installation steps and more prompt examples, see the [project README](https://github.com/apismith-labs/instagram-ai-agent-skills#instagram-creator-video-insights).

## What the results mean

A report covers the posts and transcripts that run actually found and returned. Coverage can be partial or unknown, and the report states which. A creator with no returned post is not proof that the creator posted nothing, and an empty result is not evidence that the period had no new videos. Missing metrics are never treated as zero.

## Scope

- Daily Scan and Weekly Review for user-specified public accounts only. Do not offer a single-URL analysis task or a posts-only report.
- Do not schedule runs, monitor in the background, or claim to remember accounts or transcripts across sessions.
- Process only public accounts. Do not bypass login, rate limits, or platform restrictions, and never ask for or reveal tokens, cookies, session IDs, passwords, or authorization headers.

## How this Skill runs

Before each report, read [the workflow contract](references/workflow.md). Use the bundled offline helper at `scripts/workflow.py` for settings validation, UTC window construction, candidate selection and coverage status, batch splitting, and transcript reconciliation. Invoke it with `python3 <skill-directory>/scripts/workflow.py` and one JSON object on stdin; consume its JSON result and treat any nonzero exit or `error` as a stop condition. The helper makes no network calls and stores no settings. If the host cannot safely execute it or provide private in-memory inputs, explain that limitation without starting Actor calls.

### First use and saved settings

The first setup confirms only: (1) the public accounts to monitor, (2) the maximum number of videos per creator to include in each report, and (3) whether the user agrees to save the account list and setting. Do not ask for a report budget or per-run cost setting. Save only if the host supports user-authorized persistence. Otherwise provide a reusable request containing the accounts and per-creator video limit. Routine runs reuse available settings and do not repeat setup.

The per-creator limit applies after candidate discovery: it selects how many eligible returned videos are sent for transcript processing and analysis. It is not an Actor retrieval limit, does not limit discovery reads, does not guarantee complete account coverage, and does not cap usage or cost. If an older saved settings object contains `report_budget_usd`, ignore that field; it is not a current setting and must not affect planning or Actor calls.

Use plain language and reply in the user's language. Do not expose schema fields or require users to configure Actor runs. If Apify readiness is not established, follow the first-use host-specific guidance above; for ChatGPT, display its complete setup block rather than generic connection-settings or plugin-search instructions. Never ask them to paste a token, cookie, password, session ID, or authorization value into chat.

Be transparent that Profile Posts discovery and Transcript processing may involve multiple Actor runs and may generate Apify usage according to the user's account and each Actor's current rules. Do not conceal calls, estimate a fixed fee, promise a fee cap, or repeatedly ask about a budget. Users can review actual usage in Apify Console. Follow approvals required by the host.

### Request and modes

- Accept public Instagram usernames or profile URLs, a report mode, and optional timezone/report language.
- If mode is omitted, use Daily Scan: the rolling 24 hours before the request. Weekly Review uses the rolling 7 days. Resolve explicit calendar periods in the user's timezone and show the exact UTC boundaries and displayed timezone. Pass the requested IANA timezone to the helper as `display_timezone`; if none is specified, use and label UTC.
- Explain briefly that the report discovers recent posts, transcribes eligible videos, and analyzes their spoken content.
- Normalize supplied account names/profile URLs conservatively. Keep each requested account mapped to its normalized identity. Reject ambiguous or unsupported input; never broaden to other accounts.

### Execution

1. At the first actual analysis request, check the tools actually exposed by the selected host, their live input schemas, authorization, run-status query, and result/Dataset read capabilities for the [Instagram Profile Posts & Reels Scraper](https://apify.com/apple_yang/instagram-post-scraper) (`apple_yang/instagram-post-scraper`). Tool names and argument shapes vary by host; do not assume every host exposes `call-actor` or the same contract. Before Profile Posts discovery, do not require an output enum or a Reel/non-Reel mapping; a string `type` field without an enum is not a blocker to retrieving raw records or processing records that meet the project rule below. If the Profile Posts Actor/tool, authorization, required input contract, run-status query, or ability to read raw results is unavailable or unconfirmed, stop before that Actor call and explain the specific blocker; do not try another Actor. Inspect returned output fields and preserve their raw values after discovery without guessing aliases. Verify the [Instagram Transcript API & Profile Scraper](https://apify.com/apple_yang/instagram-transcripts-scraper) (`apple_yang/instagram-transcripts-scraper`) live contract only before any Transcript call. If the host cannot expose plugin or authorization status, say it cannot be confirmed rather than inferring it. For OpenClaw, show the first-time setup guidance above only when the host is identified as OpenClaw; for ChatGPT, use the complete ChatGPT first-use block below when its condition applies; for other identified hosts, use the corresponding platform guide without showing OpenClaw commands. Never install a plugin or change host configuration automatically. These conditions do not create a budget-parameter requirement.
2. Run the helper `settings` operation using the accounts, positive integer per-creator video limit, and save consent. If the current request omits `per_creator_limit` and no existing user-authorized setting is available, ask the user to confirm that processing limit before discovery; do not save it without explicit consent. For Daily/Weekly boundaries, call `window` with the request timestamp and mode. Keep its `end_utc_exclusive` value through selection and pass the requested IANA timezone as `display_timezone` to `select` (use and label `UTC` when the request specifies none).
3. Use the host's live-supported input to discover posts for the requested accounts and time window. For every `apple_yang/instagram-post-scraper` request, explicitly include the JSON field `"skipPinnedPosts": true`; do not omit it and rely on the Actor default. Before the call, verify the live input schema accepts this field as a boolean; if it is absent or conflicts, stop and report the schema mismatch rather than omitting or changing the value. This setting applies only to Profile Posts discovery and must never be passed to the Transcript Actor. There is no user override for this project default. A true value skips pinned posts, including ones that fall within the requested time window. Disclose that exclusion and do not claim all time-matching posts were covered; report an excluded-post count only if the Actor returns a verifiable count. Keep `resultsLimit` separate from the local `per_creator_limit`; never pass `per_creator_limit` as Actor input. When the live schema supports it, use `resultsLimit=50` as the project default. This default reflects the project owner's prior runtime observation of a per-Creator result/usage limit; the public schema describes a maximum result count but does not guarantee per-Creator semantics. Submit one username per run while scope behavior remains unverified. Preserve each run boundary, submitted account mapping, exact run status, all raw returned rows (including original `type` and `productType` values), and any explicit Dataset completeness evidence. Set `retrieval_complete` to `true` only with traceable host/Actor evidence that the Dataset was fully read; the helper checks only evidence-object shape and cannot authenticate its truth. Do not infer completeness from `SUCCEEDED`, a count below `resultsLimit`, an empty result, or no truncation marker. Missing pagination metadata or extra completeness flags do not block processing exact-Video records after retrieval, but do not claim a full time-window scan. If the run is `SUCCEEDED`, the Dataset has been fully read, and that Creator's raw returned row count is below `resultsLimit`, report in the user's language that the Actor-returned data was fully read and the configured result limit was not reached. This says only that the returned Dataset was read and the configured limit was not reached; it does not guarantee every post in the requested window was found. If the returned row count reaches the limit, say results may have been capped or truncated.
4. Run helper operation `select` with the exact Profile Posts field map and every per-run result. The project processing rule is exact and case-sensitive: only a row whose `type` value is the string `"Video"` and whose `url` is a usable Instagram post URL is a transcription candidate. This is the project owner's confirmed handling rule, not an enum guaranteed by the Actor schema; the public schema currently types `type` as a string without enum values. `productType` is not a gate. Do not use `isReel`, `productType`, URL shape, or field names to infer media type. Any missing, null, non-string, or other `type` value stays unresolved as unknown and is never sent to the Transcript Actor. Retain the row and report the actual type field presence/value. The Transcript Actor can process Reels and regular video posts, so do not distinguish them or require Reel classification. The helper reports `returned_raw_rows` as the Dataset row count only when a run maps to one Creator; it is `null` if multiple creators share a run and cannot be apportioned. `discovered_returned_in_window` counts attributable raw rows with usable identity/URL and timestamps inside the requested window, including duplicates, regardless of media type. `type_video_candidates` counts deduplicated exact-Video rows with usable URLs before the processing cap. `unknown_media_type` counts attributable in-window raw rows whose type is missing, null, non-string, or not exactly `"Video"`, including duplicate rows and regardless of URL usability. This count reports unknown type rows, not interface errors; it does not by itself make the run `partial_interface_error`. A confirmed `"Video"` row without a usable URL is a structural interface error. Also report selected and actually processed counts, and each discovery run status. Preserve unresolved identity/interface rows with actual evidence. Valid, attributable exact-Video rows may proceed even when pagination or extra completeness metadata is unavailable; preserve run status and returned rows without claiming a full scan. Do not send rows with unresolved identity, invalid required fields/URL, or unknown type. A missing discovery run means no rows were returned for that Creator in this attempt, while coverage and additional candidates remain unknown. Report unknown type values, unverified publication-time values, selected/processed videos, omitted candidates, failures, and partial/unknown coverage. Never describe `per_creator_limit` as a discovery cap or complete account scan.

Use the Profile Posts Actor's contracted post-publication field as the primary publication-time source. The current observed numeric values for Profile Posts `timestamp` are Unix seconds; set `timestamp_unit: "unix_seconds"` in `post_contract` only when the current type/unit evidence confirms it. Never infer a numeric unit from magnitude or a field name. The helper filters the UTC instant against its UTC window, then derives `published_at_local` and `published_at_utc` from that same instant; display the local value with its `display_timezone` and do not relabel UTC as local time. For an unknown or unparseable type, unit, or timezone, preserve the raw value and report `timestamp_unverified`; do not guess window membership or publication date. The Transcript Actor's string `timestamp` is run time, not publication time. Its numeric `createTime` is a post-time cross-check only after URL/ID reconciliation confirms the same record; the Profile Posts time remains authoritative.
5. Build Transcript batches only from selected, deduplicated URLs and only within a batch size supported by the current Transcript schema/account. Split internally when supported. Use the host's currently exposed tool and live argument schema; do not require `callOptions`, `maxTotalChargeUsd`, `maxItems`, or run-options readback. Do not hide these calls. Do not automatically retry, create replacement runs, expand the user's request, or interrupt discovery/transcription merely to ask about a budget. If a functional interface, authorization, batch, or read failure prevents remaining work, retain usable results and mark affected videos/account coverage partial.
6. Call helper operation `reconcile` only after at least one exact-Video candidate was selected, submitted to the Transcript Actor, and a result set/run status is available. If selection yields no exact-Video candidates (including when all returned media types are unknown), do not call the Transcript Actor or `reconcile`; the helper also rejects an empty submitted-candidate list. For a valid Transcript run, pass the complete submitted-candidate set and every returned transcript row to `reconcile`. It requires the exact `Video` mapping in `post_contract`, canonicalizes verified Instagram URL variants, uses only verified URL/code/pk fields, supports verified stable-ID fallback, and returns a status for every submitted post even when no row returned. It distinguishes explicit empty text, missing text, malformed rows, segment-only results, Actor errors, duplicate rows, identity conflicts, unmatched rows, and run/Dataset pending states. Never match by row order.
7. If the host exposes Dataset pagination and a reliable completion signal, read all pages and preserve that signal as completeness evidence. If it does not, do not claim discovery completeness. A `reconcile` success means a returned transcript row matched its submitted post; it does not establish that discovery or transcript Dataset reading was complete. Incomplete or unknown discovery runs may still supply validated exact-Video rows for transcription; preserve their status and keep report coverage partial/unknown. If a transcript run or Dataset is incomplete, preserve affected transcript results as pending/provisional. Preserve confidently matched partial results.

Keep Dataset total rows (`dataset_total`), rows the plugin/tool read (`result_count` or `returned_items`), and model-visible, parseable rows (`model_visible_rows`, normally the number of records actually present in `posts`) separate. In original OpenClaw Apify plugin v0.5.3, `resultCount` describes rows read into plugin memory, not rows visible to the model; do not use it as either the visible-row count or Dataset total.

Inspect the actual tool payload before `select`. An observed `[…truncated]` marker, OpenClaw `... N more characters truncated` marker, incomplete JSON, `truncated: true`, `hasMore: true`, evidence that a source row count exceeds model-visible rows, or an unread page means retrieval is explicitly incomplete: set discovery `retrieval_complete` to `false` and preserve the source and detail in `retrieval_complete_evidence`. `truncation_markers` is the list of non-empty marker strings actually observed; any non-empty valid list means incomplete, including marker text not previously known. With no incomplete signal but no reliable proof of the end, use `null`/unknown. In particular, the original OpenClaw Apify plugin v0.5.3 was observed to serialize Dataset output with a 50,000-character cap and no pagination or structured truncation signal; for that version, `SUCCEEDED`, `allDone`, `resultCount`, one successful `collect`, and `resultCount` below the Actor's `resultsLimit` do not prove complete retrieval.

For a paginated tool, continue from each `nextOffset` until a reliable terminal signal. `nextOffset` must be `null` or a non-negative integer (a Boolean is invalid); reject malformed values as unverified evidence. The current evidence contract recognizes normalized `next_offset_kind` values `exact` and `speculative` (trim surrounding whitespace and compare case-insensitively); unknown values cannot establish completeness. `speculative` permits probing but does not establish that another page exists. `next_offset_kind` describes the cursor from the page represented by that evidence; when claiming all pages were read, it must describe the terminal page. If an earlier page's speculative cursor is retained for audit, put it in a separate `prior_page_cursors` field rather than reusing the terminal page field; the helper preserves this field but does not validate its contents. A terminal page with `has_more: false` conflicts if `next_offset` is non-null or `next_offset_kind` is `speculative`; a matching `dataset_total` cannot override that conflict. Mark `retrieval_completeness_conflict` and never report `retrieval_complete: true` for it. The discovery field `retrieval_complete` is tri-state: `false` means positively incomplete, while `null` or omission means unknown. An explicit `false` remains `false` when evidence is insufficient; if it conflicts with otherwise reliable complete evidence, keep `false` and set `retrieval_completeness_conflict: true`. Set it to `true` only when JSON is complete and either `dataset_total` equals `model_visible_rows`, or all pages were actually read (`all_pages_read: true`) and the terminal page says `has_more: false`; there must be no truncation, cursor conflict, or count contradiction. A claimed `true` that conflicts with an observed incomplete signal stays fail-closed (`false` for explicit truncation, otherwise `null`) and sets the conflict flag. The normalized `retrieval_complete_evidence` object must include non-empty `source` and `detail`, and may also include `dataset_total`, `result_count`, `returned_items`, `model_visible_rows`, `truncated`, `truncation_marker_detected`, `truncation_markers`, `json_complete`, `has_more`, `all_pages_read`, `next_offset`, and `next_offset_kind`. The helper validates the current page's cursor types/consistency and count consistency; it preserves but does not validate historical `prior_page_cursors`, and cannot authenticate the source or truth of the host's evidence. This normalization reflects the repository evidence contract; it does not confirm a live plugin enum. Discovery `retrieval_complete` is distinct from Transcript `dataset_complete` and must not be copied between them.

A separately tested isolated plugin copy exposed pagination fields and read a Dataset 24/24 without a second truncation in the tested model response. That copy is not the official installed v0.5.3 plugin; do not describe the original plugin as having those capabilities or direct users to install the isolated copy.

### Analysis and report

Use a natural equivalent of “Creator Video Insights” in the user's language as the report title. Analyze only Actor-returned transcript text. Keep that text distinct from generated summaries and analysis. Do not infer visuals, editing, product display, creator intent, audience reaction, or causation. Link each insight to its post URL and quote a short supporting transcript excerpt where useful.

**Daily Scan:** show the exact UTC window and timezone. For each Creator label `returned_raw_rows` as raw Dataset rows read, `discovered_returned_in_window` as attributable in-window raw rows with usable URLs (duplicates included), `unknown_media_type` as attributable in-window unknown-type raw rows (duplicates included; URL not required), and `type_video_candidates` as deduplicated usable-URL rows with exact `type == "Video"` before the local limit. Then show selected/processed videos, those omitted by the user limit, each discovery run status, and coverage/failure status. Because `"skipPinnedPosts": true` excludes pinned posts, do not label returned rows as all posts in the time window; give an excluded count only if the Actor provides a verifiable count. For each selected video show its URL, `published_at_local` with the explicit `display_timezone`, the UTC instant if useful, transcript status and, when available, transcript highlights, opening hook, core point, speaking structure, delivery and closing/CTA. If the helper marks the source timestamp `timestamp_unverified`, retain its raw value and say publication time could not be verified; do not guess. Give a concise interpretation based on transcript evidence. Preserve post details when transcription fails.

**Weekly Review:** show the same coverage accounting. Summarize recurring topics, hooks, speaking structures and CTAs only from successfully matched transcripts in this report. Link every pattern to representative posts and transcript evidence. Call out small samples and incomplete coverage; do not describe them as long-term trends.

Keep the default report readable: show transcript highlights and source-linked analysis rather than every full transcript inline. If asked to expand a video, provide its actual returned transcript separately, link its post, and label the transcript as Actor-returned text.

Never treat missing metrics as zero. Engagement counts, if returned, are optional collection-time context only; they must not replace or lead the report.

At the end, include a short copyable request containing the accounts, report mode, exact time range and per-creator limit. Do not imply that the Skill will remember settings or prior transcripts in another session.

### Privacy and safety

Process only user-specified public accounts. Respect Instagram, Apify and host access controls; do not bypass login, rate limits, or restrictions. Never request or reveal tokens, cookies, session IDs, passwords, or authorization headers. Persist the account list and per-creator limit only after explicit consent and only through supported host storage. Never persist transcript libraries or report history.

## Other host setup

Use only the branch for a host that is explicitly identified. Skill installation and Apify connection/authorization are separate. Do not install plugins, change host configuration, start OAuth, or use another Actor, direct HTTP/API, shell, token, cookie, or session value to bypass missing tools or authorization. At first use, if the host does not expose a usable Apify tool, confirms authorization is missing, or readiness cannot be established, stop before starting an Actor and explain that no Actor was started and no results were received. Reply in the user's language.

### ChatGPT

When ChatGPT is explicitly identified and Apify readiness is missing or uncertain, stop first and provide these setup steps; do not require the user to invoke the Skill with `@` to receive them:

1. If the user has no Apify account, direct them to [Apify Console registration](https://console.apify.com/sign-up).
2. Open **Plugins → + → Add custom MCP server**. Set **Name** to `Apify MCP` and **Server URL** to `https://mcp.apify.com`.
3. Set **Authentication** to **OAuth**.
4. Read the risk notice, confirm its checkbox, then choose **Create as a plugin**. Follow ChatGPT's prompts to sign in to Apify and approve access.
5. The project has observed that regular chat may not reliably invoke Skills; prefer a new ChatGPT Work mode chat for retrying. If continuing in the current chat, refresh available tools first. This is a project test observation, not a guarantee about every account or workspace.

The MCP connection and Skill installation are separate, and one Apify MCP connection can serve multiple Skills. Never request an API key or other credentials in chat. If the custom-server entry is unavailable, point the user to the [OpenAI custom MCP guide](https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt) and advise checking account, workspace, or administrator permissions. See the [project ChatGPT guide](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/chatgpt.md#1-add-and-authorize-the-apify-mcp-connection) for complete setup details. Actual tool availability and permissions vary by account and workspace.

### Codex desktop and CLI

Installing the Skill and Apify plugin are separate. Install this Skill's full directory using the supported Codex route, then install the Apify plugin in the matching Codex surface and complete its browser OAuth flow. Desktop and CLI have different plugin menus; do not apply one surface's commands to the other. Start a new session and explicitly invoke `$instagram-creator-reels-insights`; continue only when the Skill and required Apify tools are available. For the exact routes, see the [project Codex guide](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/codex.md), [Apify Codex desktop guide](https://docs.apify.com/integrations/codex-app), and [Apify Codex CLI guide](https://docs.apify.com/integrations/codex-cli). Do not overwrite an existing Skill directory.

### Claude Web and Claude Desktop chat

Install and enable the trusted Skill through Claude's Skills interface, then add the official Apify Plugin/Connector and complete Apify's authorization flow. In a new chat, enable the connector and select this Skill with `/` if that selector is available, or name the Skill in the request. Workspace administrators may restrict Skill uploads or connectors. Claude Desktop chat uses account-level settings; do not apply Claude Code CLI commands to it. See the [project Claude guide](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/claude-web.md), [Apify Claude.ai guide](https://docs.apify.com/integrations/claude-ai), and [Anthropic remote MCP guide](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp).

### Claude Code CLI

Claude Code CLI is separate from Claude Desktop chat and remote code sessions. Install the Skill through supported account sync or in `~/.claude/skills/instagram-creator-reels-insights/`. Install the Apify plugin with Claude Code's CLI flow, authenticate the `plugin:apify:apify` MCP connection in `/mcp`, and complete browser authorization. Continue only when the Skill is available and the session exposes the required Apify tools. These steps apply to the CLI, not the Claude Desktop Code tab or remote sessions. See [Claude Code Skills](https://code.claude.com/docs/en/skills), the [Apify Claude Code CLI guide](https://docs.apify.com/integrations/claude-code-cli), and the [project Claude guide](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/claude-web.md).

### Manus

Manus uses its own Custom MCP connector flow. Add the hosted Apify MCP endpoint `https://mcp.apify.com` using the documented HTTP configuration, then complete the OAuth authorization when Manus prompts during a tool call. Separately import this Skill from its stable repository folder, enable it, and enable the Apify connector in the task. Continue only when the Skill is selectable and the current session exposes a usable Apify tool. Do not replace OAuth with an API token. Check account permissions and current platform documentation because interfaces and access may vary. See the [project Manus guide](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/manus.md), [Apify Manus guide](https://docs.apify.com/integrations/manus), and [Manus Skills guide](https://help.manus.im/en/articles/14753565-how-to-share-and-use-skills-in-manus).

### Unknown or other hosts

If the host or product surface is unclear, ask which host the user is using before giving menu paths or commands. Do not generalize OpenClaw, ChatGPT, MCP, Connector, plugin-store, or CLI instructions to another host. Use the matching platform guide when one exists; otherwise say that host-specific setup steps are not documented and point to that host's official setup documentation. Never claim the Skill can inspect host settings or determine whether a plugin is installed.
