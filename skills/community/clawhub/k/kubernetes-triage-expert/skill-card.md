## Description: <br>
Analyze Kubernetes faults from user-provided evidence, classify the fault, rank likely hypotheses, request the next highest-value checks, and keep facts separate from guesses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ghostwritten](https://clawhub.ai/user/ghostwritten) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and platform engineers use this skill to triage Kubernetes incidents from supplied statuses, logs, events, and change context without granting cluster access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may include secrets, tokens, kubeconfigs, or sensitive operational logs while providing incident evidence. <br>
Mitigation: Redact sensitive values before using the skill and provide only the minimum evidence needed for triage. <br>
Risk: Incomplete evidence can lead to premature or incorrect root-cause conclusions. <br>
Mitigation: Treat the output as advisory, require hypotheses to be tied to supplied evidence, and validate findings with targeted checks before making changes. <br>
Risk: Unclear language prompts may produce Chinese output by default. <br>
Mitigation: State the preferred response language explicitly when a specific language is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ghostwritten/kubernetes-triage-expert) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown triage report with canonical sections for assessment, confirmed facts, hypotheses, next checks, and conclusions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Limits active hypotheses and next checks to three each; preserves Kubernetes identifiers, status strings, event reasons, and exact error text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
