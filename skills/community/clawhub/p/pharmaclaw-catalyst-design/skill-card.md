## Description:

Organometallic catalyst recommendation and novel ligand design for drug synthesis reactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cheminem](https://clawhub.ai/user/cheminem)

### License/Terms of Use:

MIT-0

## Use Case:

Medicinal chemists, process chemists, and chemistry automation agents use this skill to rank organometallic catalysts for synthesis steps and generate ligand variants for optimization or downstream IP review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Catalyst and ligand suggestions may be chemically incomplete or unsuitable for a specific substrate, scale, safety profile, or regulatory context.

Mitigation: Use the output as decision support and require expert chemistry review before laboratory use or downstream automation.

Risk: The ligand designer depends on RDKit and may fail or produce limited variants if RDKit is missing, unpinned, or installed from an untrusted source.

Mitigation: Install RDKit from a trusted, pinned source in a controlled Python environment before running ligand-design workflows.

Risk: Optional output paths for JSON or image files could write to unintended locations if untrusted paths are passed through automation.

Mitigation: Use explicit, controlled output directories and avoid passing untrusted file paths into the scripts.

Risk: Broad trigger terms and chaining to other chemistry or IP agents can amplify incorrect recommendations.

Mitigation: Review intermediate recommendations before chaining them into retrosynthesis, patent, or other automated workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cheminem/skills/pharmaclaw-catalyst-design)
- [Catalyst database](references/catalyst_database.json)
- [Suzuki coupling review DOI](https://doi.org/10.1021/cr00039a007)
- [dppf palladium catalyst DOI](https://doi.org/10.1002/anie.199510311)
- [SPhos palladium catalyst DOI](https://doi.org/10.1021/ja0474332)
- [XPhos palladium catalyst DOI](https://doi.org/10.1021/ja052551p)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON-producing Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce JSON recommendation results and optional ligand structure image files when drawing is requested.]

## Skill Version(s):

1.0.0 (source: release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
