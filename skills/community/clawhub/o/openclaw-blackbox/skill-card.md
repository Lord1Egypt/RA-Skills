## Description: <br>
OpenClaw Blackbox helps agents inspect failed, stalled, expensive, or unusual OpenClaw runs from local disk evidence, list sessions and failures, find the session behind a request, and generate terminal, Markdown, JSON, or HTML reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shan8851](https://clawhub.ai/user/shan8851) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to debug OpenClaw cron runs, session failures, context overflows, missing transcripts or trajectories, message delivery issues, and other local run-evidence problems without relying on hidden LLM calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the @shan8851/blackbox npm package and its publisher. <br>
Mitigation: Install only when the package and publisher are trusted in the deployment environment. <br>
Risk: Generated Markdown, JSON, or HTML reports may include private prompts, tool outputs, URLs, and local paths. <br>
Mitigation: Review and redact reports before sharing them outside the trusted debugging context. <br>
Risk: Request search can match multiple sessions or the wrong run when local evidence is ambiguous. <br>
Mitigation: Use explicit session IDs or scoped OPENCLAW_HOME paths when possible. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/shan8851/openclaw-blackbox) <br>
- [Publisher profile](https://clawhub.ai/user/shan8851) <br>
- [Project homepage](https://github.com/shan8851/openclaw-blackbox) <br>
- [npm package @shan8851/blackbox](https://www.npmjs.com/package/@shan8851/blackbox) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, HTML, shell commands, guidance] <br>
**Output Format:** [Terminal text, Markdown reports, JSON reports, HTML reports, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are generated from local OpenClaw state and may include prompts, tool outputs, URLs, and local paths.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
