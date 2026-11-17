# Anti-AI patterns: a diagnostic catalog

This document extends the short pattern list in `SKILL.md`. The goal is **not** to make text quirky or to bypass detectors. The goal is to give the host model a precise diagnosis of what makes a draft read as generic AI output, and a concrete fix for each pattern.

Use this as a *diagnostic catalog*, not a rules engine. The final rewrite must be done with editorial judgment, not by deleting the matched substring.

## Sources and lineage

This catalog draws on three sources, layered:

- **[Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)** is the primary lexical and phrasal reference. It catalogs the words, phrases, and structural habits that WikiProject AI Cleanup uses to identify LLM-generated text. Most of the lexical and phrasal entries below are organized around this list, sometimes merged, sometimes split, sometimes extended. Wikipedia is the authoritative substrate — the patterns it lists are community-maintained, regularly updated, and tied to the editor workflow that actually removes AI-written content from a high-stakes surface. When this catalog diverges from the Wikipedia list (by adding, merging, or splitting a category), the divergence is called out in the entry, not silently introduced.
- **[blader/humanizer](https://github.com/blader/humanizer)** is the curation and presentation layer. It turns the Wikipedia list into a 30-category rewriting checklist, with the principle "rewrite, don't delete" and a hard default on em dashes and decorative formatting. We borrow the catalog organization and the hard-default philosophy for em dashes and formatting. We *do not* borrow the "must always include editing report" stance as a hard rule, because the report is appropriate when the user asks, not as a default output.
- **`humanize-skill` adds two layers that the Wikipedia list does not cover**:
  - **Structural and formatting layer** (section 4 below) — heading cadence, bullet-list overuse, intro-body-summary sandwich, decorative formatting, TL;DR-before-content.
  - **Cognitive layer** (section 5 below) — uniform confidence, no stated limits, missing first person, hidden reasoning, generic examples, conflict avoidance, hedging without commitment.

The cognitive layer is the one detector-style tools are most sensitive to. Removing only the Wikipedia-level lexical tells (the "em dashes and contractions" approach) does not get you close to human-looking prose on a high-stakes surface. Treat the structural and cognitive layers as equally important.

## Wikipedia catalog index

The pattern names below are the canonical labels used by [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) and WikiProject AI Cleanup. Each Wikipedia label is mapped to the local section that diagnoses and fixes it. Use this index as the authoritative cross-reference: when the two diverge, the local section wins for the rewrite, the Wikipedia entry wins for the underlying category. Anchors link to the Wikipedia page sections where the labels are defined; if a label has been merged or renamed upstream, the Wikipedia page is the source of truth, and this catalog follows it.

### Lexical tells (words and phrases)

| Wikipedia label | Local section |
|---|---|
| [Significance inflation](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Significance_inflation) — "pivotal", "testament", "landmark", "watershed", "paradigm shift" | [§1.1](#11-significance-inflation) |
| [Promotional vocabulary](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Promotional_vocabulary) — "groundbreaking", "revolutionary", "cutting-edge", "seamless", "robust" | [§1.2](#12-promotional-vocabulary) |
| [Vague attribution](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Vague_attribution) — "experts say", "studies show", "widely recognized" | [§1.3](#13-vague-authority) |
| [AI tells: approval and enthusiasm words](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Communication_tells) — "thrilled", "excited to announce", "proud to share" | [§1.4](#14-approval-and-enthusiasm-words) |
| [Inflated symbolism or hedging](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Inflated_symbolism) — synonym cycling and "lexical smoothing" | [§1.5](#15-lexical-smoothing) |
| [Generic intensifiers](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Generic_intensifiers) — "very", "really", "incredibly" | [§1.6](#16-generic-intensifiers) |
| [Corporate / consulting-deck phrases](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Sycophantic_/_corporate_language) — "delve into", "navigate the landscape", "unlock potential" | [§1.7](#17-corporate-and-product-noun-drift) |

### Communication and chatbot tells

| Wikipedia label | Local section |
|---|---|
| [Chatbot residue](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Communication_tells) — "Great question!", "I hope this helps", "Feel free to" | [§2.8](#28-chatbot-residue) |
| [Filler transitions](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Communication_tells) — "In order to", "Due to the fact that", "It is worth noting that" | [§2.9](#29-filler-transitions) |
| [Knowledge-cutoff disclaimers](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Communication_tells) — "As of my last update", "as an AI model" | not in catalog — surface-dependent; remove when leaking through, do not introduce |

### Phrasal and structural patterns

| Wikipedia label | Local section |
|---|---|
| [Negative parallelism](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Phrasal_patterns) — "not just X, but Y", "more than just X — it is Y" | [§2.1](#21-negative-parallelism) |
| [Rule of three / forced trios](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Rule_of_three) — "innovative, scalable, and seamless" | [§2.2](#22-forced-trios), [§3.3](#33-the-rule-of-three-rhythm) |
| [Universal-audience framing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Phrasal_patterns) — "Whether you are X or Y", "for teams of 5 or 50,000" | [§2.3](#23-the-whether-you-are-x-or-y-opener), [§5.1](#51-universal-audience-framing) |
| [False ranges](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Phrasal_patterns) — "from brainstorming to shipping" | [§2.4](#24-false-ranges) |
| [Throat-clearing openers](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Phrasal_patterns) — "In today's rapidly evolving landscape", "In an era defined by" | [§2.5](#25-the-in-todays-world-opener) |
| [Copula avoidance](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Phrasal_patterns) — "serves as", "stands as", "boasts" | [§2.6](#26-copula-avoidance) |
| [Superficial participles](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Phrasal_patterns) — "showcasing", "highlighting", "underscoring" | [§2.7](#27-superficial-participles) |
| [Generic conclusions](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Phrasal_patterns) — "In conclusion", "The future looks bright", "Exciting times lie ahead" | [§2.10](#210-generic-conclusions) |

### Syntactic tells (sentence shape)

| Wikipedia label | Local section |
|---|---|
| [Em dash overuse](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Syntactic_tells) | [§3.2](#32-em-dash-dependency) — hard default with voice-profile exception |
| [Balanced parallelism](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Syntactic_tells) — "we listen, we learn, we deliver" | [§3.1](#31-balanced-parallelism-overuse) |
| [Uniform sentence length](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Syntactic_tells) | [§3.6](#36-uniform-sentence-length) |
| [Nominalization](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Syntactic_tells) — verb-to-noun drift | [§3.4](#34-nominalization) |
| [Perfectly clean sentence boundaries](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Syntactic_tells) — no fragments, no run-ons | [§3.5](#35-perfectly-clean-sentence-boundaries) |

### Structural and cognitive layers (added by humanize-skill)

These layers are *not* on the Wikipedia list. Detector-style tools are most sensitive to them. They are listed here so the catalog index is complete, but they are flagged as additions so a Wikipedia reader does not assume they are upstream content.

| Local label | Where it lives |
|---|---|
| H2-every-few-paragraphs, bullet-list as default, intro-body-summary sandwich, decorative formatting, TL;DR-before-content | [§4](#4-structural-layer-paragraph-and-section-shape) |
| Universal-audience framing (cognitive), uniform confidence, no stated limits, missing first person, no visible thinking, generic examples, conflict avoidance, hedging without commitment | [§5](#5-cognitive-layer-the-deepest-tell) |

If a pattern appears in the Wikipedia list but is not in this index, treat the Wikipedia entry as authoritative and add the gap here in a follow-up revision. The index is meant to be exhaustive, not selective.

## How to read this catalog

Each entry has four parts:

- **Pattern** — what the AI-looking version looks like.
- **Why it reads as AI** — the underlying tell, not just the surface symptom.
- **Fix** — what to actually do, with the depth the rewrite needs.
- **Caution** — when to keep the pattern anyway (formal/legal/medical/reference writing, or when the user explicitly wants a neutral register).

When a pattern is removed, the *idea* it was carrying still needs to land. Do not leave formula fragments behind.

---

## 1. Lexical layer (word choice)

AI text overuses a small cluster of prestige and approval words. They are not wrong in isolation. They become AI tells through **density and clustering**.

### 1.1 Significance inflation

- **Pattern**: "pivotal", "testament", "landmark", "watershed", "broader landscape", "paradigm shift", "game-changer", "cornerstone", "crucial juncture", "defining moment".
- **Why**: these words replace the actual claim. The writer is not describing *what* changed; they are borrowing authority from a stock phrase.
- **Fix**: state the change in plain terms. "We cut report build time from 9 minutes to 40 seconds" beats "a pivotal milestone in our data tooling journey." If no concrete change exists, the sentence should be cut.
- **Caution**: in retrospective history writing, "landmark" and "watershed" can be used sparingly with a specific referent. Do not blanket-delete.

### 1.2 Promotional vocabulary

- **Pattern**: "groundbreaking", "revolutionary", "cutting-edge", "best-in-class", "industry-leading", "next-generation", "seamless", "robust", "powerful", "scalable", "world-class", "must-have".
- **Why**: it sounds like a brochure, not a person. AI has no business being excited. The words also cluster — when you see two in one paragraph, the whole paragraph is suspect.
- **Fix**: replace the adjective with the *behavior*. "Loads in 200ms" is more credible than "blazing fast." If the product really is faster, the number is the proof.
- **Caution**: marketing copy aimed at buyers may legitimately use these. The skill should default to dropping them, but accept them when the surface and audience require it.

### 1.3 Vague authority

- **Pattern**: "experts say", "studies show", "industry reports suggest", "many believe", "it is widely recognized", "observers note".
- **Why**: this is a placeholder where a citation should be. AI uses it because the model cannot name a real source. The reader is left to trust the writer's word, and the writer is hiding.
- **Fix**: name the source, or cut the attribution, or mark `needs_evidence`. "A 2024 Stanford HAI report found..." or "this is my read, not a survey."
- **Caution**: in op-eds and personal essays, "I think" and "in my experience" are honest, not vague. Do not flatten voice into over-citation.

### 1.4 Approval and enthusiasm words

- **Pattern**: "thrilled", "excited to announce", "proud to share", "delighted", "honored", "passionate about".
- **Why**: AI does not have feelings. "Thrilled to announce" is the default opening for any release, which is exactly why it reads as template. Genuine enthusiasm is concrete (the specific thing that surprised you, the moment you saw it work).
- **Fix**: replace with the actual thing. "I have been wanting this for two years" or "I was not sure it would work, and it does" beats "thrilled to share."
- **Caution**: if the user actually is excited, they will say so in their own way. Match their diction; do not impose a flat tone.

### 1.5 Lexical smoothing

- **Pattern**: replacing a plain word with a fancier synonym, often within the same paragraph. "Tool, platform, solution, system, ecosystem" in one piece. "Use, leverage, utilize, harness, employ" in another.
- **Why**: synonym cycling is a classic AI habit. Humans repeat the clearest word. AI diversifies vocabulary as a quality signal.
- **Fix**: pick the most concrete noun and stick with it. Repeat it. Repetition is human.
- **Caution**: technical writing often requires term variation to avoid ambiguity. Distinguish "lexical smoothing for show" from "lexical precision for clarity."

### 1.6 Generic intensifiers

- **Pattern**: "very", "really", "incredibly", "extremely", "absolutely", "truly", "deeply". Often used in clusters with vague nouns.
- **Why**: intensifiers amplify nothing. "Very important" is no more specific than "important." They are also how AI papers over weak claims.
- **Fix**: replace with the specific scale or reason. "Important because it ships to 20,000 customers tomorrow" beats "very important."

### 1.7 Corporate and product-noun drift

- **Pattern**: "delve into", "navigate the landscape", "embark on a journey", "unlock potential", "drive value", "move the needle", "synergy", "leverage", "optimize for" (when "improve" fits), "robust solution" (when "tool" fits).
- **Why**: these are consulting-deck phrases. They promise analysis without doing any.
- **Fix**: name the action. "We are reducing deploy time" beats "we are optimizing for developer velocity."

---

## 2. Phrasal layer (idioms and templates)

Some patterns are entire phrases, not single words. They are the high-signal AI tells because they are *memorized openings and closers*.

### 2.1 Negative parallelism

- **Pattern**: "not just X, but Y", "more than just X — it is Y", "X is not only Y, it is Z", "going beyond X, it is Y".
- **Why**: the structure claims a reframe but the reframe is generic. "Not just a tool, but a complete ecosystem" is filler dressed as insight.
- **Fix**: state the actual point. If X and Y differ, say how. If they do not differ, the sentence is decoration.
- **Caution**: the structure is not always bad. "Not just fast, but predictable" makes a real claim. Keep the ones that actually contrast.

### 2.2 Forced trios

- **Pattern**: lists of three adjectives or items that sound balanced but are vague. "Innovative, scalable, and seamless." "Fast, reliable, and secure." "Visionary, bold, and principled."
- **Why**: trios look polished. They also let the writer avoid picking the one attribute that actually matters.
- **Fix**: keep the attribute that is real and load-bearing. Cut the rest. "Fast" is a claim. "Fast, reliable, and secure" is a poster.
- **Caution**: trios are natural in some surfaces (product headlines, signature lines, award blurbs). Use judgment.

### 2.3 The "Whether you are X or Y" opener

- **Pattern**: "Whether you are a startup founder or an enterprise architect", "From beginners to seasoned professionals", "For teams of 5 or 50,000".
- **Why**: the universal-audience claim is the AI substitute for choosing an audience. It is also a sales pattern. The writer never says who they are actually writing to.
- **Fix**: pick the audience. "If you maintain a Linux server with under 1GB of RAM" is sharper than "for any developer, anywhere."

### 2.4 False ranges

- **Pattern**: "from X to Y" without a real scale. "From brainstorming to shipping." "From ideation to deployment." "From individual contributors to enterprise teams."
- **Why**: the range looks like coverage. Often X and Y are unrelated ends, not a continuum.
- **Fix**: list the actual cases. If the range is real ("from 10MB to 10TB"), keep it and add the unit.

### 2.5 The "in today's world" opener

- **Pattern**: "In today's rapidly evolving landscape", "In an era defined by", "In the age of", "As we navigate the modern", "In a world where".
- **Why**: this is throat-clearing. The reader already knows what era it is.
- **Fix**: start with the actual subject. Cut the opener entirely.

### 2.6 Copula avoidance

- **Pattern**: "serves as", "stands as", "acts as", "functions as", "boasts", "features" used where "is" or "has" would do. "The library serves as a wrapper around the API" instead of "The library wraps the API."
- **Why**: AI learned that "is" is too plain. The longer form is borrowed from formal writing, used as a default.
- **Fix**: prefer the simple copula. "Is" and "has" are usually the strongest verbs.
- **Caution**: in encyclopedic and reference writing, "serves as" is sometimes the correct technical term. Do not flatten register where neutral precision is the goal.

### 2.7 Superficial participles

- **Pattern**: "showcasing", "highlighting", "underscoring", "reflecting", "emphasizing", "exemplifying" used at the end of a clause as decoration. "The new dashboard, showcasing real-time metrics, helps teams..."
- **Why**: these are present participles added to give the impression of analysis. They do not perform the analysis.
- **Fix**: cut the participle, or replace it with the actual cause. If "showcasing real-time metrics" means "the dashboard shows you what is happening now", say that. If it does not add new information, drop it.

### 2.8 Chatbot residue

- **Pattern**: "Great question!", "I hope this helps", "Let me know if you have any other questions", "Feel free to", "Don't hesitate to", "Happy to help", "Of course!".
- **Why**: this is the conversational layer of chat assistants, leaking into prose. It is the highest-signal AI tell in customer-facing and support contexts.
- **Fix**: cut the residue. Replace it with the actual response, which should be a direct answer.
- **Caution**: in real conversational contexts (chat, live reply), a brief acknowledgement is fine. The problem is the formula, not the existence of warmth.

### 2.9 Filler transitions

- **Pattern**: "In order to" (use "to"), "Due to the fact that" (use "because"), "At this point in time" (use "now"), "It is worth noting that" (cut), "It is important to remember" (cut), "Having said that" (cut or replace with the actual pivot).
- **Why**: these phrases fill space without adding information. They are a model habit when the next sentence is the same length as the first.

### 2.10 Generic conclusions

- **Pattern**: "In conclusion", "To sum up", "The future looks bright", "Exciting times lie ahead", "Only time will tell", "There is still much work to be done".
- **Why**: these are exit ramps. They signal the writer is done, not that the reader has learned anything.
- **Fix**: end with the specific implication, the open question, or the next concrete step. The conclusion should be a *move*, not a *farewell*.
- **Caution**: long-form academic writing uses "In conclusion" legitimately. In short web and email contexts, it is a tell.

---

## 3. Syntactic layer (sentence shape)

These patterns are about how AI builds sentences, not which words it picks.

### 3.1 Balanced parallelism overuse

- **Pattern**: two or three clauses of near-identical length and structure, often joined with commas or semicolons. "It is fast, it is reliable, and it is easy to use." "We listen, we learn, we deliver."
- **Why**: balanced structure is rhetorically clean, but real prose is messier. AI defaults to parallel form for emphasis; humans reserve it for genuine lists.
- **Fix**: vary the structure. If two of the three points are minor, cut them.

### 3.2 Em dash dependency

This is a **hard-default** pattern. The default behavior of the skill is to remove em dashes from the rewrite. The fix is *not* "use em dashes more sparingly"; the fix is "use a different construction".

- **Pattern**: long parenthetical asides joined with em dashes, often twice per paragraph. "The system — which was built in 2019 and serves 20,000 users — has remained stable."
- **Why**: em dashes are a clean way to inject clauses. AI overuses them because the resulting sentence is grammatically valid and looks considered. They also make the text look more "writerly" than it is. The frequency, not the existence, is the tell — a paragraph with one em dash is fine; a paragraph with three is not.
- **Fix (default)**: split into separate sentences, or use parentheses, or use commas if the aside is short, or restructure the sentence to remove the parenthetical. A paragraph with no em dashes is not worse writing; in many cases it is better.
- **Fix (voice-profile exception)**: if the user's samples show a stable em-dash habit (more than 1 per paragraph on average, sustained across the corpus), the rewrite can preserve the user's habit. This is one of the few patterns where the voice profile overrides the default. Mark the exception in `notes.md` so the user can see the call.
- **Caution**: in literary and essayistic prose by named human authors, em dashes are a natural rhythm tool. The skill should not flatten good prose just because em dashes appear. The default is for *AI-looking* drafts, not for established human writing the user is asking to copy-edit.

### 3.3 The rule-of-three rhythm

- **Pattern**: every list is three items. Every paragraph has three points. Every section has three subsections.
- **Why**: three is the AI default for "complete". It is also where human writing uses two, or four, or five.
- **Fix**: let the number follow the content. Two strong points beats three padded ones.

### 3.4 Nominalization

- **Pattern**: turning verbs into nouns. "We performed an analysis of" instead of "we analyzed". "Make a decision about" instead of "decide on". "Conduct a review of" instead of "review".
- **Why**: nominalization is a habit of formal and bureaucratic writing. AI defaults to it because it sounds more "official".
- **Fix**: prefer the verb. Decided. Analyzed. Reviewed.

### 3.5 Perfectly clean sentence boundaries

- **Pattern**: every sentence is grammatically complete, with a clear subject and verb. No fragments, no trailing clauses, no rhetorical asides.
- **Why**: AI rarely produces fragments or run-ons. Humans do, especially in casual registers.
- **Fix**: allow the user's natural rhythm. If the user is fragment-heavy in samples, the rewrite can be too. Do not over-correct into uniformity.
- **Caution**: technical and legal writing should stay clean. Match the surface.

### 3.6 Uniform sentence length

- **Pattern**: most sentences are 15-25 words, with little variation.
- **Why**: this is the model's "safe" length. Real prose has 6-word punches next to 35-word explanations. The absence of variation is itself a tell.
- **Fix (default)**: vary the length where it serves emphasis. A short sentence after a long one is a real human rhythm. A fragment after a long sentence is a real human rhythm. A list of three with one short item is a real human rhythm.
- **Fix (rhythm construction)**:
  - *The long-then-short move*: load a complex idea into a long sentence, then land the conclusion in a short one. "The model reduces p99 latency from 800ms to 95ms by replacing JSON parsing with protobuf. It is faster, and the schema catches the typos we used to miss." The contrast is the rhythm.
  - *The fragment-as-pause*: a one-word or two-word sentence at a point of emphasis. "Fast. Cheap. The third thing does not exist." Use sparingly — one per page, not one per paragraph.
  - *The list of three with variation*: most lists are three items, but a list of two is more emphatic, and a list of four or five loses rhythm. Match the number to the content.
  - *The opening variation*: not every paragraph opens with the same grammatical role. A subject-verb opening, a dependent clause, a question, a sentence fragment, an interjection — the openings should rotate.
- **Caution**: do not randomize rhythm for its own sake. Variation should follow meaning, not a pattern of "long, short, long, short." Variation in the service of emphasis is craft; variation as a way to game a detector is performance.
- **Voice-profile check**: if the user writes long sentences (engineering blog, academic prose), do not chop them short in the name of "rhythm". Match the user's natural length first, then introduce variation within that range.

---

## 4. Structural layer (paragraph and section shape)

### 4.1 The H2-every-few-paragraphs habit

- **Pattern**: short documents with a heading every 2-3 paragraphs, even when the content does not warrant a new section.
- **Why**: heading-heavy formatting mimics "well-structured" documents. It also hides that each section is thin.
- **Fix**: use headings only at real transitions. Long sections under one heading are fine when the topic holds.

### 4.2 The bullet list as default

- **Pattern**: turning every enumeration into a bulleted list, even when prose would be clearer.
- **Why**: lists are scannable and look polished. They also let the writer avoid connecting the items.
- **Fix**: keep lists for genuinely parallel items. Use prose when the items have a narrative or when the connections matter.

### 4.3 The "intro, body, summary" sandwich

- **Pattern**: every piece starts with a thesis paragraph, has middle sections, and ends with a summary. Even short pieces.
- **Why**: AI defaults to essay structure regardless of length. A 200-word note gets the same scaffold as a 2000-word essay.
- **Fix**: match the structure to the surface. A tweet does not need an intro. A status update does not need a summary.

### 4.4 Decorative formatting

- **Pattern**: excessive bold, emojis, Title Case headings, ALL CAPS for emphasis, multiple exclamation marks.
- **Why**: formatting is another surface signal AI uses to imply energy. Real writers use bold sparingly.
- **Fix**: plain formatting by default. Use bold only when the reader would otherwise miss the key term.

### 4.5 The TL;DR before the content

- **Pattern**: "TL;DR" or "Summary:" block at the top, followed by the same content in longer form.
- **Why**: AI often produces a summary, then explains what it just said. The summary is the only useful part.
- **Fix**: if a summary is needed, lead with the actual content. Do not duplicate.

---

## 5. Cognitive layer (the deepest tell)

This is the layer that detector-style signals actually pick up most. It is not about words or syntax. It is about how the text *thinks*.

### 5.1 Universal-audience framing

- **Pattern**: claims that address everyone and therefore no one in particular. "Anyone can benefit from this." "Everyone has felt this way."
- **Why**: AI is trained to be safe for all audiences. Real writing addresses a real reader.
- **Fix**: name the reader, or the moment, or the situation. Specificity is the cure.

### 5.2 Uniform confidence

- **Pattern**: every claim is stated with the same level of confidence, regardless of how solid the evidence is.
- **Why**: AI cannot easily model uncertainty. "This will transform the industry" and "this is one approach among several" come out the same way.
- **Fix**: vary the confidence to match the evidence. "X" for supported claims. "Probably X" or "I think X" for personal reads. "X, though the evidence is mixed" for contested claims. The variation is honest.

### 5.3 No stated limits

- **Pattern**: solutions without tradeoffs. Tools that "work for any team size, any stack, any use case".
- **Why**: AI defaults to completeness claims because it does not know the actual limits. Real products have limits.
- **Fix**: state the limit. "Best for teams under 50." "Does not support Windows yet." "Tradeoff: slower cold start."

### 5.4 Missing "I" and missing "we"

- **Pattern**: writing that avoids first person even when the author has a point of view. "It is believed that" instead of "I think". "It can be argued" instead of "I argue".
- **Why**: AI defaults to impersonal voice because impersonality feels safe. It also feels like nobody.
- **Fix**: if the user has a stance, let it appear. "I think", "in my read", "for our team" are honest and human.

### 5.5 No visible thinking

- **Pattern**: the text jumps from topic A to topic B without showing the link. The reader has to infer the connection.
- **Why**: AI writes "topic A. Topic B. Topic C." with the relations hidden. Real writers show their work: "this matters because", "the catch is", "what changed is", "I had assumed X, then I saw Y".
- **Fix**: make the connections visible. A good test: if you remove all the connective phrases, does the document still make sense? If yes, you had no real argument; if no, the connectives were doing the work — keep them visible, do not hide them.

### 5.6 Generic examples

- **Pattern**: "For example, a small startup" with no name, no scale, no specifics. "Imagine a team of five engineers".
- **Why**: hypothetical examples are AI's substitute for real ones. The reader cannot verify or relate to a vague "startup".
- **Fix**: use real examples from the user's domain, or admit the example is hypothetical and give it specific dimensions. "A team of 5 engineers in fintech, building for 6 months" is closer to real.

### 5.7 Conflict avoidance

- **Pattern**: prose that refuses to disagree. "Some say X, others say Y" without taking a position.
- **Why**: AI is trained to be balanced. Real writing often has a side.
- **Fix**: if the user has a position, state it. If not, mark the question as open. Balance is not the same as neutrality of thought.

### 5.8 Hedging without commitment

- **Pattern**: "might", "could", "potentially" stacked across a sentence, with no clear claim at the end.
- **Why**: AI hedges to seem careful. Too much hedging produces a sentence that says nothing.
- **Fix**: hedge on the parts that are genuinely uncertain, commit on the parts that are not. One hedge per claim is usually enough.

---

## What this catalog is not

- It is not a checklist to apply mechanically. Match the patterns to the surface, the audience, and the user's actual voice.
- It is not a detector-evasion tool. Removing these patterns improves writing quality, and high-quality writing is harder to misclassify, but no pattern removal guarantees any specific detector outcome.
- It is not a license to inject quirks. Detecting AI patterns is not the same as making prose "feel" different. Real human voice is consistent, specific, and grounded — not random.

The catalog is a *diagnosis* tool. The *cure* is editorial judgment applied to the specific draft, the specific user, and the specific surface.
