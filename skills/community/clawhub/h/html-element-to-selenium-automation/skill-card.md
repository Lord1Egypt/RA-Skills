## Description: <br>
Converts a webpage into page-structure analysis, operation steps, and runnable Python Selenium automation code using captured screenshots and rendered HTML. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[icestorms](https://clawhub.ai/user/icestorms) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to inspect authorized web pages, identify DOM and interaction patterns, and produce Selenium scripts for workflows such as navigation, form entry, login handling, and search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate real browser interactions on pages that may be sensitive or outside the user's authorization. <br>
Mitigation: Use it only on pages the user owns or is authorized to test, and review the target URL and intended action before execution. <br>
Risk: Login support can use credentials, and captured screenshots or HTML may include private account data. <br>
Mitigation: Use low-privilege test accounts, avoid broad ROUTER_* credential configuration, store outputs in controlled locations, and treat generated captures as private data. <br>
Risk: Broad activation language may lead to browser automation when the requested scope is ambiguous. <br>
Mitigation: Confirm the URL, authorization, credential scope, and intended action before enabling login or executing generated Selenium code. <br>


## Reference(s): <br>
- [Selenium Patterns](artifact/references/selenium-patterns.md) <br>
- [Operation Examples](artifact/references/examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/icestorms/html-element-to-selenium-automation) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python code blocks, Selenium examples, page analysis, shell commands, and generated page-capture files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save screenshots, rendered HTML, viewport screenshots, and page metadata while analyzing a target page.] <br>

## Skill Version(s): <br>
2.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
