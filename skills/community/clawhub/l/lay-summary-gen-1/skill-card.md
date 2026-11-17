## Description:

Generates plain-language summaries of medical research abstracts for non-expert audiences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External readers, patient-communication teams, and researchers can use this skill to turn medical research abstracts into plain-language summaries with key takeaways and jargon replacements. Generated summaries require review before patient, public, or EU CTR-related use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated medical summaries may be incomplete, inaccurate, or unsuitable for patient, public, or EU CTR-related communication.

Mitigation: Review each generated summary for medical accuracy, audience fit, and regulatory suitability before sharing or relying on it.

Risk: The skill is a draft-quality helper rather than a validated medical or regulatory compliance tool.

Mitigation: Treat its output as a drafting aid and route patient-facing, public, or compliance-sensitive summaries through qualified domain review.

Risk: The artifact includes a local Python execution path that processes user-provided abstract text.

Mitigation: Run the script in a controlled workspace and avoid processing sensitive health data unless the environment and review process are approved for that data.

## Reference(s):

- [Lay Summary Gen References](artifact/references/guidelines.md)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/lay-summary-gen-1)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON object or Markdown response with assumptions, risks, and next checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a lay summary, reading level estimate, key takeaways, word counts, and jargon replacements.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
