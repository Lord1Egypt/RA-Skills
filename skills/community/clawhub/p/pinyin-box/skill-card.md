## Description:

Pinyin Box helps an agent turn Chinese text, or text extracted from images, into pinyin-grid or mizige handwriting practice sheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanglinzhen](https://clawhub.ai/user/yanglinzhen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate Chinese handwriting practice materials from provided text or from OCR-extracted image text. It guides the agent to clean the input, call the pinyin-box CLI, and return generated PNG or PDF worksheet files with basic character and page information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation uses a broad package specifier and a direct wheel URL, which can make supply-chain review harder.

Mitigation: Install in a dedicated virtual environment or sandbox and use a reviewed, exactly pinned, hash-verified dependency source.

Risk: Images processed for OCR may contain sensitive text.

Mitigation: Treat uploaded images and extracted text as sensitive and avoid retaining or exposing them beyond the worksheet-generation task.

Risk: Passing user-provided text to a CLI can be unsafe if command strings are assembled directly.

Mitigation: Invoke the CLI with structured arguments rather than building a shell command string from user text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yanglinzhen/skills/pinyin-box)
- [pinyin-box 1.0.0 wheel listed in requirements.txt](https://github.com/yanglinzhen/pinyin-box/releases/download/v1.0.0/pinyin_box-1.0.0-py3-none-any.whl)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PNG or PDF worksheet files with concise Markdown status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include output file paths, character counts, and page counts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
