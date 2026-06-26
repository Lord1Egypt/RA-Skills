## Description: <br>
AI security testing and evaluation CLI for running red-team evaluations, checking vulnerabilities, and reviewing results for AI products. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juhengwu](https://clawhub.ai/user/juhengwu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security engineers and developers use this skill to connect a configured Know Your AI product, inspect available evaluations and datasets, launch red-team evaluation runs, and review run history and results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required KNOW_YOUR_AI_DSN credential grants access to a configured Know Your AI product. <br>
Mitigation: Use only a DSN from the expected Know Your AI dashboard, treat it as a secret, and avoid sharing logs or command output that may reveal connection details. <br>
Risk: Running an evaluation can create remote evaluation history, consume service quota, and trigger tests against the configured product. <br>
Mitigation: Run doctor first to verify the target host and product, then use evaluation limits such as max prompts and timeout values appropriate for the environment. <br>


## Reference(s): <br>
- [Know Your AI homepage](https://knowyourai.hydrox.ai) <br>
- [HydroxAI](https://hydrox.ai) <br>
- [ClawHub skill page](https://clawhub.ai/juhengwu/know-your-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, API calls] <br>
**Output Format:** [Markdown and terminal text from Node.js CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18 or newer and the KNOW_YOUR_AI_DSN environment variable.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
