---
name: jep-primitive-skills
version: 2.0.0
description: Construct explicitly unsigned J/D/T/V event drafts.
---

# jep-primitive-skills

Use only when the user requests this specific operation. Review SECURITY.md before running the service.

## Primitive behavior

The four endpoints construct unsigned draft events only. `success` means draft construction succeeded. Responses explicitly include `draft=true` and `signature_valid=false`. They do not delegate real authority, stop a process or independently verify evidence. The caller's issuer must be assigned to its authenticated identity, and each operation needs the matching `draft:*` permission.

Prefilled signatures are rejected because timestamp/nonce construction would invalidate them. To sign an audit/consensus event, construct the complete input dataclass for that service, then use `sign_event` from that service's security profile. Do not copy a draft projection's signature or claim it is a verified event. The adapter copies extensions and does not invent an orphan-fault exception for termination.

## Setup

Work from the package directory containing `skill/` and `requirements.txt`. Install locked dependencies with `pip install --require-hashes -r requirements.txt`, provision the documented authentication configuration, and run on 127.0.0.1. This package never starts a daemon or changes another runtime automatically.
