## Description: <br>
Lightpanda browser is a drop-in replacement for Chrome and the Openclaw default browser that is faster and lighter for tasks without graphical rendering, such as data retrieval with CDP clients like Playwright or Puppeteer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krichprollsch](https://clawhub.ai/user/krichprollsch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation engineers use this skill to install and run Lightpanda as a lightweight CDP-compatible browser for data retrieval and web automation when graphical rendering is not needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install script downloads a nightly Lightpanda binary from GitHub, so users depend on that release channel and its availability. <br>
Mitigation: Install only when the Lightpanda nightly release channel is trusted, and rely on the script's checksum verification before executing the binary. <br>
Risk: A CDP browser server can control and inspect browser sessions. <br>
Mitigation: Keep the server bound to 127.0.0.1, close it when finished, and avoid sensitive logged-in sessions or untrusted automation scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krichprollsch/lightpanda-browser) <br>
- [Lightpanda agent skill source](https://github.com/lightpanda-io/agent-skill) <br>
- [Lightpanda browser issues](https://github.com/lightpanda-io/browser/issues) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides install commands, CDP server startup guidance, and Playwright/Puppeteer connection examples.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
