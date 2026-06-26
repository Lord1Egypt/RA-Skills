## Description: <br>
Creates interactive architecture diagrams and other structured visualizations from architecture descriptions, business logic, knowledge-base content, workflows, mind maps, and long-form text using ContextWeave. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qhyw99](https://clawhub.ai/user/qhyw99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, architects, and technical teams use this skill to turn system descriptions, code architecture, process flows, and dense text into visual diagrams. It can generate new ContextWeave diagrams, edit existing diagram sessions, import or export CW code, and attach file links through a controlled two-step workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagram prompts, architecture descriptions, and CW or request file content may be sent to the ContextWeave backend. <br>
Mitigation: Avoid submitting confidential system details unless the backend is trusted for that data. <br>
Risk: The skill can use a bundled anonymous API key when CONTEXTWEAVE_MCP_API_KEY is not set. <br>
Mitigation: Set a user-controlled CONTEXTWEAVE_MCP_API_KEY before use when account separation or credential control is required. <br>
Risk: Session IDs and saved .cw files may contain sensitive diagram context. <br>
Mitigation: Store generated session IDs and .cw files only in appropriate locations and avoid sharing them when they include sensitive content. <br>
Risk: The E2E test script performs live remote workflow checks. <br>
Mitigation: Review the test script before running it and execute it only in an environment approved for remote requests. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/qhyw99/interactive-architecture-diagram) <br>
- [Publisher Profile](https://clawhub.ai/user/qhyw99) <br>
- [ContextWeave API Endpoint Example](https://api.contextweave.site) <br>
- [ContextWeave Default Runtime Endpoint](https://pptx.chenxitech.site) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code] <br>
**Output Format:** [JSON status objects with generated diagram session identifiers, asset URLs, and optional saved CW code files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and may use CONTEXTWEAVE_MCP_API_KEY for authenticated ContextWeave requests.] <br>

## Skill Version(s): <br>
0.1.18 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
