## Description:

ResonanceEngine analyzes conversation text for engagement, trust, decision-readiness, and style-match signals, then returns response guidance and conversion-oriented predictions for chatbot workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcools1977](https://clawhub.ai/user/jcools1977)

### License/Terms of Use:

MIT

## Use Case:

Developers and teams building chatbot workflows can use this skill to analyze conversation history and produce response-tuning guidance, yield predictions, and prompt text for the next bot response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation analytics and personalization may be used without clear user awareness.

Mitigation: Use only in contexts where users are clearly told that conversation analytics and personalization may be used.

Risk: Generated prompt-tuning text can steer bot behavior in sensitive or high-pressure sales contexts.

Mitigation: Require policy review before sensitive-domain or high-pressure sales use, and keep generated prompt text out of privileged system prompts unless it is reviewed and constrained.

Risk: Recommendations may include scarcity or social-proof tactics that need factual support.

Mitigation: Verify scarcity and social-proof claims before using them in customer-facing responses.

Risk: Unpinned or unreviewed installation could introduce unexpected code changes.

Mitigation: Install from a pinned, reviewed release in an isolated environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jcools1977/skills/openpaw)
- [Publisher Profile](https://clawhub.ai/user/jcools1977)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [Python objects, dictionaries, human-readable summaries, and prompt-tuning text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally without API-key or MCP dependencies according to discovery signals.]

## Skill Version(s):

0.1.0 (source: frontmatter, pyproject.toml, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
