## Description: <br>
Use npm for package install, version inspection, dist-tags, and safe publish flows for OpenClaw or ClawHub package releases, published-version validation, and npm auth/OTP publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jvy](https://clawhub.ai/user/jvy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to run npm package checks, inspect versions and dist-tags, and follow release-safe publish/auth flows for OpenClaw and ClawHub package work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: npm publish and dist-tag commands can change public package state or release the wrong package version. <br>
Mitigation: Confirm the npm account, package name, package directory, local version, target version, and release tag before running publish or dist-tag commands. <br>
Risk: OTP and npm auth workflows can expose sensitive credentials if copied into logs or chat history. <br>
Mitigation: Use OTPs only for the immediate publish step, avoid logging them, and keep read-only verification commands isolated with a temporary userconfig when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jvy/npm) <br>
- [Publisher profile](https://clawhub.ai/user/jvy) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces npm release workflow guidance and command examples for package inspection, publishing, dist-tag management, auth checks, and OTP handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
