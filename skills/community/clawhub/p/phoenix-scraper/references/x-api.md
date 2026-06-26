# X API v2 Reference

Use X API v2 (bearer token) for X.com — do NOT scrape X.com directly.

## Auth
```
Authorization: Bearer $X_BEARER_TOKEN
```

## Endpoints

### Lookup user by username
```
GET https://api.twitter.com/2/users/by/username/:username
    ?user.fields=id,name,username,public_metrics
```

### Get user's recent tweets
```
GET https://api.twitter.com/2/users/:id/tweets
    ?max_results=10
    &tweet.fields=created_at,text,public_metrics,entities
    &exclude=retweets,replies
```

## Rate Limits (Free tier)
- 500k tweets/month read
- 1 app / 1 user token
- ~15 req/15min per endpoint

## Known User IDs
| Handle | User ID |
|--------|---------|
| @RupertLowe10 | 1121375429884039175 |
| @RestoreBritain_ | 1930183861176090624 |
| @kathrynporter26 | 3155110801 |
| @lnallalingham | 1799032775938326528 |
| @procurementfile | 1866094824480260096 |

## Python Example
```python
import urllib.request, json, os

token = os.environ["X_BEARER_TOKEN"]
user_id = "1121375429884039175"
url = f"https://api.twitter.com/2/users/{user_id}/tweets?max_results=10&tweet.fields=created_at,text"
req = urllib.request.Request(url)
req.add_header("Authorization", f"Bearer {token}")
with urllib.request.urlopen(req, timeout=15) as r:
    data = json.loads(r.read())
tweets = data.get("data", [])
```
