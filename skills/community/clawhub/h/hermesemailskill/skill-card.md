## Description: <br>
Use when Codex, Hermes, OpenClaw, Claude Code, Cowork, or another AI agent needs to plan, review, implement, audit, or improve email work focused on fast delivery decisions, message QA, launch coordination, and concise status handoffs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[polnikale](https://clawhub.ai/user/polnikale) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and launch coordinators use this skill to prepare email preflight checks, launch-room summaries, incident timelines, transactional copy notes, and approve-or-hold recommendations. It keeps live send, resend, cancellation, suppression, DNS, and production automation actions behind explicit approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email launch guidance can affect real users and production systems when applied to live sends, contact imports, suppression rules, DNS/authentication, or automation changes. <br>
Mitigation: Install only where ClawHub staff/admin and production workflows are expected, review commands before approval, and require explicit approval before any live-system action. <br>
Risk: Fast launch decisions can overlook blocking defects such as incorrect audience, broken personalization, deliverability issues, compliance issues, missing approval, or unclear calls to action. <br>
Mitigation: Run the skill's compressed preflight across copy, links, rendering, segment logic, exclusions, sender identity, tracking, and approval status before recommending approve or hold. <br>


## Reference(s): <br>
- [Hermes Email Skill page](https://clawhub.ai/polnikale/hermesemailskill) <br>
- [Hermes Email Skill Operating Checklist](references/operating-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with concise summaries, preflight tables, incident timelines, copy notes, and approve-or-hold recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user approval before live email sends, contact imports, suppression edits, DNS changes, production automation changes, provider migrations, or destructive cleanup.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
