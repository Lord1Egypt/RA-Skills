## Description: <br>
Facebook browser automation skill for posting, reading comments, generating intelligent replies, and tracking comment threads for brand engagement and high-frequency community operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x-rayluan](https://clawhub.ai/user/x-rayluan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External social media operators and agents use this skill to automate Facebook posting, comment reading, reply drafting or posting, and follow-up engagement for brand/community operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act through a logged-in Facebook browser profile and post public replies automatically. <br>
Mitigation: Prefer Draft or Query mode for normal use, require human approval for sensitive replies, and keep the documented per-session reply limit. <br>
Risk: The skill stores comments, receipts, logs, and screenshots that may contain social data. <br>
Mitigation: Use a dedicated low-risk browser profile or account where possible and periodically delete stored comments, receipts, logs, and screenshots. <br>
Risk: The security verdict is suspicious because the skill combines social posting automation with limited controls around stored social data. <br>
Mitigation: Inspect the referenced local scripts before use and set explicit monitoring and posting limits before allowing execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/x-rayluan/openclaw-mark) <br>
- [Publisher profile](https://clawhub.ai/user/x-rayluan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON receipt examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local receipts, comment snapshots, logs, and screenshots under the configured workspace.] <br>

## Skill Version(s): <br>
1.0.1 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
