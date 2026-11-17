## Description:

Generates agent-optimized llms.txt files for business websites by crawling public pages, filling gaps conversationally, and producing structured markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ngm9](https://clawhub.ai/user/ngm9)

### License/Terms of Use:

MIT

## Use Case:

Business owners, marketers, and developers use this skill to make a public website easier for AI agents to understand and transact with. It crawls public site pages, asks for missing business details, and produces a publishable llms.txt draft for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The crawler may fetch unintended internal or sensitive URLs.

Mitigation: Run it only with contained outbound network access and provide public business website URLs, not private intranet or sensitive application URLs.

Risk: Untrusted page text can influence the generated llms.txt draft.

Mitigation: Review crawl results and the final markdown before publication, and remove unsupported claims or links.

Risk: The generated file may include inaccurate business claims, pricing, team details, or testimonials.

Mitigation: Treat the output as a draft and manually verify public claims, quotes, contact paths, and links before deploying the llms.txt file.

## Reference(s):

- [llms.txt Specification & Examples](references/llms_txt_spec.md)
- [llmstxt.org](https://llmstxt.org)
- [ClawHub Skill Page](https://clawhub.ai/ngm9/skills/llms-txt-generator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown llms.txt content with short conversational guidance and gap reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a final llms.txt draft intended for manual verification before publication.]

## Skill Version(s):

0.1.0 (source: package.json and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
