## Description: <br>
Publishes, edits, and configures Mowen notes through the Mowen Open API, including rich text, images, tags, publication status, and privacy settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jacobluo](https://clawhub.ai/user/jacobluo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to help an agent prepare and run Mowen note publishing, editing, and privacy-setting workflows. It is intended for users who already have a Mowen Open API key and want agent-assisted note creation with text and images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish or edit Mowen notes using the user's API key. <br>
Mitigation: Confirm the exact note content, target note ID, publication status, and privacy setting before running the generated command. <br>
Risk: Selected local images or image URLs can be uploaded to Mowen. <br>
Mitigation: Review every image path and URL first, and do not provide sensitive local files or private/internal URLs unless they are intended to be sent to Mowen. <br>
Risk: Passing an API key on the command line can expose it through shell history or process listings. <br>
Mitigation: Prefer the MOWEN_API_KEY environment variable for routine use. <br>


## Reference(s): <br>
- [Mowen Open API reference](references/mowen_api.md) <br>
- [ClawHub skill page](https://clawhub.ai/jacobluo/mowenskill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with JSON request examples and shell command invocations; the helper script returns JSON results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Mowen API key through MOWEN_API_KEY or an explicit command-line argument.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
