## Description: <br>
Verify real outcomes before saying work is complete when implementing, fixing, configuring, or automating work where behavior must be confirmed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisang1000](https://clawhub.ai/user/jisang1000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI coding assistants use this skill to verify the actual user-visible outcome of setup, fixes, automation, configuration changes, and browser or script work before reporting completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outcome verification in production systems, real accounts, or irreversible workflows could cause unintended state changes if the check itself is not read-only. <br>
Mitigation: Keep verification read-only where possible, use dry-runs or smoke tests, and explicitly approve any state-changing verification step. <br>


## Reference(s): <br>
- [Final Review](references/final-review.md) <br>
- [Publish Notes](references/publish-notes.md) <br>
- [Example Publish Command](references/publish-command-example.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jisang1000/jisang1000-verification-before-completion) <br>
- [Publisher Profile](https://clawhub.ai/user/jisang1000) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown, Shell commands] <br>
**Output Format:** [Markdown guidance and concise completion reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend dry-runs, smoke tests, state inspection, or read-only verification before completion claims.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
