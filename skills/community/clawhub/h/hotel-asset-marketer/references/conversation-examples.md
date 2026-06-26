# Conversation Examples

This document shows complete conversation flows for HotelPost MCP, covering various scenarios and tool combinations.

---

## Example 1: Basic Flow — Generate and Publish to Instagram

```
User: Generate a post and publish it to Instagram

Assistant: Let me check what marketing scenarios are available first.
→ call list_scenarios
Assistant: Available scenarios:
1. Instagram — B2C Visual Dreams
2. Century-Old Heritage — Tradition & Innovation
3. Business Select — Exclusive for Business Travelers
...
Which scenario would you like?

User: Century-Old Heritage

Assistant: Generating post content for "Century-Old Heritage" scenario...
→ call generate_content(scenarioId="xxx", language="en")
Assistant: 📝 Draft list (3 different angles):
• [GENERATING] Workday Light Between Shadows — slotIndex: 0, Images: 3
• [GENERATING] Century Heritage · Legacy — slotIndex: 1, Images: 3
• [GENERATING] Explore Century-Old Heritage — slotIndex: 2, Images: 3
→ Wait 15s → call get_drafts(scenarioId="xxx")
Assistant: 📋 3 drafts available:
• [ACTIVE] Workday Light Between Shadows — v1, Images: 3
  Common Copy: Morning light through old windows, reflecting the gentleness of time...
  Instagram: Every beam of light is a story of time...
• [ACTIVE] Century Heritage · Legacy — v1, Images: 3
• [ACTIVE] Explore Century-Old Heritage — v1, Images: 3
All drafts are ready.

User: Post the first one to Instagram

Assistant: Let me confirm your Instagram account first.
→ call list_connections
Assistant: 3 social accounts bound:
1. 📸 INSTAGRAM — demo_brand
2. 📘 FACEBOOK — Demo Brand Page
3. 🐦 X — demo_brand

Assistant: Publishing "Workday Light Between Shadows" to Instagram...
→ call publish_post(draftId="draft_demo_001", connectionIds=["conn_instagram_demo"])
Assistant: ✅ Publishing task submitted
📋 1 publishing task queued
🆔 Post ID: post_xxx
→ Wait 30s → call get_post_status(draftId="xxx")
Assistant: 📊 Publishing status (1 record)
📸 INSTAGRAM — ✅ published
   Published at: 2026/3/12 15:14
   Link: https://example.com/posts/demo-post-001
✅ Success: 1 | ❌ Failed: 0
```

---

## Example 2: Multi-Platform Publishing

```
User: Generate a post and publish to Facebook and LinkedIn

Assistant: [list_scenarios → user selects → generate_content → get_drafts]
Assistant: Draft generated:
• [ACTIVE] Workday Light Between Shadows — v1, Images: 3

User: This one, publish to Facebook and LinkedIn

Assistant: → call list_connections
Assistant: 4 social accounts bound:
1. 📸 INSTAGRAM — demo_brand
2. 📘 FACEBOOK — Demo Brand Page
3. 🐦 X — demo_brand
4. 💼 LINKEDIN — Demo Brand Team

Assistant: Publishing to Facebook and LinkedIn...
→ call publish_post(draftId="draft_demo_002", connectionIds=["conn_facebook_demo", "conn_linkedin_demo"])
Assistant: ✅ Publishing task submitted
📋 2 publishing tasks queued
→ Wait 30s → call get_post_status(draftId="xxx")
Assistant: 📊 Publishing status (2 records)
📘 FACEBOOK — ✅ published
   Link: https://example.com/profiles/demo-brand
💼 LINKEDIN — ✅ published
   Link: https://example.com/companies/demo-brand
✅ Success: 2 | ❌ Failed: 0
```

---

## Example 3: Scheduled Publishing

