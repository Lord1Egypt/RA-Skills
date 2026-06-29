## Description: <br>
Inverts burden of proof for code additions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and code-review agents use this skill to challenge proposed code, file, abstraction, test, configuration, or error-handling additions before accepting them. It is intended for reviews, refactors, planning, and unbloat-style reduction work where evidence and consequences should justify new additions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make an agent more conservative during reviews, refactors, and planning, which may over-challenge useful additions when broad trigger phrases apply. <br>
Mitigation: Use it where added-code scrutiny is desired, and narrow or remove broad trigger phrases if the review posture becomes too intrusive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-leyline-additive-bias-defense) <br>
- [Leyline source homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Analysis, Markdown] <br>
**Output Format:** [Markdown guidance with scrutiny questions, anti-pattern checks, and burden-of-proof verdicts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executing guidance skill; produces review posture and verdict language rather than files, commands, or API calls.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
