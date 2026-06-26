## Description: <br>
Obsidian Remote lets an agent control a running Obsidian desktop app through Obsidian's built-in CLI for note, vault, search, task, plugin, sync, publish, and developer-tool workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[douglascorrea](https://clawhub.ai/user/douglascorrea) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge workers, and automation agents use this skill to inspect, update, search, and manage an Obsidian vault through the live desktop app. It is useful when an agent needs structured command guidance for notes, daily notes, tasks, properties, tags, plugins, sync, publish, bases, themes, snippets, file history, or Obsidian developer tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad control over a live Obsidian vault, including private notes and app internals. <br>
Mitigation: Install it only when live Obsidian vault control is intended, start with a test or backed-up vault, and review proposed actions before execution. <br>
Risk: Destructive, publishing, restore, plugin, theme, snippet, bulk-search, eval, and CDP commands can expose or change sensitive vault content. <br>
Mitigation: Require manual confirmation for those actions, avoid dev-tool and eval commands unless explicitly needed, and do not use the skill on vaults containing credentials or private material without additional safeguards. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/douglascorrea/obsidian-remote) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may return text, Markdown, JSON, TSV, or CSV depending on the selected Obsidian CLI format option.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
