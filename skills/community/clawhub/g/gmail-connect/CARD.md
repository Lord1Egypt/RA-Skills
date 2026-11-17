# 📬 Gmail Connect

Connect OpenClaw to Gmail on Ubuntu with a local OAuth wizard. Search and read mail, check for new messages, and optionally send reviewed drafts.

| Listing field | Value |
| --- | --- |
| Display name | Gmail Connect |
| Slug | `gmail-connect` |
| Publisher | Your authenticated ClawHub publisher; expected GitHub login: `svetlyoh` |
| Version | `0.1.3` preview |
| Categories | `integrations`, `productivity`, `communication` |
| Topics / discovery tags | `gmail`, `email`, `oauth`, `ubuntu`, `local-first` |
| Release tags | `latest`, `preview` |
| Source folder | [GitHub skill source](https://github.com/svetlyoh/web-wallet/tree/master/openclaw/skills/gmail-connect/gmail-connect) |
| Requirements | Ubuntu, Python 3.10+, existing OpenClaw with host execution, your own Google Cloud project and Desktop OAuth client |

## What you can do

- Follow the local browser wizard to configure your Google project and authorize Gmail.
- Search mail and read plain-text messages through your OpenClaw agent.
- Check recent inbox arrivals or enable an optional separate systemd user monitor.
- Prepare local drafts, then review and send each exact message in the browser after opting into send access.

## Access and data

Read-only access is the default (`gmail.readonly`). Sending adds `gmail.send` only when enabled. Credentials, tokens, mail metadata, and local drafts stay in owner-only local files; they are not encrypted at rest. Google OAuth and Gmail API calls leave the host. Email is rendered as text, without remote images.

The wizard listens on `127.0.0.1`. The recommended setup needs no public tunnel or Pub/Sub and makes no gateway configuration changes or restarts.

## Preview limits

Live Ubuntu/OpenClaw, Google OAuth, Gmail, and reboot acceptance are pending. ClawHub's security result is determined after submission. Attachments, label changes, deletion, and multi-account UI are outside this release. Automatic chat alerts require a separately configured OpenClaw automation.

See [README.md](README.md), [PRIVACY.md](PRIVACY.md), and [PUBLISHING.md](PUBLISHING.md). This editable card documents the intended fields; importing the folder does not automatically apply categories, topics, or release tags. Set them in ClawHub or use the publishing command. ClawHub reserves `skill-card.md` for its generated hosted card, so this author-maintained file is named `CARD.md`.
