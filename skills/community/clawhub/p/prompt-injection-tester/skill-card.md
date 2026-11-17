## Description:

Test LLM applications for prompt injection vulnerabilities, run attack simulations, evaluate defenses, and generate hardening recommendations for AI systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, and AI application teams use this skill to assess chatbots, RAG systems, AI agents, and other LLM-integrated applications for prompt injection weaknesses. It supports structured attack simulation, defense evaluation, vulnerability scoring, and prioritized hardening recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes risky prompt-injection example payloads that could be misused against systems without authorization.

Mitigation: Use the skill only on applications you own or have explicit permission to test, and do not apply payloads to third-party systems.

Risk: Testing against production systems can expose sensitive prompts, tool behavior, or application data in reports.

Mitigation: Prefer approved test environments, document authorization, and redact sensitive payloads, responses, and system details from shared reports.

Risk: Hardening recommendations may be incomplete or unsuitable for a specific deployment.

Mitigation: Review recommendations with application owners and validate changes before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/skills/prompt-injection-tester)
- [ClawHub Publisher Profile](https://clawhub.ai/user/charlie-morrison)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown security report with vulnerability summary, critical findings, and prioritized hardening recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include example payloads, defense maturity scoring, and remediation priorities.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
