## Description: <br>
A newspaper and magazine PDF download skill that uses CLI commands to query collected issues, locate specific issues, and return PDF download links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1787812757](https://clawhub.ai/user/1787812757) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to check recent newspaper and magazine updates, resolve a requested publication issue, and obtain JSON results containing issue metadata and, when configured with an Import Token, PDF download links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Import tokens and generated download links may function like credentials if exposed in chat logs, command history, saved files, or shared outputs. <br>
Mitigation: Keep config.json private, prefer environment or private configuration for tokens, use --no-save for routine queries, and do not share generated links publicly. <br>
Risk: The skill connects to pick-read.vip and the evidence security verdict is suspicious because token handling requires review before installation. <br>
Mitigation: Install only if the publisher and pick-read.vip service are trusted, review the security guidance before use, and validate network behavior in the target environment. <br>
Risk: The artifact script disables normal HTTPS certificate verification while retrying API requests. <br>
Mitigation: Review this behavior before deployment and consider restoring standard HTTPS verification where the runtime environment supports it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/1787812757/newspaper-download-skill) <br>
- [pick-read.vip](https://pick-read.vip) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON returned by CLI commands, with Markdown guidance for command usage and token setup.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Query commands can run without authentication; download links require an Import Token and should be treated as sensitive.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
