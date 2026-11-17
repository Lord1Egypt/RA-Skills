## Description:

Get what is said in YouTube videos and Shorts, TikToks and Instagram reels as text, for one link or a creator's latest or most-viewed videos, then summarize it, pull hooks, claims and quotes, or repurpose it into posts and scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mesmerlord](https://clawhub.ai/user/mesmerlord)

### License/Terms of Use:

MIT-0

## Use Case:

People who share video links can retrieve transcripts and use them to understand what was said, check claims and quotes, or create summaries and reusable drafts. The skill can also gather videos from a creator's account for comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests send selected video links and creator identifiers to LurkAPI and consume account credits.

Mitigation: Keep the API key out of chat and review per-call and batch costs before making requests.

Risk: Transcripts contain spoken words but not on-screen visuals, and auto-captions can mishear names or numbers.

Mitigation: Check important claims and uncertain wording against the original video, and do not treat a transcript as a description of its visuals.

## Reference(s):

- [YouTube transcript API documentation](https://lurkapi.com/docs/youtube/transcript.md)
- [TikTok transcript API documentation](https://lurkapi.com/docs/tiktok/transcript.md)
- [TikTok video API documentation](https://lurkapi.com/docs/tiktok/video.md)
- [Instagram media transcript API documentation](https://lurkapi.com/docs/instagram/media-transcript.md)
- [YouTube channel videos API documentation](https://lurkapi.com/docs/youtube/channel-videos.md)
- [YouTube channel Shorts API documentation](https://lurkapi.com/docs/youtube/channel-shorts.md)
- [TikTok profile videos API documentation](https://lurkapi.com/docs/tiktok/profile-videos.md)
- [Instagram user reels API documentation](https://lurkapi.com/docs/instagram/user-reels.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Transcript text and Markdown summaries, analyses, quotes, and repurposed drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes timestamps when available; content depends on the requested video and available captions.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
