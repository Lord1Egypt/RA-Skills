## Description:

Interactive Japanese learning assistant. Supports vocabulary, grammar, quizzes, roleplay, PDF/DOCX material parsing for study/homework help, and OCR translation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chndranndr](https://clawhub.ai/user/chndranndr)

### License/Terms of Use:


## Use Case:

External learners and instructors use this skill for beginner Japanese vocabulary, grammar explanations, quizzes, conversation practice, translation, and guided study or homework help from PDF/DOCX course materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF parsing may send private schoolwork, IDs, grades, copyrighted course packets, or other sensitive documents to Google Gemini.

Mitigation: Use the PDF parser only after explicit user consent, avoid sensitive documents, and review materials before upload.

Risk: The skill can save extracted study content into local reference files without clear consent controls.

Mitigation: Require the agent to ask before saving extracted content and review reference-file changes before relying on or redistributing them.

## Reference(s):

- [Skill page](https://clawhub.ai/chndranndr/skills/japanese-tutor)
- [Publisher profile](https://clawhub.ai/user/chndranndr)
- [Japanese Grammar - Beginner Level](references/grammar.md)
- [Lesson 2 Grammar](references/grammar_lesson2.md)
- [Pelajaran 1: Kalimat Dasar & Kosakata Profesi](references/lesson_1.md)
- [Japanese Vocabulary - Beginner Level](references/vocab.md)
- [Lesson 2 Vocabulary](references/vocab_lesson2.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown conversational responses with optional code or shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append extracted vocabulary, grammar, and lesson notes to local reference files when study materials are ingested.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
