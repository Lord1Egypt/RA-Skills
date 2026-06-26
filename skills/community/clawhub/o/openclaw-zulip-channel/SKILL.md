---
name: openclaw-zulip-channel
description: Install and configure the OpenClaw Zulip channel plugin from npm. Use when OpenClaw needs to add Zulip support, switch from a local path install to the published npm package, validate Zulip plugin health, or help a user configure Zulip bot credentials, streams, DM policy, and stream behavior.
---

# OpenClaw Zulip Channel

Install the published npm plugin, wire the `channels.zulip` config, and verify the gateway comes back clean.

## Install or switch to npm

Run:

```bash
openclaw plugins install openclaw-channel-zulip
```

If a local dev path is overriding the plugin, remove the path override from `plugins.load.paths`, then restart the gateway so only the installed plugin loads.

The plugin id is `zulip`, even though the npm package name is `openclaw-channel-zulip`.

## Minimal config

Add or verify:

```json
{
  "channels": {
    "zulip": {
      "enabled": true,
      "url": "https://your-org.zulipchat.com",
      "email": "yourbot@your-org.zulipchat.com",
      "apiKey": "your-zulip-api-key",
      "streams": ["general"],
      "dmPolicy": "allowlist",
      "allowFrom": ["*"]
    }
  }
}
```

## Common knobs

Use `streams` to control which streams are monitored.

Use `requireMention` when the bot should only answer when mentioned in streams.

Use `groupPolicy` and `groupAllowFrom` to control stream access.

Use `typingMode`, reactions, and block streaming settings for reply behavior.

## Verification

After install or config changes:

```bash
openclaw gateway restart
openclaw doctor --non-interactive
```

Confirm doctor reports `Zulip: ok` and plugin errors are zero.

Then do a smoke test with one DM and one stream message.

## Credentials

Get the Zulip bot email and API key from Zulip bot settings.

Use the organization base URL like `https://your-org.zulipchat.com`.

Store secrets in OpenClaw config or supported env vars, not in chat.

## Publish/update notes

Publish the npm package separately from this skill. This ClawHub skill is the install and setup wrapper that points people at the published plugin.

When the npm package updates, bump this skill version and update any install or config guidance that changed.
