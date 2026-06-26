## Description: <br>
Manage Namecheap DNS records safely by fetching existing entries, merging changes, auto-backing up, previewing diffs, dry-running, and rolling back updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jarekbird](https://clawhub.ai/user/jarekbird) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and domain operators use this skill to inspect, add, remove, back up, and restore Namecheap DNS records while previewing changes and preserving existing records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change DNS records for domains accessible to the configured Namecheap API key. <br>
Mitigation: Use dry-run first, review the diff, keep backups enabled, and restrict the API key to domains and users that are appropriate for the task. <br>
Risk: Crafted domain input could run unintended local shell commands. <br>
Mitigation: Do not pass untrusted domain strings; prefer a patched version that validates domain names and calls dig with argument arrays instead of shell command strings. <br>
Risk: Namecheap DNS updates can remove records that are not visible through the Namecheap API. <br>
Mitigation: Run the verify command before destructive operations, review ghost record warnings, and use the force option only after confirming the hidden records can be removed. <br>


## Reference(s): <br>
- [ClawHub Namecheap DNS Skill](https://clawhub.ai/jarekbird/namecheap-dns) <br>
- [Namecheap API Documentation](https://www.namecheap.com/support/api/) <br>
- [Namecheap Domains DNS API Methods](https://www.namecheap.com/support/api/methods/domains-dns/) <br>
- [Namecheap API Access Settings](https://ap.www.namecheap.com/settings/tools/apiaccess/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Files] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create DNS backup JSON files and DNS snapshots before changes.] <br>

## Skill Version(s): <br>
1.1.0 (source: package.json and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
