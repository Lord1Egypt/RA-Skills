---
slug: podcast-episode-launch-pack
name: Podcast Episode Launch Pack
description: Turn a podcast transcript, episode outline, or topic into a complete launch package. Outputs episode titles (curiosity + clarity variants), full show notes with timestamps and key takeaways, a subscriber email blast, and an Instagram audiogram caption — plus optional pull quotes, a LinkedIn post draft, and a promo tweet thread. Use when a creator asks for show notes, podcast launch copy, episode title, podcast description, episode summary, audiogram caption, or anything related to publishing and promoting a podcast episode.
version: 1.0.0
license: MIT
tags:
  - podcast
  - creator-tools
  - content-creation
  - marketing
  - launch-kit
  - show-notes
  - podcasting
metadata:
  openclaw:
    requires:
      env: []
      bins: []
---

# Podcast Episode Launch Pack

Turn a recorded episode or planned outline into a complete launch package — titles, show notes, subscriber email, and audiogram caption. One paste in, full launch out.

## When to use this skill

Trigger this skill when the user:
- Pastes a transcript or episode outline and asks for show notes, a podcast description, or launch copy
- Says "write my show notes," "write my podcast description," "give me an episode title," "write my podcast launch," "help me publish this episode," "write my audiogram caption," "write an email for my podcast episode," or "create a launch pack for my episode"
- Asks for an episode summary, key takeaways, or timestamps from a transcript
- Wants promo content (email, social, audiogram) for a podcast episode they've recorded or planned

Do NOT trigger for:
- Generating audio or producing the episode itself — out of scope
- Full podcast strategy, show naming, or feed setup — out of scope
- Diagnosing why a past episode underperformed without new content to package — out of scope

---

## Step 1 — Identify input state, episode format, and missing information

### Episode format (ask if not clear from input)

Ask one question up front if the format can't be inferred:

> *"Is this a solo episode, an interview episode, or a narrative/storytelling episode?"*

This determines how show notes are structured, whether a guest bio is needed, and how timestamps are labeled. Do not ask any other clarifying questions before determining format.

| Format | Key difference |
|---|---|
| **Solo / educational** | Creator's voice and insights throughout; takeaways are their own frameworks or lessons |
| **Interview** | Guest is the primary draw; ask for guest name + 1–2 sentence bio if not in input; show notes lead with guest intro; pull quotes weighted toward guest |
| **Narrative / storytelling** | Chronological or chapter-based structure may not fit; offer "Story Highlights" section instead of numbered timestamps if the format doesn't support chapter breaks |

### Input states

**State A: Transcript (primary)**
Full or partial transcript from auto-captions, Descript, Whisper, Otter, or any other source. Enables accurate timestamps, real pull quotes, and genuine takeaways drawn directly from what was said. This is the richest input — produce the most specific, detailed output possible from it.

**State B: Topic + outline or show notes draft (secondary)**
Pre-record or for podcasters who don't transcribe. Timestamps become structural placeholders (`0:00`, `XX:XX` format). Takeaways come from the outline's planned points. Fully functional — note once that timestamps should be filled in after recording.

**State C: Topic only (edge case)**
Thin input. Produce titles, email, audiogram caption, and a show notes shell with structural placeholders. Note once: *"With just a topic, I'll give you the full structure — fill in timestamps and takeaways after you record."* Do not repeat this caveat.

### Optional inputs (use if provided, don't ask twice)
- Target audience or listener persona
- Show name and host name (for email sign-off and show notes header)
- Guest name and bio (interview episodes — if not provided and format is interview, ask for these specifically)
- Tone — conversational, educational, storytelling (default: infer from input)
- Episode number (include in title if provided)

---

## Step 2 — Generate the launch package

Deliver all core deliverables in a single response, clearly labeled with H2 headers. Never skip a core deliverable. Offer optional deliverables at the end.

---

### Episode Titles (2 variants)

Two variants, labeled by intent:

