## Description: <br>
Lemma is an AI operating system platform for business teams that helps agents design, provision, test, and improve Lemma pods, datastores, integrations, functions, workflows, desks, assistants, agents, widgets, and workspace execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deepak-jha-kgp](https://clawhub.ai/user/deepak-jha-kgp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business automation teams use Lemma to design and operate AI-powered business systems with routed guidance for data, integrations, functions, workflows, desks, assistants, agents, widgets, and workspace execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide changes to Lemma platform resources and connected workflows. <br>
Mitigation: Use test pods where possible, review CLI payloads before production changes, and verify upstream resources before wiring downstream desk actions. <br>
Risk: Tokens, connected accounts, scheduled workflows, and event-triggered workflows can create unintended access or side effects if handled carelessly. <br>
Mitigation: Protect Lemma tokens and connected accounts, grant only needed access, and double-check scheduled or event-triggered workflows before leaving them active. <br>


## Reference(s): <br>
- [Lemma ClawHub release](https://clawhub.ai/deepak-jha-kgp/lemma) <br>
- [Known CLI behavior](modules/lemma-main/references/known-cli-behavior.md) <br>
- [Design MD reference](https://github.com/VoltAgent/awesome-design-md/tree/main/design-md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON examples, code snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes work to module-specific guides before implementation and emphasizes verification before production changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
