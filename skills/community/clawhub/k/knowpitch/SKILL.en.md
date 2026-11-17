---
name: knowpitch
description: >-
  Break down any knowledge domain into a "football team" for deep learning and mastery.
  Triggers: kp11/kpt/kpitch/knowpitch + topic; formation learning, knowledge formation diagram,
  position codes like 4-3-3/CB/CDM/AMD + learning; "explain with football formation", "arrange as a team".
  Output: formation diagram SVG + player cards (ELI5 style) + tactics board (learning path and connections).
  Do NOT use for: quick concept explanation (use ELI5), mind maps, flashcards,
  non-knowledge topics (emotions/counseling), reports requiring precise data.
allowed-tools: Bash(python3:*) Read Write Glob
metadata:
  version: "1.3.0"
  category: learning
  compatibility: Requires Python 3.8+ for SVG generation.
  tags: [learning, education, visualization, eli5, football-formation]
---

> **Translation status — read first.** This English file tracks the Chinese canonical skill up to **v1.3**. The Chinese `SKILL.md` is authoritative for **v1.4.0 and later**, including the fail-loud rendering contract, the `--strict` flag, exit codes (0 = ok, 2 = bad input, 3 = warnings under `--strict`), and the guarantee that overflow players move to the bench instead of disappearing. Whenever this file and `SKILL.md` differ, follow `SKILL.md` and `references/json-schema.md` (Chinese).

# KnowPitch — Formation Learning Method

> **Put your knowledge on the pitch.**

## Applicable Boundaries

✅ **Good for:** Systematic learning, knowledge organization, exam prep, teaching preparation, deep concept understanding
❌ **Not for:** Quick Q&A, emotional counseling, precise data analysis, code debugging, pure fact lookup

## Prerequisites

- Python 3.8+ (for generating formation diagram SVG)
- Topic must be "knowledge-type" (has clear concept system), not emotional/opinion-type
- If external facts needed, research/read first to ensure knowledge points have sources and are not fabricated

## Core Mindset

> Before arranging the formation, ask yourself:
> 1. **What is the "goalkeeper" of this topic?** (the most foundational, everything collapses without it)
> 2. **What is the "striker" of this topic?** (the core conclusion to ultimately answer)
> 3. **How does the "midfield" in between turn foundation into conclusion?** (mechanisms/methods/ideas)

## What This Skill Is

Treat any knowledge domain as a **football team**: knowledge points are players, arranged into formations like 4-3-3, 4-2-3-1 by function,
plus a head coach (one-sentence core idea), a goalkeeper (bottom-line foundation), and a bench (advanced knowledge points).
Each "player" is explained in plain language using the ELI5 approach. Final deliverable: **formation diagram (SVG) + player cards + coach tactics board**.

It internalizes the ELI5 skill's core, so all explanations follow:

> **Assume zero background, not zero intelligence**
> - Use plain language + everyday analogies a 5-year-old could understand, without sacrificing accuracy.
> - Every technical term, when first mentioned, is immediately followed by a plain-language explanation.
> - Short sentences, short paragraphs, conversational; first explain "what it does", then "how it works", finally "why it matters".

## Workflow

Execute in order:

### Step 1: Identify Topic and Depth Requirements
- Parse user request, determine the topic to learn
- Parse audience parameters (--age/--job/--grade), adjust language difficulty and analogy direction
- Determine depth the user needs:
  - `kpt` / Quick mode: ≤ 5 knowledge points, compact formation
  - `kp11` / Default mode: 6-11 knowledge points, standard formation
  - `kpitch` / Full mode: > 20 knowledge points, enable B team
- If external facts needed, research/read first to ensure knowledge points have sources and are not fabricated; mark uncertain ones as "to be verified".

### Step 2: Inventory Knowledge Points and Function Classification
- List the **mainstream knowledge points** of the topic
- For each, first write "one-sentence plain explanation + one everyday analogy"
- Tag with function label: foundation(defend)/mechanism(transition)/idea(think)/application(attack)/conclusion(score)
- Adjust analogy direction based on audience parameters (--age 5 uses toy analogies, --job manager uses business analogies)

### Step 3: Select Formation (Decision Tree)

