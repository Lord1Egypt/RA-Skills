## Description: <br>
Discover and resolve open source GitHub issues across community repos during idle time, including issue triage, forking, fixes, and pull request creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kbo4sho](https://clawhub.ai/user/kbo4sho) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and maintainers use this skill to find approachable open source issues, evaluate whether they are suitable for agent work, implement focused fixes, and open pull requests with required disclosure. It is suited for community contribution workflows that intentionally permit an agent to act on GitHub through a configured token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make public GitHub changes through forks, commits, and pull requests. <br>
Mitigation: Install only when this behavior is intended, start with --dry-run, avoid --auto or --yes until reviewed, and use repository allowlists. <br>
Risk: The skill may run tests or commands in third-party repositories. <br>
Mitigation: Run unknown repositories in a sandbox and review candidate issues before allowing changes. <br>
Risk: The security evidence notes local token reading and token-prefix echo behavior. <br>
Mitigation: Use a dedicated least-privileged GitHub token and remove the local token-read and token-prefix echo before use. <br>


## Reference(s): <br>
- [OSS Contributor ClawHub Page](https://clawhub.ai/kbo4sho/oss-contributor) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown status summaries, pull request text, code changes, shell commands, and JSON activity logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create forks, branches, commits, pull requests, and local activity or history files when run with write-enabled options.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
