# Architecture (current v2.1)

## Memory layers

- `memory/events.jsonl` — episodic raw entries
- `memory/semantic.jsonl` — promoted stable facts
- `memory/procedural.jsonl` — promoted workflows
- `memory/self_model.jsonl` — promoted identity rules
- `memory/consolidation-log.jsonl` — dream-cycle decisions
- `memory/ledger.jsonl` — integrity receipts
- `memory/onchain-anchors.jsonl` — local date/tx map for anchors

## Integrity model

For each appended event row:
- `entry_hash = sha256(canonical_entry_without_hashes)`
- `chain_hash = sha256(prev_hash + entry_hash)`
- `prev_hash` links to prior chain tip

Guarantee: immutable append history + tamper-evident linkage.

## Consolidation model

Dream cycle scans last 24h and promotes repeated patterns into semantic/procedural/self_model.

Important: promoted layers are abstractions and do not replace raw events.

## Anchor model (v2)

`pensieve_anchor` encrypts and writes daily payload to Algorand note(s):

- encryption: AES-GCM
- note prefix: `NXP2`
- if payload fits note size => single TX
- else => multi-TX chunked payload with per-chunk hash + full content hash

Payload includes full content:
- `events`
- `semantic`
- `procedural`
- `self_model`

This enables disaster recovery from blockchain + keys.
