# Downstream module boundaries

Enforce responsibilities and dependency direction, not a fixed count of packages.
A small application may implement these boundaries as modules in one wheel.
Split distributions only when ownership, dependencies, or release cadence justify it.

| Boundary | Owns | Must not own |
| --- | --- | --- |
| contracts | Observation/action specs, transition identity, schema versions | Game IO, optimizer, file/network handlers |
| environment | Authorized game interaction, observation mapping, action execution, reset/attach | Policy selection or learner imports |
| rewards | Reward composition, success/termination semantics and safety budgets | Game IO or optimizer updates |
| policy | Observation-to-action inference, exploration and recurrent policy state | Environment control or persistent dataset mutation |
| learner | Objectives, gradients, optimizer/scheduler state, parameter updates | Game-specific transport or UI automation |
| collection | Policy/environment interaction and ordered trajectories | Optimizer implementation or invented terminal outcomes |
| storage | Dataset/checkpoint serialization, integrity and migrations | Reward decisions or training orchestration |
| application | Composition, lifecycle/configuration, logging and monitoring setup | Duplicated domain algorithms |

Reuse GLR ports and data contracts rather than defining parallel versions.
Contracts are the inward dependency boundary. Concrete engine, learner, storage,
and monitoring integrations depend on narrow ports; application code composes
them. No circular imports. Environment code does not import the policy/learner;
policy inference must remain usable without starting training or a live game.

Distinguish the game's full state, the observation available to a policy, and
the policy's internal/recurrent state. Define which information crosses each
boundary; privileged state must not silently leak into evaluation observations.
An Agent is a clearly scoped policy executor or composition, not an object that
accumulates capture, reward, optimizer, persistence, logging, and recovery logic.

Test the boundaries: import the environment without learner extras, run policy
inference without an optimizer, replay reward fixtures without game IO, and test
storage migrations without starting roles. Maintain explicit allowed dependencies
with an import checker suitable for the project; behavioral tests remain required.

## Migrate an existing project

1. Inventory entrypoints and import edges. Assign each function/class one owner
   from the table; identify mixed responsibilities and cycles before moving files.
2. Preserve representative offline traces and expected decisions/rewards. Record
   observation/action/reward contract digests and checkpoint provenance.
3. Move one cohesive unit and its callers into the installed namespace. Keep a
   thin, time-bounded compatibility import when needed; no source-path injection.
4. Move construction and logger/SDK configuration into the composition root.
   Replace direct environment-to-learner references with existing GLR ports.
5. Verify replay parity and installed-wheel tests after each migration. A module
   move must not silently change observation order, action indices, reward scale,
   RNG behavior, or terminal/truncation semantics.
6. Follow `FRAMEWORK_MIGRATION.md` for any serialized class/module references,
   config entrypoints, or checkpoint changes. Renaming Python modules can break
   pickle-based artifacts; never deserialize unknown checkpoints to discover
   their behavior. Use supported loaders/converters and preserve originals.
7. Update `MIGRATIONS.md` with old/new ownership, compatibility imports and removal
   versions, data impact, tests, and rollback. Do not mark the whole project
   migrated while known legacy paths remain.