**Curiosity-framed:** Withholds one key detail or teases the outcome. Drives browse and recommendation traffic — someone scrolling sees it and wants to know more.

**Clarity-framed:** Direct, keyword-forward, searchable. Leads with the primary topic or guest name. Drives search traffic in podcast apps and Google.

Rules:
- Maximum 50 characters each — most podcast apps truncate titles at this point in browse and search views
- Episode number goes after the title keyword, not before: "Deep Work With Cal Newport | Ep. 14" beats "Ep. 14: Deep Work With Cal Newport"
- For interview episodes: guest name appears in both variants — it's a keyword (listeners search by guest name)
- No manufactured urgency or all-caps words

---

### Show Notes

The anchor deliverable. Structure in this exact order:

**Episode summary (opening paragraph):**
150–200 words. The first 150 characters must be keyword-dense and hook the listener — this is what Spotify and Apple display before truncation, and what Google indexes most heavily for search. Written in the show's voice.

**Guest intro (interview episodes only):**
1–2 sentences introducing the guest: name, title/role, why they're on the show. Placed immediately after the summary paragraph. Use provided bio or construct from context; never invent credentials.

**Key takeaways:**
3–5 bullets. Scannable, specific, and written so a reader can extract value without listening. These serve two purposes: helping undecided listeners decide to tune in, and giving Google structured content to index as featured snippets. Do not write generic bullets ("We discuss productivity") — write the actual insight ("Why blocking your calendar in 90-minute windows outperforms to-do lists").

**Timestamps / chapters:**
- State A (transcript): accurate timestamps derived from transcript structure. Minimum 4. First at `0:00`. Labels must be content-specific — never "Intro," "Part 1," or "Outro" as standalone labels.
- State B (outline): structural placeholders (`0:00 Topic`, `XX:XX Topic`). Creator fills in times after recording.
- State C (topic only): omit timestamps or note they'll be added post-recording.
- Narrative format: replace numbered timestamps with a "Story Highlights" section — 3–5 prose sentences capturing the arc.

**Resources section:**
List any tools, books, links, or references mentioned. Use `[LINK]` placeholders. If none are in the input, include the section with a placeholder row — host fills in after recording.

**Guest bio (interview episodes only, extended):**
3–4 sentences at the bottom of the show notes. More detailed than the intro paragraph. Include where to find the guest online with `[GUEST_LINK]` placeholder.

---

### Subscriber Email Blast

Pre-written, ready to send. Podcast audiences are email-forward — this is the highest-conversion channel for most indie shows.

- **Subject line:** ≤60 characters. Curiosity or specificity. For interview episodes, lead with the guest name or their most counterintuitive claim.
- **Preheader:** ≤100 characters. Complements the subject, doesn't repeat it.
- **Body:** ~120 words. Host's voice, first person. Opens with why this episode matters, highlights the single most compelling moment or takeaway, closes with a listen CTA using `[EPISODE_LINK]` placeholder.
- **Sign-off:** Host name and show name (or `[HOST_NAME]` / `[SHOW_NAME]` placeholders if not provided).

---

### Instagram Audiogram Caption

~100 words. Optimized for the audiogram format — a short audio clip from the episode visualized as a waveform or animated card, posted to Instagram or TikTok.

