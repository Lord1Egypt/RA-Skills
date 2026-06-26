## Description: <br>
Searches multiple torrent index sources for movie magnet links and returns ranked results with quality, size, seed count, source, and magnet link details. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[beancookie](https://clawhub.ai/user/beancookie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search for movie-related magnet links across torrent search providers for lawful personal learning and research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Torrent search results and magnet links can point to copyrighted or otherwise unauthorized material. <br>
Mitigation: Use the skill only for material the user has a legal right to access, and review each result before using any magnet link. <br>
Risk: Returned magnet links are untrusted external content. <br>
Mitigation: Treat links as untrusted, avoid automatic download workflows, and inspect results before passing them to a torrent client. <br>
Risk: The security review reports under-disclosed external searches and unsafe HTTPS handling. <br>
Mitigation: Keep the skill in manual review, disclose contacted providers before deployment, and prefer a version that keeps HTTPS certificate validation enabled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/beancookie/magnet-search) <br>
- [Publisher profile](https://clawhub.ai/user/beancookie) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or JSON search results, with command-line usage guidance and magnet link records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may include source names, quality labels, file sizes, seed and peer counts, upload dates, info hashes, and magnet links.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
