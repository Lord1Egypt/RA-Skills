## Description: <br>
Fetches Legion Hardware ASR transcripts after intent clarification and produces outreach insight reports from transcript text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[legionspace-hackathon](https://clawhub.ai/user/legionspace-hackathon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, operations, and customer outreach teams use this skill to summarize completed ASR recordings, confirm the intended time window and analysis focus, and generate transcript-grounded outreach reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetched transcripts, script stdout, and generated reports may contain sensitive business or customer information. <br>
Mitigation: Run the skill only in approved environments and handle transcript-derived outputs as sensitive data. <br>
Risk: A JWT or Legion API endpoint configured for the wrong environment could expose data or send requests to an unintended service. <br>
Mitigation: Provide the auth token through the intended Authorization or environment channel, verify the endpoint before use, and avoid untrusted LEGION_HARDWARE_BASE_URL values. <br>
Risk: Ambiguous user requests could lead to analysis over an unintended time window or focus area. <br>
Mitigation: Use the built-in intent parsing and clarification flow before fetching recordings; apply defaults only after confirmation or explicit default acceptance. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/legionspace-hackathon/legion-loan-outreach-insight) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON script output plus Markdown or text report content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output is a report page; users can request text-only or custom export-oriented delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
