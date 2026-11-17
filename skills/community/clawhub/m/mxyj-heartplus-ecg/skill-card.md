## Description:

This skill helps Heart+ App users send ECG measurement notifications, connect authorized Apple Watch ECG data, generate ECG report explanations, and retrieve historical, latest, or specified ECG reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mxyjhelowin](https://clawhub.ai/user/mxyjhelowin)

### License/Terms of Use:

MIT-0

## Use Case:

External Heart+ App users with a supported Apple Watch use this skill to initiate ECG measurement, complete authorization, and view ECG analysis reports through an agent. Agents use it to run the documented phone, authorization, measurement, and report-query commands while preserving medical disclaimers and high-risk escalation language.

### Deployment Geography for Use:

China mainland

## Known Risks and Mitigations:

Risk: The skill downloads and runs a native Heart+ security helper locally.

Mitigation: Install only from the trusted publisher, keep the configured SHA-256 checks enabled, and review before use on managed or shared systems.

Risk: The workflow handles phone-number-linked requests and health report data.

Mitigation: Use only in trusted agent workspaces, avoid shared machines, and clear local session and report caches when the workflow is complete.

Risk: ECG report output may be mistaken for medical diagnosis.

Mitigation: Present ECG results as informational, retain the Apple Watch ECG limitation disclaimer, and direct high-risk symptoms to medical or emergency services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mxyjhelowin/skills/mxyj-heartplus-ecg)
- [Publisher profile](https://clawhub.ai/user/mxyjhelowin)
- [Heart+ App Store listing](https://apps.apple.com/cn/app/%E5%BF%83%E8%84%8F-%E5%BF%83%E7%8E%87-%E5%BF%83%E8%B7%B3-%E5%BF%83%E8%84%8F%E5%81%A5%E5%BA%B7%E6%A3%80%E6%B5%8B/id1584620848)
- [Apple Watch ECG measurement guide](https://support.apple.com/zh-cn/120277)
- [uv Linux installer](https://astral.sh/uv/install.sh)
- [uv Windows installer](https://astral.sh/uv/install.ps1)
- [SessionKey获取说明](references/SessionKey获取说明.md)
- [交互话术库](references/交互话术库.md)
- [如何下载心脏+](references/如何下载心脏+.md)
- [如何使用iwatch测量心电](references/如何使用iwatch测量心电.md)
- [报告输出说明](references/报告输出说明.md)
- [脚本与流程说明](references/脚本与流程说明.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, short user-facing text, JSON tool results, and uv command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report content is expected to be passed through without summarization; local state is scoped by session key.]

## Skill Version(s):

0.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
