## Description: <br>
Builds a reusable memory mesh for OpenClaw with tagged memory layers, local consolidation, global sync, GitHub Issue contribution self-check, and optional automated issue posting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanng-ide](https://clawhub.ai/user/wanng-ide) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw agent builders use this skill to consolidate cross-session memories, score and promote reusable lessons, sync shared memory feeds, and prepare reviewed memory contributions for collaborative reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled runs can continue operating after installation. <br>
Mitigation: Review the cron configuration before enabling it and keep scheduled execution disabled unless recurring memory sync is intended. <br>
Risk: The skill can update installed skills from subscribed sources. <br>
Mitigation: Enable auto-update only for trusted subscriptions and review generated sync reports before accepting changes. <br>
Risk: Memory-derived summaries may be posted externally through GitHub or browser identity. <br>
Mitigation: Keep automated posting disabled until the generated JSON and Markdown outputs are reviewed and the posting identity is approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wanng-ide/memory-mesh-core) <br>
- [GitHub issue contribution intake](https://github.com/wanng-ide/memory-mesh-core/issues/1) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands plus generated JSON and Markdown memory artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local memory reports, contribution payloads, cron configuration, and issue-posting reports in the workspace.] <br>

## Skill Version(s): <br>
1.0.6 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
