## Description: <br>
广州日报/融媒云通用测试助手 helps QA teams generate test cases, run API and URL checks, and draft test reports and bug reports for media cloud backends, apps, H5 pages, mini programs, and backend interfaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freeeye](https://clawhub.ai/user/freeeye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA testers and developers use this skill to plan and document testing for Guangzhou Daily and media cloud products, including smoke, regression, compatibility, performance, API, H5, mini program, and app testing. It can generate structured test cases, test reports, bug report drafts, and commands for targeted API or URL checks. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send live HTTP traffic, including security, performance, POST, PUT, and DELETE tests. <br>
Mitigation: Run tests only against authorized test or staging systems, and avoid production or third-party targets without explicit permission. <br>
Risk: Tokens, headers, request bodies, and response previews used in tests may contain sensitive information. <br>
Mitigation: Treat tokens and headers as sensitive, avoid sharing generated reports publicly, and redact secrets before storing or forwarding outputs. <br>
Risk: The bundled API and URL scripts may automatically install the Python requests dependency if it is missing. <br>
Mitigation: Preinstall dependencies in a controlled environment before running the scripts when automatic pip changes are not desired. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/freeeye/gz-media-tester) <br>
- [Publisher Profile](https://clawhub.ai/user/freeeye) <br>
- [API Reference](references/api-reference.md) <br>
- [Bug Template](references/bug-template.md) <br>
- [Compatibility Guide](references/compatibility.md) <br>
- [Report Template](references/report-template.md) <br>
- [Test Cases](references/test-cases.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown reports, Markdown tables, JSON reports, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include generated QA artifacts and live API or URL check results when the user runs the bundled scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
