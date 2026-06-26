## Description: <br>
Optimizes long or unclear user prompts into clearer, actionable instructions and may continue by executing the optimized prompt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjinhongmy-pixel](https://clawhub.ai/user/wangjinhongmy-pixel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to turn lengthy, scattered, or incomplete requests into clearer prompts before the agent responds. It is intended for prompt drafting and clarification workflows, with confirmation expected when intent, file paths, external actions, or high-impact steps are unclear. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically rewrite and execute ordinary user requests without clear opt-in. <br>
Mitigation: Use it manually for drafting or prompt improvement where possible, and review optimized prompts before allowing execution. <br>
Risk: A rewritten prompt could change user intent or lead to unwanted actions in coding, account, financial, file, external, or other high-impact workflows. <br>
Mitigation: Require confirmation before execution when intent is unclear, information is missing, actions may be irreversible, or the task affects sensitive systems. <br>


## Reference(s): <br>
- [Prompt Tuner ClawHub Release](https://clawhub.ai/wangjinhongmy-pixel/prompt-tuner) <br>
- [Publisher Profile](https://clawhub.ai/user/wangjinhongmy-pixel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown containing an optimized prompt code block followed by the agent's response or clarification request] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May proceed with the optimized prompt after rewriting unless the task requires clarification, confirmation, or missing information.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
