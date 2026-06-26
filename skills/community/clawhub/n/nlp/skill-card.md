## Description: <br>
Process text with NLP for tokenization, sentiment analysis, entity extraction, summarization, and similarity measurement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to run local command-line text processing tasks, including quick document analysis, sentiment checks, entity extraction, summaries, similarity scoring, and keyword-based classification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running local shell tooling on chosen text or files can expose file contents through terminal output, including extracted emails, URLs, names, or other document details. <br>
Mitigation: Use non-sensitive inputs when possible and handle generated output according to the applicable data handling policy. <br>
Risk: Heuristic NLP results such as sentiment, summaries, classifications, and entity extraction can be incomplete or inaccurate. <br>
Mitigation: Treat outputs as quick analysis aids and review important results before relying on them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xueyetianya/nlp) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads inline text, files, or stdin and writes results to stdout/stderr; stateless.] <br>

## Skill Version(s): <br>
3.4.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
