## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement. Use when: (1) A command or operation fails unexpectedly, (2) User corrects Claude ('No, that's wrong...', 'Actually...'), (3) User requests a capability that doesn't exist, (4) An external API or tool fails, (5) Claude realizes its knowledge is outdated or incorrect, (6) A better approach is discovered for a recurring task. Also review learnings before major tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LuckyJin](https://clawhub.ai/user/LuckyJin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to log command failures, user corrections, missing capabilities, knowledge gaps, and recurring best practices into structured learning files for later review and promotion into project memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning logs and promoted memory files may retain private context, secrets, or incorrect guidance across sessions. <br>
Mitigation: Review and redact entries before saving or promotion; require explicit approval before adding content to prompt, memory, or shared session files. <br>
Risk: Always-on hooks and empty hook matchers can broaden where reminders or error capture run. <br>
Mitigation: Keep hooks project-local, use scoped matchers where possible, and enable only the hook events needed for the workspace. <br>
Risk: Cross-session transcript sharing can expose context beyond the original session. <br>
Mitigation: Share only reviewed, minimal summaries across sessions and avoid sending raw transcripts or sensitive project details. <br>


## Reference(s): <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>
- [ClawHub release page](https://clawhub.ai/LuckyJin/my-test-2) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional generated markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append structured entries to .learnings files and suggest promotion into agent prompt or memory files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
