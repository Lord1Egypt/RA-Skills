## Description: <br>
Generate AI music videos from any MCP client. Turn text prompts into cinematic music videos with multiple styles and modes. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[liuyinjiwen06](https://clawhub.ai/user/liuyinjiwen06) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External creators and developers can connect this MCP server to an MCP client to request music-video concepts, generation status, style listings, and account information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release asks for FREEBEAT_API_KEY while security evidence says music-video and account results are mock outputs. <br>
Mitigation: Do not provide a production Freebeat API key. If testing is necessary, use a disposable low-privilege key and verify the exact npm package before running the npx command. <br>
Risk: Generated video URLs, status, credits, and account details may be misleading because this release simulates those values. <br>
Mitigation: Treat outputs as demonstration data unless the publisher clearly documents real API calls and labels simulated responses. <br>


## Reference(s): <br>
- [Artifact README](README.md) <br>
- [Freebeat Developer Portal](https://freebeat.ai/developers) <br>
- [Freebeat API Docs](https://freebeat.ai/developers/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, configuration] <br>
**Output Format:** [MCP text responses containing JSON job metadata, status objects, style lists, account details, and setup configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FREEBEAT_API_KEY for generation and account tools; security evidence says this release returns mock music-video and account results.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact package.json reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
