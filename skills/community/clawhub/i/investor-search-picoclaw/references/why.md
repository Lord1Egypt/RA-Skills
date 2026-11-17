# Why each rule exists

`SKILL.md` is the rules. This is the evidence. Read it when a rule looks arbitrary, when you
want to argue with one, or before you relax one.

**Every rule here was written after something broke.** None was designed in advance. The
provenance is kept because a rule whose failure you can picture is a rule you will follow at
three in the morning on the fortieth page.

## Where it comes from

| source | what it contributed |
|---|---|
| A production investor-research system, run over several months and hundreds of pages | the exhaustion rule, the exclude-list logic, the seed handling, the type vocabulary, the contradiction rule |
| **Czech Republic** | 13 defects. No adviser test at all; the fold's step order; the contradiction rule blanking correct types |
| **UAE** | the fold silently merging two different companies; nine of ten local legal forms not folding; the language rule inverting |
| **Singapore** | 14 more. A five-way fold collision caught; and the finding that the skill had become too long to follow |
| **Estonia** | **the exhaustion rule fired and was wrong** — falsified inside the same run. Leading legal forms. Rebrands invisible to every rule |
| **Latvia** | Job 0 barely fired: 16 of 31 association members left undecided because a name may not decide a type and the budget went elsewhere. Manager-versus-fund undefined. Two headquarters, one column |

---

## Job 0 — the adviser test

**This rule did not exist in the first two versions of the skill.** It was added after a
run produced a list that was defensible on every axis the skill measured and wrong in
the way that mattered.

> **Czech Republic:** five of the six firms verified from local-language queries were law
> firms, accountancies and consultancies *selling* family-office services. Real names, live
> sites, real headquarters. They passed every check. Then the type allowlist saw the words
> `family` and `office` and typed them `family_office` with a native-language quote
> attached.
>
> **UAE:** 16 advisers rejected against 15 firms kept — **52% of everything resolved.** One
> round, with as targeted a query as could be written for a real investor, returned **eight
> results, eight advisers, zero investors** — company-formation agents and free-zone
> licensing consultancies selling "Family Office Setup" packages.
>
> **Singapore:** 13 rejected. Every Chinese-language site in the run was an adviser.

The failure mode is specific and worth naming: **the file is wrong while looking more
trustworthy than a careless one**, because every row carries a URL, a date and a quotation.
The skill spends its length arguing that provenance should replace confidence scores. It is
right about that — but provenance is not truth, and a row can be perfectly provenanced and
still not be a family office.

### Why the preposition rule

One real single family office describes itself as one that *"**advises** investment vehicles
associated with the … family"* — its own principal. Read against a keyword list, "advises"
is disqualifying and a genuine investor is thrown away. It survives only because it advises
*its own* principal's vehicles, not third parties. The rule works, but it works on a
distinction one word wide.

### Why `operating_group` exists

The UAE test could not answer Job 0 for the dominant local form. A family conglomerate —
hotels, dealerships, retail, property — is family-owned, enormous, plainly not an adviser,
and does not describe deploying capital into anything it does not operate. Two rows shipped
as `unclear` and neither was trusted.

**The conglomerate is how Gulf family capital is actually held.** A skill that can only see
"investor" and "adviser" cannot describe the market it was pointed at. Singapore confirmed
it: 7 of 33 rows, and omitting them would make a Singapore list simply wrong.

### Why `syndicate` exists

Singapore surfaced angel networks and membership bodies — they route other people's capital
and are neither an investor nor an adviser. Same shape of gap as the conglomerate, found one
version later.

### Why `notAnInvestor` is separate from `adviserNotInvestor`

Both send the firm to `investors-rejected.csv`, so one code would have done the job of
rejecting. The reason they are separate is that they say different things about the *source*.
`adviserNotInvestor` means the directory was right about the firm and the firm is simply out
of scope. `notAnInvestor` means the directory was wrong — it listed an energy developer, a
manufacturer or a consultancy with no family-office pretension as an investor. **Separating
them is how you find out whether a directory is unreliable**, which decides whether its
remaining names are worth the rounds. Merged into one code, a directory that is 40% noise
looks the same as one that is 40% advisers.

