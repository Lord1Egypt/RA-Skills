## Description:

孕期搭子 Pregnancy Buddy is a pregnancy companion agent for expectant mothers that explains prenatal reports, answers food-safety questions, suggests nutrition and preparation plans, tracks milestones, creates baby-development visuals, drafts monthly letters, and offers emotional support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iriswong31](https://clawhub.ai/user/iriswong31)

### License/Terms of Use:

MIT-0

## Use Case:

External users, especially expectant mothers, use this skill for conversational pregnancy support, prenatal-checkup preparation, report explanation, food-safety guidance, meal planning, milestone tracking, preparation checklists, and emotionally supportive pregnancy journaling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may handle sensitive pregnancy and prenatal-report details, and its reminder and letter workflows may rely on cross-session remembering.

Mitigation: Ask for clear consent before retaining pregnancy details, explain what is remembered and for how long, and avoid storing identifying information unless it is necessary.

Risk: Prenatal report OCR may process uploaded documents through Tencent Cloud.

Mitigation: Disclose third-party OCR processing before upload, encourage users to redact names and identifiers, and offer a manual text-entry path.

Risk: Pregnancy guidance can be mistaken for diagnosis or treatment advice.

Mitigation: Keep medical disclaimers visible, avoid diagnosis and medication dosing, and direct urgent symptoms or abnormal findings to the user's clinician or emergency care.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/iriswong31/skills/pregnancy-buddy)
- [ClawHub Publisher Profile](https://clawhub.ai/user/iriswong31)
- [Online Demo](https://iriswong31.github.io/work-analysis/digital-care/pregnancy-buddy/)
- [Pregnancy Weekly Guide](references/pregnancy-weekly-guide.md)
- [Prenatal Checkup Guide](references/prenatal-checkup-guide.md)
- [Meal Nutrition Guide](references/meal-nutrition-guide.md)
- [Preparation Checklist](references/preparation-checklist.md)
- [Timeline Milestones](references/timeline-milestones.md)
- [Baby Visualization Prompts](references/baby-visualization-prompts.md)
- [Letter Templates](references/letter-templates.md)
- [Conversation Examples](references/conversation-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with optional generated prompts, letters, checklists, OCR text summaries, and shell command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use Tencent Cloud OCR for prenatal report images and image-generation prompts when platform tools are available.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
