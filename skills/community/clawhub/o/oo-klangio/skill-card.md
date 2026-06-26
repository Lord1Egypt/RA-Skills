## Description: <br>
Klangio (klang.io). Use this skill for ANY Klangio request - reading, creating, and updating data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate Klangio through an OOMOL-connected account for music transcription, beat and downbeat tracking, chord recognition, guitar strum recognition, source separation, job status checks, and result downloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation wording could cause the skill to be selected for an unintended Klangio-adjacent request. <br>
Mitigation: Use the skill only for explicit Klangio tasks and confirm that the requested action is in scope before running connector commands. <br>
Risk: Write actions can create Klangio processing jobs or otherwise change account state. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running actions tagged as write or destructive. <br>
Risk: Credential, connection, or billing steps may affect the user's OOMOL account. <br>
Mitigation: Run first-time setup or account remediation steps only after a matching command failure and user approval. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-klangio) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [Klangio Homepage](https://klang.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct the agent to inspect live connector schemas before running Klangio actions and to handle downloaded result files through OOMOL OSS transit storage.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
