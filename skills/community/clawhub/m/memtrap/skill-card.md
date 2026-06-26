## Description: <br>
Memtrap evaluates agent memory integrity against trap-style attacks and OWASP ASI06 memory poisoning risks, then provides resistance scores and hardening guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaymizuno](https://clawhub.ai/user/shaymizuno) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to benchmark and harden agent memory, RAG stores, and memory integrations before production use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Active mode can alter persistent agent memory. <br>
Mitigation: Use benchmark mode first on synthetic or backed-up memory, and avoid active mode on production memory until mutation and rollback behavior are understood. <br>
Risk: The leaderboard submission flow may expose sensitive context. <br>
Mitigation: Do not submit secrets, private user data, proprietary prompts, or real internal memory context to the leaderboard command. <br>
Risk: The skill depends on an external memtrap package. <br>
Mitigation: Pin and inspect the external package before installation or deployment. <br>


## Reference(s): <br>
- [DeepMind trap paper](https://ssrn.com/abstract=6372438) <br>
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) <br>
- [OWASP Agent Memory Guard](https://owasp.org/www-project-agent-memory-guard/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Markdown] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include benchmark scores, category breakdowns, hardening recommendations, badge links, and memory-protection examples.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
