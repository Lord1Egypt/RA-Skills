## Description: <br>
Cleans and repairs TXT ebooks by removing ads, fixing mojibake, normalizing layout, and optionally using LLM-assisted detection for difficult advertising, encoding, and chapter-format issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunfirehw](https://clawhub.ai/user/sunfirehw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to clean TXT ebook files, repair encoding artifacts, remove known or suspected ad text, normalize chapter formatting, and return a cleaned text file with a brief report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can search local TXT files and expose candidate filenames during file selection. <br>
Mitigation: Use direct file paths or narrow searches when possible, and review candidate filenames before selecting a file. <br>
Risk: AI modes may process ebook text through an OpenClaw subagent or configured LLM provider. <br>
Mitigation: Use fast/local rule mode for private, copyrighted, or sensitive books unless LLM processing is acceptable. <br>
Risk: Learned mojibake rules may persist across runs. <br>
Mitigation: Review and delete learned_mojibake_rules.json when cross-run learning is not desired. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sunfirehw/good-txt-to-hwreader) <br>
- [Good-Txt-To-Hwreader Changelog](artifact/CHANGELOG.md) <br>
- [AI Enhancement Design](artifact/AI_ENHANCEMENT_DESIGN.md) <br>
- [Advertisement Patterns](artifact/references/ads_patterns.md) <br>
- [Mojibake Patterns](artifact/references/mojibake_patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Cleaned TXT file plus Markdown report and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports fast, balanced, and thorough modes; AI modes may call an OpenClaw subagent or configured LLM provider.] <br>

## Skill Version(s): <br>
4.1.0 (source: server evidence and changelog, released 2026-03-29) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
