## Description: <br>
Generate release notes for GitCode repositories from commits by tag range or since-date, grouped as feat/fix/docs/other, and output Markdown for Release pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[autoxj](https://clawhub.ai/user/autoxj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release managers use this skill to fetch GitCode commit history for a specified repository and range, then turn the commit data into concise Chinese Markdown release notes for GitCode Release pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads GitCode commit history available to the configured token. <br>
Mitigation: Use a revocable read-only GITCODE_TOKEN and run the skill only for intended repositories and ranges. <br>
Risk: Generated release notes can omit nuance or summarize commits incorrectly. <br>
Mitigation: Review the Markdown output against the source commit data before publishing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/autoxj/gitcode-release-notes) <br>
- [GitCode commits API documentation](https://docs.gitcode.com/docs/apis/get-api-v-5-repos-owner-repo-commits) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown release notes generated from JSON commit data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a required GITCODE_TOKEN and a repository range such as --since-date, --from, or --from with --to.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