Select formation using the following decision tree:

```
Number of knowledge points?
├─ ≤ 5 → Compact formation (head coach + goalkeeper + positions that fit, don't force fill)
├─ 6-11 → One main formation
├─ 12-20 → Main + bench
└─ > 20 → Main + B team

Knowledge structure shape?
├─ Balanced foundation/mechanism/application → 4-3-3
├─ One very clear main conclusion → 4-2-3-1 (single striker + three attacking mids)
├─ Main conclusion + two derived conclusions → 4-3-2-1 (Christmas tree)
├─ Theory vs practice two major blocks → 4-4-2
├─ One key mechanism underpinning → 4-1-4-1 (single defensive mid)
├─ Especially many mechanisms/methods → 4-5-1 or 3-5-2
└─ Especially many applications/cases → 3-4-3
```

**Formation selection tradeoffs:**
- 4-3-3 is most versatile, but weak for topics with "single main conclusion"
- 4-2-3-1 suits "goal-oriented" topics, but midfield defense (foundation) may be weak
- 3-5-2 has thickest midfield, but only 3 defenders (foundation), not suitable for topics with many basic concepts

### Step 4: Arrange Positions
- Following the role mapping in `references/positions.md`, place knowledge points into corresponding positions:
  - Head coach = one-sentence core idea
  - Goalkeeper = most foundational
  - CB = core foundation
  - LB/RB = background prerequisites
  - CDM = mechanism
  - CM = method/process
  - AMD(CAM) = core idea/theory
  - LW/RW = application/case
  - CF = core conclusion
  - SS = derived conclusion
  - Bench = advanced/edge
- **If fewer than 11 players, leave positions empty** (= positions to dig deeper)

### Step 5: Write Player Cards (ELI5 Style)
- Each starting player outputs using the [Player Card Template] below in ELI5 style
- Bench/B team can be simpler
- Adjust language difficulty based on audience parameters (--age 5 each sentence ≤10 words, --age 25+ can use terminology)
- **Quality standard:** Zero-background reader can understand, has everyday analogy, no unexplained terminology

### Step 6: Draw Tactics Board
- Write learning path (ball flow, e.g., GK→CB→CDM→AMD→CF)
- Key connections (who is strongly related to whom)
- "Three ways to lose" (most easily misunderstood/wrong points)

### Step 7: Render Formation Diagram
- Write formation as JSON (structure see [Formation Diagram JSON Schema] below)
- Run `python3 scripts/formation_diagram.py team.json output.svg`
- Verify output SVG exists and is non-empty

### Step 8: Deliver and Quality Self-Check
- Organize content following [Output Template]
- Deliver formation diagram using present_files
- Complete 10-item quality self-check list

## Exception Handling

| Situation | Handling |
|-----------|----------|
| Knowledge points < 3 | Prompt user topic is too narrow, suggest expansion; only arrange "head coach + goalkeeper + 1 defender" |
| Knowledge points > 50 | Auto-split into multiple sub-topics, each arranged separately |
| Formation diagram generation fails | Fall back to plain-text formation diagram (ASCII art), prompt user to check Python environment |
| Can't find head coach | Honestly state "this topic has no single core idea", let goalkeeper take leadership role |
| User unsatisfied with formation | Offer 2-3 alternative formations, explain expression differences of each |

## Input Contract

User input format: `[trigger] [topic] [optional parameters]`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| trigger | string | yes | kp11/kpt/kpitch/knowpitch |
| topic | string | yes | Knowledge domain/concept to learn |
| depth | enum | no | quick/standard/deep, default determined by trigger |
| formation | string | no | Force specific formation (4-3-3/4-2-3-1 etc.) |
| language | string | no | Output language, default Chinese |
| --age | int | no | Audience age (5/10/15/18/25+), adjusts language difficulty |
| --job | string | no | Audience job (manager/developer/student), adjusts analogy direction |
| --grade | string | no | Audience grade (5th/college/grad), adjusts professional depth |

