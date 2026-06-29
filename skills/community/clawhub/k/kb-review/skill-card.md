## Description: <br>
Generate and save knowledge-base reviews such as literature reviews, research gaps, onboarding notes, stage summaries, and experiment suggestions based on existing KB sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myd2002](https://clawhub.ai/user/myd2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge-base users use this skill to synthesize existing personal or team Paper-KB sources into reviews, research-gap analyses, onboarding notes, stage summaries, and experiment suggestions. It is designed to ground outputs in reviewed KB material and save generated Markdown back to the knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests Gitea admin-level access and includes helpers that can mutate repositories and persistent system configuration. <br>
Mitigation: Install only in a controlled Paper-KB/Gitea environment and prefer a least-privilege token limited to the specific KB repositories and paths. <br>
Risk: Generated reviews and onboarding documents are saved back to knowledge-base repositories by default, including shared team KBs. <br>
Mitigation: Require user confirmation and human review before saving generated content to shared repositories. <br>
Risk: The artifact contains a hardcoded Gitea URL and unpinned Python dependencies. <br>
Mitigation: Review the configured endpoint and pin dependencies before production deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/myd2002/skills/kb-review) <br>
- [Publisher profile](https://clawhub.ai/user/myd2002) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON helper-script responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should include a sources section and should state when the knowledge base lacks enough material.] <br>

## Skill Version(s): <br>
3.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
