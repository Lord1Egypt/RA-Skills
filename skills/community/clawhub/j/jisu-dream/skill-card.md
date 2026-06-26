## Description: <br>
Searches Duke of Zhou dream interpretations by keyword with pagination support for dream-meaning questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to look up short entertainment-oriented interpretations for dream keywords, then summarize the most relevant results in conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dream search keywords are sent to JisuAPI and may reveal sensitive personal details if users include them. <br>
Mitigation: Avoid sensitive personal details in dream queries and use a dedicated JisuAPI key that can be rotated or revoked. <br>
Risk: Dream interpretations are entertainment and learning references, not reliable decision, medical, or safety advice. <br>
Mitigation: Summarize results as non-authoritative guidance and include a brief reminder not to over-rely on dream meanings for real-world decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/jisu-dream) <br>
- [JisuAPI Dream API](https://www.jisuapi.com/api/dream) <br>
- [JisuAPI](https://www.jisuapi.com/) <br>
- [Dream search endpoint](https://api.jisuapi.com/dream/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON command output from the dream search script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and the JISU_API_KEY environment variable; search requests include a keyword plus optional pagenum and pagesize values.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
