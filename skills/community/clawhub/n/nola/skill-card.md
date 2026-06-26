## Description: <br>
Nola is an AI engineering squad lead that dispatches 14 specialist agents to build, test, review, document, and ship code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flikq](https://clawhub.ai/user/flikq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill in OpenClaw to coordinate software development work such as feature implementation, bug investigation, code review, testing, documentation, deployment planning, and release tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can coordinate subagents that modify repositories and prepare release actions. <br>
Mitigation: Review diffs before release steps and explicitly require approval before commits, pushes, PRs, server startup, test execution, or scraping outputs. <br>
Risk: Broad multi-agent delegation can perform more work than intended if the user prompt is vague. <br>
Mitigation: Use narrow prompts with explicit scope, files, deliverables, and approval boundaries. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/flikq/nola) <br>
- [Publisher profile](https://clawhub.ai/user/flikq) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown status updates, delegated agent task prompts, code changes, shell commands, configuration snippets, and review summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May coordinate multiple subagents and repository-modifying workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
