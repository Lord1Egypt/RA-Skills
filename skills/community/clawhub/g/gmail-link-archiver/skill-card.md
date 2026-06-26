## Description: <br>
Connects to Gmail via IMAP, filters emails by subject prefix in a specified mailbox, crawls discovered links with Playwright, converts crawled content to Markdown, and saves it to the OpenClaw workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinwangmok](https://clawhub.ai/user/jinwangmok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to archive newsletter or read-later links from selected Gmail messages into local Markdown files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a Gmail App Password in a local configuration file. <br>
Mitigation: Use a dedicated Gmail App Password, keep the generated config file private, and revoke the app password or delete ~/.config/gmail-link-archiver/config.json when the workflow is no longer needed. <br>
Risk: A broad subject prefix can cause the skill to crawl many links from matching email messages. <br>
Mitigation: Use a narrow subject prefix and begin with a small --max-links value before larger archive runs. <br>
Risk: Dependency setup installs Playwright, Chromium, and Python packages for local execution. <br>
Mitigation: Run setup in an isolated environment when possible and review the setup command before execution. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/jinwangmok/gmail-link-archiver) <br>
- [Publisher profile](https://clawhub.ai/user/jinwangmok) <br>
- [Gmail App Passwords](https://myaccount.google.com/apppasswords) <br>
- [gmail_link_archiver.py](references/gmail_link_archiver.py) <br>
- [setup.sh](references/setup.sh) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files with YAML frontmatter plus terminal status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves one Markdown file per crawled page using a sanitized URL slug and short hash.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
