## Description: <br>
Creative exploration during quiet hours that turns idle heartbeat time into freeform thinking and writes reflections to local files for later human review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can add this skill to a heartbeat routine so the agent occasionally captures thoughtful, freeform reflections during quiet hours. It is intended for later human review, not automated decision-making. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write local state and dream notes under WORKSPACE, which may be the wrong project if the environment is misconfigured. <br>
Mitigation: Confirm WORKSPACE before enabling the heartbeat routine and review created files under data/ and memory/dreams/. <br>
Risk: Idle journaling can capture reflections around sensitive or unrelated work. <br>
Mitigation: Enable the heartbeat routine only in appropriate contexts, avoid use around sensitive work, and keep maxDreamsPerNight low. <br>
Risk: Dream entries are speculative notes and may be incomplete, misleading, or not useful. <br>
Mitigation: Treat generated entries as drafts for human review rather than operational guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marjoriebroad/mar-dreaming) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Shell command output plus Markdown files written by the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local JSON state and optional topic configuration; requires jq and python3.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence; artifact frontmatter lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
