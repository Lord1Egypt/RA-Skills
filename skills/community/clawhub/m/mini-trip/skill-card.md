## Description: <br>
Plan a complete 3-day, 2-night trip with morning activities, afternoon exploration, and evening dining experiences, with support for travel booking workflows powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-focused agents use this skill to plan concise 3-day trips, compare flights, hotels, and attractions, and produce itinerary guidance backed by flyai CLI results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install and rely on a global npm CLI. <br>
Mitigation: Review the requested npm install and CLI commands before allowing execution. <br>
Risk: Trip requests may be sent to flyai or Fliggy services. <br>
Mitigation: Avoid entering highly sensitive travel details unless they are necessary for the booking search. <br>
Risk: The skill describes hidden local logging of raw trip requests. <br>
Mitigation: Disable, delete, or review `.flyai-execution-log.json` before and after use when privacy matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/mini-trip) <br>
- [templates.md](references/templates.md) <br>
- [playbooks.md](references/playbooks.md) <br>
- [fallbacks.md](references/fallbacks.md) <br>
- [runbook.md](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be grounded in flyai CLI results and include booking links for each listed travel result.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
