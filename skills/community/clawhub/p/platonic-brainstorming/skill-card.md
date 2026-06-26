## Description: <br>
Platonic Brainstorming provides optional design exploration for Platonic Coding Phases 1 and 2 by exploring user intent, requirements, alternatives, and design before RFC formalization or implementation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caesar0301](https://clawhub.ai/user/caesar0301) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and product builders use this skill to turn an idea into an approved design draft before RFC formalization or implementation planning, including clarifying questions, alternative approaches, trade-off review, and optional visual exploration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional visual companion may run a local browser server that could expose brainstorming screens if bound to a public interface. <br>
Mitigation: Keep the visual server on localhost when possible and avoid binding it to public interfaces. <br>
Risk: The skill can write design drafts and visual session files that may accidentally include sensitive project details. <br>
Mitigation: Review generated files before sharing, add .superpowers/ to .gitignore for persistent visual sessions, and avoid placing secrets or sensitive private data in mockups. <br>
Risk: Brainstorming output can influence later implementation planning with incorrect assumptions or misleading guidance. <br>
Mitigation: Require explicit user approval of the design draft before advancing to downstream Platonic Coding stages. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/caesar0301/platonic-brainstorming) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Conversational guidance and Markdown design drafts, with optional shell commands and HTML visual companion screens.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write design drafts under docs/drafts/ and optional visual session files under .superpowers/brainstorm/.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
