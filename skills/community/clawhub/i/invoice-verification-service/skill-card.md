## Description: <br>
Use the local invoice service script to initialize app keys, query quota and packages, verify invoice text or images, batch-verify local folders, and create or query recharge orders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fenghaozhe-git](https://clawhub.ai/user/fenghaozhe-git) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to run a Node.js helper for invoice verification workflows, including quota checks, package lookup, invoice text or image verification, batch folder verification, and recharge order management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload sensitive invoice text, invoice images, extracted identifiers, and local file metadata to the configured invoice API endpoint. <br>
Mitigation: Review the configured API base URL before real invoice use, install only when the endpoint is trusted, and avoid unattended or implicit verification of sensitive invoices. <br>
Risk: The helper can create recharge orders, which is a payment-related action. <br>
Mitigation: Require explicit user approval before order creation and confirm amount and payment destination before following any payment URL. <br>
Risk: The helper persists app keys, configuration, and batch verification result files on disk. <br>
Mitigation: Periodically inspect or delete ~/.openclaw/invoice-skill/config.json and generated *.verify.json or invoice-verify-results-* files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fenghaozhe-git/invoice-verification-service) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; script actions return JSON and batch verification may write JSON result files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js. Invoice image verification accepts PNG or JPEG payloads up to 2 MB, and directory verification writes per-image result JSON plus a summary for multi-file batches.] <br>

## Skill Version(s): <br>
0.4.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
