## Description: <br>
Persona Creator analyzes a user's Markdown chat history to create, refresh, delete, and apply persona JSON profiles for style-aware role play. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taget](https://clawhub.ai/user/taget) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn workspace chat memories into reusable persona profiles, refresh or forget those profiles, and temporarily answer in a selected profile's communication style. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes local chat-history memory files into persistent persona profiles, which can expose sensitive personal data if broad or sensitive histories are used. <br>
Mitigation: Use a narrow memory directory, avoid histories containing secrets or sensitive personal data, and review generated persona JSON before using role-play mode. <br>
Risk: The security summary notes that sensitive intermediate data is insufficiently contained during persona generation. <br>
Mitigation: Delete /tmp/persona_meta.json, /tmp/persona_analysis_prompt.txt, /tmp/persona_analysis_result.json, and unneeded persona backups after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/taget/persona-creator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown status messages, JSON persona files, and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires at least 10 extracted user messages; may create temporary analysis files and persona backups during use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
