## Description: <br>
Automates RZL Klientenportal.at for login and logout, uploading receipts and invoices, listing released files, and downloading accountant-provided documents via Playwright. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[odrobnik](https://clawhub.ai/user/odrobnik) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, accounting staff, and developers use this skill to automate document exchange with an RZL Klientenportal account, including uploading accounting documents and downloading accountant-provided files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Klientenportal credentials and can access sensitive accounting documents. <br>
Mitigation: Prefer environment variables or a protected config file, do not commit config.json, and run logout on shared machines. <br>
Risk: Upload and download commands can move financial documents to or from the portal. <br>
Mitigation: Review upload patterns, document categories, and download destinations before running commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/odrobnik/klientenportal) <br>
- [RZL Klientenportal](https://klientenportal.at) <br>
- [RZL Software](https://www.rzl.at) <br>
- [Setup instructions](SETUP.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, JSON, Files, Configuration guidance] <br>
**Output Format:** [CLI text output, optional JSON for received-file listings, and downloaded document files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads are written under /tmp/openclaw/klientenportal by default or to a workspace-/tmp-scoped output directory.] <br>

## Skill Version(s): <br>
1.5.1 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
