## Description:

Provides multi-perspective A-share investment research guidance across fundamentals, technical signals, news sentiment, risk debate, and composite scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, investors, and finance-oriented agent operators use this skill to structure A-share research workflows, compare multiple analysis angles, and produce investment research summaries or risk-aware decision support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is suspicious because the skill requests broad command access and API key setup without clear enforceable limits.

Mitigation: Review before installing, run only in an isolated environment, store API keys in the platform secret manager, and require approval before commands execute.

Risk: The artifact describes investment suggestions and risk signals that may be inaccurate, incomplete, or unsuitable for a user's financial situation.

Mitigation: Treat outputs as decision-support material only and require qualified human review before making investment decisions.

Risk: The artifact includes security checklist claims, but the authoritative evidence warns not to rely on that checklist as proof that protections are enforced.

Mitigation: Validate security controls independently and do not treat the skill text's security statements as implementation guarantees.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/multi-research)
- [Skill homepage](https://skillhub.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured analysis, JSON examples, Python snippets, and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include finance research summaries, risk signals, composite scores, setup guidance, troubleshooting steps, and investment suggestions that require human review.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
