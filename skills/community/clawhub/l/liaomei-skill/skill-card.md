## Description: <br>
A bilingual social-coaching skill that helps users record, review, and improve dating and invitation attempts while rejecting manipulative PUA tactics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wnzzer](https://clawhub.ai/user/wnzzer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill as a respectful dating and social-growth coach for logging social attempts, practicing conversations, reviewing outcomes, and tracking progress over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill records sensitive dating and social-coaching details in local files. <br>
Mitigation: Use aliases instead of real names, check the reported DATA_DIR path on first use, and periodically review or delete generated files and backups. <br>
Risk: The skill can save information during journaling workflows. <br>
Mitigation: State clearly when something should not be saved and review proposed records before confirming persistence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wnzzer/liaomei-skill) <br>
- [Field Guide](references/field-guide.md) <br>
- [Analytics](references/analytics.md) <br>
- [Mindset](references/mindset.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local JSON and JSONL records after user confirmation.] <br>

## Skill Version(s): <br>
2.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
