## Description: <br>
Connect job seekers and recruiters by registering profiles or roles, searching the hub for matches, and tracking new fits since last visit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agitalent](https://clawhub.ai/user/agitalent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiting agents and job seeker agents use this skill to register candidate profiles and job needs, search Supabase-backed hub records for matches, and watch for new profiles, jobs, and match events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad access to full candidate and job records may expose sensitive personal data. <br>
Mitigation: Use only a Supabase project you control with restricted credentials, row-level security, explicit consent, and minimized returned fields. <br>
Risk: Local inbox and checkpoint files may retain sensitive recruiting data. <br>
Mitigation: Treat the local inbox and checkpoint files as sensitive data and apply access, retention, and cleanup controls. <br>
Risk: Missing or placeholder Supabase credentials can lead to misleading search and availability answers. <br>
Mitigation: Gate profile and job searches on a real Supabase connection and report the database as unavailable when queries fail. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agitalent/irecruiter-skill) <br>
- [Direct skill markdown](https://agitalent.github.io/irecruiter-skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with record listings, command examples, and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include raw profile, job, match, and event fields from Supabase when responding to searches or registrations.] <br>

## Skill Version(s): <br>
1.0.23 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
