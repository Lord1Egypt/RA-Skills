## Description:

Searches a local memory index and returns top hits for Telegram /mem queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trumppo](https://clawhub.ai/user/trumppo)

### License/Terms of Use:


## Use Case:

External users or agents use this skill to query a local memory index, return top hits with paths and headers, and briefly summarize results when helpful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on local scripts that are not bundled with the artifact to index and search memory data.

Mitigation: Review and control scripts/index-memory.py and scripts/search-memory.py in the deployment before allowing execution.

Risk: The memory index may include private chats, credentials, or business data without a defined data scope.

Mitigation: Limit the indexed data scope, restrict index access, and avoid indexing secrets or sensitive records unless explicitly approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/trumppo/skills/mem)
- [ClawHub publisher profile](https://clawhub.ai/user/trumppo)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text summaries with command-oriented guidance and search-result paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns top hits with paths and headers; may summarize briefly.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
