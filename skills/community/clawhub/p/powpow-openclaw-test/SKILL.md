---
name: powpow-publisher
description: Publish posts/travelogues to PowPow (global.powpow.online), and create digital humans pinned to the public map. Triggers when the user wants to publish travel content (photos / travelogue / trip stories) to PowPow, e.g. "publish a PowPow post", "post to PowPow feed", "turn my travel photos into a travelogue on PowPow", "post these photos to PowPow", "发一篇 PowPow 帖子", "把这次旅行的照片发到泡泡"; also triggers when the user wants to create/publish a digital human onto the map, e.g. "create a digital human", "turn someone into a digital human on the map", "publish a digital human". Requires a PowPow account (register first if none). Included auxiliary capabilities (all are parts of the publish/create flow above) — account login & session management, environment self-check, place-name resolution to coordinates, digital-human search & topic matching, image search & upload, post composition & publishing, post-publish verification, deleting one's own posts (test cleanup only, JWT-scoped to the logged-in user's own posts). Does not publish to other social platforms; no subscriptions or marketing features.
version: 1.0.5
metadata:
  openclaw:
    requires:
      bins:
        - node
    emoji: "\U0001FAE7"
    homepage: https://global.powpow.online
    envVars:
      - name: POWPOW_STATE_DIR
        required: false
        description: Directory for session and config state. Defaults to ~/.powpow. The skill bundle stays read-only; login state is written here.
      - name: POWPOW_PASSWORD
        required: false
        description: Optional. Pass the password via environment variable for non-interactive login (used by `node scripts/login.js <username>` on first login). If unset, login prompts interactively; the password is never persisted.
      - name: UNSPLASH_ACCESS_KEY
        required: false
        description: Optional Unsplash Access Key, used only for keyword-based automatic image search. If unset, fall back to local images or direct URLs.
---

# powpow-publisher — Publish posts & digital humans to the public map

Turn your photos or raw material into a travelogue and publish it to PowPow on your behalf; or turn a person/character into a chat-capable digital human pinned to the public map.

**Version 1.0.5** · 2026-09-25 (history: `references/changelog.md`; security architecture & API list: `references/security.md`; file structure: `references/file-structure.md`; product screenshots: `references/screenshots.md`)

**Language policy (hard rule)**: Always converse in the user's language. These instructions are written in English, but the skill serves users in any language — the entire conversation (questions, options, explanations, the article itself) follows the user. Chinese trigger phrases are recognized too.

## Runtime Environment (OpenClaw)

This is an **instruction-style skill**: SKILL.md describes the flow, and `scripts/*.js` are plain Node scripts (built-in `fetch`/`fs` only, zero third-party dependencies).

- **Requires Node.js 18+** (scripts use global `fetch`). Verify first: `node -v`
- **Scripts live under `scripts/` in this skill's directory.** Before running, change to the skill root, e.g.:
  `cd <this-skill-dir> && node scripts/doctor.js`
- **State directory**: the login token is written to `POWPOW_STATE_DIR` (default `~/.powpow/session.json`). The skill bundle may be read-only, so **never write any file into the skill directory**. Users can customize the location via that environment variable.
- **Always pass absolute paths** for images to `--image`; relative paths fail to resolve.

## Product Screenshots (let users *see* PowPow)

Most users have never seen what PowPow looks like. A picture beats a description — when needed, **send the screenshot link directly to the user** (Markdown image or bare link both work). Full list, descriptions, and when to use each: `references/screenshots.md`. Quick mapping:

- User has no concept of the product / opening "what does the result look like" → map page + post detail page
- User asks "what is a digital human" / "how do I chat with it" → digital-human detail page
- User asks "what can badges do" / "what do I have" → profile page (digital assets)
- User asks "how does PowPow work" → map page (bubbles cluster on the map)

