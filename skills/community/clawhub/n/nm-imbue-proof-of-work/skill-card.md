## Description: <br>
Enforces validation and evidence before claiming work complete. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill before declaring implementation, configuration, review, or delivery work complete. It guides them to reproduce the problem, test the solution in the current environment, capture evidence, and document blockers or acceptance criteria. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation can add validation overhead outside proof-of-work or pre-PR checks. <br>
Mitigation: Invoke the skill only for completion claims, pre-PR checks, and other workflows where evidence capture is required. <br>
Risk: Evidence logs can accidentally include environment variables, API keys, tokens, credentials, or authentication output. <br>
Mitigation: Redact or mask secrets before adding command output, logs, tickets, or citations to evidence records. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/athola/skills/nm-imbue-proof-of-work) <br>
- [OpenClaw metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/imbue) <br>
- [Acceptance criteria reference](https://www.atlassian.com/agile/project-management/definition-of-done) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with checklists, YAML-style output contracts, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Evidence-oriented output may include command snippets, acceptance criteria, validation status, and reproducibility notes.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
