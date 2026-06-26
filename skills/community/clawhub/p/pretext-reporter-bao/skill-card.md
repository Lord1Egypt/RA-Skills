## Description: <br>
Pretext Reporter Bao measures multilingual text, computes line layouts, and produces Markdown, JSON, and Canvas-oriented layout reports using the bundled Pretext library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baojun-billion](https://clawhub.ai/user/baojun-billion) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to measure text, validate UI layout behavior, generate layout reports, and prepare Canvas or SVG text-rendering data for multilingual interfaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package ships browser automation, local report-server, and demo or browser-check scripts beyond the public text-measurement API. <br>
Mitigation: Use the core text-measurement APIs for normal workflows and review those scripts before running them. <br>
Risk: Some bundled diagnostic flows may open or control browsers, start local services, collect browser environment details, or post diagnostic reports to a URL supplied in a page query string. <br>
Mitigation: Run diagnostics only in a controlled environment and avoid supplying untrusted report URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baojun-billion/pretext-reporter-bao) <br>
- [Publisher profile](https://clawhub.ai/user/baojun-billion) <br>
- [Pretext GitHub repository](https://github.com/chenglou/pretext) <br>
- [Pretext documentation](https://github.com/chenglou/pretext#readme) <br>
- [Pretext demo](https://chenglou.me/pretext) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, code, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON objects, TypeScript API results, and Canvas report configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include measured dimensions, line counts, line-level layout details, and optional Canvas rendering settings.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
