## Description:

Retrieves recent Article or Review records from PubMed for a named journal and saves PMIDs, titles, and abstracts as structured JSON for downstream summarization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenghan66](https://clawhub.ai/user/chenghan66)

### License/Terms of Use:

MIT-0

## Use Case:

Medical and life science researchers use this skill to monitor recent Article or Review publications from a named journal and collect PMIDs, titles, and abstracts for downstream AI summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted journal name can make the skill write outside its disclosed output folder and overwrite local files.

Mitigation: Use trusted journal names only, sanitize output filenames, and constrain the output directory before broad use.

Risk: The skill performs outbound PubMed requests and writes local JSON archives.

Mitigation: Install only from a trusted publisher and run it in an environment with filesystem and network access limited to the intended collection task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenghan66/skills/journal-intel-extractor)
- [PubMed](https://pubmed.ncbi.nlm.nih.gov/)

## Skill Output:

**Output Type(s):** [JSON, Files, Text]

**Output Format:** [JSON file with PMID, english_title, and abstract records, plus console status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local archives under ~/Documents/Journal_Intel/ and retrieves up to 50 PubMed results per run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
