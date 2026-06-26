## Description: <br>
Research any person using the Nyne Deep Research API by submitting an email, phone, social URL, or name, then retrieve a dossier with psychographic profile, social graph, career analysis, conversation starters, and approach strategy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MichaelFanous2](https://clawhub.ai/user/MichaelFanous2) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and authorized users use this skill to submit a person identifier to Nyne Deep Research and retrieve a dossier for relationship research, outreach preparation, or due diligence. Use should be limited to lawful, authorized cases where sending personal identifiers to Nyne is permitted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends personal identifiers to an external Nyne API. <br>
Mitigation: Require explicit user confirmation and a lawful, authorized purpose before submitting any email, phone number, social profile, or name. <br>
Risk: Generated dossiers may contain sensitive personal data. <br>
Mitigation: Treat results as sensitive data, minimize retention, and avoid displaying or storing sections that are not necessary for the user's authorized task. <br>
Risk: API secrets may be exposed if stored in broadly sourced shell profiles or displayed in logs. <br>
Mitigation: Store Nyne credentials in a restricted environment file or secret manager and avoid echoing full secret values. <br>
Risk: Phone and multi-profile lookups increase privacy and misuse risk. <br>
Mitigation: Prefer the least sensitive identifier that can satisfy the task and avoid phone or multi-profile lookups unless clearly necessary. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/MichaelFanous2/nyne-deep-research) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/MichaelFanous2) <br>
- [Nyne API](https://api.nyne.ai) <br>
- [Nyne Deep Research endpoint](https://api.nyne.ai/person/deep-research) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Asynchronous API flow; submits person identifiers and polls for JSON dossier results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
