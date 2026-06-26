## Description: <br>
OpenClaw CWS Publisher helps developers package and harden Chrome extensions with Chrome Web Store package, listing, design, local E2E, Chrome release, competitor, leak, GitHub, and ClawHub release gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and extension release maintainers use this skill to prepare a Chrome extension repository for Chrome Web Store submission, public release checks, metadata generation, and publish-command review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce release and publish commands for Chrome Web Store, GitHub, or ClawHub workflows. <br>
Mitigation: Review every generated command and release artifact before execution or submission. <br>
Risk: Leak reports and scan outputs may contain sensitive repository details. <br>
Mitigation: Keep generated leak reports private and resolve findings before public release. <br>
Risk: The public artifact is instruction-only and expects companion scripts from a trusted checkout. <br>
Mitigation: Use a trusted companion-script checkout and run the skill only against the intended extension repository. <br>


## Reference(s): <br>
- [OpenClaw CWS Publisher ClawHub page](https://clawhub.ai/zack-dev-cm/openclaw-cws-publisher) <br>
- [OpenClaw CWS Publisher homepage](https://github.com/zack-dev-cm/openclaw-cws-publisher) <br>
- [Chrome Web Store Program Policies](https://developer.chrome.com/docs/webstore/program-policies/policies) <br>
- [Manifest V3 remote-code requirements](https://developer.chrome.com/docs/webstore/program-policies/mv3-requirements) <br>
- [Chrome extension activeTab model](https://developer.chrome.com/docs/extensions/develop/concepts/activeTab) <br>
- [Chrome extension permission warnings](https://developer.chrome.com/docs/extensions/develop/concepts/declare-permissions) <br>
- [Chrome release notes](https://developer.chrome.com/release-notes/) <br>
- [ChromiumDash Chrome release feed](https://chromiumdash.appspot.com/fetch_releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated release metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference repo-local reports, ZIP artifacts, launch metadata, and publish commands for user review.] <br>

## Skill Version(s): <br>
0.3.5 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
