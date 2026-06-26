## Description: <br>
Automatically search for low-competition GitHub bounty tasks and generate a concise report with bounty details and estimated difficulty. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[santosparra651-arch](https://clawhub.ai/user/santosparra651-arch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and bounty hunters use this skill to find open GitHub issues labeled as bounties with low comment counts, then review a sorted report before choosing tasks to pursue. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The listing name and CLI/package name differ slightly, which could lead users to install an unintended package. <br>
Mitigation: Confirm the ClawHub listing, publisher handle, and package command before installation or execution. <br>
Risk: The skill contacts GitHub's public API when run and depends on returned issue metadata. <br>
Mitigation: Run it in an environment where GitHub API access is expected, and review the generated issue links before acting on the report. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/santosparra651-arch/github-bounty-hunter-v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text report with issue titles, URLs, comment counts, and estimated difficulty] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Contacts GitHub's public API when executed; authenticated GitHub access may improve rate limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
