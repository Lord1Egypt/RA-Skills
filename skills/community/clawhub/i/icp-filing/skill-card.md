## Description: <br>
ICP filing assistant for China websites that provides filing guidance, document checklists, provider selection help, timelines, common questions, domain filing query guidance, provincial prefixes, and footer code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site operators, and businesses preparing China website ICP filings can use this skill to generate filing checklists, process timelines, domain query instructions, provincial ICP prefixes, and footer markup. <br>

### Deployment Geography for Use: <br>
Global, for websites subject to China ICP filing requirements. <br>

## Known Risks and Mitigations: <br>
Risk: Generic helper commands can save user-entered text and command history in local plaintext under ICP_FILING_DIR or ~/.local/share/icp-filing. <br>
Mitigation: Avoid entering IDs, filing materials, tokens, business details, or private notes; set ICP_FILING_DIR to a reviewed location before use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown-style summaries, with optional HTML footer code and shell-command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns summaries to stdout; generic helper commands may also write local data and command history under ICP_FILING_DIR or ~/.local/share/icp-filing.] <br>

## Skill Version(s): <br>
2.3.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