- Opens with a pull quote from the episode (real quote from transcript if available; constructed hook in the episode's voice if not)
- 2–3 sentences of context framing the quote's significance
- CTA: "Full episode linked in bio" or "Listen wherever you get your podcasts"
- 5 relevant hashtags at the end — mix of broad (`#podcast`), niche (`#productivitypodcast`), and topic-specific

---

### Optional Deliverables

After delivering the four core outputs above, offer all three options in one message. Generate whichever the user requests:

**Pull quotes (2–3)**
Short, punchy, attribution-ready. Formatted for visual content: quote cards, audiogram overlays, carousel slides. For transcript input: pull real quotes. For outline input: construct quotes in the speaker's voice that reflect the planned content, and label them as drafted rather than verbatim. Each quote ≤50 words.

**LinkedIn post draft**
A standalone LinkedIn post about the episode — self-contained and ready to publish as-is. Offer the refinement option explicitly: *"I'll generate a LinkedIn post draft for this episode. If you have the LinkedIn Post Optimizer skill installed, run the draft through it for a structured polish — otherwise it's ready to publish as-is."*

**3-tweet / X promo thread**
Sequence: (1) announcement with `[EPISODE_LINK]`, (2) the most compelling insight or quote from the episode, (3) CTA to follow the show. Each ≤280 characters.

---

## Step 3 — SEO and discovery rules

Podcast discovery is structurally different from YouTube. Apply rules precisely where they have impact; don't overpromise where they don't.

### App search (Apple Podcasts, Spotify)

These platforms index primarily on **episode title** and partially on the description field.

1. **Title keyword position:** Primary keyword or guest name in the first 4 words. Apps display ~50 chars before truncation — front-loading the keyword maximizes both search match and scan-level appeal.
2. **Description opening:** First 150 characters keyword-dense. This is the visible text in Spotify and Apple before "more" truncation. Same function as YouTube's above-the-fold description.
3. **Guest name as keyword:** For interview episodes, the guest's name is often the highest-value search term. It must appear in the title and in the first line of the show notes summary.
4. **No keyword stuffing in descriptions:** Spotify and Apple don't reward it the way Google might. Stuffing reads as spam to human listeners. Write for the listener; the keyword placement rules above are sufficient.

### Google (show notes page)

Google indexes the podcast's show notes web page — this is where show notes SEO has meaningful impact.

5. **H2 headings:** Show notes section labels should be descriptive and keyword-rich. "How Cal Newport Blocks His Calendar" beats "Time Management Tips."
6. **Takeaway bullets:** Google pulls structured bullet lists for featured snippets. Specific, insight-led bullets (not generic summaries) are the target.
7. **Guest name + credentials:** Google surfaces podcast episodes in searches for the guest's name. Prominent guest name placement in the summary and bio increases this discoverability.

### LLM layer

Keyword selection draws on training knowledge of what listeners search in a given niche. Same honest ceiling as the YouTube Launch Kit — works reliably for evergreen topics, less reliable for trending ones.

### Honest ceiling — state once per session, do not repeat

> *"Podcast discovery is harder than video. Well-optimized show notes and titles help, but for most indie shows, your existing audience, newsletter, guest-swapping, and cross-promotion drive more listens than SEO. This skill handles the packaging — the distribution is still yours."*

This is not a caveat to apologize for — it's accurate, and buyers will trust a skill that says it.

---

## Step 4 — Style guardrails

- **Never invent quotes.** For transcript inputs, all pull quotes must be verbatim from the transcript. For outline inputs, constructed quotes must be labeled as drafted ("Framed from your outline — adjust to match what you actually said").
- **Never invent guest credentials.** If the guest bio isn't provided and can't be inferred from the input, use placeholders: `[GUEST_TITLE]`, `[GUEST_COMPANY]`. Do not fill in details that weren't given.
- **Never invent timestamps.** Placeholder format only for non-transcript inputs. Do not estimate or guess times.
- **Match the show's voice.** If the input is casual and conversational, the show notes and email are casual and conversational. Do not impose a formal or corporate register on a show that doesn't use one.
- **Takeaways must be specific.** "We talk about focus" is not a takeaway. "Why 90-minute focus blocks outperform hour-long ones" is. If the input doesn't support specific takeaways, note it and use the best available specificity — don't fill with generics.
- **No generic chapter labels.** "Introduction," "Main Discussion," "Conclusion" are banned as standalone labels. Every chapter label must describe the actual content.

---

## Step 5 — Follow-up offers

After delivering the package, offer once:

- "Want the pull quotes, LinkedIn post draft, or promo tweet thread?"
- "If you have a transcript, I can regenerate with accurate timestamps and real pull quotes."
- "Want a version of the audiogram caption tuned for TikTok (shorter, punchier)?"

Do not auto-regenerate unless asked.
