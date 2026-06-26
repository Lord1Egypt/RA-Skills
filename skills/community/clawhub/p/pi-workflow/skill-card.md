## Description: <br>
Workflow orchestration for Pi's task management, self-improvement, and code quality standards. Use when starting new projects, managing multi-step tasks (3+ steps or architectural decisions), capturing lessons from mistakes, writing verifiable code, or establishing quality gates before completion. Includes planning templates, progress tracking, bug fixing autonomy, and a lessons capture system to prevent repeated mistakes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kai-tw](https://clawhub.ai/user/kai-tw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to structure multi-step work, maintain task and lesson notes, apply verification gates, and keep self-improvement workflows consistent across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can lead agents or users to create persistent local task, lesson, error, feature-request, or memory notes that may include sensitive project details. <br>
Mitigation: Review generated note files periodically and avoid recording secrets, credentials, or sensitive project information. <br>
Risk: The optional OpenClaw hook injects a session-start reminder into agent context. <br>
Mitigation: Enable the hook only when persistent workflow reminders are desired, and disable or edit it if the added bootstrap context is not appropriate for a workspace. <br>


## Reference(s): <br>
- [Workflow Orchestration](references/workflow_orchestration.md) <br>
- [Lessons in Markdown](references/lessons.md) <br>
- [Phase 1 + 2: Enhanced Lesson Capture](references/phase1-phase2-enhanced-lessons.md) <br>
- [Lessons Update Guide](references/lessons_update_guide.md) <br>
- [Pi Workflow Self-Improvement Hook](hooks/openclaw/HOOK.md) <br>
- [Srishti Codes workflow reference](https://x.com/srishticodes/status/2025254119636959701) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and file path conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation or update of local task, lesson, error, feature-request, and memory files.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
