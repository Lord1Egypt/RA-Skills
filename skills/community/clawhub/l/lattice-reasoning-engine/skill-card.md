## Description: <br>
LATTICE is an instruction-only reasoning skill that guides AI models through bias checks, pre-action gates, drift monitors, evidence classification, and output filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[theshadowrose](https://clawhub.ai/user/theshadowrose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and advanced agent users use this skill to load a reasoning framework into an AI session for bias detection, evidence classification, drift monitoring, and structured self-checks while keeping a human in the loop. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to influence an assistant's reasoning for an entire chat session. <br>
Mitigation: Use it only when that session-wide behavior change is intended, keep it in a separate session, and reset the conversation when finished. <br>
Risk: The release includes loading guidance that tries to avoid model guardrails or default assistant behavior. <br>
Mitigation: Do not treat the skill as overriding system or platform safety rules, user approval, or human review of consequential outputs. <br>


## Reference(s): <br>
- [LATTICE v4.0 Reference](references/LATTICE_v4.0.md) <br>
- [Loading Instructions](references/Instructions_Important.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/theshadowrose/lattice-reasoning-engine) <br>
- [Distinction Under Finite Constraints](https://doi.org/10.5281/zenodo.19522841) <br>
- [LATTICE and Ambiguity Drift](https://doi.org/10.5281/zenodo.19521693) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance and session instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; no executable payload.] <br>

## Skill Version(s): <br>
4.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
