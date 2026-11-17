## Description:

AI-powered academic paper reviewer. Uses a multi-agent system (Deconstructor, Devil's Advocate, Judge) to analyze papers for logical flaws, contradictions, and empirical validity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sschepis](https://clawhub.ai/user/sschepis)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and technical reviewers use this skill to analyze academic papers or scientific claims for logical flaws, contradictions with literature, and empirical validity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paper text and extracted claims may be sent to configured third-party LLM and search providers.

Mitigation: Use the skill only with approved providers and non-confidential content unless data handling has been reviewed.

Risk: The shell-based SkillSearchAdapter introduces unsafe command execution risk.

Mitigation: Disable or replace that adapter before production use, or strictly constrain executable paths and arguments.

Risk: Credential handling and report storage paths are under-scoped for sensitive manuscripts.

Mitigation: Use least-privilege credentials and harden report storage paths before processing confidential or unpublished work.

Risk: The arXiv adapter uses an HTTP endpoint.

Mitigation: Switch the arXiv integration to HTTPS before relying on it in higher-trust environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sschepis/skills/peer-reviewer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON merit report with scores, objections, defense strategy, and suggested improvements]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also save the report as a JSON file when run through the standalone CLI.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
