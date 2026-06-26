# Instagram Collector Skill

## Purpose
Collects Instagram profile data for a given handle using the Apify Instagram Profile Scraper. Extracts follower count, engagement metrics, posting frequency, and top hashtags. This collector feeds into the Marketing Audit Pipeline to populate the Instagram Performance section of the final report.

## Input Schema
```typescript
// Function signature
collectInstagram(handle: string): Promise<InstagramData>

// The handle parameter is the Instagram username without the @ symbol.
// Example: "gymshark" (not "@gymshark")
```

## Output Schema
```typescript
interface InstagramData {
 followers: number;
 posts: number;
 engagementRate: number; // Calculated: (avgLikes + avgComments) / followers * 100
 postingFrequency: string; // e.g. "1.2 posts/day", "3 posts/week", "unknown"
 avgLikes: number;
 avgComments: number;
 topHashtags: string[]; // Up to 10 most-used hashtags from recent posts
 error?: string; // Present only when collector fails
}
```

## API Dependencies
- **API Name:** Apify Instagram Profile Scraper
- **Actor ID:** `apify~instagram-profile-scraper`
- **Endpoint:** `https://api.apify.com/v2/acts/apify~instagram-profile-scraper/runs`
- **Auth:** `APIFY_API_TOKEN` environment variable
- **Cost estimate:** ~$0.005 per run on Apify free/paid tier
- **Rate limits:** Depends on Apify plan; free tier allows limited concurrent runs

## Implementation Pattern

### Data Flow
1. Receive `handle` string from the pipeline
2. Call `apifyService.scrapeInstagramProfile(handle)` which starts an Apify actor run
3. Apify runs asynchronously -- the service polls for completion (timeout: 60s)
4. Fetch the actor's dataset results once complete
5. Map the raw Apify response to the `InstagramData` interface

### Engagement Rate Calculation
```typescript
engagementRate = ((avgLikes + avgComments) / followers) * 100;
```
- If `followers` is 0, set `engagementRate` to 0 to avoid division by zero
- Engagement rate is expressed as a percentage (e.g., 3.5 means 3.5%)

### Posting Frequency Calculation
- Analyze timestamps from the last 30 posts returned by Apify
- Calculate the time span between the oldest and newest post
- Divide the number of posts by the number of days in that span
- Format as a human-readable string:
 - >= 1 post/day: `"X.X posts/day"`
 - < 1 post/day but >= 1/week: `"X posts/week"`
 - < 1 post/week: `"X posts/month"`
 - If no timestamp data available: `"unknown"`

### Top Hashtags Extraction
- Iterate through captions of recent posts
- Extract all `#hashtag` tokens using regex: `/#(\w+)/g`
- Count frequency of each hashtag
- Return the top 10 most frequently used

### Apify Response Mapping
Key fields from Apify's raw output:
- `followersCount` -> `followers`
- `postsCount` -> `posts`
- `latestPosts[].likesCount` -> used for `avgLikes`
- `latestPosts[].commentsCount` -> used for `avgComments`
- `latestPosts[].caption` -> used for hashtag extraction
- `latestPosts[].timestamp` -> used for posting frequency

## Error Handling
- Entire function wrapped in `try/catch`
- On failure, return `EMPTY_INSTAGRAM_DATA` with `error` field set:
 ```typescript
 return { ...EMPTY_INSTAGRAM_DATA, error: 'Instagram data unavailable: <reason>' };
 ```
- Never throw -- always return a valid `InstagramData` object
- Log errors with Winston logger including handle and error details:
 ```typescript
 logger.error('Instagram collector failed', { handle, err });
 ```
- Common failure scenarios:
 - Apify token invalid or expired
 - Actor run timeout (profile too large or Apify overloaded)
 - Profile is private or does not exist
 - Rate limit exceeded on Apify

## Example Usage
```typescript
import { collectInstagram } from '../collectors/instagramCollector';

// Successful collection
const data = await collectInstagram('gymshark');
// Returns:
// {
// followers: 6800000,
// posts: 4520,
// engagementRate: 1.85,
// postingFrequency: "1.3 posts/day",
// avgLikes: 120000,
// avgComments: 5800,
// topHashtags: ["gymshark", "fitness", "gym", "workout", "fitnessmotivation", ...],
// }

// Failed collection (graceful degradation)
const failedData = await collectInstagram('nonexistent_handle_12345');
// Returns:
// {
// followers: 0,
// posts: 0,
// engagementRate: 0,
// postingFrequency: "unknown",
// avgLikes: 0,
// avgComments: 0,
// topHashtags: [],
// error: "Instagram data unavailable: Profile not found"
// }
```

## Notes
- The collector depends on `apifyService.ts` for the actual API communication. The collector handles only data mapping and calculations.
- Apify actor runs are asynchronous. The service layer handles polling. If the run does not complete within 60 seconds, it should be treated as a timeout error.
- This collector is independently testable. In tests, mock `apifyService.scrapeInstagramProfile` to return fixture data.
- Instagram data can be stale -- Apify scrapes public data which may be cached. This is acceptable for audit purposes.
- The `EMPTY_INSTAGRAM_DATA` constant is defined in `src/types/audit.types.ts` and should be imported for fallback returns.
- This collector must never block the pipeline. Even a complete failure returns valid typed data with an error flag, allowing other collectors to proceed.
