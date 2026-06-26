## Description: <br>
Detects AI-generated writing patterns in prose. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, documentation maintainers, and reviewers use this skill to audit prose, technical documentation, and repository text for dense AI-writing markers, identity leaks, hallucinated references, stubs, and weak evidence behind public claims. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can steer an agent toward broad repository audits, CI gates, network checks, and remediation workflows that exceed a passive prose review. <br>
Mitigation: Invoke it on explicit target files or directories, review proposed checks before execution, and approve any CI or repository-wide changes separately. <br>
Risk: Automated remediation could remove acceptable prose, domain-specific wording, or low-confidence findings without enough context. <br>
Mitigation: Treat findings as review recommendations, require human approval for edits, and avoid auto-applying low-confidence changes. <br>
Risk: The identity-linked fiction heuristic may be unsuitable for automated decisions. <br>
Mitigation: Use that heuristic only as a manual review signal and do not make acceptance, rejection, or enforcement decisions from it alone. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-scribe-slop-detector) <br>
- [ClawHub metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/scribe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with findings, scores, recommendations, and optional command or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include line-anchored findings, severity labels, confidence levels, and remediation guidance.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
