# Lead Gen Search Playbook

## Core Search Query Templates

### By Industry + Title
```
"[job title]" "[industry]" site:linkedin.com
"VP Marketing" "SaaS" site:linkedin.com/in
"Head of Operations" "e-commerce" site:linkedin.com
```

### By Company Signals (Funded)
```
"[company] series A" OR "series B" site:techcrunch.com 2025 OR 2026
"[industry] startup funding" site:crunchbase.com
```

### By Hiring Signals (Buying Intent)
```
site:linkedin.com/jobs "[role]" "[company type]"
site:greenhouse.io "[role]"
"we're hiring" "[role]" "[industry]" site:linkedin.com
```

### By Tech Stack (Uses Competitor)
```
"powered by [competitor]" OR "built with [competitor]"
site:g2.com "[competitor]" reviews
"we use [tool]" site:linkedin.com
```

### By Community Presence
```
site:reddit.com/r/[niche] "looking for" OR "recommend" OR "help"
site:indiehackers.com "[pain point]"
"[job title]" site:twitter.com "[pain point keyword]"
```

### By Directory Listings
```
site:clutch.co "[industry]" "[location]"
site:capterra.com "[software category]" "[company size filter]"
site:g2.com/categories/[category]
```

### Company + Decision Maker Combo
```
"[company name]" "[job title]" site:linkedin.com
"[company name]" "contact" OR "team" site:[company domain]
```

---

## Trigger Event Searches

| Trigger | Search Pattern | Why It Works |
|---|---|---|
| New funding | `"[company] raises" 2026` | Flush with budget |
| New exec hire | `"[company] appoints" OR "joins as"` | New broom, new vendors |
| Product launch | `"[company] launches" OR "announces"` | Growth mode |
| Job posting | `site:linkedin.com/jobs "[role]" "[company]"` | Scaling = buying |
| Rebranding | `"[company] rebrand" OR "new identity"` | Active spend period |
| Expansion | `"[company] expands to" OR "opens in"` | New budgets unlocked |

---

## LinkedIn URL Patterns for Manual Prospecting

```
# Company page
linkedin.com/company/[company-name]

# People at a company
linkedin.com/search/results/people/?currentCompany=[company-id]&keywords=[title]

# Alumni of a company
linkedin.com/search/results/people/?pastCompany=[company-id]
```

---

## Email Format Discovery

For any company, try these patterns and validate:
1. `firstname@company.com`
2. `firstname.lastname@company.com`
3. `f.lastname@company.com`
4. `flastname@company.com`
5. `lastname@company.com`

To find the pattern:
- Search `"@company.com"` — often exposed in press releases, GitHub commits, blog author bios
- Check `hunter.io` format for the domain (free tier available)
- Look at company blog post authors — sometimes email is listed
- Check GitHub: `site:github.com "[company domain]" email`
