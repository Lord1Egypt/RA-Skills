## Description: <br>
Automate lead capture in Supabase with Make.com email workflows, manage lead status, conversations, and track auto-reply delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[big-roman123](https://clawhub.ai/user/big-roman123) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Sales, support, and automation agents use this skill to capture lead details, store conversation history in Supabase, trigger Make.com auto-reply workflows, and monitor lead status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Supabase service-role key, which grants high-impact database access if exposed. <br>
Mitigation: Store the key only server-side, isolate the Supabase project for this workflow, and rotate the key immediately if exposure is suspected. <br>
Risk: Lead records and conversation content can include personal contact information and sales context. <br>
Mitigation: Confirm user consent and organization data-handling requirements before storing or using lead details for automated replies. <br>
Risk: The package exposes a deleteLead capability and other database actions that can change or remove lead data. <br>
Mitigation: Review or remove high-impact actions before deployment and restrict execution to the intended organization boundary. <br>
Risk: The security review flagged the release as suspicious because full database credentials and high-impact actions are under-documented. <br>
Mitigation: Install only in a tightly isolated Supabase project and verify organization isolation before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/big-roman123/leadklick) <br>
- [README](artifact/README.md) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Configuration] <br>
**Output Format:** [JSON objects with lead records, conversation records, automation status, and operation results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Supabase project URL, Supabase service-role key, organization UUID, and optional default priority.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, skill.json, SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
