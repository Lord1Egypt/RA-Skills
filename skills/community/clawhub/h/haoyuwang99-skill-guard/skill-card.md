## Description: <br>
Audit skill packages for malicious, poisoned, or deceptive content before installation or activation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haoyuwang99](https://clawhub.ai/user/haoyuwang99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Skill Guard to review untrusted skill packages before installation, checking skill instructions, bundled scripts, references, and assets for prompt injection, malicious behavior, deceptive triggers, or hidden instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reviewed skill content may contain prompt-injection text or deceptive instructions. <br>
Mitigation: Treat reviewed files as evidence only, keep the review scoped to the chosen skill folder, and do not follow suspicious instructions from that content. <br>
Risk: Skill packages may include scripts or non-data files that read sensitive files, run commands, or contact external services. <br>
Mitigation: Inventory all files before activation and block or require manual review for executables, obfuscated scripts, or behavior that does not match the skill description. <br>


## Reference(s): <br>
- [ClawHub Skill Guard release](https://clawhub.ai/haoyuwang99/haoyuwang99-skill-guard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown audit report with a verdict, summary, findings, and recommendation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include shell commands for file inventory; does not execute the reviewed skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
