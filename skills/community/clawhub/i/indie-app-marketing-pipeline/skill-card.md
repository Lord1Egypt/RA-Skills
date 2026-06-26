## Description: <br>
Template-driven multi-platform content pipeline for indie iOS developers that generates and schedules a full week of social posts for TikTok, YouTube Shorts, X/Twitter, and Facebook from a reusable content bank. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zakmcintyre](https://clawhub.ai/user/zakmcintyre) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and indie iOS app builders use this skill to create a reusable social content bank, generate weekly posting plans, and schedule daily posts through Postiz with optional video-generation integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The daily publisher can queue live posts on connected social accounts through Postiz. <br>
Mitigation: Use the weekly planner and daily publisher dry-run modes first, review generated plans and content, and only run live publishing after confirming platform integration IDs and scheduled times. <br>
Risk: The setup flow can write a local .env file containing a Postiz API key. <br>
Mitigation: Protect the generated .env file, avoid committing it, and prefer environment-specific secret management when available. <br>
Risk: The optional video-generation script path can execute a configured local command. <br>
Mitigation: Do not enable config.videoGen.script until the command construction is fixed or the script path and inputs are tightly controlled. <br>


## Reference(s): <br>
- [Content Bank Guide](references/content-bank-guide.md) <br>
- [Platform Strategy](references/platform-strategy.md) <br>
- [Postiz docs](https://docs.postiz.com) <br>
- [ClawHub skill page](https://clawhub.ai/zakmcintyre/indie-app-marketing-pipeline) <br>
- [Publisher profile](https://clawhub.ai/user/zakmcintyre) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands plus generated JSON configuration and weekly plan files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a Postiz API key; supports dry-run preview modes before live scheduling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
