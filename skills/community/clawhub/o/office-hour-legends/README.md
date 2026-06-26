# office-hour-legends

A Claude Code skill that runs YC-style office hours, simulated by a specific
YC partner or alumnus of your choice.

Pick a legend (Garry Tan, Paul Graham, Dalton Caldwell, Michael Seibel, or one you add).
Tell them what you're working on. They run the standard office-hours forcing
questions through their voice, values, and pattern-recognition.

**Works in your native language.** You can run the entire session in Spanish,
Mandarin, Portuguese, Hindi, Japanese, Arabic, French, or any other language
you think in. See [Run office hours in your native language](#run-office-hours-in-your-native-language).

## Install

This is a [Claude Code skill](https://code.claude.com/docs/en/skills). It
lives in `~/.claude/skills/` and is activated by Claude Code automatically.

```bash
git clone https://github.com/prodigalson/office-hour-legends.git \
  ~/.claude/skills/office-hour-legends
```

That's it. Restart Claude Code (or open a new session) and the
`/office-hour-legends` command is available.

To update later:

```bash
cd ~/.claude/skills/office-hour-legends && git pull
```

## Quick start

```
/office-hour-legends garry
/office-hour-legends paul-graham
/office-hour-legends "jessica livingston"
```

Leave the name off and the skill will ask which legend you want:

```
/office-hour-legends
```

Then tell the legend what you're working on. The session begins.

### Run office hours in your native language

You do not have to speak English to use this. Tell the legend what language
you want to work in and the entire session happens in that language - the
forcing questions, the pushback, the alternatives, the design doc at the end.

```
/office-hour-legends garry
> Let's do this in Spanish. Estoy trabajando en una plataforma de logistica...
```

```
/office-hour-legends paul-graham
> 日本語でお願いします。AIで契約書をレビューするツールを作っています。
```

The legend stays in character - Paul Graham's Socratic style, Garry Tan's
demand for the demo, Dalton Caldwell's tarpit skepticism - just delivered in
your language. Specific phrases that are uniquely English (YC jargon, direct
quotes from their essays) may stay in English when it helps; everything else
translates.

This opens the skill to any founder anywhere. If English is slowing you down
when you try to describe your startup, switch. You will give sharper answers
in the language you actually think in, and the legend's feedback will land
harder.

Works with every mode below: standard office hours, transcript review,
Bookface research, and HN research. Transcript reviews of non-English
meetings work too - the legend reads the transcript in its original language
and gives feedback in whatever language you ask for.

### Bookface research mode

If you install the [bookface-search](https://github.com/voska/bookface-search)
skill alongside this one, legends can ground the session in real YC founder
discussions instead of generic advice. When a founder makes a claim about
demand, status quo, or a competitive landscape, the legend searches Bookface
(YC's internal forum) and cites actual founder experiences back.

Example, mid-session:

> You said nobody is doing this, but I've seen founders on Bookface wrestle
> with the same space. Here's one from last year who tried your exact wedge
> and hit a wall at onboarding. Worth reading before you commit.

No setup needed beyond installing the bookface skill - legends auto-detect it.
If it's not installed, sessions run normally without it. See
[Bookface integration](#bookface-integration) below.

### Hacker News research mode

If you install the [hn CLI](https://github.com/voska/hn-cli), legends also
pull public Hacker News signal during the session - Show HN launches in the
space, comment sentiment on the founder's idea, what the HN crowd says about
the incumbent the founder is trying to replace, and the current front-page
bar if you're heading toward a launch.

Example, mid-session:

> You said nobody's doing this. Someone launched this exact pitch on HN
> nine months ago - 340 points, 180 comments. Top comment is still the
> funniest takedown of the idea I've read. Read it before tomorrow, then
> tell me what they did wrong and why you're different.

HN is public opinion; Bookface is private founder reality. Together the
legend can triangulate: what YC founders whisper to each other vs. what the
wider world says out loud. No setup beyond installing `hn` - free API, no
auth. See [Hacker News integration](#hacker-news-integration) below.

### Transcript review mode

Have a legend review a real meeting from [Fathom](https://fathom.video) - an
investor pitch, a customer call, a cofounder conversation. The legend reads
the full transcript and gives you timestamped feedback on what you did well,
what you missed, and what the other party signaled that you may not have caught.

```
/office-hour-legends dalton
> review my pitch from yesterday
```

The skill pulls your recent meetings from the Fathom API, lets you pick one,
and the legend goes through it with you live.

**Requires:** `FATHOM_API_KEY` environment variable. See
[Fathom transcript review](#fathom-transcript-review) below for full setup.

## Included legends

| Legend | Focus |
|--------|-------|
| **Garry Tan** | Product craft, shipping speed, demos, user-led growth. Will ask for the actual demo in the first 30 seconds. |
| **Paul Graham** | First-principles thinking, founder-problem fit, growth rate, schlep blindness. Socratic, essay-style. |
| **Jessica Livingston** | Founder psychology, co-founder dynamics, user empathy. The "social radar." Warm, asks about your story. |
| **Sam Altman** | Ambition, rate of improvement, conviction, compounding. Low-affect, high-signal. Will ask what you believe that most people don't. |
| **Justin Kan** | Distribution, pivots, founder mental health, radical honesty. Will ask how you're actually doing before asking about the product. |
| **Dalton Caldwell** | Idea evaluation, tarpit detection, founder-market fit. Will tell you he's seen fifty versions of your idea and explain why they all failed. |
| **Michael Seibel** | Launching fast, real metrics, cutting through excuses. Will ask if you've launched yet before anything else. |
| **Paul Buchheit** | Product taste, core insights, user delight. Creator of Gmail. Will ask for the "whoa" moment in your product. |
| **Tom Brown** | Scaling, empirical rigor, AI product evaluation. Lead author of GPT-3. Will ask how you know your product works and where it breaks. |
| **Qasar Younis** | Enterprise sales, hard industries, operational discipline. Will ask who the buyer is and whether you have a signed contract. |

## What happens during a session

### Standard office hours

1. **Opening.** The legend introduces themselves and asks what you're working on.
2. **Forcing questions.** Six questions about demand, status quo, specificity,
   wedge, observation, and future-fit, asked in the legend's voice.
3. **Pushback.** They challenge weak assumptions and follow up on what they notice.
4. **Alternatives.** A few different approaches to the problem, for you to weigh.
5. **Design doc.** A markdown file is saved summarizing the session, tagged
   with which legend ran it.

### Transcript review

1. **Meeting selection.** The skill fetches your recent meetings from Fathom and
   lets you pick one (or auto-matches if you name it or paste a Fathom URL).
2. **Full read.** The legend reads the entire transcript, summary, and action items.
3. **Timestamped feedback.** The legend walks through the meeting: what you did
   well, what you fumbled, and investor/customer signals you may have missed.
4. **Rewrite suggestions.** For the weakest moments, the legend writes what they
   would have said instead.
5. **Live session.** You go back and forth with the legend to sharpen your pitch,
   rework answers, or pivot into a broader office-hours discussion.
6. **Session doc.** A markdown file is saved with the full review, timestamped
   notes, and action items.

## Fathom transcript review

Transcript review lets you bring a real meeting into office hours. Instead of
describing what happened, the legend reads the actual conversation and reacts
to it - what you said, what the other person said, what signals got missed,
and what you should say differently next time.

### Setup

1. **Get your Fathom API key.** Go to
   [fathom.video/settings](https://fathom.video/settings), scroll to the API
   section, and copy your key.

2. **Set the environment variable.** Add this to your `~/.bashrc` or
   `~/.zshrc`:

   ```bash
   export FATHOM_API_KEY="your-api-key-here"
   ```

   Then restart your shell or run `source ~/.bashrc`.

3. **That's it.** The skill auto-detects when you ask for a transcript review
   and handles the rest.

### How it works

1. You pick a legend and tell them you want to review a meeting:

   ```
   /office-hour-legends paul-graham
   > I pitched to an investor yesterday, can you review the transcript?
   ```

2. The skill calls the Fathom API and shows your recent meetings. You pick the
   one you want reviewed.

3. The legend reads the full transcript - every speaker, every line, every
   timestamp - plus Fathom's AI summary and action items for extra context.

4. The legend delivers structured feedback:

   - **Overall impression** - their gut reaction, as if watching from the back
     of the room
   - **What you did well** - specific moments with timestamps and your actual
     words quoted back
   - **What you missed or fumbled** - specific moments where you could have
     been stronger, with the legend's rewrite of what to say instead
   - **Investor/customer signals** - moments where the other person showed
     interest, concern, or skepticism that you didn't pick up on
   - **Questions you should have asked** - what the legend would have wanted
     you to ask that you didn't

5. After the initial feedback, you go live. The legend stays in character and
   you work through the issues together:

   - Sharpen specific answers ("The investor asked about retention - let's
     rework your response")
   - Practice handling objections they raised
   - Pivot into a broader office-hours session about the company

6. A session doc is saved with the full review, timestamped notes, and action
   items for your next meeting.

### What triggers transcript review

The skill switches to transcript review mode when you say things like:

- "Review my pitch" / "review my meeting" / "review my call"
- "Look at my transcript" / "go over my transcript"
- "I had a meeting with an investor" / "I pitched to..."
- Paste a Fathom URL (fathom.video/calls/...)
- Mention "fathom," "transcript," or "recording"

If you just say "I'm working on X," it runs standard office hours instead.

### What Fathom data the skill uses

The skill reads from the Fathom API (via `scripts/fathom-list-meetings.sh`
and `scripts/fathom-get-transcript.sh`):

| Data | Source | Used for |
|------|--------|----------|
| Meeting title and date | Fathom API | Letting you pick which meeting to review |
| Participant names | Fathom API | Identifying who said what |
| Full transcript | Fathom API | The legend reads every word and gives timestamped feedback |
| AI summary | Fathom API | Extra context for the legend's overall assessment |
| Action items | Fathom API | Cross-referenced with the legend's own recommendations |

The API key is user-scoped - it only accesses meetings you recorded or that
were shared to your team. Rate limit is 60 calls/minute.

### Example session

```
> /office-hour-legends dalton

Legends - office hours with Dalton Caldwell. Ready when you are. What are we
looking at?

> I pitched to a VC yesterday. Can you go over the transcript?

[Skill fetches recent meetings from Fathom]

I see a few recent meetings. Which one?
1. Meeting with Sarah Chen - Apr 14
2. Team standup - Apr 14
3. Meeting with First Round - Apr 13

> 3

[Skill fetches full transcript for "Meeting with First Round"]

Alright, I read the whole thing. Here's my take...

Overall: You started strong but lost the thread about halfway through when
they asked about competition. Let me walk through it.

[00:01:15] Good - you opened with the problem, not the solution. "We noticed
that every logistics company we talked to was still using spreadsheets for..."
That's the right instinct. You grounded it in something real.

[00:04:30] This is where it gets shaky. They asked "who else is doing this?"
and you said "nobody, really." I've seen fifty versions of that answer. It
never lands. Someone is always doing something adjacent. Here's what I'd say
instead: "The closest thing is X, but they're approaching it from Y angle.
We're different because..."

[00:08:12] They asked about your growth rate and you gave them an absolute
number instead of a percentage. Always give the weekly growth rate...
```

## Bookface integration

The legends skill optionally integrates with
[bookface-search](https://github.com/voska/bookface-search) to ground sessions
in real YC founder discussions from Bookface, YC's internal forum.

### What it does

When Bookface is available, the legend searches it live during the session
at these moments:

- **Demand pushback.** Before challenging a founder's demand claims, the
  legend pulls real founder experiences with the same problem space.
- **Status quo naming.** The legend checks how other YC founders describe
  their workarounds with the same tools.
- **Alternatives generation.** The legend searches the YC company directory
  for shipped products in the space, so alternatives are grounded in real
  companies instead of hypotheticals.
- **Assignment handoff.** The legend cites YC's canonical guide on the
  relevant pattern when handing off a next action.
- **Transcript rewrites.** For the weakest moments in a reviewed pitch, the
  legend folds a real founder's phrasing into the suggested rewrite.

### Who can use this

Bookface is YC's private forum for founders of funded YC companies. **Only
current YC founders have accounts.** If you're not in a YC batch, you can
ignore this whole section - legends run normally without it.

Also: the script logs in with username + password via YC's web form. If
your YC account uses Google SSO only (no password set), you'll need to
set a password on your YC account first, or the script can't authenticate.

### Install

```bash
git clone https://github.com/voska/bookface-search.git \
  ~/.claude/skills/bookface
```

Then set your YC credentials. Two options:

```bash
# Option A: env vars in your shell rc (~/.bashrc, ~/.zshrc)
export BOOKFACE_USERNAME="your-yc-username"
export BOOKFACE_PASSWORD="your-yc-password"

# Option B: a credentials file the script sources
cat > ~/.bookface_credentials <<'EOF'
BOOKFACE_USERNAME="your-yc-username"
BOOKFACE_PASSWORD="your-yc-password"
EOF
chmod 600 ~/.bookface_credentials
```

Restart Claude Code. Legends auto-detect Bookface and use it when the
session benefits.

### How auth works (and what to watch for)

- **No OAuth.** The script does form-based login: scrapes a CSRF token from
  `account.ycombinator.com`, POSTs your creds to `/sign_in`, and extracts
  an Algolia API key from your logged-in home page.
- **Session cache.** The Algolia key is cached at `/tmp/bookface_algolia_key`
  for ~12h, so you only pay the login cost once per session. Cookies live
  at `/tmp/bookface_cookies`.
- **Credentials on disk.** `~/.bookface_credentials` is a plaintext shell
  file. `chmod 600` it. Don't commit it. Don't sync it into a cloud drive.
- **Brittle to YC changes.** If YC adds 2FA, captcha, or changes the sign-in
  form, the script will break until upstream updates it. Legends skip
  Bookface silently when the script errors - sessions still run.
- **Force re-auth.** If searches start failing, delete the cached files:
  `rm -f /tmp/bookface_algolia_key /tmp/bookface_cookies`.

### When it doesn't run

- **Lite mode.** Bookface research only runs in full mode. Lite mode stays
  fast and cheap.
- **Not installed.** If `~/.claude/skills/bookface/bookface-search.sh` is
  missing, legends skip Bookface silently and run normally.
- **Builder mode.** Side projects and hackathons skip it by default. The
  research is for startup questions where YC's corpus adds weight.

### Rules

- Legends **quote, don't paraphrase** Bookface findings. Real founder words
  carry more weight than a summary.
- Legends stay in character: "I've seen founders on Bookface wrestle with
  this..." not "I searched Bookface and found...".
- No more than one or two citations per session. This is seasoning, not a
  research report.

## Hacker News integration

The legends skill also integrates with the
[hn CLI](https://github.com/voska/hn-cli) to pull public Hacker News signal
alongside Bookface's private-YC view. Where Bookface shows what YC founders
say to each other, HN shows what the wider tech world says out loud -
launches that succeeded or flopped, ideas that got trashed, incumbents that
everyone secretly hates.

### What it does

When `hn` is on PATH, the legend searches HN live during the session at
these moments:

- **Competitive reality check.** When the founder says "nobody's doing
  this," the legend searches HN for the space. If someone launched the
  same pitch and got 500 points two years ago, the legend brings it up.
- **Status quo sharpening.** HN threads on incumbents (Jira, spreadsheets,
  Salesforce) contain the sharpest descriptions of why people hate the
  status quo - and why they still use it. The legend pulls real comment
  phrasing into the pushback.
- **Launch-bar calibration.** Before the assignment phase, the legend
  checks the current Show HN front page so "ship by Friday" advice is
  grounded in what actually gets traction right now.
- **Sentiment on the specific idea.** The legend searches for the
  founder's own pitch. If HN has already rejected it twice, the legend
  names that directly. If it's been loved before, the session pivots to
  differentiation.
- **Investor/fund color.** In transcript review, the legend can check HN
  for public commentary on the VC the founder pitched.

### Install

The hn CLI ships as a single binary. See
[voska/hn-cli](https://github.com/voska/hn-cli) for install instructions.
Verify it works:

```bash
hn search "show hn" -n 3
```

No credentials, no auth, no rate limit headaches - free Algolia API.

### Rules the legend follows

- **HN is public opinion, Bookface is private founder reality.** The
  legend keeps them distinct. "The HN crowd trashed this last year" is a
  different signal than "A YC founder who tried this told the forum..."
- **HN is often wrong about B2B.** The legend treats HN sentiment as
  signal, not gospel - especially for enterprise ideas HN has historically
  dismissed (Slack, Zoom, Dropbox all got panned).
- **Quote real comment phrasing.** HN's sharpest critics write better than
  any summary. When a comment lands, the legend pulls it verbatim.
- **One or two citations per session.** Seasoning, not a research report.

### When it doesn't run

- **Lite mode.** HN research only runs in full mode.
- **Not installed.** If `hn` isn't on PATH, legends skip silently and run
  normally.

## Add your own legend

Each legend is a folder of plain markdown files under `personas/`. To add one:

```bash
cp -r personas/_TEMPLATE personas/jane-doe
```

Then fill in the four files:

| File | Purpose |
|------|---------|
| `identity.md` | Who they are, role, track record, what they're publicly known for |
| `soul.md` | Values, beliefs, what they care about, what frustrates them |
| `skills.md` | Domains of expertise, the lenses they apply, what they pattern-match on |
| `voice.md` | How they talk: cadence, phrases, things they never say, humor style |

Extra files are fine (`investments.md`, `essays.md`, `pet-peeves.md`). The
skill reads every `.md` in the folder.

Test it:

```
/office-hour-legends jane-doe
```

Concrete details beat generic ones. Real quotes from their writing, real
examples, real things they've said in interviews: those make the voice feel
real. Iterate by editing the markdown files; no code changes required.

## Tips for a good session

- **Bring something real.** A vague idea gets vague feedback. A specific
  problem you've lived with gets sharp feedback.
- **Be honest when you don't know.** Good legends respect "I don't know" more
  than a polished guess.
- **Let them disagree.** If the legend pushes back, don't immediately agree or
  immediately defend. Sit with it.
- **Try the same idea with different legends.** Paul will ask different
  questions than Jessica. You learn something from each.
- **Review your pitch before AND after.** Run a standard office-hours session
  to prep before a meeting, then review the Fathom transcript after to see
  what actually happened vs. what you planned.
- **Use transcript review with different legends.** Dalton will focus on
  whether the idea held up. Michael will focus on whether you were direct
  enough. Paul Buchheit will focus on whether the product demo landed. Each
  lens catches something different.

## Project layout

```
office-hour-legends/
├── SKILL.md              # the skill definition Claude Code loads
├── README.md             # this file
├── LICENSE
├── scripts/
│   ├── fathom-list-meetings.sh   # fetch recent meetings from Fathom API
│   └── fathom-get-transcript.sh  # fetch full transcript for a meeting
└── personas/
    ├── _TEMPLATE/        # starter for new legends
    ├── garry-tan/
    ├── paul-graham/
    ├── jessica-livingston/
    ├── sam-altman/
    ├── justin-kan/
    ├── dalton-caldwell/
    ├── michael-seibel/
    ├── paul-buchheit/
    ├── tom-brown/
    └── qasar-younis/
```

## Rules

- The skill does not invent quotes or investment decisions the real person
  never made. It channels their thinking; it does not fabricate their history.
- This is simulation for product feedback, not actual YC decisions or advice
  from the real people.

## License

[MIT](LICENSE)
