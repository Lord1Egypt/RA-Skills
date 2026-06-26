## Description: <br>
Fetches BBC News and generates a Daily English News PDF with full articles, Chinese translations, and vocabulary for English learners. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[effeceee](https://clawhub.ai/user/effeceee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and educators use this skill to fetch recent public news articles and create an English-learning PDF with article text and vocabulary support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to BBC News and Google Translate, so article text or vocabulary terms may be sent to external services. <br>
Mitigation: Use it only with public or appropriately licensed text, and confirm that sending derived terms to Google Translate is acceptable for the deployment. <br>
Risk: The generated PDF is copied to a fixed output path and may replace a previous file. <br>
Mitigation: Review the configured output location before running the skill and preserve any existing files that should not be overwritten. <br>
Risk: Python dependencies are declared without pinned versions. <br>
Mitigation: Install dependencies in an isolated environment and pin reviewed versions before production use. <br>


## Reference(s): <br>
- [Ket News Fetcher on ClawHub](https://clawhub.ai/effeceee/ket-news-fetcher) <br>
- [BBC News RSS](https://feeds.bbci.co.uk/news/rss.xml) <br>
- [BBC Learning English](https://www.bbc.co.uk/learningenglish/english/course/lower-intermediate) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, configuration, guidance] <br>
**Output Format:** [PDF file with console status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a Daily English News PDF from recent public news articles; requires python3 and Python packages for HTML fetching, parsing, translation, and PDF generation.] <br>

## Skill Version(s): <br>
6.8.0 (source: release metadata and openclaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
