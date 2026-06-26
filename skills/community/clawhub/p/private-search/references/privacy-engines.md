# Privacy Search Engines — Reference Guide

## Brave Search

**Website:** https://search.brave.com  
**API:** https://api.search.brave.com  
**Docs:** https://api.search.brave.com/app/documentation/

### Pricing
| Plan | Queries/mo | Cost |
|------|-----------|------|
| Free | 2,000 | $0 |
| Basic | 20,000 | $3/mo |
| Pro | 200,000 | $30/mo |

### Key Features
- Fully independent search index (not Google/Bing)
- No user tracking or query logging for monetization
- Strong privacy policy
- Good coverage for English + major European languages

### Setup
```bash
export BRAVE_API_KEY=your_key_here
export PRIVATE_SEARCH_ENGINE=brave
```

### API Example
```bash
curl -H "X-Subscription-Token: $BRAVE_API_KEY" \
  "https://api.search.brave.com/res/v1/web/search?q=your+query&count=5"
```

---

## Kagi

**Website:** https://kagi.com  
**API:** https://kagi.com/api  
**Docs:** https://help.kagi.com/kagi/api/

### Pricing
| Plan | Cost | Notes |
|------|------|-------|
| Starter | $5/mo | 300 searches/mo |
| Professional | $10/mo | Unlimited |
| Ultimate | $25/mo | Unlimited + premium models |

### Key Features
- No ads, ever
- Highest quality results (users consistently rate above Google)
- Personalizable result ranking
- Premium: Orion browser, Kagi AI assistant

### Setup
```bash
export KAGI_API_KEY=your_key_here
export PRIVATE_SEARCH_ENGINE=kagi
```

### API Example
```bash
curl -H "Authorization: Bot $KAGI_API_KEY" \
  "https://kagi.com/api/v0/search?q=your+query&limit=5"
```

---

## SearXNG (Self-Hosted)

**GitHub:** https://github.com/searxng/searxng  
**Docs:** https://docs.searxng.org/

### Cost
- Free (self-hosted)
- Server cost: ~$4–$6/mo on Hetzner CX11

### Key Features
- Fully self-hosted — zero third-party dependency
- Aggregates results from multiple sources
- Completely private (no queries leave your server)
- Highly configurable

### Quick Deploy (Docker)
```bash
docker run -d \
  -p 8080:8080 \
  -v ./searxng:/etc/searxng \
  --name searxng \
  searxng/searxng:latest
```

### Setup with this skill
```bash
export SEARXNG_URL=http://localhost:8080
export PRIVATE_SEARCH_ENGINE=searxng
```

### API Example
```bash
curl "http://localhost:8080/search?q=your+query&format=json&pageno=1"
```

---

## Tracking Parameter Stripping

When `PRIVATE_SEARCH_STRIP_TRACKING=true`, the skill strips these params from all result URLs:

**UTM params:** utm_source, utm_medium, utm_campaign, utm_term, utm_content  
**Google:** gclid, gclsrc, dclid, gbraid, wbraid  
**Facebook:** fbclid, fb_action_ids, fb_action_types, fb_source  
**Microsoft:** msclkid  
**General:** ref, referrer, source, affiliate_id, partner_id  

This ensures no affiliate/tracking identifiers leak from search results into your agent's browsing sessions.

---

## Engine Recommendation Guide

| User Type | Recommended Engine |
|-----------|-------------------|
| Casual user, wants easy setup | Brave (free tier) |
| Power user, quality matters most | Kagi Professional |
| Developer, privacy absolutist | SearXNG self-hosted |
| Enterprise / team | SearXNG self-hosted + Brave fallback |
