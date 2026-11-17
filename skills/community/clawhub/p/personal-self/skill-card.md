## Description: <br>
Personal Self is a de-identified personal profile template that lets users replace 12-dimension placeholders with their own information to create a reusable self-role skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals use this skill to build and maintain a reusable personal self-role profile. After filling the placeholders, an agent can respond from the user's stated identity, experience, preferences, abilities, motivations, and constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to store a broad set of sensitive real-life details in a reusable local profile. <br>
Mitigation: Avoid entering exact financial details, medical conditions, home or work locations, names of private contacts, internal access permissions, or anything unsuitable for reuse in future assistant sessions or shared skill directories. <br>
Risk: Filled profile data may influence future assistant responses beyond the immediate task. <br>
Mitigation: Keep placeholders for details that are not needed, review filled fields before reuse, and reset dimensions that should no longer affect the agent's behavior. <br>


## Reference(s): <br>
- [Personal Self skill page](https://clawhub.ai/wangjiaocheng/skills/personal-self) <br>
- [Publisher profile](https://clawhub.ai/user/wangjiaocheng) <br>
- [Character data template](references/character-data.md) <br>
- [Character behavior requirements](references/character-requirements.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance and editable Markdown profile data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses placeholder-based profile fields and asks for confirmation before writing personal information into the local character data file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
