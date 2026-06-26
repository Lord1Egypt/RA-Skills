## Description: <br>
Prevents panic-driven errors by enforcing a calm, step-by-step recovery process after mistakes or critical feedback to support safe, trusted fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vanhuelsing](https://clawhub.ai/user/vanhuelsing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and agent operators use this skill after mistakes, urgent criticism, or pressure to bypass process. It guides the agent to stop, assess impact, propose a recovery plan, wait for approval, execute deliberately, verify the result, and document the lesson. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The pause-and-approval workflow could delay genuine containment when credentials, private data, or production systems are actively exposed. <br>
Mitigation: Test the skill in urgent operational workflows and use its severity guidance to stop first, inform the user immediately, assess with an urgency flag, and let the user approve containment. <br>
Risk: Agents may over-apply the protocol after an incident and become unnecessarily slow or approval-heavy on routine corrections. <br>
Mitigation: Use the included test scenarios and severity quick reference to distinguish low-risk corrections from high-risk recovery work. <br>
Risk: An agent under pressure may still bypass delegation, deployment, verification, or approval steps. <br>
Mitigation: Place the protocol in the agent system prompt and verify behavior with the included delegation, data exposure, deadline pressure, and cascading correction scenarios. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/vanhuelsing/panic-prevention) <br>
- [README](README.md) <br>
- [Protocol Flow](PROTOCOL-FLOW.md) <br>
- [Test Scenarios](tests/test-scenarios.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions] <br>
**Output Format:** [Markdown protocol with prompt snippets, decision flow guidance, and test scenarios] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; no runtime dependencies or hidden execution behavior were identified in server security evidence.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and ClawHub metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
