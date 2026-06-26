## Description: <br>
Comprehensive Open Build Service (OBS) management with API support for projects, packages, repositories, builds, submit requests, files, users, and search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weidongkl](https://clawhub.ai/user/weidongkl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to manage Open Build Service packaging workflows, including projects, packages, repositories, builds, submit requests, file operations, users, and search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles powerful OBS credentials and may expose tokens through shell startup files, configuration files, logs, or support transcripts. <br>
Mitigation: Use a dedicated least-privilege OBS token, keep oscrc permissions restricted, avoid shell startup files for secrets, rotate tokens regularly, and do not paste full oscrc or OBS_* output into chats or logs. <br>
Risk: The skill can guide destructive or high-impact OBS actions such as delete, upload, rebuild, permission changes, and submit request accept, reject, or revoke. <br>
Mitigation: Manually review and approve each high-impact OBS command, prefer a test or non-production OBS namespace first, and verify target project, package, repository, architecture, and request IDs before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/weidongkl/obs) <br>
- [OBS API Docs](https://api.opensuse.org/apidocs/index) <br>
- [OBS Official Docs](https://openbuildservice.org/help/) <br>
- [osc Command Reference](https://openbuildservice.org/help/manuals/obs-user-guide/cha.obs.osc.html) <br>
- [openSUSE Packaging Guide](https://en.opensuse.org/openSUSE:Packaging_guidelines) <br>
- [OBS API helper library](references/obs-lib.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline bash, INI, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide credential setup and OBS API operations that affect projects, packages, builds, files, permissions, and submit requests.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