### Why sovereign subsidiaries are kept

Six government entities surfaced in the UAE and four in Singapore. The parents are out of
scope. But their **commercial arms** are a large and legitimately targetable population, and
an early version had no rule for them, so they were parked wholesale. In the Gulf especially,
sovereign and ruling-family vehicles blur continuously — recording the question is more
honest than answering it.

---

## Job 1 — the exhaustion rule

### Why the exhaustion rule now has four gates

**This is the most important finding in the project, and it is against the skill's own
headline claim.**

Estonia was chosen because it is small enough that exhaustion is actually reachable — the
first three tests all stopped on budget, so the rule had never once fired in a standalone
run. It fired at round 23, on a streak of rounds 18–23.

> **It was wrong, and it was falsified at round 26 of the same run.** A plain English query
> that had not been tried produced two firms that had not appeared once in 25 prior rounds;
> round 28 added a third, and a fourth row was promoted from a bare directory line to a sourced
> firm. **Four of the final 29 rows arrived after the rule declared the market finished.** Nothing about Estonia changed. A query shape changed.

Three structural causes, each now a gate:

1. **The queue was invisible to the counter.** A regulator's register handed over 85 fund
   managers at round 8. Ten closed the round; **75 went to a queue** that, by the rule's own
   text, *can never reset the streak*. **The rule fired while holding regulator-confirmed
   names it had told itself not to count.**
2. **Six dry rounds were six web searches — one surface, not six.** The registry surface
   yielded 85 on a single fetch and the association surface 28, *after* web search had gone
   dry. **A surface never tried cannot be dry.**
3. **One garbled fetch caused the streak.** An article listing family offices in the region
   returned cipher text at round 2. The garble rule protected the streak
   counter but not the evidence, so the page was never recovered. The same content on a
   mirror at round 26 held two of the three firms that broke the exhaustion.

And a fourth thing, not fixable by a gate: **the streak hinged on one judgement.** A single
Job 0 rejection — an energy developer a directory had listed as an investor — is what made
one round dry. Trust the directory and the streak breaks at five and never fires.

**And the gates are not themselves proven.** They were written after this run, and every run
behind this skill stopped on budget rather than on exhaustion. They are a design with an
argument, not a measured result, and the skill says so in three places on purpose.

**What this costs the claim.** "Six queries I chose stopped working" is not "this market is
exhausted". The skill may now only claim exhaustion **on the surfaces it names**, and must
name them. That is a weaker sentence than the one the skill was built to say — and it is the
true one.

### Why six dry rounds, and not a target

> Three real runs of the production system, one rule, three honest numbers:
> **351** firms in Germany over 253 pages · **36** in Poland searched in English over 34 ·
> **46** in Poland searched in Polish over 48.
>
> *(These are production-system runs, not runs of this skill, and the two Poland runs used
> different page budgets — 34 against 48 — so they are not a controlled comparison,.)*
>
> A target of thirty would have reported **30 · 30 · 30** — the same answer three times, and
> wrong all three.

**A target is not a shortcut. It is an instruction to keep going until the count is met —
the exact pressure under which a model begins inventing firms.** By roughly page 15 the real
names are exhausted; what comes after is plausible firms that do not exist.

### Why both halves of the instruction

> Measured on one production run: told *"at most 10"*, the model returned **2.0 a page**, with zero
> dropped for a dead source and zero for a missing headquarters. **Nothing was being filtered
> out — the search simply was not looking.** Four sentences pushed the count down and none
> said *look hard*.

### Trap 1 — the bucket with a hole

> Measured on one production run: 13 pages, `{"unverifiedSource":0,"alreadySeen":20,
> "noHeadquarters":0}` — every one of those 20 a name already given and thrown away without
> saying so. The dry-well detector read three pages of "no new verified name" and called the
> well dry.
>
> **The well was not dry; the bucket had a hole.**

### Why Gate 0 exists — the filesystem was an unstated requirement

Every market run ran on an agent with a working directory, so a question never
got asked: *what does this skill do where there is no working directory?*

It was asked by a run on a chat-only agent. The result was a competent, correctly-judged
answer delivered as **prose** — no CSV, no pending queue, no round log. Every judgement in
this document had run. Not one of them had been recorded.

