## Description: <br>
Helps agents create Amazon SP-API Uploads API destinations through LinkFox and upload a selected file to the returned URL for A+ Content or Messaging workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and marketplace operators use this skill to create Amazon upload destinations and transfer binary files that downstream SP-API workflows can reference. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a LinkFox API key and Amazon SP-API seller context. <br>
Mitigation: Keep LINKFOXAGENT_API_KEY in the environment, avoid committing credentials, and run only in sessions intended for LinkFox/Amazon SP-API uploads. <br>
Risk: The upload workflow reads a user-selected local file and sends its bytes to an upload URL. <br>
Mitigation: Review the file path, content type, marketplace, and resource before execution, and upload only to destinations returned by the Amazon upload-destination workflow. <br>
Risk: Incorrect resource paths, marketplace IDs, or headers can cause failed uploads or uploads that cannot be used by downstream SP-API workflows. <br>
Mitigation: Match resource values to the downstream Amazon API documentation and pass the returned uploadDestination headers unchanged. <br>


## Reference(s): <br>
- [API reference](references/api.md) <br>
- [Amazon createUploadDestinationForResource](https://developer-docs.amazon.com/sp-api/reference/createuploaddestinationforresource) <br>
- [Amazon Create an upload destination](https://developer-docs.amazon.com/sp-api/docs/create-an-upload-destination) <br>
- [Amazon Messaging API reference](https://developer-docs.amazon.com/sp-api/docs/messaging-api-v1-reference) <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-amazon-store-uploads) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute bundled Python scripts that read a selected file, call LinkFox/Amazon SP-API upload destination endpoints, and PUT bytes to the returned upload URL.] <br>

## Skill Version(s): <br>
0.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
