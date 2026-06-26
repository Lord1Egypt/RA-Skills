## Description: <br>
孕期搭子 is an AI pregnancy companion for expectant mothers that supports prenatal report interpretation, food safety checks, nutrition and meal guidance, fetal development visualization, timeline reminders, emotional support, and monthly baby-letter drafting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iriswong31](https://clawhub.ai/user/iriswong31) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, especially first-time expectant mothers, use this skill for pregnancy companionship, prenatal-checkup preparation, report explanation, food and nutrition guidance, fetal development updates, and supportive letter drafting. It is informational support and does not replace obstetric care. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may retain sensitive pregnancy details for proactive reminders and monthly baby-letter generation. <br>
Mitigation: Make memory-based features opt-in, disclose what details are stored, and provide clear review and deletion controls before using reminders or baby-letter drafting. <br>
Risk: Prenatal report images, PDFs, URLs, or local files may be processed by Tencent Cloud OCR. <br>
Mitigation: Ask for explicit consent before OCR use, advise users to remove identifiers when possible, and avoid OCR for users who are not comfortable with external processing. <br>
Risk: Pregnancy and medical guidance may be mistaken for clinical diagnosis or care instructions. <br>
Mitigation: Present guidance as informational support, preserve the skill's medical disclaimers, and direct users to obstetric care for abnormal results, urgent symptoms, medication questions, or diagnosis. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/iriswong31/pregnancy-buddy) <br>
- [Online Demo](https://iriswong31.github.io/work-analysis/digital-care/pregnancy-buddy/) <br>
- [Pregnancy Weekly Guide](references/pregnancy-weekly-guide.md) <br>
- [Prenatal Checkup Guide](references/prenatal-checkup-guide.md) <br>
- [Meal Nutrition Guide](references/meal-nutrition-guide.md) <br>
- [Timeline Milestones](references/timeline-milestones.md) <br>
- [Preparation Checklist](references/preparation-checklist.md) <br>
- [Baby Visualization Prompts](references/baby-visualization-prompts.md) <br>
- [Letter Templates](references/letter-templates.md) <br>
- [Conversation Examples](references/conversation-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, generated prose, optional image-generation prompts, OCR text summaries, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask users for pregnancy week, due date, symptoms, food questions, checkup timing, or report images before producing guidance.] <br>

## Skill Version(s): <br>
2.1.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
