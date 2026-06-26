## Description: <br>
Tracks AI API usage by logging calls, reporting spending by model and period, and suggesting cheaper model choices to optimize costs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OdinBot33](https://clawhub.ai/user/OdinBot33) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to log AI API calls, estimate cost from token counts, and review spend by model, day, task type, and source. The reports help users identify high-cost usage patterns and choose cheaper models for simpler tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Usage logging creates a local usage.jsonl file that may contain task descriptions or other user-provided details. <br>
Mitigation: Avoid logging secrets, full prompts, customer data, or sensitive project details in the description field, and confirm that local log creation is acceptable before installing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/OdinBot33/oee-ai-cost-tracker) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Pricing data](artifact/pricing.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets; runtime scripts produce JSONL records and terminal text reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a local usage.jsonl file in the skill directory when logging usage; no external dependencies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
