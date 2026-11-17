## Description:

Generates hand-drawn style knowledge-card images by searching and summarizing topics from Wikipedia and Baidu Baike, then rendering them in one of three visual styles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[east5ringroad-kyle](https://clawhub.ai/user/east5ringroad-kyle)

### License/Terms of Use:

MIT-0

## Use Case:

External users, students, educators, content creators, and training teams use this skill to turn a topic or custom detail text into a shareable 804x440 sketch-note PNG for learning, teaching, or knowledge sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Topics, custom detail text, and generated prompts may be sent to third-party services.

Mitigation: Use only non-sensitive topics and review provider data-handling terms before deployment.

Risk: The security evidence reports an unused API key requirement and limited disclosure of external providers and data sent.

Mitigation: Use revocable low-quota API keys, remove unused key requirements, and document provider data flows before production use.

Risk: Intermediate image files are written before the final PNG is produced.

Mitigation: Run the skill in a controlled output directory and confirm temporary-file cleanup succeeds before sharing generated media.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/east5ringroad-kyle/skills/pollinations-sketch-note)
- [Publisher profile](https://clawhub.ai/user/east5ringroad-kyle)
- [Artifact README](artifact/README.md)
- [Artifact detailed introduction](artifact/INTRO.md)
- [Pollinations image generation endpoint](https://gen.pollinations.ai/image/{prompt})
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Files, Images, Shell commands]

**Output Format:** [PNG image file with a MEDIA path emitted to the agent conversation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs fixed-size 804x440 cards with an overlaid title, summary text, signature, and timestamp.]

## Skill Version(s):

0.0.1 (source: changelog and package.json, released 2026-03-11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
