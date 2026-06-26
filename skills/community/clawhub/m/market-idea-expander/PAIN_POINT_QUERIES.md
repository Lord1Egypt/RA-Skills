# Pain Point Research Query Templates

Generate platform-specific search queries for: Reddit, X (Twitter), Threads, LinkedIn, and Google.

## Reddit

```
"{Niche}" (
  site:reddit.com
  inurl:comments|inurl:thread
  | intext:"I think"|"I feel"|"I was"|"I have been"|"I experienced"|
  "my experience"|"in my opinion"|"IMO"|"my biggest struggle"|
  "my biggest fear"|"I found that"|"I learned"|"I realized"|
  "my advice"|"struggles"|"problems"|"issues"|"challenge"|
  "difficulties"|"hardships"|"pain point"|"barriers"|"obstacles"|
  "concerns"|"frustrations"|"worries"|"hesitations"|
  "what I wish I knew"|"what I regret"
)
```

## X / Twitter

Generate **3 separate X search queries** targeting different pain point angles. Use X's native search at `x.com/search`.

**Query 1 — Frustration & Rants:**
```
"{Niche}" ("I hate"|"so frustrating"|"why is it so hard"|"nobody talks about"|
"my problem with"|"rant"|"ugh"|"tired of"|"sick of"|"done with")
-filter:retweets min_faves:5 lang:en
```

**Query 2 — Wishes & Gaps:**
```
"{Niche}" ("wish there was"|"can't find a good"|"why doesn't"|"someone should build"|
"there should be"|"nobody makes a"|"impossible to find"|"why is there no")
-filter:retweets min_faves:3 lang:en
```

**Query 3 — Confessions & Realizations:**
```
"{Niche}" ("unpopular opinion"|"honest take"|"real talk"|"be honest"|
"nobody tells you"|"I learned the hard way"|"I wasted"|"mistake I made"|
"what I wish I knew"|"regret")
-filter:retweets min_faves:5 lang:en
```

> 💡 **X research tip:** Also check the **"Latest" tab** (not "Top") so you see raw unfiltered posts, not just viral ones. Look for replies too — that's where real frustration lives.

## Threads

Generate **3 separate Threads search queries**. Search directly at `threads.net/search`.

**Query 1 — Pain Points & Struggles:**
```
"{Niche}" "my biggest struggle" OR "nobody talks about" OR "real talk" OR
"honest review" OR "I've been dealing with" OR "why is it so hard"
```

**Query 2 — Community Opinions:**
```
"{Niche}" "unpopular opinion" OR "controversial take" OR "hot take" OR
"am I the only one" OR "can we talk about" OR "does anyone else"
```

**Query 3 — Lessons & Regrets:**
```
"{Niche}" "things I wish I knew" OR "what I learned" OR "don't make my mistake" OR
"this took me years" OR "advice I wish I got" OR "what no one tells you"
```

> 💡 **Threads research tip:** Also search the **niche hashtag** (`#{niche}`) and sort by Recent. Threads tends to have longer, more opinion-heavy posts than X — great for emotional language and specific complaints you can use verbatim in your copy.

## LinkedIn

```
"{Niche}" (
  "challenge I face"|"what nobody tells you"|"lesson learned"|
  "mistake I made"|"wish I knew earlier"|"real talk"|
  "industry problem"|"gap in the market"|"what clients ask me"
) filter:posts
```

## Google (Validation)

```
"{Niche}" ("problems with"|"issues with"|"frustrating"|"doesn't work") site:reddit.com OR site:quora.com
"{Niche} alternatives" OR "{Niche} competitors" site:reddit.com
best "{Niche}" forum complaints
```

## Running These Queries

If a web search tool is available, these queries can be run directly to collect results. Reddit and X often restrict automated access to search results — if a query returns nothing useful, fall back to a broader query or suggest the user run it manually in their browser.
