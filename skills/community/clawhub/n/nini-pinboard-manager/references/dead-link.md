# Dead Link Detection Mode

Check all bookmarks for broken URLs and report results for user action.

## Step 1: Fetch all bookmarks

Same as Tag Audit Step 1 (reuse `/tmp/pinboard_all.json` cache if available).

## Step 2: Check links in batches

Process 10 URLs per batch using HTTP HEAD requests:

```bash
# HEAD request with 10 second timeout
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -L --max-redirs 5 -I -m 10 "URL")
```

Classification (based on final status after following redirects):

| Status | Meaning | Action |
|--------|---------|--------|
| 2xx | Working | No action |
| 403, 405 | HEAD rejected | Retry with GET |
| 4xx (other) | Broken | Report to user |
| 5xx | Server error | Report to user |
| 000 | Timeout/unreachable | Report to user |

For HEAD-rejected URLs, retry once with GET:

```bash
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -L --max-redirs 5 -m 10 "URL")
```

## Step 3: Present results

Show broken links grouped by status:

```text
### Dead Links Found (12 items)

#### 404 Not Found (5)
1. 「Article title」 — https://example.com/gone
   Tags: programming
   -> [delete] [keep] [skip]

2. ...

#### Timeout (4)
1. 「Slow site article」 — https://slow-site.com/article
   Tags: reference
   -> [delete] [keep] [skip]

#### Server Error 5xx (3)
1. ...
```

## Step 4: Apply user decisions

For deletions:

```bash
curl -s "https://api.pinboard.in/v1/posts/delete?auth_token=$PINBOARD_AUTH_TOKEN&format=json&url=ENCODED_URL"
sleep 3  # Rate limit
```

## Step 5: Summary

```text
Dead Link Check Complete
- Links checked: 200
- Working: 188
- Broken: 8 (deleted: 5, kept: 3)
- Timeout: 4 (deleted: 1, kept: 3)
```
