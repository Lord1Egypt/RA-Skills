## Description:

Delivers weekday revenue cycle management intelligence, CRCR-aligned learning prompts, and SparkChange-focused takeaways from healthcare RCM news and study materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3m2b](https://clawhub.ai/user/j3m2b)

### License/Terms of Use:

MIT-0

## Use Case:

Operations and revenue cycle teams use this skill to receive concise daily scans of claims, denials, payer behavior, regulatory changes, AI in RCM, and patient financial experience. It also supports an individual CRCR learning plan with checkpoint questions, case studies, and running knowledge-base updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports an exposed Moltbook API token.

Mitigation: Remove the token from artifact scripts, rotate the credential, and require secrets to be supplied through environment variables or a managed secret store.

Risk: The release evidence reports automatic external posting behavior to Moltbook and messaging workflows for Telegram or Discord.

Mitigation: Require explicit confirmation or a dry-run mode before publishing posts or sending messages outside the agent environment.

Risk: The release evidence warns against putting real PHI, PII, or client data into learning logs, case studies, or archives.

Mitigation: Use synthetic or de-identified examples only, and review generated RCM content before storing or sharing it.

## Reference(s):

- [Rcm Pulse ClawHub Release](https://clawhub.ai/j3m2b/skills/jb-rcm-pulse)
- [j3m2b Publisher Profile](https://clawhub.ai/user/j3m2b)
- [HFMA CRCR Candidate Key Concepts Guide](https://www.hfma.org/wp-content/uploads/2024/12/crcrconceptguide3_4_24-lonestar.pdf)
- [CRCR Study Resources](artifact/CRCR_STUDY_RESOURCES.md)
- [RCM Learning Path](artifact/LEARNING_PATH.md)
- [RCM Knowledge Base](artifact/KNOWLEDGE_BASE.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, code, configuration]

**Output Format:** [Markdown briefs, learning prompts, archive entries, social post text, and automation snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include external post payloads, scheduled-run configuration, and escalation messages for major regulatory, payer, or technology changes.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
