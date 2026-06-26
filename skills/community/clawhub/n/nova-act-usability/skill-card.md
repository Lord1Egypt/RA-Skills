## Description: <br>
AI-orchestrated usability testing using Amazon Nova Act that generates personas, runs browser-based tests, interprets raw responses, and produces HTML reports for real user workflows such as booking, checkout, and posting with safety guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zouchaoqun](https://clawhub.ai/user/zouchaoqun) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and QA teams use this skill to evaluate website usability by simulating realistic personas and browser workflows, then reviewing interpreted results and an HTML report. It is especially suited to checkout, booking, signup, posting, and general UX evaluation flows that can be tested without completing final material-impact actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate browser workflows that approach state-changing actions such as checkout, signup, posting, and form submission. <br>
Mitigation: Run it in test or sandbox environments and supervise workflows involving carts, checkout, signup, posting, or forms. <br>
Risk: Nova Act traces and generated reports can persist screenshots, page content, and sensitive information visible during testing. <br>
Mitigation: Avoid authenticated or confidential production sites and review or delete nova_act_logs and reports after use. <br>
Risk: Using ANTHROPIC_API_KEY may send site analysis to a third-party model provider for persona generation. <br>
Mitigation: Leave ANTHROPIC_API_KEY unset unless third-party persona generation is acceptable. <br>
Risk: The skill requires a Nova Act API key and gives the agent browser control against the target site. <br>
Mitigation: Install only when this operating model is acceptable, keep credentials scoped, and monitor runs that interact with real services. <br>


## Reference(s): <br>
- [Nova Act Cookbook](references/nova-act-cookbook.md) <br>
- [Persona Examples](references/persona-examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zouchaoqun/nova-act-usability) <br>
- [Publisher Profile](https://clawhub.ai/user/zouchaoqun) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON/HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local Nova Act trace logs, adaptive test results JSON, and an HTML usability report in the working directory.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
