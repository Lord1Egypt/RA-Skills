## Description: <br>
Deep research workflow for /deepresearch with sources, claims, synthesis, and resumable state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jkobject](https://clawhub.ai/user/jkobject) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research-focused agents use this skill to run source-grounded investigations that need lanes, citations, durable notes, and resumable evidence tracking across turns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research ledgers saved under .deepresearch may contain sensitive source URLs, notes, claim summaries, or decision context. <br>
Mitigation: Review ledger contents before sharing a workspace and avoid recording secrets or sensitive research context. <br>
Risk: User-supplied slugs can affect where local ledger state is written. <br>
Mitigation: Use simple slug values without path separators. <br>
Risk: Research synthesis can mislead when claims remain weak, conflicting, or unverified. <br>
Mitigation: Run the brief command, preserve uncertainty, and cite important conclusions before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jkobject/omoc-deepresearch) <br>
- [Publisher profile](https://clawhub.ai/user/jkobject) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown synthesis with inline shell commands and local JSON ledger files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or resumes .deepresearch/<slug>/ state containing lanes, sources, claims, notes, and brief summaries.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
