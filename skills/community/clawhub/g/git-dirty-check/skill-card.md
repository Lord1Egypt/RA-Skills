## Description: <br>
Read-only triage for a local git working tree that summarizes uncommitted changes and applies conservative risk flags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amitb-quantum](https://clawhub.ai/user/amitb-quantum) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to quickly summarize staged, unstaged, untracked, and conflicted local git changes before a commit, handoff, or local review. It helps identify conservative path- and filename-based risk flags without modifying repository state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may display repository file names, git status, diff stats, and limited non-sensitive diff samples. <br>
Mitigation: Avoid using it where even limited local repository change details should not be shown. <br>
Risk: Secret-bearing files could be present in a dirty working tree. <br>
Mitigation: Inspect matching secret-bearing filenames only at the filename level and do not print values from those files. <br>
Risk: Conservative risk flags can be incomplete or over-broad because they rely mostly on paths, filenames, and diff stats. <br>
Mitigation: Treat the output as triage guidance and run targeted review or project-specific checks before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amitb-quantum/git-dirty-check) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with structured sections and inline read-only git commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output follows a fixed section order and may cap changed-file listings, diff inspection, and sensitive-file detail.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
