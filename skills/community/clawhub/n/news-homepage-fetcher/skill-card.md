## Description: <br>
Homepage-first news collection from major international, Singaporean, and China-focused outlets for opening news homepages, extracting article text and metadata, translating into Chinese, deduplicating stories, and assembling Word-ready daily digests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alanwu2024](https://clawhub.ai/user/alanwu2024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Editors, analysts, and agent operators use this skill to collect public homepage news from selected international, Singaporean, and China-focused outlets, preserve source links and metadata, translate or summarize content in Chinese, and assemble daily news digests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill browses public news sites whose access, translation, and redistribution terms may vary by source. <br>
Mitigation: Use the skill within each source's access and reuse terms, avoid paywalled or login-restricted content, and prefer summaries or internal-use documents unless redistribution rights are clear. <br>
Risk: Generated Chinese summaries or translations may omit uncertainty or overstate facts from developing news stories. <br>
Mitigation: Preserve source links, publication metadata, uncertainty language, and extraction notes so a reviewer can verify important claims against the original article. <br>
Risk: Homepage extraction can encounter duplicate links, dynamic pages, videos, live blogs, or incomplete article bodies. <br>
Mitigation: Filter for body-style articles, deduplicate by event and source, and mark restricted or failed extraction cases instead of filling missing content from inference. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alanwu2024/news-homepage-fetcher) <br>
- [Source catalog](artifact/references/source_catalog.md) <br>
- [Machine-readable source manifest](artifact/references/source_manifest.yaml) <br>
- [Translation and Word output specification](artifact/references/translation_docx_spec.md) <br>
- [Daily news digest template](artifact/templates/daily_news_digest_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Word-ready Markdown or structured JSON-style article records with source metadata, Chinese titles, summaries, translated body text, keywords, and extraction notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include failure notes for paywalled, login-restricted, dynamically loaded, duplicate, or incomplete article pages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
