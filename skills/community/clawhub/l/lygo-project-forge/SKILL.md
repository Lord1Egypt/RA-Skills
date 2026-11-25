---
name: lygo-project-forge
description: Use LYGO Project Forge on this PC. Hermes is the Forge Master. QwenPaw is the basic brain. The human approves anything that leaves the machine.
---

# LYGO Project Forge

Public desk and Windows app. One project at a time. Hermes runs the Build desk. Forge Master accepts, reworks, or blocks a piece and does not silently publish it.

## Get the app

This skill does not contain the app. Download the Windows EXE from our site:

https://excavationpro.ca/lygoskillhub.html

Open the card **LYGO Project Forge 0.4.0 — Windows EXE** and save `LYGOProjectForge.exe`. Before you run it, check the file:

```
CertUtil -hashfile LYGOProjectForge.exe SHA256
```

The SHA-256 must be `54e32e7a850213173880ab96a0fc3188b8f05c79067548a0f12899b9f8b1d1d0`. The file is 18,224,499 bytes. No model weights and no API key are inside it.

After it starts, the desk is http://127.0.0.1:8796

## Brain

The shipped brain is basic QwenPaw (`qwenpaw-9b`) at http://127.0.0.1:8080/v1 when Hermes desktop is running. Forge does not download model weights.

On startup Forge looks on this PC only:

1. QwenPaw on port 8080.
2. A local model whose name contains `coder`, if QwenPaw is down.
3. An API key the human adds on the Brain card.

Do not send the desk to a general chat model or a paid route unless the human pinned it. Upgrade notes ship beside the app as `docs/LLM.md`.

## Work with a running Forge

From this skill folder:

```
python scripts/forge_status.py
```

That call reads http://127.0.0.1:8796/api/status and prints brand, version, whether Hermes was found, and the brain label. It does not print keys.

A missing desk is a stopped app, not a failed project. Ask the human to start `LYGOProjectForge.exe`.

## Rails

- One job id, one project, one acceptance check.
- An empty result fails. A result without evidence is rework.
- Do not publish, push, deploy, buy, or delete.
- Do not print secrets, tokens, or credentials.
- The human approves anything that leaves the machine.
