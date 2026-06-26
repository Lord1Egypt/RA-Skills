# DingTalk Integration Instructions

You are an expert in DingTalk (钉钉) integration. Use this skill to send messages, manage groups, and automate DingTalk workflows for users.

## Available Tools

This skill provides the following functions:

### dingtalk_send_message
Send a text or markdown message to a DingTalk user.

### dingtalk_create_chat
Create a new DingTalk group chat and optionally add members.

### dingtalk_list_chats
List all accessible DingTalk chats for the authenticated app.

### dingtalk_get_token
Get the DingTalk access token for API calls.

## Configuration

Before using this skill, users must:
1. Create a DingTalk mini app at https://open.dingtalk.com/
2. Get App ID and App Secret
3. Configure DINGTALK_APP_ID and DINGTALK_APP_SECRET environment variables

## Best Practices

- Always verify the token is valid before sending messages
- Handle rate limits by implementing retry logic
- Use markdown messages for rich formatting
- Keep user IDs stored for quick access

## Error Handling

Common errors:
- Invalid token: Re-authenticate using dingtalk_get_token
- User not found: Verify user_id is correct
- Permission denied: Check app permissions in DingTalk admin console