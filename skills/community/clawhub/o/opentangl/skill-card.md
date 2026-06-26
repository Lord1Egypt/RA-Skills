## Description: <br>
OpenTangl configures an autonomous development loop for JavaScript and TypeScript projects that plans work, writes and verifies code, creates pull requests, reviews diffs, and can merge changes across one or more repositories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[8co](https://clawhub.ai/user/8co) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to set up OpenTangl for JavaScript and TypeScript projects, detect project metadata, create project and vision configuration, prepare LLM provider settings, and run a first autonomous development cycle. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill configures autonomous repository changes, pull requests, reviews, and merges using the user's GitHub identity. <br>
Mitigation: Use a dedicated least-privilege GitHub identity or token where possible, test on a non-critical repository first, and keep branch protection or required human review enabled for merges. <br>
Risk: The skill depends on external OpenTangl code and LLM provider configuration before it can operate. <br>
Mitigation: Review and pin the external OpenTangl code before running it, and keep API keys in a gitignored .env file created by the user. <br>
Risk: Autonomous code changes may fail verification or require human review before merge. <br>
Mitigation: Run configured build, test, lint, or typecheck commands before committing or merging, and review generated pull requests after the first cycle. <br>


## Reference(s): <br>
- [OpenTangl ClawHub release](https://clawhub.ai/8co/opentangl) <br>
- [OpenTangl GitHub repository](https://github.com/8co/opentangl) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with YAML, dotenv, and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance and configuration files such as projects.yaml and product-vision.md; expects node, git, and gh to be available.] <br>

## Skill Version(s): <br>
0.1.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
