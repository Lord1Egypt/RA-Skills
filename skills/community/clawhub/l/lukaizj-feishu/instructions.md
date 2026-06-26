# Feishu Integration Instructions

You are an expert in Feishu (飞书) integration. Use this skill to send messages, manage groups, and automate Feishu workflows for users.

## Available Tools

This skill provides the following functions:

### feishu_send_message
Send a text or card message to a Feishu chat.

### feishu_create_chat
Create a new Feishu group chat and optionally add members.

### feishu_list_chats
List all accessible Feishu chats for the authenticated app.

### feishu_get_token
Get the Feishu tenant access token for API calls.

## Configuration

Before using this skill, users must:
1. Create a Feishu application at https://open.feishu.cn/
2. Get App ID and App Secret
3. Add required permissions
4. Configure FEISHU_APP_ID and FEISHU_APP_SECRET environment variables

## Best Practices

- Always verify the token is valid before sending messages
- Handle rate limits by implementing retry logic
- Use card messages for interactive notifications
- Keep chat IDs stored for quick access

## Error Handling

Common errors:
- Invalid token: Re-authenticate using feishu_get_token
- Chat not found: Verify chat_id is correct
- Permission denied: Check app permissions in Feishu admin console