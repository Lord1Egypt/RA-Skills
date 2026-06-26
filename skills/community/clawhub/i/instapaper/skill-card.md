## Description: <br>
Use when operating the instapaper-cli (ip) tool or troubleshooting it: authenticating, listing/exporting/importing bookmarks, bulk mutations, folders/highlights/text, choosing output formats (ndjson/json/plain), cursor-based sync, and interpreting stderr-json/exit codes for automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vburojevic](https://clawhub.ai/user/vburojevic) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation-focused users use this skill to operate the Instapaper CLI reliably, including authentication, bookmark import and export, bulk bookmark changes, folders, highlights, text extraction, cursor-based sync, and structured error handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external Instapaper CLI that can access credentials and change bookmark data. <br>
Mitigation: Install the external ip CLI only from a trusted source, consider pinning or reviewing a specific release, and protect Instapaper credentials. <br>
Risk: Bulk import, export, folder, highlight, and delete operations can modify or remove user data. <br>
Mitigation: Require explicit approval before running bulk or destructive commands and use dry-run, idempotent, or confirmation flags where available. <br>


## Reference(s): <br>
- [Instapaper Skill Page](https://clawhub.ai/vburojevic/instapaper) <br>
- [commands.md](references/commands.md) <br>
- [output-and-sync.md](references/output-and-sync.md) <br>
- [errors.md](references/errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands and structured-output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe NDJSON, JSON, plain text, structured stderr, progress events, cursor files, and output files produced by the external ip CLI.] <br>

## Skill Version(s): <br>
0.2.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
