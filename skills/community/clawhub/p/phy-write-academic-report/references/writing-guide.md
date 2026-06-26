# Writing Guide: Thesis-Length Academic Documents

This guide codifies the writing principles for producing publication-quality thesis-length
reports (40-100+ pages). It inherits the core philosophy from the
[ml-paper-writing](https://github.com/Orchestra-Research/ml-paper-writing) skill and
extends every principle to the scale and structure demanded by FYP reports, MSc/PhD
dissertations, and technical reports.

**Foundational sources**: Neel Nanda, Andrej Karpathy, Gopen & Swan, Michael Lipton,
Jacob Steinhardt, Ethan Perez, Simon Peyton Jones, Gregory Farquhar.

---

## Table of Contents

1. [The Narrative Principle](#1-the-narrative-principle)
2. [Time Allocation for Thesis Writing](#2-time-allocation-for-thesis-writing)
3. [Abstract Writing](#3-abstract-writing)
4. [Introduction Structure](#4-introduction-structure-for-thesis)
5. [Literature Review Chapter](#5-literature-review-chapter)
6. [Gopen & Swan's 7 Principles of Reader Expectations](#6-gopen--swans-7-principles-of-reader-expectations)
7. [Micro-Level Tips (Ethan Perez)](#7-micro-level-tips-ethan-perez)
8. [Word Choice (Lipton, Steinhardt)](#8-word-choice-lipton-steinhardt)
9. [Mathematical Writing](#9-mathematical-writing)
10. [Figure Design](#10-figure-design)
11. [Common Mistakes](#11-common-mistakes-thesis-specific)
12. [Pre-Submission Checklist](#12-pre-submission-checklist-for-thesis)

---

## 1. The Narrative Principle

### Origin

Neel Nanda's advice for ML papers: *"Your paper should tell exactly one story. Every
paragraph either advances the story or should be cut."* Andrej Karpathy echoes this:
*"Start with the key insight. Build from there."*

### Adaptation for Thesis

A conference paper tells one story in 8 pages. A thesis tells **the same one story** in
60-100 pages. The difference is not that you tell more stories; the difference is that
you tell the same story with more evidence, more context, and more rigour.

| Document | Story Length | Story Structure |
|----------|-------------|-----------------|
| Conference paper (8 pp) | 1 insight, tight arc | Problem -> Method -> Result |
| Thesis (60-100 pp) | 1 insight, extended arc | Background -> Gap -> Design -> Build -> Evaluate -> Reflect |

### The Spine Test

Write the **spine** of your thesis in six sentences, one per chapter:

```
Ch1: Autonomous GUI agents waste time and money re-exploring websites.
Ch2: Existing approaches lack pre-computed state maps, falling back to reactive exploration.
Ch3: We build a crawler that produces UI Transition Graphs offline.
Ch4: We evaluate on 90 tasks from Mind2Web using browser-use + Gemini Flash.
Ch5: Structured UTG retrieval doubles success rate from 25.6% to 50.0%.
Ch6: Pre-computed navigation maps are a viable alternative to reactive exploration.
```

Every section you write must serve exactly one of these six sentences. If a section does
not clearly belong to any of them, it is either in the wrong chapter or should be cut.

### Applying the Spine Across Chapters

| Chapter | What the Spine Sentence Means for Writing |
|---------|-------------------------------------------|
| Introduction | Motivate the ONE problem. Do not survey the field yet. |
| Literature Review | Show WHY existing work does not solve this problem. Every paper you cite should connect to the gap. |
| System Design | Describe WHAT you built and WHY you made each design choice. |
| Experimental Setup | Explain HOW you will test whether your contribution solves the problem. |
| Results | Present EVIDENCE that it works (or where it falls short). |
| Conclusion | Restate the contribution in light of the evidence. |

### Common Violations

| Violation | Symptom | Fix |
|-----------|---------|-----|
| Tangential background | 3 pages on neural networks when the project is about web crawling | Cut to 1 paragraph or move to appendix |
| Second storyline | Chapter 3 describes two systems, only one is evaluated | Keep the evaluated system; move the other to future work |
| Results without connection | Presenting numbers without linking back to the research question | Every result paragraph must start by stating what claim it supports |
| Literature review as book report | Summarizing papers without relating them to your gap | Restructure around themes, not papers |

---

## 2. Time Allocation for Thesis Writing

### Conference Paper vs. Thesis Time Budget

A conference paper is roughly even across sections. A thesis is front-loaded on results
and literature, back-loaded on revision.

| Activity | Conference Paper (% of total) | Thesis (% of total) |
|----------|:----:|:----:|
| Planning & outline | 10% | 8% |
| Literature review | 10% | 18% |
| Methods / system design | 20% | 12% |
| Results & analysis | 20% | 22% |
| Figures & tables | 15% | 15% |
| Introduction & abstract | 10% | 5% |
| Revision & polish | 15% | 15% |
| Cross-referencing & compilation | 0% | 5% |

### Why the Differences?

1. **Literature review expands**: You must demonstrate mastery of a field, not just
   position your paper. Budget 18% of writing time.
2. **Results chapter is the core**: Examiners spend the most time here. It deserves the
   most polish. Budget 22%.
3. **Cross-referencing is non-trivial**: With 6+ chapters written by parallel agents (or
   at different times), labels, notation, and terminology drift. Budget explicit time for
   unification.
4. **Introduction shrinks (proportionally)**: The introduction still matters, but at
   3-5 pages out of 80, it takes less relative effort than a 1.5-page intro in an 8-page
   paper.

### Recommended Writing Order

Do **not** write chapters in order. Follow this sequence:

```
1. Results (Ch5)         -- Write what you found. This is the heart.
2. Methods (Ch3)         -- Write what you built. Reference the results.
3. Experimental Setup (Ch4)  -- Write how you tested. Bridge Ch3 and Ch5.
4. Literature Review (Ch2)   -- Write what others did. Now you know what to emphasize.
5. Introduction (Ch1)        -- Write the motivation. Now you know the full story.
6. Conclusion (Ch6)          -- Write the reflection. Easiest when everything else exists.
7. Abstract                  -- Write the summary. Last, always last.
```

This order works because each chapter is easier to write when you already know what comes
after it.

---

## 3. Abstract Writing

### Conference Abstract (150-250 words)

Farquhar's 5-sentence formula:

| Sentence | Function | Example |
|----------|----------|---------|
| 1 | Context: What is the problem area? | "Autonomous GUI agents explore web applications reactively, incurring high latency and API costs." |
| 2 | Gap: What is missing? | "No existing system provides pre-computed navigation maps for arbitrary websites." |
| 3 | Approach: What do you do? | "We introduce UTG-Crawl, a tool that generates UI Transition Graphs offline." |
| 4 | Result: What did you find? | "On 90 Mind2Web tasks, structured UTG retrieval doubles agent success rate from 25.6% to 50.0% (p < 0.001)." |
| 5 | Implication: Why does it matter? | "Pre-computed state maps offer a scalable alternative to per-task reactive exploration." |

### Thesis Abstract (250-400 words)

Keep the 5-sentence skeleton, but **expand each sentence into a 2-4 sentence paragraph**:

| Paragraph | Function | Word Budget |
|-----------|----------|:-----------:|
| 1 | Context + problem significance | 50-80 |
| 2 | Gap + what specifically is missing | 40-60 |
| 3 | Approach + key design decisions | 60-100 |
| 4 | Results + headline numbers | 60-100 |
| 5 | Implications + limitations + future | 40-60 |

### Thesis Abstract Template

```
[Context paragraph]: {Domain} is important because {reason}. Current approaches
{describe state of the art}. However, {problem with current approaches}.

[Gap paragraph]: Specifically, {what is missing}. This means {consequence of the gap}.

[Approach paragraph]: This report presents {system name}, a {brief description}.
The system works by {high-level mechanism}. Key design decisions include
{decision 1} and {decision 2}.

[Results paragraph]: We evaluate on {benchmark} with {N tasks / subjects / etc.}.
{System name} achieves {metric = value}, compared to {baseline = value}
({statistical significance}). We find that {secondary finding}.

[Implications paragraph]: These results demonstrate that {takeaway}. Limitations
include {honest limitation}. Future work could extend this to {direction}.
```

### Rules for Both Lengths

- **No citations** in the abstract. It must stand alone.
- **No undefined acronyms**. Spell out on first use even if defined in the body.
- **Include one number**. A quantitative result makes the abstract concrete.
- **No "In this paper/report, we..."** as the opening. Start with the problem.

### Good vs. Bad Abstract Opening

| Quality | Example |
|---------|---------|
| Bad | "In this report, we present a system for crawling web applications." |
| Bad | "Artificial intelligence has made tremendous progress in recent years." |
| Good | "Autonomous GUI agents spend 60-80% of their interaction budget on exploration rather than task execution." |
| Good | "Web applications change state through user actions, but no existing tool systematically maps these state transitions." |

---

## 4. Introduction Structure for Thesis

### Length: 3-5 pages (not 1-1.5 like conference)

The thesis introduction serves a fundamentally different purpose than a conference intro.
A conference intro sells the paper to reviewers who are experts. A thesis intro
establishes the context for examiners who may not be specialists in your exact topic.

### Section-by-Section Structure

#### 4.1 Background (1-2 pages)

**Purpose**: Establish the problem domain in concrete terms.

**Start specific, not generic.** The first sentence of your thesis determines whether the
examiner leans forward or leans back.

| Quality | First Sentence |
|---------|----------------|
| Bad (generic) | "The field of artificial intelligence has seen rapid advancement in recent years." |
| Bad (too broad) | "Web applications are widely used in modern society." |
| Good (specific, concrete) | "A GUI agent that can navigate a flight-booking website must discover which buttons lead to which pages before it can plan a booking sequence." |
| Good (problem-first) | "When an autonomous agent encounters a new website, it has no map. Every click is a gamble." |

**Structure the background as a funnel**:
```
Broad context (1-2 sentences)
  -> Specific problem area (2-3 sentences)
    -> The exact challenge this project addresses (2-3 sentences)
```

#### 4.2 Motivation (0.5-1 page)

**Purpose**: Why this problem matters **now**. Why should anyone care?

Include at least one of:
- A quantitative cost/waste argument ("Reactive agents make 15-30 API calls per task")
- A qualitative impossibility argument ("Without a map, agents cannot plan multi-step paths")
- A practical urgency argument ("As LLM API costs decrease, exploration overhead becomes the bottleneck")

Avoid:
- Vague claims about "growing importance"
- Appeals to market size (this is not a pitch deck)
- "To the best of our knowledge" (either you know or you do not)

#### 4.3 Objectives and Scope (0.5 page)

**Purpose**: Transform the motivation into a numbered list of testable objectives.

```latex
The objectives of this project are:
\begin{enumerate}
    \item Design and implement a web crawler that produces UI Transition Graphs
          from arbitrary web applications.
    \item Evaluate whether UTG-augmented agents outperform baseline agents on
          standardised web navigation tasks.
    \item Analyse the trade-off between UTG information density and agent
          performance through controlled ablation.
\end{enumerate}
```

**Explicitly state scope boundaries**:

```latex
\textbf{In scope}: Single-domain web applications with standard HTML elements.
\textbf{Out of scope}: Native mobile applications, CAPTCHAs, multi-factor
authentication flows.
```

This protects you during the viva/defence. When an examiner asks "But what about X?",
you can point to the scope statement.

#### 4.4 Project Schedule (0.5 page)

Include a Gantt chart or timeline figure. This demonstrates project management maturity.

The schedule should show:
- Planning and literature review phase
- System design and implementation phase
- Evaluation phase
- Writing phase
- Key milestones and deliverables

#### 4.5 Report Organization (0.5 page)

A brief roadmap of remaining chapters. One sentence per chapter is sufficient:

```latex
The remainder of this report is organized as follows.
Chapter~\ref{ch:literature} reviews related work in web crawling, GUI agents,
and state abstraction.
Chapter~\ref{ch:system} describes the design and implementation of the UTG crawler.
...
```

**Keep this mechanical.** Do not try to make it exciting. Its purpose is navigation, not
persuasion.

---

## 5. Literature Review Chapter

### Organize Methodologically, Not Paper-by-Paper

The most common mistake in thesis literature reviews is **the annotated bibliography
anti-pattern**: summarizing papers one by one in chronological order. This produces
boring, unstructured prose that demonstrates reading but not understanding.

| Approach | Structure | Reader Experience |
|----------|-----------|-------------------|
| Bad: Paper-by-paper | "Smith (2020) did X. Jones (2021) did Y. Lee (2022) did Z." | Tedious. No synthesis. |
| Good: Methodological | "One line of work uses graph-based state representations [Smith, Jones]. Another uses vision-only approaches [Lee, Park]. We combine insights from both." | Clear landscape. Reveals gap. |

### Template for a Literature Review Section

Each section should follow this structure:

```
1. Topic sentence: What problem/approach does this section cover?
2. Group A: "One line of work [refs] approaches this by..."
3. Group B: "In contrast, [refs] use a different strategy..."
4. Comparison: "Group A excels at X but struggles with Y, while Group B..."
5. Bridge to your work: "Our approach draws on {specific element} from Group A
   while addressing the limitation of {specific weakness} in Group B."
```

### Example: Good vs. Bad Literature Review Paragraph

**Bad (paper-by-paper)**:
> Zhang et al. (2023) proposed WebAgent, which uses HTML summarization to generate
> programs. Gur et al. (2024) introduced WebLinx, a benchmark for conversational web
> navigation. Deng et al. (2024) built Mind2Web, a dataset of 2,350 web tasks.
> Zhou et al. (2024) proposed WebArena, a realistic web environment.

**Good (methodological grouping)**:
> Evaluation of web agents has evolved from synthetic environments to realistic
> benchmarks. Early benchmarks like MiniWoB++ (Shi et al., 2017) used simplified
> web pages, limiting transfer to real websites. Recent work addresses this through
> two strategies: curating tasks on live websites (Mind2Web; Deng et al., 2024)
> or building self-hosted replicas (WebArena; Zhou et al., 2024). We evaluate on
> Mind2Web because its tasks target real, publicly accessible websites where our
> crawler can operate without infrastructure setup.

### Positioning Table/Figure

Consider including a positioning table that explicitly maps your work against the
literature:

```
| System        | Pre-computed Map | DOM-based State | Graph Structure | Eval Scale |
|---------------|:---:|:---:|:---:|:---:|
| WebAgent      |     |  Y  |     | 812 |
| SeeAct        |     |     |     | 1300 |
| Mind2Web      |     |  Y  |     | 2350 |
| Ours (UTG)    |  Y  |  Y  |  Y  |  90  |
```

This makes your contribution immediately visible.

### Research Gap Statement

End the literature review with an explicit gap statement. This is the bridge between
"what exists" and "what we build":

```
Despite significant progress in GUI agent benchmarks and HTML understanding,
no existing system provides a pre-computed, graph-structured map of website
state spaces. Agents continue to explore reactively, discovering navigation
paths through trial-and-error during task execution. This report addresses
this gap by introducing offline UTG crawling as a complement to online
agent reasoning.
```

### Length Guidance

| Thesis Length | Literature Review Pages | Number of References |
|:---:|:---:|:---:|
| 40-60 pp (FYP) | 8-12 | 30-50 |
| 80-100 pp (MSc) | 12-18 | 50-80 |
| 200+ pp (PhD) | 25-40 | 100-200+ |

---

## 6. Gopen & Swan's 7 Principles of Reader Expectations

These principles, from George Gopen and Judith Swan's "The Science of Scientific
Writing" (American Scientist, 1990), describe how readers **actually process** English
prose. Violating these expectations forces readers to re-read, misinterpret, or lose
focus. In a 100-page thesis, even small violations compound into an exhausting read.

### Principle 1: Subject-Verb Proximity

**Rule**: Keep the grammatical subject and its main verb as close together as possible.

When words intervene between subject and verb, the reader must hold the subject in
working memory while processing the interruption. This drains cognitive resources.

| Quality | Example |
|---------|---------|
| Bad | "The crawler, which was designed to handle SPAs with dynamic content loading and client-side routing while respecting rate limits and domain boundaries, **extracts** interactable elements." |
| Good | "The crawler **extracts** interactable elements from SPAs. It handles dynamic content loading, client-side routing, rate limits, and domain boundaries." |

**The fix is almost always the same**: split the sentence. Move the interrupting clause
into its own sentence.

**Measurement**: Count the words between subject and main verb. If the count exceeds 8-10,
restructure.

### Principle 2: Stress Position

**Rule**: Place the most important information at the end of a sentence.

English sentences have a natural stress position: the period. Readers unconsciously
assign the most emphasis to whatever they read just before the full stop. Burying the
key point mid-sentence wastes this emphasis.

| Quality | Example |
|---------|---------|
| Bad | "The success rate **doubled** from 25.6% to 50.0%, which we observed when using the URL condition." |
| Good | "When using the URL condition, the success rate **doubled from 25.6% to 50.0%**." |

**Application**: When writing a result sentence, place the number at the end. When
writing a motivation sentence, place the consequence at the end.

### Principle 3: Topic Position

**Rule**: Place familiar, contextual information at the beginning of a sentence.

The opening of a sentence sets the reader's frame. If you start with unfamiliar or
complex information, the reader has no context for interpreting it.

| Quality | Example |
|---------|---------|
| Bad | "A 768-dimensional CLIP embedding of each screenshot is stored in the topic position of our state representation." |
| Good | "Each state is represented by a 768-dimensional CLIP embedding of its screenshot." |

**The first few words should answer**: "What is this sentence about?" If the reader
cannot tell by word 5, the topic position is wrong.

### Principle 4: Old Before New

**Rule**: Present information the reader already knows before introducing new information.

This principle creates a chain: each sentence picks up where the last one left off.
New information in sentence N becomes old information in sentence N+1.

| Quality | Example |
|---------|---------|
| Bad (new before old) | "DOM hashing produces the state identifier. The state identifier, computed from the structural signature of the page, determines whether two pages are equivalent." |
| Good (old before new) | "The state identifier determines whether two pages are equivalent. **This identifier** is computed by hashing the structural signature of the DOM." |

**Test**: Underline the first noun phrase of each sentence. If it was not mentioned in
the previous sentence (or does not refer to a concept already established), the
transition is jarring.

### Principle 5: One Unit, One Function

**Rule**: Each paragraph should make exactly one point. Each sentence should express
exactly one idea.

When a paragraph tries to make two points, readers lose track of which one matters.
When a sentence crams in two ideas, the second one is often missed.

| Level | Bad | Good |
|-------|-----|------|
| Sentence | "The crawler extracts actions and the state abstractor hashes the DOM and the graph stores transitions." | "The crawler extracts actions. The state abstractor hashes the DOM. The graph stores transitions." |
| Paragraph | A paragraph that discusses both the crawling algorithm AND the evaluation metrics | Split into two paragraphs, one per topic |

**Paragraph architecture**:
```
Sentence 1: Topic sentence (the one point this paragraph makes)
Sentences 2-4: Evidence, explanation, or elaboration
Final sentence: Transition or summary
```

### Principle 6: Action in Verb

**Rule**: Express actions as verbs, not as nominalizations (noun forms of verbs).

Nominalizations drain energy from prose. They hide the actor and make sentences
passive and lifeless.

| Nominalization | Verb Form |
|----------------|-----------|
| "The **extraction** of actions was performed by the crawler." | "The crawler **extracted** actions." |
| "**Computation** of the hash occurs in O(n) time." | "The hash **is computed** in O(n) time." |
| "We performed an **investigation** of the failure modes." | "We **investigated** the failure modes." |
| "The **utilization** of DOM hashing enables..." | "DOM hashing **enables**..." |
| "The **implementation** of the system was done in Python." | "We **implemented** the system in Python." |

**Detection trick**: Search your draft for words ending in "-tion", "-ment", "-ness",
"-ance". Many will be nominalizations that should be verbs.

### Principle 7: Context Before New

**Rule**: Before presenting new technical content, establish the context that makes it
interpretable.

This is the "set the stage" principle. It applies at every scale: within sentences,
within paragraphs, and within sections.

| Scale | Bad | Good |
|-------|-----|------|
| Sentence | "We used xxHash because it is non-cryptographic." | "State hashing must be fast rather than collision-resistant. **Therefore**, we used xxHash, a non-cryptographic hash function." |
| Paragraph | Jump straight into algorithm pseudocode | Open with 2 sentences explaining what the algorithm does and why it is needed, then present the pseudocode |
| Section | Present Table 5.3 without explaining what it shows | Open the section by stating the research question, then present the table as evidence |

**Application to figures and tables**: Never place a figure before the paragraph that
explains its purpose. The reader needs context before they can interpret the visual.

### Summary Table: All 7 Principles

| # | Principle | Mnemonic | Test |
|:-:|-----------|----------|------|
| 1 | Subject-verb proximity | "Don't interrupt yourself" | Count words between subject and verb. Target: <8. |
| 2 | Stress position | "Save the best for last" | Is the key information at the end of the sentence? |
| 3 | Topic position | "First things first" | Can the reader tell the topic by word 5? |
| 4 | Old before new | "Build on known ground" | Does the sentence start with something already established? |
| 5 | One unit, one function | "One idea per container" | Does this paragraph make exactly one point? |
| 6 | Action in verb | "Verbs do, nouns sit" | Any nominalizations that should be verbs? |
| 7 | Context before new | "Set the stage first" | Is there context before every new concept? |

---

## 7. Micro-Level Tips (Ethan Perez)

These sentence-level habits, drawn from Ethan Perez's writing advice and standard
academic style guides, apply to every page of the thesis.

### 7.1 Minimize Pronoun Ambiguity

Pronouns create ambiguity when the antecedent is unclear. In technical writing, this
ambiguity can change meaning.

| Bad | Problem | Good |
|-----|---------|------|
| "This shows that the method works." | What does "this" refer to? | "This result shows that the method works." |
| "It is computed efficiently." | What is "it"? | "The state hash is computed efficiently." |
| "They are stored in the graph." | Who are "they"? | "The transitions are stored in the graph." |
| "We did this because it improved performance." | Double ambiguity | "We added caching because caching reduced latency by 40%." |

**Rule of thumb**: Every "this", "it", and "they" should have an unambiguous antecedent
within the same sentence or the immediately preceding one. If in doubt, repeat the noun.

### 7.2 Position Verbs Early

Front-loading verbs increases sentence energy and reduces the reader's cognitive load.

| Verb Late | Verb Early |
|-----------|------------|
| "The system, after processing the DOM and filtering hidden elements, extracts actions." | "The system extracts actions after processing the DOM and filtering hidden elements." |
| "Conditions A and B, which serve as ablation controls, were run first." | "We ran conditions A and B first as ablation controls." |

### 7.3 Active Voice (Default) vs. Passive Voice (Exception)

**Default to active voice.** It is clearer, shorter, and assigns responsibility.

| Passive | Active |
|---------|--------|
| "The DOM was hashed by the state abstractor." | "The state abstractor hashed the DOM." |
| "It was found that URL-based retrieval is fragile." | "We found that URL-based retrieval is fragile." |
| "The evaluation was conducted on 90 tasks." | "We evaluated on 90 tasks." |

**Exception**: Use passive voice when the actor is irrelevant or unknown:
- "The dataset was collected from Mind2Web." (the collector is irrelevant)
- "Informed consent was obtained." (required phrasing in ethics sections)

### 7.4 Delete Filler Words

Search your entire draft for these words. Delete them unless they carry genuine meaning:

| Filler | Frequency in Drafts | Replace With |
|--------|:---:|---------|
| "actually" | Very high | Delete |
| "basically" | High | Delete |
| "essentially" | High | Delete |
| "very" | Very high | Delete or use a stronger adjective |
| "really" | High | Delete |
| "quite" | Medium | Delete |
| "somewhat" | Medium | Delete or quantify |
| "relatively" | Medium | Quantify (relative to what?) |
| "in order to" | High | "to" |
| "due to the fact that" | Medium | "because" |
| "it is important to note that" | High | Delete the phrase, keep the content |
| "it should be noted that" | High | Delete the phrase, keep the content |

### 7.5 Paragraph Architecture

Every paragraph should follow a predictable structure:

```
[Topic sentence]     -- What this paragraph is about (1 sentence)
[Development]        -- Evidence, explanation, or examples (2-5 sentences)
[Transition/summary] -- Connect to next paragraph or summarize (1 sentence, optional)
```

**Topic sentence test**: Read only the first sentence of every paragraph in a chapter.
If these sentences alone tell a coherent story, your paragraphs are well-structured.

### 7.6 Sentence Length Variation

Monotonous sentence length makes prose tedious. Alternate between short and long
sentences to create rhythm.

| Bad (monotone) | Good (varied) |
|----------------|---------------|
| "The crawler visits a page. It extracts all actions. It hashes the DOM. It stores the state. It picks the next action." | "The crawler visits a page and extracts all interactable elements. It then hashes the DOM to produce a state identifier. If the state is new, the crawler stores it and picks the next unexplored action." |

**Guideline**: Average sentence length of 15-20 words. Mix short sentences (8-12 words)
for emphasis with longer ones (20-30 words) for explanation.

### 7.7 Transition Words Between Paragraphs

Explicit transitions prevent the reader from feeling lost between paragraphs. Use them
at paragraph boundaries, especially across page breaks.

| Relationship | Transition Words |
|-------------|-----------------|
| Addition | "Furthermore," "Moreover," "In addition," |
| Contrast | "However," "In contrast," "Nevertheless," |
| Cause | "Therefore," "Consequently," "As a result," |
| Example | "For instance," "Specifically," "In particular," |
| Sequence | "First," "Next," "Finally," |
| Summary | "In summary," "Overall," "To summarize," |

---

## 8. Word Choice (Lipton, Steinhardt)

Michael Lipton and Jacob Steinhardt have both written about how imprecise word choice
undermines technical writing. These rules apply with extra force in a thesis, where the
examiner is evaluating your precision of thought.

### 8.1 Be Specific

Vague terms signal vague thinking. Replace every vague word with the most specific
term available.

| Vague | Specific |
|-------|----------|
| "performance" | "success rate" or "latency" or "throughput" (which one?) |
| "good results" | "50.0% success rate, doubling the baseline" |
| "the system works well" | "the system completes 45 of 90 tasks within the time limit" |
| "significant improvement" | "24.4 percentage point improvement (p < 0.001, McNemar's test)" |
| "various techniques" | "BFS exploration, DOM hashing, and action deduplication" |
| "recently" | "in 2024" or "since the introduction of GPT-4V" |
| "large-scale" | "2,350 tasks across 137 websites" |
| "state-of-the-art" | Name the specific system and its performance |

### 8.2 Eliminate Hedging

Hedging makes claims weaker without adding honesty. Remove hedging words unless you are
genuinely uncertain.

| Hedged (weak) | Direct (strong) |
|---------------|-----------------|
| "This may suggest that UTGs are useful." | "This demonstrates that UTGs are useful." |
| "The results seem to indicate an improvement." | "The results show an improvement." |
| "It is possible that the approach could work." | "The approach works." (if you have evidence) |
| "We believe this is due to information density." | "This is due to information density." (if you have evidence) |

**Exception**: Hedge genuinely uncertain claims. "Judge non-determinism may account for
up to 5 percentage points of variance" is honest hedging because you have quantified the
uncertainty.

**Test**: For every "may," "might," "could," "seems," and "appears" in your draft, ask:
"Do I have evidence?" If yes, remove the hedge. If no, either add the evidence or
explicitly state why you cannot be certain.

### 8.3 Consistent Terminology

Pick one term per concept. Use it everywhere. Never vary for "elegant" prose.

| Inconsistent (confusing) | Consistent (clear) |
|--------------------------|---------------------|
| "state", "page", "screen", "view" used interchangeably | "state" everywhere; define it once in Ch3 |
| "action", "interaction", "operation", "event" | "action" everywhere |
| "UTG", "state graph", "transition graph", "navigation map" | "UTG" as the acronym, "UI Transition Graph" spelled out once |
| "success rate", "accuracy", "completion rate", "pass rate" | "success rate" everywhere |

**Create a terminology table** in Chapter 1 or Chapter 3:

```latex
\begin{table}[t]
\centering
\caption{Key terminology used throughout this report.}
\begin{tabular}{ll}
\toprule
Term & Definition \\
\midrule
State & A unique configuration of available actions on a web page \\
Action & An interactable element (button, link, input field) \\
UTG & UI Transition Graph: a directed graph of states and transitions \\
Step & One LLM reasoning turn (may execute multiple browser actions) \\
\bottomrule
\end{tabular}
\end{table}
```

### 8.4 Avoid Hype Words

These words signal marketing, not science. Never use them in academic writing:

| Banned | Why | Replacement |
|--------|-----|-------------|
| "revolutionary" | Unsubstantiated | "novel" or describe what makes it new |
| "groundbreaking" | Unsubstantiated | Describe the specific advance |
| "dramatically" | Vague intensifier | Quantify: "by 24.4 percentage points" |
| "cutting-edge" | Marketing language | "recent" |
| "state-of-the-art" (as adjective) | Overused and often wrong | Name the specific system |
| "game-changing" | Marketing language | Describe the specific impact |
| "leverages" | Jargon | "uses" |
| "utilizing" | Jargon | "using" |
| "facilitates" | Vague | Name the specific action |
| "holistic" | Meaningless in technical context | Describe what is actually comprehensive |

---

## 9. Mathematical Writing

### 9.1 Notation Conventions

Define all notation in a central location (notation table or dedicated section) and
refer to it consistently.

**Notation table template**:

```latex
\begin{table}[t]
\centering
\caption{Notation used throughout this report.}
\begin{tabular}{cl}
\toprule
Symbol & Meaning \\
\midrule
$G = (V, E)$ & UI Transition Graph with states $V$ and transitions $E$ \\
$s_i \in V$ & A state (node) in the UTG \\
$(s_i, a, s_j) \in E$ & A transition from $s_i$ to $s_j$ via action $a$ \\
$h(d)$ & Hash function mapping DOM structure $d$ to a state identifier \\
$|V|$ & Number of unique states discovered \\
$|E|$ & Number of unique transitions discovered \\
\bottomrule
\end{tabular}
\end{table}
```

### 9.2 State Assumptions Formally

Every mathematical claim should explicitly state its assumptions before the result.

**Bad**:
> The expected number of states is bounded by $|V| \leq n^k$.

**Good**:
> **Assumption**: The web application has $n$ distinct URL paths, each with at most $k$
> modal states.
>
> **Proposition**: Under this assumption, the state space is bounded by $|V| \leq n \cdot k$.

### 9.3 Define Before Use

Every symbol must be defined before (or immediately after) its first use. Never assume
the reader will look up the notation table.

**Bad**:
> We compute $h(d)$ for each page.

**Good**:
> We compute the state hash $h(d)$, where $d$ is the DOM structure of the current page.

### 9.4 Equation Formatting Rules

| Rule | Bad | Good |
|------|-----|------|
| Display equations for important formulas | Inline: $\text{success\_rate} = \frac{\text{passed}}{\text{total}} \times 100$ | Display: Use `\begin{equation}` |
| Number equations that are referenced | Unnumbered equation referenced as "the equation above" | `\begin{equation} \label{eq:success_rate}` and "Equation~\ref{eq:success_rate}" |
| Punctuate equations as part of the sentence | Equation followed by a new sentence with no punctuation | End displayed equations with a period or comma |
| Use consistent font for variables | Mix of italic, roman, and bold for the same type of variable | Italic for variables, bold for vectors/matrices, roman for functions |

### 9.5 When NOT to Use Math

Not every concept benefits from formal notation. Use mathematics when:
- Precision is essential (algorithm specifications)
- The relationship is complex and words would be ambiguous
- You need to reference the formula later

Avoid mathematics when:
- A sentence expresses the idea clearly ("the hash is computed in linear time")
- The notation adds complexity without precision
- You are in the introduction or conclusion (minimize notation in narrative chapters)

---

## 10. Figure Design

### 10.1 The Self-Contained Caption Principle

**A reader should understand the figure from its caption alone, without reading the main
text.** This is the single most important rule of figure design.

Every caption must answer:
1. **What** does this figure show?
2. **How** should the reader interpret it? (axis meanings, color coding)
3. **What** is the takeaway?

| Bad Caption | Good Caption |
|-------------|-------------|
| "Results of the ablation study." | "Ablation study results on 90 Mind2Web tasks. Bars show success rate for each condition. Error bars indicate 95% confidence intervals (Wilson). The URL condition (C) and Tools condition (D) both achieve 50.0%, doubling the 25.6% baseline (A). Differences are statistically significant (p < 0.001, McNemar's test)." |
| "System architecture." | "Architecture of the UTG crawler. Five core modules process web pages from left (browser automation) to right (graph output). Arrows indicate data flow. The state abstractor (center) determines whether a new page represents a novel state by hashing its DOM structure." |

### 10.2 Vector vs. Raster

| Content Type | Format | Why |
|-------------|--------|-----|
| Plots (bar, line, scatter) | PDF (vector) | Scales without pixelation |
| Diagrams (architecture, flow) | PDF (vector) | Clean lines at any zoom |
| Screenshots | PNG (300+ DPI) | Photographs cannot be vectorized |
| Photographs | PNG or JPEG (300+ DPI) | Raster by nature |

**Always generate both** `figure.pdf` and `figure.png`. LaTeX uses the PDF; the PNG is
for previewing and presentations.

### 10.3 Colorblind-Safe Palettes

8% of men have some form of color vision deficiency. Use palettes designed for
universal accessibility.

**Recommended: Okabe-Ito palette**

| Color | Hex | Use |
|-------|-----|-----|
| Orange | `#E69F00` | Primary category 1 |
| Sky blue | `#56B4E9` | Primary category 2 |
| Bluish green | `#009E73` | Primary category 3 |
| Yellow | `#F0E442` | Highlight / warning |
| Blue | `#0072B2` | Primary category 4 |
| Vermillion | `#D55E00` | Emphasis / alert |
| Reddish purple | `#CC79A7` | Primary category 5 |
| Black | `#000000` | Text / baseline |

**Alternative: Paul Tol palette** for situations requiring more than 8 colors.

**Never** use red-green distinctions as the only differentiator. Always add a secondary
cue: shape (circle vs. square), pattern (solid vs. dashed), or label.

### 10.4 Typography in Figures

| Element | Recommended Size | Font |
|---------|:---:|------|
| Axis labels | 11-12pt | Match document font (serif for LaTeX default) |
| Tick labels | 10pt | Same font |
| Legend text | 10pt | Same font |
| Title | None | Remove; use the caption instead |
| Annotations | 9-10pt | Same font |

**Remove all default matplotlib titles.** The LaTeX caption serves this function.
Having both a title inside the figure and a caption below creates redundancy and
wastes space.

### 10.5 Consistent Style Across All Figures

All figures in the thesis should share:
- Same color palette
- Same font family and sizes
- Same line widths (1.5-2pt for data, 0.5-1pt for grid)
- Same figure dimensions or consistent aspect ratios
- Same legend position convention (e.g., always upper right or outside)

**Implement this via a shared style file**:

```python
# style.py - import in every figure script
import matplotlib.pyplot as plt
import matplotlib

COLORS = ['#E69F00', '#56B4E9', '#009E73', '#F0E442',
          '#0072B2', '#D55E00', '#CC79A7', '#000000']

def apply_style():
    matplotlib.rcParams.update({
        'font.size': 11,
        'font.family': 'serif',
        'axes.labelsize': 12,
        'axes.titlesize': 13,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.figsize': (6.5, 4),
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'lines.linewidth': 1.5,
        'axes.grid': True,
        'grid.alpha': 0.3,
    })
```

### 10.6 Common Figure Mistakes

| Mistake | Why It's Bad | Fix |
|---------|-------------|-----|
| Title inside figure AND caption below | Redundant information | Remove the figure title |
| Tiny text (6-8pt in figure) | Illegible when printed | Minimum 9pt for any text |
| PNG for line plots | Pixelated when zoomed | Export as PDF |
| Rainbow colormap | Not colorblind-safe, perceptually non-uniform | Use sequential (viridis) or qualitative (Okabe-Ito) |
| 3D bar charts | Distort perception of values | Use 2D bars |
| Inconsistent axis ranges across subplots | Prevents comparison | Share axes or explicitly note different scales |
| Legend covering data | Obscures the content | Move legend outside plot area |

---

## 11. Common Mistakes (Thesis-Specific)

These mistakes are specific to long-form academic documents. They are rare in conference
papers but endemic in theses.

### 11.1 Padding

**Symptom**: Pages of background that any computer science student already knows.

**Examples**:
- Two pages explaining what HTML is
- A page on the history of web browsers
- Explaining Python as a programming language

**Fix**: Assume your reader has a CS degree. Start from where their knowledge ends.
Ask: "Would my examiner already know this?" If yes, cut it to one sentence or
delete entirely.

| Padding | Appropriate |
|---------|-------------|
| "HTML, or HyperText Markup Language, is the standard markup language for creating web pages. It was created by Tim Berners-Lee in 1993..." | "The crawler parses the HTML DOM tree to extract interactable elements." |
| "Python is a high-level, interpreted programming language known for its readability..." | "The system is implemented in Python 3.12 using Playwright for browser automation." |

### 11.2 Inconsistent Voice Across Chapters

**Symptom**: Chapter 3 uses "we" while Chapter 5 uses "the system." Chapter 2 is
formal while Chapter 4 is casual.

**Cause**: Chapters written at different times (or by different agents) without style
unification.

**Fix**: After all chapters are written, do a dedicated style unification pass:
- Choose "we" or "the author" and use it everywhere
- Choose present tense ("the system extracts") or past tense ("the system extracted")
  and be consistent within each chapter
- Match formality level across all chapters

| Convention | Recommendation |
|------------|----------------|
| Person | "We" (even for single-author theses; it means "the author and the reader") |
| Tense for system description | Present: "The crawler extracts actions" |
| Tense for experiments | Past: "We evaluated on 90 tasks" |
| Tense for results | Present: "Table 5.1 shows that..." |

### 11.3 Missing Chapter Transitions

**Symptom**: Each chapter starts abruptly with no connection to the previous one.

**Fix**: End each chapter with a 2-3 sentence transition paragraph and begin each
chapter with a 2-3 sentence context paragraph.

```latex
% End of Chapter 3
Having described the system architecture and its five core modules, we now
turn to the experimental methodology used to evaluate the system's effectiveness.

% Start of Chapter 4
Chapter~\ref{ch:system} described the design and implementation of the UTG
crawler. This chapter presents the experimental setup used to evaluate whether
UTG-augmented agents outperform baseline agents.
```

### 11.4 Results Without Claims

**Symptom**: Tables and figures presented without interpretation. "Table 5.2 shows the
results" followed immediately by the next table.

**Fix**: Every result must answer three questions:

1. **What claim does this result support?**
2. **What are the specific numbers?**
3. **Is it statistically significant?**

**Bad**:
> Table 5.2 shows the results of the ablation study.

**Good**:
> Table 5.2 shows that structured UTG retrieval (conditions C and D) doubles the
> agent's success rate from 25.6% to 50.0% (p < 0.001, McNemar's test). This
> supports our hypothesis that pre-computed navigation maps reduce exploration
> overhead.

### 11.5 Citing Without Integrating

**Symptom**: Citations appear as afterthoughts: "(Smith et al., 2023)" dropped into
sentences without integration.

| Bad | Good |
|-----|------|
| "State abstraction is important (Li et al., 2022)." | "Li et al. (2022) demonstrated that DOM-based state abstraction reduces state explosion by 60% compared to URL-based approaches." |
| "Many approaches exist (A, B, C, D)." | "Recent approaches fall into two categories: DOM-based (A, B) and vision-based (C, D). DOM-based approaches achieve higher precision but require page source access." |

### 11.6 Overly Long Sentences

**Symptom**: Sentences exceeding 40 words, with multiple clauses chained by commas.

**Detection**: Run a sentence-length analysis. Flag all sentences over 35 words.

**Fix**: Split. A 40-word sentence almost always contains two ideas that are better
expressed as two sentences.

### 11.7 Figures Distant From Text

**Symptom**: A figure is discussed on page 34 but appears on page 37.

**Fix**: Use LaTeX float placement `[htbp]` and discuss the figure in the text
immediately before or after it. If LaTeX places the figure far away, use `[H]` from
the `float` package (sparingly) or restructure the text.

### 11.8 Copy-Pasted Code Blocks Without Explanation

**Symptom**: Large code blocks dropped into the text with only "The code below
implements X."

**Fix**: Code in the body should be:
- Short (10-20 lines maximum)
- Accompanied by line-by-line or block-by-block explanation
- Formatted with `lstlisting` or `minted` (with syntax highlighting)
- Relegated to appendices if longer than 20 lines

### 11.9 The "Future Work Dump"

**Symptom**: The future work section lists 10+ vague ideas ("explore more datasets,"
"try other models," "improve efficiency").

**Fix**: List 2-4 concrete, actionable directions. For each, explain:
1. What specifically would be done
2. Why it is the logical next step
3. What result you would expect

---

## 12. Pre-Submission Checklist for Thesis

### Content Quality

- [ ] **Spine test passed**: Can you summarize each chapter in one sentence, and do
      the six sentences tell one coherent story?
- [ ] **Every claim has evidence**: No unsupported assertions. Every claim cites data,
      a reference, or logical argument.
- [ ] **Numbers verified**: Every number in the text matches the source data. Spot-check
      at least 5 key numbers against raw results.
- [ ] **Consistent terminology**: One term per concept, used identically in every chapter.
- [ ] **No padding**: Remove any background a CS graduate already knows.
- [ ] **Honest limitations**: At least 3 substantive limitations, not just "time constraints."

### Writing Quality

- [ ] **Active voice**: Passive voice used only where justified (actor irrelevant).
- [ ] **No filler words**: "actually," "basically," "very" removed unless genuinely needed.
- [ ] **Pronoun clarity**: Every "this," "it," "they" has an unambiguous antecedent.
- [ ] **Paragraph structure**: Every paragraph has a topic sentence. First sentences of
      all paragraphs tell the chapter's story when read alone.
- [ ] **Sentence length variation**: Average 15-20 words, mix of short and long.
- [ ] **Chapter transitions**: Every chapter ends with a bridge to the next and begins
      with a context-setting paragraph.
- [ ] **Consistent voice**: Same person (we/I), same tense conventions across all chapters.

### Figures and Tables

- [ ] **Self-contained captions**: Every figure/table can be understood from its caption alone.
- [ ] **Vector graphics**: All plots and diagrams are PDF (not PNG).
- [ ] **Colorblind-safe**: No red-green only distinctions. Okabe-Ito or equivalent palette.
- [ ] **No titles inside figures**: Caption serves this function.
- [ ] **Consistent style**: Same colors, fonts, sizes across all figures.
- [ ] **Tables use booktabs**: `\toprule`, `\midrule`, `\bottomrule`. No vertical lines.
- [ ] **Best values bolded**: In comparison tables, bold the best result per metric.

### Mathematical Content

- [ ] **All symbols defined**: Every symbol is defined before or immediately after first use.
- [ ] **Notation table**: Central reference for all notation (if math-heavy).
- [ ] **Assumptions stated**: Every mathematical claim states its assumptions.
- [ ] **Equations numbered**: Referenced equations have numbers; unreferenced ones may be
      unnumbered.
- [ ] **Equations punctuated**: Displayed equations end with period or comma.

### Citations and References

- [ ] **No fabricated citations**: Every BibTeX entry fetched from Semantic Scholar,
      CrossRef, or arXiv (NEVER from AI memory).
- [ ] **All citations resolved**: No `[?]` in the compiled PDF.
- [ ] **Citation style consistent**: Matches university requirements (Harvard, APA, IEEE,
      numbered, etc.).
- [ ] **Integrated citations**: Citations are woven into sentences, not dropped as
      parenthetical afterthoughts.

### LaTeX and Compilation

- [ ] **No undefined references**: `\ref` and `\cite` all resolve.
- [ ] **No duplicate labels**: Run `cross_ref_audit.py` or grep for duplicates.
- [ ] **No overfull hboxes**: Fix all major overfull warnings (minor ones in URLs are
      acceptable).
- [ ] **Table of Contents accurate**: Matches actual chapter/section titles.
- [ ] **List of Figures / Tables complete**: All figures and tables appear.
- [ ] **Page numbers correct**: Front matter uses roman numerals; body uses arabic.
- [ ] **Appendices lettered**: A, B, C (not numbered as chapters).

### University-Specific Requirements

- [ ] **Title page format**: Matches university template exactly.
- [ ] **Margins**: Comply with university specifications (often 1.5" left for binding).
- [ ] **Font and size**: As specified (often 12pt Times New Roman or Computer Modern).
- [ ] **Abstract word count**: Within university limit (typically 250-350 words).
- [ ] **Declaration of originality**: Signed and included.
- [ ] **Word/page count**: Within university limits.
- [ ] **Binding and submission format**: Print copies, digital submission, or both.

### Final Read-Through

- [ ] **Read aloud**: Read the abstract and introduction aloud. Awkward phrasing
      becomes obvious when spoken.
- [ ] **Fresh eyes**: If possible, have someone else read at least the abstract,
      introduction, and conclusion.
- [ ] **Print preview**: View the PDF at 100% zoom on screen (or print). Check figure
      sizes, text legibility, page breaks.
- [ ] **Spell check**: Run a spell checker. LaTeX-aware tools (e.g., `aspell` with
      `--mode=tex`) avoid flagging commands.

---

## Appendix A: Quick Reference Card

### Sentence-Level Checklist (Apply to Every Sentence)

```
1. Subject and verb within 8 words of each other?
2. Key information at the end (stress position)?
3. Topic clear by word 5?
4. Starts with old/known information?
5. One idea only?
6. Action expressed as verb (not nominalization)?
7. Context established before new content?
```

### Paragraph-Level Checklist (Apply to Every Paragraph)

```
1. Topic sentence first?
2. One point per paragraph?
3. Evidence/explanation follows topic sentence?
4. Transition to next paragraph at end?
5. Under 8 sentences?
```

### Chapter-Level Checklist (Apply to Every Chapter)

```
1. Opens with context paragraph connecting to previous chapter?
2. Advances the thesis spine (one-sentence summary)?
3. Ends with transition to next chapter?
4. Consistent terminology with all other chapters?
5. Consistent voice (person, tense) with all other chapters?
6. All figures/tables have self-contained captions?
7. All claims supported by evidence or references?
```

---

## Appendix B: Recommended Reading

| Source | What You Learn | Read When |
|--------|---------------|-----------|
| Gopen & Swan, "The Science of Scientific Writing" (1990) | The 7 principles in full | Before writing any chapter |
| Neel Nanda, "How to write a great research paper" | Narrative structure, one-story principle | Before planning outline |
| Simon Peyton Jones, "How to write a great research paper" (talk) | Paper structure, conveying ideas | Before writing introduction |
| Ethan Perez, ML writing tips | Micro-level sentence optimization | During revision pass |
| Jacob Steinhardt, "Thoughts on ML writing" | Word choice, eliminating vagueness | During revision pass |
| Michael Lipton, "Troubling Trends in ML Scholarship" | Avoiding hype, being precise | Before writing results |
| Andrej Karpathy, writing advice (various posts) | Start with the insight, build outward | Before planning outline |
| Gregory Farquhar, "How to write a great abstract" | 5-sentence abstract formula | When writing abstract |
| Strunk & White, "The Elements of Style" | General concise writing | Reference throughout |
| Knuth, "Mathematical Writing" | Notation, equation formatting | When writing formal definitions |
