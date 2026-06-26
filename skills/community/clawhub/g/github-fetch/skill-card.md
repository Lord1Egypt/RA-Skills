## Description: <br>
Provides fallback workflows and helper shell scripts for cloning GitHub repositories and fetching individual files when direct GitHub access is unreliable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[d9g](https://clawhub.ai/user/d9g) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to retrieve public GitHub repositories or individual files through SSH, direct HTTPS, and CDN/proxy fallbacks when GitHub connectivity is unreliable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted repository URLs, branch names, refs, or output paths may lead the clone script to run unintended shell commands. <br>
Mitigation: Use only trusted inputs, review commands before execution, and prefer fixing shell quoting and validation in github-clone.sh before installation. <br>
Risk: The scripts may use local SSH credentials and may route public fetches through third-party mirrors or CDNs. <br>
Mitigation: Do not use mirror or CDN fallback paths for private repositories, and confirm credential and network exposure is acceptable before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/d9g/github-fetch) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with shell command examples and script-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose running bundled shell scripts with repository URLs, refs, branches, timeouts, and output paths.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
