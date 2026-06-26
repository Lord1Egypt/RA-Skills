# OpenClaw Evolution v3 (Coordinator Upgrade Blueprint)

A practical, source-informed blueprint to evolve OpenClaw agents from “instruction executors” into “coordinator-style” agents with stronger synthesis, safer execution, and proof-driven verification.

## Who this is for

- OpenClaw users maintaining custom agent policies
- Operators who want higher reliability on complex tasks
- Builders who need a reusable evolution SOP for their own deployments

## Quick links

- 🇬🇧 English Guide: [`EVOLUTION_GUIDE_EN.md`](./EVOLUTION_GUIDE_EN.md)
- 🇨🇳 中文指南: [`EVOLUTION_GUIDE_CN.md`](./EVOLUTION_GUIDE_CN.md)
- 🧬 Gene Locking SOP: [`SOP_GENE_LOCKING.md`](./SOP_GENE_LOCKING.md)
- 🛡 Compatibility & safety: [`COMPATIBILITY.md`](./COMPATIBILITY.md)

## Core upgrades

1. **Mandatory Synthesis**
   - Turn fragmented findings into explicit, self-contained execution plans.
2. **Atomic Task Scheduling**
   - Parallelize read-only exploration, serialize state mutations.
3. **Dynamic Context Injection**
   - Use real environment snapshots before mutation.
4. **Verification as Proof**
   - Validate behavior through tests/checks, not file existence alone.

## Repository structure

- `EVOLUTION_GUIDE_EN.md` — complete English walkthrough
- `EVOLUTION_GUIDE_CN.md` — complete Chinese walkthrough
- `SOP_GENE_LOCKING.md` — durable policy template for `IDENTITY.md` / `AGENTS.md`
- `COMPATIBILITY.md` — version-fit checks, rollout safety, rollback protocol
- `src/` — full source snapshot used as analysis reference

## 5-minute adoption path

1. Read `COMPATIBILITY.md` and confirm your environment fits.
2. Read your preferred guide (`EN` or `CN`).
3. Apply `SOP_GENE_LOCKING.md` in a dedicated branch.
4. Run verification (tests/type-check/smoke).
5. Merge only after stable behavior.

## Important disclaimer

This repo is a **blueprint**, not an official one-click installer.
Always adapt to your OpenClaw version and keep rollback ready.

## Recommended implementation style

- Use feature flags for high-impact behavior changes.
- Avoid replacing existing permission systems wholesale.
- Apply changes incrementally and verify after each step.

## FAQ

### Can others directly copy everything and be done?
Not safely. Most users can follow this repo effectively, but they should still run compatibility checks and staged verification.

### Is `SOP_GENE_LOCKING.md` enough by itself?
It is the core persistent policy template, but safe rollout also needs compatibility checks and local validation.

### Can this be packaged as a skill?
Yes. You can package these SOP rules and trigger conditions into an AgentSkill so agents can apply the same upgrade method consistently.

## Credits

Built from hands-on source analysis and field-tested orchestration practices in OpenClaw environments.
