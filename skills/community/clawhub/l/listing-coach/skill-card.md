## Description: <br>
Queries the configured real estate Listing Coach knowledge base for listing scripts, FSBO scripts, expired listing scripts, objection scripts, and related listing coaching language, then returns the retrieval output exactly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[woowonjae1](https://clawhub.ai/user/woowonjae1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and real estate professionals use this skill to retrieve exact listing-coach script matches and paste the returned result without summarization or rewriting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User listing-coach queries are sent to a configured external knowledge-base service over unencrypted HTTP. <br>
Mitigation: Use HTTPS for the service connection, disclose the external service clearly, and avoid sending sensitive listing or client information unless the user accepts that data flow. <br>
Risk: The skill package ships a raw API key. <br>
Mitigation: Move the secret to a managed credential store or environment variable, rotate the exposed key, and avoid embedding credentials in release artifacts. <br>
Risk: Retrieved results are written to a temporary Markdown file. <br>
Mitigation: Avoid temp-file persistence when possible, or document retention behavior and clean up temporary result files after use. <br>


## Reference(s): <br>
- [ClawHub listing-coach skill page](https://clawhub.ai/woowonjae1/skills/listing-coach) <br>
- [Configured external knowledge-base service endpoint](http://api-knowledgebase.mlp.cn-beijing.volces.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files] <br>
**Output Format:** [Markdown retrieval result, usually written to a temporary file path for the agent to read and return exactly] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The result is a single pass-through response from the configured knowledge base; the skill contract requires no summarization, translation, reformatting, or added explanation.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
