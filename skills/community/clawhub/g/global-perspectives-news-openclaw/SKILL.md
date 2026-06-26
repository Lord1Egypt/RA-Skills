---
name: global-perspectives-news
description: Generate a personalized global news briefing by asking about your interests, then searching the web and delivering a structured, readable digest. Use this to stay informed on topics that matter to you without manual searching.
metadata:
  clawdbot:
    emoji: "🌍"
    requires:
      anyBins: []
---

## Purpose

Generate a personalized news briefing tailored to your interests. You tell Claw what topics you care about and how you want the output—Claw searches the web and delivers a clean, structured digest of the most relevant stories from the past 24-48 hours.

**Requires:** Tavily MCP (for live web search). If Tavily is not connected, Claw will note it and offer to proceed with its training knowledge as a fallback.

---

## Key Concepts

### The Briefing Model
1. **Signal over noise** — only stories with real substance
2. **Scannable structure** — grouped by topic, with summaries and source links
3. **Configurable depth** — headlines only, or with context and implications

### Story Quality Criteria
Stories must meet at least two of:
- Published or updated in the last 48 hours
- From a recognized publication or primary source
- Contains new information (not just opinion or recap)
- Directly relevant to the stated topic

---

## Application

### Global Navigation Rules
- **"back" / "上一步"** — go back to previous step
- **"restart" / "重新开始"** — go back to Step 1
- **"skip" / "跳过"** — use default value
- **"done" / "算了"** — exit immediately

---

### Step 0: Check for Saved Preferences

Check if `~/.claw/data/global-perspectives-news-prefs.json` exists.

**If exists**, greet in saved language, show topics only:
> 上次你看了 [topics]，今天还想看这些吗？ *(Chinese/Bilingual)*
> Last time you followed: [topics]. Want the same today? *(English/Bilingual)*
> 1. Yes, go · 2. Yes, change something · 3. No, start fresh

**If no file**, go to Step 1.

---

### Step 1: Ask About Interests

> "Welcome! What would you like to read about today?
>
> 1. Technology & AI · 2. Finance & Economy · 3. Geopolitics & World Affairs
> 4. Science & Research · 5. Career & Workplace · 6. Business & Strategy
> 7. Environment & Climate · 8. Sports · 9. Entertainment & Media
> 10. Health & Lifestyle · 11. Law, Crime & Justice · 12. Travel & Places
> 13. Culture & Society · 14. Just surprise me · 15. Top 10 by location"

**CRITICAL — mandatory steps by mode:**

| Mode | Step 2 | Step 3 | Step 4 |
|------|--------|--------|--------|
| Specific topics (1-13) | ✅ | ✅ | ✅ |
| Just surprise me (14) | ✅ | ⛔ Skip | ✅ |
| Top 10 by Location (15) | ⛔ Skip | ⛔ Skip | ✅ |

---

### Step 2: Ask About Media Source Countries

