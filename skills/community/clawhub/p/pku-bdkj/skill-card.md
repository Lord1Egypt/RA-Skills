## Description: <br>
PKU BDKJ helps agents use the PKU academic discussion room CLI to log in, search rooms, manage participant groups, create reservations, and cancel reservations for bdkj.pku.edu.cn. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjsoj](https://clawhub.ai/user/wjsoj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate the PKU BDKJ CLI for finding academic discussion rooms, checking availability, managing saved participant groups, and submitting or cancelling reservations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use stored university credentials to create or cancel real room reservations. <br>
Mitigation: Require manual confirmation for each login, reservation, cancellation, room, time, reason, and participant list before execution. <br>
Risk: Session and group data are stored locally and may expose account or participant information on shared machines. <br>
Mitigation: Use the skill only on trusted machines, protect local config files, and clear stored sessions and groups when no longer needed. <br>
Risk: The workflow depends on separate bdkj and info-auth tools. <br>
Mitigation: Install and use those tools only from trusted sources before allowing the skill to access credentials or perform reservations. <br>


## Reference(s): <br>
- [PKU BDKJ ClawHub page](https://clawhub.ai/wjsoj/pku-bdkj) <br>
- [PKU BDKJ service](https://bdkj.pku.edu.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with CLI commands and concise Chinese-facing operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May depend on local session state, saved participant groups, and university SSO credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
