## Description: <br>
Checks primer sequences with local Tm, GC content, hairpin, and self-dimer heuristics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, lab automation users, and bioinformatics practitioners use this skill for a lightweight local pre-check of qPCR, sequencing, or mutagenesis primer sequences before deeper validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release text overstates off-target amplification and BLAST support that the local script does not implement. <br>
Mitigation: Use the output only as a lightweight local primer-quality screen, and require independent off-target, BLAST, template-matching, and wet-lab validation before design decisions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text CLI report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports Tm, GC content, and heuristic hairpin/self-dimer flags for forward and reverse primer sequences; BLAST, template matching, and off-target analysis are not implemented.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
