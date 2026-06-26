## Description: <br>
CI/CD pipeline anti-pattern analyzer -- detects hardcoded secrets, missing cache configs, skipped tests, unsafe deployments, no approval gates, and environment configuration issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use PipelineLint to scan CI/CD configuration and source files for pipeline quality, security, dependency, testing, deployment, and environment anti-patterns before committing or shipping changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hook installation can modify lefthook.yml and affect future commit or push workflows. <br>
Mitigation: Use normal scan mode for read-only analysis, run hook installation only when intended, and review lefthook.yml after install or uninstall. <br>
Risk: Passing a license key directly on the command line can expose it through shell history or process listings. <br>
Mitigation: Prefer PIPELINELINT_LICENSE_KEY or the documented OpenClaw configuration for license credentials. <br>


## Reference(s): <br>
- [PipelineLint homepage](https://pipelinelint.pages.dev) <br>
- [PipelineLint hook documentation](https://pipelinelint.pages.dev/docs/hooks) <br>
- [ClawHub skill page](https://clawhub.ai/suhteevah/pipelinelint) <br>
- [Publisher profile](https://clawhub.ai/user/suhteevah) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, HTML, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Plain text, JSON, HTML, and Markdown reports with shell commands for scans and optional hook operations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local analysis with tiered pattern access; optional lefthook integration can update repository hook configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
