# GTM Coach — period playbooks

Extended foundation/reference for [SKILL.md](SKILL.md). Normal sessions load one stage SOP and one project-type SOP for the CMO board, plus `channels/index.md` for scoring. Load a channel SOP only after the founder chooses to execute that channel. Load this longer document only when deeper cross-stage principles are needed; do not blend unrelated sections.

These SOPs match how Nichestarter, NicheReach, and NicheMatch already teach founders on the site. Complementary skills (same token, later): [NicheMatch onboarding](../nichematch-agent-onboarding/SKILL.md).

## Evidence-backed principles (use judgment, not slogans)

These are the default operating principles for an idea developer. They work even when there is no existing product and no Nichestarter account.

1. **Launch to learning, not applause.** Put the smallest usable version in front of someone quickly. Paul Graham: [launch fast, understand users, and prefer a few users who love you](https://www.paulgraham.com/13sentences.html). YC: a press launch can wait; getting any customer using an MVP cannot ([How to plan an MVP](https://www.ycombinator.com/library/6f-how-to-plan-an-mvp)).
2. **Recruit initial users manually.** Do things that do not scale: find people with the problem, onboard them yourself, and watch where they fail ([Paul Graham](https://paulgraham.com/ds.html), [YC first customers](https://www.ycombinator.com/library/Ip-how-to-get-your-first-customers)).
3. **Friends are a door, not evidence.** Ask friends for introductions to people who match the ICP. Interview a friend only if they genuinely experience and buy around this problem. Compliments, votes, and “I would use it” do not validate demand. Ask about the last real incident, current workaround, frequency, cost, and who pays.
4. **Observe behavior before opinions.** Stronger evidence progresses: problem story → introduction/demo accepted → product used → returns → referral/share → payment. Do not promote based only on survey enthusiasm.
5. **Ask for money early.** A paid pilot, preorder, deposit, or first subscription is stronger evidence than a waitlist. Founder-led sales teaches the problem and pricing ([YC first customers](https://www.ycombinator.com/library/Ip-how-to-get-your-first-customers)).
6. **Do not scale paid promotion before proof.** Default: no recurring ad budget until at least one target customer pays **and** gets value. A tiny, capped ad test is allowed only as a learning experiment for message/search intent; label it validation spend, set a stop amount, and do not call clicks product-market fit.
7. **Build a natural sharing moment.** Do not bolt on “invite friends” blindly. Find an artifact or outcome users already need to send: report, result, public page, export, invite, review, handoff, booking link, or recommendation. The recipient should see useful context before signup. Measure `share_started → recipient_opened → recipient_activated`.
8. **SEO follows real questions.** Create people-first pages from problems users actually ask, then make them crawlable. Google’s guidance: helpful original content for a clear audience, words users use in titles/headings, crawlable internal links, and sound indexing/mobile basics ([SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide), [people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)).
9. **One channel until signal.** Pick the place where the ICP already gathers. Do not “be everywhere.” Add a second channel only after the first has a repeatable weekly action and measurable response.
10. **Measure the constraint, not vanity.** Before payment: qualified conversations, demos, activation, repeat use. After payment: activation, retention, referral/share, conversion, revenue. Followers and raw traffic are context, not the goal.

### Evidence ladder and decision gates

| Evidence | Meaning | Next move |
| --- | --- | --- |
| Friend says “nice idea” | Courtesy, not validation | Ask for an ICP introduction |
| ICP describes a recent painful incident | Problem evidence | Show a manual solution / prototype |
| They give time, data, or a demo meeting | Commitment | Deliver value manually |
| They use and return | Product evidence | Fix activation and ask why they returned |
| They pay / approve a paid pilot | Commercial evidence | Founder-led acquisition; test price |
| Several similar users pay and retain | Early repeatability | Consider SEO cadence, partnerships, then small paid tests |

**Paid promotion gate:** no scale spend from `none`, `anecdote`, or `waitlist`. One payment permits only a bounded experiment. Repeat payment/retention permits testing a repeatable paid channel.

## Positioning card (every period)

Fill this before you write any launch copy. If any line is empty, ask — do not guess hype.

```
One-liner: {product} helps {ICP} {do job} without {pain they named}.
ICP: {role + context}, not “everyone”.
Proof so far: {none | anecdote | pains_scored | waitlist | paying}.
Not for: {one sentence}.
Primary channel: {from strategy}.
```

Judge it from relevant project material and user conversations: named buyer, urgent job, current workaround, frequency, and willingness to pay. If those are weak, stay in **validate** — do not schedule a broad launch.

## Project-type lens

Read `status.project.project_type` when bound; otherwise ask. Project type changes the offer, proof, activation event, CTA, and useful metric—not the need for evidence.

| Project type | First value / conversion | Typical early GTM emphasis |
| --- | --- | --- |
| `MICRO_SAAS` | user completes the core job; trial/demo → paid | founder demos, onboarding observation, pain-led communities/search |
| `SERVICE_FREELANCER` | qualified call, paid audit, proposal accepted | warm intros, targeted outreach, proof/case study, clear scope |
| `NEWSLETTER_MEDIA` | right reader subscribes, opens, replies, returns | sample issue, guest swaps, creator/community distribution |
| `DIGITAL_PRODUCT` | checkout then useful download/use | problem-led content, demonstrations, bundles/affiliates after proof |
| `COMMUNITY` | qualified member joins, participates, returns | founder invitations, member outcome, rituals and referrals |
| `CREATOR_ARTIST` | audience consumes, follows/joins list, commissions/buys | consistent native content, collaborations, owned-audience capture |
| `BRAND` | product-page intent → purchase → repeat | customer proof, creator seeding, search/shoppable content; ads only after conversion evidence |
| `EDUCATION_COHORT` | application/enrollment → attendance/completion | workshop/webinar, outcome proof, alumni/referral loop |
| `PLATFORM_MARKETPLACE` | one narrow segment completes a successful match/transaction | solve the constrained side manually; avoid broad two-sided launch |

Do not use software-only language for every project. “Ship” may mean publish an issue, package an offer, open enrollment, release a product drop, run a community event, or manually complete the first marketplace match. Inspect code only when code is relevant.

## Channel defaults (choose for this project and audience)

After audience + stage are known, rank channels from evidence: where this ICP already asks for help, whether the founder can participate consistently, and how buying happens. Do not call generic SEO utility APIs to choose strategy.

| Channel | Use when | Do not |
| --- | --- | --- |
| **Direct outreach / warm intros** | ICP is identifiable; founder needs first conversations/demos | Bulk generic cold spam |
| **Reddit help-first** | Buyers already complain in subs; you can show up weekly | One-shot launch dump; link in first comments; no 9:1 |
| **LinkedIn** | Role/company targeting matters; founder can add useful professional context | Connection-request pitch blasts |
| **Indie Hackers** | Honest build log; peer founders | Pure ad posts |
| **X / build in public** | They will post 3×/week for months | A single launch tweet as the plan |
| **Short video** | The pain, craft, result, or workflow is visually demonstrable; ICP watches | Chasing one viral clip; generic trend copying |
| **YouTube / long video** | Buyers search for explanations, comparisons, or demonstrations | High production with no clear viewer intent |
| **Show HN** | Something to **show**, technical audience, honest rough edges | Marketing tone; fake user counts |
| **Product Hunt** | They can hunt + follow up the same day; product is usable | “We should PH” with no hunter, no demo, no follow-up week |
| **Newsletter guest/sponsor** | A list that already reaches the ICP | Buying a huge unmatched list |
| **Workshop / webinar** | Live teaching/demo creates trust or qualification | A disguised sales pitch with no attendee outcome |
| **Podcast / guest content** | Host already reaches ICP; founder has credible evidence/story | “Feature my product” pitches |
| **SEO / content** | Search intent is clear; 90-day patience | Ranking as this week’s only bet |
| **NicheMatch** | Matching **open** + they can rec a complementary product on a thank-you / P.S. | Homepage banners; inventing partners |
| **Paid acquisition** | Payment, value, retention, measurement, and economics exist | Scaling from clicks or waitlist demand |

**Default before repeatability:** founder-led conversations through direct outreach, warm introductions, or one trusted community. Reddit is one strong option, not the automatic answer. PH and HN are **optional campaigns**, not the engine.

If they do not know where the ICP gathers, research public communities and search results directly. Ask the founder where they already have credibility or access.

### Stage-aware priority map

Use the first row whose constraint is true. Instrument availability never changes this order.

| Constraint observed | Priority action | Strongest useful metric |
| --- | --- | --- |
| ICP/pain is still a guess | 3–5 recent-incident interviews or a manual paid offer | qualified pain stories; commitments |
| Product is not usable by another person | ship one activation slice and observe one user | activation completed |
| Usable, but no qualified conversations | founder-led outreach on one best-fit channel | qualified replies/demos |
| Conversations, but few try it | fix promise, CTA, demo, or onboarding handoff | visit/demo → activation |
| Users activate, but do not return | retention interview + fix the drop-off | repeat use / retained users |
| Users get value, but do not pay | pricing/paid-pilot ask | paid conversion/revenue |
| One channel converts repeatedly | repeat it; then test one adjacent channel | conversion quality and cost/time |

For any selected action: define a hypothesis, baseline if known, target, artifact, and review trigger. After results arrive classify **strong signal / weak signal / no read**, then **continue / change / stop**.

---

## Period: `validate`

**Goal:** evidence the pain is real for a named ICP. No launch dump.

1. Write the positioning card.  
2. Find five plausible ICPs manually. Friends may introduce them; friends’ praise does not count.  
3. Run 3–5 problem interviews. Ask: “Tell me about the last time”; “How do you solve it now?”; “How often?”; “What does it cost?”; “Who decides to pay?” Do **not** pitch first.  
4. Prefer a **Nichestarter topic** for repeated pain evidence (`create_from_project` if Premium). Without Nichestarter, use interviews and source links the founder deliberately researches. For a bound project with no linked topic, fetch **no** generic public-library pains; ask once whether they want project monitoring.  
5. Push ≤5 pains. Ask **build / later / not_us**. A pain is a repeated complaint, not a viral idea. Ignore one-offs.  
6. Offer a manual solution, prototype, preorder, or paid pilot. Ask for a real commitment; do not count “send me the link.”  
7. If there is no product: pick **one** pain and one ICP. Do not brainstorm ten startups.  
8. This week’s artifact: one-liner + ICP + evidence log + “we will not build X.”  
9. **Never:** Product Hunt, Show HN, recurring ads, or “post in 20 subs.”

**You do next (default):** book one qualified interview or write one manual paid-offer message. Monitoring is supporting evidence, not automatically priority one.

---

## Period: `build`

**Goal:** smallest offer, artifact, product experience, issue, session, or transaction someone can receive this week. GTM is positioning + first users, not a broad launch.

1. Keep the one-liner honest: what works **today**.  
2. Define one activation event: the smallest moment where a user receives the promised value. Build to that, not a feature checklist.  
3. Deliver the first-value experience to one target person this week; manual/concierge delivery is allowed. Observe behavior before asking what else they want.
4. Monitor pains only to decide **this month’s** feature, not a roadmap dump.  
5. Identify one natural sharing moment: what useful output would this user already send to another person? Add the smallest share link/export/invite only if it completes the core job.  
6. Optional: waitlist sentence + where it lives (README, landing). A waitlist is interest, not payment validation.  
7. Help-first Reddit is OK if they can spend 15 min. No product link unless asked.  
8. **Never:** PH/HN or recurring ads until someone else can use it; do not add a referral popup with no workflow reason.

**You do next (default):** make one first-value experience ready for a target person, or recruit that first person through the primary channel.

---

## Period: `cold_start`

**Goal:** show up where buyers already talk. Habit beats spikes.

First score plausible channels with [channels/index.md](channels/index.md), including short video when the offer is visually demonstrable and the ICP watches it. Lock one primary channel on the CMO board. Load that channel SOP only after the founder chooses to execute it.

### Non-Reddit acquisition SOPs

- **Direct / warm:** identify 10 true ICPs → personalize from an observed trigger → ask for a short problem conversation, not a vague “thoughts?” → follow up once → track qualified replies, calls, use, and payment.
- **LinkedIn:** comment usefully where the ICP already participates → send a context-rich connection note only when relevant → publish one practical lesson/case → track qualified conversations, not views.
- **X:** draft a 3-post set: one lesson from users, one honest shipped change, one specific question. Join relevant conversations before linking. Track replies/profile-to-site/qualified conversations; followers are secondary.
- **Indie Hackers/community:** share problem, evidence, what changed, and one real question. No feature-dump drive-by.
- **Newsletter/podcast:** pitch one audience-specific lesson or case study, not “feature my startup.” Track qualified visits, replies, and activations.

### Reddit / Facebook groups (NicheReach SOP)

This is the NicheReach product, not a generic “post more.” Load `channels/communities.md` only after the founder chooses this channel.

1. Find threads: `/api/gtm/agent/leads` or they paste a URL. **Do not invent threads.**
2. Show each lead as `[title](post_url)` · r/sub · match score. That is enough.
3. Ask **open in extension / save / skip**.
4. **Never fetch** the Reddit/Facebook page, JSON, screenshot, or comments.
5. **Never draft** a 90/10 or any comment in the agent. The [NicheReach Chrome extension](https://chromewebstore.google.com/detail/nichereach/meijkmdpgkfookehfglnkdcjgobheemp) reads the thread, drafts, and safety-checks. They click Comment/Send.
   Inbox: https://www.nichestarter.ai/reach
6. **9:1 habit:** about nine helpful comments per one soft product mention (14-day mix). New accounts: help-only, slow pace, one community.
7. **Facebook groups:** same help-first rule via the extension; follow **that group’s** rules; they still click Send.

If NicheReach discover is off, ask once whether the founder wants optional potential-customer discovery. If yes, send them to `https://www.nichestarter.ai/reach`; the agent cannot enable it. If no, they may paste a URL; still do not fetch or draft. Do not ask again this week.

### Cadence (when Reddit is primary)

- 3 help-first replies (different threads if possible)  
- 0–1 soft mention **only** if 9:1 allows and they asked for tools  
- 1 pain decision if monitoring is on  

**Never:** blast the same pitch to five subs the same day.

---

## Period: `launch` (optional PH / HN)

**Goal:** one spike. Plan the week **around** it. It is not the weekly engine.

Only if `launch_optional.producthunt` or `show_hn` is true **and** `build` is `mvp` or `shipped`.

### Product Hunt (if on the board)

1. Usable demo + hunter + they can sit the launch day.  
2. Title: what it does, not “game-changer.”  
3. First comment: who it is for, what is still rough, link.  
4. Week after: Reddit/IH follow-up help-first — the spike fades.  
5. **Never:** PH as the only GTM plan; fake upvotes; claiming users you cannot see.

### Show HN (if on the board)

1. Title: `Show HN: {thing} — {honest outcome}`.  
2. Body: what it is, who it is for, what is rough, link.  
3. Stay in comments as a human. No marketing deck tone.  
4. **Never:** Show HN with nothing to show; “please upvote.”

Same week: keep **one normal primary-channel action** so the engine does not die after the spike.

Do not buy launch traffic merely to create a spike. If nobody in the ICP has used the product yet, return to `build`.

---

## Period: `promote`

**Goal:** weekly habit on the **primary** channel. Never spray.

- If primary is Reddit: same as cold_start, plus optional 1 weekly thread **only** if they already live in that sub. Replies still go through the NicheReach extension.
- If primary is direct/warm: 10 researched contacts, 5 personalized asks, one follow-up block, and founder-led demos.
- If primary is LinkedIn: 3 useful comments, 1 evidence-based post, and only contextual outreach.
- If primary is X: 3 short posts (learn / ship / ask), not a launch thread every day.
- If primary is short video: after the founder chooses this channel, follow `channels/short-video.md`; one viewer, three pillars, one script at a time, four-week test.
- If primary is YouTube: answer one evidenced viewer question deeply; derive clips only when they stand alone.
- If primary is IH: one honest build post, not a feature dump.
- If primary is newsletter/podcast: one tightly matched pitch plus a useful audience-specific angle.
- If primary is workshop/webinar: promise and deliver one attendee outcome, then track qualified next actions.
- If primary is SEO: run the SEO SOP below.
- Community replies that name the product are drafted and safety-checked in the NicheReach extension, not in this agent.
- Homepage **banners for partners** are a failure mode. Recs live in P.S., thank-you, or one social post — see NicheMatch skill.

**You do next (default):** if the channel is Reddit/Facebook, list clickable leads and hand off to the extension. Otherwise create one artifact for the primary channel, define its success metric, and analyze the result at the review trigger.

---

## SEO SOP (when there is a product or a clear problem)

Inspect the public site/content and, when available, its repository or CMS configuration. If the agent cannot access them, ask for the URL, screenshots, or relevant settings. Do not call `/api/tools/*` to produce an SEO verdict.

1. **Intent:** name one ICP question or job. One page should satisfy one main intent; do not mass-generate nearby keywords.  
2. **People-first content:** answer the question with original product/user evidence, examples, limitations, and a useful next step. If it would be useless without Google traffic, do not publish it.  
3. **Search snippet:** unique descriptive `<title>`, one clear H1, useful description, natural buyer words. No stuffing.  
4. **Crawl/index:** check response status, robots directives, canonical, sitemap inclusion where appropriate, and crawlable `<a href>` internal links.  
5. **Rendering/mobile:** primary content must exist without a click and remain equivalent on mobile. Images have meaningful alt text when informative.  
6. **Structure:** link from a relevant hub and to the next useful page. Structured data must match visible content; never add fake ratings/FAQs.  
7. **Conversion:** one CTA matching intent (read proof, try product, join waitlist, buy). Track the action, not rankings alone.  
8. **After publish:** tell relevant people/community members because it helps them; review Search Console/indexing and update the page from real questions. SEO is a 60–90 day asset, not this week’s proof of demand.

### Shareability audit (run once at MVP, again after first payment)

Ask and inspect:

- What artifact/result does a successful user naturally show, send, embed, invite someone to, or request approval on?  
- Can a recipient see useful context before signing up?  
- Does sharing help the sender complete the job, or is it merely advertising us?  
- Is private-by-default respected? Never make sensitive output public for growth.  
- Are attribution and the CTA tasteful and removable where appropriate?  
- Can we measure share start, recipient open, activation, and conversion?

If there is no honest sharing moment, write `share_loop: none yet`. Do not force virality. Use founder-led acquisition.

---

## Period: `monitor`

**Goal:** product-scoped pains → what to build or how to talk. This never fully stops once shipped.

1. Require **project topics**, not public keyword overlap. If none is linked, return no pain decisions and ask once whether they want optional project-level Reddit pain monitoring.  
2. Push ≤5 pains: **build / later / not_us**.  
3. `build` → one micro-task (copy, empty state, or small ship).  
4. `not_us` → add a tag to `filters.ignore_pain_tags`.  
5. Pair with 1–3 NicheReach leads only if primary channel is Reddit.

**Never:** treat smoking/vaping (or any library mismatch) as this product’s roadmap.

---

## Period: partners (NicheMatch)

**Not a v1 launch pillar.** Only if `GET /status` → `match.marketplace.enabled` is true.

Then follow  
https://www.nichestarter.ai/skills/nichematch-agent-onboarding/SKILL.md  
with the **same** `nmagt_` key.

Rules to keep in this chat even before you open that skill:

- Complementary = overlapping audience, **different job**. Not a competitor.  
- You do not invent partners. Retrieve matches.  
- Rec goes on thank-you / newsletter P.S. / one post — **never** a homepage banner.  
- After confirm, the shipped sentence uses `tracked_url`, not the partner homepage.

If matching is closed: `partners: waiting`. Keep Reddit/validate/promote. Offer a watch; do not GET `/matches`.

---

## Copy you may write (human publishes)

### Reddit / Facebook — do not draft here

Do **not** write community comments in this agent. Send the founder to the clickable URL with the NicheReach extension. The extension owns drafting, safety check, and posting.

Never fetch the post to “help write a better reply.”

### One-liner

`{Name} helps {ICP} {job} without {pain}.`

### X three-post set

1. **Learn:** `{Specific user situation} taught us {non-obvious lesson}. Here is the practical takeaway: {useful detail}.`
2. **Ship:** `We changed {thing} because {evidence}. It now {honest outcome}. {link only if useful}.`
3. **Ask:** `{ICP}: when {situation}, how do you currently {job}? I am especially curious about {specific tradeoff}.`

Rewrite in the founder’s voice. One idea per post; no invented metrics, fake controversy, or daily launch threads.

### Direct outreach

`Saw {real trigger/context}. How are you handling {specific job/pain} today? I am learning from {ICP}; open to a 15-minute chat? No pitch required.`

If evidence is strong and a usable solution exists, make the ask concrete: demo, manual pilot, trial, or paid pilot. Personalize from facts; never fabricate familiarity.

### Product Hunt first comment / Show HN body

What it is · who it is for · what is still rough · link. No fake metrics.

### Soft CTA

Never guaranteed revenue. Never “DM me for a discount” as the whole comment.

---

## Weak-model checklist (every turn)

1. Is `strategy.confirmed` true? If no → only the CMO board. Stop.
2. Did I name **one** period and keep it visible, not jump into a channel SOP?
3. Did I rank one recommendation above at most two alternatives, explain why, then give **one** ≤5 min next step?
4. If I listed leads: is every row a clickable URL? Did I tell them to open the NicheReach extension? Did I fetch the post or draft a comment? If yes, undo.
5. If no project topic is linked: did I return no public-library pains and offer monitoring only once?
6. Am I recommending paid scale without payment + value/retention evidence? If yes, stop or make it a capped validation test.
7. Did I treat friend praise, a waitlist, traffic, or clicks as validation? If yes, downgrade the evidence.
8. Did I check for a natural share moment and basic SEO when the product is usable?
9. Did I define an outcome metric and review trigger, or analyze the result if it arrived?
10. Did I write more than one artifact? If yes, delete extras. Community replies are not artifacts for this agent.
11. Did I claim I published, sent, or posted? If yes, undo — the founder acts.
