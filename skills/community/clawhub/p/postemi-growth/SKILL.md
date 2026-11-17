---
name: postemi-growth
description: Grow an audience and get results from social posting with Postemi. Covers choosing networks and a first niche, a 30-day posting test, reading the numbers (Postemi Insights and analytics), posting cadence per network, turning one topic into 30 post angles and scheduling them as a content plan, repurposing one idea across networks, bios and profile links that turn followers into sign-ups or customers, and a weekly review loop. Use when the user asks how to grow followers or reach, what or how often to post, for a content plan or calendar, why posts do not perform, or how to get customers from social media.
---

# Postemi growth: from posting to results

This skill is the plan; `postemi-writing` is how each post is written,
`postemi-templates` has ready drafts, and the main `postemi` skill has the
tools and commands. If the writing skills are not installed, write the posts
with the rules of the main skill and offer `postemi skills add writing` (ask
the user first). Reference files:

- [reference/30-angles.md](./reference/30-angles.md): 30 ways to post about
  one topic, with a worked example.
- [reference/review.md](./reference/review.md): the post log and the weekly
  review, step by step.

## Principles

1. **Focus.** One or two networks done well beat seven done badly. Add more
   once something works.
2. **Every post is a test.** Growth early on is learning what this audience
   wants. Post, read the numbers, keep what works, drop what does not.
3. **Consistency beats bursts.** A steady rhythm the user can keep for months
   wins over a busy week followed by silence. Long gaps cost reach.
4. **Big changes, not tiny tweaks.** With a small audience, a new topic, angle
   or format teaches more than changing one word.
5. **Real engagement only.** No bought followers, no engagement swaps, no
   bots. Comments, shares, saves and replies from real readers are the signal.
6. **What Postemi does and does not do.** Postemi writes nothing on its own,
   schedules and publishes, and shows numbers. It does not reply to comments,
   follow, connect, like or send messages for the user. Those are the user's
   part, and they matter.

## 1. Choose where to start

Ask who the user wants to reach and what they sell or share, then suggest one
main network and at most one second one:

| The user | Start with |
|---|---|
| Sells to businesses, consultant, founder, job market | LinkedIn (personal profile), then X |
| Ideas, tech, writing, building in public | X or Threads, then LinkedIn; Bluesky for tech crowds |
| Visual products, food, fashion, beauty, travel, places | Instagram (Reels and carousels), then TikTok |
| Local business (shop, cafe, salon, trades) | Facebook and Instagram |
| Teaching with video | YouTube (Shorts too) and TikTok |
| An existing community | Telegram, Discord or Slack, next to one public network |

Postemi can send the same idea to several networks at once later (section 6),
so starting narrow costs nothing.

## 2. The first niche and the 30-day test

A niche is not for life; it is the first topic the user goes deep on. The
skill of building an audience carries over when the topic changes. Find it
with data, not by thinking harder:

1. **Pick one network** (usually X or LinkedIn for text, Instagram or TikTok
   for visuals).
2. **Post at least once a day for 30 days.** Any idea from the user's
   experience: use the idea builder and the look-back test in
   `postemi-writing`. Vary topic, angle (how-to, analysis, inspiration, human
   nature) and format on purpose, so the data has something to compare.
3. **Schedule it with Postemi a week at a time.** Write seven posts with the
   user, preview them, and create them in one go (one `socialPost` entry per
   day in `create_post`, or a `--json` file with the CLI). The user only has
   to show up for the replies.
4. **Log every post** (topic, angle, format, hook, time): see
   [reference/review.md](./reference/review.md).
5. **After 30 days, read the numbers** (section 3) and pick the topic and the
   angle with the strongest early signal.
6. **Go deep on that topic** for the next weeks. Writing about the same topic
   again and again is not repetition; it is why people follow someone. The 30
   angles (section 5) make it easy.

Small numbers still count. If 20 posts got no likes and 10 got one, those 10
did infinitely better: that is the signal. The method is the same at 10
followers and at 10,000; only the zeros change.

## 3. Read the numbers

Where the numbers are:

- **Postemi Insights**, in the web app (postemi.com/app/insights): reach,
  engagement and followers per channel over time.
- **The CLI:** `postemi analytics:platform <integration-id> -d 30` for a
  channel, `postemi analytics:post <post-id> -d 7` for one post. If a post
  answers `{"missing": true}`, link it first (`posts:missing`, then
  `posts:connect`; see the main skill).
- **The MCP tools** have no analytics tool. Ask the user to open Insights, or
  to paste or screenshot the numbers, and work from that. `list_posts` gives
  the post ids, dates and channels to match them to.
- The network's own analytics, when the user has it open.

What to look at, in this order:

1. **Conversations:** comments and replies (and how long they are). The
   strongest sign a post landed.
2. **Shares, reposts and saves:** people found it worth passing on or keeping.
3. **Follows and profile visits** after a post: it made people want more.
4. **Engagement rate:** engagements divided by impressions. Compares posts
   fairly when reach differs.
5. **Reach and impressions:** how far it went. Useful, but a post can travel
   far and change nothing.
6. **Clicks and sign-ups** from the profile link, when the user tracks them.

Likes alone are the weakest signal. Compare posts with each other, not with
other people's accounts.

## 4. How often, and when

Starting points, not laws. The best cadence is the one the user can keep.

