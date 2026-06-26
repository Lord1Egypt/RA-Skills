# Paragraph OpenClaw Skill

[![License: ISC](https://img.shields.io/badge/License-ISC-blue.svg)](https://opensource.org/licenses/ISC)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-ff6b6b)](https://github.com/openclaw/openclaw)
[![Paragraph API](https://img.shields.io/badge/Paragraph-API-00c3ff)](https://paragraph.com/docs/api-reference)
[![Node.js 19+](https://img.shields.io/badge/Node.js-19%2B-green)](https://nodejs.org)

OpenClaw skill for interacting with [Paragraph.com](https://paragraph.com) - a Web3-native blogging platform with built-in tokenization, onchain storage, and community features.


## Features

- **Posts**: Create, read, list posts with markdown support
- **Publications**: Get publication details by slug or custom domain
- **Subscribers**: Add, list, import subscribers (email or wallet), get count
- **Coins**: Tokenized posts, retrieve coin data, check holders, trending coins
- **Users**: Look up user profiles by ID or wallet address
- **Feed**: Get curated posts and posts by tag
- **Web3 Integration**: Native support for wallet addresses, tokens, onchain events

**Note**: Updating posts via API is not currently supported by Paragraph.

## Implementation

This skill uses **native fetch** (Node.js 19+) to call the Paragraph REST API directly. Zero dependencies - lightweight and reliable.

## Prerequisites

1. **Paragraph Account**: Create an account at [paragraph.com](https://paragraph.com)
2. **API Key**: Generate one in Account Settings → Integrations
3. **Node.js 19+**: Required for native fetch (OpenClaw uses Node 24+)

## Installation

The skill is installed in OpenClaw's global skills directory:

```bash
~/.nvm/versions/node/v24.13.0/lib/node_modules/openclaw/skills/paragraph/
```

No dependencies to install - uses built-in `fetch`.

**Note**: This skill requires Node.js 19+ (OpenClaw runs Node 24+). It has **zero external dependencies**, making it lightweight and reliable.

## Configuration

Set these environment variables (in OpenClaw config or shell):

```bash
# Required
export PARAGRAPH_API_KEY="your_api_key_here"
export PARAGRAPH_PUBLICATION_SLUG="your_publication_slug"  # e.g., "myblog" or "jonathancolton.eth"

# Optional
export PARAGRAPH_PUBLICATION_ID="your_publication_id"  # not needed if slug is set
export PARAGRAPH_API_BASE_URL="https://public.api.paragraph.com/api"  # internal, don't change
```

**Note**: `PARAGRAPH_PUBLICATION_SLUG` is now required for proper URL construction. The skill will not auto-discover the slug. If you don't know your publication slug, you can find it in your Paragraph dashboard or by calling `paragraph_getMyPublication` after setting only the API key.

## API Reference

All tools return a standardized response:

```javascript
{
  success: boolean,  // true if operation succeeded
  data: any,         // result data on success
  error: string | null  // error message on failure
}
```

---

## Development & Testing

The skill includes a built-in test suite. Run it from the skill directory:

```bash
cd ~/.nvm/versions/node/v24.13.0/lib/node_modules/openclaw/skills/paragraph
PARAGRAPH_API_KEY="your_key" node test.js
```

### Manual Testing

You can also test individual tools by creating a test script:

```javascript
import tools from "./skill.js"

// Test connection
const conn = await tools.paragraph_testConnection({})
console.log(conn)

// Create a post
const post = await tools.paragraph_createPost({
  title: "Test",
  markdown: "# Hello"
})
console.log(post)
```

### Auto-Discovery

The skill automatically discovers your `PARAGRAPH_PUBLICATION_ID` from the API key by fetching the public feed. This means you **do not** need to manually set the environment variable unless your publication has no posts yet.

To override auto-discovery, set `PARAGRAPH_PUBLICATION_ID` explicitly.

---

### Connection & Testing

#### `paragraph_testConnection`
Verify API connectivity and credentials.
```javascript
await skills.paragraph.paragraph_testConnection({})
// Returns: { success: true, data: { message: "...", hasSubscribers: boolean, totalSubscribers: number } }
```

---

### Posts

#### `paragraph_createPost`
Create a new blog post. **Posts are always published immediately** onchain - there is no draft mode.

```javascript
await skills.paragraph.paragraph_createPost({
  title: "My Web3 Journey",           // required, max 200 chars
  markdown: "# Introduction\n\nContent...", // required
  subtitle: "A brief summary",        // optional, max 300 chars
  imageUrl: "https://example.com/cover.jpg",  // optional cover image URL
  sendNewsletter: false,              // optional, default false - email subscribers?
  slug: "my-web3-journey",            // optional URL slug (1-256 chars)
  postPreview: "Preview text...",     // optional, max 500 chars
  categories: ["web3", "blockchain"], // optional array of category tags
  waitForProcessing: false            // optional, default false - wait for onchain slug/url?
})
```

**Parameter: `waitForProcessing`** (optional, default `false`):
- When `false` (default): returns immediately with `{ id, slug?, url?, publishedAt? }` – slug and URL may be undefined if onchain processing isn't complete yet. Use this for fast, fire-and-forget operations.
- When `true`: the tool will **poll** the post for up to **~25 seconds** (1s then 2s intervals) with **5 second request timeout** and gentle backoff to be rate-limit friendly. Returns the **full post object** with all fields (`slug`, `url`, `publishedAt`, `categories`, `imageUrl`, etc.). If processing doesn't complete in time, returns partial data with `_warning`.

**Example with auto-wait:**
```javascript
const result = await skills.paragraph.paragraph_createPost({
  title: "My Post",
  markdown: "# Hello",
  waitForProcessing: true
})
console.log("Final URL:", result.data.url) // guaranteed to be present if successful
```

**Note**: With `waitForProcessing: false` (default), you'll need to call `paragraph_getPost({ postId })` later to retrieve the final slug and URL, OR construct the URL manually using the publication slug:

```javascript
// After creating a post with waitForProcessing: false
const post = await tools.paragraph_createPost({ title, markdown, waitForProcessing: false })
const postId = post.data.id

// Later, fetch the post to get the slug
const fullPost = await tools.paragraph_getPost({ postId })
const slug = fullPost.data.slug

// Get the publication slug (from env or auto-discovered)
const pub = await tools.paragraph_getMyPublication({})
const pubSlug = pub.data.slug || pub.data.customDomain

// Construct the full URL
const url = `https://paragraph.com/@${pubSlug}/${slug}`
// Example: https://paragraph.com/@jonathancolton.eth/openclaw-ideas-research-report-1
```

#### `paragraph_getPost`
Retrieve a post by its ID.
```javascript
await skills.paragraph.paragraph_getPost({ postId: "post_123" })
```

#### `paragraph_getPostBySlug`
Retrieve a post using publication slug and post slug (for URL building).
```javascript
await skills.paragraph.paragraph_getPostBySlug({
  publicationSlug: "@myblog",
  postSlug: "my-web3-journey"
})
```

#### `paragraph_listPosts`
List posts in a publication with cursor-based pagination.
```javascript
await skills.paragraph.paragraph_listPosts({
  publicationId: "pub_123",   // optional if DEFAULT_PUBLICATION_ID set
  limit: 10,                  // default 10, max 100
  cursor: "next_cursor",      // optional, for pagination
  includeContent: false       // optional - include full content (markdown, json, staticHtml)? default false
})
// Returns: { posts: [{ id, title, slug, ... }], pagination: { cursor, hasMore, total } }
```

#### `paragraph_getFeed`
Get curated feed of posts (public endpoint, works with API key).
```javascript
await skills.paragraph.paragraph_getFeed({
  limit: 20,   // default 20, max 60
  cursor: "optional_cursor"
})
// Returns: { posts: [], pagination: {} }
```

#### `paragraph_getPostsByTag`
Get posts with a specific tag, sorted by publish date (newest first).
```javascript
await skills.paragraph.paragraph_getPostsByTag({
  tag: "web3",    // required
  limit: 20,      // default 10, max 100
  cursor: "optional_cursor",
  includeContent: false  // optional - include full content (markdown, json, staticHtml)?
})
// Returns: { posts: [], pagination: {} }
```

---

### Publications

#### `paragraph_getPublication`
Get publication details by slug.
```javascript
await skills.paragraph.paragraph_getPublication({ slug: "@myblog" })
// Returns: { id, name, slug, ownerUserId, customDomain?, summary?, logoUrl? }
```

#### `paragraph_getPublicationByDomain`
Get publication details by custom domain.
```javascript
await skills.paragraph.paragraph_getPublicationByDomain({
  domain: "blog.example.com"
})
```

#### `paragraph_getMyPublication`
Get the publication associated with the current API key. This is useful when you need to retrieve the publication's slug or ID programmatically without manually configuring `PARAGRAPH_PUBLICATION_ID`. Auto-discovers and caches the publication details.
```javascript
await skills.paragraph.paragraph_getMyPublication({})
// Returns: { id, name, slug, customDomain?, ... }
```

---

### Subscribers

#### `paragraph_addSubscriber`
Add a new subscriber via email or wallet address.
```javascript
await skills.paragraph.paragraph_addSubscriber({
  email: "subscriber@example.com",  // optional
  wallet: "0x1234...",              // optional (0x address format)
  sendWelcomeEmail: true            // default: true
})
// At least one of email or wallet is required.
```

#### `paragraph_listSubscribers`
List subscribers with cursor pagination. Scoped to the publication associated with your API key.
```javascript
await skills.paragraph.paragraph_listSubscribers({
  limit: 50,   // default 10, max 100
  cursor: "next_cursor"  // optional
})
// Returns: { subscribers: [{ email, walletAddress, createdAt }], pagination: { cursor, hasMore, total } }
```

#### `paragraph_importSubscribers`
Bulk import subscribers from a CSV file.
```javascript
await skills.paragraph.paragraph_importSubscribers({
  csvPath: "/path/to/subscribers.csv",
  sendWelcomeEmail: true  // default: true
})
// Returns: { imported: number, skipped: number, total: number }
```

CSV format (columns case-insensitive):
```csv
email,wallet_address,created_at
user@example.com,,2025-01-15
,0x1234567890abcdef1234567890abcdef12345678,2025-01-16
```
- At least one of email or wallet_address required per row
- Max file size: 10MB
- `created_at` is optional (timestamp or date string)

#### `paragraph_getSubscriberCount`
Get total subscriber count for a publication.
```javascript
await skills.paragraph.paragraph_getSubscriberCount({
  publicationId: "pub_123"  // required
})
// Returns: { count: number }
```

---

### Coins (Tokenized Posts)

Paragraph coins represent tokenized posts deployed via Doppler. Each coin can be bought/sold on-chain.

#### `paragraph_getCoin`
Get coin details by coin ID.
```javascript
await skills.paragraph.paragraph_getCoin({ coinId: "Bxf0rHsK2K97U6NE2UQo" })
```

#### `paragraph_getCoinByContract`
Get coin details by Ethereum contract address.
```javascript
await skills.paragraph.paragraph_getCoinByContract({
  contractAddress: "0x06fc3d5d2369561e28f261148576520f5e49d6ea"
})
```

#### `paragraph_getPopularCoins`
Retrieve trending/popular coins.
```javascript
await skills.paragraph.paragraph_getPopularCoins({})
// Returns: array of coins with { id, contractAddress, metadata }
```

#### `paragraph_listCoinHolders`
List token holders for a specific coin.
```javascript
await skills.paragraph.paragraph_listCoinHolders({
  coinId: "coin_id_here",  // required
  limit: 50,
  cursor: "optional"
})
// Returns: { holders: [], pagination: { cursor, hasMore, total } }
```

---

### Users

#### `paragraph_getUser`
Get user profile by user ID.
```javascript
await skills.paragraph.paragraph_getUser({ userId: "user_123" })
```

#### `paragraph_getUserByWallet`
Get user profile by Ethereum wallet address.
```javascript
await skills.paragraph.paragraph_getUserByWallet({
  walletAddress: "0x1234..."
})
```

---

## Error Handling

All tools return `{ success, data, error }`. Always check `success` before using `data`.

Example:
```javascript
const result = await skills.paragraph.paragraph_createPost({
  title: "Test",
  markdown: "Content"
})

if (!result.success) {
  console.error("Operation failed:", result.error)
  // Handle: missing params, auth errors, rate limits, validation failures
} else {
  console.log("Post created:", result.data.id)
}
```

Common errors:
- `PARAGRAPH_API_KEY environment variable not set` - configure your key
- `postId is required` / `title and markdown required` - check parameter names
- `HTTP 401` - invalid or expired API key
- `HTTP 404` - resource not found (wrong ID/slug)
- `HTTP 429` - rate limited (implement retry with backoff)

---

## Rate Limits

Paragraph API enforces rate limits (default: ~100 requests/period). The skill does not implement automatic retries.

If you hit rate limits:
1. Add delays between calls: `await new Promise(r => setTimeout(r, 200))`
2. Implement exponential backoff in your agent logic
3. Contact `support@paragraph.com` to request limit increases

---

## Web3 Features & Coin Integration

Paragraph's coin system (via Doppler) enables tokenized posts:

1. **Tokenize a post**: When creating a post, include `coinData` (not yet exposed in this skill - may require direct API call or future SDK support)
2. **Track coin performance**: Use `paragraph_getCoin` and `paragraph_listCoinHolders` to monitor engagement
3. **Onchain events**: New coins are deployed via Doppler; monitor `Airlock.Create` events on Base for real-time discovery (see Paragraph docs)

Current coin tools are **read-only**. Coin creation/minting may require additional API access or wallet signing.

---

## Integration with Content Pipeline

This skill enables Paragraph as the **Web3-native distribution channel** in your automated content pipeline:

```
[Research Agent] → [Writer Agent] → [Publisher Agent (paragraph adapter)] → [Analytics Agent]
```

**Workflow**:
1. Writer generates markdown draft
2. Publisher Agent calls `paragraph_createPost` with `published: false`
3. Review/approval step
4. Publish: `paragraph_updatePost` with `published: true` OR create with `published: true`
5. If tokenizing: capture coin ID from response, track via `paragraph_getCoin` and `paragraph_listCoinHolders`
6. Analytics: correlate engagement (views, holders) with content performance

**Monetization**:
- Coin holdings indicate stakeholder engagement
- Potential future: enable coin-gated content, tips, revenue sharing
- Combine with NFT project announcements for community ownership

---

## Troubleshooting

### "Authentication failed" / "401"
- Verify `PARAGRAPH_API_KEY` is set correctly in OpenClaw environment
- Check API key hasn't been revoked (generate new one in Paragraph settings)
- Ensure API key has proper permissions (should be publication-scoped)

### "Not Found" / "404"
- Check endpoint paths: base URL should be `https://public.api.paragraph.com/api`
- Verify publication IDs, post IDs, slugs are correct
- Encode slugs with `encodeURIComponent` if they contain special characters

### "Rate limit exceeded" / "429"
- Reduce call frequency; add 100-200ms delays
- Use pagination efficiently (fetch only what you need)
- Contact Paragraph support to increase your limits

### "Invalid request" / "400"
- For `paragraph_createPost`: ensure `title` and `markdown` are provided
- For `paragraph_addSubscriber`: at least one of `email` or `wallet` required
- Check field types: `tags` must be array of strings, `limit` must be number

### CSV import fails
- Ensure file is `.csv` format, not Excel (`.xlsx`)
- Max file size: 10MB
- Column headers: use `email` or `subscriberEmail`, `wallet_address`; headers are case-insensitive
- At least one of email or wallet must be present per row

---

## Development

### Adding New Tools
Follow the pattern in `skill.js`:
1. Add async function to `tools` object
2. Use `wrapTool` for automatic error handling: `wrapTool(async (params) => { ... })`
3. Use `request(method, endpoint, body, params, options)` helper
4. Validate parameters, return data (no need to wrap in `{success}` - `wrapTool` does it)
5. Document with JSDoc and update this README

### Testing
```bash
cd ~/.nvm/versions/node/v24.13.0/lib/node_modules/openclaw/skills/paragraph
npm test
```

Tests include:
- Module loading (tool count)
- Parameter validation
- API key detection
- Live connection test (if PARAGRAPH_API_KEY set)

### API Documentation
- Official OpenAPI spec: https://raw.githubusercontent.com/paragraph-xyz/paragraph-sdk-js/main/openapi.json
- API Reference: https://paragraph.com/docs/api-reference
- SDK (TypeScript): https://github.com/paragraph-xyz/paragraph-sdk-js
- MCP Server (for AI dev): https://paragraph.mintlify.app/mcp

---

## Technical Notes

- **Base URL**: `https://public.api.paragraph.com/api` (all endpoints prefixed with `/v1`)
- **Authentication**: `Authorization: Bearer {PARAGRAPH_API_KEY}` header
- **Content-Type**: JSON for most, `text/csv` for imports, `multipart/form-data` for file uploads
- **Pagination**: Cursor-based on most list endpoints (`cursor`, `hasMore`, `limit` parameters)
- **Rate Limits**: 100 requests per period (check `x-ratelimit-*` response headers)
- **No Dependencies**: Uses Node.js native `fetch` (v19+), `FormData`, `fs` (dynamic import for CSV)

---

## License

ISC

---

## Related

- **Memory**: `memory/2026-02-14.md` - Blog platform shortlist & content pipeline strategy
- **Deep Dive**: `memory/paragraph-api-deep-dive-2026-02-14.md` - Full API analysis
- **Implementation**: `memory/paragraph-skill-implementation-2026-02-14.md` - Development notes

---

**Last Updated**: 2026-02-14
**Version**: 1.2.0 (auto-discovery, fixed createPost fields, removed updatePost)
**Status**: ✅ Production Ready - Verified with live API

---

## Changelog

### v1.2.0 (2026-02-14)
- **feat**: Auto-discover `PARAGRAPH_PUBLICATION_ID` from feed – no manual config needed
- **fix**: Correct `paragraph_createPost` payload fields (`markdown`, `imageUrl`, `categories`)
- **fix**: Remove non-existent `paragraph_updatePost` (endpoint doesn't exist in Paragraph API)
- **fix**: Correct `paragraph_listPosts` endpoint to `/v1/publications/{id}/posts`
- **docs**: Update examples to reflect actual API behavior (no draft mode, onchain processing)
- **docs**: Clarify that `slug` and `url` may be undefined immediately after post creation

### v1.1.0 (2026-02-13)
- Initial implementation with 19 tools
- Zero-dependency native fetch
- Full test coverage