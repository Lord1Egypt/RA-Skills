## Description:

Recognizes AliPay and WeChat mobile payment bill screenshots and extracts transaction time, merchant, amount, income or expense type, and related fields as structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to submit a local mobile payment bill screenshot to Scnet's OCR API and receive normalized transaction fields for review, reconciliation, or recordkeeping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment bill screenshots can contain sensitive personal, social, and financial data and are uploaded to Scnet's OCR service.

Mitigation: Use only screenshots approved for external processing, confirm consent for any third-party information, and delete local or cloud copies after use where appropriate.

Risk: A configurable SCNET_API_BASE can send the image and API key to an endpoint other than the documented Scnet host.

Mitigation: Keep SCNET_API_BASE at https://api.scnet.cn/api/llm/v1 unless the alternate endpoint is fully trusted, and review config/.env before running.

Risk: The required Scnet API key could be exposed if pasted into chat or stored with broad file permissions.

Mitigation: Store the key in an environment variable or config/.env with restricted permissions, and avoid including the key in prompts or transcripts.

## Reference(s):

- [Sugon-Scnet mobile payment bill OCR API docs](references/api-docs.md)
- [Mobile payment bill field summary](assets/templates/fields-summary.md)
- [ClawHub skill page](https://clawhub.ai/scnet-sugon/skills/mobile-pay-bill-ocr)
- [Scnet service website](https://www.scnet.cn)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON data on stdout, with human-readable error text on failure.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCNET_API_KEY and a local image path; uploads the image to Scnet's OCR service.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact SKILL.md and skill.yaml report 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
