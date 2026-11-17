# Host adaptation / 平台适配

安装时读 [install.md](install.md)：包含通用对话安装和五个平台的手动操作。所选文档格式的依赖见 [setup.md](setup.md)。宿主提供联网、执行、图片与交付工具；Skill 负责学习流程、材料和课程状态。

## Approved-plan scheduling handoff

After approval, use the current host's native automation tools. Verify the saved job ID, local time, IANA timezone and next execution; record the ID with `schedule-record`. The job should name this skill and the absolute course directory. Do not assume earlier chat context is available.

For Codex, use the automation tool available in the current client. For WorkBuddy, use its native Automation feature. For OpenClaw and Doubao work mode, inspect the actual native scheduling interface. If no scheduler is available, offer manual continuation.

Use the [readiness](readiness.md) report to distinguish foreground observations from a real scheduled-context check. After approval and job verification, test the actual background execution host, binary/profile, course path, credentials and pinned account/location. Keep unavailable/untested capabilities explicit; a synthetic host report or interactive keychain success never establishes unattended operation. No live jobs for sample projects. Preserve pending artifacts and never republish merely to test credentials.

DSH's Host Schedule provides create/list/update/delete in supported presets. Use a daily local-time rule with an explicit zone rather than a fixed 86400-second interval. The Host must run for execution. Native pause is unavailable in the documented upstream: pause course state immediately; do not report a host pause that did not occur. Deletion also removes host delivery history, so preserve relevant records and explain the impact before an authorized deletion.

Sources: [DSH Schedule](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/guide/schedule.md), [WorkBuddy Automation](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Automation-Guide), [OpenClaw cron](https://docs.openclaw.ai/cron).

## Native task instruction

“Use omni-learning-anything at INSTALLED_SKILL_PATH to continue COURSE_ABSOLUTE_PATH. Read config, approved plan, state and recent lessons; run next. Respect pause/completion/daily limit. Reuse pending artifacts. For a new lesson, research actual sources, author within the time budget, include an explanatory figure and >=5 expansion links, render and inspect the configured format; publish/read back the configured destination and its saved task/document. Run delivered only after a verified primary receipt and actual host delivery. Uncertain writes require reconciliation, never blind creation. Remain quiet on repeats. When complete, stop the recorded task and verify.”

Check the host receipt separately from the Skill's document and delivery state. A reminder receipt alone does not establish document delivery. Runtime handoff guidance is part of normal usage; the host scheduler itself is outside this Skill's test scope.

## Short-check boundary

Daily lesson jobs may prepare a frozen short check and include an invitation with the material, then finish normally. Never start an interactive check, wait for responses, create a quiz reminder/task or schedule another conversation. Checks run only on the learner's actual request; preserve existing lesson schedules separately. See [assessment](assessment.md).
