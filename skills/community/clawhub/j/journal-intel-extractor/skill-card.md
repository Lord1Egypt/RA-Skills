## Description: <br>
Fetches recent PubMed articles or reviews for a selected journal, extracts PMIDs, titles, and abstracts, and saves structured JSON for AI-assisted literature summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenghan66](https://clawhub.ai/user/chenghan66) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, clinicians, science communicators, and agent workflows use this skill to monitor recent PubMed-indexed journal updates and collect article abstracts for downstream review or AI-assisted summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts PubMed and may expose queried journals or research topics through network requests. <br>
Mitigation: Use it only in environments where outbound PubMed access is acceptable and the queried topics are appropriate to disclose to that service. <br>
Risk: Article abstracts are saved locally under ~/Documents/Journal_Intel and may reveal sensitive research interests on shared machines. <br>
Mitigation: Review file permissions and periodically delete archived JSON files when the collected topics should not persist. <br>
Risk: Unpinned Python dependencies can change behavior over time. <br>
Mitigation: Pin and maintain requests, beautifulsoup4, and lxml in the deployment environment when reproducibility or parser security matters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chenghan66/journal-intel-extractor) <br>
- [Publisher Profile](https://clawhub.ai/user/chenghan66) <br>
- [PubMed](https://pubmed.ncbi.nlm.nih.gov/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, guidance] <br>
**Output Format:** [Console status text and local JSON files containing article metadata and abstracts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes dated journal JSON archives under ~/Documents/Journal_Intel when results are found.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
