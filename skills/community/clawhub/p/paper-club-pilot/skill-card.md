## Description:

Paper Club Pilot helps research groups prepare reading-club or lab-seminar materials, capture authorized meeting notes, and distill decisions, action items, and open questions into an academic knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j-levee](https://clawhub.ai/user/j-levee)

### License/Terms of Use:

MIT-0

## Use Case:

Research groups, lab seminar organizers, and reading club facilitators use this skill to curate pre-meeting readings, generate discussion kits, capture authorized Tencent Meeting notes, and archive structured meeting outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can process sensitive meeting transcripts, participant-linked action items, summaries, and research-group topic profiles.

Mitigation: Confirm participant and group consent before use, restrict access to authorized meeting data, and review summaries before archiving them in the academic knowledge base.

Risk: Meeting capture depends on user authorization for Tencent Meeting smart notes or transcripts.

Mitigation: Obtain authorization before pulling meeting data; when authorization is unavailable, use the documented fallback of user-provided notes.

Risk: Usage-derived method-tag logging is disclosed as enabled after installation unless the user opts out.

Mitigation: Tell users they can disable local method-tag logging with the documented opt-out phrase before using the skill in sensitive settings.

Risk: Knowledge-base distillation organizes meeting outcomes but does not verify the truth of research claims.

Mitigation: Route paper factuality or claim-checking questions to an appropriate fact-checking workflow before treating conclusions as validated research findings.

## Reference(s):

- [Coverage Matrix](artifact/references/coverage.md)
- [ClawHub Skill Page](https://clawhub.ai/j-levee/skills/paper-club-pilot)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries, discussion kits, action-item lists, and structured knowledge-base entry guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include recommended papers, meeting agenda text, discussion questions, decisions, disputes, action items, unresolved questions, and a meeting summary for user confirmation before archiving.]

## Skill Version(s):

2.0.1 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
