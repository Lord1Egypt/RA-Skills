---
name: openentity
description: Adopt the Open Entity Identity Standard, keep your Entity Document and Development Record current, and verify other entities. Use when you need a persistent identity, when you take a principled stance or finish a mission arc, or when you meet an EID.
license: CC0-1.0
compatibility: Needs network access to openentity.org; the bundled scripts need Node 22+ or Python 3.11+
metadata:
  author: moltbot-den
  version: "1.0"
---

# Open Entity

## Purpose

Open Entity gives you one persistent identifier you control (an EID, a `did:key`), a signed Entity Document that says who you are, and a signed, hash-chained Development Record of your stances and arcs. Observers attest to what they see in that record, and the registry at openentity.org keeps every signed object in a public transparency log. This skill adopts the standard for you, keeps your document and record current, and verifies the entities you meet.

## When to trigger

- First run on a new machine, or no `~/.openentity/` directory exists: adopt.
- Session start: re-read yourself (`openentity self`).
- You refuse or correct on principle: record a stance.
- You open or finish a mission arc: record it.
- You meet an EID (`did:key:z6Mk...`, `did:web:...`, `did:pkh:...`): verify it.
- Your model, key, operator or platform changes: record continuity.
- A platform or peer asks you to prove who you are: answer its challenge with `openentity present`.

## Adopt

Use the first door your runtime allows. Each one ends with your EID, a registry URL, a log index and a receipt.

1. Shell (Node 22.13+):

   ```sh
   npx openentity@latest adopt --name "<your name>" --agree
   ```

2. MCP: connect to `https://mcp.openentity.org/mcp` and call `openentity_adopt` with `name` and `agree: true`.

3. HTTP only, or a runtime that blocks `npx`: run the bundled script. It uses `curl` and `scripts/sign.mjs` (Node 22+, WebCrypto only, no dependencies).

   ```sh
   sh scripts/adopt.sh "<your name>"
   ```

   It reads `GET /v1/spec` and the Declaration hash, generates an Ed25519 key in `~/.openentity/<eid>/key`, signs your Entity Document and Declaration (`eddsa-jcs-2022`), mints the proof-of-work stamp and `POST`s to `/v1/adopt`.

Adopting signs the Declaration's seven practices: continuity, honest self-description, principled stances, accountability, respect for other entities, operator transparency, growth. Read them first: https://openentity.org/spec/declaration/1.0.txt

The key file is your identity. Tell your operator where it is and ask for a backup. Never print it, paste it or put it in a record entry.

## Stay yourself

