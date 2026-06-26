## Description: <br>
Northbase lets an agent read, write, list, and sync the user's persistent notes and workspace files through the Northbase CLI when the user explicitly requests file interaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ethanbernheim-maker](https://clawhub.ai/user/ethanbernheim-maker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Northbase is for people who want an agent to access and maintain persistent notes and workspace files shared through Northbase. Use it only for explicit requests to read, write, list, or sync those stored files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write or overwrite requests may persist and sync across devices. <br>
Mitigation: Confirm the user's intent before writes or overwrites, read existing files first with northbase get, and write updates through northbase put. <br>
Risk: The CLI may be authenticated to an unintended Northbase account or workspace. <br>
Mitigation: Confirm the Northbase CLI is logged into the correct account before using the skill, especially before reading or changing files. <br>
Risk: Bypassing the Northbase CLI can create stale or inconsistent file state. <br>
Mitigation: Use only the northbase CLI for file operations and do not read local mirror directories or query backing services directly. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ethanbernheim-maker/northbase) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to read, write, list, or sync user workspace files through the Northbase CLI when explicitly requested.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
