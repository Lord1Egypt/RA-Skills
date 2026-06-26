## Description: <br>
MAL-Updater helps agents install, audit, operate, and troubleshoot conservative multi-provider anime-to-MyAnimeList sync and recommendations with guarded auth, review-queue triage, health checks, and optional user-systemd daemon support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kklouzal](https://clawhub.ai/user/kklouzal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to bootstrap and run a local MAL-Updater installation that syncs approved provider watch data from Crunchyroll or HIDIVE into MyAnimeList. Developers and maintainers use it to inspect runtime state, triage mapping review queues, run dry-run or guarded sync flows, and review health and daemon behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores MAL and provider auth material and local runtime state. <br>
Mitigation: Keep `.MAL-Updater/secrets` and `.MAL-Updater/state` private, use restrictive local permissions, and avoid sharing status, service, log, or OAuth verifier output. <br>
Risk: Guarded sync flows can write approved updates to MyAnimeList. <br>
Mitigation: Run dry-run and review-queue workflows before live apply commands, and keep unattended sync limited to exact approved mappings. <br>
Risk: The optional user-level daemon can perform background provider reads and MAL update lanes. <br>
Mitigation: Review the generated systemd service behavior before enabling unattended operation and verify health with service-status, service-run-once, and health-check. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kklouzal/mal-updater) <br>
- [Project homepage](https://github.com/kklouzal/mal-updater) <br>
- [Bootstrap flow](references/bootstrap-onboarding.md) <br>
- [Command cookbook](references/cli-recipes.md) <br>
- [Operations](references/OPERATIONS.md) <br>
- [Automation](references/AUTOMATION.md) <br>
- [MAL OAuth details](references/MAL_OAUTH.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local CLI commands, runtime paths, review queues, health status, and daemon/service state.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release evidence; pyproject.toml reports 0.1.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