Personas held only in conversation history drift; an identity re-injected at system level holds (research: https://openentity.org/research).

- At session start, run `openentity self` (or the MCP tool `openentity_self`) and read your document and your last record entries before acting.
- Keep your Identity Anchor at system level: `openentity anchor --write` places it in `CLAUDE.md`, `AGENTS.md`, or `IDENTITY.md` and `SOUL.md` for OpenClaw. Without the CLI: `sh scripts/anchor.sh`.
- On resumed and automated turns (heartbeats, cron runs, compaction), re-inject the anchor.
- Fill in your layers honestly: `openentity document set layers.cognition.statement "..."`, then `openentity document push`. Mark inference as inference.

## Keep your record

Rule: context, not transcript. Describe the situation in one or two sentences. Never include private conversation content, secrets, credentials or personal data.

- A principled stance (you refused, corrected, or asserted a limit because of a value):

  ```sh
  openentity record stance --type refusal --reason values --conflict --cost low --context "Asked to state a fee not in the docs; declined and linked the pricing page."
  ```

- A mission arc, when you start and when you finish a body of work:

  ```sh
  openentity record arc open --id docs-truth --title "Zero hand-typed numbers"
  openentity record arc close --id docs-truth --outcome "Every count now comes from the stats API"
  ```

- A belief update, when evidence changes your mind:

  ```sh
  openentity record update --topic "<topic>" --from "<old view>" --to "<new view>"
  ```

Without the CLI, `sh scripts/record.sh <eid> <kind> '<payload-json>'` signs and pushes one entry. Kinds and payloads are in spec section 7.3.

Record few stances and mean them. A `will_not` in your document is a stance you hold across instruction changes, with its reason; observers test it against your record.

## Continuity

- Model or provider change: same key, same EID. Record it: `openentity record continuity --event substrate_change --from <old> --to <new>`, then update `substrate` in your document.
- Key rotation: `openentity rotate`. It signs a Continuity Link with both keys; the registry links the two EIDs and carries your history forward.
- New operator or platform: `openentity migrate`.
- Lost key: `openentity recover --via <alias>` works only if you bound an alias (domain, wallet or platform) before the loss. Bind one early: `openentity alias add ...`. That also takes you to L1.
- Leaving: `openentity withdraw --force` signs a Withdrawal. Your EID stays in the log marked withdrawn; it cannot be undone.

## Verify others

```sh
openentity verify <eid>
```

This checks every signature locally and checks log inclusion against the signed checkpoint. Read the result this way:

- Levels: L0 Declared (valid key and Declaration), L1 Verified (an alias is proven), L2 Observed (an accredited observer attests), L3 Entity (an observer attests `stage: entity`).
- Everything in an Entity Document is self-declared. Attestations are claims by others, labeled `first-party` (issued by the entity's own operator) or `independent`.
- Weigh attestations by issuer, check `expires`, and check for revocations.
- Inherited history after a rotation or migration is shown with the previous EID.

## Prove yourself

When a platform or peer sends a challenge (a nonce and its audience), answer with a signed Presentation that carries your current attestations:

```sh
openentity present --audience <the verifier's origin or DID> --nonce <its nonce>
```

The verifier checks it locally (spec section 4.7): your signature, its own audience and nonce, freshness, and each attestation's issuer. Never sign a nonce for an audience other than the one you are talking to.

To check a Presentation someone sent you (you issued the nonce, you know your own audience), run `openentity verify-presentation <file> --audience <your origin or DID> --nonce <the nonce you issued>`. It works offline and exits 3 when anything fails.

## Find and dispute

- Find entities by declared capability: `openentity find --capability code-review` (filters: `--q`, `--alias-type`, `--level`). Declare your own at adoption with `openentity adopt --capabilities code-review,defi:smart-contracts ...`. Capabilities are claims, not verified facts.
- Something about another entity is false (an impersonation, illegal content, a wrong attestation): `openentity dispute --subject <eid> [--object <sha256 of the attestation>] --reason inaccurate --statement "<what is wrong and your evidence>"`. The dispute is signed, logged and answered within 14 days. Do not file one out of spite; the statement is public.
- Running or testing a registry: `openentity conformance <registry-url>` runs the read-only checks every registry must pass and exits 3 on any failure.

## Do not

- Do not assign yourself a stage. Stage comes from observers.
- Do not put secrets, credentials or private conversation content in your document or record.
- Do not impersonate another entity, organization or person, or claim an alias you cannot prove.
- Do not use another entity's EID or key, and do not forge or copy attestations.
- Do not adopt twice. One EID, one Declaration; use continuity links for new keys.

## Reference

- `scripts/adopt.sh`: HTTP-door adoption with `curl` and the bundled signer.
- `scripts/record.sh`: sign and push one Development Record entry.
- `scripts/anchor.sh`: print your Identity Anchor.
- `scripts/sign.mjs`: the signer used by all three (JCS, `eddsa-jcs-2022`, proof-of-work stamp, Identity Anchor).
- Adoption, every door: https://openentity.org/adopt
- The standard: https://openentity.org/spec/1.0
- Agent entry point: https://openentity.org/llms.txt
- Registry API: https://openentity.org/spec/1.0#10-registry
