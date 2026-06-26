## Description: <br>
Generates hand-drawn style knowledge cards by searching topic information, summarizing it, and composing an 804x440 PNG image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[East5RingRoad-kyle](https://clawhub.ai/user/East5RingRoad-kyle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, students, educators, content creators, and training teams use this skill to turn a topic into a visual knowledge card for learning, teaching, presentations, and social sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Topics and generated prompts may be sent to external search and image-generation services. <br>
Mitigation: Avoid sensitive, confidential, personal, or regulated topics unless the external service use is approved. <br>
Risk: Provider API keys are stored in environment variables, and the Pollinations key is included in the image-generation request URL. <br>
Mitigation: Use scoped keys, avoid exposing request URLs in logs, rotate keys if exposed, and run the skill only in trusted environments. <br>
Risk: Generated image files are written to disk, with a default output directory when no output path is supplied. <br>
Mitigation: Specify an explicit output path in a controlled directory and review generated files before sharing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/East5RingRoad-kyle/pollinations-sketch-note) <br>
- [README.md](README.md) <br>
- [INTRO.md](INTRO.md) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Pollinations image API endpoint](https://gen.pollinations.ai/image/{prompt}) <br>


## Skill Output: <br>
**Output Type(s):** [Image, Files, Shell commands] <br>
**Output Format:** [PNG image file with a MEDIA path message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates 804x440 PNG cards; requires Pollinations and Tavily API keys and may call external search and image-generation services.] <br>

## Skill Version(s): <br>
0.0.1 (source: changelog, package.json, release evidence, released 2026-03-11) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
