# WeChat Benchmark Fit And Writing Workflow

Use this playbook when the user sends WeChat articles they like plus one of
their own drafts, notes, transcripts, ideas, or published articles, and wants
Lingzao to judge whether those references are suitable benchmarks, find better
references when needed, and produce an original WeChat public-account article.

Trigger phrases include:

- 我喜欢这几篇公众号文章
- 这些能不能成为我的对标
- 结合我自己的内容判断适不适合学
- 帮我找更适合我的公众号对标
- 学习这些文章以后帮我写一篇
- 公众号对标校准
- 根据我的内容写公众号

## Product Model

Start from the user's taste and real material, not from a request for an account
archive:

```text
liked public links + user's own content
-> explain what the user actually likes
-> diagnose the user's content identity and resources
-> judge benchmark fit
-> supplement better references only when needed
-> extract mechanisms, not wording
-> write an original article from the user's own facts
```

Do not require historical articles before starting. One current piece of the
user's own content is enough for a first calibration. Historical material may
improve confidence later, but it is optional.

## Minimum Input

Accept the smallest useful package:

- 1-5 public article links the user likes
- one piece of the user's own content: draft, note, transcript, article,
  product update, customer question, case, or voice memo
- intended destination: personal WeChat account or official WeChat account

Infer the reader, account role, and goal from the material when possible. Ask
only when the missing answer would materially change the benchmark judgment.

If the user has no liked links, accept their own content first and use it to
define a narrow benchmark-search brief. If the user has links but no own
material, analyze taste and reference quality, but do not claim that the
references fit the user yet.

## Current Capability Boundary

Lingzao can:

- open a user-provided public WeChat article with `get-article-detail`
- save a complete public article as Markdown with
  `get-article-detail --output <path>`
- read public article metrics with `get-article-stats` when needed
- expand related public articles from a seed URL with
  `get-related-articles`
- compare reference mechanisms with user-provided content
- produce personal-account or official-account drafts, HTML-ready structures,
  cover directions, and image directions

Lingzao does not currently promise:

- finding a complete account archive from only an account name
- a WeChat hot-ranking feed
- copying another account's voice, identifiable wording, story, or brand asset
- guaranteed reads, followers, sales, or conversion
- automatic background monitoring, draft-box sync, or publishing merely
  because the Skill is installed

Do not describe cross-platform topic signals as a WeChat ranking. If WeChat
reference discovery is not reachable from the available seed links, label the
gap honestly.

## Stage 1: Read The User's Taste

Open the liked links only after confirming the research scope.
Default to a maximum of 3 reference articles in the first pass.

For each reference, identify what may be creating the user's attraction:

- topic or reader problem
- title promise
- opening tension
- author identity or point of view
- story or case density
- evidence system
- section rhythm
- emotional movement
- practical method
- commercial transition
- visual or layout feeling when visible

Separate:

- `user explicitly likes`
- `Lingzao infers they may like`

Do not treat popularity as the same thing as suitability.

## Stage 2: Read The User's Own Content

Create a compact user-content card:

- current topic
- intended reader
- real experience, fact, case, or product evidence
- central judgment
- natural voice
- strongest distinctive resource
- account role: personal, official, or unclear
- content goal: trust, method, product education, reflection, or conversion
- current weakness: topic, opening, evidence, structure, voice, or ending

Do not flatten a personal account into a generic method account. Do not turn an
official account into a founder diary.

## Stage 3: Judge Benchmark Fit

Score each reference qualitatively across these dimensions:

| Dimension | Fit Question |
| --- | --- |
| Reader | Is it speaking to a similar reader and problem? |
| Account role | Is it personal, official, media, expert, or sales-led like the user? |
| Account stage | Is the reference usable at the user's current trust and audience stage? |
| Evidence | Can the user support a similar structure with their own real facts? |
| Identity | Does the style fit the user's identity and speaking position? |
| Business path | Does its conversion path fit the user's actual product or goal? |
| Format | Can the user sustain its length, rhythm, images, and production cost? |
| Originality room | Can the mechanism be adapted without copying recognizable expression? |

Return one of three conclusions:

- `strong fit`: worth learning as a primary benchmark
- `partial fit`: learn named mechanisms only
- `not fit`: attractive, but likely to distort the user's account

For every conclusion, explain:

- why it fits or does not fit
- what can be learned
- what should not be copied
- what the user would need to make this route credible

