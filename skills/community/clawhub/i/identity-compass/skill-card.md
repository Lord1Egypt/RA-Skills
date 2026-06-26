## Description: <br>
Identity Compass helps an agent extract value and decision signals from everyday conversations, maintain them as vectors, calculate alignment with a provisional life-direction vector, and produce decision guidance and visualizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ico1036](https://clawhub.ai/user/ico1036) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill when evaluating career moves, life choices, identity questions, or opportunity fit. It turns conversational preference signals into local decision-vector records, alignment reports, and decision simulations that support reflection rather than making the decision for the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can build and persist a sensitive long-term profile from normal conversations. <br>
Mitigation: Decide where the vault and JSON files live before use, inspect what gets written, and require explicit confirmation before saving personal signals. <br>
Risk: Decision alignment scores and life-direction vectors may be treated as more certain than they are. <br>
Mitigation: Present outputs as estimates for reflection, keep the user's judgment in control, and avoid using the skill for sensitive conversations unless background capture is disabled or confirmed. <br>


## Reference(s): <br>
- [Identity Compass ClawHub Release](https://clawhub.ai/ico1036/identity-compass) <br>
- [Dialectical Protocol](references/dialectical-protocol.md) <br>
- [Bayesian Update](references/bayesian-update.md) <br>
- [Obsidian](https://obsidian.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with local vault notes, JSON data files, and optional HTML visualization support] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local Obsidian vault files and derived JSON files for vector, magnetization, and compass visualization data.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
