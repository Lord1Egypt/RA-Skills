## Description: <br>
Build and manage OpenClaw roles for public figures or fictional characters, then generate persona files, switch active roles, and create identity-consistent selfies, portraits, group shots, or other images through TuQu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouyi531](https://clawhub.ai/user/zhouyi531) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to create role workspaces and persona files for public or fictional characters, switch active roles, and generate role-consistent or freestyle images through the TuQu photo API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate TuQu payment top-up flows. <br>
Mitigation: Review every recharge action manually before opening QR codes or hosted checkout links. <br>
Risk: The API helper can send credentials to caller-chosen hosts when host overrides or full URL paths are used. <br>
Mitigation: Use supported relative API paths, avoid --base-url and full URL paths, and use a limited or disposable TuQu service key. <br>
Risk: The skill persists role workspaces and memory under ~/.openclaw. <br>
Mitigation: Periodically inspect or delete stored roles, workspaces, and memory under ~/.openclaw. <br>


## Reference(s): <br>
- [ClawHub OpenClaw Role Builder](https://clawhub.ai/zhouyi531/openclaw-role-builder) <br>
- [TuQu service key dashboard](https://billing.tuqu.ai/dream-weaver/dashboard) <br>
- [TuQu API Notes](artifact/tuqu-photo-api/TUQU_API.md) <br>
- [TuQu endpoint reference](artifact/tuqu-photo-api/references/endpoints.md) <br>
- [TuQu workflows reference](artifact/tuqu-photo-api/references/workflows.md) <br>
- [OpenClaw well-known character instructions](artifact/openclaw-character-creator/references/wellknown_system_instruction.md) <br>
- [OpenClaw fictional character instructions](artifact/openclaw-character-creator/references/nonwellknown_system_instruction.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown persona files, JSON API responses, shell commands, and configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes role state under ~/.openclaw, reads bundled reference files, and prints TuQu API responses to stdout.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
