# Content Adapter

## Purpose
Interface specification for connecting content generation and management systems to the Marketing OS.

---

## Interface Contract

### Adapter Name
`content`

### Supported Operations

| Operation | Method | Description |
|---|---|---|
| `generate_copy` | POST | Generate marketing copy (ads, emails, social posts) |
| `generate_image` | POST | Generate marketing visuals |
| `generate_video` | POST | Generate short-form video content |
| `publish_content` | POST | Publish content to a channel |
| `schedule_content` | POST | Schedule content for future publication |
| `get_content_status` | GET | Check publication status |
| `get_content_performance` | GET | Retrieve performance metrics for published content |

---

### Input Schema (Request)

```json
{
  "operation": "string — one of the supported operations",
  "parameters": {
    "content_type": "ad_copy | email | social_post | blog | landing_page | image | video",
    "brief": {
      "objective": "string — what this content should achieve",
      "target_audience": "string — who this is for",
      "key_messages": ["string — main points to convey"],
      "tone": "string — professional | casual | urgent | inspirational",
      "cta": "string — call to action",
      "constraints": {
        "max_length": "number — character/word limit",
        "brand_guidelines_ref": "string",
        "required_keywords": ["string"],
        "prohibited_terms": ["string"]
      }
    },
    "channel": "string — where to publish (linkedin, twitter, email, blog, etc.)",
    "schedule": {
      "publish_at": "ISO 8601",
      "timezone": "string"
    },
    "variations": "number — how many variations to generate (for A/B testing)",
    "campaign_id": "string — for tracking",
    "task_id": "string — for tracking"
  },
  "auth": {
    "method": "api_key | oauth2",
    "credentials_ref": "string"
  }
}
```

### Output Schema (Response)

```json
{
  "adapter": "content",
  "operation": "string",
  "timestamp": "ISO 8601",
  "status": "success | partial | error",
  "data": {
    "content_id": "string — unique content identifier",
    "content_type": "string",
    "generated_content": [
      {
        "variation_id": "string",
        "content": "string — the actual content (text, URL for media)",
        "metadata": {
          "word_count": "number",
          "reading_time": "string",
          "sentiment": "string",
          "readability_score": "number"
        }
      }
    ],
    "publication": {
      "status": "draft | scheduled | published | failed",
      "published_url": "string",
      "published_at": "ISO 8601",
      "platform_post_id": "string"
    },
    "performance": {
      "impressions": "number",
      "clicks": "number",
      "engagement_rate": "number",
      "shares": "number",
      "comments": "number",
      "conversions": "number"
    }
  },
  "metadata": {
    "source": "string — content platform name",
    "generation_model": "string — AI model used if applicable",
    "generation_time_ms": "number"
  },
  "error": {
    "code": "string",
    "message": "string",
    "retryable": "boolean"
  }
}
```

---

## Potential Content Platforms

| Platform | Type | Use Case |
|---|---|---|
| OpenAI / Claude API | LLM | Copy generation |
| DALL-E / Midjourney API | Image AI | Visual content |
| Runway / Pika API | Video AI | Video content |
| Buffer / Hootsuite | Social scheduling | Multi-channel publishing |
| Mailchimp / SendGrid | Email | Email campaigns |
| WordPress API | Blog / CMS | Content publishing |
| Webflow API | Landing pages | Page creation |
| Canva API | Design | Template-based visuals |

---

## Integration Steps

1. Implement the adapter interface for your content stack
2. Register in `configs/system.config.json` under `adapters.content`
3. Set `enabled: true`, provide endpoint and auth
4. Test with a `generate_copy` call
5. The Marketing Operator will use this adapter during Execution Sprint to:
   - Generate campaign content
   - Publish to channels
   - Track content performance

---

## Content Quality Guardrails

- All generated content must pass brand guideline check before publishing
- A/B test variations should differ meaningfully (not just word swaps)
- Content must include proper attribution if using third-party assets
- Automated publishing requires human approval unless `auto_mode: true` in config
- Content performance must be tracked and fed back through the feedback loop

---

## Future Extensions

- **Personalization**: Generate audience-specific content variations
- **Localization**: Multi-language content generation
- **Dynamic content**: Real-time content based on user behavior
- **Content recycling**: Repurpose high-performing content across channels
