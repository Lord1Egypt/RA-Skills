## Description:

Processes text for tokenization, sentiment analysis, entity extraction, summarization, similarity scoring, and classification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to perform local command-line text analysis on supplied text or files, including word counts, simple sentiment, entity extraction, extractive summaries, similarity scores, and keyword classification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary reports that one summarization option can be abused to run arbitrary shell commands.

Mitigation: Review before installing and run only in a constrained environment until --ratio validates numeric input and passes it to AWK as data.

Risk: The server security guidance says JSON output should be treated as untrusted until proper escaping is implemented.

Mitigation: Do not pipe --json output into trusted automation without independent validation or escaping.

Risk: The server security guidance warns against feeding confidential or regulated documents unless local processing is approved.

Mitigation: Use only approved local-processing environments for sensitive documents and avoid supplying confidential text otherwise.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/nlp)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written to stdout or stderr; the skill is documented as stateless and processes provided text, files, or stdin locally.]

## Skill Version(s):

3.4.2 (source: server release metadata; artifact frontmatter says 3.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
