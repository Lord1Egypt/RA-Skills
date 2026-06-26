## Description: <br>
Guides agents through image-based patent similarity searches using the Zhihuiya patent database for design patents and utility model patents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and IP review teams use this skill to search for visually similar design or utility model patents from an image URL and review ranked patent matches for prior-art or infringement-risk research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patent-search inputs, image URLs, and feedback summaries may be sent to LinkFox/Zhihuiya. <br>
Mitigation: Use a dedicated LinkFox API key, avoid private or authenticated image URLs, and confirm user acceptance before using confidential unpublished designs. <br>
Risk: Similarity scores and returned patent matches may be mistaken for a legal infringement determination. <br>
Mitigation: Present results as research support only and direct users to consult a qualified patent attorney for legal advice. <br>


## Reference(s): <br>
- [Zhihuiya Patent Image Search API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-zhihuiya-patent-image-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples, shell command examples, and patent-search result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call an external LinkFox/Zhihuiya API using an API key and a user-provided image URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