Do not tell the user to learn an account merely because the article is popular
or beautifully written.

## Stage 4: Supplement Better References

Search or expand only when:

- the liked references are mostly `not fit`
- the set lacks a needed account role or content type
- the user's own content reveals a clearer benchmark category
- the user explicitly asks Lingzao to find alternatives

First derive a search brief from the user's content:

- target reader
- account role
- topic category
- evidence type
- tone
- business path
- current account stage
- excluded styles

Then return up to 3 better starter references. Prefer real public article links
with a one-line fit reason. Use `get-related-articles` only from a confirmed
seed URL and within the confirmed research scope.

When direct WeChat discovery is not available, use reachable public content
signals only as topic/mechanism references and label them separately. Do not
present a Xiaohongshu or Douyin creator as a verified WeChat benchmark account.

## Stage 5: Extract Mechanisms

Build a benchmark mechanism table:

| Reference | Learnable Mechanism | Why It Fits | User's Own Replacement Material | Do Not Copy |
| --- | --- | --- | --- | --- |

Mechanisms may include:

- title tension
- opening question or scene
- story-to-judgment transition
- evidence placement
- section progression
- method explanation
- ending movement
- content-to-product transition

Do not reuse identifiable sentences, personal stories, private details,
signature metaphors, or visual identity.

## Stage 6: Map Back To The User

Before writing, require this mapping:

| Reference Mechanism | User's Real Fact/Case | User's New Judgment | Use or Park |
| --- | --- | --- | --- |

If the user lacks the facts needed to support the article, produce:

- one-sentence topic judgment
- missing-material list
- interview or reflection prompts
- a detailed outline

Do not fabricate a finished personal article from benchmark material.

## Stage 7: Write The Original Article

### Personal WeChat Account

Use the user's real scene, choice, correction, limitation, and judgment. The
article may borrow a reference's structural mechanism, but it must sound like
the user's lived experience rather than a generic expert article.

### Official WeChat Account

Use a concrete reader problem, official judgment, reusable workflow, evidence
boundary, and next step. Do not invent founder history or use private diary
language.

### Dual-Account Route

For one shared mother topic:

- personal account: experience, decision, correction, and judgment
- official account: problem, method, workflow, and reusable boundary

Do not publish one article twice with only a changed title or cover.

## Output Contract

Return:

1. user taste summary
2. user-content card
3. benchmark fit table
4. recommended primary and secondary references
5. learnable vs non-copyable mechanism table
6. one selected article direction
7. 3 WeChat-native titles
8. complete draft or requested outline
9. evidence and originality notes
10. next material or test needed

If images are requested, route to the WeChat path in
`visual-generation-and-cover-workflow.md` or
`image-generation-execution-workflow.md`.

## Quality Gate

Before marking the output ready, check:

- every reference has a real public link
- benchmark fit is judged against the user's actual content
- popularity is not used as proof of fit
- the central facts and stories belong to the user
- no recognizable source wording or identity asset was copied
- personal and official voices are separate
- title is a complete WeChat judgment, not a stretched Xiaohongshu title
- unsupported metrics or commercial claims are removed or scoped
- the article contains a real judgment, not only a reference-shaped structure
- final publication remains a human decision

## Optional Learning Library

After 2-3 successful calibration rounds, offer a lightweight library:

```text
wechat-benchmark-library/
  preferences.md
  user-content-profile.md
  accepted-benchmarks.md
  rejected-benchmarks.md
  mechanism-library.md
  drafts/
  state.json
```

Save why each reference was accepted or rejected. This teaches the workflow the
user's taste without requiring a full historical archive.

## Optional Scheduled Layer

Only propose a recurring task after the benchmark category and writing route
have been validated manually.

A scheduled run should:

- read the accepted benchmark list and user-content profile first
- process only new user-submitted or reachable articles
- deduplicate before online calls
- compare new references with the user's latest content
- update fit judgments instead of assuming every source remains useful
- stop at the confirmed research boundary
- create drafts only; never publish automatically

The Agent runtime owns the schedule. Lingzao owns each scoped calibration and
writing run.

## First MVP

Use:

- 1 piece of the user's own content
- up to 3 liked public links
- 1 benchmark-fit report
- up to 3 supplemental references only if needed
- 1 original WeChat article direction
- 1 complete draft or detailed outline
- 1 review round before creating any recurring automation
