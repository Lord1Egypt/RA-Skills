## Description: <br>
Query Chinese labor law on overtime, leave, contracts, and severance rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, advisors, and developers can use this skill to look up Chinese labor-law reference material for worker rights, overtime, leave, contracts, disputes, and severance. It also includes a command-line logging utility, so users should avoid recording confidential employment or dispute details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release mixes Chinese labor-law lookup behavior with a generic plaintext local logging tool. <br>
Mitigation: Review the installed commands before use and rely only on the labor-law reference behavior if that is the intended use case. <br>
Risk: Logging commands can store confidential employment, salary, contract, employee, or dispute details in local plaintext files. <br>
Mitigation: Do not enter sensitive details into logging commands; use non-sensitive summaries or a separate approved secure records system. <br>
Risk: The documented remove command does not provide verified erasure of stored sensitive data. <br>
Mitigation: Do not rely on remove for data deletion until the implementation is corrected and deletion behavior is independently verified. <br>
Risk: The legal reference content may be incomplete, outdated, or not applicable to a specific jurisdiction or case. <br>
Mitigation: Treat outputs as general reference material and consult a qualified labor lawyer for case-specific decisions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ckchzh/labor-law) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown tables, terminal text, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some commands write plaintext local logs under the configured labor-law data directory.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
