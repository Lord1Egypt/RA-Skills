## Description: <br>
Syncs Obsidian Markdown notes to a Notion database while preserving rich text, tables, lists, code blocks, callouts, quotes, and equations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[molaters](https://clawhub.ai/user/molaters) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to configure and run an Obsidian-to-Notion sync that uploads selected Markdown notes into a Notion database with mapped properties and native Notion blocks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The sync script can automatically trash same-titled Notion pages and recreate them without a dry run, confirmation step, or built-in backup safeguard. <br>
Mitigation: Review scripts/sync.py before use, test only on a duplicate or low-risk Notion database first, and export or back up the database before running. <br>
Risk: A Notion integration token and directory filters control what content is uploaded, so over-scoped credentials or broad target directories can expose unintended notes. <br>
Mitigation: Use a minimally scoped Notion integration token via NOTION_API_KEY, avoid committing configured files, and restrict TARGET_DIRS and EXCLUDE to only the intended notes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/molaters/obsidian-notion) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, code] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python configuration edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a configured sync workflow; running the script can modify or trash Notion pages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
