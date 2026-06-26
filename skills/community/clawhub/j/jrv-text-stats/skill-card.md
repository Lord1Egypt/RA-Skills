## Description: <br>
Analyze text files for word count, character count, line count, sentence count, reading time, speaking time, readability scores (Flesch Reading Ease, Flesch-Kincaid Grade Level), and vocabulary statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, editors, and other external users use this skill to analyze local text files or stdin for counts, readability metrics, vocabulary statistics, and estimated reading or speaking time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads any local file path supplied by the user and may expose derived details such as counts or the longest word. <br>
Mitigation: Run it only on text the user is comfortable analyzing or disclosing in summarized form. <br>
Risk: Source provenance is unavailable for this release. <br>
Mitigation: Review the artifact files and security evidence before using it in environments that require verified source provenance. <br>
Risk: Readability and syllable metrics are heuristic and English-optimized. <br>
Mitigation: Treat readability scores and difficulty labels as approximate indicators rather than authoritative measurements. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text or JSON statistics, with Markdown guidance and shell command examples for agent use] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports multiple input files, stdin input, compact summaries, UTF-8 text with encoding-error fallback, and heuristic English-optimized syllable counting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
