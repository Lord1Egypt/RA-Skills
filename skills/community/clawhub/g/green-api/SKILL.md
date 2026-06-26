---
name: green-api
version: 1.0.0
description: Send and receive WhatsApp messages, manage groups, contacts, and instances via GREEN-API MCP gateway.
homepage: https://green-api.com
metadata: { "openclaw": { "emoji": "💬" } }
---

# GREEN-API WhatsApp Skill

Use this skill when the user wants to send or receive WhatsApp messages, manage contacts, groups, or WhatsApp instances via GREEN-API.

## Connection

Before using any tools, connect an instance with `whatsapp_connect` by providing `instance_id` and `api_token` (from console.green-api.com). This validates credentials and stores them for the session.

Call `whatsapp_disconnect` when done.

## Chat ID format

- **Personal chats:** `79876543210@c.us` (phone number in international format + `@c.us`)
- **Group chats:** `120363XXX@g.us` or `79876543210-1581234048@g.us`

## Tools

### Session

| Tool | Description |
|---|---|
| `whatsapp_connect` | Connect instance (required first). Params: `instance_id`, `api_token`, optional `api_url` |
| `whatsapp_disconnect` | Disconnect instance and clear credentials |

### Messaging

| Tool | Description |
|---|---|
| `whatsapp_send_message` | Send text message. Params: `instance_id`, `chat_id`, `message`, optional `quoted_message_id`, `link_preview` |
| `whatsapp_send_file` | Send file by URL. Params: `instance_id`, `chat_id`, `url`, optional `file_name`, `caption` |
| `whatsapp_upload_file` | Upload file to GREEN-API storage, returns URL. Params: `instance_id`, `file_base64`, `filename`. Use returned URL with `whatsapp_send_file` |
| `whatsapp_send_file_by_upload` | Send file directly via base64 (no separate upload step). Params: `instance_id`, `chat_id`, `file_base64`, `filename`, optional `caption` |
| `whatsapp_send_location` | Send location. Params: `instance_id`, `chat_id`, `latitude`, `longitude`, optional `name`, `address` |
| `whatsapp_send_contact` | Send contact card. Params: `instance_id`, `chat_id`, `phone_number`, optional `first_name`, `last_name`, `company` |
| `whatsapp_send_poll` | Send poll. Params: `instance_id`, `chat_id`, `message` (question), `options` (string array, 2–12), optional `multiple_answers` |
| `whatsapp_forward_messages` | Forward messages between chats. Params: `instance_id`, `chat_id` (destination), `chat_id_from` (source), `messages` (ID array) |
| `whatsapp_edit_message` | Edit a sent message. Params: `instance_id`, `chat_id`, `id_message`, `message` (new text) |
| `whatsapp_delete_message` | Delete a message. Params: `instance_id`, `chat_id`, `id_message` |

### Instance management

| Tool | Description |
|---|---|
| `whatsapp_get_state` | Get instance state: `authorized`, `notAuthorized`, `blocked`, `sleepMode`, `starting`, `yellowCard` |
| `whatsapp_get_settings` | Get instance settings (webhooks, delays, flags) |
| `whatsapp_set_settings` | Update instance settings. Params: optional `webhook_url`, `webhook_url_token`, `outgoing_webhook`, `incoming_webhook`, `state_webhook`, `mark_incoming_messages_readed`, `delay_message`, etc. |
| `whatsapp_get_qr` | Get QR code for authorization (instance must be unauthorized) |
| `whatsapp_get_authorization_code` | Get auth code by phone number (alternative to QR). Params: `instance_id`, `phone_number` |
| `whatsapp_get_wa_settings` | Get WhatsApp account info (avatar, phone, state, device ID) |
| `whatsapp_reboot` | Reboot instance |
| `whatsapp_logout` | Log out instance (required before re-authorizing) |

### Contacts & history

| Tool | Description |
|---|---|
| `whatsapp_check_whatsapp` | Check if a phone number has WhatsApp. Params: `instance_id`, `phone_number` |
| `whatsapp_get_contacts` | Get all contacts |
| `whatsapp_get_contact_info` | Get info about a contact or group. Params: `instance_id`, `chat_id` |
| `whatsapp_get_contact_avatar` | Get avatar of contact or group. Params: `instance_id`, `chat_id` |
| `whatsapp_get_chat_history` | Get chat message history. Params: `instance_id`, `chat_id`, optional `count` (default 100) |
| `whatsapp_get_message` | Get a specific message. Params: `instance_id`, `chat_id`, `id_message` |
| `whatsapp_last_incoming_messages` | Get recent incoming messages. Params: `instance_id`, optional `minutes` (default 1440) |
| `whatsapp_last_outgoing_messages` | Get recent outgoing messages. Params: `instance_id`, optional `minutes` (default 1440) |
| `whatsapp_read_chat` | Mark messages as read. Params: `instance_id`, `chat_id`, optional `id_message` |

### Notifications (manual polling)

| Tool | Description |
|---|---|
| `whatsapp_receive_notification` | Get one notification from the queue |
| `whatsapp_delete_notification` | Acknowledge/delete a notification. Params: `instance_id`, `receipt_id` |

### Groups

| Tool | Description |
|---|---|
| `whatsapp_create_group` | Create a group. Params: `instance_id`, `group_name`, `chat_ids` (participant array) |
| `whatsapp_get_group_data` | Get group info (members, name, link). Params: `instance_id`, `group_id` |
| `whatsapp_add_group_participant` | Add member. Params: `instance_id`, `group_id`, `participant_chat_id` |
| `whatsapp_remove_group_participant` | Remove member. Params: `instance_id`, `group_id`, `participant_chat_id` |
| `whatsapp_set_group_admin` | Promote member to admin. Params: `instance_id`, `group_id`, `participant_chat_id` |
| `whatsapp_remove_group_admin` | Demote admin. Params: `instance_id`, `group_id`, `participant_chat_id` |
| `whatsapp_leave_group` | Leave a group. Params: `instance_id`, `group_id` |

### Partner API (instance provisioning)

These require a `partner_token` from the GREEN-API partner dashboard.

| Tool | Description |
|---|---|
| `whatsapp_create_instance` | Create a new instance |
| `whatsapp_delete_instance` | Delete an instance. Params: `partner_token`, `instance_id` |
| `whatsapp_get_instances` | List all partner instances |

## Resources

- `whatsapp://instance/{id}/state` — read current instance authorization state
- `whatsapp://instance/{id}/settings` — read instance settings

## Prompts

- `whatsapp_customer_support` — system prompt template for a customer support agent. Args: `instance_id`, `language`
- `whatsapp_broadcast` — template for planning and executing broadcast messaging. Args: `instance_id`, `message_template`

## Important notes

- Always `whatsapp_connect` before calling any other tool.
- Use `whatsapp_check_whatsapp` to verify a phone number has WhatsApp before sending.
- For broadcasts, add delays between messages to avoid rate limiting.
- File uploads use base64 encoding. Max file size: 100 MB.
- Poll options must be unique, 2–12 items, max 100 chars each.
- Message quoting only works within the same chat.
