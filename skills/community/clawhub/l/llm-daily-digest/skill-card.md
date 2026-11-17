## Description:

Generates a Chinese Markdown digest of the day's LLM and AI developments by gathering, deduplicating, ranking, and summarizing public updates from official vendor blogs, GitHub, arXiv, Hugging Face, Papers With Code, Hacker News, X/Twitter, and Chinese AI media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flowbywind](https://clawhub.ai/user/flowbywind)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate a daily Chinese LLM news brief covering model releases, product updates, research papers, open-source projects, and industry events. It can be run from an agent session or triggered by a separately configured recurring automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill browses many public web sources, so report quality can be affected by unavailable pages, access restrictions, or transient source failures.

Mitigation: Review the collection statistics and source coverage notes in each digest before relying on the report.

Risk: Broad AI-news prompts may trigger the skill and cause the agent to browse public sources and save a local Markdown report.

Mitigation: Use explicit trigger wording when requesting daily digests and confirm saved files under ~/.openclaw/workspace/digests.

Risk: Recurring daily operation is not automatic unless the user configures a separate cron job.

Mitigation: Configure and review the external cron trigger separately, including the prompt text and schedule.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flowbywind/skills/llm-daily-digest)
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills)
- [OpenClaw cron jobs documentation](https://docs.openclaw.ai/automation/cron-jobs)
- [OpenAI News](https://openai.com/news/)
- [Anthropic News](https://www.anthropic.com/news)
- [Google AI Blog](https://blog.google/technology/ai/)
- [DeepMind Blog](https://deepmind.google/discover/blog/)
- [Meta AI Blog](https://ai.meta.com/blog/)
- [GitHub Trending](https://github.com/trending)
- [arXiv recent cs.CL papers](https://arxiv.org/list/cs.CL/recent)
- [Hugging Face trending models](https://huggingface.co/models?sort=trending)
- [Papers With Code latest papers](https://paperswithcode.com/latest)
- [Hacker News](https://news.ycombinator.com/)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files, Guidance]

**Output Format:** [Structured Chinese Markdown digest plus a session reply with the report path, three highlights, and collection statistics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves reports under ~/.openclaw/workspace/digests/YYYY-MM-DD.md and uses versioned suffixes instead of overwriting an existing daily report.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
