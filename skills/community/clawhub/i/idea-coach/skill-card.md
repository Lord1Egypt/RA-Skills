## Description: <br>
AI-powered idea/problem/challenge manager with GitHub integration. Captures, categorizes, reviews, and helps ship ideas to repos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[udiedrichsen](https://clawhub.ai/user/udiedrichsen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and individual users use Idea Coach to capture ideas, problems, and challenges, organize them by priority and review cadence, and move ready work into GitHub repositories or issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Idea notes may include sensitive personal, business, or planning information stored in the local ideas file. <br>
Mitigation: Avoid storing secrets or highly confidential plans, and review the local storage path before use. <br>
Risk: GitHub actions can create public repositories or sync idea details to issues under the authenticated GitHub account. <br>
Mitigation: Confirm the active gh account, repository visibility, and issue contents before using shipping or sync commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/udiedrichsen/idea-coach) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores idea records locally and can invoke GitHub CLI commands when the user chooses GitHub actions.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
