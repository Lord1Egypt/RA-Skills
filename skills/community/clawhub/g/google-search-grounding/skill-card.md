## Description: <br>
Google web search via Gemini Search Grounding as the primary mode, with Custom Search JSON API fallback modes for raw link results and image search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shaharsha](https://clawhub.ai/user/Shaharsha) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill when an agent needs Google-backed web search, grounded synthesized answers with citations, raw search results, or image result URLs. It is especially suited to workflows that need multilingual search with configurable language and country hints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Google services and may expose sensitive prompt content. <br>
Mitigation: Avoid sending private data in search queries and review query content before use. <br>
Risk: Google API keys may incur quota usage or billing charges if overused or overprivileged. <br>
Mitigation: Use a restricted Google API key and monitor quota and billing. <br>
Risk: Default Hebrew and Israel locale settings may bias results toward that language or region. <br>
Mitigation: Review GOOGLE_SEARCH_LANG and GOOGLE_SEARCH_COUNTRY defaults and override them for the intended audience. <br>
Risk: The installer adds a Python dependency to the execution environment. <br>
Mitigation: Install dependencies in an isolated Python environment when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Shaharsha/google-search-grounding) <br>
- [Google Programmable Search Engine](https://programmablesearchengine.google.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or JSON returned by a Python CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search mode controls grounded answers, raw links, or image URLs; language and country can be set per call.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
