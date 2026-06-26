# Error Handling

## Common Errors and Solutions

### 1. Scenario Not Found

**Trigger**: `generate_content` returns "Scenario not found"
**Solution**: Call `list_scenarios` again and let user select from the list

### 2. Asset Library Empty

**Trigger**: `generate_content` returns "Asset library is empty"
**Solution**: Tell user they need to upload image assets first in the Web admin panel (/assets page)

### 3. Draft Still Generating

**Trigger**: `get_drafts` returns status=GENERATING
**Solution**: Wait 10-15 seconds and call `get_drafts` again. Poll up to 3 times. If still GENERATING after 3 polls, tell user to try again later.

### 4. Social Account Unavailable

**Trigger**: `publish_post` returns "accounts no longer active"
**Solution**: Tell user they need to re-bind social media accounts in the Web admin panel

### 5. Facebook/LinkedIn Missing Channel Selection

**Trigger**: `publish_post` returns "Missing channel selection"
**Solution**: Tell user they need to select a Page or Company Page for Facebook/LinkedIn in the Web settings page

### 6. Caption Exceeds Platform Character Limit

**Trigger**: `publish_post` returns character limit error
**Solution**: Use `regenerate_draft` with feedback="Caption must be under N characters"

### 7. Draft Has No Assets for Regeneration

**Trigger**: `regenerate_draft` returns "No associated assets"
**Solution**: Tell user this draft lacks image assets and suggest regenerating via `generate_content`

### 8. Publishing Failed

**Trigger**: `get_post_status` returns status=failed
**Solution**: Display error message (usually Token expired or platform API limit). Suggest user re-authorize social media accounts in Web panel and retry.

## Polling Strategy

```
After generate_content:
  Wait 15s → get_drafts
  If still GENERATING → wait 10s → get_drafts
  If still GENERATING → wait 10s → get_drafts
  If still GENERATING → tell user "Generation is taking longer, please check back later"

After publish_post:
  Wait 30s → get_post_status
  If pending → wait 15s → get_post_status
  If still pending → tell user "Publishing in progress, check back later"
```
