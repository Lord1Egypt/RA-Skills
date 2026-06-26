## Description: <br>
Book hotels with genuine hot spring baths, including natural onsen pools, private hot spring rooms, and Japanese-style ryokan experiences, powered by Fliggy through the flyai CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travel users use this skill to search for onsen hotels, private hot spring rooms, and ryokan-style stays from real-time flyai CLI results. It is also used to prepare booking-oriented Markdown summaries with current prices and booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install and run the global flyai CLI package. <br>
Mitigation: Review the CLI package before installation and approve installation manually in managed environments. <br>
Risk: Local execution logs can contain raw travel queries and may include sensitive booking-related details. <br>
Mitigation: Avoid entering highly sensitive travel, passport, payment, or booking reference information, and review or delete `.flyai-execution-log.json` after use. <br>
Risk: Travel availability and pricing can change between search and booking. <br>
Mitigation: Confirm price, room details, policies, and booking links on the provider page before purchase. <br>


## Reference(s): <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/onsen-hotel) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be based on flyai CLI results and include booking links when results are available.] <br>

## Skill Version(s): <br>
3.2.1 (source: server release metadata; artifact frontmatter states 3.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
