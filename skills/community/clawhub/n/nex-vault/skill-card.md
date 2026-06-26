## Description: <br>
Nex Vault helps agents set up and operate a local contract and document vault for tracking business documents, extracting deadlines and clauses, and surfacing expiry or renewal alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nexaiguy](https://clawhub.ai/user/nexaiguy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External business users, agency operators, SME owners, directors, and managers use this skill to manage contracts, leases, policies, subscriptions, certificates, permits, and other documents while tracking expirations, renewal deadlines, termination notice periods, costs, and optional Telegram alerts. <br>

### Deployment Geography for Use: <br>
Global, with Belgian and EU contract-date formats emphasized by the source documentation <br>

## Known Risks and Mitigations: <br>
Risk: Telegram credential setup can unsafely modify the user's shell startup file. <br>
Mitigation: Review before installing and avoid the built-in Telegram credential setup unless it is fixed to use safe app-scoped storage instead of ~/.bashrc. <br>
Risk: The local-only privacy framing under-discloses that enabled Telegram alerts may send document names and deadline details to Telegram. <br>
Mitigation: If Telegram alerts are enabled, assume document names and deadline details may be sent to Telegram and disclose that external notification path to users. <br>
Risk: Exports can contain sensitive vault information, potentially including extracted document text. <br>
Mitigation: Use the vault only for files intentionally added and treat CSV or JSON exports as sensitive business records. <br>


## Reference(s): <br>
- [Nex Vault README](README.md) <br>
- [Nex Vault Skill Documentation](SKILL.md) <br>
- [Nex AI Homepage](https://nex-ai.be) <br>
- [Nex Vault ClawHub Listing](https://clawhub.ai/nexaiguy/nex-vault) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text CLI output and Markdown guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may create local vault files, alerts, CSV or JSON exports, and optional Telegram notifications.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
