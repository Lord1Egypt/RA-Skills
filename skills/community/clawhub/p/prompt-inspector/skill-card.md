## Description: <br>
Detect prompt injection attacks and adversarial inputs in user text before passing it to your LLM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aunicall](https://clawhub.ai/user/aunicall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI application teams use this skill to screen user-provided text for prompt injection, jailbreak, instruction override, and related adversarial patterns before forwarding input to an LLM. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Inspected text may be sent to Prompt Inspector or another configured endpoint. <br>
Mitigation: Use the skill only for data flows approved by your organization, and avoid submitting secrets, regulated data, customer records, or proprietary system prompts unless that transfer is allowed. <br>
Risk: API keys can be exposed when passed directly on the command line. <br>
Mitigation: Prefer the PMTINSP_API_KEY environment variable or the documented local environment file instead of inline command arguments. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/aunicall/prompt-inspector) <br>
- [Prompt Inspector website](https://promptinspector.io) <br>
- [Prompt Inspector documentation](https://docs.promptinspector.io) <br>
- [Product information](references/product-info.md) <br>
- [Usage guide](references/usage.md) <br>
- [FAQ](references/faq.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Human-readable text or JSON detection results with command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Detection results include a safety verdict, risk score, threat categories, request ID, and latency when returned by the configured Prompt Inspector endpoint.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
