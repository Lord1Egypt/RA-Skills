## Description: <br>
Use when OpenClaw needs to access AICFO through one bearer API key for session introspection, company selection, connector actions, Company-DB reads, document workflows, and the local adapter bridge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elvismusli](https://clawhub.ai/user/elvismusli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate AICFO through a scoped API key, resolve company access, read company data, inspect documents, and run bounded connector actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A single AICFO API key can read company data and trigger connector or document workflow changes. <br>
Mitigation: Use a least-privilege API key, set an explicit company scope, and require manual approval before connector actions or write-like document operations. <br>
Risk: Connector actions, imports, deletes, clarification submissions, reprocessing, or saved templates may change external systems or business workflows. <br>
Mitigation: Review the planned action, confirm the target company and provider scope, and approve only bounded operations with clear input payloads. <br>


## Reference(s): <br>
- [AICFO Homepage](https://aiceo.city) <br>
- [ClawHub Skill Page](https://clawhub.ai/elvismusli/openclaw-aicfo-agent) <br>
- [Operations Reference](references/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command examples and JSON command payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node and an AICFO_API_KEY; company scope should be selected from session results when no implicit company is available.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
