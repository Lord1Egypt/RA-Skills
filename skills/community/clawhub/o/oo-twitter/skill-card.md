## Description: <br>
Operate X (Twitter) through an OOMOL-connected account to read, create, update, and delete account data with schema-first oo CLI connector commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to perform X (Twitter) tasks through an OOMOL-connected account, including reading profiles, posts, timelines, bookmarks, lists, Spaces, DMs, and search results. It also supports user-approved posting, following, muting, list management, bookmark, DM, media upload, and deletion workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate an OOMOL-connected X/Twitter account and read private account data, including DMs, when requested. <br>
Mitigation: Install and use it only for accounts where that level of OOMOL-connected tooling access is acceptable, and review requested read targets before execution. <br>
Risk: Write actions can change X/Twitter account state, including posts, follows, DMs, lists, bookmarks, mutes, and media uploads. <br>
Mitigation: Confirm the exact payload and expected account effect with the user before running any action tagged as write. <br>
Risk: Destructive actions can delete or remove account data such as posts, DMs, lists, list members, and bookmarks. <br>
Mitigation: Require explicit approval for the exact destructive target before execution. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/oomol/oo-twitter) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [X homepage](https://x.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
