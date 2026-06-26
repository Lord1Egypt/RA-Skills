## Description: <br>
Searches Hivemind's curated Web3 marketing knowledge base for practitioner insights, frameworks, playbooks, and case studies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[divine-comedian](https://clawhub.ai/user/divine-comedian) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to retrieve practitioner-backed Web3 marketing intelligence for strategy, go-to-market planning, content creation, competitive research, and project marketing audits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries may disclose private launch, marketing, or strategy details to the configured Hivemind API provider. <br>
Mitigation: Use only with a trusted configured Hivemind API provider and avoid submitting confidential details that should not leave the operating environment. <br>
Risk: Hivemind credentials are sent to the configured endpoint for authentication. <br>
Mitigation: Configure HIVEMIND_API_URL only for the intended provider endpoint and protect HIVEMIND_API_KEY and HIVEMIND_VERCEL_BYPASS as secrets. <br>
Risk: Retrieved practitioner intelligence can be incomplete, stale, or mismatched to a user's specific Web3 marketing context. <br>
Mitigation: Synthesize multiple retrieved results, preserve context such as document type and channel metadata, and review recommendations before using them for launch or strategy decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/divine-comedian/myosin-hivemind) <br>
- [Publisher profile](https://clawhub.ai/user/divine-comedian) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; the CLI can also return formatted text or raw JSON search results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HIVEMIND_API_URL, HIVEMIND_API_KEY, and HIVEMIND_VERCEL_BYPASS credentials; search options include query, persona, relevance threshold, maximum results, intent filtering, objective filtering, reranking, metadata boosting, and raw output.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
