## Description:

Find, compare, and add Notion Marketplace templates with linked free shortlists, explicit workspace selection, browser-driven duplication, and Notion API verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patrick-erichsen-2](https://clawhub.ai/user/patrick-erichsen-2)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to discover free Notion Marketplace templates, compare a short list, add the selected template to a chosen Notion workspace, and verify the installed page through the Notion API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can add a selected Notion template into a user's workspace.

Mitigation: Require explicit workspace selection before duplication and verify the resulting page through the Notion API.

Risk: Paid or ambiguous Marketplace listings could cause unwanted spending or incorrect selection.

Mitigation: Default to free-only discovery, exclude ambiguous prices, and require explicit opt-in and action-time confirmation before any paid checkout.

Risk: Browser success alone may not prove that the template was installed.

Mitigation: Search and fetch the candidate page through the Notion API and report browser-only success as unverified if API confirmation fails.

## Reference(s):

- [Notion Marketplace Categories](https://www.notion.com/templates/category)
- [Notion Marketplace](https://app.notion.com/marketplace)
- [ClawHub Skill Page](https://clawhub.ai/patrick-erichsen-2/skills/notion-marketplace)

## Skill Output:

**Output Type(s):** [Markdown, API Calls, Guidance]

**Output Format:** [Markdown with linked template shortlist, workspace and destination details, installed page URL or ID, and verification evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports browser success as unverified when API verification cannot confirm the installed page.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
