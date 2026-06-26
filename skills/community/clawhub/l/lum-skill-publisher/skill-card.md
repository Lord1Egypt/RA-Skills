## Description: <br>
Researches, structures, and publishes ClawHub skills by analyzing listing patterns, generating gap reports, patching README/SKILL files, and preparing clawhub publish commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ragesaq](https://clawhub.ai/user/ragesaq) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and skill maintainers use this skill to research ClawHub marketplace patterns, evaluate drafts, patch skill files, and prepare publication commands for ClawHub releases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Draft edits could introduce incorrect or misleading claims into skill files. <br>
Mitigation: Review all diffs before accepting patches and scan the skill before publishing. <br>
Risk: Marketplace skills installed for research may be untrusted reference material. <br>
Mitigation: Treat downloaded skills as reference material only and review any copied content or patterns before reuse. <br>
Risk: Publishing runs under the active ClawHub account and could release the wrong slug, version, changelog, or visibility. <br>
Mitigation: Confirm clawhub whoami and approve the final publish command only after checking slug, version, changelog, and intended visibility. <br>


## Reference(s): <br>
- [ClawHub Skill Publisher listing](https://clawhub.ai/ragesaq/lum-skill-publisher) <br>
- [ClawHub](https://clawhub.ai) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Gap Analysis Examples](examples/gap-analysis.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and file patch guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose README.md and SKILL.md edits and final publish commands for user review.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