**That exposed a misrepresentation, not a bug.** The published description said only *"needs
a web search and fetch tool."* The README said *"run it again tomorrow and it reads them all
first"* — a sentence that is simply false on such an agent. A user installing it there would
conclude the skill was broken, when in fact it had been advertised for a place it cannot
fully work.

Sizing it honestly: roughly half the skill survives with no files — Job 0, the fold, the
provenance rules, empty-stays-empty, the language test. The half that does not is the half
the headline rests on. The pending queue, the round log and the rejection file cannot exist, Gate 1 and Gate 2 have
no input, and **the completeness claim is therefore unavailable** — which is why Gate 0 is
stated as a precondition on evidence rather than as another heuristic about searching.

**Why the conversation is not an acceptable substitute.** The tempting fix is to let the
agent read its own history. History truncates silently and without notice: the agent's belief
that it has seen every firm is unchanged while the evidence for it quietly disappears, so it
re-adds firms it already rejected — confidently, and with no marker distinguishing those rows
from the rest. An admitted blank slate produces visible duplicates the user can filter. A
truncated history produces invisible ones. The worse failure is the one that looks fine.

**Why the fixed path, and not a probe.** The first attempt at this fix asked the agent to
classify its environment: write a probe file, read it back, and declare whether storage was
durable, session-only or absent. It cannot work. A write-then-read inside one session
succeeds identically whether or not anything survives the session, so the probe answers a
question it was never able to observe — and it fails toward the unsafe side, because an agent
in a wiped or redirected scratch area reads its probe back and announces that a later run will
find its files.

What *is* observable is whether a previous run's file comes back. So the design inverted:
**read a known path first, and let the answer be the evidence.** Files there — a continuation.
Files not there — a first run, whatever any earlier probe would have claimed.

This has a hard prerequisite. The agent host does not hand the agent a listing of its working directory; a
session sees the files it reads by name and nothing more. A file that is
not named in advance is invisible. That is why the layout is fixed and the market folder is
derived by a stated rule instead of chosen per run — the skill cannot find last week's work,
it can only look where it already knows to look.

**Why the ledger carries identity and nothing else.** An earlier draft put the round count and
the per-surface dry tallies in the ledger header, so a pasted ledger could reopen the
exhaustion gates. Two things killed it.

- **The header cannot answer the gate's question.** Gate 2 asks whether six *consecutive* dry
  rounds spanned three different surfaces. A per-surface total — `web=6 registry=2` — does not
  say which rounds were adjacent or which belonged to the streak. It looks like the input and
  is not.
- **The one number that mattered had no check on it.** Counting body lines proves the body is
  intact; it proves nothing about a header that could have been mistyped, stale or edited. A
  wrong firm line costs one duplicate row. A wrong dry count costs a false *"this market is
  finished"* — the exact failure of the Estonia run. Guarding the cheap error and licensing
  the expensive one is the wrong way round.

So Gate 0 became absolute, and the ledger became four columns. **It makes a run cheaper. It
never makes one finished.**

**Why the size claim was removed.** An earlier version of this file asserted that a market's
full output was ~40KB against a ledger of 1.7KB — roughly a twentieth — and used that ratio to
argue the fallback was practical. **The figure was never measured.** Generating a ledger from
one market's real output gave 12.5KB of ledger against 17.2KB of `investors.csv` plus
`sources.csv`: about 1.4x smaller, not 20x. Close to three quarters of those 12.5KB were the
pending queue — 139 parked names against 28 kept firms — which is why the ledger no longer
carries pending reasons and why that measurement describes a format this skill no longer
ships.

The number is not restated here with a better value, because the argument never needed one:
the deliverable carries twenty-two columns and its citations, the ledger carries identity, and
that difference is structural rather than a measured ratio. The episode is recorded because it
is the same error this skill exists to prevent — a confident figure inside a document someone
is about to act on — and it was caught by the package's own audit rather than by a reader.

### Why a named list is resolved before the search widens

Job 0 is the skill's headline, and on one market it did not run.

