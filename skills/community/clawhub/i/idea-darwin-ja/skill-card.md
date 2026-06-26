## Description: <br>
Idea Darwin エンジン（日本語版）は、生のアイデアを進化論ベースで自動反復し、深化・交配・変異のラウンドを実行して高ポテンシャルなアイデアを浮上させます。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[warmskull](https://clawhub.ai/user/warmskull) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a local, round-based brainstorming workflow that turns raw ideas into structured idea cards, scores them, evolves them, and summarizes ranking or review decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and updates local project notes, reports, configuration, and graph files during idea-evolution rounds. <br>
Mitigation: Run it in a dedicated folder or version-controlled workspace and review generated changes after each round. <br>
Risk: Brainstorming outputs and scores can be speculative or misleading if treated as final decisions. <br>
Mitigation: Use the generated rankings, critiques, and validation notes as review aids, and keep the user as the final decision maker. <br>
Risk: Important idea files may be overwritten or reorganized as the workflow maintains its local state. <br>
Mitigation: Keep backups of important idea files and review workspace changes before continuing additional rounds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/warmskull/idea-darwin-ja) <br>
- [Project homepage](https://github.com/warmskull/idea-darwin) <br>
- [Action reference](references/actions.md) <br>
- [Prompt templates](references/prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and structured local project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains idea cards, round reports, leaderboards, configuration, stimuli notes, and relation graphs in the user's workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
