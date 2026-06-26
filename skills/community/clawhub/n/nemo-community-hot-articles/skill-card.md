## Description: <br>
Gets trending articles from the Nemo community without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geeeeeeeeeeeeeeeek](https://clawhub.ai/user/geeeeeeeeeeeeeeeek) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent fetch current popular Nemo community articles and summarize article metadata such as title, section, popularity, and URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes an outbound HTTPS request to link-nemo.com, exposing normal network metadata such as IP address. <br>
Mitigation: Confirm that outbound access to link-nemo.com is allowed before installation or use. <br>
Risk: The documented example uses jq even though only curl is declared as required. <br>
Mitigation: Install jq or use another JSON parser before relying on the example command. <br>
Risk: Trending article data is live third-party content and may change or become unavailable. <br>
Mitigation: Treat results as current external content and verify important details from the returned article URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/geeeeeeeeeeeeeeeek/nemo-community-hot-articles) <br>
- [Nemo popular articles](https://www.link-nemo.com/popular) <br>
- [Nemo popular articles API](https://www.link-nemo.com/api/popular/article) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell command examples and article metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require outbound HTTPS access to link-nemo.com and a JSON parser such as jq for the documented example.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
