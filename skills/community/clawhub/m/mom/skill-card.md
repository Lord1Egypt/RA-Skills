## Description: <br>
Parenting co-pilot for mothers that tracks baby feeding, sleep, crying, and soothing patterns from parent-reported observations while clearly avoiding medical advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realteamprinz](https://clawhub.ai/user/realteamprinz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill as a local parenting memory aid for logging baby-care observations, summarizing routines, and finding parent-reported patterns in feeding, sleep, crying, soothing, milestones, and caregiver handoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Baby-care and caregiver-routine details are stored as local plain-text files. <br>
Mitigation: Use the skill only on devices with appropriate access controls, confirm all caregiver consent before shared use, and delete ~/.mom-skill/babies/ when records should no longer be retained. <br>
Risk: Outputs may be mistaken for medical advice during stressful baby-care situations. <br>
Mitigation: Treat responses as a memory aid only and contact a pediatrician or emergency care provider for fever, persistent rash, eating or drinking concerns, or any health issue. <br>
Risk: Pattern summaries depend on parent-entered observations that may be incomplete or inaccurate. <br>
Mitigation: Review logged observations before relying on summaries, and keep important health or allergy notes available for professional care discussions. <br>


## Reference(s): <br>
- [Mom.skill ClawHub Page](https://clawhub.ai/realteamprinz/mom) <br>
- [Publisher Profile](https://clawhub.ai/user/realteamprinz) <br>
- [Soothing Techniques Reference](references/soothing-techniques.md) <br>
- [Baby Profile Template](templates/BABY-PROFILE.md) <br>
- [Hermes Agent](https://github.com/NousResearch/hermes-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Conversational text and Markdown summaries, with local Markdown and JSONL record structures described for baby-care logs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Designed for local plain-text baby-care records under ~/.mom-skill/babies/; outputs are a memory aid and not medical advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
