## Description: <br>
Helps agents manage X/Twitter activity through the OpenTweet API, including posts, scheduling, threads, media uploads, evergreen queues, inspiration search, AI repurposing, and analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[petricbranko](https://clawhub.ai/user/petricbranko) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and content teams use this skill to let an agent prepare, schedule, publish, and analyze X/Twitter content through OpenTweet while respecting account, subscription, and confirmation checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish, schedule, auto-retweet, auto-reply, and otherwise affect public X/Twitter activity. <br>
Mitigation: Require explicit user approval before publishing, scheduling batches, evergreen queues, auto-retweets, and auto-replies, and verify the target account before posting. <br>
Risk: The skill requires a sensitive OpenTweet API credential. <br>
Mitigation: Protect OPENTWEET_API_KEY as a secret and avoid exposing it in prompts, logs, command output, or generated content. <br>
Risk: Agent-generated or repurposed content may be posted publicly if not reviewed. <br>
Mitigation: Show generated or repurposed content to the user for review before saving it as an auto-scheduled or publish-ready post. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/petricbranko/opentweet-x-poster) <br>
- [OpenTweet OpenClaw posting guide](https://opentweet.io/features/openclaw-twitter-posting) <br>
- [OpenTweet API documentation](https://opentweet.io/api/v1/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, code] <br>
**Output Format:** [Markdown with HTTP request examples and JSON response handling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENTWEET_API_KEY. The skill instructs agents to verify account access, parse actual API responses, and ask for confirmation before public publishing actions.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
