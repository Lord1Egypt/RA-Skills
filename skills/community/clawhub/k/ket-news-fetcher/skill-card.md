## Description:

Fetches BBC News articles and generates a Daily English News PDF for English learners with article text and vocabulary translations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[effeceee](https://clawhub.ai/user/effeceee)

### License/Terms of Use:

MIT-0

## Use Case:

External users, educators, and English learners use this skill to collect current BBC News items into a Chinese-supported English learning PDF with vocabulary lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches public news pages and sends extracted vocabulary or text chunks to Google Translate.

Mitigation: Review network and content-sharing policies before running it, especially if the source text is changed from public news content.

Risk: The generated PDF is copied to a fixed workspace path.

Mitigation: Run it only in a workspace where that destination is expected, or adjust the output path before deployment.

Risk: Dependency versions are not pinned in the release metadata.

Mitigation: Pin dependency versions for reproducible installs before operational use.

Risk: The release has a quality gap around full article translation.

Mitigation: Review generated PDFs before relying on them for full article translations, and update the implementation if complete translation is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/effeceee/skills/ket-news-fetcher)
- [BBC News RSS feed](https://feeds.bbci.co.uk/news/rss.xml)
- [BBC Learning English](https://www.bbc.co.uk/learningenglish/english/course/lower-intermediate)
- [News in Levels](https://www.newsinlevels.com/level-1/)
- [VOA Learning English](https://learningenglish.voanews.com/english/learning-english)
- [Google Translate endpoint](https://translate.googleapis.com/translate_a/single)

## Skill Output:

**Output Type(s):** [Files, Text, Shell commands]

**Output Format:** [PDF file with console status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a daily English-learning PDF, writes an intermediate file under /tmp, and copies the PDF to a fixed workspace path.]

## Skill Version(s):

6.8.0 (source: server release, OpenClaw metadata, and artifact changelog dated 2026-03-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
