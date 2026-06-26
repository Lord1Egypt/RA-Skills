## Description: <br>
Evaluate hi-fi and audio gear options, build system recommendations, guide installation and tuning, and analyze used-market pricing/resale value. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ruodong](https://clawhub.ai/user/Ruodong) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and audio enthusiasts use this skill to compare hi-fi components, match speakers, amplifiers, DACs, and headphone rigs, tune room or desk setups, and judge second-hand listing value. It produces decision-ready recommendations with trade-offs, caveats, and next actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CSV listing data used for price analysis may contain unrelated personal information. <br>
Mitigation: Provide only listing fields needed for price analysis, such as price, model, platform, condition, date, and notes. <br>
Risk: Hi-fi recommendations and used-market price bands may be incomplete if inputs omit room, budget, condition, accessories, shipping, or local-market context. <br>
Mitigation: Gather the missing essentials before deciding and treat the result as advisory guidance to review against the actual listing and setup constraints. <br>


## Reference(s): <br>
- [Workflows](references/workflows.md) <br>
- [Checklists](references/checklists.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with optional inline bash command for CSV price analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a local CSV helper that reads listing prices and prints robust used-market price bands.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
