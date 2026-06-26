## Description: <br>
OpenKM Document Management via REST API (folders, documents, metadata, versioning, search, workflows). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pes0](https://clawhub.ai/user/pes0) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and document management users use this skill to let an agent list, search, upload, download, organize, version, and route documents in OpenKM through its REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, change, and delete documents using the configured OpenKM account. <br>
Mitigation: Use a least-privilege OpenKM user and confirm delete, move, restore-version, checkin, upload-version, and workflow task actions before execution. <br>
Risk: OpenKM credentials are required in environment variables. <br>
Mitigation: Keep OPENKM_PASSWORD out of shared profiles and logs, and avoid OPENKM_DEBUG except during local troubleshooting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pes0/openkm-rest) <br>
- [README.txt](artifact/README.txt) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Text, JSON] <br>
**Output Format:** [Markdown with inline shell commands and CLI text or JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenKM connection settings in environment variables; workflow commands depend on OpenKM workflow configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
