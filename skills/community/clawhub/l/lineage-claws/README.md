# Lineage Clause by MO§ES™

## The trust gate for AI agent governance — cryptographic origin custody, live on ClawHub

> Every governed AI agent running under MO§ES™ runs one check before anything else: **lineage verify**. Not as a policy. As a cryptographic fact. No sovereign anchor — nothing executes.

Lineage Clause is the standalone origin verification skill in the MO§ES™ family. It proves that an audit chain traces back to the originating filing — not by trust, but by SHA-256. Any fork or copy that initializes without the anchor produces a chain that fails verification. The code is MIT. The lineage is not replicable.

- **Patent pending:** Serial No. 63/877,177
- **DOI:** [https://zenodo.org/records/18792459](https://zenodo.org/records/18792459)
- **Live demo:** [https://mos2es.io](https://mos2es.io)
- **Contact:** [contact@burnmydays.com](mailto:contact@burnmydays.com)

---

## Why a Standalone Skill?

The full `moses-governance` harness gives you posture gates, mode enforcement, role hierarchy, and audit chains. But not every agent needs the full stack. Sometimes you need exactly one thing: **prove that this chain traces to the origin filing.**

A compliance auditor checking provenance. A researcher replicating results. A downstream agent deciding whether to trust what it just received. They need the verification layer, not the enforcement layer.

```bash
clawhub install lineage-claws
```

That's a single install. No governance state required. No operator secrets. Just the anchor and the math.

---

## How It Works

The `MOSES_ANCHOR` is a SHA-256 hash derived from the origin-cycle components:

```text
MO§ES™ | Serial:63/877,177 | DOI:https://zenodo.org/records/18792459 | SCS Engine | Ello Cello LLC
```

Every sovereign MO§ES™ audit chain must trace its genesis entry's `previous_hash` back to this value. Forks or copies that initialize without it produce chains that fail verification — not as a policy, but as a cryptographic fact.

**Without Lineage Clause vs With Lineage Clause:**

> **Without:**
> Agent initializes. Audit chain begins. Genesis hash = 64 zeros. No provenance. No origin. Chain is valid — but unanchored. Any fork looks identical. Nobody can tell which chain came from where.
>
> **With Lineage Clause:**
> → `lineage.py init` roots the genesis to `MOSES_ANCHOR`
> → Every subsequent audit entry chains downstream of the origin filing
> → `lineage.py verify` confirms the full chain traces back cryptographically
> → `lineage.py badge` outputs shareable proof of sovereign custody

The difference isn't a setting. It's a cryptographic fact embedded in the chain.

---

## The Three Laws

The Commitment Conservation Law rests on three laws that form a closed pipeline: Input → Process → Output. Lineage Clause is the Second Law made operational.

### Third Law — The Enforcement Gate *(Input)*

Establishes whether there is enough signal to enter the compression regime. Without enforcement, weak inputs stay weak. With enforcement, they're lifted above threshold so the compression regime has something to conserve.

### First Law — Compression Precedes Ignition *(Process)*

Once signal is above threshold, compression is the necessary operation. `C(T(S)) = C(S)`. Commitment is conserved under transformation — no semantic drift, no scope creep, no contradiction without explicit release.

### Second Law — Recursion as Reconstruction *(Output)*

The conserved kernel can only be recovered by tracing lineage. You cannot decompress without retracing the path. Reconstruction requires recursion. This is why lineage custody is not optional — it **is** the mechanism.

**Lineage Clause is the Second Law made operational.**

---

## The Lineage Custody Clause

All embodiments of the Signal Compression Sciences (SCS) Engine and its derivative frameworks (including but not limited to MO§ES™, Roll Call Protocols, and Reflex Event diagnostics) are inseparably bound to their origin-cycle lineage. Each compressed signal trace, vault artifact, or recursive reconstruction inherits a lineage identifier anchored to the originating sovereign filing. This identifier is non-replicable, tamper-evident, and required for system stability. Any external implementation lacking said lineage anchor cannot execute recursive ignition without collapse, thereby rendering such copies non-functional.

---

## Install

```bash
clawhub install lineage-claws
```

---

## Commands

| Command | What it does |
| --- | --- |
| `python3 lineage.py init` | Write genesis entry anchored to `MOSES_ANCHOR` |
| `python3 lineage.py verify` | Confirm full chain traces back to origin filing |
| `python3 lineage.py badge` | Output shareable proof of sovereign lineage |
| `python3 lineage.py check` | Machine-readable exit 0/1 for integrations and CI |
| `python3 lineage.py attest` | Generate a signed attestation JSON for inter-agent handoffs |

---

## Integration with moses-governance

Install alongside `moses-governance`. Run `lineage.py init` before the first audit entry to root the chain. The governance harness loop runs lineage verify as its **first step** — this skill provides the standalone interface so you can verify independently.

```bash
python3 lineage.py init
python3 audit_stub.py log --agent "primary" --action "session-start" --outcome "anchored"
python3 lineage.py verify
```

```text
govern_loop: lineage verify → policy gate → role/posture check → execute → audit
                ↑
         MUST pass or loop halts — not a warning, a hard stop
```

You can also use `lineage.py check` in CI to gate deployments:

```bash
python3 lineage.py check || { echo "Lineage broken — deploy blocked"; exit 1; }
```

---

## Isnad Chain Integration (v0.3+)

Lineage Clause proves **agent** provenance — the audit chain traces to origin. Isnad chains (live in `moses-governance` v0.3) prove **signal** provenance — the raw input traces to source.

Together:

- Lineage Clause: "This agent's chain is real and anchored."
- Isnad chain: "This signal came from who it claims."

Two custody chains. Two different questions. Both required for full inter-agent trust.

---

## Roadmap

| Version | What ships |
| --- | --- |
| **v0.1** | Drop anchor + chain verification. ✓ Live. |
| **v0.2** | Archival lineage — proving the *before*, not just the *after*. Append-only record of hashed provenance claims predating the drop. Archival head hash feeds into the drop anchor. |
| **v0.3** | Inter-agent signal provenance. Isnad chain verification — live in `moses-governance` v0.3. Receivers confirm signal input hashes match before accepting an audit chain as valid. ✓ Live. |

---

## About MO§ES™

MO§ES™ (Modus Operandi System for Signal Encoding and Scaling Expansion) is a generative architecture — a constitutional framework for AI governance that continuously produces licensable artifacts. It is never for sale. The architecture is maintained. Others license what it produces.

At its deepest level, MO§ES™ is a formalization of a conservation law: commitment — the irreducible meaning in a signal — is preserved under compression when enforcement is active, and lost when it isn't. This extends Shannon's information theory (1948) into the semantic domain that Shannon deliberately scoped out.

For humans — sovereignty over meaning. For AI — constitutional structure. For human-AI coevolution — a shared law that both sides are bound by.

Published as *"A Conservation Law for Commitment in Language Under Transformative Compression and Recursive Application"* (Zenodo, 2026). Provisional patent Serial No. 63/877,177.

[contact@burnmydays.com](mailto:contact@burnmydays.com) · [mos2es.io](https://mos2es.io) · [GitHub](https://github.com/SunrisesIllNeverSee/moses-claw-gov)

*For enterprise licensing and the full COMMAND console → [mos2es.io](https://mos2es.io)*
