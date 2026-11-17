## Description:

Twitch engagement via PizzaParty.gg - 4 daily sessions for LevelUpLove.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wespeakallday](https://clawhub.ai/user/wespeakallday)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run scheduled Twitch chat engagement sessions for PizzaParty.gg point earning with configured Twitch credentials and streamer inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can post public Twitch chat messages using the user's account.

Mitigation: Use only a dedicated low-privilege Twitch token, validate streamer inputs before execution, and confirm that planned use complies with account and platform policies.

Risk: OAuth tokens may be exposed through command history or process listings when passed as command-line arguments.

Mitigation: Provide credentials through a protected secret manager or short-lived execution environment and avoid storing invocations that contain tokens.

Risk: The released artifact asks for more secrets than the code uses and does not implement the advertised PizzaParty scraping or scheduling flow.

Mitigation: Review the implementation before deployment, provide only secrets required by the executed code, and verify scheduling and scraping behavior outside the skill before relying on it.

## Reference(s):


## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands, Configuration]

**Output Format:** [JSON session summary file and command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires caller-provided Twitch OAuth credentials and streamer input.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
