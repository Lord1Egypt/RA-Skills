# General Forecasting — Tetlock Superforecasting

Core probabilistic forecasting methodology from Philip Tetlock & Dan Gardner,
*Superforecasting* (2015), validated by the **Good Judgment Project (GJP)** —
IARPA-sponsored tournaments with thousands of volunteer forecasters.

## The Commandments (1–8)

From Tetlock & Gardner, *Superforecasting* appendix. Commandments 9–10 (teamwork,
deliberate practice) are omitted here; the skill workflow covers evidence-gathering
and structured output separately.

(Implicit 11th: don't treat these as rigid rules — stay flexible.)

### 1. Triage

Focus effort on the **Goldilocks zone** — not "clocklike" questions (simple
rules of thumb suffice) and not "cloudlike" ones (even fancy models can't beat
a dart-throwing chimp).

- **Too cloudy**: "Who wins the presidency twelve years out?" In 1940 you could
  not have named Dwight Eisenhower for 1952 — believing you could is classic
  hindsight bias.
- **Closer but still hard**: In March 2015, the 2016 U.S. field was uncertain but
  far more tractable than a race twelve years ahead.
- **Often cloudy in practice**: oil prices, currency markets — you may only
  discover unpredictability after wasted effort.

Two triage errors to weigh: failing to predict the predictable vs. wasting time
on the unpredictable. Which is worse in your situation?

### 2. Decompose (Fermi-ization)

Break intractable questions into knowable and unknowable parts. Expose
assumptions. Make best guesses — better to discover errors quickly than hide
them behind vague language.

**Canonical Fermi**: "How many piano tuners in Chicago?" → pianos × tunings
per year ÷ hours per tuner.

**Book case — Arafat polonium** (IARPA tournament): "Will French or Swiss
inquiries find elevated polonium in Arafat's remains?" Most people substitute
"Did Israel poison Arafat?" and dive into geopolitics. Superforecaster Bill
Flack instead asked:

- Can polonium still be detected after years in the ground?
- What pathways yield "yes"? (Israel poisoned him / enemies poisoned him /
  remains contaminated post-mortem to frame Israel)
- Two labs — either positive counts.

He opened near **60%**, then updated to **65%** when the Swiss team's delay
suggested confirmatory testing (polonium found; ruling out lead decay as source).
Final Brier score on that question: **0.36** (strong on a hard item).

**Trap**: substituting an easy question for a hard one (e.g. "Would Israel
assassinate Arafat?" instead of "Will a polonium test turn positive?").

GJP forecasters Fermi-ized bird-flu epidemics, oil prices, Boko Haram, Aleppo,
bond spreads, and similar "impossible to quantify" questions.

### 3. Balance outside and inside views

Nothing is 100% unique — search for a **comparison class** and ask: *How often
do things of this sort happen in situations of this sort?* Anchor on the
outside view (base rate), then adjust with case specifics.

Kahneman (*Thinking, Fast and Slow*, citing distributional / reference-class
reasoning) calls the outside view the single most important advice for
forecasting accuracy. See `kahneman-tversky-outside-view.md`.

- **Kahneman's textbook**: Israeli team estimated 2–3 years from the inside;
  similar projects averaged **7 years**, many never finished. Actual: **8 years**,
  never used.
- **Larry Summers**: doubles employee time estimates and bumps the time unit
  (1 hour → 2 days; 2 days → 4 weeks) to correct for the planning fallacy —
  then adjusts if someone delivers on time.
- **Seemingly unique events**: hunts for Joseph Kony; Greece's Syriza government
  vs. creditors (2015) — still have reference classes.
- **Arafat outside view**: famous dead person, prima facie case for exhumation —
  poisoning found in such investigations is well above 0% but below 100% (or
  evidence would have surfaced before burial). Rough range 20–80%; midpoint
  **50%** as starting point before inside-view paths.

### 4. Update beliefs — neither under- nor over-react

Belief updating is boring but compounds. Usually **small, frequent steps**
(0.40 → 0.35, 0.60 → 0.65); occasionally **large jumps** when evidence is strongly
diagnostic. Superforecasters are imperfect Bayesians but far better than most.

Research: Atanasov, Witkowski, Ungar, Mellers & Tetlock (2020), *Organizational
Behavior and Human Decision Processes* — "Small steps to accuracy: incremental
belief updaters are better forecasters." **Caveat**: small updates correlate with
skill; forcing small updates alone does not reliably improve accuracy.

- **Flack on Arafat**: see §2 — 60% → 65% on Swiss delay.
- **Ambiguous clues**: a critical North Korea article in Chinese state media —
  signal of pressure on Pyongyang, or editorial error? Fine line between early
  detection and being suckered.
- **Illustrative — China recession scare**: fear of global contagion may drop once
  you check base rates — under one IMF-style global-recession definition, four
  episodes since the 1970s; Japan's 1990s slump did not trigger a global recession
  despite its economic weight. (Definitions of "global recession" vary.)

### 5. Clashing causal forces (dragonfly eye)

For every argument, find a counterargument worth taking seriously. List in
advance what evidence would nudge you toward the other side. Synthesize many
perspectives — like a dragonfly's compound eye — into one probability.

- **Saudi OPEC cuts, Nov 2014**: (1) Saudi reserves buffer low oil prices;
  (2) Saudis need high prices for social spending; (3) shale + demand may be
  beyond their control — cuts futile. Net: **~80% no** (Saudis did not cut;
  shocked many experts).
- **Dove vs. hawk on Iran**: each camp should pre-commit to signs that would
  shift them. Good synthesis turns a template dove or hawk into a **dove-hawk**
  with nuanced views on when hard vs. soft policy works.
- **"Crowd within"**: assume your first judgment is wrong, argue why, re-estimate
  — nearly as good as a second forecaster.

### 6. Granular probabilities

Few things are certain or impossible; "maybe" is not informative. Use as many
degrees of doubt as the problem permits. In poker, edge comes from separating
60/40 from 55/45.

- **Obama / bin Laden, Abbottabad**: intelligence gave probability estimates;
  Obama called it "fifty-fifty." Tetlock: if basketball buddies gave the same
  numbers for a college game, he'd hear "between 3:1 and 4:1" — granular norms
  exist in sports but not always in national security.
- **George Tenet, "slam dunk" on Iraqi WMD**: treated like certainty; stricter
  numeric standards would have blocked the phrase.
- **Steve Ballmer on iPhone (2007)**: "no significant market share" — undefined
  threshold and time horizon; impossible to score fairly.
- **Brian Labatte**: asked fiction vs. nonfiction split — "70%… no, **65/35**."
  Mellers (GJP): finer granularity correlates with accuracy; rounding
  superforecasters' estimates hurts performance.

Most people default to three mental settings: gonna happen / not / maybe.
Superforecasters fight over single percentage points.

### 7. Balance prudence and decisiveness

Long-run accuracy needs good **calibration** (of things you call 70%, do ~70%
actually happen?) and **resolution** (daring to leave the base rate and make
informative calls). Avoid both the waffler (stuck on "maybe") and the blowhard
(overconfident, unwilling to qualify). Tamp down both misses and false alarms
where the world allows.

- **Archie Cochrane (1956)**: evidence-based-medicine pioneer told by a
  specialist his axilla was full of cancer and he had little time left — he
  accepted and planned accordingly. Pathology found **no cancer**. Intelligence
  and stature are no shield against overconfidence.

### 8. Post-mortem — learn from mistakes and successes

Own failures; ask where reasoning broke. Beware hindsight ("I knew it all along").
Also post-mortem **wins** — success may be luck or offsetting errors.

- **Devyn Duffy's team on Arafat**: assumed polonium's half-life made detection
  "virtually impossible" without questioning whether decay products could still
  signal polonium. Lesson: challenge expertise assumptions; re-examine premises.
- **Guinea elections**: team was right but protests nearly blocked the vote —
  "we lucked out too."
- **Bay of Pigs (1961)**: Joint Chiefs said "fair chance" of success; planners
  later indicated they meant roughly **3:1 against**. Kennedy heard something
  far more optimistic — vague language in high-stakes decisions.
- **Norway attacks (2011)**: many assumed Islamist terror (post-9/11 pattern);
  perpetrator was right-wing Breivik — **WYSIATI** (what you see is all there is).

Score past predictions; label known facts vs. inferred judgments vs. unknowns.

## Superforecaster habits

Pragmatic · decompose analytically · dragonfly eye (synthesize many views) ·
think in probabilities not yes/no · update diligently in small steps · act as
intuitive psychologists who watch for their own biases. Underneath: growth
mindset + grit.

## How to apply in this skill

- Adopt the fox stance; surface multiple competing hypotheses.
- **Fermi-decompose** the query into sub-questions before forecasting.
- Use the **dragonfly eye**: generate 2–4 independent angles, then aggregate.
- Assign **granular probabilities** (e.g. "~55–65%"), not just high/med/low.
- Treat any new evidence gathered via tools as a **small Bayesian update** to a
  stated prior, and show the prior → posterior shift.
