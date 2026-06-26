## Description: <br>
Automates pull request wrap-up for single PR merges and batch PR cleanup to reduce repetitive manual work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinasilva](https://clawhub.ai/user/chinasilva) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill when they ask an agent to merge a single pull request, clean up multiple pull requests, or enable auto-merge after checks pass. It guides the agent to prefer local repository scripts, fall back to GitHub CLI commands, and report completed, waiting, or blocked outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use the current GitHub CLI account to merge or auto-merge pull requests. <br>
Mitigation: Require an exact PR list and explicit confirmation before batch mode, auto-merge, local workflow scripts, or repository metadata updates. <br>
Risk: Batch defaults may allow multiple repository changes to merge after checks pass. <br>
Mitigation: Review each PR, CI state, and repository merge policy before enabling or accepting automated merges. <br>
Risk: Local scripts such as scripts/automerge, scripts/massageprs, or ensure-workflow-docs may change repository state. <br>
Mitigation: Review script contents and expected file changes before allowing the agent to run them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chinasilva/peter-pr-ops) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/chinasilva) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports whether PR work is completed, waiting on CI, blocked, or followed by a docs/SESSION-BOOTSTRAP.md refresh.] <br>

## Skill Version(s): <br>
1.2.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