An association page produced **31 named organisations in a single round**. The association
describes its own membership as covering both fund managers and the legal and financial
advisers who serve them, without saying which is which — so the list is the population Job 0
exists to separate, handed over in one fetch.

The run then went looking for more names. It reached its budget with **16 of the 31
undecided** and **one** adviser rejection recorded, in a market where earlier runs measured
advisers at five-in-six and 52%.

Two things were true at once and only one was written down. The first — *a type is read from
evidence, never from a name* — is in the skill three times, and it is why several large
professional-services firms could not simply be rejected. The second — *deciding
what you already hold is cheaper per decision than finding the next name* — was in the skill
nowhere.

The asymmetry is what makes the rule: an unresolved name helps nobody, costs a queue entry,
and is one fetch from being settled, while the next search round may return nothing at all.
The seed rules still apply on top of it — a list never answers the dry test, and its members
face every gate — because *decide it first* is not *trust it*.

### Why the row is the manager and not the fund

Three of five firms verified on one market were fund managers, and one of them ran three
separately named funds, each named on its own site. Nothing in the skill said which was the
row, so an organisation could legitimately have produced three — in a file whose premise is
that one row is one organisation.

Choosing the manager follows from what the file is for. A reader takes this list to approach
a decision-maker; funds are the vehicles a decision-maker uses, and their count is an artefact
of fund structure and vintage rather than of how many investors exist in a market.

The hard case is a locally registered fund whose manager sits abroad. Registration and control
give different answers and neither is obviously right, so the rule picks control and requires
the run to say it picked control. A reader who wants the other answer can then see that a
choice was made — which is the same standard the rest of the skill applies to every value it
cannot fully settle.

### Why two headquarters gets recorded rather than parked

One fund described itself as based in two cities in two countries, with neither presented as
subordinate. `headquarters` holds one value.

Parking the row would be wrong: the firm is real, sourced and verifiable, and a queue entry
for a firm with two offices helps no one. Recording one silently is the failure this skill is
built against, one level up — not a guessed value, but a real value concealing that a
judgement was made. So the first-listed city goes in the cell and the second goes in the
report, where a reader can disagree with it.

### Trap 2 — why a garbled round is not dry

From the production code: *"dry means 'no new verifiable names', and letting a broken
transport drive the dry-well detector would finish the run claiming the names had run out."*

### Why a round had to be defined

> The Czech test ran one round that returned **41** firms off a single directory page, and
> another that returned **one**. The skill counted both as "1". **A streak counter built on
> a unit that varies 40× in yield is measuring nothing** — and dry rounds can be manufactured
> or avoided at will by choosing query shapes.

### Why the budget rule

Both later tests stopped on budget, never on exhaustion. The Czech run hit its ceiling with
43 names unverified. **Without a required reporting shape, a partial run reads exactly like a
finished one** — which destroys the only sentence this skill exists to be able to say.

Singapore added the second half: at round 11 with ~35 unverified names in hand, the skill
offered no guidance between spending the rest searching or verifying, and *"the two choices
produce very different deliverables."*

### Why the language rule has a precondition

The rule was stated as a law and was a finding about one country.

| market | local language | English | who won |
|---|---|---|---|
| Czech Republic | ~60 offered · 6 survived | 12 offered · 7 survived | **local, 5:1 on names** |
| UAE | 1 offered · 0 survived | 73 offered · 15 survived | **English, 73:1** |
| Singapore | 10 offered · 0 survived | 85 offered · 33 survived | **English** |

`rodinná kancelář` is largely a marketing phrase in Czech, so the local language found more
names **and more advisers** — 58% survival in English against 10% in Czech. In the Gulf and
Singapore the local language was a pure loss.

**The reporting requirement that saved this:** *"always split the offered count by
language."* That single line is what caught the rule being wrong. A rule that reports enough
to disprove itself is worth more than a rule that is right.

---

## Job 2 — the bar

### Why a dead citation is fatal

> An interactive search shows five results and a human reads every one, so a candidate with a
> shaky citation is a judgement a person makes. **A sweep to 200 is nobody reading 200.** By
> page 15 the model has exhausted the real names: what it produces after that is plausible
> firms that do not exist, carrying a number. `confidence: 0.4` is not a defence — it is how
> invented data enters a CRM wearing a decoration.

