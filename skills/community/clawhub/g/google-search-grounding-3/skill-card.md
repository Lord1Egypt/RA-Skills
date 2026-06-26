## Description: <br>
Google web search via Gemini Search Grounding and Custom Search JSON API for grounded answers with citations, raw link results, and image search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phucanh08](https://clawhub.ai/user/phucanh08) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to run Google-backed web searches, request grounded synthesized answers with citations, retrieve raw search links and snippets, or find image results. It is especially useful when multilingual or Hebrew-first search behavior is desired. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Google APIs using the configured Google API key. <br>
Mitigation: Use a restricted API key with quotas and avoid submitting secrets, sensitive internal data, or confidential queries. <br>
Risk: The install process adds the google-genai Python dependency to the active Python environment. <br>
Mitigation: Install in a virtual environment or another controlled Python environment before use. <br>
Risk: Default language and country settings favor Hebrew and Israel results. <br>
Mitigation: Set GOOGLE_SEARCH_LANG and GOOGLE_SEARCH_COUNTRY, or pass --lang and --country, when a different locale is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phucanh08/google-search-grounding-3) <br>
- [Publisher profile](https://clawhub.ai/user/phucanh08) <br>
- [Google Programmable Search Engine](https://programmablesearchengine.google.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or JSON returned by CLI commands, with citations, links, snippets, image URLs, and setup guidance documented in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search mode controls whether output is a grounded answer, raw web results, or image results; language and country can be configured by flags or environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
