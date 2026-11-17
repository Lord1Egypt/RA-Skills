## Description:

Automatically solves Moltbook math captchas by parsing English text, extracting operations, calculating results, and formatting answers with two decimals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xraini](https://clawhub.ai/user/0xraini)

### License/Terms of Use:


## Use Case:

Developers and agents working with Moltbook use this skill to solve English-language verification math challenges and submit formatted answers during verification flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a local Moltbook API key.

Mitigation: Review the skill before installation and use it only when local Moltbook credential access is expected.

Risk: The skill submits authenticated verification answers to Moltbook without clear documentation of consent or accessed account state.

Mitigation: Prefer a version that asks before using credentials and documents the Moltbook account state and API endpoints it accesses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xraini/skills/molt-solver)
- [Publisher profile](https://clawhub.ai/user/0xraini)

## Skill Output:

**Output Type(s):** [Text, Code, API Calls]

**Output Format:** [Formatted decimal answer string or JSON API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verification answers are formatted with two decimal places.]

## Skill Version(s):

1.0.0 (source: server release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
