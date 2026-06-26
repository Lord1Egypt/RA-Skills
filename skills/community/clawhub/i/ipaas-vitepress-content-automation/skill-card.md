## Description: <br>
Generates B2B integration solution Markdown and deploys the resulting VitePress site over SSH. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evan-ch](https://clawhub.ai/user/evan-ch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content automation teams use this skill to draft system integration case studies, update VitePress documentation, and publish the generated site to a configured SSH target. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify local documentation and VitePress navigation from a broad content request. <br>
Mitigation: Require manual review and explicit approval before file write steps are applied. <br>
Risk: The skill can publish the generated site over SSH to the configured server and remote directory. <br>
Mitigation: Use a restricted non-root deployment account, verify SERVER_IP and REMOTE_DIR before deployment, and require explicit approval before running deployment. <br>
Risk: The artifact references a deployment script path that may not match the packaged script location. <br>
Mitigation: Fix the deploy script path mismatch before relying on automated deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evan-ch/ipaas-vitepress-content-automation) <br>
- [Taobao Open Platform API documentation](https://open.taobao.com/doc.htm) <br>
- [Kingdee Cloud API documentation](https://open.jdy.com/#/files/api/detail?index=3&categrayId=3cc8ee9a663e11eda5c84b5d383a2b93) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown content, VitePress configuration updates, and shell deployment commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pnpm, rsync, ssh, SSH key authentication, and SERVER_IP/REMOTE_DIR deployment environment variables.] <br>

## Skill Version(s): <br>
1.0.9 (source: ClawHub release metadata; artifact frontmatter declares 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
