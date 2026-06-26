# MEV Engine v7.0 ⚙️

> **Kernel + Plugin Architecture.** Minimal immutable core, context-activated plugins, auto-dormancy.

**Mission → Environment → Verification** — A five-layer task execution engine.
The core execution framework of Babata OS. Each layer: core question + verification criteria + exception paths.

---

## v7.0 Architecture

```
┌─────────────────────────────┐
│      Core Kernel (immutable) │
│  Identity · MEV Skeleton     │
│  Tool Table · Safety Rules   │
└──────────┬──────────────────┘
           │
   ┌───────┼───────┐
   ↓       ↓       ↓
 active   scene   dormant
(常加载)  (按需)   (休眠)
```

**Lifecycle:** scene(30d trial) → active(triggered ≥3x) → dormant(30d unused) → scene(reactivate)

---

## MEV Five Layers

```
① Suit    → Prepare & adapt (G0 preflight + boundary check)
② Sense   → Gather & collect (hypothesis explicit, ≥2 sources)
③ Think   → Analyze & falsify (bias check + method selection)
④ Optimize → Deliver (G0-G4 五层递进门禁)
⑤ Evolve  → Reflect (lessons + framework audit)
```

---

## Delivery Gates

```
🔒 DELIVERY CHECK
[✅/❌] G0 Coverage: {n} sources
[✅/❌] G1 Structure: 完整
[✅/❌] G2 Analysis: bias={} evidence_map={}
[✅/❌] G3 Delivery: IMA={} push={}
[✅/❌] G4 Evolve: trace={}
```

---

## Changelog

| Version | Date | Changes |
|:----|:----|------|
| v7.0.0 | 2026-05-13 | **Kernel+Plugin architecture.** Core immutable, capabilities as plugins, auto-dormancy lifecycle. MEV skeleton preserved, specific rules extracted to plugins. |
| v6.5.0 | 2026-05-12 | Trust-but-verify: unified preflight, Agent E verify, IMA fallback |

---

## Install

```bash
git clone https://github.com/meta-evo-creator/mev-engine.git
clawhub install mev-engine
```

## Dependencies

Zero external dependencies. Requires Python for time-awareness probe.

## License

MIT
