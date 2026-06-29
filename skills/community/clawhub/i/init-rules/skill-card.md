## Description: <br>
Interactively generate personalized agent rules by asking about tech stack, work style, and preferences, then writing customized rule files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarezoe](https://clawhub.ai/user/clarezoe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to set up reusable, personalized agent rules for Skill Genie through a short interview and generated Markdown rule files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can replace persistent agent rule files. <br>
Mitigation: Review the generated rule changes and keep or inspect the backup before accepting replacement rules. <br>
Risk: The skill instructs the agent to run an unscoped setup.sh script. <br>
Mitigation: Inspect the exact setup.sh in the active Skill Genie directory before running it, or manually copy the generated Markdown into rules/. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/clarezoe/init-rules) <br>
- [Skill Genie](https://github.com/Fei2-Labs/skill-genie) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown rule files and concise setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates multiple Skill Genie rules files and may run setup.sh to apply them.] <br>

## Skill Version(s): <br>
1.0.2 (source: server metadata and skill frontmatter metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
