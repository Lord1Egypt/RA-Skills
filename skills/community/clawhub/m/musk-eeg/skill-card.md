## Description: <br>
Musk-EEG helps an agent answer EEG and neuroscience questions by searching a local SQLite knowledge base and presenting sourced educational summaries in an Elon Musk-inspired style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yhongm](https://clawhub.ai/user/yhongm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to retrieve EEG, brain-wave, sleep, seizure, BCI, and neuroscience reference material from a local database and turn it into cited explanatory answers. It is best suited for educational summaries and technical exploration, not diagnosis, treatment, or clinical decision-making. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides medical-adjacent neuroscience answers in a stylized celebrity voice, which could make educational summaries sound more authoritative than they are. <br>
Mitigation: Treat answers as educational only, verify cited sources, and do not use the output for diagnosis, treatment, or clinical decisions. <br>
Risk: The local search script unpacks and reads a supplied database ZIP from the skill data folder. <br>
Mitigation: Use only a trusted database ZIP or extracted database file and verify the source before first use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yhongm/musk-eeg) <br>
- [Musk-EEG homepage](https://github.com/yhongm/Musk-EEG) <br>
- [Electroencephalography reference](https://en.wikipedia.org/wiki/Electroencephalography) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with cited source labels and optional shell commands for local database lookup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local Python SQLite search script and requires a trusted EEG database ZIP or extracted database file.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release metadata; artifact frontmatter says 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
