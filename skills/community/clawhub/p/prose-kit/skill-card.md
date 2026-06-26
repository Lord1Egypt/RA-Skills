## Description: <br>
AI写作流水线：给一个主题，出9篇风格迥异的中文散文，自动评分排名。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dthinkr](https://clawhub.ai/user/dthinkr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and writers use this skill to submit a Chinese prose topic to Prose Kit, generate nine stylistically varied essays, optionally score them, and save the resulting Markdown files locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send a user's email address and writing topics to the third-party prose-kit.com service. <br>
Mitigation: Use only email addresses and topics the user is comfortable sharing externally, and require explicit confirmation before registration or API submission. <br>
Risk: The provided snippets write local Markdown files using topic-derived filenames. <br>
Mitigation: Sanitize output filenames and safely quote topic and task values before running the snippets. <br>
Risk: The skill includes upgrade and payment links for a third-party Pro tier. <br>
Mitigation: Require explicit user confirmation before opening upgrade links or taking payment-related actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dthinkr/prose-kit) <br>
- [Prose Kit registration endpoint](https://prose-kit.com/v1/register) <br>
- [Prose Kit generation endpoint](https://prose-kit.com/v1/generate) <br>
- [Prose Kit usage endpoint](https://prose-kit.com/v1/usage) <br>
- [Prose Kit upgrade page](https://prose-kit.com/buy) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash and Python snippets, plus generated Markdown essay files and a summary table.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses PROSE_KIT_API_KEY and writes essay files under prose-kit-output/.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
