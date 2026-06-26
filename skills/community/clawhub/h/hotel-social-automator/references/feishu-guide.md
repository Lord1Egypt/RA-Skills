# Feishu Platform Sending Guide

This document explains how to send card and image messages via Feishu platform.

## Prerequisites

Feishu sending depends on the `feishu-send` script, which should be installed at `/usr/local/bin/feishu-send`.

## Message Type Reference

| ID Prefix | Type | Description |
|-----------|------|-------------|
| `ou_` | User Open ID | User's unique identifier within the app |
| `oc_` | Group Chat ID | Group's unique identifier |

## Target ID Selection (Critical!)

**You must select the correct ID based on conversation type:**

- **For groups**: Use `conversation_label` or `group_subject` (e.g., `oc_xxx`)
- **For private chats**: Use `conversation_label` (e.g., `ou_xxx`)
- **DO NOT use** `sender_id`! That's the sender, not the recipient.

The `conversation_label` or `group_subject` from message metadata is the correct target ID.

## Feishu Card Format

Feishu uses Interactive Cards with the following JSON structure:

```json
{
  "config": {"wide_screen_mode": true},
  "header": {
    "title": {"tag": "plain_text", "content": "Card Title"},
    "template": "blue"
  },
  "elements": [
    {"tag": "div", "text": {"tag": "plain_text", "content": "First paragraph content"}},
    {"tag": "div", "text": {"tag": "plain_text", "content": "#tag1 #tag2"}}
  ]
}
```

### header.template Available Colors
- `blue` - Blue
- `green` - Green
- `red` - Red
- `yellow` - Yellow
- `grey` - Grey

## Sending Steps

### 1. Create Card JSON File

```bash
cat > /tmp/card.json << 'EOF'
{
  "config": {"wide_screen_mode": true},
  "header": {"title": {"tag": "plain_text", "content": "Card Title"}, "template": "blue"},
  "elements": [
    {"tag": "div", "text": {"tag": "plain_text", "content": "First paragraph content"}},
    {"tag": "div", "text": {"tag": "plain_text", "content": "#tag1 #tag2"}}
  ]
}
EOF
```

### 2. Send Card

```bash
# Group chat
feishu-send card "oc_demo_group_id" /tmp/card.json

# Private chat
feishu-send card "ou_demo_user_id" /tmp/card.json
```

### 3. Send Images

```bash
feishu-send image "oc_demo_group_id" /root/.openclaw/workspace/image1.png
feishu-send image "oc_demo_group_id" /root/.openclaw/workspace/image2.png
feishu-send image "oc_demo_group_id" /root/.openclaw/workspace/image3.png
```

## Key Rules

1. **Groups must use group ID**! Not the user ID of the message sender!
2. Card titles should use the **actual title**, do not add "Draft" prefix
3. **No prefixes for content**: Display copy directly, don't add "Copy:"; display tags directly, don't add "Tags:"
4. Images must be saved to `/root/.openclaw/workspace/` directory
5. feishu-send will automatically read credentials from OpenClaw config
6. Clean up temporary files after sending images

## Common Issues

### Message Sent to Private Chat Instead of Group

**Cause**: Used `sender_id` instead of `conversation_label`

**Solution**: Check message metadata and use the correct `conversation_label` or `group_subject`

### Image Sending Failed

**Cause**: Image path incorrect or file doesn't exist

**Solution**: Confirm image is in `/root/.openclaw/workspace/` directory and use absolute path

## Complete Example

```bash
# 1. Create card
cat > /tmp/card.json << 'EOF'
{
  "config": {"wide_screen_mode": true},
  "header": {"title": {"tag": "plain_text", "content": "Reception Moments"}, "template": "blue"},
  "elements": [
    {"tag": "div", "text": {"tag": "plain_text", "content": "In the softly lit reception, smiles and greetings are all genuine."}},
    {"tag": "div", "text": {"tag": "plain_text", "content": "#tko #hoteldaily #receptionservice"}}
  ]
}
EOF

# 2. Send card (assuming group chat)
feishu-send card "oc_demo_group_id" /tmp/card.json

# 3. Send images
feishu-send image "oc_demo_group_id" /root/.openclaw/workspace/post1.png
feishu-send image "oc_demo_group_id" /root/.openclaw/workspace/post2.png
feishu-send image "oc_demo_group_id" /root/.openclaw/workspace/post3.png

# 4. Clean up
rm /tmp/card.json
```
