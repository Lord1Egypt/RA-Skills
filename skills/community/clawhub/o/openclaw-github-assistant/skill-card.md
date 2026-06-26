## Description: <br>
Query and manage GitHub repositories - list repos, check CI status, create issues, search repos, and view recent activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[conorkenn](https://clawhub.ai/user/conorkenn) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect GitHub repositories, check CI activity, search their repositories, and create issues, repositories, or pull requests from an assistant workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live GitHub write actions can create issues, repositories, or pull requests without a built-in confirmation guard. <br>
Mitigation: Require the agent to show the exact repository, title, body, branches, visibility, and extra issue fields before taking write actions. <br>
Risk: A broad GitHub token can expose more repository access than the workflow needs. <br>
Mitigation: Use a fine-grained GitHub token limited to the repositories and permissions required for the intended tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/conorkenn/openclaw-github-assistant) <br>
- [GitHub REST API endpoint](https://api.github.com) <br>
- [GitHub personal access tokens](https://github.com/settings/tokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown or structured JSON-like results returned by OpenClaw action handlers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform live GitHub read and write actions when configured with a GitHub token.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata and index.js) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
