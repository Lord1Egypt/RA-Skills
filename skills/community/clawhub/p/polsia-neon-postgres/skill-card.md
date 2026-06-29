## Description: <br>
Use Neon PostgreSQL conventions for Polsia apps, including migration patterns and DATABASE_URL usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentlevier](https://clawhub.ai/user/agentlevier) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building Polsia apps use this skill to follow Neon PostgreSQL connection and migration conventions, including DATABASE_URL usage, start-time migrations, and parameterized queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated migration examples may affect live data if applied without review, especially destructive rollback statements such as DROP TABLE. <br>
Mitigation: Review generated migrations against the target database and environment before running them in an application start command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentlevier/polsia-neon-postgres) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown with JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance-only; no executable files are included.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