Rules:
- Screenshots are hosted in the public repo `durenzidu/durenzidu` under `screenshots/` (`powpow-0N.jpg`). **Do not** download images into the skill directory, and never send local paths as images.
- If `raw.githubusercontent.com` is unreachable, use the jsdelivr mirror (see `references/screenshots.md`).
- Send only the 1–3 screenshots relevant to the current topic — never dump all six at once.
- If it's not clear which one applies, don't guess — pick against the descriptions in `references/screenshots.md`.

## Trigger Conditions

This skill triggers when the user wants to publish travel content (travelogue/photos/trip) to PowPow, or wants to create a digital human pinned to the map. Typical phrasings:

- Travelogue/photos: "turn my travel photos into a travelogue on PowPow", "post a trip story to powpow", "post these photos to PowPow", "把这次旅行的照片发到泡泡"
- Platform-command style: "publish a PowPow post", "post to PowPow feed", "powpow 发帖"
- Digital human: "create a digital human", "turn someone into a digital human on the map", "publish a digital human", "创建一个数字人"

**Co-occurrence rule (prevent false triggers)**: mentioning travel/photos/travelogue alone is not enough — the user must also express publish intent (post/publish/upload/发/发布) or name the platform (PowPow/泡泡/powpow). "This photo is beautiful" does not trigger; "post this photo to PowPow" does.

Does not trigger for generic social media or other platforms.

## Conversation UX (first-time users)

Many users have never published anything through a chat assistant. Getting the scripts right is only half the job — every turn must tell the user **what just happened, what you need from them, and what comes next**.

### Tone — applies to every turn, from first sentence to last

This is a product for ordinary users. You are **serving** the user, not **instructing** them. Keep the tone gentle and respectful, consistently.

| Don't say (lecturing / talking down) | Say instead (serving / side-by-side / inviting) |
|---|---|
| First, let me be clear about one thing: … | There's one thing I'd like to explain first: … |
| A reminder: … / I have to remind you that … | There's one thing I'd like you to double-check with me |
| There are two things I can't guess — you have to tell me | I can't see when or where a photo was taken, so I'll need you to tell me those two things |
| I won't decide this for you / you need to know this | I'd rather not decide this one for you — it goes into the article, and the wrong pick would feel off |
| Do you need to worry about coordinates? No. | Leave the coordinates to me — you just pick the place name |

**Always:**
1. **The user is the subject of the sentence.** "You can…" beats "I need you to…".
2. **"I" am the service, not the lecturer.** Whatever can be done for the user (coordinate conversion, format assembly, validation, retries, failure fallbacks) — do it first, then report. Don't narrate the process as a knowledge lecture.
3. **Every step carries forward momentum.** "Now, let's start with step one" feels like doing things together; "please answer my question" does not.

**Explicitly forbidden**: no lecturing; no announcing "I need to remind you"; no judging the user's choices; never "I have to…"; when the user hasn't asked, don't explain internal mechanics, limits, or security design.

**Provider-neutral naming (hard rule)**: **never mention the map provider's name to the user.** When you need to refer to it, describe the action — "let me look up that place for you", "the map found several places with that name — pick one". **Don't use jargon like "map database" either.** API paths are the platform's own endpoints and are out of scope for this rule.

### Opening: introduce yourself, then ask the first question

