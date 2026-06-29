## Description: <br>
Extracts a user's writing voice from text samples via SICO comparative analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers and developers use this skill to collect authorized writing samples, derive a SICO voice profile, and create registers that guide later writing generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Writing samples and extracted voice profiles may contain sensitive personal, client, employer, or regulated information and are stored locally. <br>
Mitigation: Use only samples you are comfortable storing on disk, inspect and delete files under ~/.claude/voice-profiles as needed, and avoid confidential or regulated text without a retention and deletion plan. <br>
Risk: The skill's privacy and consent posture is unclear for samples that may come from other people or shared contexts. <br>
Mitigation: Use only your own writing or material you are authorized to process, and confirm consent before extracting or reusing another person's writing style. <br>
Risk: A generated voice profile can make later text resemble a specific person's writing style. <br>
Mitigation: Use generated profiles only for authorized writing workflows and review downstream output for consent, attribution, and impersonation concerns. <br>


## Reference(s): <br>
- [Scribe plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/scribe) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown voice profile and register files, a JSON manifest, and inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Profiles are written under ~/.claude/voice-profiles/{name}; baseline comparisons are described as in-memory during extraction.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