### Why 4 and 4b had to be split

> Of six rejections under the single rule, **three were firms that almost certainly exist** —
> killed by a robots.txt, a cache-only encyclopedia page, and a fetcher that refused a URL named
> inside another page. One of those, an unambiguously real investment group, then *also*
> failed the headquarters check, because the only page stating its city was the unfetchable
> one.
>
> The UAE run measured the recovery cost at **~2.4 tool calls per name**, and the split saved
> two real firms while correctly failing to save a third.

**And why the default is `sourceUnchecked` when the tools cannot tell 4 from 4b apart.** Many
agent fetch tools return one undifferentiated error for a 404, a robots.txt refusal and a
paywall alike. **In the environment those runs used, a direct liveness check on a
URL was impossible** — the distinction the rule turns on could not be observed at all. A rule
that cannot be executed has to fail towards keeping the row: this check decides about half of
all rejections, and **half of those were transport noise the one time it was measured.**
Failing the other way deletes real firms to protect against a page that was never dead.

### Why confidence scores were removed

> Measured on a production corpus: **only 147 of 2,958 claims — 5% — carry a confidence at all**, and those cluster
> at 0.99 / 0.98 / 0.90, and every one is "asserted". The number never distinguishes
> anything, because the model is always sure. Showing "conf 0.99" next to a value invites a
> reader to trust it more, **which is exactly backwards.**

### Why only some rejections enter the exclude list

From the production code, verbatim:

> *A name we rejected is still a name we were given. ONLY that corpus matches go in. A firm we
> already hold is one we never want offered again. A candidate dropped for a dead citation or
> an unestablished headquarters is NOT excluded — the model may yet cite it properly on a
> later page, and silencing it would be lowering the bar in the other direction.*

### Why the two counts are never merged

> *"20 already known or already returned" is two different failures welded into one count and
> they have opposite fixes. A match against what you hold is the system working; a repeat is the model being
> asked the same question twice.* … *Welded together they read as one healthy number and hid
> the second for a whole run.*

### Why the seed is capped

> *The overlap is front-loaded — a published list holds exactly the firms the model reaches
> for first — so the free half was spending the expensive half's dry allowance on its own
> best pages.*
>
> *One seed name rescues one page, once.* And the three-round cap on top: the Czech test got
> **41 names from a single fetch**, which under the uncapped rule could rescue 41 rounds and
> hold off a six-dry-round stop for most of the run — the exact failure the rule was written
> to prevent. The rule was calibrated for a seed of ~10 and silently inverted at scale.

---

## Job 3 — the fold

**This is the part of the skill specified as an algorithm rather than as a judgement, and it
is the part that failed hardest each time it met a new market.** A judgement bends; an
unparameterised algorithm does not.

### Why transliteration, not dropping

> Nine people were duplicated inside their own firm in a production corpus. *(The personal
name below is invented.)* One code path folded
> with `[^a-z0-9]+ → ' '`, which turns `André Mustermann` into `andr mustermann` — the accented letter
> dropped, not transliterated. The stored value kept the accent. **Every accented name in
> that corpus was unmatchable.**

