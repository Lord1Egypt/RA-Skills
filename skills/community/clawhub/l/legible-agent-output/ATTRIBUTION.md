# Third-Party Attributions

This skill synthesizes ideas from public UX-research and agent-design literature. The
implementation, the 7 laws, the 6-category taxonomy, the 30+ before/after transformations,
and the eval-loop protocol are original work licensed under MIT (see `LICENSE`). The
underlying concepts and the cited claims are attributed below.

The skill name `legible-agent-output` is original. The skill's own descriptive terms —
*plain-language action preview* and *legible agent state* — are **synthesized labels** for
naming convenience inside this skill. The literature uses different terms for the same
underlying ideas; we picked one label per concept to keep references stable inside the skill.
See `references/articles-sources.md` for the full cross-reference.

## Primary sources

The skill draws on six published articles. Each is cited verbatim in `references/articles-sources.md`
with a direct quote and a link. The high-level attribution:

**1. Smashing Magazine** — *Designing For Agentic AI: Practical UX Patterns For Control, Consent, And Accountability* (Feb 2026, Victor Yocco)
- Source of the **Intent Preview** pattern. The article's worked example
  *"Executing API call to cancel_booking(id: 4A7B)" → "Cancel flight AA123 to San Francisco"*
  is the direct analog of Law #1 (title first, code second) and Law #3 (translate every error).
- This skill's term *plain-language action preview* synthesizes the article's "Intent Preview".

**2. Hatchworks** — *Agent UX Patterns: Chat-First UX Fails. Use These Patterns Instead* (Mar 2026, Andy Smith)
- Source of the two failure modes *Invisible actions* and *Unclear state*. The article's
  direct quote *"users don't trust the agent — not because it's wrong, but because they
  can't see what it's doing"* anchors the anti-pattern section.
- This skill's term *legible agent state* synthesizes those two failure-mode labels.
- Pattern #1 (Expectation Management) and Pattern #3 (Failing Gracefully) directly ground
  Laws #1, #3, and #4.

**3. Exalt Studio** — *UI/UX Design for AI Startups: Best Practices for Agents, Tools & Interfaces* (Jun 2026)
- Source of the *contextual + concrete* framing for Law #2. Direct quotes used as anchors:
  *"Avoid overwhelming users with technical jargon"* and *"This result is based on your past searches"*.

**4. boost.ai** — *Common Conversational AI Mistakes (and How to Avoid Them)* (Jun 2025)
- Source of the *context retention* and *personalization* principles that reinforce Law #2.
  The high-quality vs poor-quality response side-by-side examples in the article are
  structurally identical to this skill's before/after transformations.

**5. Orange Loops** — *Designing Trustworthy AI Assistants: 9 Simple UX Patterns That Make a Big Difference* (Jul 2025, Juan José Reyes)
- Source of the *trust* framing. Direct quote used: *"expectation management is the most
  important UX pattern. When users know what an AI can and can't do, they trust it more,
  use it better, and stick with it longer."* This grounds the workflow's Phase 4
  (the optional parenthetical ID for technical users).

**6. Medium Bootcamp** — *What UX Designers Should Understand About AI Agents* (Dec 2025, Yanshi Tyagi)
- Source of the principle *"every status message, every cycle report, every plan summary
  ends up in front of a human eventually"*, which is the foundation of the anti-patterns
  section.

A seventh source from an earlier draft of this skill (LogRocket, *Overusing AI is ruining UX*)
was removed during the 2026-06-30 audit because the article does not actually make the
attributed claim. See `references/articles-sources.md` §Changelog for the full audit trail.

## What this skill is NOT derived from

- No text was copied verbatim from any specific article, blog post, book, or video.
- The 30+ before/after examples in `examples/before-after.md` are original constructions
  illustrating the 6-category taxonomy, not reproductions of any specific source.
- The 7 laws, the eval loop, and the quality checklist are the original synthesis of the
  author (Monika Zapisek).
- No proprietary consulting framework material (no BCG/McKinsey/Gartner decks, no paid
  courseware, no internal corporate style guides) is reproduced or closely paraphrased.
- The example error codes used in this skill (A127, T-B42, ENOENT, EBADF) are common
  placeholders from open-source documentation, not specific to any product.

## How to attribute when you remix

If you build a derivative skill, fork this one, or adapt the 7 laws for your own
use case, please keep:

1. This `ATTRIBUTION.md` file (or its equivalent in your derivative)
2. The MIT `LICENSE` from the parent project
3. A visible link back to the canonical source
   (`https://github.com/monikazapisekstudio/design-engineering-playbook/tree/main/skills/legible-agent-output`)
   somewhere in your derived work

That keeps the chain of credit intact without burdening downstream users.

## Note on terminology synthesis

This skill's two descriptive terms — *plain-language action preview* and *legible agent state* —
are **synthesized labels** coined for naming convenience inside this skill. They do not appear
verbatim in the source literature. The original literature uses:

- *Intent Preview* (Smashing Magazine) — what this skill calls *plain-language action preview*
- *Invisible actions* / *Unclear state* (Hatchworks) — what this skill calls *legible agent state*

The synthesized labels are not misrepresentations; they are a translation step so the skill
has a stable internal vocabulary. The original terms are preserved in the source citations
and discussed in `references/articles-sources.md` for anyone who wants the direct line to
the literature.
