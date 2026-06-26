## Description: <br>
Multi-source deep research using your own browser. Queries Perplexity, Grok, and Gemini in parallel via CDP - zero API keys, uses your existing subscriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lmanchu](https://clawhub.ai/user/lmanchu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill to submit a research question to multiple logged-in browser-based AI services, collect their responses, and synthesize a concise comparison. It supports browser-based sources and an optional API-only source when configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a CDP-enabled browser profile that may already be logged into AI services. <br>
Mitigation: Use a dedicated browser profile with only the needed accounts and keep CDP bound to localhost. <br>
Risk: Prompts and collected browser-session text can be sent to the configured cliproxy endpoint for synthesis. <br>
Mitigation: Inspect ~/.config/omni-research/config.json before running and configure only trusted local or approved endpoints. <br>
Risk: The release under-discloses data movement to a configured API or proxy despite advertising zero API keys. <br>
Mitigation: Review the scanner guidance and disclose the configured synthesis endpoint behavior to users before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lmanchu/omni-research) <br>
- [Publisher profile](https://clawhub.ai/user/lmanchu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown research summary with per-source sections; JSON output is available when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source-specific errors or rate-limit messages when a browser or API source cannot return a result.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
