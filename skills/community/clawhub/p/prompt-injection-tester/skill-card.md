## Description: <br>
Test LLM applications for prompt injection vulnerabilities - run attack simulations, evaluate defenses, and generate hardening recommendations for AI systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security reviewers, developers, and AI application owners use this skill to test chatbots, RAG systems, AI agents, and other LLM-integrated applications for prompt injection weaknesses and to generate hardening recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt-injection tests can affect systems or data if run without authorization. <br>
Mitigation: Install and use the skill only for systems you own or have explicit permission to test. <br>
Risk: Resource-heavy or data-mutating tests may disrupt production workflows. <br>
Mitigation: Prefer staging or isolated environments and obtain explicit approval before resource-heavy or data-mutating tests. <br>
Risk: RAG or tool-call testing can leave test prompts, poisoned documents, or manipulated records behind. <br>
Mitigation: Remove test prompts and poisoned documents after testing, and document cleanup for audit trails. <br>


## Reference(s): <br>
- [Prompt Injection Tester on ClawHub](https://clawhub.ai/charlie-morrison/prompt-injection-tester) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown security report with vulnerability summaries, findings, scores, and prioritized recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include test payloads, observed responses, risk ratings, and defense maturity scoring.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
