## Description: <br>
Generates a Mermaid architecture diagram showing high-level component relationships. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect a codebase scope, summarize high-level module relationships, and produce a Mermaid flowchart for onboarding, documentation, or pull request review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects codebase structure to build architecture diagrams, which can expose sensitive project relationships if used over a broad or private scope. <br>
Mitigation: Use a specific, intentional scope and avoid running it over sensitive repositories unless the generated diagram is appropriate to share. <br>
Risk: The generated Mermaid diagram may be passed to an external renderer. <br>
Mitigation: Review the Mermaid text before rendering and remove sensitive component names or relationships when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-cartograph-architecture-diagram) <br>
- [Cartograph homepage](https://github.com/athola/claude-night-market/tree/master/plugins/cartograph) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with Mermaid code and a brief summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call a Mermaid renderer to validate and render the generated flowchart.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
