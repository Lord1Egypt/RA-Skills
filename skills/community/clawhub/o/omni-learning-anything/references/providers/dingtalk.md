# 钉钉 / DingTalk

Prefer an already authorized writable official API connector. See [onboarding](../onboarding.md) for focused setup dialogue. Otherwise the supported direct route is the official DingTalk Workspace CLI `dws`; the skill does not invent an undocumented REST interface or request arbitrary app keys. Use `OMNI connect --platform dingtalk --location OFFICIAL_FOLDER_LINK --save-as NAME` for a new course. It parses the folder link, verifies the current identity and folder, and pins `account_id`/`cli_profile` to organization:user. Preserve that `--profile` on every command. Before publication the adapter rejects a changed organization/account. Confirm existing authorized login and a course `folder_id` or `workspace_id`.

Install/login through official documented channels when needed. Enterprise/admin authorization may be required; do not claim a personal desktop login grants CLI scopes. OAuth success can still be rejected by the organization CLI data-access check. Have the administrator enable and save CLI access for the current member in the same organization, then log in again; `dws doctor --json` can distinguish auth and network failures. Do not repeatedly reissue device codes before the actual setting changes. Do not materialize tokens in the course or scheduler prompt.

The adapter invokes argument arrays without a shell:

```sh
dws doc import --file /course/sources/Day01.docx --folder CONFIRMED_FOLDER --name LESSON_TITLE --format json
dws doc import get --task-id RETURNED_TASK --folder CONFIRMED_FOLDER --format json
dws doc info --node RETURNED_NODE --format json
dws doc read --node RETURNED_NODE --content-format markdown --format json
```

Import returns node/document URL or an async task. Save it immediately. On resume carry the original `--folder` or `--workspace`; current dws may return a completed task with `verified=false` when placement was not checked. Keep that document/task pending and query the same task with its target before acceptance. Initial import includes up to roughly five minutes of conversion polling; the adapter allows ten minutes including upload, while normal read/query commands retain a one-minute limit. The structured `timed_out=true`, `status=processing`, `taskId` result is recoverable even with `success=false`. Reject `fallback=upload`/`converted=false`, which denotes a file object rather than an editable document. Metadata must identify ALIDOC/adoc; readback checks lesson text, source URLs and a remote image. CLI output that lacks these fields remains unverified rather than guessing success. Version changes require checking the current leaf command schema and updating the adapter contract.

On timeout with no saved node/task, inspect the target folder/history before another import. UI fallback imports embedded DOCX, then verifies the actual editable document and records a host receipt. Do not send test documents to chats or groups unless separately instructed.

Official sources checked 2026-10-14:
- https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli
- https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/blob/main/skills/mono/references/products/doc/doc-import.md
- https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/blob/main/skills/mono/references/products/doc.md

Acceptance checked against official dws v1.0.64 on 2026-10-18: device login, organization CLI-access enforcement and a folder in the current user’s personal document space succeeded. DOCX import failed during OSS upload; folder readback was empty. No editable-document receipt or content pass was recorded. API connectivity alone does not prove upload-host connectivity. Do not copy raw CLI errors into shared logs: an upload failure can contain a signed storage URL.

Current contract reference: https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/blob/v1.0.64/internal/helpers/import_flow.go

2026-10-25 acceptance supersedes the earlier upload blocker for the tested host: official dws v1.0.65, checksum-verified release, plan + Day01 DOCX import succeeded in the same private folder. Native image/text/source-list inspection, exact semantic href readback, fixed organization:user, repeat receipt-byte stability and exactly two folder documents passed. No live schedule was created. Current Markdown includes escaped punctuation and optional image titles; readback normalization handles them without accepting plain-text source URLs as hyperlinks.
