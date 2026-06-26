## Description: <br>
Operate an Obsidian knowledge base as a persistent LLM wiki using a raw-to-source-to-wiki pattern. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ducheneadas-source](https://clawhub.ai/user/ducheneadas-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and knowledge workers use this skill to maintain an Obsidian vault as a living knowledge base by ingesting raw notes, maintaining source summaries, compiling formal wiki pages, preserving reusable outputs, and running recurring maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vault maintenance can move, rewrite, or reorganize notes in ways that may be hard to reverse. <br>
Mitigation: Use a backed-up or version-controlled vault and require a preview before bulk moves, rewrites, heartbeat maintenance, or write-back work. <br>
Risk: Sensitive query outputs or private source material could be saved into reusable wiki pages. <br>
Mitigation: Restrict the agent to the intended vault directory and review proposed saved outputs before they are written. <br>


## Reference(s): <br>
- [Adaptation Checklist](references/adaptation-checklist.md) <br>
- [Heartbeat](references/heartbeat.md) <br>
- [Object Model](references/object-model.md) <br>
- [Workflow](references/workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown notes, Obsidian wiki pages, maintenance findings, source summaries, structured answers, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update or reorganize vault files when the user authorizes maintenance work.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
