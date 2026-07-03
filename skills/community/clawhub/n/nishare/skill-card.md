## Description: <br>
Use when the user wants to publish, update, or explain how to publish AI-generated HTML, image, or document content to Nishare via its API, needs curl examples, API-Key/Bearer authentication, workspace targeting, payload validation rules, or wants an agent prompt that returns a Nishare shareUrl. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[momofa](https://clawhub.ai/user/momofa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create or update Nishare shares for generated HTML, Markdown, and image content. It provides API endpoints, authentication options, payload rules, response handling, and curl examples for returning a shareUrl to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may publish sensitive content or private documents to an external sharing service. <br>
Mitigation: Review generated payloads before publishing and avoid uploading secrets or private documents unless sharing is intended. <br>
Risk: Nishare API credentials may be exposed if pasted into prompts, examples, or published content. <br>
Mitigation: Store credentials in environment variables or a secret manager and use placeholder keys in prompts and examples. <br>


## Reference(s): <br>
- [Nishare API Reference](references/api.md) <br>
- [Server-resolved source repository](https://github.com/momofa/nishare) <br>
- [ClawHub skill page](https://clawhub.ai/momofa/skills/nishare) <br>
- [Nishare production service](https://nishare.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with curl examples and JSON payload details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Nishare shareUrl responses, API error messages, validation matches, and authentication header guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
