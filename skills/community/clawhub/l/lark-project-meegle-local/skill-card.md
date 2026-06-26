## Description: <br>
Connects to Lark Project and Meegle so an agent can query and manage work items and todos, checking login state and using Device Code authorization when needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuliyuan2026](https://clawhub.ai/user/wuliyuan2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers who use Lark Project or Meegle can ask an agent to inspect todos, query work items, create or update work items, and look up project metadata through the Meegle CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs the @lark-project/meegle npm package through npx. <br>
Mitigation: Install and use it only when the user trusts that npm package and its updates. <br>
Risk: Device Code authorization grants access to the user's Meegle or Feishu Project account. <br>
Mitigation: Have the user review the authorization flow and revoke or remove stored tokens when access is no longer needed. <br>
Risk: Create and update commands can make real changes to business project data. <br>
Mitigation: Confirm intended write operations and target work items before executing create or update commands. <br>
Risk: Parsed URLs or custom hosts could direct login or queries to an unintended site. <br>
Mitigation: Review the parsed host before starting Device Code login or acting on a work item URL. <br>


## Reference(s): <br>
- [Meegle CLI npm package](https://www.npmjs.com/package/@lark-project/meegle) <br>
- [MQL syntax reference](references/mql-syntax.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses npx to run the Meegle CLI with JSON output for parsing.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
