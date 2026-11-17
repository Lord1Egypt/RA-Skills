# jep-primitive-skills 2.0.0 — repair candidate

## Primitive behavior

The four endpoints construct unsigned draft events only. `success` means draft construction succeeded. Responses explicitly include `draft=true` and `signature_valid=false`. They do not delegate real authority, stop a process or independently verify evidence. The caller's issuer must be assigned to its authenticated identity, and each operation needs the matching `draft:*` permission.

Prefilled signatures are rejected because timestamp/nonce construction would invalidate them. To sign an audit/consensus event, construct the complete input dataclass for that service, then use `sign_event` from that service's security profile. Do not copy a draft projection's signature or claim it is a verified event. The adapter copies extensions and does not invent an orphan-fault exception for termination.

See [SECURITY.md](SECURITY.md) for configuration, signing, migration and installation.
