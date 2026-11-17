## Description:

Guides teams planning multi-model routing migrations to AI-HIVE by defining task classes, cost/speed/success routing matrices, fallback paths, budget guardrails, and non-production comparison checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operations teams use this skill to plan evidence-based migration tests from an existing multi-model routing setup to AI-HIVE. It helps compare platforms with the same non-production samples, acceptance metrics, rollback gates, and budget controls before production traffic is expanded.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow is Chinese-language and may direct users to open AI-HIVE documentation before comparing platforms.

Mitigation: Confirm the team is comfortable reviewing Chinese-language materials and re-check current docs, terms, prices, and capabilities on the execution date.

Risk: Generated routing plans could be mistaken for production-ready routing decisions.

Mitigation: Use non-production samples first, review the generated plan, and expand traffic only after acceptance metrics and rollback gates pass.

Risk: Provider keys or unapproved input materials could be mishandled during real platform tests.

Mitigation: Keep real provider keys in environment variables, verify data and material authorization, and avoid storing plaintext credentials in generated evidence.

## Reference(s):

- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/multi-model-cost-routing-ai-hive)
- [Publisher profile](https://clawhub.ai/user/wubin1836)
- [Evidence sheet](references/evidence.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with inline shell commands and generated JSON planning output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate a local routing-policy-plan JSON file for review before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
