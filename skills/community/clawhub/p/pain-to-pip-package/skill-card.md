## Description: <br>
Complete pipeline: Reddit pain scan -> cluster -> build pip-installable CLI tool -> push to GitHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minirr890112-byte](https://clawhub.ai/user/minirr890112-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide an automation pipeline that scans Reddit for developer pain points, clusters opportunities, generates pip-installable CLI tools, and publishes results to GitHub after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The pipeline can publish generated code to GitHub without clear limits or approval steps. <br>
Mitigation: Review the implementation before use, run locally or in dry-run mode first, and require manual approval before any push, package release, or scheduled production run. <br>
Risk: Repository or package publishing could expose broader access than intended. <br>
Mitigation: Use a repository-scoped GitHub token with minimal permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/minirr890112-byte/pain-to-pip-package) <br>
- [HermesMade GitHub repository](https://github.com/minirr890112-byte/HermesMade) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and pipeline descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe publishing generated code to GitHub; require review before push, package release, or scheduled production use.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
