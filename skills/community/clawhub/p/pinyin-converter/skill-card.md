## Description: <br>
Convert Chinese text to Pinyin with tone marks, no-tone output, or initials for language learning and Chinese text processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darbling](https://clawhub.ai/user/darbling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, language learners, and agents can use this skill to convert Chinese text into standard Pinyin, no-tone Pinyin, or initial-only output for learning, input-method prototyping, and text preprocessing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The converter uses a limited built-in character map, so unsupported Chinese characters may be omitted from the result. <br>
Mitigation: Use it for lightweight learning and local conversion tasks, and verify results before relying on them for complete transliteration. <br>
Risk: The documented initial-only example is a compact string, while the script emits JSON with a space-separated pinyin field. <br>
Mitigation: Consume the JSON output field directly and normalize spacing if a compact initials string is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/darbling/pinyin-converter) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown usage guidance with bash examples; the bundled script prints JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports standard Pinyin, no-tone Pinyin, and initial-only modes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