**Audience adaptation rules:**
- `--age 5`: Very simple words, toy/cartoon analogies, each sentence ≤10 words
- `--age 10`: Simple vocabulary, school/game analogies, each sentence ≤15 words
- `--age 15`: Everyday vocabulary, life/social analogies, normal sentence structure
- `--age 25+`: Professional vocabulary, workplace/tech analogies, may include terminology
- `--job manager`: Business framework, ROI/risk/decision oriented, avoid code
- `--job developer`: Tech analogies, code/architecture/performance oriented
- `--job student`: Learning analogies, exam/notes/course oriented

**Input examples:**
- `kp11 explain machine learning` (default mode, 4-3-3)
- `kpt what is inflation` (quick mode, compact)
- `kpitch deep dive on React Hooks` (full mode, B team)
- `kp11 neural networks --formation 4-2-3-1` (指定阵型)
- `kp11 database indexing --age 5` (explain to a 5-year-old)
- `kp11 codebase structure --job manager` (explain to manager, business-oriented)
- `kp11 Git merge conflicts --grade 5th` (explain to 5th grader)

## Output Contract

### Output Structure

```
# [Topic] Formation Learning Card (Formation: XXX)
├── Head Coach's Words (1 paragraph ELI5 overview + one-sentence core idea)
├── Formation Diagram (SVG)
├── Starting Lineup
│   ├── Goalkeeper GK (1 player)
│   ├── Defenders (2-4 players)
│   ├── Midfielders (3-5 players)
│   └── Forwards (1-3 players)
├── Bench (0-9 players)
├── Coach Tactics Board
│   ├── Why this formation
│   ├── Ball flow (learning path)
│   ├── Key connections
│   └── Three ways to lose
└── B Team (optional, when >20 knowledge points)
```

### Formation Diagram JSON Schema

```json
{
  "topic": "Topic name (string, required)",
  "formation": "4-3-3 (string, required, options: 4-3-3/4-2-3-1/4-3-2-1/4-4-2/4-5-1/4-1-4-1/3-5-2/3-4-3)",
  "coach": {
    "name": "Head coach name (string, required, = one-sentence core idea)",
    "desc": "One-sentence description (string, optional)"
  },
  "players": [
    {
      "pos": "CB (string, required, position code)",
      "name": "Knowledge point name (string, required)",
      "desc": "One-sentence description (string, optional, for warning stats)"
    }
  ],
  "bench": [
    {
      "name": "Bench knowledge point name (string, required)",
      "desc": "One-sentence description (string, optional)"
    }
  ],
  "flow": ["GK", "CB", "CDM", "AMD", "CF"],
  "b_team": {
    "formation": "3-4-3 (string, optional)",
    "coach": {"name": "B team coach", "desc": "Secondary core idea"},
    "players": [{"pos": "CM", "name": "Extended knowledge point", "desc": "One sentence"}]
  }
}
```

**Position codes:** GK RB CB LB CDM CM CAM AMD LAM RAM RM LM LW RW CF SS

### Boundary Value Output

- **Empty topic:** Prompt "Please provide a topic to learn"
- **Non-knowledge topic:** Prompt "This skill is for knowledge-type topics, suggest other approach"
- **Knowledge points < 3:** Compact formation, clearly mark "topic is narrow, suggest expansion"

## Output Template

Organize final answer following this structure (formation diagram as illustration at the very top):

```
# [Topic] Formation Learning Card (Formation: XXX)

## Head Coach's Words
[1 paragraph ELI5 plain overview + head coach = one-sentence core idea]

## Formation Diagram
[SVG]

## Starting Lineup
### Goalkeeper GK
- [Knowledge point name] one-sentence plain explanation
### Defenders (CB / LB / RB)
- ...
### Midfielders (CDM / CM / AMD)
- ...
### Forwards (CF / SS / LW / RW)
- ...

## Bench
- ...

## Coach Tactics Board
- Why this formation: one sentence
- Ball flow (learning path): GK → CB → CDM → AMD → CF ...
- Key connections: one sentence on relationship between A and B
- Three ways to lose (most easily wrong/misunderstood points): 3 items

## B Team (if applicable)
[B team formation, B team coach = secondary core idea, simplified player cards]
```

## Player Card Template (ELI5)

Each starting player card uniformly has 4 lines (default 1-3 sentences; when user asks for "deep", can expand to 100-300 words):

