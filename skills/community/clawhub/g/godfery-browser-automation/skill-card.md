## Description: <br>
Automates web browser tasks through CLI commands for navigation, interaction, data extraction, screenshots, form handling, and browser cleanup using local Chrome or SkillBoss API Hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godferylindsay](https://clawhub.ai/user/godferylindsay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to drive browser workflows such as visiting pages, clicking or filling elements, extracting structured page data, taking screenshots, downloading files, and closing browser sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control logged-in browser sessions and interact with private or sensitive websites. <br>
Mitigation: Use isolated test profiles and test accounts, avoid real passwords or regulated data, and require explicit confirmation before submitting forms or acting on logged-in sites. <br>
Risk: Page context may be routed through SkillBoss API Hub when remote mode or AI-driven actions are used. <br>
Mitigation: Install only when remote routing is acceptable and avoid exposing confidential page content to the service. <br>
Risk: Screenshots, downloads, cookies, and saved passwords can persist on disk with limited user control. <br>
Mitigation: Review screenshot and download directories, verify downloaded files before use, and clear or isolate browser profiles after sensitive tasks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/godferylindsay/godfery-browser-automation) <br>
- [Publisher profile](https://clawhub.ai/user/godferylindsay) <br>
- [Complete setup guide](https://skillboss.co/skill.md) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [REFERENCE.md](REFERENCE.md) <br>
- [EXAMPLES.md](EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Screenshots are saved as PNG files and downloads are saved to the configured downloads directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
