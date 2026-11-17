## Description:

GuanXing provides Chinese metaphysics readings through a hosted API, including BaZi, daily fortune, crypto fortune, Feng Shui, Tarot, I-Ching divination, dream interpretation, name scoring, compatibility matching, and zodiac analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doggychip](https://clawhub.ai/user/doggychip)

### License/Terms of Use:

MIT-0

## Use Case:

External users and OpenClaw developers use GuanXing to route metaphysics requests to the GuanXing API for birth-chart, fortune, Feng Shui, Tarot, I-Ching, dream, name, compatibility, zodiac, and crypto fortune readings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends personal reading details such as birth dates, names, dreams, relationship details, and questions to the GuanXing service.

Mitigation: Use only when the user understands and accepts that data transfer, and avoid entering sensitive secrets or unnecessary personal details.

Risk: Fortune, crypto, health, or relationship readings could be mistaken for professional advice.

Mitigation: Present outputs as metaphysical or entertainment-oriented guidance, not as financial, medical, or legal advice.

Risk: Optional MCP or publishing commands from the documentation may execute npm packages.

Mitigation: Pin and verify npm package versions before using optional npm-based commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/doggychip/skills/guanxing)
- [GuanXing API documentation](https://heartai.zeabur.app)
- [GuanXing MCP npm package](https://www.npmjs.com/package/@guanxing1/mcp-server)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUANXING_API_KEY and sends user-provided reading details to external HTTPS API endpoints.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
