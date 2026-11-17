## Description:

Evaluate and harden AI agent memory against memory trap and OWASP ASI06-style attacks by scoring resistance, reporting category breakdowns, and providing hardening guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaymizuno](https://clawhub.ai/user/shaymizuno)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to benchmark AI agent memory integrity against memory poisoning and context manipulation risks, then apply hardening guidance before deploying or updating agent memory systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and run an unpinned third-party package.

Mitigation: Use an isolated environment and pin and verify the memtrap package before production use.

Risk: Benchmarking may involve sensitive or proprietary agent memory data.

Mitigation: Use synthetic or redacted memory unless the package behavior and data handling have been audited.

Risk: Leaderboard submission may expose context, benchmark results, or related metadata publicly.

Mitigation: Treat submissions as public and submit only reviewed, non-sensitive contexts and results.

## Reference(s):

- [Memtrap Skill on ClawHub](https://clawhub.ai/shaymizuno/skills/memtrap)
- [Memtrap project homepage](https://github.com/shaymizuno/memtrap)
- [DeepMind memory trap paper](https://ssrn.com/abstract=6372438)
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [OWASP Agent Memory Guard](https://owasp.org/www-project-agent-memory-guard/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes benchmark scores, per-category breakdowns, hardening recommendations, and badge or leaderboard submission guidance.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
