## Description: <br>
Creates an OpenClash GitHub Actions build workflow and pushes it directly to a user's GitHub repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[veelove](https://clawhub.ai/user/veelove) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and router maintainers use this skill to add an OpenClash build workflow to a forked iStoreOS repository, trigger GitHub Actions builds, and retrieve the generated router installer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for GitHub repository credentials and changes repository Actions permissions. <br>
Mitigation: Use a fine-grained, short-lived token limited to the target repository, revoke it after use, and avoid enabling pull request review approval unless it is explicitly needed. <br>
Risk: The generated installer can make privileged router changes, including installing packages, writing system files, enabling OpenClash, and reloading firewall or web services. <br>
Mitigation: Inspect the workflow and generated installer before running it on a router, and test in a non-critical environment before using it on production devices. <br>


## Reference(s): <br>
- [OpenClash build workflow](references/build-openclash.yml) <br>
- [OpenClash latest release API](https://api.github.com/repos/vernesong/OpenClash/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [Configuration, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with YAML workflow content and shell/API commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a GitHub repository URL and personal access token; may create a workflow file and change Actions workflow permissions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