| Network | Suggested rhythm | Notes |
|---|---|---|
| X | At least 2 short posts a day, 5 days a week; to grow faster, 3 to 5 a day, 7 days a week, plus 2 or more threads or long posts a week. Text with an image or video does best. | Every post and thread entry counts toward the account's monthly X allowance in Postemi, so tell the user how many are left when the plan needs more. |
| LinkedIn | 1 post a day at most, 3 to 5 a week is plenty. | Posting more does not grow faster here. Mornings in the audience's timezone work well. Do not go weeks without posting. |
| Instagram | 3 to 5 feed posts or Reels a week, Stories in between. | Reels for reach, carousels for saves. |
| TikTok | Up to 1 or 2 a day. | Postemi allows about 15 posts per account in 24 hours. |
| Threads, Bluesky, Mastodon | 1 to 3 a day. | Conversation matters more than volume. |
| Facebook | 3 to 5 a week. | Local and community content. |
| YouTube | 1 a week; Shorts more often. | Consistency of the day helps viewers. |
| Blog channels | 1 to 4 a month. | The long versions of the best posts. |

Timing: start with morning and early evening in the audience's own timezone
(take the user's timezone from Postemi, and ask where the audience is), then
compare times in the log. `postemi posts:find-slot <id>` suggests the next
free slot on a channel's schedule.

## 5. One topic, 30 posts

Once the user has a topic, turn it into a month of posts with the 30 angles
in [reference/30-angles.md](./reference/30-angles.md): tips, mistakes, tools,
steps, stories, lessons, myths, questions and more. Each angle becomes a
question, each answer becomes a post.

Mix the 30 across three to five **content buckets** (themes the audience
expects from the user, for example "how-to", "behind the scenes", "customer
results", "opinions") and refuse ideas that fit no bucket. That keeps the
account recognisable.

### Turning the plan into a Postemi schedule

1. Agree the network(s), the number of posts per week and the times.
2. Write the first week in full (with `postemi-writing`), show it, adjust.
3. Get the clock and timezone (`get_workspace_context`, or the CLI's saved
   timezone), and spread the posts over the days at the agreed local times.
4. Preview all of them in one `preview_post` call (one `socialPost` entry per
   post), or show the list from the CLI; fix what the preview flags.
5. On the user's yes, create them in one call with an `idempotencyKey`. Use
   `type: "draft"` (CLI `-t draft`) if the user wants to review them in the
   Postemi calendar before they go live.
6. Repeat weekly, folding in what the numbers say. Writing a month ahead is
   fine, but leave room for timely posts and for what you learn.

## 6. Repurpose: one idea, every network

A post that worked is the best raw material for the next ones:

- **Across networks, adapted, not copied.** The same idea as an X short post,
  an X thread, a LinkedIn long post with an image, an Instagram carousel, a
  Threads post, and later a blog article. Each gets its own hook, length and
  format (see `postemi-writing`). In Postemi each channel gets its own entry
  with its own text in the same request.
- **Never the same post on two X accounts:** one X channel per post.
- **Up and down in size.** A thread becomes an article; an article becomes
  five short posts; a popular reply or comment becomes its own post.
- **Again, later.** Re-share a winner after a few months with a new hook and
  a fresh example; most followers did not see it the first time.
- **Collaborations.** Instagram posts can name collaborators (a setting in
  Postemi); a post together with a partner brand or creator reaches both
  audiences.

## 7. Profile, bio and the path to a customer

Posts bring people to the profile; the profile decides whether they follow
and click. Help the user write it:

- **Bio:** "I help [who] [get what]" or "I write about [topic]", plus one line
  of proof: "Baker for 12 years. 3 shops." Clear beats clever, as with hooks.
  No list of ten roles.
- **One link,** to one next step: an e-mail list, a free guide or checklist,
  a booking page, a product page. On X the bio is the place for links, since
  Postemi removes links from X posts. On Instagram point to the link in the
  bio. On LinkedIn, feature the free resource or product in the Featured
  section.
- **Name and keywords:** put the topic word people search for in the display
  name or headline (Instagram, LinkedIn) so the profile can be found.
- **The path:** post, profile, link, e-mail or sign-up, offer. Most posts just
  give value; about one in five invites people to the next step (a free
  resource, a waitlist, the product), with a clear reason to click. On
  LinkedIn and Facebook that link can go in the first comment.
- **Pinned post:** the user's best post, or the one that explains what they do
  and where to start.

## 8. The user's part every day

Share this with the user plainly; Postemi cannot do it for them:

- Reply to every comment in the first hours after a post goes out; replies
  bring more reach and turn readers into followers.
- Leave two or three thoughtful comments a day on posts by bigger accounts in
  the same field. A good comment is a small post of its own, and a comment
  that does well is an idea for a full post.
- Thank people who share.

## 9. Review and iterate

Once a week (15 minutes), with the user:

1. Pull the numbers for the week (section 3) into the log.
2. Name the top three and the bottom three posts, and what they had in common
   (topic, angle, hook pattern, format, time).
3. Decide one bigger change for next week: more of the winning angle, a new
   format, a different time, dropping a topic that never lands.
4. Write and schedule next week with that change.

Once a month: is the main network working? Is the niche still the right
first one? Is the profile link getting clicks? Keep, adjust, or try the
second network. Details and a log template: [reference/review.md](./reference/review.md).
