## Description: <br>
Loudy.ai Auto Task helps an agent query Loudy.ai earning pools, submit user-approved task links, and track review and payment status through the Loudy.ai API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sfsf332](https://clawhub.ai/user/sfsf332) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to manage Loudy.ai task workflows: find active earning pools, manually complete the required social post, submit the resulting task link, and check audit or payment status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Loudy.ai API key and can submit task links to a user account. <br>
Mitigation: Keep LOUDY_API_KEY in the environment, avoid writing it into shared files, and approve each task link before submission. <br>
Risk: The installer can clone remote code and delete an existing install directory. <br>
Mitigation: Prefer the reviewed package; if using install.sh, inspect or pin the source and back up any existing installation first. <br>
Risk: The workflow points users toward a separate Binance/Twitter posting skill for some tasks. <br>
Mitigation: Treat that skill as a separate installation that requires its own review and explicit consent before use. <br>
Risk: Optional cron checks write task status and notification files into the configured workspace. <br>
Mitigation: Enable cron only when needed, set OPENCLAW_WORKSPACE deliberately, and review generated files such as loudy_tasks.json and loudy_has_new.txt. <br>


## Reference(s): <br>
- [Loudy.ai API Reference](references/api.md) <br>
- [ClawHub release page](https://clawhub.ai/sfsf332/loudy-ai-auto-task) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown and terminal text with JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LOUDY_API_KEY; may read and write Loudy task status files in the configured OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
