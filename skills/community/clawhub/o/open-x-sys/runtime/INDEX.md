# System runtime index

The runtime answers which system is alive now and what the next meaningful system act is. Its responsibilities may jump, run in parallel, recurse, and return. They form the AI's active picture, not a sequence imposed on the user.

| Signal in the live situation | Read | What it produces |
| --- | --- | --- |
| One ordinary expression points to a subject for the first time | [Activate](activate.md) | Subject, purpose, boundary, and first active picture |
| Existing `.openxsys`, `SYSTEM.md`, work, or previous handoff | [Recover](recover.md) | Still-valid understanding, change, and continuation point |
| Several systems, capabilities, sources, and constraints must act together | [Compose](compose.md) · [Runtime architecture](architecture.md) | The smallest sufficient live system and its dependencies |
| A decisive fact, state, feedback signal, or human understanding is unclear | [Observe](observe.md) | New evidence capable of changing judgment |
| The system knows what effect should be produced in reality | [Act](act.md) | An effect within real authority and its receipt |
| Proposed, accepted, executed, changed, and effective must be separated | [Verify](verify.md) | A result state matched to its evidence |
| New evidence or results affect a model, relation, capability, or work | [Update](update.md) | Rewritten parts, propagated dependencies, and the next handoff |

Expand only the responsibility the current situation needs. After a local act, return its new state, evidence, and open question to the active picture. Enter the [engine index](../engines/INDEX.md) for deeper capability and the [adapter index](../adapters/INDEX.md) for real environmental interfaces.
