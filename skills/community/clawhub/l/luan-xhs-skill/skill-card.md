## Description: <br>
End-to-end Xiaohongshu operations including positioning, topic research, content production, publish execution, and post-incident recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zarflan](https://clawhub.ai/user/zarflan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and operators use this skill to plan Xiaohongshu account positioning, generate post ideas and copy, prepare or publish Xiaohongshu notes, manage comments, and recover from common publishing failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a reusable Xiaohongshu creator-session file and perform live posting actions. <br>
Mitigation: Prefer dry-run or draft flows, and confirm the target account, media path, visibility, and post content before allowing publication. <br>
Risk: Stored Xiaohongshu session data and displayed OpenClaw gateway tokens are sensitive. <br>
Mitigation: Treat ~/.openclaw/workspace/xhs_user_info.json and gateway tokens as secrets, and avoid using the skill from shared workspaces. <br>
Risk: The included OpenClaw gateway setup material can expose a token during setup or troubleshooting. <br>
Mitigation: Only install when that setup is needed, restrict access to the local workspace, and avoid sharing logs or screenshots that include tokens. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zarflan/luan-xhs-skill) <br>
- [XHS Publish Flows](references/xhs-publish-flows.md) <br>
- [XHS Runtime Rules](references/xhs-runtime-rules.md) <br>
- [XHS Comment Ops](references/xhs-comment-ops.md) <br>
- [XHS Evaluation Patterns](references/xhs-eval-patterns.md) <br>
- [Xiaohongshu Creator Platform](https://creator.xiaohongshu.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline commands and script-driven workflow instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use saved Xiaohongshu creator sessions and browser automation scripts when the user authorizes publish or login flows.] <br>

## Skill Version(s): <br>
0.2.5 (source: server release evidence and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
