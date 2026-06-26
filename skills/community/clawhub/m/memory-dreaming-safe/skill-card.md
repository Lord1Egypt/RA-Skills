## Description: <br>
Autonomous memory consolidation for OpenClaw agents that gathers signal from daily logs, session transcripts, learnings, and plan files, then supports curated MEMORY.md updates and optional Obsidian or Markdown knowledge-base sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deathrowsushy](https://clawhub.ai/user/deathrowsushy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to review accumulated agent memory, identify durable patterns or contradictions, consolidate useful learnings into MEMORY.md, and optionally sync structured notes to an Obsidian vault or Markdown knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A scheduled agent may read private agent history, including session transcripts and memory logs. <br>
Mitigation: Disable transcript scanning or limit configured source paths before enabling the cron workflow. <br>
Risk: Automatic runs may modify persistent memory or vault files without the confirmation promised in the main documentation. <br>
Mitigation: Require an explicit preview and approval step before any persistent write, and run the first cycles manually until the behavior is reviewed. <br>
Risk: Broad plan scanning and Obsidian sync can expand the amount of workspace and vault content the skill reads or writes. <br>
Mitigation: Keep Obsidian sync disabled until reviewed, and constrain plan search paths to the intended workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deathrowsushy/memory-dreaming-safe) <br>
- [README.md](artifact/README.md) <br>
- [Architecture - Memory Dreaming](artifact/references/architecture.md) <br>
- [Dream Prompt](artifact/references/dream-prompt.md) <br>
- [Obsidian Sync - How It Works](artifact/references/obsidian-sync.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, proposed file changes, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce memory summaries, proposed diffs, cron setup instructions, and optional Markdown notes for long-term memory or vault sync.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
