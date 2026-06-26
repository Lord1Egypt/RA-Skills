## Description: <br>
Guides AI agents to build NocoBase pages, including menus, tables, forms, popups, KPIs, JS blocks, outlines, and event flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Alexander-lq](https://clawhub.ai/user/Alexander-lq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and NocoBase operators use this skill to guide an agent through creating or modifying pages with FlowModel tools, including CRUD pages, menu structure, forms, tables, filters, popups, KPIs, and page debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently modify or delete NocoBase pages, routes, fields, columns, JavaScript, and event-flow code. <br>
Mitigation: Require the agent to inspect the target page, identify the exact route, page, tab, collection, and proposed change, and obtain confirmation before cleanup, deletion, field or column removal, or JavaScript and event-flow changes. <br>
Risk: Full-replace FlowModel updates can overwrite existing layout or configuration when changes are poorly scoped. <br>
Mitigation: Inspect the target page first and apply changes through the documented read, merge, and update workflow or higher-level page-building tools that preserve existing state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Alexander-lq/pagesskill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline tool-call examples, code blocks, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing instructions for NocoBase page-building tool calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
