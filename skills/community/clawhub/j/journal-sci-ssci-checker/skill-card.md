## Description: <br>
Checks whether psychology academic journals are indexed by SCI or SSCI to help evaluate literature quality and filter eligible journal articles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jiaqi-Guo-0114](https://clawhub.ai/user/Jiaqi-Guo-0114) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, reviewers, and corpus builders use this skill to check whether a non-preprint psychology journal appears in a local SCI/SSCI journal list before downstream paper quality assessment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled journal list can become stale or incomplete relative to official SCI/SSCI records. <br>
Mitigation: Confirm consequential journal-status decisions directly in official Web of Science or Journal Citation Reports sources and update the local list on a regular review cycle. <br>
Risk: Fuzzy journal-title matching can select the wrong journal when titles are abbreviated, renamed, or similar. <br>
Mitigation: Review the matched journal name and index classification before relying on a PASS or FAIL result. <br>


## Reference(s): <br>
- [Bundled journal list](data/journals.txt) <br>
- [Web of Science Master Journal List](https://mjl.clarivate.com/) <br>
- [Journal Citation Reports](https://jcr.clarivate.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON-style lookup result with concise text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a bundled journal list and fuzzy title matching; not a live database query.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
