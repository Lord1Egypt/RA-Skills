## Description: <br>
Shapes agent behavior via instruction framing and style transfer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent authors use this skill to structure prompts, skill instructions, style-transfer requests, and multi-agent review dispatches for clearer agent behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad review-planning activation could produce reviewer instructions that drift from the intended scope or independence model. <br>
Mitigation: Review generated reviewer instructions before use and confirm they preserve the intended scope, independence, and higher-priority system or developer constraints. <br>
Risk: Prompt-structuring guidance can introduce incorrect or misleading review framing if applied mechanically. <br>
Mitigation: Use the generated framing as guidance and have a human reviewer check it against the actual task, review goals, and constraints before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-imbue-latent-space-engineering) <br>
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/imbue) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text] <br>
**Output Format:** [Markdown guidance and prompt patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No shell execution, credential use, persistence, or destructive behavior indicated by security evidence.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
