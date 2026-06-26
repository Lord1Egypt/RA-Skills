## Description: <br>
AI-powered insurance agent training coach that helps parse product documents, generate question banks, assess agent skill levels, schedule personalized training, and support role-play practice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gechengling](https://clawhub.ai/user/gechengling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Insurance training teams, agency leaders, and insurtech platforms use this skill to create product knowledge drills, objection-handling practice, competency assessments, and daily coaching plans for insurance agents. Outputs are training references and should be reviewed by qualified insurance and compliance professionals before real-world use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent profiles, client schedules, and product documents can contain sensitive personal, customer, or confidential business information. <br>
Mitigation: Use synthetic or anonymized data unless the organization has approved the handling path for real agent, client, schedule, and product-manual data. <br>
Risk: Sales scripts, objection-handling examples, and pressure-closing content may be misleading or non-compliant if used directly with customers. <br>
Mitigation: Treat generated scripts as draft training material and require review by qualified insurance, legal, and compliance professionals before operational use. <br>
Risk: The package contains Python scripts and network-capable examples despite documentation that also describes the skill as non-executable. <br>
Mitigation: Run included scripts only intentionally in a controlled environment after reviewing their dependencies, inputs, and network behavior. <br>


## Reference(s): <br>
- [README](artifact/README.md) <br>
- [Agent Profile Template](artifact/references/agent_profile_template.md) <br>
- [Question Bank Templates](artifact/references/question_bank_templates.md) <br>
- [Training Evaluation Rubric](artifact/references/training_evaluation_rubric.md) <br>
- [ClawHub Release Page](https://clawhub.ai/gechengling/insurance-agent-trainer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown and JSON training materials, including product profiles, question banks, role-play prompts, coaching feedback, scoring rubrics, and daily training plans.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are advisory training references and require human review before use in insurance sales, compliance, or customer communication.] <br>

## Skill Version(s): <br>
5.2.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
