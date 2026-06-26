## Description: <br>
Implement Google Pay for web and Android with tokenization safety, gateway alignment, and production-ready checkout operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to plan, implement, validate, launch, and operate Google Pay integrations for web, Android, PSP-mediated checkout, and recurring payment flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checkout and payment changes can affect live authorizations, captures, refunds, and customer conversion. <br>
Mitigation: Use test mode first, verify backend or PSP behavior before release, and require the launch and validation checklists before production rollout. <br>
Risk: PSP secrets or raw Google Pay token payloads could be exposed if copied into chat, logs, screenshots, or local notes. <br>
Mitigation: Keep PSP secrets and raw payment tokens out of chat and local notes; store only minimal metadata such as request id, status, amount, and currency. <br>
Risk: Local project state under ~/google-pay may retain integration decisions, validation evidence, or incident notes. <br>
Mitigation: Review or delete ~/google-pay when retained project state is no longer wanted. <br>


## Reference(s): <br>
- [Google Pay Skill Page](https://clawhub.ai/ivangdavila/google-pay) <br>
- [Google Pay](https://pay.google.com) <br>
- [Google Pay JavaScript Client Library](https://pay.google.com/gp/p/js/pay.js) <br>
- [Google Pay Developer Documentation](https://payments.developers.google.com) <br>
- [setup.md](artifact/setup.md) <br>
- [implementation-playbook.md](artifact/implementation-playbook.md) <br>
- [validation-checklist.md](artifact/validation-checklist.md) <br>
- [launch-playbook.md](artifact/launch-playbook.md) <br>
- [failure-handling.md](artifact/failure-handling.md) <br>
- [recurring-payments.md](artifact/recurring-payments.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with checklists, implementation notes, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local project notes under ~/google-pay when the user approves setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
