# Example Workflows

## 1. Upload Image and Post to Multiple Platforms

**User:** "Post this image to Instagram and Twitter"

**Claude's steps:**
1. Authenticate with Posta
2. List connected accounts to find Instagram and X/Twitter account IDs
3. Upload the image via the 3-step signed URL flow
4. Wait for processing to complete (poll media status)
5. Create the post with both account IDs
6. Show preview to user (caption, platforms, media)
7. On approval, publish immediately or schedule

```bash
source "${POSTA_SKILL_ROOT:-${OPENCLAW_SKILL_ROOT:-${CLAUDE_PLUGIN_ROOT:-}}}/skills/posta/scripts/posta-api.sh"

# Get accounts
ACCOUNTS=$(posta_list_accounts)
# → Find Instagram account ID and X account ID

# Upload image
MEDIA_ID=$(posta_upload_media "/path/to/image.jpg" "image/jpeg")

# Get account IDs (integers) and convert to strings for socialAccountIds
INSTA_ID=$(echo "$ACCOUNTS" | jq -r '.[] | select(.platform == "instagram") | .id | tostring')
X_ID=$(echo "$ACCOUNTS" | jq -r '.[] | select(.platform == "x") | .id | tostring')

# Create post as draft first
POST=$(posta_create_post '{
  "caption": "Check this out!",
  "hashtags": ["photo", "vibes"],
  "mediaIds": ["'"${MEDIA_ID}"'"],
  "socialAccountIds": ["'"${INSTA_ID}"'", "'"${X_ID}"'"],
  "isDraft": true
}')

POST_ID=$(echo "$POST" | jq -r '.id')

# After user confirms, publish
posta_publish_post "$POST_ID"
```

---

## 2. View Best Performing Posts

**User:** "Show me my best performing posts this month"

**Claude's steps:**
1. Authenticate with Posta
2. Fetch analytics overview for the period
3. Fetch top posts sorted by engagements
4. Format into a readable table
5. Suggest insights (best day, best platform, best content type)

```bash
source "${POSTA_SKILL_ROOT:-${OPENCLAW_SKILL_ROOT:-${CLAUDE_PLUGIN_ROOT:-}}}/skills/posta/scripts/posta-api.sh"

# Get overview stats
OVERVIEW=$(posta_get_analytics_overview "30d")

# Get top posts
TOP_POSTS=$(posta_api GET "/analytics/posts?limit=10&sortBy=engagements&sortOrder=desc")

# Get best times
BEST_TIMES=$(posta_get_best_times)

# Display to user as formatted tables
echo "$OVERVIEW" | jq '.'
echo "$TOP_POSTS" | jq '.items[] | {caption: .caption[:50], platform: .platform, engagements: .engagements, impressions: .impressions}'
```

---

## 3. Generate AI Image and Caption from Scratch

**User:** "Generate a social media post about spring flowers"

**Claude's steps:**
1. Generate an image using fal.ai (FLUX) with a spring flowers prompt
2. Write the caption and hashtags directly (you are Claude — no text API needed)
3. Upload the image to Posta
4. Ask user which accounts to post to
5. Create the post

```bash
source "${POSTA_SKILL_ROOT:-${OPENCLAW_SKILL_ROOT:-${CLAUDE_PLUGIN_ROOT:-}}}/skills/posta/scripts/posta-api.sh"

# Generate image with fal.ai — returns a hosted URL, not raw bytes
RESULT=$(curl -s -X POST "https://fal.run/fal-ai/flux/schnell" \
  -H "Authorization: Key ${FAL_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "vibrant spring flowers in a garden, cherry blossoms, tulips, daffodils, photorealistic, natural colors, proper white balance, high quality, detailed",
    "image_size": "square_hd",
    "num_images": 1
  }')
IMAGE_URL=$(echo "$RESULT" | jq -r '.images[0].url')

# Upload the hosted image to Posta
MEDIA_ID=$(posta_upload_from_url "$IMAGE_URL" "image/jpeg")

# Write the caption yourself (you are Claude) — no external text API
CAPTION="Spring has sprung 🌸 Fresh blooms, fresh starts. What's the first flower you look for each spring?"

# Show user for approval before posting
echo "Caption: ${CAPTION}"
echo "Image: ${IMAGE_URL}"
```

---

## 4. Create Post with Multiline Caption

**User:** "Create a LinkedIn post about EU data sovereignty with a detailed caption"

**Claude's steps:**
1. Write the multiline caption to a temp file
2. Use `posta_create_post_from_file` to handle escaping correctly
3. Manage the post lifecycle with get/update/delete helpers

