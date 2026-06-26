# Phrase blacklist (Daily chat + Social media only)

Purpose: AI detectors (and humans) often pick up **overrepresented LLM phrases** and **template-shaped writing**. Use this as a **post-draft scrub** (manual rewrite, not find/replace).

How to use:
1) Scan for blacklist phrases + templated closers
2) Rewrite in-context with simpler, specific language (or delete)
3) Delete filler sentences that add no new meaning
4) Avoid heavy punctuation normalization (don’t mass-replace quotes/dashes)

---

## Global (all supported scenarios)
Avoid unless the user explicitly wants a formal/PR tone:
- “delve into”, “dive into”, “unpack” (as a crutch)
- “in today’s (fast-paced) world”, “in this day and age”
- “it is important to note that…”, “it’s worth mentioning…”, “needless to say…”
- “a testament to”, “in the realm of”, “the landscape of” (generic)
- “robust”, “comprehensive”, “powerful”, “cutting-edge”, “groundbreaking”, “revolutionary”, “unparalleled”
- “leverage”, “unlock”, “seamlessly”, “synergy”, “holistic”, “pivotal”
- filler transitions: “moreover/furthermore/additionally” when overused
- excessive em-dashes (—) as default punctuation

Prefer:
- short, direct sentences
- concrete nouns/verbs
- one clear point per sentence

---

## daily_chat (texts / DMs)
### Avoid
- therapy-speak unless user speaks that way: “I hear you”, “hold space”, “validate”
- over-polished apologies: “I sincerely apologize for any inconvenience”
- mini-essays with perfect symmetry

### Use instead
- small, human acknowledgments: “my bad”, “that’s on me”, “totally fair” (when appropriate)
- specific next step: “I’ll do X by Y” (only if user provided Y or asked for it)

---

## social (all platforms)
### Avoid
- CTA spam: “Like/Share/Comment below” (unless user asked)
- generic hooks: “You won’t believe…”, “Here’s the thing…”, “Let’s dive in”
- listicle framing by default: “10 ways to…” (unless requested)
- corporate cadence: “I’m thrilled to announce…”, “proud/excited to share…” (unless that’s explicitly desired)
- fake humility / humblebrag templates

### Use instead
- a concrete first line: what happened / what you noticed / what you learned
- a slightly imperfect rhythm (one short sentence can help)

---

## Platform-specific notes
### social_x (X/Twitter)
Avoid:
- long paragraphs
- too many hashtags
- over-formal transitions
Prefer:
- short lines; one punchy sentence; occasional fragment

### social_reddit
Avoid:
- marketing tone, “DM me for details”, “limited spots”
Prefer:
- directness, context, one real question at end (posts)

### social_linkedin
Avoid:
- “Agree?” / “Thoughts?” every time as a crutch
- influencer clichés: “I was today years old…”, “Let that sink in”, “Game changer”, “Humbled”
Prefer:
- one clear takeaway + one concrete example; understated tone

### social_instagram / social_tiktok
Avoid:
- over-explaining what the viewer can see
Prefer:
- short, visual, caption-y phrasing

### social_xiaohongshu (小红书)
Avoid:
- “宝子们/姐妹们冲/狠狠爱了/YYDS/天花板/闭眼入” (unless user asked for that vibe)
- “小红书爆款标题模板”腔
Prefer:
- 具体、朴素、有细节的表达

### social_wechat_moments (朋友圈)
Avoid:
- 教程腔、营销腔
Prefer:
- 更私人、更克制的几句 + 一个小细节
