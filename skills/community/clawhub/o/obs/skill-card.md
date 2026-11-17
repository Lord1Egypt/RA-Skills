## Description:

Comprehensive Open Build Service (OBS) management with API support for projects, packages, repositories, builds, submit requests, files, users, and search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weidongkl](https://clawhub.ai/user/weidongkl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to manage Open Build Service projects, packages, files, builds, submit requests, and related search or user lookup workflows from an agent-assisted command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses OBS credentials for remote API calls that can alter projects and packages.

Mitigation: Use a least-privilege OBS token, store credentials outside committed files, rotate tokens regularly, and avoid persisting OBS_TOKEN in shell startup files when possible.

Risk: OBS operations can delete projects, delete packages, upload files, trigger rebuilds, or accept, reject, and revoke submit requests.

Mitigation: Test against a sandbox project first and review every target project, package, file, build, and request ID before executing state-changing commands.

Risk: The authoritative security review marks this release as suspicious because it handles credentials and remote destructive actions with unsafe shell implementation and limited warnings.

Mitigation: Review the generated shell commands before running them, avoid untrusted parameter values, and restrict execution to a controlled shell environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weidongkl/skills/obs)
- [OBS API Docs](https://api.opensuse.org/apidocs/index)
- [OBS Official Docs](https://openbuildservice.org/help/)
- [osc Command Reference](https://openbuildservice.org/help/manuals/obs-user-guide/cha.obs.osc.html)
- [openSUSE Packaging Guide](https://en.opensuse.org/openSUSE:Packaging_guidelines)
- [OBS API library](references/obs-lib.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that call remote OBS APIs and modify projects, packages, files, builds, or submit requests.]

## Skill Version(s):

1.0.1 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
