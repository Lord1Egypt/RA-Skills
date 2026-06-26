## Description: <br>
Manage sales leads locally. Use when adding prospects, scoring leads, setting follow-ups, tracking conversions, or viewing funnels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales teams, founders, and operators use this skill to manage a local lead pipeline, including prospect creation, scoring, follow-up scheduling, conversion tracking, and funnel reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lead, deal, and follow-up data is stored locally in ~/.leads/leads.json. <br>
Mitigation: Protect local workstation access, back up the file when it matters to the business, and handle the file according to internal CRM data policies. <br>
Risk: Notes and lead records may contain sensitive business or personal information. <br>
Mitigation: Avoid storing secrets or unnecessary sensitive details in lead notes or deal records. <br>
Risk: Score, follow-up, and convert commands intentionally modify local CRM state. <br>
Mitigation: Review command arguments before execution and keep a backup if changes need to be reversible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xueyetianya/leads) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [BytesAgain feedback](https://bytesagain.com/feedback/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [Plain text stdout with local JSON data stored in ~/.leads/leads.json] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may create or update local lead records, scores, follow-ups, conversion status, and deal values.] <br>

## Skill Version(s): <br>
3.4.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
