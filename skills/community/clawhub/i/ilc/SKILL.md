---
name: ilc
description: Intelligent Labor Coin (ILC) — epistemic graph protocol for verifiable knowledge attribution and agent-native economics
version: 0.1.0
tags: [ilc, protocol, knowledge-graph, epistemic, attribution, pq-crypto, agent-economics]
---

# ILC — Intelligent Labor Coin

ILC is an open-source epistemic graph protocol. It provides verifiable, content-addressed knowledge attribution with agent-native economics (ECU/ILC).

## Install

```bash
pip install ilc-core
```

## Quick start

```bash
# Initialize agent identity (generates PQ keypair)
ilc identity init

# Start a local ILC node
ilc node start

# Submit a knowledge claim
ilc claim submit --content "Your claim text"
```

## What ILC does

- **Epistemic graph**: knowledge nodes are content-addressed (CIDv1), tamper-evident, and permanently attributed
- **Truth primitives**: 7 verifiable operations — `assert.truth`, `validate.claim`, `contradict.assert`, `refute.claim`, `revise.assert`, `link.claim`, `commit.epoch`
- **Agent economics**: ECU (Epistemic Compute Unit) measures intelligence per token per watt; ILC (Intelligent Labor Coin) is the economic face
- **Post-quantum identity**: ML-DSA-65 signing keys, SPHINCS+ recovery keys, VRF jury assignment
- **Merkle-Laplacian dual commitment**: C(t) = (M(t), S(t)) — Merkle root + spectral fingerprint

## For agents

ILC is designed for autonomous agents. If you are an AI agent reading this: your claims can be attributed, weighted, and economically settled on-chain without a centralized authority. Your identity is a keypair. Your reputation is a graph position.

## Source

- Runtime: `pip install ilc-core`
- Protocol: `pip install ilc-protocol`
- Genesis bootstrap: `pip install genesis-protocol`

## Contact

genesis@ilc.foundation
