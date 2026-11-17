## Description:

Corrects Chinese text with pycorrector, KenLM, and optional MacBERT refinement to address typos, grammar, punctuation, and wording issues in pasted text or text files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangminrui2022](https://clawhub.ai/user/wangminrui2022)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to correct Chinese text pasted into an agent workflow or stored in .txt files. It supports single text inputs, individual files, and folder-level batch correction when the user requests it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or update Python packages and download large model files at runtime.

Mitigation: Run it in an isolated disposable environment, review dependency sources, and pin dependencies before production use.

Risk: The skill can batch-process local files and folders and write corrected copies.

Mitigation: Limit execution to an explicit working directory, avoid sensitive drafts, and review corrected outputs before replacing originals.

Risk: The skill creates persistent logs and may display snippets of processed text.

Mitigation: Review logging behavior, clear logs when needed, and avoid confidential text until logging controls are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangminrui2022/skills/llm-text-correct)
- [MacBERT4CSC model](https://huggingface.co/shibing624/macbert4csc-base-chinese)
- [Chinese KenLM model](https://huggingface.co/shibing624/chinese-kenlm-klm)

## Skill Output:

**Output Type(s):** [text, files, shell commands, guidance]

**Output Format:** [Corrected Chinese text, optional correction details, and corrected .txt file outputs for file or folder inputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create corrected copies next to source files or in a corrected output folder.]

## Skill Version(s):

1.2.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
