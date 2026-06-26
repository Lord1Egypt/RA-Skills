## Description: <br>
Collects HouseSigma listing data through automated or manual workflows and saves it into a Hauscout SQLite database for dashboard updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sonim1](https://clawhub.ai/user/sonim1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers or operators maintaining the local Hauscout project use this skill to collect HouseSigma listings, manage search profiles, and update the SQLite-backed dashboard data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically modify a local SQLite database and publish those changes through Git and Vercel workflows. <br>
Mitigation: Back up the SQLite database, confirm the Git remote and deployment target are intended for this data, and add a manual review step before pushing or deploying collected data. <br>
Risk: The workflow depends on a local Hauscout project and collector script outside the skill artifact. <br>
Mitigation: Use the skill only when you control the referenced Hauscout project and have reviewed the local collect.ts script. <br>
Risk: Automated collection may trigger service rate limits or headless browsing blocks. <br>
Mitigation: Keep request delays, review collection volume before scheduling cron runs, and use headed browser checks when blocked. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and SQL command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local file paths and database commands that require review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
