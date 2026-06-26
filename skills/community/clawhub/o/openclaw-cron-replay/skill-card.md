## Description: <br>
Replay OpenClaw cron job formatting and delivery decisions locally using a trusted local openclaw-cron-replay installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pfrederiksen](https://clawhub.ai/user/pfrederiksen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to replay saved OpenClaw cron job inputs locally, understand why a run produced or suppressed a message, compare prompt or result changes, and inspect likely final delivery text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The replay workflow depends on a local openclaw-cron-replay binary or source checkout selected by the user. <br>
Mitigation: Use only a trusted local installation, inspected local source checkout, or pinned internal install workflow before running replay commands. <br>
Risk: Cron config, prompt, payload, result, and metadata files may contain secrets or sensitive local data. <br>
Mitigation: Review files for secrets before use and keep replay outputs local unless they have been sanitized. <br>
Risk: Running replay commands with elevated privileges can expand the impact of a bad local install or unsafe input path. <br>
Mitigation: Avoid root or elevated execution unless it is required for access to the cron artifacts being inspected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pfrederiksen/openclaw-cron-replay) <br>
- [OpenClaw Cron Replay repository](https://github.com/pfrederiksen/openclaw-cron-replay) <br>
- [GitHub Publish Notes](references/github-publish-notes.md) <br>
- [Publish Checklist](references/publish-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and concise interpretation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to request JSON or Markdown output from a trusted local openclaw-cron-replay tool.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
