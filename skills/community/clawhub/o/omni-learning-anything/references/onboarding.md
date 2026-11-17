# Guided first connection

The agent does the setup work; the learner chooses the destination and reviews official authorization. Default cloud delivery uses official APIs, directly or through an official CLI/authorized API connector. Browser import is an explicitly accepted fallback. An installed skill alone cannot grant access.

## Normal conversation

Understand the study request before asking setup questions: use [intent](intent.md) for broad/ambiguous goals, reuse already supplied information and combine routine missing settings. Check only the selected route with [readiness](readiness.md); no token, ID extraction or diagnostic editing is assigned to the learner.

1. Reuse the course brief. If the destination is missing, ask once: “计划和每日材料希望保存到哪里？” Once selected, ask only for that platform's course parent-page/folder link, or Obsidian Vault path and course subdirectory. Explain how to create/copy a link if requested. Do not collect credentials for every supported platform.
2. Inspect the existing writable API connector/official CLI and identity. Reuse adequate authorization. Otherwise the agent installs/checks the official tool, initiates login and shows the official URL, code and permission explanation (plus Feishu QR). The learner signs in, chooses the correct account/workspace/organization and grants access on that official page. Do not request passwords or token values in chat.
3. Agent completes polling, verifies identity and the selected location, optionally saves a named metadata connection, and creates the actual course plan. Ask a further question only for a concrete missing permission, invalid location or organizational restriction. Report the verified plan link; plan approval is still required before daily scheduling.

Two or three short connection exchanges is the normal target, not a guaranteed upper bound. App/administrator approvals, missing workspace membership or a locked keychain may require additional action. Explain the next specific action instead of repeatedly issuing login codes. Nothing changes platform/account merely because the user has not replied.

Show an authorization link's actual validity period when returned by the official tool. An expired code restarts only that authorization step; reuse completed app setup, profile and confirmed destination. After polling finishes, inspect official status/doctor before issuing another code. Distinguish expiry, missing organization/member permission, scope mismatch, network failure and locked keychain. Follow the exact selected provider's correction; never ask for blanket permissions or change organizations to make a check pass. Do not infer successful authorization from the learner's confirmation alone.

Example: user “保存到飞书，这个课程文件夹：<link>。” Agent “我会检查现有授权；如需授权，请在官方页面选择你自己的组织并核对文档权限。” User completes it. Agent runs connection checks, publishes and checks the plan, then returns the link for approval. Users do not need to find object IDs, write config files or paste API keys into the conversation.

## Agent commands

Resolve `omni_learning.py` from this installed bundle. `OMNI` below denotes `python /installed/omni-learning-anything/scripts/omni_learning.py`; these commands are run by the agent, not assigned as learner homework.

```sh
OMNI connect --platform notion --location 'https://www.notion.so/CONFIRMED_PAGE_ID' --save-as personal-notion
OMNI connect --platform feishu --location 'https://my.feishu.cn/drive/folder/CONFIRMED_FOLDER' --save-as personal-feishu
OMNI connect --platform obsidian --location '/confirmed/Vault' --subdir 'Omni Learning/Topic' --save-as local-notes
OMNI connect --platform dingtalk --location 'https://alidocs.dingtalk.com/i/nodes/CONFIRMED_FOLDER' --save-as personal-dingtalk
OMNI tencent-auth login --name personal-tencent
OMNI connect --platform tencent --location 'https://docs.qq.com/desktop/' --auth-profile personal-tencent --save-as personal-tencent
OMNI connection-list
OMNI connect --connection personal-feishu
OMNI connection-show --name personal-feishu
```

Names use lowercase letters, digits, hyphens or underscores and start with a letter. Choose a new name for another account/location. For Notion multiple workspaces supply `--workspace-id` using the confirmed official CLI workspace listing; Feishu named app configurations use `--cli-profile`; DingTalk fixes the organization:user profile; Tencent uses `--auth-profile` for a private OS keyring authorization and pins the returned user ID. Preserve these selections during login and API calls. Never globally switch defaults as a shortcut. `connection-show` reads saved metadata; reuse with `connect --connection` checks live access again. Cloud identifiers are extracted from official HTTPS links; Feishu needs a drive folder, not a Wiki/document link. Public Notion links still require API access.

`connect` returns `ready`, or `stage` + `next_action` + selected-platform `agent_argv`/`agent_command`/`guide`. Run suggested commands only after reading that provider's current official help. Prefer `agent_argv` for execution; it retains the selected Feishu profile. Configuration creation uses `--name`, while user login uses `--profile`. Handle install, configuration, authorization and destination stages separately; an authorization error is not evidence the learner chose another platform. For missing scopes use the exact documented permission and least sufficient grant, not “all”.

A successful result contains a `delivery` object. Copy it into the new intake `config.json` before `init`; the course stores a snapshot, not a live profile reference. Profiles live outside courses under `~/.config/omni-learning-anything/connections/`, owner-only, containing destination/account/profile metadata and no secret. Do not publish profile files or private account summaries. A saved connection cannot silently replace another account/location.

`ready: true` means read-only identity/location checks passed. Listing a folder does not prove write/import permission. Only actual `publish`, provider readback and document inspection establish plan/lesson delivery. Never edit an approved course destination or erase pending receipts to retry elsewhere.

## Platform setup

- [Notion](providers/notion.md): official `ntn` login, full workspace membership, selected parent page. Agent polls after the learner confirms login. OS keychain is the default; no automatic plaintext token fallback.
- [Feishu](providers/feishu.md): official `lark-cli` application setup if absent, then explicit user authorization for the needed docs/drive operations. These may be separate official steps. Agent shows exact links and generated QR codes; it completes device polling after the user confirms. Never substitute bot identity or international Lark.
- [Obsidian](providers/obsidian.md): local existing Vault, no cloud account/key; agent checks path and protects existing notes. Official Obsidian CLI may help open notes when available; local files remain the publisher's route.
- [Tencent Docs](providers/tencent.md): official application/API access and OAuth are required when no writable API connector exists; guide through that platform's actual prerequisites. The default new route uses official public OAuth with PKCE and a loopback callback, followed by MCP API import/export; no hosted OAuth service or manual key exchange is required. Agent initiates login, user reviews the account/document permissions, then the agent checks identity/location. Legacy application API credentials remain supported.
- [DingTalk](providers/dingtalk.md): official `dws` device login and organization CLI access for the current member. Explain administrative prerequisites only when returned by the platform. Agent runs current command help/doctor and finishes authorization.

For API-key alternatives, provide the selected platform's official instructions and offer to configure a private host credential loader within existing authorization. Never tell the learner to send a secret in chat. If the host cannot safely store/load credentials, report that blocker and preserve the course.

## Scheduling and recovery

Daily runs need the same official binaries, private credential context and confirmed account/location. Test that the actual scheduler host can access them; an interactive desktop keychain can be unavailable to a background host. Do not promise unattended delivery based on browser login or a successful foreground command. Keep pending work and resume the same page/task after reauthorization. For account changes start an explicitly approved course version. See [delivery recovery](delivery.md#recovery).
