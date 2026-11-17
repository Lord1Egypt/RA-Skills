## Description:

Automate patient support with AI-driven chatbot that answers queries, schedules appointments, and integrates with EMR/CRM systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncreighton](https://clawhub.ai/user/ncreighton)

### License/Terms of Use:

MIT-0

## Use Case:

Healthcare providers, clinics, and wellness businesses use this skill to automate routine patient support, appointment scheduling, billing and insurance FAQs, reminders, and escalation workflows across chat and messaging channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects to sensitive healthcare systems and may access protected health information through EMR, CRM, messaging, and analytics integrations.

Mitigation: Complete HIPAA and BAA review before deployment, minimize collected patient data, obtain explicit patient consent and notice for EMR access and logging, and de-identify analytics outputs where possible.

Risk: The release asks users to deploy opaque mutable code and external widget or package artifacts.

Mitigation: Install only pinned, reviewed package and widget builds, scan them before deployment, and avoid mutable production dependencies.

Risk: Broad credentials could permit excessive access to EMR, CRM, Twilio, or model-provider systems.

Mitigation: Use narrowly scoped non-production credentials during setup, runtime-only production secrets, strict EMR write limits, and least-privilege access for each integration.

Risk: Patient-facing responses could be mistaken for medical diagnosis, prescription guidance, emergency care, or clinical judgment.

Mitigation: Keep medical-disclaimer and escalation boundaries active, route urgent or medication-related issues to qualified staff, and require human review for complex clinical or billing cases.

## Reference(s):

- [Healthcare Chatbot Pro on ClawHub](https://clawhub.ai/ncreighton/skills/healthcare-chatbot-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with configuration examples, code snippets, shell commands, and sample patient-support messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires reviewed runtime integrations and credentials for OpenAI, Twilio, EMR, CRM, and optional calendar systems.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
