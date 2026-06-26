## Description: <br>
Podwise helps agents use the Podwise CLI to find, process, summarize, translate, research, and export podcast or audio insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saitowu](https://clawhub.ai/user/saitowu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to search podcasts, inspect followed shows and listening history, retrieve transcript-grounded summaries, create notes, generate recaps, research topics, debate episode claims, and build language-learning materials through the Podwise CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Podwise CLI can access Podwise account data, listening and reading history, selected transcripts, and local media chosen for processing. <br>
Mitigation: Install and run the skill only if the user trusts the Podwise CLI, and confirm processing or export actions before sending local media or account-derived content. <br>
Risk: The installation reference includes a curl-piped shell installer. <br>
Mitigation: Prefer Homebrew or a reviewed release binary, and inspect installer scripts before execution. <br>
Risk: API keys and account configuration can be exposed through shared terminals or copied configuration paths. <br>
Mitigation: Keep API keys out of shared terminals, use the browser authorization flow where possible, and protect the Podwise config file. <br>
Risk: taste.md and generated workflow files may contain personal preferences, listening patterns, summaries, or exported episode content. <br>
Mitigation: Avoid storing unrelated sensitive notes in taste.md, review generated file paths and export destinations, and do not share generated files without checking their contents. <br>


## Reference(s): <br>
- [ClawHub Podwise release page](https://clawhub.ai/saitowu/podwise) <br>
- [Podwise homepage](https://podwise.ai) <br>
- [Podwise CLI reference](references/cli.md) <br>
- [Podwise installation reference](references/installation.md) <br>
- [Podwise documentation](https://docs.podwise.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, CLI command snippets, parsed JSON results when requested, and optional local files such as notes, reports, CSV, Anki TSV, SRT, or VTT.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or write taste.md and workflow output files in the current working directory; Podwise CLI calls can access account history, selected transcripts, and local media selected by the user.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
