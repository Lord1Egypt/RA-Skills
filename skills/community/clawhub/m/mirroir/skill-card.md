## Description: <br>
Control a real iPhone through macOS iPhone Mirroring -- screenshot, tap, swipe, type, launch apps, record video, OCR, and run multi-step scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jfarcand](https://clawhub.ai/user/jfarcand) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and other external users use Mirroir to inspect and control a paired iPhone from an agent workflow for app testing, screenshots, OCR, video recording, messaging workflows, settings checks, and multi-step iOS scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad control over logged-in iPhone apps, including the ability to send messages, submit forms, change settings, type text, and record the screen. <br>
Mitigation: Install only for intentional iPhone control, supervise sessions, close sensitive apps and notifications, and require manual confirmation before messages, forms, settings changes, recordings, or credential use. <br>
Risk: The setup requires privileged macOS helpers, Karabiner-Elements, Screen Recording permission, and Accessibility permission. <br>
Mitigation: Prefer Homebrew or an inspected package over curl-to-bash, grant permissions deliberately, and review or remove the helper daemon, Karabiner extension, Screen Recording permission, and Accessibility permission when finished. <br>


## Reference(s): <br>
- [Mirroir homepage](https://mirroir.dev) <br>
- [Apple iPhone Mirroring support](https://support.apple.com/en-us/105071) <br>
- [Mirroir on ClawHub](https://clawhub.ai/jfarcand/mirroir) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, markdown] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration snippets, and step-by-step tool guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS 15+, iPhone Mirroring, iphone-mirroir-mcp, Karabiner-Elements, Screen Recording permission, and Accessibility permission.] <br>

## Skill Version(s): <br>
0.13.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
