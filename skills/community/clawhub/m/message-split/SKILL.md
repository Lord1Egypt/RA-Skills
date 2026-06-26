---
name: message-split
description: "长消息自动拆分 skill。当回复内容超过渠道限制时，自动将消息拆分为多条有序发送，避免截断或丢消息。Auto-split long messages into smaller chunks before sending, with sequence markers."
---

# Message Split Skill

## Problem

Many messaging channels (Feishu, Telegram, etc.) have a per-message character limit (~4000 chars for Feishu). When a response exceeds this limit, it either gets truncated or silently fails, leaving the user with no feedback.

## Solution

Before sending any message, check its length and split if necessary.

## Usage

```python
def send_long_message(text, channel="{active_channel}"):
    """
    Send a message, splitting it into multiple chunks if it exceeds the length limit.
    
    Args:
        text: The message text to send
        channel: Target channel (feishu/telegram/discord/whatsapp/signal/imessage/openclaw-weixin)
    
    Returns:
        Number of chunks sent
    """
    MAX_LEN = 3600  # Feishu limit with margin
    CHUNK_HEADER = "[{i}/{total}]\n"
    
    if len(text) <= MAX_LEN:
        message(action="send", channel=channel, message=text)
        return 1
    
    chunks = split_text(text, MAX_LEN)
    total = len(chunks)
    
    for i, chunk in enumerate(chunks, 1):
        header = f"[{i}/{total}]\n" if total > 1 else ""
        message(action="send", channel=channel, message=header + chunk)
    
    return total


def split_text(text, max_len):
    """
    Split text into chunks of at most max_len characters.
    Attempts to split at sentence boundaries or line breaks for readability.
    """
    import re
    
    # Try to split at sentence-ending punctuation first
    sentence_split = re.split(r'(?<=[。！？.!?])\s+', text)
    
    chunks = []
    current = ""
    
    for sentence in sentence_split:
        if len(current) + len(sentence) + 1 <= max_len:
            current += (" " + sentence if current else sentence)
        else:
            if current:
                chunks.append(current)
            # If single sentence exceeds limit, split by words/characters
            if len(sentence) > max_len:
                for i in range(0, len(sentence), max_len - 100):
                    chunks.append(sentence[i:i + max_len - 100])
                current = ""
            else:
                current = sentence
    
    if current:
        chunks.append(current)
    
    return chunks
```

## Channel Limits Reference

| Channel | Max chars (approx) | Notes |
|---------|-------------------|-------|
| Feishu | 4000 | Hard limit |
| Telegram | 4096 | |
| Discord | 2000 | Embed limit 6000 |
| WhatsApp | 65000 | But relayed messages get truncated |
| Signal | 700 | Very low |
| iMessage | ~4000 | Via macOS relay |

## Notes

- Always use `MAX_LEN = 3600` as a safe default (leaves room for header)
- If channel is unknown, default to feishu behavior
- Splitting is done on word/sentence boundaries when possible to preserve readability
- Sequence headers `[{i}/{total}]` are only added when `total > 1`
