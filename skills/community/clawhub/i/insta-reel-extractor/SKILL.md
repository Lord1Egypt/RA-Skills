---
name: instagram-reels-monitor
description: Monitor Instagram DMs for reels. Use when you need to check Instagram DMs for new unread messages containing reels, click them, extract the reel link, and append to an instagram_reels.csv file.
---

# Instagram Reels Monitor

This skill monitors an already open Instagram Direct Messages tab for new messages containing reels and saves them to a CSV file.

## Requirements
- An active browser session with a tab open to `https://www.instagram.com/direct/inbox/`.
- The user must have the OpenClaw browser relay attached to that tab.

## Workflow

1. Use the `browser` tool with `action: tabs` and `profile: chrome` to find the `targetId` for the Instagram Messages tab.
2. Use the `browser` tool with `action: act`, `kind: evaluate` to run a script that checks for new, unread messages in the DM list.
3. If an unread message is found, click the conversation to open it.
4. Once the conversation is open, use `browser` `action: act`, `kind: evaluate` to extract the `href` of any link containing `/reel/` or `/p/` (if it's a video/reel).
5. Extract the Instagram user ID of the sender.
6. Append the data to `instagram_reels.csv` in the format `userid,reel_link`.
7. Return to the main inbox view (if necessary) to check for more messages.

## Example Scripts

### Extract Reel Links from an Open Conversation
```javascript
() => {
    const links = Array.from(document.querySelectorAll('a'));
    return links.filter(a => a.href.includes('/reel/')).map(a => a.href);
}
```

### List DM Conversations
```javascript
() => {
    const buttons = Array.from(document.querySelectorAll('div[role="button"]'));
    return buttons.map(b => b.innerText.replace(/\n/g, ' '));
}
```