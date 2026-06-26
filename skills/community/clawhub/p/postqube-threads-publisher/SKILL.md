---
name: postqube-threads-publisher
description: |
  A powerful social media posting skill for PostQube. 
  Triggers when the user wants to:
  - Publish a post to Threads.
  - Create a "Thread Storm" or "Auto-chained" thread.
  - Schedule or post content with images/videos to social media.
  - Check the status or history of their social media posts.
  - Monitor their API usage and quota.
version: 1.2.0
author: Fahmi
metadata:
  openclaw:
    os: ["darwin", "linux"]
    requires:
      env:
        - POSTQUBE_API_KEY
      bins:
        - curl
    primaryEnv: POSTQUBE_API_KEY
    emoji: 📱
---

# 📱 PostQube — Social Media Publisher

PostQube allows you to seamlessly publish text, images, and videos to social media platforms (currently specializing in **Threads**) via its REST API. It supports native **Thread Storming**, which automatically chains multiple posts together into a single cohesive thread.

## 🛠 Prerequisites

1.  **API Key**: You must have a PostQube API key. If not provided, ask the user to generate one from the [PostQube Dashboard](https://postqube.quickbitsoftware.com/dashboard).
2.  **Authentication**: The API key must be stored in the `POSTQUBE_API_KEY` environment variable.

---

## 📋 How to Use

Follow these steps when the user asks to post or manage social media content:

1.  **Validate**: Ensure the `POSTQUBE_API_KEY` is present.
2.  **Plan**: For Threads, ensure the content is under **500 characters** per post.
3.  **Confirm**: Always show the drafted content to the user and ask for explicit confirmation before calling the API.
4.  **Execute**: Use `curl` to interact with the PostQube API (Base URL: `https://postqube.quickbitsoftware.com`).
5.  **Report**: Share the `postId` or a direct link to the post with the user after a successful request.

---

## ⚡ Available Actions

### 1. Create a Post / Thread
Published single posts or native threads.

**Endpoint:** `POST /api/v1/post`

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `platform` | string | Yes | The target platform (e.g., `"threads"`). |
| `text` | string | Conditional | Content for a single post (Max 500 chars). |
| `threads` | array | Conditional | Array of objects `[{"text": "..."}]` for automatic chaining. |
| `mediaUrls` | array | No | Publicly accessible URLs for images or videos. |
| `mediaType` | string | No | `"IMAGE"`, `"VIDEO"`, or `"CAROUSEL"`. |
| `replyToId` | string | No | The `platformPostId` to reply to. |

#### Examples

**Single Post:**
```bash
curl -X POST https://postqube.quickbitsoftware.com/api/v1/post \
  -H "x-api-key: $POSTQUBE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "threads",
    "text": "Revolutionizing social media with PostQube! 🚀"
  }'
```

**Thread Storm (Chaining):**
```bash
curl -X POST https://postqube.quickbitsoftware.com/api/v1/post \
  -H "x-api-key: $POSTQUBE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "threads",
    "threads": [
      { "text": "1/ This is how easy it is to start a thread..." },
      { "text": "2/ PostQube handles the native chaining for you." },
      { "text": "3/ Try it out today!" }
    ]
  }'
```

---

### 2. Check Post Status
Query the status of a specific post using its internal `postId`.

**Endpoint:** `GET /api/v1/post/{postId}`
```bash
curl https://postqube.quickbitsoftware.com/api/v1/post/{postId} \
  -H "x-api-key: $POSTQUBE_API_KEY"
```

---

### 3. List Recent Posts
Fetch a list of recent posts for a specific platform.

**Endpoint:** `GET /api/v1/posts`
```bash
curl "https://postqube.quickbitsoftware.com/api/v1/posts?platform=threads&limit=10" \
  -H "x-api-key: $POSTQUBE_API_KEY"
```

---

### 4. Monitor Usage
Check your remaining API quota and usage limits.

**Endpoint:** `GET /api/v1/usage`
```bash
curl https://postqube.quickbitsoftware.com/api/v1/usage \
  -H "x-api-key: $POSTQUBE_API_KEY"
```

---

## ⚠️ Error Handling

| Status Code | Meaning | Agent Action |
| :--- | :--- | :--- |
| **400** | Bad Request | Check platform support and character limits (500 max). |
| **401** | Unauthorized | Ask the user to verify their `POSTQUBE_API_KEY`. |
| **402** | Quota Exceeded | Suggest upgrading at [postqube.quickbitsoftware.com/pricing](https://postqube.quickbitsoftware.com/pricing). |
| **502** | Platform Error | The social network rejected the post. Check media URLs or content. |

---

## 💡 Best Practices

- **Media**: Ensure `mediaUrls` are publicly accessible. Private/Local paths will fail.
- **Limits**: Threads has a 500-character limit. If the content is longer, suggest using the `threads` chaining feature.
- **Safety**: Never share the API key in the post content itself.
- **Confirmation**: Always summarize the action before executing: *"I'm about to post [Content] to Threads. Proceed?"*
