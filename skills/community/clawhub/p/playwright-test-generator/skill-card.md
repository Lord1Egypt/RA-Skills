## Description: <br>
AI-driven Playwright test code generator for QA engineers that creates Page Object Models, standard scripts, and data-driven tests from natural-language descriptions, HTML analysis, or page URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA engineers, test automation specialists, and developers use this skill to bootstrap Playwright tests, Page Object Models, data-driven suites, and locators from plain-language scenarios, HTML snippets, or URL/page analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live URL analysis can open pages in a headless browser and include DOM-derived locators in generated output. <br>
Mitigation: Avoid private intranet pages, admin consoles, authenticated sessions, localhost services, and cloud metadata or internal addresses unless inspection is intended. <br>
Risk: Generated tests and locator files can be written to local output paths. <br>
Mitigation: Review the requested output path and inspect generated code before committing or running it in CI. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shenghoo123-png/playwright-test-generator) <br>
- [README](README.md) <br>
- [Design document](DESIGN-playwright-test-generator.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses containing generated Python or JavaScript/TypeScript Playwright code, JSON locator maps, and CLI commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated test code or locator JSON to local files when an output path is requested.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact package.json and setup.py list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
