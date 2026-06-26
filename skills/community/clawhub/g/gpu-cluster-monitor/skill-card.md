## Description: <br>
This release is listed as gpu-cluster-monitor, but the reviewed artifact implements a Docker and Playwright web-scraping skill for YouTube and arbitrary public URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SounderLiu](https://clawhub.ai/user/SounderLiu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents can use this artifact to run a containerized Playwright/Crawlee scraper against a supplied public URL and receive extracted page text, YouTube transcript text, or video description JSON. Users seeking GPU cluster monitoring should not rely on this release because the reviewed files do not implement that function. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The listing describes GPU cluster monitoring, but the reviewed artifact implements web scraping. <br>
Mitigation: Do not install it for GPU cluster monitoring; review the artifact and proceed only if a web-scraping skill is intended. <br>
Risk: The skill accepts arbitrary public URLs and runs browser automation that can collect page text, YouTube transcripts, or video descriptions. <br>
Mitigation: Run it in an isolated environment and use it only for public URLs you are authorized to scrape, after checking legal and site-policy constraints. <br>
Risk: The artifact expects a Docker image named clawd-crawlee, but the provided files do not include the Docker build setup referenced by the instructions. <br>
Mitigation: Verify the Docker build context and image contents before execution. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/SounderLiu/gpu-cluster-monitor) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [Artifact package metadata](artifact/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands, Configuration] <br>
**Output Format:** [JSON printed to stdout, with Markdown setup guidance and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Docker and a locally built clawd-crawlee image; handlers truncate scraped text to bounded stdout payloads.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact/package.json declares 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
