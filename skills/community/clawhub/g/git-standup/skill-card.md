## Description: <br>
Analyzes Git commit history to generate structured daily, weekly, or date-range standup reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antonia-sz](https://clawhub.ai/user/antonia-sz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to summarize Git commits by date range, author, repository, directory, and commit type for standup updates or work reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may include sensitive project activity from local Git history. <br>
Mitigation: Review each report before sharing it outside the intended audience. <br>
Risk: The README includes direct GitHub clone instructions for an external repository whose executable was not part of the submitted artifact. <br>
Mitigation: Inspect the external repository before using that direct clone path. <br>
Risk: The skill can write output to a user-selected path. <br>
Mitigation: Choose output paths deliberately to avoid overwriting or exposing files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/antonia-sz/git-standup) <br>
- [Publisher profile](https://clawhub.ai/user/antonia-sz) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown or JSON report text, optionally written to a selected output path.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports can be filtered by date range, author, repository path, output format, and grouping mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, skill.yaml, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
