---
name: miro-api
description: Complete Miro REST API reference for building integrations, automating workflows, and programmatically managing boards, cards, shapes, users, and team resources. Language-agnostic documentation with examples, authentication patterns, rate limiting, webhooks, and error handling.
---

# Miro REST API

The Miro REST API enables programmatic access to create, read, update, and delete boards, items, users, and team resources. This skill provides comprehensive documentation for integrating Miro with external systems, automating workflows, and building custom applications.

## Quick Start

**Base URL:** `https://api.miro.com/v2`

**Authentication:** OAuth 2.0 or Personal Access Tokens

**Example Request:**
```bash
curl -X GET https://api.miro.com/v2/boards \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "data": [
    {
      "id": "board-id-123",
      "name": "My Board",
      "owner": {"id": "user-id", "email": "user@example.com"},
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-20T14:45:00Z"
    }
  ]
}
```

## Core Capabilities

### 1. Board Management
- **List boards** - Get all boards in your workspace
- **Create boards** - Programmatically create new boards
- **Update board settings** - Modify name, sharing, permissions
- **Delete boards** - Soft-delete boards (recoverable)
- **Board sharing & access** - Manage team member permissions

### 2. Items (Cards, Shapes, Text, Stickies)
- **Create items** - Add cards, shapes, text, stickies, images to boards
- **Read items** - Fetch item details, properties, attachments
- **Update items** - Modify content, position, style, metadata
- **Delete items** - Remove items from boards
- **Batch operations** - Efficient bulk create/update

### 3. Shapes & Connectors
- **Shape library** - Rectangle, circle, diamond, line, arrow, etc.
- **Shape styling** - Fill color, stroke, line width, opacity
- **Connectors** - Create connections between shapes
- **Geometry** - Position, rotation, dimensions

### 4. Text & Rich Content
- **Text shapes** - Add formatted text to boards
- **Rich text** - Bold, italic, underline, font sizes
- **Text alignment** - Left, center, right, justified
- **Font families** - System fonts and custom typefaces

### 5. Images & Files
- **Upload images** - Add images to boards
- **Image management** - Reference, replace, delete
- **Attachments** - Embed files and URLs

### 6. Frames & Grouping
- **Frames** - Organizational containers for items
- **Groups** - Logical grouping of related items
- **Hierarchy** - Nested structures and relationships

### 7. Comments & Collaboration
- **Add comments** - Comment on boards and items
- **Thread replies** - Nested comment threads
- **Mentions** - Tag team members (@username)
- **Comment reactions** - Emoji reactions to comments

### 8. Users & Team Management
- **List team members** - Get users in workspace
- **User profiles** - Email, name, role, permissions
- **Invitations** - Invite users to workspace
- **Team settings** - Manage workspace configuration

### 9. Webhooks & Events
- **Board events** - item.created, item.updated, item.deleted
- **Comment events** - comment.created, comment.deleted
- **Webhook management** - Register, test, delete webhooks
- **Event payload** - Complete event data with timestamps

### 10. Advanced Features
- **Exports** - Export boards as PNG/PDF/CSV
- **Import** - Batch import items from external sources
- **Integrations** - Connect with Slack, Jira, Figma, etc.
- **Custom metadata** - Attach custom properties to items

## Authentication

### OAuth 2.0 (Recommended for Production)
```
1. Register app at https://miro.com/app/settings/user-profile/apps
2. Redirect user to authorization endpoint
3. Exchange auth code for access token
4. Use token in Authorization header: Bearer <token>
5. Refresh token when expired (3600 seconds)
```

### Personal Access Tokens (Development)
```bash
curl -X GET https://api.miro.com/v2/boards \
  -H "Authorization: Bearer YOUR_PERSONAL_TOKEN"
```

**Creating a PAT:**
1. Go to https://miro.com/app/settings/user-profile/apps
2. Click "Create new app" or "Personal access token"
3. Select required scopes (boards:read, items:write, etc.)
4. Copy token (shown only once)
5. Store securely (never commit to version control)

## API Endpoints Overview

### Boards
- `GET /boards` - List all boards
- `POST /boards` - Create new board
- `GET /boards/{board_id}` - Get board details
- `PATCH /boards/{board_id}` - Update board
- `DELETE /boards/{board_id}` - Delete board

### Items
- `GET /boards/{board_id}/items` - List items on board
- `POST /boards/{board_id}/items` - Create item
- `GET /boards/{board_id}/items/{item_id}` - Get item details
- `PATCH /boards/{board_id}/items/{item_id}` - Update item
- `DELETE /boards/{board_id}/items/{item_id}` - Delete item

### Comments
- `GET /boards/{board_id}/comments` - List comments
- `POST /boards/{board_id}/comments` - Add comment
- `GET /boards/{board_id}/comments/{comment_id}` - Get comment
- `PATCH /boards/{board_id}/comments/{comment_id}` - Update comment
- `DELETE /boards/{board_id}/comments/{comment_id}` - Delete comment

