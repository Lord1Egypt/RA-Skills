## Description: <br>
Use when Vietnam equity recommendations need D1-backed approvals, compliance checks, audit logging, decision journals, or approved target portfolio state transitions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ndtchan](https://clawhub.ai/user/ndtchan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and portfolio-governance operators use this skill to manage approval-gated Vietnam equity recommendations, Cloudflare D1 state changes, compliance checks, audit events, and approved target portfolio transitions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A misconfigured Cloudflare D1 database or approval workflow could record governance state in the wrong environment. <br>
Mitigation: Confirm the intended D1 database and approval workflow before installation or use. <br>
Risk: Providing broker credentials or execution permissions could blur the boundary between governance records and live trading. <br>
Mitigation: Do not provide broker credentials or execution permissions; this skill is designed for approvals, audit records, and target state only. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ndtchan/institutional-governance) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Guidance] <br>
**Output Format:** [Structured text or Markdown fields covering D1 write intent, affected tables, approval status, compliance status, state transition, audit summary, mutation permission, broker execution permission, and confidence.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Broker execution must remain false; state mutation is gated by compliance checks and explicit approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
