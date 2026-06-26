## Description: <br>
Uses Wikmd to manage a personal local Markdown wiki that an agent can consult, update, and optionally serve over local HTTP for manual review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[errant](https://clawhub.ai/user/errant) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to keep a local personal wiki of projects, research, decisions, resources, and other reusable context. It supports reading existing Markdown pages, creating or updating wiki pages, and recording useful findings with git history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages proactive reads and writes in a local personal wiki, which could capture incorrect, sensitive, or unwanted information. <br>
Mitigation: Use a dedicated PERSONAL_WIKI_ROOT folder, review proposed edits before committing, and avoid storing secrets or sensitive third-party information. <br>
Risk: Serving the wiki on 0.0.0.0 can expose wiki content to the local network. <br>
Mitigation: Keep the Wikmd host bound to 127.0.0.1 unless network access is intentional and appropriate. <br>


## Reference(s): <br>
- [Wikmd project](https://github.com/Linbreux/wikmd) <br>
- [Wikmd documentation](https://linbreux.github.io/wikmd/) <br>
- [Wikmd Markdown Reference](references/wikmd-formatting.md) <br>
- [ClawHub skill page](https://clawhub.ai/errant/personal-memory-wiki) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local Markdown files under PERSONAL_WIKI_ROOT/wiki when the user accepts those changes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
