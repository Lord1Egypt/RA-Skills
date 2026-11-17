## Description:

Goal Achiever guides an agent through configurable content-publishing goals by reading task and prompt files, decomposing work into JSON tasks, executing or developing supporting scripts, recording results, scoring outcomes, and generating retrospective inputs for later batches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ldz2010326](https://clawhub.ai/user/ldz2010326)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run iterative publishing workflows for a selected target platform, including task planning, script-backed execution, logging, scoring, and retrospective planning. It is intended for automated content workflow orchestration and should be used only where account, platform, and posting controls are approved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated publishing could post or modify content through logged-in platform sessions without enough human control.

Mitigation: Require per-post approval, approved account and platform allowlists, and clear posting scopes before enabling publishing actions.

Risk: Generated or registry-selected scripts could perform unsafe actions during execution.

Mitigation: Run scripts in a sandbox, review script diffs before execution, and block access to credentials or accounts that are not required for the approved task.

Risk: Scheduled background jobs could continue running after the original task context has changed.

Mitigation: Do not allow LaunchAgent or cron registration unless explicitly requested, reviewed, and paired with an owner, schedule, and removal path.

Risk: Prompt and registry self-updates could change future agent behavior in ways the user has not reviewed.

Mitigation: Require human review and versioned change tracking before prompt, registry, or workflow updates become active.

Risk: External publishing guidance references internal APIs and anti-automation-sensitive flows that may violate platform expectations.

Mitigation: Use only approved platform interfaces and prohibit internal-API use, anti-automation bypass, or session manipulation unless explicitly authorized by the platform and account owner.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ldz2010326/skills/goal-achiever)
- [Prompt Registry](references/prompts/prompt_registry.md)
- [Goal Prompt](references/prompts/goal_prompt.md)
- [Retro Prompt](references/prompts/retro_prompt.md)
- [Prompt Authoring Guide](references/prompts/prompt_authoring_guide.md)
- [Technical Decision Reference](references/technical-decision-reference.md)
- [External Publishing Design Reference](references/external-publishing-design-reference.md)
- [Cron Design Reference](references/cron-design-reference.md)
- [Logging Guide](references/logging.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON task files, prompt text, configuration snippets, and script or shell-command proposals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update workflow files, prompts, run logs, script registry entries, and generated scripts during agent execution.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
