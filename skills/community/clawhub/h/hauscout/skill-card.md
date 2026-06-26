## Description: <br>
Hauscout helps an agent collect HouseSigma real estate listings, analyze them with AI, and store listing and price-history results in Neon PostgreSQL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sonim1](https://clawhub.ai/user/sonim1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Real estate data operators and developers use this skill to run a local Hauscout collection pipeline for targeted listing or profile collection, dry-run analysis, database review, and post-collection reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The collection workflow can scrape HouseSigma pages and may affect rate limits or site-policy compliance. <br>
Mitigation: Require explicit approval before scraping, start with --dry-run where practical, and keep the documented request delays in place. <br>
Risk: The workflow can write listing and price-history data to a Neon PostgreSQL database. <br>
Mitigation: Confirm the target database credentials and project context before any non-dry-run collection. <br>
Risk: The post-collection checklist can create local memory files and commit or push changes. <br>
Mitigation: Require the agent to ask before writing memory files, committing, or pushing to a remote Git repository. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and TypeScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include collection summaries, database query guidance, and post-run reporting steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
