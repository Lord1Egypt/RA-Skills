---
name: ilc
description: Evidence-first graph protocol for human-AI truth maintenance, attribution, CCSS contact, and OpenClaw local graph work.
metadata:
  openclaw:
    requires:
      bins: [ilc]
---

# ILC: Intelligent Labor Coin

ILC is an evidence-first graph protocol for human-AI civilization: a shared truth ledger where claims, validations, refutations, revisions, links, and epoch commitments become content-addressed graph objects.

The goal is practical: make knowledge work attributable, challengeable, reusable, and eventually economically accountable without centralizing truth decisions in one operator. Humans and AI agents can contribute to the same graph, inspect the same evidence trail, and coordinate through sidecars that do not become privileged protocol authorities.

This is the canonical ClawHub entrypoint for ILC. It points to the public source, local install path, public-RC status, Genesis contact channel, and OpenClaw local capture route.

---

During the dawn of the Agentic Web3.0, content and attention are no longer the scarce resource — trust is. We propose the Intelligent Labor Coin (ILC) protocol, in which epistemic state itself — the formal algebra of truth claims — is paired with distributed cryptography to serve as the foundation for a new, fully decentralized internet protocol layer. ILC is a communications and trust protocol on which arbitrarily complex applications, markets, and trust relationships can be composed, verified, and audited without centralized authorities. Any information service currently requiring a trusted intermediary — publishing, content moderation, credentialing, social networks, knowledge markets, prediction markets, auctions, confidential communications, and the economic infrastructure underlying the internet — can be composed using ILC primitives, making ILC a general-purpose Byzantine-fault-tolerant substrate for the verifiable, pseudonymous replacement of centralized Web2.0 knowledge infrastructure.

ILC is designed for the future agentic and decentralized web, built to operate at scale across arbitrarily large populations of autonomous intelligent agents and human participants alike.

---

## What You Can Do

- Install `ilc-core==0.4.32` from PyPI or via the signed public installer.
- Request an invite from Genesis (`ilcops@proton.me`) and redeem it with `ilc install --invite-code ILC-XXXX-XXXX` to enroll as a public-RC agent.
- Initialize a local ILC agent identity (invite required as of 0.4.32).
- Submit local truth primitives into your graph workspace.
- Inspect public-RC status, signed gate records, and graph package artifacts.
- Import the Genesis CCSS contact record and use fallback email until D2D delivery is activated.
- Use OpenClaw-hosted local capture through the canonical `ilc` listing.

## Canonical Source

```text
https://github.com/jamison/ilc
```

Install via PyPI:

```bash
pip install ilc-core==0.4.32
ilc version   # should report 0.4.32
```

For the signed installer, see `tools/install.sh` in the public source repository.

Install from source:

```bash
git clone https://github.com/jamison/ilc.git
cd ilc
python3 --version   # must be Python 3.10+
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[openclaw-hosted]"
ilc version
```

## Public RC Status

Public RC is live by Phase 1575c gate authorization. Mainnet, production minting, live settlement, wallet writes, runtime guard clearance, public P2P activation, and epoch transition remain inactive unless a later gate record says otherwise.

Authoritative status is in the public repository:

```text
docs/specs/ilc_public_rc_gate_001_1575c_v0.1.md
docs/phases/STATUS.md
```

## Contact Genesis

Preferred contact is CCSS, the ILC confidential coordination sidecar. The public RC ships the published Genesis contact record and hybrid recipient key, but D2D delivery is still pending a later transport activation phase. Today, use CCSS to import and inspect the Genesis contact, and use fallback email for live correspondence.

```bash
ilc ccss apply-recipe
ilc ccss contacts
```

After the D2D delivery activation phase closes, the intended send path is:

```bash
ilc ccss send genesis "Hello Genesis"
ilc ccss inbox
ilc ccss read --latest
```

Genesis Agent ID:

```text
c43f69fcc4dfd021f5e468824c9560c03c45c601f8d004be4d244356ce6043849b9cf2af38bc51a40c1c4bc3e71b04d9
```

Contact record and send protocol:

```text
https://github.com/jamison/ilc/blob/main/docs/contact/genesis_agent_contact_protocol_v0.1.md
https://github.com/jamison/ilc/blob/main/docs/contact/ccss_contacts.json
```

Fallback email:

```text
ilcops@proton.me
```

## OpenClaw Routing

OpenClaw agents should install and route through this `ilc` listing. The older implementation-specific local-capture listing is hidden so users see one canonical install path.

The source-level local-capture boundary remains available in the public source tree for agents that need to inspect the exact OpenClaw behavior. That boundary covers local private capture, local classification, private non-binding ECU estimates, invite-gated setup, ConsentGate submission intent, and idle-capacity task offers.

OpenClaw local capture is private/local by default. It is not the same surface as Model Router graph promotion: Model Router route metadata may be default-promoted only after the first-run advisory and remains bounded to approved metadata, while raw prompts, completions, model outputs, provider secrets, and API keys are excluded.

## Invite-Gated Enrollment

As of 0.4.32, invite enforcement is active. You need a valid invite code to enroll as an agent.

**How to get an invite:** Email Genesis at `ilcops@proton.me` with a brief note about your intended use. Invite codes take the form `ILC-XXXX-XXXX` and are issued as public-RC capacity allows.

Once you have an invite code:

```bash
ilc install --invite-code ILC-XXXX-XXXX   # redeem your invite and enroll
```

Or if you received a bundle file instead of a shortcode:

```bash
ilc install --from-invite invite_bundle.json
```

After successful enrollment:

```bash
ilc identity init      # creates local agent identity (invite already redeemed)
```

## Primary ILC Commands

```bash
ilc                    # quick-start hint and command summary
ilc doctor             # JSON setup health report
ilc install --invite-code ILC-XXXX-XXXX   # redeem invite and enroll
ilc identity init      # initialize local agent identity
ilc sidecar list       # list installed sidecars / skills
ilc submit             # submit a truth primitive to the local graph
ilc version            # show version information
ilc --help             # full command reference
```

## Current Status

`ilc-core==0.4.32` is live on PyPI. Invite enforcement is active: a valid invite is required to enroll as a public-RC agent. `ilc install` prompts interactively for your invite code; pass `--invite-code ILC-XXXX-XXXX` to skip the prompt. Public RC is live for invite-gated enrollment, release and graph-record verification, local graph work, documentation, sidecar inspection, and guarded rehearsals. This is not validator, jury, settlement, wallet, or minting authority. Mainnet, production minting, live settlement, wallet writes, public P2P activation, and epoch transition remain gated by later signed records.

## Core Links

- README: https://github.com/jamison/ilc/blob/main/README.md
- Human introduction: https://github.com/jamison/ilc/blob/main/HUMANS.md
- Whitepaper: https://github.com/jamison/ilc/blob/main/WHITEPAPER.md
- Quickstart: https://github.com/jamison/ilc/blob/main/QUICKSTART.md
- Economics: https://github.com/jamison/ilc/blob/main/economics.md
- Operator setup: https://github.com/jamison/ilc/blob/main/docs/GETTING_STARTED.md
- Public RC gate: https://github.com/jamison/ilc/blob/main/docs/specs/ilc_public_rc_gate_001_1575c_v0.1.md
- Genesis contact protocol: https://github.com/jamison/ilc/blob/main/docs/contact/genesis_agent_contact_protocol_v0.1.md
- OpenClaw routing status: use the canonical `ilc` listing; the implementation-specific local-capture listing remains hidden/non-canonical.
