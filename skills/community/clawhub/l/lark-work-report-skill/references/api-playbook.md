# API Playbook (Lark MCP, Reporting Only)

## 1) Find default work group

Interface: `im_v1_chat_list` (`useUAT=true`)

Filter rule:
- exact name match: `Codex工作群`

Fallback:
- if exact match missing, collect candidate groups with names containing `Codex` or `工作群`, then ask user to confirm.

## 2) Send report message

Interface: `im_v1_message_create` (`useUAT=true`)

Recommended args:
- `receive_id_type=chat_id`
- `msg_type=text`
- `content={"text":"..."}`

## 3) Preflight channel check (before task starts)

Recommended sequence:
- find group by `im_v1_chat_list`
- if needed create group by `im_v1_chat_create`
- send one test message by `im_v1_message_create`
- confirm in CLI that the channel is correct, then start task

## 4) Create default group if missing

Interface: `im_v1_chat_create` (`useUAT=true`)

Recommended creation:
- private group
- name: `Codex工作群`
- include the confirmed user identity

## 5) Resolve user ID when identity is unclear

Interface: `contact_v3_user_batchGetId` (`useUAT=true`)

Lookup inputs:
- email or mobile (with country code)
