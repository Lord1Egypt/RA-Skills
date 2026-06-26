## Description: <br>
A self-evolving novel writing engine for OpenClaw agents that supports context preparation, chapter writing, multi-role review, continuity tracking, quality checks, foreshadowing management, character voice management, and token cost optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[awoo129](https://clawhub.ai/user/awoo129) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and writers use this skill to manage long-form Chinese fiction projects, generate chapter context or drafts, review chapters, track continuity, and export manuscript outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send unpublished manuscript, world-building, character notes, chapter plans, and rewrite inputs to third-party LLM providers. <br>
Mitigation: Install and use it only when that data sharing is acceptable; avoid sensitive manuscript material unless the configured provider and account meet the user's privacy requirements. <br>
Risk: The skill requires sensitive API credentials and includes paths that use SenseNova or DeepSeek API keys. <br>
Mitigation: Use dedicated API keys, store them in environment variables or a reviewed secret manager, and rotate or revoke them if exposed. <br>
Risk: Helper scripts and lesson sync features may run with project-directory access and external API behavior that should be reviewed before use. <br>
Mitigation: Run the skill in a dedicated project directory and review DeepSeek helper scripts and lesson sync targets before executing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/awoo129/lobster-novel) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/awoo129) <br>
- [Project homepage](https://github.com/awoo129/lobster-novel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, plain text, JSON-like project state, exported manuscript files, and CLI-oriented shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or update local novel project files and may call third-party LLM APIs when API keys are configured.] <br>

## Skill Version(s): <br>
1.4.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
