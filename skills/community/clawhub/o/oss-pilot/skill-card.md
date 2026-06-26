## Description: <br>
End-to-end open-source GitHub contribution automation that helps agents discover issues, implement fixes, open pull requests, monitor CI and review status, and retain repository-specific contribution context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cypherm](https://clawhub.ai/user/cypherm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and open-source contributors use this skill to identify suitable GitHub issues, make scoped fixes, prepare pull requests, respond to automation and review feedback, and keep local lessons for future contributions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify local repositories and make public GitHub changes through broad contribution workflows. <br>
Mitigation: Prefer explicit oss-prefixed commands, verify the authenticated gh account and target repository before use, and review each proposed git or GitHub action before approval. <br>
Risk: Build, lint, test, and package-manager commands from unfamiliar repositories can execute untrusted project scripts. <br>
Mitigation: Run unfamiliar repositories in a container or VM and review package scripts, Makefile targets, and other build hooks before approving execution. <br>
Risk: Repository profiles and PR context files may retain contribution history, maintainer notes, and workflow decisions in ./oss-pilot-data. <br>
Mitigation: Periodically inspect ./oss-pilot-data and remove stale or sensitive profiles and archived PR context. <br>


## Reference(s): <br>
- [Oss Pilot on ClawHub](https://clawhub.ai/cypherm/oss-pilot) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Claude Code](https://claude.ai/code) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command snippets, code-change instructions, PR descriptions, and local profile/context files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update ./oss-pilot-data profiles and PR context files, run git and gh workflows, and propose public GitHub actions for user approval.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
