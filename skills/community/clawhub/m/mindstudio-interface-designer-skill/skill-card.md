## Description: <br>
Master frontend skill for MindStudio Interface Designer that guides UI/UX discovery, maps MindStudio workflow variables, and produces production-grade React interface code for forms, wizards, dashboards, data displays, and other user input experiences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sol1986](https://clawhub.ai/user/Sol1986) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
MindStudio builders, frontend developers, and workflow designers use this skill to plan, design, and implement React interfaces for MindStudio User Input blocks. It is intended for interactive forms, onboarding flows, dashboards, chat-style inputs, upload interfaces, and other workflow entry points that need polished UX and correct variable handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated chat or upload interfaces may submit unnecessary conversation history, files, secrets, or user data into downstream workflow variables. <br>
Mitigation: Confirm exactly which variables are submitted, minimize conversation history, and avoid sending secrets or unnecessary data before using an interface in production. <br>
Risk: Generated React interface code may behave incorrectly if deployed into a live MindStudio workflow without review. <br>
Mitigation: Review the generated component, variable mapping, bridge usage, validation, accessibility, and data handling before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Sol1986/mindstudio-interface-designer-skill) <br>
- [MindStudio Interface Designer documentation](https://university.mindstudio.ai/docs/building-ai-agents/interface-designer) <br>
- [README.md](artifact/README.md) <br>
- [EXAMPLES.md](artifact/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with React and TypeScript code examples, implementation plans, and configuration notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for MindStudio Interface Designer React components that submit confirmed workflow variables through the MindStudio bridge.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
