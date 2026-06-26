## Description: <br>
Generates local Vue 3 and Arco Design prototype workspaces using the Pangea 3 Linear theme, mock data, and reusable page/layout templates for rapid requirements alignment and demos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ysredcity](https://clawhub.ai/user/ysredcity) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and product teams use this skill to quickly create local frontend prototypes for lists, forms, dashboards, and management interfaces. It is intended for requirement review and demonstration with mock data rather than backend implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or update files in a local prototype workspace. <br>
Mitigation: Use a throwaway or clearly chosen target directory before running workspace initialization. <br>
Risk: The template workflow can install npm dependencies and start a local Vite development server. <br>
Mitigation: Review dependencies with normal supply-chain caution before installation and run the dev server only in an appropriate local environment. <br>


## Reference(s): <br>
- [Layout Template](references/layout-template.md) <br>
- [Pangea Design System Token](references/design-tokens.md) <br>
- [UX Base Specification](references/ux-spec.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Vue, TypeScript, Markdown guidance, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates a local prototype folder, uses mock data, and can start a local Vite development server.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
