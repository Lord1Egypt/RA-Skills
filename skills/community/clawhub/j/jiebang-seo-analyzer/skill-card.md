## Description: <br>
Extracts webpage metadata and runs SEO health checks for a supplied public URL, including title, description, Open Graph and Twitter Card data, canonical links, scores, and optimization suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiebang-tools](https://clawhub.ai/user/jiebang-tools) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and website operators use this skill to inspect public webpages for SEO metadata and practical optimization issues. It is suited for extracting page tags, checking common SEO health signals, and returning structured suggestions for improvement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-supplied URLs are sent to the third-party jiebang.site service. <br>
Mitigation: Use the skill only with public URLs that are acceptable to share with that service, and avoid internal, private, authenticated, or token-containing URLs. <br>
Risk: The skill uses an admin-labeled credential for requests to the remote service. <br>
Mitigation: Replace the credential with a narrowly scoped read-only token before deployment. <br>
Risk: The third-party URL processing boundary is not clearly disclosed in the artifact text. <br>
Mitigation: Disclose that submitted URLs are processed by jiebang.site before users rely on the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiebang-tools/jiebang-seo-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/jiebang-tools) <br>
- [Jiebang service endpoint](https://www.jiebang.site) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON responses containing extracted metadata, SEO scores, checks, issue messages, and suggestions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on the remote service response and the accessibility of the submitted URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
