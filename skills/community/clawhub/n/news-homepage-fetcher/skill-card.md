## Description:

Homepage-first news collection from major international, Singaporean, and China-focused outlets. Use for: opening news homepages, clicking article links, extracting article text and metadata, translating into Chinese, deduplicating stories, and assembling Word-ready daily digests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alanwu2024](https://clawhub.ai/user/alanwu2024)

### License/Terms of Use:

MIT-0

## Use Case:

External users and news workflow operators use this skill to collect daily articles from major news homepages, extract article metadata and body text, translate or summarize content in Chinese, deduplicate stories, and assemble Word-ready daily news digests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetched news content can be incomplete, dynamically loaded, paywalled, or otherwise limited by publisher access controls.

Mitigation: Use HTTPS sources where possible, record paywalls or extraction failures, switch to accessible articles, and avoid filling gaps with unsourced content.

Risk: News summaries or translations can introduce factual errors, overstate uncertainty, or lose attribution.

Mitigation: Review fetched article content before relying on or publishing the digest, preserve source links and metadata, and retain uncertainty from the original article.

Risk: Using full article text may raise publisher terms-of-use or copyright concerns.

Mitigation: Confirm that collection, translation, and publication of article text comply with the selected publishers' terms before distributing the digest.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alanwu2024/skills/news-homepage-fetcher)
- [News source catalog](references/source_catalog.md)
- [Machine-readable source manifest](references/source_manifest.yaml)
- [Translation and Word output specification](references/translation_docx_spec.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Word-ready Markdown, structured JSON, or DOCX-ready intermediate content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves source links, article metadata, Chinese summaries and translations, extraction notes, and failure or access-limit notes.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
