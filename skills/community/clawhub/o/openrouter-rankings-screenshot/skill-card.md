## Description: <br>
Capture OpenRouter Rankings across Categories scenarios and page sections, then create a Feishu document with screenshots and a sales-oriented summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neymar011ren](https://clawhub.ai/user/neymar011ren) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations users use this skill to capture OpenRouter ranking screenshots, summarize model trends for sales readers, and share the result through a Feishu document and chat notification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill posts generated reports through the configured Feishu integration, so an incorrect recipient or document permission setting could share the digest with the wrong audience. <br>
Mitigation: Verify the Feishu recipient, document permissions, and chat notification target before enabling scheduled or automated runs. <br>
Risk: Screenshots can be incomplete or misleading if OpenRouter charts are still loading or a category capture fails. <br>
Mitigation: Use the bundled screenshot validation workflow and do not create or send the Feishu document when validation fails. <br>
Risk: Generated screenshots and summaries are cached locally, and local paths should not be exposed to report recipients. <br>
Mitigation: Share the Feishu document URL and short summary only; avoid sending host file paths, file:// URLs, or raw local media references. <br>


## Reference(s): <br>
- [OpenRouter Rankings](https://openrouter.ai/rankings) <br>
- [ClawHub Skill Page](https://clawhub.ai/neymar011ren/openrouter-rankings-screenshot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown summaries, PNG screenshots, JSON manifest data, Feishu document link, and short chat text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Feishu integration, a Chromium executable, and local cache storage for generated screenshots and summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
