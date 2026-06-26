## Description: <br>
Idea Darwin evolves raw ideas into scored idea cards through structured rounds of deepening, derivation, crossbreeding, critique, validation, and ranking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[warmskull](https://clawhub.ai/user/warmskull) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, founders, product teams, and other external users use this skill to maintain an idea-evolution workspace from ideas.md, generate scored idea cards, run iteration rounds, and review rankings and next-step briefings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and updates local planning files such as cards, reports, configuration, and graph data. <br>
Mitigation: Run it in a dedicated project folder and review generated or modified files before relying on them. <br>
Risk: Broad brainstorming or idea-selection requests may trigger the workflow automatically. <br>
Mitigation: Invoke the skill explicitly when desired, or tell the agent not to use Idea Darwin for ad hoc brainstorming. <br>
Risk: Scoring, rankings, critiques, and validation outcomes are generated judgments and can be incomplete or misleading. <br>
Mitigation: Use the results as decision support and apply human review before dormancy, removal, prioritization, or execution decisions. <br>


## Reference(s): <br>
- [Idea Darwin GitHub homepage](https://github.com/warmskull/idea-darwin) <br>
- [Standard Actions Reference](references/actions.md) <br>
- [Prompt Templates](references/prompts.md) <br>
- [Idea Card Template](assets/card-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, YAML configuration, JSON relationship data, and conversational status or round briefings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local planning files including idea cards, round reports, leaderboard, stimuli entries, and relationship graph data.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
