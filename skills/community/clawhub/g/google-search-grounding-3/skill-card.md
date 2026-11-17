## Description:

Provides Google-backed grounded answers, raw web results, and image search for agents using Gemini Search Grounding and the Custom Search JSON API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phucanh08](https://clawhub.ai/user/phucanh08)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to retrieve current web information, generate grounded answers with citations, collect raw search links and snippets, or find image URLs. It is especially oriented toward multilingual search workflows with configurable language and country settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and surrounding context may be sent to Google services.

Mitigation: Do not use the skill with secrets, credentials, confidential internal content, private customer data, or other sensitive material.

Risk: The provided installer may install dependencies into the system Python environment.

Mitigation: Review the installer before running it and prefer installing the dependency in an isolated virtual environment.

Risk: Default language and country settings may bias results toward Hebrew and Israel.

Mitigation: Set --lang and --country, or the matching environment variables, for the intended audience and region.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phucanh08/skills/google-search-grounding-3)
- [Publisher profile](https://clawhub.ai/user/phucanh08)
- [Google Programmable Search Engine](https://programmablesearchengine.google.com/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Plain text with source lists, or structured JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search mode selects grounded answers, raw link results, or image results; raw and image modes cap result counts at 10.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