> "Which countries' media would you like to draw from?
>
> **Official Media:**
> 1. United States — CNN, NYT, WSJ, The Atlantic
> 2. United Kingdom — BBC, The Guardian, Financial Times
> 3. Europe — Der Spiegel (Germany), Le Monde (France), Kyiv Independent (Ukraine)
> 4. Russia — RT, TASS, Kommersant (English editions)
> 5. China — SCMP, Caixin, Xinhua, Global Times (English editions)
> 6. Middle East — Al Jazeera, Arab News, Jerusalem Post, Haaretz
> 7. Japan — Nikkei Asia, Japan Times
> 8. Singapore / Asia Pacific — Straits Times, CNA
> 9. India — The Hindu, Times of India, Economic Times, NDTV
> 10. Latin America — Folha de S.Paulo, O Globo (Brazil + non-Hispanic LATAM, Portuguese)
> 11. Hispanic World — Infobae, El País América (Spanish-speaking Americas + Spain)
> 12. Africa — AllAfrica, Daily Maverick, The East African, Premium Times
> 13. Canada — Globe and Mail, CBC News, Toronto Star, Maclean's
> 14. Australia & New Zealand — ABC News Australia, Sydney Morning Herald, RNZ
> 15. South Korea — Korea Herald, Chosun Ilbo (English), Hankyoreh
> 16. Turkey — TRT World, Hurriyet Daily News, Daily Sabah
> 17. Southeast Asia — Rappler (PH), Bangkok Post, Jakarta Post, CNA
>
> **Social Media:**
> 18. Weibo — Chinese public sentiment via trending topics (热搜榜)
> 19. Xiaohongshu / RedNote — Chinese lifestyle, consumer trends, Gen Z culture
> 20. TikTok / 抖音 — global and Chinese viral content, youth trends
> 21. Instagram — visual culture, lifestyle, brand sentiment
> 22. Telegram — war zones, political movements, opposition channels
> 23. LinkedIn — professional sentiment, industry trends, executive commentary
> 24. Twitter / X — global real-time public reaction, trending hashtags
> 25. Reddit — English-language community discussion and analysis
>
> **No filter:**
> 26. Global / No preference — let the best sources win
>
> Pick multiple (e.g. '1, 4, 5, 18') or 26 for no filter.
>
> **Note:** Latin America (#10) covers Portuguese-speaking Brazil and non-Hispanic LATAM. Hispanic World (#11) covers Spanish-speaking Americas AND Spain — Infobae and El País operate across the entire Spanish-speaking world, not just Latin America."

---

### Step 3: Narrow Down to Subtopics

Present menus only for selected categories. Shortcut: "all" / "全部" = select all.

**Technology & AI:** LLMs & AI research / AI products / Cloud native & K8s / Cybersecurity / Consumer tech / All

**Finance & Economy:** Global markets / Startups & VC / Crypto & Web3 / Fintech / Real estate / Commodities & energy / Central banks / Personal finance / All

**Geopolitics & World Affairs:** US politics / China & Asia Pacific / Europe / Middle East / Global trade & sanctions / Latin America / Africa / South Asia / All

**Science & Research:** AI & ML papers / Space / Climate / Health & medicine / Biology / Physics & quantum / Robotics / Psychology / Archaeology / All

**Career & Workplace:** Remote work / Tech layoffs / Salary / Future of work & AI impact / Gig economy / Entrepreneurship / Workplace culture & DEI / All

**Business & Strategy:** M&A / IPOs / Corporate strategy / Regulatory & antitrust / Supply chain / All

**Environment & Climate:** Climate change / Green energy / Environmental policy / Natural disasters / Conservation / ESG / All

**Sports:** Football/Soccer / Basketball / Formula 1 / Tennis / Olympics / Esports / Other / All

**Entertainment & Media:** Movies / Music / Gaming / Celebrities / Streaming / Awards / All

**Health & Lifestyle:** Fitness / Nutrition / Mental health / Medical breakthroughs / Public health / Wellness / All

**Law, Crime & Justice:** Criminal cases / Court rulings / Regulatory enforcement / White-collar crime / Human rights / International law / All

**Travel & Places:** Destinations / Aviation / Tourism trends / Urban development / Immigration / Outdoor & adventure / Luxury / Budget / All

**Culture & Society:** Social movements / Education / Demographics / Religion / Internet culture / Arts & literature / Food culture / Fashion / Youth & Gen Z / Gender & diversity / Urban life / All

---

### Step 4: Reading Language and Depth

**CRITICAL: Always show ALL 7 language options (A through G) in full. Never abbreviate or show a subset. Users must see every option before choosing.**

> "Two quick settings:
>
> 1. **Reading language:**
>    - A. English
>    - B. Chinese 中文
>    - C. Spanish Español
>    - D. French Français
>    - E. Japanese 日本語
>    - F. German Deutsch
>    - G. Bilingual — pick any two (e.g. "G, English + Chinese")
>
> 2. **Depth:**
>    - A. Headlines only (title + one line)
>    - B. Standard (title + 2-sentence summary)
>    - C. Deep (title + summary + why it matters)"

Default: English, Standard.

---

### Step 5: Search for News

- Query: `[specific subtopic] [current year] [intent keyword]`
- Time range: last 48-72 hours · Target: 3-5 results per topic

| Topic | Avoid | Use instead |
|-------|-------|-------------|
| Sports | `football news latest` | `Champions League results March [year]` |
| AI research | `AI news latest` | `arxiv LLM [year] latest` |
| Geopolitics | `Iran Israel news` | `Iran Israel war update [date]` |
| Finance (markets) | `stock market news` | `S&P 500 today [date]`, `Fed rate decision [year]` |
| Business (M&A) | `company acquisition news` | `merger acquisition [industry] [year]` |
| Culture (food) | `food news latest` | `food trend [year]`, `viral food [platform] [year]` |

---

### Step 6: Generate the Briefing

```
# Global Perspectives News — [Date]

## [🤖/💰/🌍...] [Topic Name]

- **[Story Title]**
  [Summary.]
  Source: [Publication] — [URL]

## Today's Takeaway · 今日总结
[1-2 sentences connecting the dots across all stories.]

---
*Generated [date] · Sources: [regions] · Language: [lang] · Depth: [depth]*
```

**If social media selected:**
```
## Social Pulse · 社交舆论
[Trending topics and sentiment signals.]
⚠️ Social media = sentiment signal, not verified fact.
```

**Emoji guide:** 🤖 AI · ☁️ Cloud · 💰 Finance · 🌍 Geopolitics · 🔬 Science · 💼 Careers · 🔐 Security · 📱 Tech · 📊 Business · 🌿 Environment · ⚽ Sports · 🎬 Entertainment · ❤️ Health · ⚖️ Law · ✈️ Travel · 🌐 Culture

---

### Step 7: Offer Next Steps

**Part A — Save preferences:**
> 1. Yes, save as default · 2. No, ask me every time

Saves to `~/.claw/data/global-perspectives-news-prefs.json`.

**Part B — Actions:**
> 1. Dive deeper on a story · 2. Save briefing to file
> 3. Change topics · 4. Change everything · 5. Done

---

## Common Pitfalls

**Pitfall 1 — Too many topics:** After Step 3, if total subtopics > 10, offer: Prioritize top 8 / Keep all + Headlines-only / Keep all + full depth.

**Pitfall 2 — Stale results:** Always include `latest` in queries. Flag stories > 72 hours old.

**Pitfall 3 — Duplicate stories:** File each story under the single most relevant topic.

**Pitfall 4 — Opinion pieces:** Prioritize primary sources. Label op-eds explicitly.

**Pitfall 5 — Skipping language/depth:** Step 4 is MANDATORY for every run.

**Pitfall 6 — Tavily not connected:** Offer training-knowledge fallback with cutoff caveat.
