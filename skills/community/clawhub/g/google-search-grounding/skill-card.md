## Description:

Google web search via Gemini Search Grounding and Custom Search JSON API for synthesized cited answers, raw link results with snippets, and image search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaharsha](https://clawhub.ai/user/shaharsha)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to run Google-backed web searches, get grounded answers with source citations, retrieve raw search links and snippets, or find image URLs. It is useful when an agent needs current search results, multilingual query support, or Hebrew/Israel defaults.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can modify the host Python environment using an unpinned google-genai dependency.

Mitigation: Review install.sh before running it, and prefer installing google-genai in a virtual environment with a pinned, reviewed version.

Risk: Search queries are sent to Google APIs and could expose secrets, credentials, private customer data, or sensitive internal terms.

Mitigation: Avoid submitting sensitive data in searches, and set GOOGLE_SEARCH_LANG and GOOGLE_SEARCH_COUNTRY explicitly for the intended locale.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shaharsha/skills/google-search-grounding)
- [Publisher profile](https://clawhub.ai/user/shaharsha)
- [Google Programmable Search Engine](https://programmablesearchengine.google.com/)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration]

**Output Format:** [Plain text or JSON, with source citations, links, snippets, image URLs, and setup commands shown in Markdown documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search mode returns synthesized answers and citations; raw mode returns titles, links, and snippets; image mode returns image links and thumbnails when JSON output is requested.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