### Team Members
- `GET /teams/{team_id}/members` - List team members
- `POST /teams/{team_id}/members` - Invite member
- `DELETE /teams/{team_id}/members/{user_id}` - Remove member

### Webhooks
- `GET /teams/{team_id}/webhooks` - List webhooks
- `POST /teams/{team_id}/webhooks` - Create webhook
- `PATCH /teams/{team_id}/webhooks/{webhook_id}` - Update webhook
- `DELETE /teams/{team_id}/webhooks/{webhook_id}` - Delete webhook

## Rate Limiting

**Default Limits:**
- 300 requests per minute (5 req/sec)
- 50,000 requests per month

**Headers:**
- `X-RateLimit-Limit` - Limit for this time window
- `X-RateLimit-Remaining` - Requests left
- `X-RateLimit-Reset` - Unix timestamp when limit resets

**Handling Rate Limits:**
```bash
# Check remaining requests
X-RateLimit-Remaining: 45

# Wait until reset time
curl -i https://api.miro.com/v2/boards | grep X-RateLimit
```

**Best Practices:**
1. Check `X-RateLimit-Remaining` before requests
2. Implement exponential backoff on 429 responses
3. Batch operations when possible
4. Cache board/item data locally
5. Use webhooks for real-time updates instead of polling

## Error Handling

### Common HTTP Status Codes
- `200 OK` - Successful request
- `201 Created` - Resource created
- `204 No Content` - Successful deletion
- `400 Bad Request` - Invalid parameters
- `401 Unauthorized` - Missing/invalid token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource doesn't exist
- `429 Too Many Requests` - Rate limited
- `500 Server Error` - Miro API error

### Error Response Format
```json
{
  "code": 400,
  "message": "Invalid request parameter",
  "details": {
    "param": "board_id",
    "reason": "Expected UUID format"
  }
}
```

## Supported Item Types

| Type | Description | Can Contain |
|------|-------------|------------|
| `CARD` | Note-like item with title + content | Text, emoji |
| `SHAPE` | Geometric shapes (rect, circle, etc.) | Fill, stroke styling |
| `TEXT` | Rich text formatting | Bold, italic, colors |
| `STICKY` | Virtual sticky note | Text, color options |
| `IMAGE` | Image/photo uploads | File data |
| `FRAME` | Container/group for items | Nested items |
| `CONNECTOR` | Line connecting shapes | Source/target references |
| `EMBED` | Embedded content (Figma, YouTube, etc.) | External URLs |

## Pagination

**Query Parameters:**
- `limit` - Items per page (1-100, default 100)
- `cursor` - Pagination cursor (from previous response)

**Response:**
```json
{
  "data": [...items...],
  "cursor": "next-page-cursor-token",
  "limit": 100
}
```

## Field Selection (Sparse Fieldsets)

**Optimize responses by requesting specific fields:**
```bash
GET /boards/{board_id}/items?fields=id,type,title,position
```

## Real-Time Updates

### Option 1: Webhooks (Recommended)
- Receive instant notifications for board changes
- No polling required
- Supports filtering by event type

### Option 2: Polling
- Periodic GET requests to check for changes
- Less efficient but works everywhere
- Implement exponential backoff

## SDK & Library Support

**Official SDKs:**
- JavaScript/Node.js
- Python
- Go

**Community Libraries:**
- Java, C#, Ruby, PHP
- (Check GitHub for latest)

## Integration Patterns

### Sync External Data to Miro
1. Fetch data from external source (Jira, Airtable, etc.)
2. Transform to Miro item format
3. Batch create items on board
4. Set custom metadata for tracking

### Slack Integration
```
User mentions @miro-bot in Slack
→ Bot creates board or card
→ Sends link back to Slack channel
```

### Jira Sync
```
Jira ticket created → POST to Miro board
Miro item updated → PATCH Jira ticket
Real-time sync via webhooks
```

## Security Best Practices

1. **Token Management**
   - Never commit tokens to git
   - Use environment variables
   - Rotate tokens regularly
   - Use minimal required scopes

2. **Data Privacy**
   - Don't log sensitive board content
   - Encrypt data in transit (HTTPS)
   - Validate webhook signatures

3. **Access Control**
   - Verify user permissions before operations
   - Use board/item permissions
   - Audit API usage

## Reference Files

See detailed documentation:
- `references/endpoints.md` - Complete endpoint reference
- `references/authentication.md` - Auth patterns and flows
- `references/webhooks.md` - Webhook setup and payloads
- `references/errors.md` - Error codes and handling
- `references/examples.md` - Code examples (curl, HTTP)
- `references/rate-limiting.md` - Detailed rate limit info
- `references/best-practices.md` - Performance and design patterns

## Links

- **API Docs:** https://developer.miro.com/
- **Playground:** https://developers.miro.com/playground
- **Status:** https://status.miro.com
- **Support:** https://support.miro.com
- **Community:** https://community.miro.com

## Version History

- **v2** (Current) - Latest stable API
- **v1** (Deprecated) - Legacy, use v2

