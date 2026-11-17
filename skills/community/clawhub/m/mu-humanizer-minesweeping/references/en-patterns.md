# English AI Patterns — Quick Reference

Use for English writing quality editing. Same structure: disposition / trigger / exclude / risk / fix. `rewrite` may offer an edit, `conditional` needs its stated premise, and `review_only` only flags a concern; see `edit-policy.md`. Fixes must only use information already present in the source; never add facts, names, dates, numbers, examples, or citations.

---

## 🔴 Critical

### 1. Chatbot Artifacts (delete entirely)
**Trigger:** I hope this helps / Let me know if / Great question / Certainly! / Happy to help / As an AI / Here's a
**Exclude:** Actual chat transcripts, chatbot UI copy
**Risk:** LOW
**Fix:** Delete the artifact while preserving any adjacent source information.

### 2. Significance Inflation
**Disposition:** conditional
**Trigger:** stands as a testament / serves as a reminder / pivotal moment / evolving landscape / indelible mark / rich tapestry / setting the stage
**Exclude:** Actual historical turning points with evidence
**Risk:** HIGH — don't shrink genuinely important events or add concrete details absent from the source
**Fix:** If the source itself supplies concrete facts, remove only redundant inflation while retaining its claim strength. If it supplies no such facts, delete a purely empty flourish only when the remaining sentence is complete; otherwise do not rewrite and raise an editorial note.

### 3. Copula Avoidance
**Trigger:** serves as a/the → is / stands as → is / boasts a → has / features a → has / offers a → has
**Exclude:** When the elaborate verb genuinely adds meaning
**Risk:** LOW
**Fix:** Use is/are/has directly

---

## 🟠 High

### 4. AI Vocabulary (replace with simpler words)
**Trigger:** Abstract vocabulary used repeatedly where a plain word would preserve the source meaning.
**Exclude:** Terms used as official names, quoted text, or terms whose precise meaning would be narrowed by replacement.
**Risk:** LOW — replace only when the alternative preserves the original claim's strength and scope.
**Fix:** Use the following substitutions only when they fit the source context and do not add information.

| AI Word | Replace With |
|---------|-------------|
| additionally | also / and, if the link is needed |
| crucial | retain only when the source supports the strength; otherwise delete the unsupported modifier or do not rewrite and raise an editorial note |
| delve | examine / discuss, when the context fits |
| enhance | improve, when the change is concrete |
| foster | support |
| garner | get / earn |
| intricate | complex |
| landscape (abstract) | field / area |
| leverage | use |
| moreover/furthermore | also |
| multifaceted | complex |
| nuanced | subtle |
| paradigm | model / approach |
| pivotal | key |
| realm | area |
| showcase | show |
| synergy | cooperation |
| tapestry | mix |
| testament | proof |
| underscore | show |

### 5. Filler Phrases
**Trigger:** A phrase adds little meaning and can be shortened or removed without losing source information.
**Exclude:** Legal, technical, or quoted wording where the phrase carries a precise function.
**Risk:** LOW — preserve any qualification, causal relation, or comparison carried by the phrase.
**Fix:** Apply the context-appropriate operation below; do not add facts or claims.

| Filler | Fix |
|--------|-----|
| in order to | to |
| due to the fact that | because |
| at this point in time | now |
| has the ability to | can |
| it is important to note that | delete |
| it should be noted that | delete |
| Additionally, / Furthermore, | delete or "also" |
| In conclusion, / Overall, | delete |
| utilize | use |
| facilitate | help |
| implement | add |
| prioritize | focus on |
| optimize | improve |
| streamline | simplify |

### 6. Vague Attributions
**Disposition:** review_only
**Trigger:** experts argue / industry reports / widely regarded / it is widely believed / many believe / according to experts
**Exclude:** When actual source is named in same paragraph
**Risk:** HIGH — do not invent or add a source that isn't already in the text
**Fix:** Keep the sentence unchanged and raise it in a separate editorial note asking the user to supply the source, or delete the unsupported claim. Never add a citation, name, or source inside the rewrite itself.

---

## 🟡 Medium

### 7. Promotional Language
**Trigger:** vibrant / groundbreaking / renowned / breathtaking / bustling / game-changing / cutting-edge / world-class / revolutionary
**Exclude:** Marketing copy where promotional tone is intentional
**Risk:** LOW
**Fix:** Replace with a plain description using only details already stated in the source, or delete

### 8. Rule of Three
**Disposition:** conditional
**Trigger:** "innovate, inspire, and transform" / "not only X, but also Y" patterns used decoratively
**Exclude:** Genuinely three distinct items
**Risk:** LOW
**Fix:** Remove only decorative or duplicative items. If all items carry distinct source information, do not rewrite; record the pattern as an untreated signal rather than forcing a shorter list.

### 9. Em Dash Overuse
**Trigger:** 3+ em dashes in a short piece, or em dash used as default connective
**Exclude:** Single em dash creating real emphasis
**Risk:** LOW
**Fix:** Vary with commas, colons, conjunctions, periods. Not every dash needs replacing

---

## ⚪ Style Signals

- Excessive bold in body text
- Every sentence same length
- Perfect paragraph structure (never varies)
- Negative parallelism crutch
- Curly quotes in technical contexts (copy-paste artifact)
