## Description: <br>
Complete Oblien workspace environment covering the Firecracker microVM runtime, authentication with gateway JWTs or raw tokens, and the Internal API for files, search, command execution, terminal sessions, and file watching on port 9990. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hydralerne](https://clawhub.ai/user/Hydralerne) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill as a reference for connecting to and operating an Oblien workspace runtime, including authentication, file access, code search, command execution, terminal sessions, and file watching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documents high-privilege runtime operations including filesystem changes, command execution, terminal access, file watching, and token-based access. <br>
Mitigation: Install it only when the agent should understand and operate an Oblien workspace runtime, and review file deletion, command execution, and long-running task operations before allowing impactful changes. <br>
Risk: Authentication examples involve gateway JWTs, raw connection tokens, client IDs, client secrets, and bearer tokens that could expose workspace access if copied into prompts, logs, terminal history, or shared output. <br>
Mitigation: Keep real secrets and bearer tokens out of prompts, logs, terminal history, and shared outputs; rotate short-lived gateway JWTs and handle raw tokens only for intended direct workspace-to-workspace access. <br>
Risk: Gateway access requires public gateway exposure and direct access requires private workspace links, so network configuration can affect both reachability and exposure. <br>
Mitigation: Enable public gateway access only when needed, prefer private links and scoped paths where practical, and verify network settings before using runtime operations. <br>


## Reference(s): <br>
- [Oblien documentation](https://oblien.com/docs) <br>
- [ClawHub skill page](https://clawhub.ai/Hydralerne/oblien-runtime) <br>
- [ripgrep project](https://github.com/BurntSushi/ripgrep) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown reference material with TypeScript, HTTP, JSON, cURL, SSE, and WebSocket examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable automation is bundled; the skill provides runtime API guidance and examples for agent use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
