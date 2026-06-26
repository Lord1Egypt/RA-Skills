## Description: <br>
Iteratively improves AI prompts by analyzing, rewriting, comparing, and refining them for clarity, structure, constraints, examples, and output format compliance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and prompt authors use this skill to improve underperforming prompts, design A/B prompt variants, and tune prompts for specific goals or models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt content may include secrets, customer data, or proprietary internal instructions. <br>
Mitigation: Review and redact sensitive content before using the skill in an agent session. <br>
Risk: An optimized prompt may change task intent or add constraints that do not fit the user's environment. <br>
Mitigation: Review generated prompts and test them against representative inputs before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/prompt-evolution-engine) <br>
- [Skill source](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown sections containing analysis, an optimized prompt, changes made, and expected impact.] <br>
**Output Parameters:** [Prompt content, goal, target model, max_tokens, style, and iterations when provided.] <br>
**Other Properties Related to Output:** [May generate A/B test variants, comparison notes, and test inputs for prompt evaluation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
