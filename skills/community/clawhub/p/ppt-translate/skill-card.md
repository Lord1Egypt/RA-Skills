## Description:

Translate Chinese PowerPoint presentations to English while preserving images, charts, shapes, media, and presentation layout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[birkhoff-china](https://clawhub.ai/user/birkhoff-china)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill to localize Chinese PPTX presentations into English while keeping non-text slide content and business presentation styling intact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Presentation text, speaker notes, and API credentials may be sent to a configured LLM endpoint.

Mitigation: Use only trusted local endpoints or trusted HTTPS providers, and confirm provider data-handling terms before processing confidential decks.

Risk: API keys can be supplied on the command line, where they may appear in shell history or process listings.

Mitigation: Prefer environment-based secret handling and avoid passing API keys directly in command arguments.

Risk: The configured endpoint is arbitrary and may be unreachable or untrusted.

Mitigation: Verify the endpoint URL and model before use, and review generated presentations before sharing them.

## Reference(s):

- [PPT Translation Tool Technical Reference](reference.md)
- [Ollama](https://ollama.com)
- [ClawHub skill page](https://clawhub.ai/birkhoff-china/skills/ppt-translate)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Files, Configuration]

**Output Format:** [Markdown instructions, command-line examples, and generated PPTX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an English PPTX output file and may leave untranslated source text in place when endpoint requests fail.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
