## Description: <br>
Searches Google Scholar through SerpAPI, parses academic paper metadata, and can download available PDF files for literature review workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rutianze](https://clawhub.ai/user/rutianze) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and research-focused agents use this skill to search Google Scholar via SerpAPI, parse paper metadata such as titles, authors, years, abstracts, and citation counts, and optionally save available PDFs for literature review tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SerpAPI keys can be exposed through examples that print, echo, hardcode, or back up credentials. <br>
Mitigation: Use environment variables or a secret manager, avoid logging secrets, and rotate the key immediately if exposure is suspected. <br>
Risk: Search results and downloaded PDFs are saved locally and may include copyrighted or sensitive research material. <br>
Mitigation: Scope downloads to a chosen folder, use --no-download when only search results are needed, and review copyright and access terms before bulk downloading. <br>
Risk: Research queries are sent to SerpAPI as a third-party service. <br>
Mitigation: Install and use the skill only when sending those queries to SerpAPI is acceptable for the intended workflow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/rutianze/google-scholar-api) <br>
- [API Guide](artifact/references/api_guide.md) <br>
- [Usage Examples](artifact/references/usage_examples.md) <br>
- [SerpAPI Google Scholar API](https://serpapi.com/google-scholar-api) <br>
- [SerpAPI Search API](https://serpapi.com/search-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance, Python code snippets, shell commands, JSON search results, and optional downloaded PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SerpAPI key supplied through environment variables or an equivalent secret-management mechanism.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
