## Description:

TokenSaver helps agents store, compress, and retrieve Korean and English context to reduce token usage, with async processing, optional fast JSON support, LRU caching, and JVM-free tokenization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dorongss](https://clawhub.ai/user/dorongss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use TokenSaver to compress, persist, search, import, export, and reload bilingual context so an agent can work with shorter retrieved summaries instead of full prior content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic memory indexing and local persistence can duplicate sensitive or regulated data for later retrieval.

Mitigation: Do not store secrets, regulated data, private profile files, or agent instructions; require explicit indexing consent and documented retention before use.

Risk: Auto-sync, backup import, and vector-cache behavior may expand local data exposure before hardening is complete.

Mitigation: Disable those features until URI path validation, pickle removal, and explicit indexing controls are fixed and reviewed.

Risk: Ambiguous install identity can cause users to install an unintended package.

Mitigation: Install only from a verified canonical package name and pinned version that matches the reviewed ClawHub release.

Risk: Prompt templates may steer an agent toward unrelated personal business or health goals.

Mitigation: Review and neutralize bundled prompt templates before deployment in shared or production agent environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dorongss/skills/openviking-korean)
- [TokenSaver API Reference](docs/API_REFERENCE.md)
- [TokenSaver README](README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce compressed context records, search results, backup files, import/export guidance, and installation commands.]

## Skill Version(s):

3.1.0 (source: ClawHub release metadata, clawhub.json, setup.py, openviking_korean/__init__.py; pyproject.toml reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