```bash
source "${POSTA_SKILL_ROOT:-${OPENCLAW_SKILL_ROOT:-${CLAUDE_PLUGIN_ROOT:-}}}/skills/posta/scripts/posta-api.sh"

# Get LinkedIn account (IDs are integers, convert to string)
ACCOUNTS=$(posta_list_accounts)
LINKEDIN_ID=$(echo "$ACCOUNTS" | jq -r '.[] | select(.platform == "linkedin") | .id | tostring')

# Write multiline caption to file (avoids JSON escaping issues)
cat > /tmp/caption.txt << 'EOF'
The EU is taking a bold stance on data sovereignty.

Here's what every tech leader needs to know:

1. New regulations require EU data to stay in EU infrastructure
2. Cloud providers must offer EU-only deployment options
3. Compliance deadlines are approaching fast

What's your company's strategy? Drop a comment below.
EOF

# Upload media
MEDIA_ID=$(posta_upload_media /tmp/eu_data.png "image/png")

# Create post from file — handles all escaping correctly
POST=$(posta_create_post_from_file /tmp/caption.txt "[\"${MEDIA_ID}\"]" "[\"${LINKEDIN_ID}\"]" true '["datasovereignty", "EU", "cloud", "tech"]')
POST_ID=$(echo "$POST" | jq -r '.id')

# Review the created post
posta_get_post "$POST_ID" | jq '{id, caption, status}'

# After user confirms, schedule
posta_schedule_post "$POST_ID" "2026-03-06T09:00:00Z"

# Or if user changes mind, delete
# posta_delete_post "$POST_ID"
```

---

## 5. Check Platform Specs Before Posting

**User:** "What are the character limits and media requirements for each platform?"

**Claude's steps:**
1. Fetch platform specifications
2. Display formatted table of limits

```bash
source "${POSTA_SKILL_ROOT:-${OPENCLAW_SKILL_ROOT:-${CLAUDE_PLUGIN_ROOT:-}}}/skills/posta/scripts/posta-api.sh"

# Get all platform specs at once
SPECS=$(posta_get_platform_specs)
echo "$SPECS" | jq '.'

# Or get specs for a specific platform
posta_get_platform "tiktok"

# Get aspect ratio reference
posta_get_aspect_ratios
```

---

## 6. Compare Post Performance and Export Analytics

**User:** "Compare my last 3 posts and export a report"

**Claude's steps:**
1. Get top posts to find IDs
2. Compare posts side by side
3. Export analytics

```bash
source "${POSTA_SKILL_ROOT:-${OPENCLAW_SKILL_ROOT:-${CLAUDE_PLUGIN_ROOT:-}}}/skills/posta/scripts/posta-api.sh"

# Get recent posts with analytics
TOP=$(posta_get_analytics_posts 3 0 "engagements" "desc")
POST_IDS=$(echo "$TOP" | jq -r '[.items[].id] | join(",")')

# Compare them side by side
COMPARISON=$(posta_compare_posts "$POST_IDS")
echo "$COMPARISON" | jq '.'

# Export full analytics report
posta_export_analytics_csv "30d"
posta_export_analytics_pdf "90d"

# Check engagement benchmarks
posta_get_benchmarks
```

---

## 7. View Content Calendar and Manage Schedule

**User:** "Show me what's scheduled for next week"

**Claude's steps:**
1. Fetch calendar view for the date range
2. Display posts organized by day

```bash
source "${POSTA_SKILL_ROOT:-${OPENCLAW_SKILL_ROOT:-${CLAUDE_PLUGIN_ROOT:-}}}/skills/posta/scripts/posta-api.sh"

# Get next week's calendar
CALENDAR=$(posta_get_calendar "2026-03-16" "2026-03-22")
echo "$CALENDAR" | jq '.items[] | {id, caption: .caption[:60], status, scheduledAt, platforms: [.socialAccounts[].platform]}'

# To reschedule a post: cancel then re-schedule
posta_cancel_post "$POST_ID"
posta_schedule_post "$POST_ID" "2026-03-18T10:00:00Z"
```

---

## 8. Media Library Management

**User:** "Show me my uploaded media and clean up old files"

```bash
source "${POSTA_SKILL_ROOT:-${OPENCLAW_SKILL_ROOT:-${CLAUDE_PLUGIN_ROOT:-}}}/skills/posta/scripts/posta-api.sh"

# List all media
ALL=$(posta_list_media "" "" 50)
echo "$ALL" | jq '.items[] | {id, name, type, mime_type, processing_status, created_at}'

# List only completed images
IMAGES=$(posta_list_media "image" "completed")

# List only videos
VIDEOS=$(posta_list_media "video")

# Delete unused media
posta_delete_media "$MEDIA_ID"

# Generate a carousel PDF from multiple images
CAROUSEL=$(posta_generate_carousel_pdf '["id1", "id2", "id3"]' "Weekly Highlights")
echo "$CAROUSEL" | jq '{media_id, page_count}'

# Generate a carousel PDF with text over background images (LinkedIn document post)
# Upload background images first (e.g. AI-generated), then composite slide text on top.
# Optional 3rd arg: a logo media ID shown bottom-right of every slide (upload it first).
DECK=$(posta_generate_text_carousel_pdf '[
  {"media_id":"bg1","title":"Turn any article into a carousel","body":"AI writes the slides."},
  {"media_id":"bg2","title":"On-brand copy","body":"One slide at a time."},
  {"media_id":"bg3","title":"Create once. Post everywhere.","body":"Start free at getposta.app"}
]' "Launch deck" "$LOGO_ID")
PDF_ID=$(echo "$DECK" | jq -r '.media_id')
# Attach the generated PDF to a LinkedIn post
posta_create_post "$(jq -n --arg m "$PDF_ID" '{caption:"New on the blog 👇", socialAccountIds:[123], mediaIds:[$m]}')"
```
