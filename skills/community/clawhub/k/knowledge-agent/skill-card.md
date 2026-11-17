## Description:

Knowledge Agent helps OpenClaw users turn domain expertise into a client-facing consulting agent with layered knowledge, safety constraints, search verification, and Feishu group delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonlin1212](https://clawhub.ai/user/simonlin1212)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, consultants, and OpenClaw users use this skill to build domain-specific consulting agents that answer client questions in Feishu groups while preserving knowledge boundaries and safety constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: No-mention Feishu delivery and broad group access can make the agent respond in unintended groups.

Mitigation: Prefer an allowlisted Feishu group, disclose the bot to participants, test group behavior before inviting clients, and avoid the open all-groups policy unless that exposure is intended.

Risk: Broad web, browser, and file-write access can amplify bad search results or expose more workspace state than needed.

Mitigation: Pin or verify search skill dependencies, keep tool permissions least-privileged, cite sources when possible, and cross-check search results against the curated knowledge base.

Risk: The setup script creates files from user-supplied agent IDs, domains, and workspace paths.

Mitigation: Review and validate those inputs before running the script, avoid untrusted values, and inspect the generated workspace files before deployment.

Risk: Paid consulting answers may still be incomplete, outdated, or misleading.

Mitigation: Keep human monitoring and escalation paths, require the agent to say when it is uncertain, and periodically test out-of-domain, fabricated-concept, and source-verification cases.

## Reference(s):

- [Knowledge Agent release page](https://clawhub.ai/simonlin1212/skills/knowledge-agent)
- [Three-Layer Knowledge Architecture](references/knowledge-layers.md)
- [Safety Constraints for Paid Consulting](references/safety-constraints.md)
- [Anti-Hallucination: Quality Controls](references/anti-hallucination.md)
- [Feishu Group Delivery Setup](references/feishu-delivery.md)
- [Complete Example: Douyin Operations Consultant](references/example-douyin.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks, template-backed configuration files, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate AGENTS.md, SOUL.md, IDENTITY.md, MEMORY.md, TOOLS.md, and a knowledge/ directory scaffold.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
