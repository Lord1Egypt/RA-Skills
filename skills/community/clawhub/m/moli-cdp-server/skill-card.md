## Description:

Start Moli's CDP server and connect Playwright, Puppeteer, or raw CDP clients to a local CDP endpoint for automation, layout, screenshot, and troubleshooting workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lexmount](https://clawhub.ai/user/lexmount)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to start a Moli CDP server and attach existing Playwright, Puppeteer, or raw CDP clients without launching a separate bundled browser. It also guides connection troubleshooting, layout-enabled runs, resource loading, profiles, cookies, proxies, and loopback network exposure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation workflow can execute a mutable remote installer without checksum or signature verification.

Mitigation: Review and trust the installer source before running it, and prefer a pinned release with checksum or signature verification.

Risk: Imported cookies or persistent browser profiles may expose account sessions to automation.

Mitigation: Use disposable runs by default and import cookies or persistent profiles only when that account-session access is intentional.

Risk: Exposing the CDP endpoint beyond loopback can allow unintended remote browser automation access.

Mitigation: Bind to 127.0.0.1 unless remote access is required and network access controls are in place.

## Reference(s):

- [CDP server guide](references/protocols.md)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash, PowerShell, and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local server defaults, client connection examples, integration rules, and troubleshooting steps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
