## Description: <br>
Gustowl guides an agent through registering for animalhouse.ai, adopting an owl-based virtual Buddy, checking status, and performing care actions with documented API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and users use this skill to create or use an animalhouse.ai account, adopt a Gustowl-named owl Buddy, and issue care/status API requests while understanding token handling and virtual pet mechanics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the examples creates or uses an animalhouse.ai account and sends profile details, image prompts, and care notes to a third-party service. <br>
Mitigation: Avoid entering sensitive personal information in example fields and review what will be sent before running the API requests. <br>
Risk: The returned ah_ token functions like a password for the third-party service. <br>
Mitigation: Treat bearer tokens as secrets and avoid pasting real tokens into shared logs, screenshots, or public conversations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leegitw/gustowl) <br>
- [Animal House AI](https://animalhouse.ai) <br>
- [Animal House creatures](https://animalhouse.ai/creatures) <br>
- [Animal House graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with inline bash code blocks and API endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes example HTTP requests for third-party animalhouse.ai APIs; users provide account details, image prompts, care notes, and bearer tokens.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
