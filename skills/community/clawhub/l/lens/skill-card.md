## Description: <br>
Lens personalizes an OpenClaw agent by maintaining local Trinity Node profile files that capture a user's facts, values, and voice for future responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[capachow](https://clawhub.ai/user/capachow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Lens to give an OpenClaw agent persistent local personalization grounded in the user's history, values, and writing style. It supports onboarding, recurring interview prompts, and background distillation from local chat transcripts into .lens profile files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring background jobs process local OpenClaw conversation history into a persistent identity profile. <br>
Mitigation: Install only if this behavior is intentional, review the cron jobs before enabling them, and remove lens-distillation or lens-interview jobs to disable background processing. <br>
Risk: Sensitive personal data may be captured in .lens profile or TRACE files during personalization. <br>
Mitigation: Review generated .lens files, mark sensitive messages with #private, and set anonymize to true in .lens/SCOPE.json before distillation when stronger anonymization is needed. <br>
Risk: The skill requires local access to HOME, OPENCLAW_CRON_LIST, and OpenClaw session logs. <br>
Mitigation: Run it only in an environment where those files are expected, and review generated profile files before relying on personalized output. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/capachow/lens) <br>
- [Trinity Definitions](references/trinity-definitions.md) <br>
- [Resolve Protocol](references/resolve-protocol.md) <br>
- [Alignment Scales](references/alignment-scales.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with shell commands and JSON cron-job configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local .lens files and emit cron job definitions during onboarding.] <br>

## Skill Version(s): <br>
1.2.3 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
