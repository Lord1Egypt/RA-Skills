## Description: <br>
Universal game architecture DSL with six primitives (LOOP, TILEGRID, CONTROLBLOCK, POOL, EVENT, DISPATCHER) for designing portable game and simulation loops, translating between architectures, explaining engine structure to AI agents, and refactoring systems into explicit state and flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stusatwork-oss](https://clawhub.ai/user/stusatwork-oss) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to map game or simulation systems into six reusable primitives, produce portable architecture sketches, and compare implementations across 68K, Cell, CUDA, and ECS-style designs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes code snippets and architecture examples that may omit production hardening or full engine integration details. <br>
Mitigation: Treat snippets as reference patterns and review, adapt, and test any implementation before using it in production. <br>
Risk: Architecture mappings can oversimplify differences between legacy loops, heterogeneous compute, GPU kernels, and ECS scheduling. <br>
Mitigation: Validate the proposed Primitive Map, Dataflow Sketch, and Portability Notes against the target runtime's memory, timing, and concurrency constraints. <br>


## Reference(s): <br>
- [Universal Game Primitives release page](https://clawhub.ai/stusatwork-oss/primitives-dsl) <br>
- [Quick Card](assets/quick_card.md) <br>
- [Architecture Mapping](references/architecture_mapping.md) <br>
- [Classic Shooter Worked Example](references/example_shooter.md) <br>
- [Mall Simulation Tick Worked Example](references/example_mall_tick.md) <br>
- [NPC One Step Worked Example](references/example_npc_step.md) <br>
- [Anthropic Skills Repository](https://github.com/anthropics/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with tables, text diagrams, and concise pseudocode] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Expected outputs include a Primitive Map, Dataflow Sketch, one Worked Example, and Portability Notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
