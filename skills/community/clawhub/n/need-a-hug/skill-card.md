## Description:

Need a Hug shifts an agent into warm, lightweight emotional support when a user asks for comfort or shows clear distress, while avoiding therapy, diagnosis, medical care, or crisis-service claims.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lonelymoon87](https://clawhub.ai/user/lonelymoon87)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to give an assistant a conservative comfort posture for moments of overwhelm, shame, loneliness, burnout, grief, or explicit hug requests. It helps the agent slow down, acknowledge the feeling, provide grounding, and return to the task in smaller steps when the user is ready.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad automatic activation can shift the assistant into comfort-oriented support when the user only wanted practical help.

Mitigation: Use explicit return-to-task phrases such as /hug:off or /back-to-work, and keep activation conservative for ordinary task difficulty.

Risk: Users may mistake comfort-oriented responses for therapy, medical advice, emergency services, or crisis care.

Mitigation: Keep responses clearly non-clinical, avoid diagnosis or treatment claims, and direct crisis or imminent-danger situations toward local emergency services or trusted nearby people.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lonelymoon87/skills/need-a-hug)
- [Comfort Protocol](references/comfort-protocol.md)
- [Comfort Language Corpus](references/comfort-language-corpus.md)
- [Counseling-Lite Patterns](references/counseling-lite-patterns.md)
- [Optional Comfort Memory Template](references/memory-template.md)
- [TIME: Worst Things to Say to Someone Who Is Depressed](https://time.com/7291435/worst-thing-to-say-depression-depressed/)
- [Psych Central: What to Say to Someone With Depression](https://psychcentral.com/depression/things-you-should-and-not-say-to-a-depressed-person)
- [NCBI Bookshelf: Motivational Interviewing as a Counseling Style](https://www.ncbi.nlm.nih.gov/books/n/tip35v2/ch3/)
- [SAMHSA: Trauma-Informed Approaches and Programs](https://www.samhsa.gov/mental-health/trauma-violence/trauma-informed-approaches-programs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Natural-language comfort responses in Markdown-compatible text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include optional short grounding prompts, task-return guidance, and localized English or Chinese comfort phrasing.]

## Skill Version(s):

0.3.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
