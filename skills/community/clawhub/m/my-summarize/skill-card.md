## Description: <br>
Summarize URLs or files with the summarize CLI, including web pages, PDFs, images, audio, and YouTube links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shahuquan-dotcom](https://clawhub.ai/user/shahuquan-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, employees, and external users can use this skill to ask an agent to summarize URLs, local documents, media files, and YouTube links through the summarize CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on an external CLI and configured AI or extraction providers, which may receive summarized content. <br>
Mitigation: Use trusted provider configurations, dedicated or restricted API keys, and avoid summarizing secrets, regulated documents, or private URLs unless sending that content is approved. <br>
Risk: Optional Firecrawl and Apify fallbacks can send web or YouTube content through additional services. <br>
Mitigation: Disable optional fallbacks when they are not needed and enable them only for workflows where those services are approved. <br>
Risk: Installation depends on the summarize Homebrew tap. <br>
Mitigation: Install only when the Homebrew tap and CLI source are trusted for the deployment environment. <br>


## Reference(s): <br>
- [Summarize homepage](https://summarize.sh) <br>
- [ClawHub release page](https://clawhub.ai/shahuquan-dotcom/my-summarize) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports configurable summary length, token limits, extract-only mode, and optional Firecrawl or Apify fallback services.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
