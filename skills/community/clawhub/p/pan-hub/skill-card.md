## Description:

Helps an agent route supported cloud drive sharing links and direct URLs through a unified download workflow to a local folder, NAS, or private storage, with login guidance and credential handling instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lisong2003-lgtm](https://clawhub.ai/user/lisong2003-lgtm)

### License/Terms of Use:

CC BY-NC-SA 4.0

## Use Case:

Developers and people managing personal or organizational files can use the skill to download supported cloud drive shares or direct links to local storage, NAS, or private storage. It also provides setup guidance for account authorization, download destinations, and credential handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious with medium confidence, citing an unauthenticated download control API, automatic clipboard-triggered downloads, persistent services, capabilities beyond the stated downloader purpose, and partial inspection of some files and checks.

Mitigation: Review the reported controls, clipboard monitoring, and background services before installing. The scan guidance says this is not a claim of malicious intent and does not establish unrestricted file overwrite or response-body exfiltration.

## Reference(s):

- [Project overview and supported storage](README.md)
- [Agent usage and privacy](references/20-Agent调用与隐私.md)
- [Remote NAS and private storage](references/21-远程NAS与私有存储.md)
- [MCP and agent interface](references/23-MCP与Agent接口.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, JSON plans, Guidance]

**Output Format:** [Shell commands, JSON plans, and Markdown or plain text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.7.0 (source: ClawHub release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