```
User: Generate a Christmas post, schedule for 2pm tomorrow

Assistant: [select scenario → generate_content → get_drafts]
Assistant: Draft generated:
• [ACTIVE] Christmas Special — v1, Images: 4
Confirm which platforms to publish to?

User: All platforms

Assistant: → call list_connections
Assistant: 4 social accounts bound:
1. 📸 INSTAGRAM — demo_brand
2. 📘 FACEBOOK — Demo Brand Page
3. 🐦 X — demo_brand
4. 💼 LINKEDIN — Demo Brand Team

Assistant: Setting up scheduled publishing...
→ call schedule_post(draftId="xxx", connectionIds=[...], scheduledAt="2026-12-25T06:00:00Z")
Assistant: ✅ Scheduled publishing set
📅 Publish time: 2026/12/25 14:00 (UTC+8)
🆔 Post ID: post_xxx
Will automatically publish to 4 social accounts at the scheduled time.
Use list_posts to view all scheduled posts.
```

---

## Example 4: Modify Draft — Condense Copy

```
User: The copy is too long, condense it

Assistant: → call regenerate_draft(draftId="xxx", feedback="Condense copy to under 100 characters")
Assistant: Regeneration submitted...
→ Poll get_drafts(draftId="new_draftId")
Assistant: New draft ready:
• [ACTIVE] Workday Light Between Shadows — v2, Images: 3
  Common Copy: Morning light, old windows, gentle time. Step into...
Ready to publish if satisfied?
```

---

## Example 5: Modify Draft — Regenerate Specific Platform

```
User: The Instagram copy isn't suitable, can you regenerate just the Instagram version?

Assistant: → call regenerate_draft(draftId="xxx", feedback="More suitable for Instagram style", platform="instagram")
Assistant: Instagram copy regenerated...
→ call get_drafts(draftId="new_draftId")
Assistant: Instagram copy updated:
  Instagram: Capture the gentleness of every beam of light, wander in time...
Ready to publish when satisfied.
```

---

## Example 6: Modify Draft — Switch Language (English Post)

```
User: Translate this post to English and post to X

Assistant: → call regenerate_draft(draftId="xxx", language="en", platform="x")
Assistant: Second English variant generated...
→ call get_drafts(draftId="new_draftId")
Assistant: X (Twitter) copy:
  X: Step into the soft morning light, where time whispers...
→ call list_connections
Assistant: 🐦 X — demo_brand

Assistant: Publishing English version to X...
→ call publish_post(draftId="draft_demo_en_001", connectionIds=["conn_x_demo"])
Assistant: ✅ X (Twitter) published successfully!
```

---

## Example 7: Modify Draft — Add Price Information

```
User: Regenerate this and add room rate info and booking link

Assistant: → call regenerate_draft(draftId="xxx", feedback="Add room rate: Standard room 688 yuan/night, breakfast included. Add booking guidance")
Assistant: Regeneration submitted...
→ Poll get_drafts(draftId="new_draftId")
Assistant: New draft ready:
• [ACTIVE] Workday Light Between Shadows — v2, Images: 3
  Common Copy: Morning light through old windows... Standard room 688 yuan/night, breakfast included.
  Book now: https://...
Ready to publish when satisfied?
```

---

## Example 8: Query Post List — Filter by Status

```
User: Show me recently failed posts

Assistant: → call list_posts(status="FAILED")
Assistant: 📋 Post list (2 posts, page 1)
❌ Workday Light Between Shadows
   ID: post_xxx | Status: FAILED | Scheduled: Not scheduled
   └─ ❌ INSTAGRAM: failed (Token expired)
   └─ ✅ FACEBOOK: published
❌ Christmas Special — Scheduled post
   ID: post_yyy | Status: FAILED | Scheduled: 2026/12/25 14:00
   └─ ❌ INSTAGRAM: failed (Permission revoked)

Assistant: Suggest re-authorizing these accounts in the Web panel and retry. Want me to check the specific failure reasons?
```

---

## Example 9: Query Post List — Paginated

```
User: Show me all my recent posts

Assistant: → call list_posts()
Assistant: 📋 Post list (15 posts, page 1)
✅ Workday Light Between Shadows — 2026/3/12 15:14
   └─ ✅ INSTAGRAM: published
   └─ ✅ FACEBOOK: published
📅 Christmas Special — Scheduled 2026/12/25 14:00
   └─ 🔘 INSTAGRAM: pending
⚠️ New Year Campaign — Partial success
   └─ ✅ INSTAGRAM: published
   └─ ⚠️ FACEBOOK: failed (Content violated policy)
❌ New Year Special — Failed
   └─ ❌ X: failed (Token expired)

More posts available, use page: 2 to view next page.
```

