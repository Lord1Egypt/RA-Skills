## Description: <br>
Github Manager Free helps personal developers use the GitHub CLI to inspect and manage repository issues, pull requests, workflow runs, and structured command output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to ask an agent for GitHub CLI commands and guidance for daily repository maintenance, pull request review preparation, and CI failure triage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad GitHub command authority, including commands that can affect issues, pull requests, aliases, and workflow runs. <br>
Mitigation: Confirm any issue, pull request, alias, or workflow-rerun action explicitly, and prefer narrowly scoped GitHub tokens for the repositories and actions needed. <br>
Risk: The security review notes that the skill mixes read-only positioning with state-changing examples. <br>
Mitigation: Use review-only commands first and require explicit approval before running write-capable GitHub CLI commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/github-manager-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authenticated GitHub CLI; jq is optional for JSON filtering.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
