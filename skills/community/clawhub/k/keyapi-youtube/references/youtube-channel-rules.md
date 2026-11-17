# YouTube Channel Module Rules

## 1. Module Scope

Use this module for YouTube channel description, channel videos, channel search, and channel ID/URL conversion.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## 2. Channel identity conversion and resolution

- Documentation: `https://docs.keyapi.ai/en/youtube/get_channel_id.md`
- Documentation: `https://docs.keyapi.ai/en/youtube/get_channel_id_from_url.md`
- Documentation: `https://docs.keyapi.ai/en/youtube/get_channel_url.md`
- Purpose: Resolve channel names, URLs, handles, and channel IDs into the form needed by downstream endpoints.

### Best Suited For

- channel URL to ID conversion
- handle/name resolution
- normalizing channel identifiers
- preparing channel video workflows

### Routing Rules

- Use channel ID from URL when the user provides a channel URL.
- Use get channel ID when the user provides a channel name/handle according to docs.
- Use channel URL from channel ID when the user needs handle/URL output.
- Do not call conversion endpoints when the required identifier is already known.

## 3. Channel profile baseline

- Documentation: `https://docs.keyapi.ai/en/youtube/get_channel_description.md`
- Purpose: Retrieve detailed channel profile information.

### Best Suited For

- channel reports
- creator validation
- subscriber/view/join-date/social link context when returned

### Routing Rules

- Use after resolving channel ID/URL when identity is uncertain.
- Keep channel profile facts separate from video-level performance facts.

## 4. Channel video catalog

- Documentation: `https://docs.keyapi.ai/en/youtube/get_channel_videos.md`
- Purpose: Retrieve videos from a channel.

### Best Suited For

- creator content audit
- channel catalog collection
- recent upload review
- video candidates for enrichment

### Routing Rules

- Use continuation tokens exactly as documented.
- Enrich only selected videos with video information/comments unless a broad audit is approved.

## 5. Channel discovery search

- Documentation: `https://docs.keyapi.ai/en/youtube/search_channel.md`
- Documentation: `https://docs.keyapi.ai/en/youtube/search_channels.md`
- Purpose: Search YouTube channels.

### Best Suited For

- creator/channel discovery
- competitor channel research
- channel shortlist creation

### Routing Rules

- Use channel search when the target channel is unknown.
- After selecting candidates, use channel description and channel videos for enrichment.

## 6. Common Workflows

- Channel report: channel resolution -> channel description -> channel videos -> selected video detail/comments.
- Channel discovery: search channels -> channel description for candidates -> channel videos for selected channels.
- Identifier normalization: URL/name/ID conversion -> downstream channel or video workflow.