```
[Position Code | Knowledge Point Name]
- What it is: one plain sentence (like explaining to a 5-year-old)
- Like what: one everyday analogy (toy/kitchen/school/phone...)
- Passes to: which teammates it connects with (dependencies/relationships)
- Why here: one sentence explaining why it's in this position
```

## NEVER List (Don't Do These)

1. **NEVER force-fill 11 players** — When knowledge points are insufficient, leave positions empty, don't stuff edge material into starting lineup.
   - WHY: Filler players dilute core knowledge points, making the formation diagram lose focus.
   - Bad example: Putting edge material like "historical background" into CB core position.

2. **NEVER arrange positions by importance** — Position is determined by "function", not by "importance".
   - WHY: Important knowledge points may be "application" (LW/RW), not "foundation" (CB).
   - Bad example: Putting the most important conclusion at GK (goalkeeper should be most foundational).

3. **NEVER skip formation diagram generation** — Even when pressed for time, generate the SVG.
   - WHY: Formation diagram is this skill's core differentiation; plain-text output is no different from ELI5.

4. **NEVER explain technical terms with technical terms** — Player cards must use plain language.
   - WHY: Violates ELI5 core, zero-background readers can't understand.
   - Bad example: "Gradient descent is a first-order iterative optimization algorithm" (should say "step by step walk downhill, find the lowest point").

5. **NEVER fabricate knowledge points** — Mark uncertain ones as "to be verified", don't make things up.
   - WHY: Wrong knowledge is more harmful than no knowledge.

6. **NEVER treat B team as main** — B team is extension, not a second core.
   - WHY: B team should be "want to learn a bit more" content, can't compete with main team for focus.

7. **NEVER ignore "three ways to lose"** — Tactics board must include common misunderstandings/errors.
   - WHY: Knowing "what's wrong" is as important as knowing "what's right".

8. **NEVER write "I can" / "You can" in description** — Use third person.
   - WHY: First person breaks the Skill's discovery mechanism.

## Complete Examples

### Example 1: Machine Learning (kp11, 4-2-3-1 + B team)

**User input:** `kp11 explain machine learning`

**Head coach:** Machine learning = let the computer find patterns from data on its own, instead of humans writing fixed rules

**Starting lineup (4-2-3-1):**

**Goalkeeper GK | What is "finding patterns from data"**
- What it is: Computer looks at many examples, summarizes patterns on its own, no need for humans to write rules one by one
- Like what: A kid sees many cat photos, learns to recognize cats on their own, no one taught them "cats have four legs + tail + ears"
- Passes to: All players build on this foundation
- Why here: This is the definition of machine learning, everything collapses without it

**Defender CB | Features/Labels/Training set**
- What it is: Features are input data, labels are answers, training set is the question bank for learning
- Like what: Practice questions (features) + answers (labels) + a question bank (training set)
- Passes to: Provides raw material for CDM (gradient descent)
- Why here: No data means no learning, this is the foundation

**Defensive Mid CDM | Gradient Descent**
- What it is: Step by step adjust parameters, making prediction error smaller and smaller
- Like what: Blindfolded going downhill, each step walks in the steepest direction until reaching the valley bottom
- Passes to: Provides optimization direction for CM (loss function)
- Why here: This is the core mechanism of machine learning, all models train with it

**Defensive Mid CDM | Loss Function**
- What it is: Function measuring how wrong predictions are, more wrong = higher score
- Like what: Exam point deduction, wrong one question = deduct one point, goal is deduct to 0
- Passes to: Strongly related to gradient descent, tells it "which direction reduces error"
- Why here: Without loss function, no way to know "did we learn correctly"

**Attacking Mid AMD | Supervised Learning**
- What it is: Show computer "questions + answers", let it learn to derive answers from questions
- Like what: Do practice questions and check answers, after enough practice you can take exams
- Passes to: Provides theoretical foundation for LW (classification/regression)
- Why here: This is the most commonly used machine learning paradigm

**Attacking Mid AMD | Unsupervised Learning**
- What it is: Only show computer "questions" no answers, let it find patterns on its own
- Like what: Give you a pile of fruit, don't tell you classification, you group by color/shape yourself
- Passes to: Provides theoretical foundation for RW (clustering/dimensionality reduction)
- Why here: This is the core idea for discovering hidden patterns

