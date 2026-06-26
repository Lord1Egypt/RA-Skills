## Description: <br>
Multi-engine web search across 6 engines: DuckDuckGo, DDG Lite, Yahoo, Yahoo JP, Startpage, and Google headless Chromium, with no API keys required and results ranked by cross-engine frequency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nirveshdagar](https://clawhub.ai/user/nirveshdagar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run local, multi-source web searches for current information, fact checking, research, and source discovery without paid search API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and the user's IP address may be visible to third-party search engines. <br>
Mitigation: Do not use the skill for passwords, API keys, confidential project names, personal data, or regulated information. <br>
Risk: The Google mode uses headless Chromium and may be blocked or brittle. <br>
Mitigation: Disable the Google engine when browser automation risk, reliability, or policy constraints outweigh the extra search coverage. <br>


## Reference(s): <br>
- [Engine Notes & Troubleshooting](references/engines.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/nirveshdagar/multi-engine-websearch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and optional JSON search results from the bundled command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include title, URL, snippet, and source engine list; callers should cite returned URLs when summarizing results.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
