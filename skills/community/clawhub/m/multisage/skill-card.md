## Description:

Query Multisage for multi-expert AI answers from Claude, GPT, and Gemini.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waleedkadous](https://clawhub.ai/user/waleedkadous)

### License/Terms of Use:


## Use Case:

Developers, researchers, and external users use this skill to ask Multisage for synthesized answers from multiple AI providers, including standard consultations and deeper research-style analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to Multisage and downstream AI providers.

Mitigation: Use the skill only for content that is acceptable to share with those services, and avoid sending secrets, regulated data, or confidential material.

Risk: API key handling examples can expose credentials if an agent searches or prints environment files.

Mitigation: Configure MULTISAGE_API_KEY through a trusted environment mechanism and prevent agents from reading or echoing .env files.

Risk: Global package installation and shell command templates can introduce supply-chain or command-construction risk.

Mitigation: Prefer a pinned local CLI installation and pass untrusted text with safe argument handling.

## Reference(s):

- [Multisage ClawHub Skill Page](https://clawhub.ai/waleedkadous/skills/multisage)
- [Multisage API Key Settings](https://multisage.ai/settings)
- [Multisage Pricing](https://multisage.ai/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying CLI can return synthesized answers, expert details, credits used, stage breakdowns, and thread IDs for asynchronous deep research.]

## Skill Version(s):

2.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
