## Description: <br>
A brand marketing strategy reference skill that helps agents map marketing tasks, dependency paths, and analysis model requirements across diagnostics, competition, positioning, marketing mix, growth, consumer insight, measurement, execution, and sales monetization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business teams use this skill as a marketing strategy knowledge base for selecting task types, dependency paths, and required analysis components. Agents can use it to produce marketing guidance and structured strategy outputs when the required Universal Task OS dependency is available, or to provide reference-only lookup when it is not. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to automatically install the universal-task-os dependency, which may add behavior the user has not reviewed. <br>
Mitigation: Require explicit approval of the universal-task-os source and version before installation, and use reference-only mode when that approval is not available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjiaocheng/marketing-strategy-domain) <br>
- [Marketing catalog](artifact/references/marketing-catalog.md) <br>
- [Marketing requirements](artifact/references/marketing-requirements.md) <br>
- [Exemplars index](artifact/references/exemplars.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text] <br>
**Output Format:** [Markdown and structured text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Full strategy workflow depends on the external universal-task-os skill; without it, use is limited to reference lookup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
