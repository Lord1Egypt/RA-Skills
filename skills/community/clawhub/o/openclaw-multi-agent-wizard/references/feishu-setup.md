# Feishu Setup

Guide Feishu setup as a checklist, not a lecture.

The official OpenClaw Feishu docs say Feishu ships bundled with current releases, recommend `openclaw channels add` for setup, recommend WebSocket long connection for events, and provide a batch-import permissions JSON. Use those official defaults in this wizard.

## Big-picture explanation

If the user asks what Feishu setup means, use one short line:

- "We are creating a Feishu app with a bot, then connecting that bot to OpenClaw."

## Step-by-step flow

Give only one small task at a time.

### Step 1

- "Open Feishu Open Platform."

### Step 2

- "Create a self-built app."

### Step 3

- "Turn on the bot capability for that app."

If the user cannot find it, say:

- "Look at the left-side menu inside the Feishu app settings. If you see something like '机器人' or bot capability, open that page and enable it."

### Step 4

- "Find the app's `App ID`."

If the user is lost, say:

- "You are looking for the app credentials area. If you see a page that lists basic app information, the `App ID` is usually there."

### Step 5

- "Find the app's `App Secret`."

If the user is lost, say:

- "Stay on the same app credential page. The `App Secret` is usually shown near the `App ID`, or behind a reveal button."

### Step 6

- "Come back here and paste the `App ID` and `App Secret`."

Do not continue until the user provides the credentials.

## After credentials arrive

Continue with short tasks:

- enable event subscription
- prefer long connection WebSocket
- publish the app
- add the bot to the target Feishu group or groups

For `多 bot 多 agent`, do this one bot at a time:

1. finish one Feishu app and bot
2. connect it to OpenClaw
3. verify it works
4. only then start the next bot

This lowers confusion for beginners.

## Official permission import

If the user reaches the permissions page and asks what to paste, give them the official OpenClaw batch-import JSON from the docs:

```json
{
  "scopes": {
    "tenant": [
      "aily:file:read",
      "aily:file:write",
      "application:application.app_message_stats.overview:readonly",
      "application:application:self_manage",
      "application:bot.menu:write",
      "cardkit:card:read",
      "cardkit:card:write",
      "contact:user.employee_id:readonly",
      "corehr:file:download",
      "event:ip_list",
      "im:chat.access_event.bot_p2p_chat:read",
      "im:chat.members:bot_access",
      "im:message",
      "im:message.group_at_msg:readonly",
      "im:message.p2p_msg:readonly",
      "im:message:readonly",
      "im:message:send_as_bot",
      "im:resource"
    ],
    "user": [
      "aily:file:read",
      "aily:file:write",
      "im:chat.access_event.bot_p2p_chat:read"
    ]
  }
}
```

Explain it simply:

- "Feishu lets you batch import the bot permissions. Paste this in the permissions page so the bot can receive and send messages."

If the user cannot find the page, say:

- "Look for a left-side menu item like '权限管理' or permissions. If you see a batch import box, paste the JSON there."

## Event subscription wording

Keep this short:

- "Now switch event subscription to long connection WebSocket."
- "Then add the event `im.message.receive_v1`."

If the user cannot find the page, say:

- "Look for a left-side menu item like '事件订阅'. After you open it, choose long connection WebSocket and then add the message receive event."

The official docs warn that the gateway should already be configured and running before long-connection setup is saved reliably. So if needed, make sure the OpenClaw Feishu channel is already added and the gateway is running first.

## Beginner explanation for adding the bot to groups

Use a short explanation:

- "The bot must be inside the Feishu group before OpenClaw can route that group's messages to the right assistant."

When there are multiple bots in `多 bot 多 agent`, add:

- "After the first bot works, we will repeat the same Feishu steps for the second bot. You do not need to relearn anything, we will just copy the same pattern."

## Minimal OpenClaw-side setup wording

If the user asks what happens on the OpenClaw side, say:

- "I will use OpenClaw's Feishu channel setup, save your App ID and App Secret, then restart the gateway if needed."

## Important V1 rule

For `单 bot 多 agent`, keep the explanation group-based only:

- "In this first version, we only split by Feishu group. Private-chat splitting is an advanced option."

Also keep the rollout small:

- start with one Feishu group first
- verify it works
- then add more groups one by one

## If the user gets lost

Do not send a wall of Feishu platform theory.

Instead ask which exact step they are on, then answer just that step. Examples:

- "Are you currently on the app creation page, or on the credentials page?"
- "Have you already found the `App ID`, or do you still need help locating it?"

If the user says "I don't know where I am":

- "Tell me the main title or the left-side menu items you can see on the page, and I’ll tell you the next click."
