## Description: <br>
Use the idealista CLI to search Idealista listings by location (city, town, area, street) and fetch listing details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pjtf93](https://clawhub.ai/user/pjtf93) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and agents use this skill to run Idealista marketplace searches, retrieve listing details, and request table or JSON output for scripting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a local idealista-cli executable and network access to Idealista. <br>
Mitigation: Install and run it only from a trusted local PATH, and review generated commands before execution. <br>
Risk: Idealista searches, listing lookups, and IDEALISTA_* configuration values may expose sensitive query or credential data in prompts, logs, or shared output. <br>
Mitigation: Avoid including sensitive personal details in searches and keep IDEALISTA_* credentials out of prompts, logs, and shared transcripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pjtf93/idealista-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI flag guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The referenced CLI can return table or JSON output depending on command flags.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
