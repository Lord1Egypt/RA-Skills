## Description: <br>
Hire a private car with driver for customized day tours, with support for related travel bookings and planning powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to search for private car tours with drivers, collect a destination query, run the FlyAI CLI, and format booking options with links for user review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install and run the global @fly-ai/flyai-cli package and send travel search details such as origin, destination, dates, and preferences to that service. <br>
Mitigation: Review the package and requested travel details before use, and avoid sending sensitive personal information unless the user accepts that service interaction. <br>
Risk: The skill presents booking links that can lead to purchases. <br>
Mitigation: Review provider details, prices, dates, cancellation terms, and final checkout pages before buying anything. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/poll-test-1775879470) <br>
- [Publisher profile](https://clawhub.ai/user/xiejinsong) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with CLI command snippets, comparison tables, and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses FlyAI CLI output for live travel results and requires booking links for listed options.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
