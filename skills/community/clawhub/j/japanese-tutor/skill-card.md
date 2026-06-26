## Description: <br>
Interactive Japanese learning assistant. Supports vocabulary, grammar, quizzes, roleplay, PDF/DOCX material parsing for study/homework help, and OCR translation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chndranndr](https://clawhub.ai/user/chndranndr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Learners and tutors use this skill for Japanese vocabulary practice, grammar explanations, quizzes, conversation roleplay, translation, and guided study or homework support from PDF, DOCX, image, or text materials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF parsing sends uploaded PDF content to Gemini for OCR and layout analysis. <br>
Mitigation: Avoid parsing confidential PDFs, school records, or personal documents unless third-party processing is acceptable. <br>
Risk: Extracted study material may be saved into local reference markdown files and reused later. <br>
Mitigation: Review or delete saved reference files when extracted lesson material should not persist. <br>


## Reference(s): <br>
- [Japanese Tutor Skill Definition](SKILL.md) <br>
- [Japanese Grammar - Beginner Level](references/grammar.md) <br>
- [Lesson 2 Grammar](references/grammar_lesson2.md) <br>
- [Pelajaran 1: Kalimat Dasar & Kosakata Profesi](references/lesson_1.md) <br>
- [Japanese Vocabulary - Beginner Level (N5)](references/vocab.md) <br>
- [Lesson 2 Vocabulary](references/vocab_lesson2.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/chndranndr/japanese-tutor) <br>
- [Publisher Profile](https://clawhub.ai/user/chndranndr) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text, code, shell commands] <br>
**Output Format:** [Markdown and text responses with optional shell commands for parsing files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local markdown reference files with extracted vocabulary, grammar, and lesson material.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
