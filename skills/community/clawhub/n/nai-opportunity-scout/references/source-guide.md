# Source Configuration Guide

How to configure sources effectively for opportunity scanning.

## Supported Source Types

### Reddit

Format: `reddit:r/<subreddit>`

Reddit is the richest source for demand signals. People vent, ask for help, and
describe workarounds in detail.

**Best subreddits by niche:**

- **SaaS / software**: r/SaaS, r/startups, r/EntrepreneurRideAlong, r/microsaas
- **Small business**: r/smallbusiness, r/Entrepreneur, r/ecommerce
- **AI / automation**: r/AI_Agents, r/LocalLLaMA, r/AiForSmallBusiness, r/ChatGPT
- **Self-hosted / developer**: r/selfhosted, r/homelab, r/webdev, r/devops
- **Specific verticals**: r/realestateinvesting, r/freelance, r/accounting

**Tips:**
- Niche subreddits (under 100k members) often have higher signal density than large ones.
- Sort by "new" to catch emerging pain before it gets solved.
- r/SaaS and r/smallbusiness are gold mines for B2B product ideas.

### Hacker News

Format: `hackernews`

HN skews technical and founder-oriented. Good for developer tools, infrastructure,
and technical product gaps.

**HN-specific signals:**
- "Show HN" comment threads often reveal what's missing from presented solutions.
- "Ask HN" threads starting with "What tool do you wish existed?" are pure signal.
- Comments on product launches that say "I want this but for X" = adjacent opportunities.

### GitHub Issues

Format: `github:<owner>/<repo>`

Open issues and feature requests on popular repos are direct demand signals from
users who tried the tool and found it lacking.

**Tips:**
- Sort by most thumbs-up reactions — this surfaces the most-wanted features.
- Issues with "help wanted" or "good first issue" labels but no PRs = opportunity.
- Feature request issues that keep getting reopened = persistent unmet demand.

## Choosing Sources for Your Niche

**Start with 3-5 sources per niche.** More sources = more noise, not necessarily
more signal. Quality of subreddit selection matters more than quantity.

**Strategy:**
1. Pick 1-2 subreddits where your target users actually hang out
2. Add HN if your niche is technical
3. Add 1 GitHub repo if there's a dominant open-source tool in the space
4. Monitor results for 2-3 scans, then adjust: drop noisy sources, add discovered ones

## Keyword Configuration

### Signal Keywords (Required)

These identify demand expressions. The defaults cover most cases:
`wish, need, looking for, alternative to, frustrated, anyone solved, workaround,
hate that, shut up and take my money, I'd pay for, why is there no, someone should build`

### Niche Keywords (Required)

These scope the search to your domain. Be specific:
- Good: "invoicing small business", "self-hosted dashboard"
- Bad: "software", "app" (too broad, drowns in noise)

### Combining Keywords

The scanner combines niche + signal keywords into queries like:
`site:reddit.com/r/SaaS "I wish" invoicing small business`

This targets demand expressions within your specific domain and community.

## Scan Frequency

- **Daily**: High-velocity niches (AI, crypto, trending tech). Catches signals fast
  but generates more to review.
- **Weekly**: Stable niches (B2B tools, self-hosted). Less noise, still catches
  persistent signals. Recommended starting point.

## Avoiding Noise

1. **Be specific in niche keywords** — broad terms flood results with irrelevant posts
2. **Curate subreddits** — one well-chosen subreddit beats five vaguely related ones
3. **Review and adjust** — after each scan, note which sources produced signal vs noise
4. **Use history tracking** — recurring signals across scans are more reliable than one-offs
