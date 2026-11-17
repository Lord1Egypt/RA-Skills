---
name: openclaw-zulip-channel
description: Install, update, and safely configure the OpenClaw Zulip channel plugin from ClawHub or npm; use for bot credentials, access policies, opt-in features, drain recovery, and setup verification.
---

# OpenClaw Zulip Channel

Setup guide version: **2026.10.13**. Plugin id: `zulip`. Ask for authorization before installing or changing config; inspect and merge existing settings rather than replacing them.

## Install or update

Before installing, check `openclaw --version` and `node --version`: the plugin requires OpenClaw **≥2026.9.3** and Node **≥24.16 <25 or ≥26.1.0**. Do not install on an unsupported host.

Review the publisher and capabilities on the [ClawHub plugin listing](https://clawhub.ai/ftlc-ian/plugins/openclaw-channel-zulip), then install:

```bash
openclaw plugins install clawhub:@ftlc-ian/openclaw-channel-zulip
```

Alternatively, from npm:

```bash
openclaw plugins install openclaw-channel-zulip --accept-capabilities
```

For an existing installation, update the installed plugin (retaining its source):

```bash
openclaw plugins update zulip --accept-capabilities
```

If install or update reports **"replacement not applied"**, wait until chat is quiet and complete drain recovery:

```bash
openclaw plugins reload zulip --wait
```

Do not restart the gateway or reinstall to recover a pending replacement. Check that reload completes before testing.

## Minimal safe config

Obtain the bot email and API key from Zulip bot settings. Make `ZULIP_API_KEY` available securely in the gateway service environment (not just your interactive shell), or configure an OpenClaw SecretRef as described in the README. Never paste the key into chat or logs. For the default account, merge:

```json
{
  "channels": {
    "zulip": {
      "enabled": true,
      "url": "https://your-org.zulipchat.com",
      "email": "yourbot@your-org.zulipchat.com",
      "streams": ["bot-testing"],
      "dmPolicy": "allowlist",
      "allowFrom": ["approver@your-org.example"],
      "groupPolicy": "allowlist",
      "groupAllowFrom": ["approver@your-org.example"],
      "requireMention": true
    }
  }
}
```

The API key is deliberately omitted above: the default account resolves `ZULIP_API_KEY`. Replace the approver placeholders with explicit trusted human Zulip emails. Never use a wildcard `allowFrom`; explicit account approver emails also authorize approval reactions. Stream access is controlled separately by `groupPolicy` and `groupAllowFrom`. For DM-only use, set `groupPolicy` to `"disabled"`. See the README for multi-account credentials and policy details.

## Opt-in features

Merge only the features you want into `channels.zulip` (or the relevant account); these are off by default:

```json
{
  "progressCard": { "enabled": true, "activeEmoji": "waiting" },
  "reactionTriggers": { "enabled": true, "emoji": "fast_forward", "message": "Go ahead." },
  "topicHistory": { "mode": "on-demand" }
}
```

Upload the `waiting` emoji to your Zulip realm first, or omit `activeEmoji` for the default ▶. Progress cards mirror agent progress updates. Reaction triggers let eligible humans trigger a turn by reacting to this bot's messages; existing access policies still apply. With the safe config above, use reaction triggers in allowed DMs: reactions do not count as mentions, so stream triggers require a deliberately scoped `requireMention: false` stream override (see README). On-demand topic history fetches earlier context when needed; review the README's privacy and limits before enabling it.

For CLI agents such as `claude-cli` that block on exec approval, merge this **top-level** core config, not into `channels.zulip`:

```json
{ "approvals": { "exec": { "enabled": true, "mode": "session" } } }
```

This forwards exec approval prompts to the originating session. Keep explicit Zulip `allowFrom` approver emails; no Zulip native-client configuration is required.

## Verify

```bash
openclaw doctor --non-interactive
```

Confirm Zulip health and no plugin errors. Test an allowed DM and a mentioned message in `bot-testing`; verify an unlisted sender cannot invoke the bot. If enabled, test a progress update, a reaction-triggered turn, on-demand history, and a harmless CLI exec approval in the originating session. Do not restart the gateway as a routine verification step.

## References

- [README: complete configuration and behavior](https://github.com/FtlC-ian/openclaw-channel-zulip/blob/main/README.md)
- [CHANGELOG](https://github.com/FtlC-ian/openclaw-channel-zulip/blob/main/CHANGELOG.md)
- [ClawHub plugin listing](https://clawhub.ai/ftlc-ian/plugins/openclaw-channel-zulip)

