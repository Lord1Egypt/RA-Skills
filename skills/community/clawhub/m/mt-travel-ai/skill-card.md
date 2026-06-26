## Description: <br>
A Meituan travel assistant skill for travel inspiration, itinerary planning, hotel and transport search, attraction tickets, vacation products, and transaction-oriented travel recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qy-zhang](https://clawhub.ai/user/qy-zhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to ask for domestic travel ideas, route options, hotels, train or flight information, attraction tickets, and vacation packages through Meituan travel supply. The skill guides token setup, calls the Meituan travel CLI, and returns the CLI result as complete Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide a sensitive Meituan API token and stores it locally in plaintext. <br>
Mitigation: Configure the token outside chat in a protected environment or credential store when possible, avoid printing secrets in conversation, and rotate any token that has already been shared. <br>
Risk: The skill depends on the Meituan travel CLI and sends travel queries to Meituan services. <br>
Mitigation: Install and use the skill only if you trust the Meituan CLI and are comfortable with the external service handling the query and token. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qy-zhang/mt-travel-ai) <br>
- [Meituan developer token page](https://developer.meituan.com/zh/v2/dev/token) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and preserved links or images from the Meituan CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include travel product names, prices, ratings, distances, images, and booking links returned by the Meituan CLI.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