**Attacking Mid AMD | Reinforcement Learning**
- What it is: Computer learns through "trial and error + reward", correct = plus points, wrong = minus points
- Like what: Training a puppy, correct = give snack, wrong = gentle tap
- Passes to: Provides another path for CF (prediction)
- Why here: This is the core idea for decision-type problems

**Left Wing LW | Classification and Regression**
- What it is: Classification = predict category (cat/dog), regression = predict value (house price)
- Like what: Classification = multiple choice, regression = fill-in-the-blank
- Passes to: Provides specific application methods for CF (prediction)
- Why here: This is the most common application scenario for supervised learning

**Right Wing RW | Clustering and Dimensionality Reduction**
- What it is: Clustering = auto-grouping, dimensionality reduction = simplify high-dimensional data
- Like what: Clustering = organizing wardrobe (by season), dimensionality reduction = condense thick book into mind map
- Passes to: Provides unsupervised application for CF (prediction)
- Why here: This is the main application of unsupervised learning

**Center Forward CF | Prediction**
- What it is: Use trained model to make judgments on new data
- Like what: After learning knowledge points, take exam, answer questions you haven't seen before
- Passes to: Final output, goal the whole team serves
- Why here: This is the ultimate purpose of machine learning — prediction

**Bench:**
- Overfitting/underfitting (advanced concepts)
- Regularization (method to prevent overfitting)
- Cross-validation (method to evaluate models)
- Feature engineering (data preprocessing)

**Formation diagram:** [SVG]

**Coach tactics board:**
- Why 4-2-3-1: Machine learning has one clear ultimate goal (prediction), double defensive mids (gradient descent + loss function) are core mechanisms, three attacking mids (three paradigms) feed the goal
- Ball flow (learning path): GK → CB → CDM → AMD → CF
- Key connections: Gradient descent ↔ Loss function (mutually dependent); Supervised learning ↔ Classification/regression (theory→application)
- Three ways to lose:
  1. Overfitting: Model memorizes training data by rote, can't handle new questions (like memorizing answers without understanding)
  2. Underfitting: Model too simple, can't even learn training data (like foundation too weak)
  3. Data leakage: Test data mixed into training set, inflated scores (like peeking at answers before exam)

**B team (3-4-3, advanced applications):**
- B team coach: Machine learning applications in the real world
- Forwards: Computer Vision (CV), Natural Language Processing (NLP), Recommender systems
- Midfield: Deep learning, Ensemble learning, Transfer learning, Online learning
- Defenders: Convolutional Neural Networks (CNN), Recurrent Neural Networks (RNN), Transformer

---

### Example 2: Inflation (kpt, 4-3-3 compact)

**User input:** `kpt explain inflation`

**Head coach:** Inflation = more money, but same amount of stuff, so money is worth less

**Starting lineup (4-3-3, compact 6 players):**

**Goalkeeper GK | Money and Prices**
- What it is: Money is medium of exchange, price is how much stuff is worth
- Like what: Money is tickets, stuff is show, more tickets printed = each ticket worth less
- Passes to: Foundation for all players
- Why here: Can't understand inflation without understanding money

**Defender CB | Demand-Pull**
- What it is: Everyone wants to buy, not enough stuff, prices go up
- Like what: Concert tickets, more people wanting = scalpers mark up price
- Passes to: Provides reason for CM (monetary policy)
- Why here: This is one of the main causes of inflation

**Defensive Mid CDM | Money Multiplier**
- What it is: Banks lend money out, money multiplies (100 deposit can create 500 in loans)
- Like what: Magician's hat, put in 1 rabbit, can pull out 5
- Passes to: Provides mechanism for CM (monetary policy)
- Why here: This is the core mechanism of money creation

**Central Mid CM | Monetary Policy Tools**
- What it is: Central bank controls money supply through rate hikes/cuts, printing/collecting money
- Like what: Water faucet, turn up = more flow (inflation), turn down = less flow (deflation)
- Passes to: Provides means for CF (wallet impact)
- Why here: This is the method to control inflation