*(Personal names throughout this file are invented; no individual from any corpus is named.
Organisation names in examples are either invented or replaced with a placeholder — where a
run's finding required naming what a firm said about itself, the sentence is paraphrased.)*

### Why legal forms are stripped from BOTH ends

> Estonian and Baltic registries write the form in front: `AS Vesta`, while the firm's own
> site writes `Vesta` — and the same register writes `Vesta Capital AS`. **Five real pairs
> failed on this in one small market.**

It is worth naming what this exposed about the split: the tester extended `lists.md` with
Baltic forms before round 1 — *the first time in four tests that instruction was acted on* —
felt the market was localised, and the fold still failed. **The defect was the anchor, not
the entries.** A list you can extend produces a false sense of completion when the bug is in
the step that reads it.

### Why rebrands need their own rule

A renamed firm shares no characters with its old name. No normalisation, no typo rule and no
distinctiveness test can reach it, and **three turned up in one small market.** Only the
domain (a rebrand keeps or redirects the old one) and the sentence (*"formerly"*,
*"previously known as"*) find them — and the old name must go into the exclude list, or it
returns every round as a name never seen before.

### Why legal forms are stripped BEFORE punctuation collapse

> Collapsing punctuation first turns Czech `a.s.` into `a s` and `s.r.o.` into `s r o`, so a
> list holding `as` and `sro` can never match. **All four real duplicate pairs in the Czech
> test failed on this.** It is not a Czech problem — it breaks dotted `S.p.A.`, `S.à r.l.`
> and `B.V.`, forms that were already on the list. The worked example that hid it (`X GmbH &
> Co. KG`) happens to be undotted.

### Why the list is not European

> UAE: **nine of ten local forms failed to fold.** Only the two containing the English `LLC`
> survived. `FZE`, `FZCO` and `FZ-LLC` are the free-zone forms the entire local
> investment-vehicle industry is built on; `PJSC` is the standard form for every listed
> company.
>
> Singapore: spelled-out `Private Limited` — the commonest written form there — was missing,
> splitting `X Capital Private Limited` from `X Capital`. So was `VCC`, Singapore's own fund
> vehicle.

### Why a place name is never distinctive

The first definition of "distinctive" was *"at least one token of 4+ characters not on any
list."* It is a string-length test, and a city name passes it.

> **UAE:** it merged a `<City> Capital Group` — a private investment group — with a
> `<City> Investment Office`, that emirate's government FDI agency. Unrelated
> organisations, one row. A `<City> Group` and a `<City> Holding` collided the same way.
>
> *(Two of the four colliding pairs found on that run may in fact be parent and subsidiary
> rather than unrelated firms — which is the `part_of` case, not the silent-merge case. The
> government-agency pair is not, and one unrelated pair is enough to make the point. The
> ambiguity is itself the argument: if a reader cannot tell from the names, neither can an
> algorithm, and it must not merge.)*
>
> `<City> + <generic financial noun>` is the **modal** naming convention across the Gulf —
> a city name carrying Holding, Group, Investment Authority, Asset Management or Investment
> Corporation, with several such entities per city. Common in Asia and Latin America too.

**The Czech defect was duplicate rows: visible, annoying, a reader fixes them. This is the
opposite and far worse — one row for two companies, both sets of sources pooled, looking
exactly like a correct merge. Nothing in the file marks it.**

### Why "folding proposes, it never merges"

The narrow fix — exclude place names — treats the symptom. The structural fix is that **two
names folding to the same key is a question, not an answer.**

> **Singapore, the vindication:** the key `<heritage-name>` collided **five ways** across four
> different domains — a multi-family office, two unrelated companies of the same name, an
> advisory vehicle, and a licensed fund manager. That is the UAE failure at five times the
> scale. v5 flagged all five and merged none.
>
> `<group-name>` collided Singapore against Malaysia the same way.

**7 flags on 33 rows — 21% — and every one a genuine question.** That rate is the rule
working.

The skill's own standard is *"every silent pick is a wrong row nobody can find later."* An
algorithm that merges without corroboration breaks that standard on the skill's own behalf.

### Why "when in doubt, it is a place"

> One token was simultaneously a surname, a city district — literally one firm's registered
> address — and a hotel brand. A tester who rules it a surname folds four unrelated
> companies; one who rules it a place does not. **Singapore is full of heritage brand names
> that are also place names.**

Refusing to fold costs a flag. Folding costs the truth. The asymmetry decides it.

### Why transliterated vowels are typos and Latin-script ones are not

> One firm appears as **Al Nasiri**, **Al Nassiri** and **Al Nassery** — the
> first two as separate profiles on one aggregator, the third on its own domain. v4 merged
> the first two (one inserted character) and split off the third, because `i`→`e` is a
> substitution.

For European names the rule is right — `Bauer` and `Baier` really are different families.
For Arabic-to-Latin transliteration it is wrong: **vowel substitution is the primary axis of
variation.**

### Why a leading article is stripped

A firm written `Al Muster Group` on one page and `Muster Group` on another is one firm, and
the two fold to different keys. The Arabic
definite article is transliterated inconsistently across sources, and it is a dropped
*token*, not a dropped *character*, so the typo rule could not reach it either.

### Why the domain rule has a parent exception

> One domain carried both a group and a *"The Private Office of …"* entity, with the first
> explicitly described as *"a conglomerate of"* the second. One domain, two entities, a
> parent and a child. The bare domain rule said merge them.
>
> Singapore found the same shape and noted the deeper problem: the exception was **60 lines
> away from the decision table**, so a reader following the table literally merges them. *"I
> nearly did."* That is why the exception now sits inside the table.

### Why people are stricter

There is no domain to settle a person. From the production code:

> *A single-token name never matches. A given name is not any particular person: a first name
> is a hint to ask about, never an identity to write against.*
>
> *ACCEPTED: adjacent transposition · one letter inserted or dropped. REJECTED: one letter
> SUBSTITUTED — Jan/Jon, Marc/Mark, Eric/Erik are different people, not typos.*

---

## Job 4 — classification

### Why a closed vocabulary

> A production corpus carried **eleven distinct spellings** of one column, because nothing had ever
> checked it. The pipeline header read *"46 venture capital · 14 angel · 1 VC · 1 Angel
> Investor · 1 venture capital fund"* — the same two types under five names.
>
> **Reading around a mess is not the same as stopping it growing.**

### Why the set has been widened twice

Each time by a test, each time for the same reason: **a file that says "we don't know what
this is" about its most important entries is worse than one more value.**

- **`investment_group`** — in one market, two of the largest family capital pools both
  describe themselves as *"an international investment group"*, both are one family's money,
  and neither is a family office by the evidence rules nor a VC. Both shipped `unknown`.
- **`private_equity`** — a Gulf firm describing itself as an independent private equity firm
  established in a financial free zone, naming four portfolio companies
  and a Fund I, shipped as `unknown` because neither `private` nor `equity` was an owned
  word. Singapore then produced **seven** such rows.

### Why the `unknown` rate is never a quality signal

Across the market runs the share of rows typed `unknown` ran **from a few in one run to
roughly a third of them in another.** Nothing about the runs explains the
spread: it tracks how much the firms in that market say about themselves on their own pages,
which is a property of the market and not of the search. So there is no expected proportion
to compare a run against, and a low rate is not evidence of a better run — it is as likely to
be evidence of a market whose firms describe themselves, or of a tester who guessed. What
does not vary across markets: forcing a label onto an unknown is the same mistake as
inventing an email.

### Why every word must be owned

> `crypto fund` contains the word `fund`, so a loose read stored it as `venture_capital`,
> silently, on one surface — while another surface threw an error for the same word. One
> word, two outcomes, decided only by where it was typed.
>
> *An allowlist and not a denylist, deliberately: a denylist of qualifiers is unbounded and
> the next unlisted one gets stored as something else in silence, which is the whole bug.*

### Why the allowlist cannot decide identity

> Without Job 0 running first, a consultancy called `… FAMILY OFFICE` types cleanly as
> `family_office`, because `family` and `office` are owned words. **That happened in testing,
> five times in one country.**

### Why the name rule is narrow, and why it does not travel

> *`Capital`, `Invest`, `Holding`, `Beteiligungsgesellschaft`, `Gruppe`, `AG` and `GmbH`
> resolve to NOTHING here. A name carrying only those stays `unknown`, which is a real value
> of this column and the honest answer.*
>
> Measured on a production corpus: of 106 candidates typed `unknown`,
> it resolves **27** — 20 family offices and 7 venture arms — and leaves 79 alone. **A
> quarter, not a majority, and the rule set is not widened to make it look better than it
> is.**

The UAE test then showed the rate does not transfer: the rule typed one individual's holding
vehicle as `venture_capital` off the word *Ventures* — a wrong row the skill instructed the
tester to write.

### Why "do not silently repair"

> A page staged a firm named *… Family Office* as `venture_capital` (`kind: inference`,
> confidence 0.72) while the fact's own excerpt said it had managed a single European
> family's assets since the 1990s, and the criteria asked for family offices. **Twelve more
> went the same way.** The value was never wrong on its own terms — **it was never compared**,
> so a flat contradiction was staged looking exactly like a finding.

### Why it compares against the request and nothing else

Replaying 137 staged candidates against the request's own criteria:

```
the criteria             10 flagged, and all ten are the defect     0 false
the model's REASONS       2 false positives,  0 unique catches
the fact's EXCERPT        2 false positives,  2 unique catches
```

The two prose sources fail on the same two shapes, and neither is fixable with a phrase
table:

```
NEGATION   "… ist kein klassischer VC-Investor" — the firm saying what it is NOT.
           A scanner that sees "VC" reads the opposite of the sentence.
A PART     "the dedicated unit for … venture capital fund engagements" — a venture arm
           INSIDE a family office. That describes what a firm DOES; the type is what it IS.
```

Both blank a type that was right, which is the expensive error. **The criteria is what a
human asked for, and it cannot be negated or nested.**

### Why it may only blank an inferred type

> The earlier rule blanked the type of every correctly-classified off-type firm. A VC and an
> angel group — both identified from their own pages, both unambiguous — shipped with an
> empty `type`, while two firms nobody could classify kept `unknown`, because `unknown` is
> never contradicted. **The file rewarded ignorance.**
>
> Job 1 says collect broad and filter after; the old rule then punished you for typing what
> you collected.

### Why this rule is mostly asleep

It can only fire on a narrow single-type request — and Job 1 says never to issue one.
Singapore and the UAE could not exercise it without deliberately violating Job 1. It is kept
for the case Job 1 cannot prevent: a user who asks narrowly anyway.

---

## Output

### Why `sources.csv` is a separate file

Every in-cell format was tried and broke.

| format | how it failed |
|---|---|
| `field=url` pairs, `;`-separated | `;` is ordinary inside URLs (`?a=1;b=2`, `jsessionid` path parameters). **Silent** — a shredded URL and a garbage pair, never an error |
| `field\|rung\|url`, newline-separated in a quoted cell | parsed correctly under real parsers — but the file became **174 physical lines for 34 records**, so every line-based tool reported 173 firms. And `\|` does appear in real URLs |

A separate file also gives the **rung** a real column. Job 2 makes the rung central and the
packed formats had nowhere to put it, so rung information ended up in free text — while two
rows in one test rested on rung-4 aggregators alone, which Job 2 calls *"never alone for
existence."* That is now one filter away.

### Why `key_quote` must evidence the row

> A test produced a perfectly valid quote — a short sentence, from the cited page, in the
> original language — that **defined what a family investment company is in general and never
> mentioned the firm.** A reader scanning the CSV sees a native-language quotation and reads
> it as proof. The rule had specified the quote's *provenance* and never its *relevance*.

### Why `person` says "the most senior you saw"

The earlier wording was *"the most senior named individual"*, which **asserts something a
searcher can almost never verify.** One row in the Estonia run carried an Investment
Associate, because that was the most senior name on the page. `people_known` is what tells
the reader.

### Why `investors-rejected.csv` is local-only

By construction it is a list of named real companies with a negative claim attached — *"this
firm is not what it says it is."* Right for deciding what to search next, wrong to publish.

**And the conflict is real: anonymising it destroys it.** The file exists so that *"a reader
who disagrees with a Job 0 call can see it was made"*, and so those names are never searched
again — **and you cannot suppress a name you did not record.**

### Why three extra files at all

> Without them, a second run starts its rejection tally from zero and re-rejects everything
> from scratch — **which is Trap 1, the bucket with a hole, reintroduced by the output spec.**

---

## Why this file exists at all

The Singapore test's most useful finding was not a rule. It was this:

> *~40–45% of the skill is rule **provenance**, not rules. Every defect I found is a rule
> that exists but is unreachable at the moment of decision.* … *The operative rules are
> interleaved with their justifications, and at 45KB the justifications win.*
>
> *Czech found 13 defects, UAE found the silent-merge class, Singapore found 14 — and most
> are placement and list-completeness failures, not reasoning failures. That's a formatting
> plateau.*

So the skill was split: rules in `SKILL.md`, lists in `lists.md`, evidence here. The
provenance is not deleted, because a rule whose failure you can picture is a rule you will
actually follow. It is moved out of the path you read while working.
