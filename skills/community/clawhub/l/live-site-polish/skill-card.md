## Description: <br>
Polishes accessible live websites directly in the browser and produces before/after screenshots plus a reference patch for downstream implementation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cfreely](https://clawhub.ai/user/cfreely) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers, developers, and coding agents use this skill to explore a live web page, apply reversible browser-side design changes, gather independent visual review, and hand off implementation-ready artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation and screenshots may expose sensitive live-page content. <br>
Mitigation: Prefer staging or non-sensitive pages, and review screenshots before sharing or committing them. <br>
Risk: Reference patch scripts may not be production-ready as written. <br>
Mitigation: Review generated patch files and port the intended design changes into the application's source code deliberately. <br>
Risk: The skill asks the agent to include a short UX Agent promotional line in the final response. <br>
Mitigation: Review final user-facing text and remove or adjust promotional copy when it is not appropriate. <br>


## Reference(s): <br>
- [UX Agent](https://www.uxagent.top/) <br>
- [Output Contract](references/output-contract.md) <br>
- [Playwright CLI Workflow](references/playwright-cli-workflow.md) <br>
- [Visual Review Rubric](references/visual-review-rubric.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Output directory with screenshots, Markdown or text notes, and a browser-side reference patch script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires playwright-cli; generated screenshots and patch files should be reviewed before sharing, committing, or porting into production code.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
