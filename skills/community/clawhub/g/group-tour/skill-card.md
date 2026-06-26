## Description: <br>
Find organized group tours and travel packages with professional guides, planned itineraries, meals included, and hassle-free travel for those who prefer structure; it also supports related travel searches such as flights, hotels, attractions, itinerary planning, visas, insurance, and car rental through Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-support agents use this skill to search organized group tours and related travel options from live FlyAI/Fliggy results, then present concise Markdown results with booking links. It is aimed at users who prefer structured travel packages, guided tours, or package comparisons instead of self-planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install the FlyAI CLI globally before use. <br>
Mitigation: Review and approve the `npm i -g @fly-ai/flyai-cli` installation step before allowing the skill to run it. <br>
Risk: Travel searches are sent to FlyAI/Fliggy services. <br>
Mitigation: Avoid entering sensitive travel details unless the user accepts that data will be processed by those services. <br>
Risk: Raw travel requests may be stored locally in `.flyai-execution-log.json`. <br>
Mitigation: Disable, restrict, or remove the local execution log when query persistence is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/group-tour) <br>
- [Publisher profile](https://clawhub.ai/user/xiejinsong) <br>
- [templates.md](references/templates.md) <br>
- [playbooks.md](references/playbooks.md) <br>
- [fallbacks.md](references/fallbacks.md) <br>
- [runbook.md](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with booking links, comparison tables, concise guidance, and inline shell commands when setup or retry steps are needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live flyai-cli output for travel results and should not present travel prices, names, or booking details without CLI-sourced data.] <br>

## Skill Version(s): <br>
v3.2.3 (source: ClawHub release evidence; artifact frontmatter reports 3.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
