## Description:

OpenVid helps an agent request branded motion graphics explainer videos from prompt text and an optional public URL through the OpenVid paid video-generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aklo360](https://clawhub.ai/user/aklo360)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to create branded explainer videos by submitting a concise prompt, an optional public brand URL, and a desired duration to OpenVid. It is intended for paid, agent-mediated video generation workflows that can handle x402 payment authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and submitted URLs are sent to the OpenVid service, and URLs may be fetched for brand extraction.

Mitigation: Submit only public URLs and non-sensitive prompt text.

Risk: Each generation request can require payment, and pricing differs between the shorter table in SKILL.md and the longer pricing table in README.md.

Mitigation: Verify the amount returned by the 402 payment response before authorizing payment.

## Reference(s):

- [OpenVid Skill on ClawHub](https://clawhub.ai/aklo360/skills/openvid)
- [OpenVid Website](https://openvid.app)
- [OpenVid API Gateway](https://gateway.openvid.app)
- [Create Video](https://openvid.app/create)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with HTTP request examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance describes paid x402 API use, public URL submission, video job polling, and payment-response verification.]

## Skill Version(s):

1.0.7 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
