## Description: <br>
Publish an NPM package to the registry, handling authentication via browser-based login with 2FA/security key support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarezoe](https://clawhub.ai/user/clarezoe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to publish npm packages, complete npm authentication with 2FA or WebAuthn when needed, run pre-publish checks, and verify the published version. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent through npm credential handling and token persistence. <br>
Mitigation: Prefer manual npm login or a tightly scoped token, inspect any script before running it, and remove temporary tokens from npm and ~/.npmrc after publishing. <br>
Risk: Publishing can expose an unintended package version or fail because of registry permissions, existing versions, or scope access. <br>
Mitigation: Run build and test checks first, confirm the package name, version, and access settings, then verify the published version with npm view. <br>


## Reference(s): <br>
- [ClawHub Npm Publish page](https://clawhub.ai/clarezoe/npm-publish) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes npm authentication, publish, troubleshooting, and verification steps.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence and frontmatter metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
