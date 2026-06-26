## Description: <br>
Generate TikTok-style talking videos from a script and image using the LovelyBots API, then poll for completion and return the final video URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[georgegally](https://clawhub.ai/user/georgegally) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams, ecommerce brands, developers, and agent pipeline builders use this skill to queue, monitor, and retrieve LovelyBots talking-video generations from a script and source image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted scripts, images, likenesses, and generated share URLs may be sensitive. <br>
Mitigation: Install only if the user trusts LovelyBots to process provided media, avoid confidential or non-consensual likeness data unless vendor terms permit it, and treat share URLs as public or bearer-style links. <br>
Risk: The LovelyBots API key can authorize paid video generation and expose account usage. <br>
Mitigation: Store LOVELYBOTS_API_KEY as a secret, never commit it, rotate it if exposed, and monitor remaining credits and account usage. <br>
Risk: Aggressive polling or high concurrency can increase API load or trigger rate limits. <br>
Mitigation: Use timeout, retry, jitter, and backoff controls; stop on terminal job states or non-retryable API errors. <br>


## Reference(s): <br>
- [LovelyBots OpenClaw Documentation](https://lovelybots.com/openclaw) <br>
- [LovelyBots Developer API Key Page](https://lovelybots.com/developer) <br>
- [ClawHub Skill Page](https://clawhub.ai/georgegally/lovelybots-video) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON examples and bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces API request guidance, polling status text, share URLs, and final video URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
