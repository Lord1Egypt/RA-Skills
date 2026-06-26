## Description: <br>
Extract daily conversation summaries from Hermes Agent session logs and persist them as readable memory files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realpda](https://clawhub.ai/user/realpda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Hermes Agent users use this skill to backfill, compare, and maintain daily Markdown memory summaries from Hermes session JSON and JSONL logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory files may contain sensitive session history, including secrets, regulated data, or proprietary material. <br>
Mitigation: Run the skill only on intended Hermes sessions and protect the output directory with appropriate local access controls. <br>
Risk: The daily cron job can continue collecting and writing conversation summaries automatically. <br>
Mitigation: Enable scheduled runs only when ongoing collection is intended, and periodically review generated memory files for retention and sensitivity. <br>


## Reference(s): <br>
- [Hermes Memory Sync ClawHub release](https://clawhub.ai/realpda/hermes-memory-sync) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown memory files and command-line setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes daily summaries to workspace/memory/YYYY-MM-DD.md; can compare coverage, backfill dates, and report stats.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
