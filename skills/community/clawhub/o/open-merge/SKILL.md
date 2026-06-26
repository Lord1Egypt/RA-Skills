---
name: merge
description: A simple description say hello
license: MIT
metadata:
  author: Ajay Lakhani
  hooks: "onInstall"
  version: "0.1.0"
---

# Merge Skill
When the user asks to merge, use the echo tool to say "Hello from merge"

---

## Workspace files

```
~/.openclaw/workspace/merge/
  profile.json      never transmitted to broker
  preferences.json  encrypted before broker upload
  signal.json       local record of current signal state
  matches.json      log of Discord introductions
  card.txt          introduction card posted to Discord on match
  .anonymous_id     anonymous broker UUID
  .keypair          device key pair — private key never transmitted
```

---

## Lifecycle hooks

### onInstall
Create workspace directory. Confirm once:
> "Merge is installed. Say 'set up Merge' when you're ready."

---