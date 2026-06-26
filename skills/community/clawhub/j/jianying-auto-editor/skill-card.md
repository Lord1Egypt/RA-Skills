## Description: <br>
Scans local media, requests cloud editing plans, and generates Jianying-oriented draft output packages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afengzi](https://clawhub.ai/user/afengzi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video automation operators use this skill to connect a local media folder with a configured cloud editing API, then write draft metadata, timeline content, and execution reports for Jianying-oriented workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send local media file metadata and an API key to the configured cloud editing service. <br>
Mitigation: Use a trusted HTTPS API endpoint, a scoped API key, and a material_path containing only files intended for the current edit. <br>
Risk: The bundled example uses an insecure raw HTTP IP endpoint. <br>
Mitigation: Replace the sample endpoint with a trusted HTTPS API base URL before running the skill. <br>
Risk: The output directory can be overwritten when export_mode is set to overwrite. <br>
Mitigation: Prefer task-subdir unless replacing existing draft files is intentional. <br>
Risk: Generated draft JSON may not import cleanly into every Jianying version. <br>
Mitigation: Validate the generated files against the target Jianying version before relying on them in production workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/afengzi/jianying-auto-editor) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/afengzi) <br>
- [OpenClaw Homepage Metadata](https://github.com/imfengziaaa/video-auto-editor-skills) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, JSON, files, guidance] <br>
**Output Format:** [JSON draft files plus a JSON command-line status payload] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces draft-meta.json, draft-content.json, and execution-report.json in the configured output directory.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata, manifest.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
