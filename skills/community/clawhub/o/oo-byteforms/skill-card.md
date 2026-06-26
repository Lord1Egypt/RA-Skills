## Description: <br>
ByteForms (forms.bytesuite.io). Use this skill for ANY ByteForms request - searching and reading data. Whenever a task involves ByteForms, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to read ByteForms forms and form responses through an OOMOL-connected account. It is intended for users who want searchable access to ByteForms data without handling raw API tokens directly in the agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose ByteForms form data and responses from the connected account into the agent session. <br>
Mitigation: Install and use it only for ByteForms accounts and forms whose data is appropriate to share with the agent. <br>
Risk: The skill depends on the OOMOL oo CLI and server-side managed credentials. <br>
Mitigation: Confirm that the OOMOL publisher and oo CLI setup are trusted before connecting the ByteForms account. <br>


## Reference(s): <br>
- [ClawHub ByteForms skill page](https://clawhub.ai/oomol/oo-byteforms) <br>
- [ByteForms homepage](https://forms.bytesuite.io/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OOMOL oo CLI actions for get_form, list_forms, and list_form_responses.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
