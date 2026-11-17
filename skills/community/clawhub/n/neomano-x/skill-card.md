## Description:

Draft, revise, and publish X (Twitter) posts with an image using the X API after an explicit human approval step.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elandivar](https://clawhub.ai/user/elandivar)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social media operators use this skill to draft, revise, and publish X posts with an optional image. The workflow is intended to keep publishing behind explicit user approval while providing setup commands for X API credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish directly to X if the publish helper is invoked with valid credentials.

Mitigation: Require human review before installation and use a dedicated low-privilege X app or account for any credentials.

Risk: OAuth helper output can expose reusable access tokens in terminal logs.

Mitigation: Avoid running the OAuth helper in logged terminals and rotate any tokens that have already been printed or captured.

Risk: The documented approval word is not a technical access control because direct publish invocation can still post immediately.

Mitigation: Do not rely on the approval word alone; restrict who can run the publish command and review commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elandivar/skills/neomano-x)
- [X OAuth request token endpoint](https://api.twitter.com/oauth/request_token)
- [X OAuth access token endpoint](https://api.twitter.com/oauth/access_token)
- [X media upload endpoint](https://upload.twitter.com/1.1/media/upload.json)
- [X tweet creation endpoint](https://api.twitter.com/2/tweets)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, API calls, guidance]

**Output Format:** [Markdown guidance with shell commands; helper scripts emit JSON for dry-run and publish results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include proposed post text, image path references, setup instructions, and X API response JSON.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
