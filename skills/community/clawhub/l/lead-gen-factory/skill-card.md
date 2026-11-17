## Description:

Run B2B lead research with lgf (Lead Gen Factory) when asked to find leads, prospect companies, research ICPs, find decision makers, or generate a lead list for any B2B target profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catafal](https://clawhub.ai/user/catafal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and revenue teams use this skill to run a CLI-based B2B lead research pipeline from a free-text ICP and receive scored, deduplicated lead results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install code from an unpinned GitHub repository.

Mitigation: Review the repository and pin a trusted commit or release before installing or running the CLI.

Risk: The workflow depends on Tavily and OpenRouter API keys.

Mitigation: Use restricted keys, store them only in the documented local configuration, and rotate them if exposed.

Risk: Generated lead records may include personal contact data such as email addresses, phone numbers, and LinkedIn URLs.

Mitigation: Minimize retained lead data and handle outreach records under applicable privacy, consent, and marketing rules.

## Reference(s):

- [Lead Gen Factory GitHub repository referenced by the skill](https://github.com/Catafal/lead-gen-factory.git)
- [ClawHub skill page](https://clawhub.ai/catafal/skills/lead-gen-factory)
- [Publisher profile](https://clawhub.ai/user/catafal)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced CLI can emit structured JSON to stdout and CSV lead files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
