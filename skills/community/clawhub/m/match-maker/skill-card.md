## Description:

AI-powered matchmaking skill for dating and relationships - profile analysis, compatibility matching, icebreaker generation, and relationship tracking for individuals seeking meaningful connections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill to evaluate dating readiness, compare compatibility with a potential partner, generate conversation starters and date ideas, and track relationship development. The guidance is intended to support human judgment, not replace personal choice or professional counseling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may collect extensive sensitive personal, dating, and relationship details.

Mitigation: Limit prompts to information necessary for the requested analysis, avoid unnecessary sensitive fields, and tell users not to share details they do not want processed.

Risk: Compatibility analysis can include details about another person who has not consented.

Mitigation: Ask users to confirm they have consent to include another person's information, and support generalized guidance when consent is unclear.

Risk: The artifact makes privacy assurances that are not confirmed by the security evidence.

Mitigation: Do not promise local-only handling unless runtime and storage behavior are separately verified.

Risk: Dating scores and relationship predictions may be over-relied on for personal decisions.

Mitigation: Frame outputs as guidance with limitations, encourage human judgment, and recommend professional support for safety, abuse, or counseling concerns.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhenstaff/skills/match-maker)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with structured scores, recommendations, and example Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include compatibility scores, profile assessments, conversation starters, date ideas, relationship health indicators, limitations, and next steps.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and README report 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
