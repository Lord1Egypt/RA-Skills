## Description: <br>
Lumi Diary is a local-first memory skill that records personal, group, and event fragments, manages portraits and milestones, and renders interactive memory scrolls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Thhoho](https://clawhub.ai/user/Thhoho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Lumi Diary to keep a local diary of personal, group, and event memories, search or edit stored fragments, and render or share interactive memory scrolls and .lumi capsules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently profiles people and archives group chat or media context, which can create consent and privacy risks. <br>
Mitigation: Use group features only when participants know Lumi is archiving, and review stored fragments, portraits, and keepsakes regularly. <br>
Risk: Durable local memories and media references may be deleted, overwritten, or stored in an unintended location. <br>
Mitigation: Set LUMI_VAULT_PATH deliberately and back up important memories before allowing destructive actions. <br>
Risk: Imported .lumi capsules can merge outside memories and media into the local vault. <br>
Mitigation: Import .lumi capsules only from trusted sources. <br>


## Reference(s): <br>
- [ClawHub Lumi Diary release](https://clawhub.ai/Thhoho/lumi-diary) <br>
- [Publisher profile: Thhoho](https://clawhub.ai/user/Thhoho) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, HTML, Files, Configuration guidance] <br>
**Output Format:** [Tool responses with local Markdown and JSON records, generated HTML memory scrolls, .lumi ZIP capsules, and optional PNG screenshots.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes durable memory data to a configurable local Lumi_Vault path; optional PNG export requires Playwright.] <br>

## Skill Version(s): <br>
0.2.0 (source: SKILL.md frontmatter, pyproject.toml, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
