## Description: <br>
A bilingual Chinese-English searchable library that helps agents answer questions about Machiavelli by returning sourced original passages rather than analysis or advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niflhum](https://clawhub.ai/user/niflhum) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and agents use this skill to locate Machiavelli-related passages in Chinese and English, cite the work and chapter or letter, and avoid unsourced paraphrase. It is intended for source lookup and quotation support, not for persona simulation or strategic advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The released artifact includes search logic and indexes but not the full original text library. <br>
Mitigation: Install the referenced library content before use, validate the expected files, and report no match rather than fabricating a passage when content is missing. <br>
Risk: Quoted or indexed passages may be incomplete, mistranslated, or tied to uncertain source status. <br>
Mitigation: Return citations with each passage, prefer public-domain source material when available, and preserve uncertainty notes such as missing public-domain letter sources. <br>
Risk: Fallback search executes a local shell command over the library directory. <br>
Mitigation: Run the provided search command only against local skill files and keep user-supplied keywords as search terms rather than executable shell fragments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/niflhum/machiavelli-library) <br>
- [Skill-referenced library content repository](https://github.com/niflhum/machiavelli-library.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with cited passages and optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the most relevant passages with work and chapter or letter citations; local grep search can be used as a fallback when indexes are insufficient.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
