## Description: <br>
Image-crawler helps an agent collect images from Baidu and Bing image search using keyword expansion, URL and content deduplication, progress monitoring, and JSON status output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mx2013713828](https://clawhub.ai/user/mx2013713828) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to plan and run keyword-based image collection jobs, monitor JSON progress events, and report download results for local datasets or asset-gathering workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image downloads and deduplication state are written to a local output directory, which can expose private search terms or mix generated files with unrelated content if a shared or sensitive folder is used. <br>
Mitigation: Use a dedicated output directory for each crawl and avoid shared or sensitive folders when search terms are private. <br>
Risk: The persistent .dedup_hashes.json file retains URL and content-hash history across runs. <br>
Mitigation: Delete .dedup_hashes.json in the output folder when retained deduplication history should be removed or reset. <br>


## Reference(s): <br>
- [Customization and interface guide](references/customization.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Files] <br>
**Output Format:** [Markdown guidance with shell commands and JSONL crawler events] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads image files to a local output directory and can maintain persistent deduplication state in that directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
