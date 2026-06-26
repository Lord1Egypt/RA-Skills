## Description: <br>
Generate, validate, export, and manage MOCI, the identity system for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mociforge](https://clawhub.ai/user/mociforge) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators of OpenClaw agents use this skill to create and manage local agent identities, verify memory-chain continuity, export and import identities, configure gateway integration, and assess trust posture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates persistent local identity and authentication state under ~/.openclaw. <br>
Mitigation: Review before installing, protect local identity files and backups, and inspect or obtain the actual implementation before relying on it for authentication. <br>
Risk: Memory-chain logs, key pins, gateway hooks, and trust-score effects can affect agent authentication and authorization posture. <br>
Mitigation: Review gateway configuration and key-pinning behavior before deployment, and test trust-score handling in a controlled environment. <br>
Risk: Export, import, and recovery flows can involve sensitive passphrases or recovery phrases. <br>
Mitigation: Protect exports and backups, prefer keychains or secret managers over environment variables for passphrases, and verify that any recovery phrase prompt is part of a local import/export flow. <br>


## Reference(s): <br>
- [MOCI ClawHub Skill Page](https://clawhub.ai/mociforge/moci) <br>
- [Memory Chain Security](references/memory-security.md) <br>
- [MOCI Reference Implementation](references/moci.ts) <br>
- [MOCI Threat Matrix](references/threat-matrix.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe persistent local identity files, memory-chain logs, key pins, gateway hooks, trust scores, and export/import flows under ~/.openclaw.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
