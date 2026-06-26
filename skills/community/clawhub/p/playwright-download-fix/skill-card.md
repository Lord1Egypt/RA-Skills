## Description: <br>
Automatically handles Playwright download events and saves downloaded files with the original filename reported by Playwright instead of a temporary UUID filename. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Squall0925](https://clawhub.ai/user/Squall0925) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to add a Playwright download helper to scripts, configure a download directory, and preserve suggested filenames when files are downloaded. It is most useful for browser automation workflows that need predictable downloaded file paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package promotes browser automation settings such as CSP bypass, stealth-style configuration, and a site-specific resume workflow that may exceed a simple download filename fix. <br>
Mitigation: Review the skill before installation, prefer integrating only download-helper.js into an existing Playwright script, and use an explicit download directory. <br>
Risk: Automating recruitment or resume downloads may involve privacy-sensitive data and site terms that require authorization. <br>
Mitigation: Use the recruitment workflow only when authorized to automate that site and when privacy requirements for downloaded files are understood. <br>
Risk: The referenced pw-start alias depends on a workspace script that is not included in the artifact evidence. <br>
Mitigation: Avoid the pw-start alias unless the referenced pw-start.js has been reviewed in the target environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Squall0925/playwright-download-fix) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions and helper code for Playwright scripts; downloaded files are written by the user's runtime environment.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
