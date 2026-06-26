## Description: <br>
Helps users search and interpret Hundun courses, extract course methods and models, and apply Hundun innovation workflows to business questions such as value propositions, ideas, selling points, pricing, and market entry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hundun-online](https://clawhub.ai/user/hundun-online) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to work with Hundun course search, recommendations, learning paths, and transcript-based summaries, or to structure commercial innovation tasks using the bundled Hundun playbooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends course searches, business questions, refinements, and related session metadata to Hundun/AIA services. <br>
Mitigation: Use the skill only when the provider's data handling is acceptable, and avoid confidential strategy, personal data, or proprietary plans unless that sharing has been approved. <br>
Risk: The skill requires a Hundun API key and may guide users through credential setup. <br>
Mitigation: Prefer setting HUNDUN_API_KEY as an environment variable, avoid pasting keys into chat when possible, and rotate any exposed credential. <br>
Risk: The security verdict is suspicious because credential handling and remote data submission need careful review. <br>
Mitigation: Review the skill, its requested environment variables, and its provider calls before deployment; install only where the remote service dependency is acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hundun-online/hundun) <br>
- [Publisher profile](https://clawhub.ai/user/hundun-online) <br>
- [Authentication and troubleshooting](references/auth-and-troubleshooting.md) <br>
- [Course workflow](references/course-workflow.md) <br>
- [Innovation tool shared playbook](references/innovation-tools/_shared-playbook.md) <br>
- [Asymmetric entry finder](references/innovation-tools/asymmetric-entry-finder.md) <br>
- [Idea exploder](references/innovation-tools/idea-exploder.md) <br>
- [Pricing reframer](references/innovation-tools/pricing-reframer.md) <br>
- [Selling point innovator](references/innovation-tools/selling-point-innovator.md) <br>
- [Value proposition one-liner](references/innovation-tools/value-proposition-one-liner.md) <br>
- [Hundun API key portal](https://tools.hundun.cn/h5Bin/aia/#/keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with occasional bash commands or configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include course recommendations, learning paths, transcript summaries, innovation analysis, and authentication guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
