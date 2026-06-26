## Description: <br>
Fetch and send Hacker News front-page posts on demand. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cpojer](https://clawhub.ai/user/cpojer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to request concise Hacker News front-page digests by count or topic, with crypto-related posts excluded. The skill sends each selected post as a separate text message and then attaches a generated mood image inspired by the digest. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically generates an AI image after each digest and may consume Gemini/Nano Banana API quota. <br>
Mitigation: Use a separate limited API key for this skill, monitor quota usage, or make the image step opt-in before deployment. <br>
Risk: The image-generation helper installs Python dependencies at runtime. <br>
Mitigation: Review and pin the required dependencies in a controlled environment before using the skill in production. <br>


## Reference(s): <br>
- [HN Digest on ClawHub](https://clawhub.ai/cpojer/hn-digest) <br>
- [Hacker News](https://news.ycombinator.com/) <br>
- [HN Algolia API front-page endpoint](https://hn.algolia.com/api/v1/search?tags=front_page) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Media] <br>
**Output Format:** [Plain text post messages plus a PNG image attachment] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default count is 5 posts; supports count, offset, and topic filtering for tech, health, hacking, and lifehacks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
