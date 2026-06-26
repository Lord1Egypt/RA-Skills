## Description: <br>
Run OpenAI Codex CLI from OpenClaw for coding tasks in a target project directory. Use when the user asks OpenClaw to use Codex for implementation, debugging, refactoring, review, or scripted coding workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cecwxf](https://clawhub.ai/user/cecwxf) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to have OpenClaw delegate implementation, debugging, refactoring, review, and scripted coding tasks to the Codex CLI in a specified repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Codex can read, change, and run code in the selected repository. <br>
Mitigation: Run the skill only from the intended repository, prefer a version-controlled branch, and review diffs after execution. <br>
Risk: Untrusted task text can be unsafe when placed into hand-built shell command strings. <br>
Mitigation: Use proper argument passing or quoting before invoking shell commands. <br>
Risk: Missing Codex CLI installation or authentication blocks the workflow. <br>
Mitigation: Verify `codex --version` and complete Codex sign-in before delegating work. <br>


## Reference(s): <br>
- [OpenAI Codex Operator](https://clawhub.ai/cecwxf/openai-codex-operator) <br>
- [OpenAI Codex](https://developers.openai.com/codex) <br>
- [OpenAI Codex CLI](https://developers.openai.com/codex/cli) <br>
- [OpenAI Codex Quickstart](https://developers.openai.com/codex/quickstart) <br>
- [Codex Docs Summary](references/codex-doc-summary.md) <br>
- [Codex Usage Recipes](references/codex-usage-recipes.md) <br>
- [Codex Example Runner](scripts/run-codex-example.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
