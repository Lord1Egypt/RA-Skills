## Description: <br>
Fetches and returns the daily text from the Spanish Watchtower Online Library at wol.jw.org/es when a user asks for JW daily text or related daily Bible content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djismgaming](https://clawhub.ai/user/djismgaming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve the current Spanish JW daily text from the official Watchtower Online Library and present it with the associated Bible citation, explanation, and source link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts wol.jw.org to retrieve the current daily text. <br>
Mitigation: Use the skill only in environments where outbound access to wol.jw.org is acceptable. <br>
Risk: The included helper script uses a shell-based curl call rather than the documented web_fetch approach. <br>
Mitigation: Review the helper before deployment and prefer web_fetch or a native HTTP library if executing the helper script. <br>


## Reference(s): <br>
- [Jwdiario on ClawHub](https://clawhub.ai/djismgaming/jwdiario) <br>
- [Watchtower Online Library - Spanish Daily Text](https://wol.jw.org/es/wol/h/r4/lp-s) <br>
- [Watchtower Online Library - Spanish](https://wol.jw.org/es/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown text with a source link] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Spanish source text should be presented without translation or alteration.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