---

## Example 10: Query Publishing Status — Get Platform Links

```
User: What's the status of the post from March 5th?

Assistant: → call list_posts(page=1, pageSize=10)
Assistant: 📋 Post list (page 1)
...
Assistant: Which post? Page 1 has:
1. Workday Light Between Shadows — ID: post_demo_001
2. Century Heritage · Legacy — ID: post_demo_002
3. Explore Century-Old Heritage — ID: post_demo_003

User: The second one

Assistant: → call get_post_status(postId="post_demo_002")
Assistant: 📊 Publishing status (3 records)
📸 INSTAGRAM — ✅ published
   Published at: 2026/3/5 10:30:00
   Link: https://example.com/posts/demo-post-002
📘 FACEBOOK — ✅ published
   Link: https://example.com/profiles/demo-brand
💼 LINKEDIN — ✅ published
   Link: https://example.com/companies/demo-brand
✅ Success: 3 | ❌ Failed: 0
```

---

## Example 11: Check Account Binding Status

```
User: Can my Instagram account post?

Assistant: → call list_connections
Assistant: 4 social accounts bound:
1. 📸 INSTAGRAM — demo_instagram_account (ID: conn_instagram_demo)
2. 📘 FACEBOOK — Demo Brand Page (ID: conn_facebook_demo)
3. 🐦 X — demo_social_account (ID: conn_x_demo)
4. 💼 LINKEDIN — Demo Brand Team (ID: conn_linkedin_demo)

Assistant: Instagram account demo_instagram_account is active and ready to publish.
```

---

## Example 12: View Draft Details (Platform-Specific Copy)

```
User: Let me see what copy each platform has for this draft

Assistant: → call get_drafts(draftId="xxx")
Assistant: 📝 Draft Details
ID: draft_xxx
Status: ACTIVE
Title: Workday Light Between Shadows
slotIndex: 0
Images: 3
Version: v2

Common Copy: Morning light through old windows, reflecting the gentleness of time...

Platform-specific Copy:
X(Twitter): Morning light, old windows, gentle time. Step into this century-old gem...
Facebook: Every beam of light is a story of time. Welcome to experience...
Instagram: Capture the gentleness of every beam of light, wander in time...
LinkedIn: Tradition and innovation coexist, invite you to witness century-old craftsmanship...
🖼️ Images:
  1. https://cdn.xxx.com/img1.png?sig=...
  2. https://cdn.xxx.com/img2.png?sig=...
  3. https://cdn.xxx.com/img3.png?sig=...
```

---

## Example 13: Polling Wait for Draft Generation

```
User: Generate a new post for me

Assistant: → call list_scenarios
Assistant: 📋 5 marketing scenarios:
• Business Select — Exclusive for Business Travelers (ID: sc_xxx)

User: Business Select

Assistant: → call generate_content(scenarioId="sc_xxx", language="en")
Assistant: 📝 Draft list (2 different angles):
• [GENERATING] Choice for Business Elite — slotIndex: 0, Images: 3
• [GENERATING] Top Choice for Travelers — slotIndex: 1, Images: 3
Some drafts still generating, please check back later.

Assistant: Drafts still generating, checking again...
→ Wait 15s → call get_drafts(scenarioId="sc_xxx")
Assistant: 📋 2 drafts:
• [ACTIVE] Choice for Business Elite — v1, Images: 3
• [ACTIVE] Top Choice for Travelers — v1, Images: 3
All drafts ready. Ready to publish.
```

---

## Example 14: Multi-Language Generation — Chinese & English Posts

```
User: Generate a post, I need two English variants

Assistant: [select scenario → generate_content(language="en")]
Assistant: First English draft generated:
• [ACTIVE] Workday Light Between Shadows — v1, Images: 3

Assistant: Generating a second English variant...
→ call regenerate_draft(draftId="xxx", language="en")
Assistant: Second English variant generated...
→ call get_drafts(draftId="new_draftId")
Assistant: Second English draft:
• [ACTIVE] Light and Shadow — v1, Images: 3
  Common Copy: Morning light through old windows...

Assistant: Both English variants are ready. Which one would you like to publish?
```
