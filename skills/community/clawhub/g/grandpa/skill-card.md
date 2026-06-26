## Description: <br>
Preserve your grandfather's stories, skills, life philosophy, and the quiet strength that held the family together using only memories the user provides. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realteamprinz](https://clawhub.ai/user/realteamprinz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and families use this skill to preserve memories, stories, practical skills, values, humor, and family roles associated with a grandfather. The skill helps organize user-entered memories into local Markdown and JSONL records and can answer reflective prompts based on those entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Personal family memories may be stored on the local device. <br>
Mitigation: Review the ~/.grandpa-skill/ folder and avoid entering details that should not be stored on the device. <br>
Risk: Reflective answers may feel personal because they are based on user-provided memories. <br>
Mitigation: Treat responses as memory-based assistance, keep source notes for entries, and avoid using the skill as a substitute for professional grief, medical, legal, or financial advice. <br>


## Reference(s): <br>
- [Grandpa Profile Template](templates/GRANDPA-PROFILE.md) <br>
- [ClawHub Release Page](https://clawhub.ai/realteamprinz/grandpa) <br>
- [Hermes Agent](https://github.com/NousResearch/hermes-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with local Markdown and JSONL file structures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided memories only; records are described as local files under ~/.grandpa-skill/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
