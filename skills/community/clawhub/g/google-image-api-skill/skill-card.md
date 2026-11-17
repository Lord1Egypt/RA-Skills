## Description:

This skill helps agents extract structured Google Images result metadata through the BrowserAct API for keyword, regional, and language-specific image searches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccmagia2-gif](https://clawhub.ai/user/ccmagia2-gif)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use this skill to collect Google Images metadata for visual content sourcing, competitor monitoring, market research, localized trend checks, and data enrichment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a BrowserAct API key and may lead users to expose that secret in chat or terminal logs.

Mitigation: Configure BROWSERACT_API_KEY through the environment or an approved secret manager, avoid pasting the key into chat, and rotate the key if it has already been shared.

Risk: Image-search terms and task parameters are sent to BrowserAct.

Mitigation: Use the skill only when sending those search terms and parameters to BrowserAct is acceptable for the intended workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ccmagia2-gif/skills/google-image-api-skill)
- [BrowserAct Console integrations](https://www.browseract.com/reception/integrations)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and text or JSON-like API result output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BROWSERACT_API_KEY and returns image result fields such as title, link, source, thumbnail, product flag, related content ID, and index.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
