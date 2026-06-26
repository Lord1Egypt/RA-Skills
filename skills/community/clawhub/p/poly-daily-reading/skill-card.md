## Description: <br>
Generate Guillaume's daily reading list by searching curated sources across AI, LLMs, full-stack dev, anime, horror games, and metal music; it handles deduplication, Obsidian file output, Mission Control ingestion, and weekly or yearly archiving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guillaumemaka](https://clawhub.ai/user/guillaumemaka) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Guillaume uses this skill to generate a daily, deduplicated reading list across curated technical and culture sources, write it into Obsidian, and report delivery through Mission Control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weekly and yearly archiving can delete personal Obsidian reading files after archive creation. <br>
Mitigation: Review the configured Daily Reading paths before use, add a dry-run or confirmation step, and move files to a recoverable trash or archive-staging folder instead of deleting them directly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guillaumemaka/poly-daily-reading) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Obsidian markdown reading list with supporting JSON payloads and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes daily and archive files under the configured Obsidian Daily Reading folder and records read URLs in a JSON cache.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
