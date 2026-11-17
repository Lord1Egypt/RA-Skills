## Description:

Fetches Hacker News front-page posts on demand, filters or boosts them by topic, excludes crypto, and sends a concise digest with links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cpojer](https://clawhub.ai/user/cpojer)

### License/Terms of Use:


## Use Case:

Users ask an agent for a Hacker News front-page digest, optionally specifying a count, offset, or topic such as tech, health, hacking, or lifehacks. The skill returns selected posts as individual messages and generates a mood image inspired by the digest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically runs an image-generation workflow that uses Gemini or OpenClaw credentials, which is broader than the user-facing digest description.

Mitigation: Disclose the image-generation step and required credentials before deployment, or make image generation opt-in with explicit user confirmation.

Risk: The image workflow installs Python packages at runtime and makes outbound API calls.

Mitigation: Pin and review dependencies, run the skill in a constrained environment, and allow outbound network access only to the services required for Hacker News retrieval and image generation.

Risk: The workflow writes a virtual environment and generated image files under ./tmp.

Mitigation: Run it only in workspaces where temporary file writes are acceptable and periodically remove generated artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cpojer/skills/hn-digest)
- [Hacker News front page](https://news.ycombinator.com/)
- [Algolia Hacker News Search API](https://hn.algolia.com/api/v1/search?tags=front_page)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files]

**Output Format:** [Individual text messages with post title, age, comment count, Hacker News comment link, plus a generated PNG image attachment.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Post count is bounded by the script, topics are selected from the supported topic list, crypto-related posts are excluded, and image generation may write files under ./tmp.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