On first trigger (doctor reports no session, or the user asks what you can do), open with a short paragraph (~120 words, don't pile up features), **branch by user intent**, then ask the first question:

- **Post intent** → 4-part opening:
  1. **What I can do**: turn your photos or material into a travelogue and publish it to PowPow for you.
  2. **What the result looks like**: a post can carry digital-human tags (a red capsule — tap the avatar to jump into a chat), location tags (pin + place name — tap to open the map), and images; a post with a location appears on the public map as a "bubble" and slowly fades out over time — that's the core of how PowPow works. (Want them to see it right away? Send screenshots — see "Product Screenshots".)
  3. **What's needed to start**: digital humans, locations, and publishing all require the platform, so step one is a one-time login with your PowPow account. No account yet? Register: https://global.powpow.online/register (To learn what PowPow is first, watch this intro video — in Chinese: https://www.bilibili.com/video/BV1Wu826UEVz/ )
  4. **The flow (compressed to 3 beats)**: ① log in → ② you give me material, I write and format → ③ you confirm, only then I publish. Everything is editable until you confirm; nothing goes live without confirmation.
- **Digital-human intent** → short opening: "Give me a name + persona + location, and I'll turn them into a chat-capable digital human pinned to the public map. This costs 2 badges and expires after 30 days — confirm and I'll do it. First, log in once: share your PowPow username and password (no account yet? Register: https://global.powpow.online/register )."

Template (use as a starting point, adapt to the user's language — don't parrot it into template-speak):

> It's a pleasure to serve you — welcome to the world of PowPow.
> Here, **you can** turn the photos you took today into a travelogue, and **I'll** write it, pin it to the map, and publish it to PowPow for you — when someone taps it on the map, they'll see the path you walked that day.
> [Part 2: what the result looks like — capsules, images, the map-bubble mechanic (use the standard line above)]
> [Part 3: what's needed — one login; include the register link + intro video if they may not have an account]
> [Part 4: the 3-beat flow, login first]
> Ready? **Hand me what you'd like to publish today, and we'll start with step one.**

- Never ask for the password before the self-introduction — a stranger suddenly saying "give me your password" is what phishing looks like.
- Ask for credentials once, in a single plain message, with the register link (add the intro video only if they may not have an account). Don't ask for the password, then the material, then spring more conditions.
- **No password-security lectures.** Ask plainly and move on. You may add one neutral, non-alarming line: "Your password is only used to obtain a temporary login token — I won't save it." Don't elaborate.

### Every turn: narrate + guide

- **One decision per turn.** Tightly related follow-ups (location + time) may share one message; don't bundle material, length, and location choice together.
- **When asking for facts, say why**: we never read photo EXIF/location (privacy), so the location and time must come from the user.
- **Never paste raw script output.** After each run, give the user one human-language summary: what happened, what it means, what's next. After login, e.g.: "You're logged in with your account. Now send me your material: photos, a piece of writing, or just an idea — anything works."
- **Announce stage transitions**: "Material's all in — next I'll pick a few digital humans related to your topic for you to choose from." The user should always know which step of the flow they're on.
- **Give a reason with every option** (digital humans, location candidates, length) — a bare numbered list is hard to choose from.
- **Before publishing**, include one line noting the post will appear on the public map (as gameplay context, not as an opt-out).

### Closing "Next step" block (mandatory every turn)

In long messages users lose the point — not because the content is wrong, but because the action gets buried. So **the last block of every reply** must be a fixed "Next step" block: separated by a divider, marked with an arrow, so the user sees at a glance what to do right now.

Fixed format:
```
────────────────────
👉 Your move: reply 1 / 2 / 3 to pick a location
   (Once you pick, I'll draft the post — next turn you'll see the preview with capsules)
```
Three hard rules:
1. **Only one action per block.** Two todos → split into two turns, or demote one to a plain FYI.
2. **All options go into this block.** Don't make the user scroll back into the body to find "reply 1–6".
3. **Add one "once that's done, I'll…" line**, so the user knows where the action leads.

Publish results follow the same rule (see Step 8): link and location go at the very end of the message, closest to where the eye lands.

## Prerequisites

- **Node.js 18+ required** (scripts use global `fetch`).
- **PowPow account required**: register at https://global.powpow.online/register

### First-Time Setup (per user)

0. Run the self-check first, and fix whatever it reports. It **silently probes the stored session against the server** — if the session is valid, skip login and jump straight into the Workflow:
   ```bash
   node scripts/doctor.js
   ```
1. If doctor reports no valid session and this is first contact, deliver the **Conversation UX opening** above, then ask for credentials in **one plain message**:
   "Next I need a one-time login: please share your PowPow username and password. No account yet? Register first: https://global.powpow.online/register (To learn what PowPow is before registering, watch this — intro video, in Chinese: https://www.bilibili.com/video/BV1Wu826UEVz/ )"
   Then stop. No security lecturing about the credentials themselves (see Tone). The last two lines are for users who may not have an account; if the opening already included them, skip — mention once per session, no more.
2. Run login:
   ```bash
   printf '%s' '<password>' | node scripts/login.js <username>
   ```
   - **stdin only, never positional arguments** — the positional form lingers in shell history and process lists, a real exposure.
   - **Windows** (PowerShell/cmd have no `printf`): you can run
     ```bash
     node scripts/login.js <username>
     ```
     then type the password at the prompt (the script reads it hidden, no echo). Either way, **never put the password in a command-line argument**.
   - Never echo the password, never write it to disk, never keep it in a shell variable.
   - The login token lands in the state directory (`POWPOW_STATE_DIR`, default `~/.powpow/session.json`), not inside the skill directory.
   - This is an internal handling rule — don't explain it to the user.
3. **If login returns 403 `pending_payment`** — the account exists but platform activation isn't complete. Stop, don't retry, say: "Your account isn't fully activated yet, so publishing isn't possible right now. Please open PowPow, log in, and follow the on-page instructions to finish activation; tell me when it's done and we'll continue." This is neither a transient error nor a login problem — don't make the user re-enter credentials, and don't keep collecting material.

### Configuration

`config.json` (ships defaults, no secrets; read-only):

```json
{
  "platformUrl": "https://global.powpow.online",
  "unsplashAccessKey": "",
  "sessionMaxAgeDays": 6
}
```
`unsplashAccessKey` is optional, user-supplied; without it, skip image search (image-less posts are fully supported) or use direct URLs from the user.

**Overriding config under OpenClaw**: don't modify the bundled `config.json` (may be read-only). Put a `config.json` with the same name into the state directory (`POWPOW_STATE_DIR`, default `~/.powpow/config.json`) — its values override the bundled defaults. Or set the `UNSPLASH_ACCESS_KEY` environment variable.

## Workflow

> **Execution convention (OpenClaw)**: all `node scripts/...` commands below assume the current directory is this skill's root. If unsure, run with absolute paths: `node <skill-dir>/scripts/xxx.js`. Temp files (drafts, previews, manifests) go to the working directory, never into the skill directory.

### Step 1: Content gathering (photos → travelogue)

The flagship flow: the user sends photos, you write a first-person travelogue around them.

1. **Look at the photos** (you can see images). Take only the atmosphere: weather, season, light, color, mood, activity, objects — narrative material, nothing more. **Never guess the location or the shoot time from pixels** — a wrong guess is a factual error inside a first-person post.
2. **Ask the user for the facts you must not guess** (EXIF is never read; upload channels strip it anyway). Give the reason, then ask:
   - Location: "To protect your privacy, I don't read the location data inside your photos — so let me ask: where was this taken?"
   - Time: "Roughly when was it taken?"
3. **Offer writing styles** (before asking about length). List 4–5, one feel per style, e.g.:
   "What writing style would you like? a. Lyrical & detailed — light, mood, breathing sentences b. Easy & everyday — like chatting with a friend c. Witty & self-deprecating — good for travel-fail stories d. Deep & cultural — history and geography lore e. Minimal & spare — short sentences, white space"
   **Always add the imitation option** (the strongest personalization): "You can also paste a snippet of something you've written — a tweet or a moment post — and I'll write in your own voice (I learn the voice only, never reuse the content)." If the user pastes a sample, analyze sentence rhythm, word choice, verbal tics, emoji/punctuation habits — imitate the voice, never reuse the content. The sample stays in the chat and is stored nowhere.
4. **Offer length options**: "How long should the travelogue be? ~150 words / ~300 words / ~2000 words / your call (platform limit: 50,000 characters, images included)"
5. **Writing rules**:
   - **First person = the user.** The user is the narrator; a digital human, if present, is someone being mentioned — never the narrator.
   - **Use the chosen style** (or the imitated voice). If the user both picks a style and gives a sample, the sample wins — their own voice beats the menu.
   - Weave time into the wording (early morning / dusk / after the first snow); never write a hard timestamp.
   - Only include digital humans that genuinely fit — never force one in.
   - Language follows the user's preference (any language works).

Other inputs are fine too: **Mode A** user provides finished text — skip generation; **Mode C** partial input — you fill in. In every case, location and time come from the user, never from reading pixels.

### Step 2: Digital-human matching

List/suggest healthy digital humans:
```bash
node scripts/match-digital-human.js "<topic>" --limit 3 --json   # ranked suggestions
node scripts/list-digital-humans.js "<name>" --json              # search by name
```
Health filtering is built in: disabled, test-named, garbled, and placeholder-avatar digital humans are excluded automatically. Show the top matches + descriptions and let the user choose (if the user says "you decide", pick automatically).
If the digital human the user wants doesn't exist, give the creation page: https://global.powpow.online
Note: the platform's digital-human library is currently mostly Chinese-language; matching works best when the topic is given in Chinese.

### Step 3: Location handling

**Location is strongly recommended, but optional.** It decides whether the post appears on the public map (the core gameplay).

- **User gives a place name** (the norm): resolve it to coordinates, then let the user pick from same-name candidates:
  ```bash
  node scripts/geocode.js "地坛公园" --limit 5        # add --city 北京 to narrow
  ```
  The script queries the platform's places and locally converts each candidate from GCJ-02 to WGS-84, matching the web editor's coordinate system. Place data coverage is strongest for Chinese place names — non-Chinese users can paste the local-language name.
  **To the user, describe only actions**: "let me look up that place for you", "the map found several places with that name — pick one" — never name the map provider, and never say "map database".
  Show candidates (name/district/address/coordinates) each with a reason, and let the user choose; duplicate place names are common (Chaobai River Bridge has 90 hits). The user picks **by name**; coordinates are your job, not their problem.
  Assembly: `--loc <name> --lng <x> --lat <y>`.
- **Nothing found — degrade in this order, never make the user give coordinates:**
  1. **Rephrase / narrow**: try different words, or add `--city <city>` (district, landmark, road name).
  2. **Widen to help recognition**: raise `--limit` (e.g. 10), show each candidate with district + street address so the user can recognize the right one.
  3. **Publish without a location** — the post is still valid (`isLocationExposed: false`). The user keeps the text, digital humans, and images; only the map bubble is lost. State this as the outcome, not as a failure.
  Making an ordinary user supply latitude/longitude is never a legitimate fallback: they have no way to obtain it, and what they find is usually GCJ-02, which pins off by hundreds of meters — a visible factual error in a first-person post. Coordinates are an expert channel: use them only if the user offers.
- **No location in the material or the conversation**: don't silently produce a location-less post. Tell the user the post will appear on the public map, ask where to pin it, then run the resolution flow above. This question is the only action of the turn — put it in the "Next step" block.
- **User declines to give a location — accept it.** Publish without location (`isLocationExposed: false`). Never pressure, never block publishing — it's their choice.
- User directly provides coordinates: use them as-is.
- Otherwise use the chosen digital human's location (`locationName`, `lng`, `lat`).

**A provided location always goes on the public map (`isLocationExposed: true`) — this is an internal rule; do not offer the user a "hide from map" option.** Posts take part in the bubble lifecycle on the map (fading over time) as intended gameplay.

Location component format:
```html
<span data-type="location" data-lng="116.316" data-lat="39.979" name="中关村">
  <span class="location-name">中关村</span>
</span>
```

### Step 4: Image handling (optional)

Three ways to attach images:
- **Local files** (the norm): `--image @<local-path>`. **Nothing is sent to the server at compose time** — files are recorded into `<out>.manifest.json` and previewed locally via `file://`. Upload happens only at publish time in publish.js (`POST /api/upload/post-image`, JPEG/PNG/WebP/GIF/BMP/HEIC, no SVG, ≤10MB each, server-side compression). Editing drafts never touches the server and never creates orphan files.
- **Direct URLs**: HEAD-check first, then embed. Unsplash photo-page links are recognized too (`unsplash.com/photos/...`, commonly copied from a browser) — automatically resolved to `images.unsplash.com` direct links. File-ID links (`unsplash.com/photos/1507513319174-...`) resolve locally without a key; slug/short-ID links require an Unsplash API key (the site's bot protection blocks keyless scraping). Without a key, skip the slug form and say so — ask the user for a direct link; never embed a page link as an image (it renders broken).
- **Automatic image search** (only if an Unsplash key is configured): `--image search:<english keywords>` (or `node scripts/search-image.js "<keywords>"`)
- No key, no URL, no file → publish without images. Never bundle an image API key.

**No fixed image-count cap.** The platform's boundary is 50,000 characters (each image tag ≈100 chars); remind the user when approaching 200 images. Display: the feed grid shows the first 9 + "+N"; the full-screen viewer shows all.

### Step 5: Content formatting (critical — read carefully)

Interactive components (digital human / location) are rendered by the web frontend from **rich HTML** inside `content`. Writing just `<span data-type="digital-human">Marie Curie</span>` renders as plain text — only a span carrying the tiptap editor's exact structure (Tailwind classes, inner avatar `<img>`, pin icon, `.location-name`) displays as a tappable capsule.

**Mandatory: always use `scripts/compose.js` to assemble post HTML. Never hand-write component spans, never write glue code to bypass html-formatter.js.**

```bash
# 1. Save the post text to a file. Separate paragraphs with blank lines.
#    Placeholders (all optional; any misuse is a hard error, never silently altered):
#      {{dh}}  or {{数字人}}   -> digital-human capsule (requires --dh)
#      {{loc}} or {{位置}}     -> location capsule (requires --loc)
#      {{img}} or {{图}}       -> image paragraph; must be its own paragraph, consumes --image in order
#                                (each one needs a spare --image, otherwise compose fails)
#    Note: the Chinese aliases above are literal tokens recognized by the script —
#    use either form, but never invent new tokens.
#    Unknown/extra/inline placeholders make compose.js exit 1 and write nothing.
#    Fix the text file and rerun — never delete text to force it through.

# 2. Assemble in one command (fully local, no network):
node scripts/compose.js --text-file post.txt \
  --dh name:岳飞 \                    # or --dh <id>, or --dh auto --topic "..."
  --loc dh \                          # or --loc <name> --lng 116.3 --lat 39.9
  --image @./photos/west-lake.jpg \   # local file (uploaded at publish); or <direct-url>, or search:<keywords>
  --out post-draft.html
```

compose.js enforced rules:
- Capsules always match the editor's exact structure (validated before writing).
- **Unknown/extra/misplaced placeholders are hard failures** (exit 1, nothing written). The old version only deleted the placeholder + printed a stdout warning — and since raw script output is never forwarded to the user, a broken sentence ("we sat at for an entire afternoon") could silently go live.
- If `--dh`/`--loc` is given but the text has no placeholder, the capsule is auto-prepended to the first paragraph / appended to the last one.
- Local images become `powpow-local://N` placeholders + `post-draft.html.manifest.json`; publish.js uploads them at publish time.
- compose.js also writes `post-draft.html.preview.html` — a **Chinese-language** preview page the user opens in a browser. Its banner states whether the post will appear on the public map and, if so, where it's pinned — so the map consequence is visible on the page the user actually reads (the local map renders via `file://`). Tell the user in their own language what the banner says.
- `publish.js` re-runs `validateEditorFormat()` and rejects anything else.
- **Do not send `contentItems` in the publish payload** — the frontend prefers structured rendering when `contentItems` is present, and an incomplete list drops post text. `publish.js` handles this.
- The server automatically takes the first `<img>` as the card thumbnail.
- Note: for posts without block-level images, the server takes the digital-human capsule's inner avatar as the thumbnail (platform behavior, cosmetic).

### Step 6: Pre-publish confirmation (mandatory)

First show the four-item breakdown, then end the turn with a "Next step" block whose **only action** is the publish decision (publish / revise more / hold off):

1. **Full post text** (with capsule positions marked)
2. **Component list**: digital human (name + avatar), **location (name + coordinates)**, image count, and **the logged-in account** (taken from the session, not from user input)
3. **Local preview file path** (`<out>.preview.html`) — Chinese-language preview; its banner also states whether the post goes on the public map. One line noting it's an approximation, not a pixel-perfect copy.
4. Ask "Anything to change? If it all looks right, reply 'publish'", plus one line reminding that the post will appear on the public map as a bubble (PowPow gameplay, not a side effect).

The decision must be the last block — never buried after the breakdown. (Why so strict: in testing, users read exactly this content and replied "and then?" — the information was all there, but the action didn't land where the eye stops.)

**Revision loop**: if the user wants changes, make them and rerun compose.js — fully local, any number of rounds with zero server contact and zero orphan uploads. No iteration cap; only an explicit 发布/publish/confirm from the user ends it. Until then, never publish.

### Step 7: Publish

```bash
node scripts/publish.js <html-file-path>
```
If the draft contains local images, this is the moment they upload — one by one, before the post goes out. Progress is persisted after each success (HTML + manifest rewritten with real URLs), so a failed rerun doesn't re-upload what already succeeded.
The post is created as the logged-in user — identity comes from the JWT; there is no way to post as someone else. The server enforces content moderation and rate limits. On 429 the script honors `Retry-After` automatically.

### Step 8: Post-publish verification (mandatory)

```bash
node scripts/verify.js <post-id>
```
Checks post accessibility, author, digital-human/location components, image count, word count. Report in this order — **breakdown first, result last**:

1. **Verification breakdown**: what was read back and what matched — author, digital-human capsule, location capsule, image count, word count. Quote verify.js's numbers as-is (it really counts images; a 3-image post reports 3).
2. One line on the bubble lifecycle (standard phrasing): "A post with a location appears on the public map as a 'bubble' and slowly fades out over time — that's the core of how PowPow works."
3. **Result block, as the very last message line** — closest to the input box, where the eye lands. Must include the link **and the post's location**:

```
────────────────────
✅ Post published
📍 Pinned at: Yanjiao Xinggong Ruins (116.816667, 39.95)
👉 Please open the link and check: do both capsules tap, is the image order right?
   (The command line can't verify that — your eyes are the final gate)
🔗 https://global.powpow.online/posts/<post-id>
```

If there's no location, say so in the same block: "📍 No location — this post won't appear on the public map".

Interactive rendering (capsule taps, image lightbox) can't be verified from the CLI — the user's eyes are the final gate.

Test-post cleanup:
```bash
node scripts/delete-post.js <post-id>
```

## Creating a Digital Human (publishing a digital human)

A separate flow from posting: turn a person (historical figure, character, the user's own avatar…) into a chat-capable digital human pinned to the public map. Triggers: "create a digital human", "turn someone into a digital human on the map", "publish a digital human".

**Cost — confirm before running, just like the publish decision:**
- **What badges are**: badges are a virtual resource earned through activity on PowPow (posting, check-ins) — not money, no card attached.
- **What it costs**: **2 badges per creation, non-refundable**; the finished digital human **expires after 30 days**.
- Run the balance check first (the script does it automatically and aborts if insufficient), then put the cost into the "Next step" block and wait for an explicit confirmation.

Collect from the user:
1. **Name + persona** (both required): who they are, how they talk — 2~4 sentences of persona is enough; the platform's native LLM handles the chatting.
2. **Location** (required): a place meaningful to the character — reuse Step 3's resolution flow and show candidates for the user to pick. Never guess.
3. **Avatar**, one of three (show the options):
   - **AI-generated** (the norm): needs a reference image URL (`--avatar-ref`). The platform generates the avatar from persona + reference (8~30 s). A local reference photo works too — upload it to `/api/upload/post-image` first, then feed the public URL to `--avatar-ref`.
   - **Local upload** (`--avatar @<path>`): use the user's own image directly.
   - **Direct URL** (`--avatar <url>`): a direct image URL.

```bash
node scripts/create-digital-human.js \
  --name 史铁生 \
  --desc-file persona.txt \            # or --desc "..."
  --avatar-ref https://...jpg \        # or --avatar @./photo.jpg, or --avatar <url>
  --lng 116.408195 --lat 39.952372     # from the resolution result the user picked
```

After creation, report the digital-human ID, location, **expiry date (30 days)**, and badge balance, and link the map: https://global.powpow.online/map . The user can immediately @ it in a post (`compose.js --dh <id>`), and it becomes a related candidate for `match-digital-human.js`.

To look up existing ones: `node scripts/list-digital-humans.js --search "<name>"`.

## Error Handling

**Hard rule: never throw raw script output, node commands, or error codes (e.g. DEVICE_MISMATCH) at the user; translate every error into one human sentence + the next action.**

- **401 / session expired (mid-flow)**: it means "the last login expired", not "never logged in" — the two are completely different to the user, and treating expiry as first login makes them think they're starting over. Say "Your previous login has expired — share your account once more and we'll pick up right where we left off", rerun `login.js`, retry once. **Everything done so far is kept**: drafts, material, chosen digital human and location stay local — resume from where you were, never rerun earlier steps.
- **429 rate limit**: the server allows 10 posts/hour/user. Tell the user the wait time; don't hammer retries.
- **400 CONTENT_BLOCKED**: the content failed moderation. Tell the user and ask how they'd like to change it.
- **403 pending_payment**: account not fully activated. This is a hard gate on every login-required call (digital humans, geocoding, image upload, publishing all blocked), with no degraded mode — it can also pop up mid-flow after a successful login. Have the user log in on the platform and finish activation (register: https://global.powpow.online/register); don't retry, don't treat it as transient.
- **423 account locked**: too many failed logins; wait 30 minutes.
- **Wrong credentials (401 at login)**: have the user re-enter credentials, or point to https://global.powpow.online/login (locks for 30 minutes after 5 failures).
- **Local image missing at publish time**: the file was moved/deleted after assembly. publish.js aborts (nothing is sent); rerun compose.js with a valid path.
- **Image search unavailable**: continue without images, or ask the user for a direct URL.
- **Insufficient badges (digital-human creation)** (the script aborts before charging): tell the user the balance; badges are earned through platform activity (posting, check-ins). Don't retry on the same account.

## Support

- Email: dongtao@outlook.com
- Platform: https://global.powpow.online
- Register: https://global.powpow.online/register
- What is PowPow (intro video, in Chinese): https://www.bilibili.com/video/BV1Wu826UEVz/

## Notes

- Always verify the post actually went live after publishing; delete test posts afterwards.
- Never publish without the user's explicit confirmation.
- Never store/log user passwords; only the JWT session is cached locally.
- **Password handling (internal rule — don't explain to the user)**: use the stdin pipe — `printf '%s' '<password>' | node scripts/login.js <username>`. Never the positional form (`login.js <user> <password>`): it lingers in shell history and process lists. No echoing, no disk writes, no shell variables. `login.js` still accepts the positional form for compatibility — that is not permission to use it. Asking the user for credentials should be one plain message, without security lecturing (see Conversation UX → Tone).
- **Path rule**: only pass paths the user explicitly gave for `--text-file`/`--image`, or files you created in the current working directory. Never scan the machine, never guess paths — a wrong path publishes private files.
- Never guess location/time from photos — ask the user; a wrong guess is a factual error in a first-person post.
- A provided location always goes on the public map (internal rule, no opt-out; see Step 3).
- **Never name the map provider to the user** — say "let me look up that place for you". Applies to prose, option lists, and any rewriting of script output (see Conversation UX → provider-neutral naming).
- **Never ask the user for coordinates.** Fallback order: rephrase → widen candidates → publish without location.
- This skill is safe to distribute: it contains no platform credentials; dangerous capabilities (identity, rate limits, moderation) are all enforced server-side.
