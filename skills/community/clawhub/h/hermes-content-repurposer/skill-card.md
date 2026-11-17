## Description:

Takes one long-form piece of content and repurposes it into Twitter threads, LinkedIn posts, newsletter editions, and short video scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcvanstad](https://clawhub.ai/user/marcvanstad)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, agencies, podcasters, and video teams use this skill to turn long-form source material into platform-specific social posts, newsletters, and short video scripts. It supports configurable brand voice, batch processing, source watching, and quality checks before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled runs, RSS watching, or publishing integrations may process or publish content without the operator's intended review cadence.

Mitigation: Enable scheduling, source watching, and publishing integrations only after confirming they are needed, and keep generated drafts in a review workflow before publication.

Risk: Remote source URLs can introduce untrusted or inaccurate content into generated drafts.

Mitigation: Use trusted source URLs and verify generated quotes, links, and claims against the original content before publishing.

Risk: The artifact references requirements and scripts that are not included, so dependency and runtime behavior cannot be fully verified from the provided files.

Mitigation: Review and pin dependencies and inspect any runtime scripts before installing or enabling automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marcvanstad/skills/hermes-content-repurposer)
- [README](README.md)
- [Repurpose configuration](reference/config/repurpose.yaml)
- [Source watcher configuration](reference/config/sources.yaml)
- [Narrative extraction prompt](reference/prompts/extract_narrative.yaml)
- [Twitter thread prompt](reference/prompts/twitter_thread.yaml)
- [LinkedIn post prompt](reference/prompts/linkedin_post.yaml)
- [Quality checks template](reference/templates/quality_checks.yaml)
- [Twitter thread template](reference/templates/twitter_thread/default.yaml)
- [LinkedIn thought leader template](reference/templates/linkedin/thought_leader.yaml)
- [Newsletter weekly digest template](reference/templates/newsletter/weekly_digest.yaml)
- [TikTok video script template](reference/templates/video_script/tiktok.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, configuration, guidance]

**Output Format:** [Platform-specific drafts, structured narrative JSON, markdown content, YAML configuration guidance, and script outlines.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are organized by platform and constrained by configurable character limits, duration targets, brand voice settings, and quality checks.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
