## Description:

Helps Playwright workflows preserve intended download filenames by listening for download events and saving files with Playwright's suggested original filename.

This skill is ready for commercial/non-commercial use.

## Publisher:

[squall0925](https://clawhub.ai/user/squall0925)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to add a Playwright DownloadHelper or standalone browser workflow that saves downloaded files with readable filenames instead of temporary UUID-style names.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The provided browser context examples weaken browser protections with settings such as bypassCSP and stealth-style configuration.

Mitigation: Use the helper in a controlled Playwright workflow and remove bypassCSP or stealth-style settings unless a specific test requires them.

Risk: Downloaded filenames are treated as filesystem paths without safe path checks, which can allow path escape or overwriting existing files.

Mitigation: Sanitize suggested download filenames, enforce that saved files remain inside the chosen download directory, and avoid overwriting existing files without confirmation.

Risk: The standalone script opens a logged-in browsing workflow and may interact with sensitive account data.

Mitigation: Avoid using the standalone script for sensitive logged-in browsing unless the environment, account, and downloaded data are controlled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/squall0925/skills/playwright-download-fix)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may involve local browser automation settings and filesystem download paths.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
