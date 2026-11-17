## Description:

Use this skill whenever the user wants a whole book translated: an EPUB ebook, a novel or manuscript in DOCX, or a book-length PDF. One upload returns one translated file in the same format, so an EPUB stays an EPUB. Shows the exact price for the full word count before anything is charged.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catorch](https://clawhub.ai/user/catorch)

### License/Terms of Use:

MIT-0

## Use Case:

Readers, authors, and other users use the skill to translate a full EPUB, DOCX manuscript, or book-length PDF into a requested language. It submits the document to PageTranslate, presents the exact quote before payment, and returns the translated file in its original format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploading a document sends its contents to PageTranslate.

Mitigation: Upload only the file the user asked to translate.

Risk: The benign security verdict has medium confidence because review coverage was partial.

Mitigation: Review the unresolved local path reference and skill behavior before deployment.

## Reference(s):

- [Translate a book with PageTranslate](https://pagetranslate.ai/translate-a-book)
- [PageTranslate API key setup](https://pagetranslate.ai/dashboard/api-keys)
- [PageTranslate translation pricing](https://pagetranslate.ai/faq/how-much-does-it-cost-to-translate-a-book)

## Skill Output:

**Output Type(s):** [Files, Guidance]

**Output Format:** [A translated document in the source file format (such as EPUB, DOCX, or PDF)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One translated file per submitted document; the exact price is shown before payment.]

## Skill Version(s):

0.1.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