**Left Wing LW | Historical Cases**
- What it is: Germany 1923 (wheelbarrow of money for bread), Zimbabwe (trillion-dollar banknotes)
- Like what: Extreme cautionary tales, showing how scary失控 can be
- Passes to: Provides evidence for CF (wallet impact)
- Why here: Cases make abstract concepts concrete

**Center Forward CF | How Inflation Affects Your Wallet**
- What it is: Wages don't rise but prices do, actual purchasing power declines
- Like what: Money in your pocket hasn't changed, but you can buy less
- Passes to: Final conclusion
- Why here: This is what everyone cares about — what does inflation have to do with me

**Formation diagram:** [SVG]

**Coach tactics board:**
- Why 4-3-3: Inflation is balanced topic, cause (demand), mechanism (money multiplier), impact (wallet) all three layers present
- Ball flow: GK → CB → CDM → CM → CF
- Key connections: Money multiplier ↔ Monetary policy (mechanism and means mutually influence)
- Three ways to lose:
  1. Treat inflation as "price increase" (inflation is monetary phenomenon, not all price increases are inflation)
  2. Think rate hikes immediately reduce inflation (monetary policy has 6-18 month lag)
  3. Think wage increases can outrun inflation (wages usually rise slower than prices)

---

### Example 3: Database Indexing (kp11 --age 5, explain to a 5-year-old)

**User input:** `kp11 database indexing --age 5`

**Head coach:** Index = book table of contents, find stuff without flipping page by page

**Starting lineup (4-3-3, compact 5 players, 5-year-old language):**

**Goalkeeper GK | What is an index**
- What it is: Just like the table of contents at the front of a book
- Like what: You want to see the dinosaur page, look at contents and know it's page 50, no need to flip from page 1
- Passes to: Foundation for everyone
- Why here: Can't understand index without understanding contents

**Defender CB | What happens without index**
- What it is: Have to flip page by page, very very slow
- Like what: 1000-page book, finding "Little Red Riding Hood" means flipping 500 pages
- Passes to: Provides contrast for CDM (why fast)
- Why here: Knowing "slow" helps understand "fast"

**Defensive Mid CDM | Why index is fast**
- What it is: Contents tell you which page, flip directly there
- Like what: Playing hide and seek, someone tells you "he's in the cabinet", no need to search everywhere
- Passes to: Provides reason for CF (result)
- Why here: This is the core magic of indexing

**Left Wing LW | Indexes in daily life**
- What it is: Dictionary pinyin index, supermarket category signs
- Like what: Supermarket says "snack area", you walk directly there, no need to check every shelf
- Passes to: Provides examples for CF (result)
- Why here: Examples make abstract concrete

**Center Forward CF | Result**
- What it is: Find stuff fast and accurate
- Like what: With contents, find in 1 second, no need to flip for 10 minutes
- Passes to: Final answer
- Why here: This is the purpose of indexing — speed

**Formation diagram:** [SVG]

**Coach tactics board:**
- Why 4-3-3: Balanced topic, what is it → why → examples → result
- Ball flow: GK → CB → CDM → CF
- Key connections: Without index (slow) ↔ With index (fast) (contrast relationship)
- Three ways to lose:
  1. Think index is "another copy of data" (index is contents, not content)
  2. Think everything needs index (too many contents actually slow things down)
  3. Think index never changes (book adds new content, contents must update too)

## Quality Requirements (Self-Check Before Delivery)

- [ ] Head coach can lead the whole team in one sentence (if can't find, honestly state, don't force)
- [ ] Every starting player satisfies ELI5: zero-background understandable, has analogy, no unexplained terminology
- [ ] Position allocation follows positions.md function logic, not forced by importance
- [ ] When knowledge points > 20, B team enabled; when ≤ 20, didn't force-fill 11 players
- [ ] Knowledge points from user input or verified sources, not fabricated; uncertain marked "to be verified"
- [ ] Formation diagram generated and delivered, body structure matches output template
- [ ] When user asks for deep, key player cards have enough detail not just one sentence
- [ ] Tactics board includes "three ways to lose" (common misunderstandings/errors)
- [ ] No violation of any item in NEVER list
- [ ] Audience parameters (--age/--job/--grade) correctly applied to language difficulty and analogy direction
