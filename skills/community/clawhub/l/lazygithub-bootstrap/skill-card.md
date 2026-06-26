## Description: <br>
Publish, bootstrap, or tidy a GitHub repository so the README and full GitHub About metadata stay in sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanjo92](https://clawhub.ai/user/hanjo92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, publish, or tidy GitHub repositories while keeping README content and GitHub About metadata aligned. It helps agents infer repository descriptions, homepage values, and topics, then verify the final GitHub metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may publish local files or update GitHub repository metadata with unintended visibility, descriptions, homepage values, or topics. <br>
Mitigation: Confirm the target repository, public or private visibility, README content, description, homepage, topics, and push intent before allowing the workflow to run. <br>


## Reference(s): <br>
- [Prompt Templates](references/prompt-templates.md) <br>
- [ClawHub skill page](https://clawhub.ai/hanjo92/lazygithub-bootstrap) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise verification summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local README content and GitHub repository metadata when the agent executes the suggested workflow.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
