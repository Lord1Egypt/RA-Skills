## Description: <br>
Build and validate GraphQL queries, mutations, and schemas for work with GraphQL APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and API practitioners use this skill to draft GraphQL queries and mutations, validate or format GraphQL files, extract schema snippets, and optionally introspect trusted GraphQL endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Endpoint introspection makes an outbound network request and can expose schema details from the target service. <br>
Mitigation: Use introspection only with trusted endpoints and avoid private or sensitive internal URLs unless the access is deliberate. <br>
Risk: File-based validation, formatting, and schema extraction read local files provided to the skill. <br>
Mitigation: Pass only GraphQL files that are appropriate for the agent to read. <br>


## Reference(s): <br>
- [Graphql Builder on ClawHub](https://clawhub.ai/ckchzh/graphql-builder) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local GraphQL files and may make outbound POST requests for endpoint introspection when given a URL.] <br>

## Skill Version(s): <br>
3.0.0 (source: evidence release and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
