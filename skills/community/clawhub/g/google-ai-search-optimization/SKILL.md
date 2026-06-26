---
name: google-ai-search-optimization
description: Audit websites, pages, content plans, or SEO recommendations for Google Search generative AI features such as AI Overviews and AI Mode. Use whenever the user asks about AI SEO, AEO, GEO, Google AI Overviews visibility, AI Mode readiness, agent-friendly site optimization, or whether tactics like llms.txt, chunking, structured data, or AI-generated content help Google generative search.
---

# Google AI Search Optimization

Use this skill to evaluate a website, page, content plan, or SEO proposal against Google's official guidance for generative AI features in Search.

## First Step

Read references/google-ai-optimization-guide.md before giving recommendations. Treat it as the policy source for Google AI Overviews and AI Mode guidance.

If the task involves a live website or page, gather page evidence first using the available web, scrape, Search Console, or local repo tools. If evidence is missing, state the assumption instead of inventing audit findings.

## Workflow

1. Identify the target: site, page, content cluster, ecommerce/local business surface, or SEO tactic.
2. Gather evidence:
   - For a live URL, scrape/read the page and inspect visible content structure.
   - For a site audit, sample representative pages instead of assuming the whole site behaves the same.
   - For performance or indexing questions, use Search Console data when credentials and site access are available.
3. Classify the request:
   - Readiness audit: assess current state and prioritize fixes.
   - Content review: judge uniqueness, helpfulness, first-hand expertise, and non-commodity value.
   - Technical review: crawlability, indexability, snippets, JavaScript SEO, duplicate content, page experience.
   - Tactic review: accept, reject, or qualify proposed AI SEO tactics.
   - Agentic experience review: browser-agent usability, DOM/accessibility clarity, and emerging commerce/action flows.
4. Produce prioritized recommendations with rationale and caveats.

## Output Shape

Prefer concise, decision-oriented output:

- Verdict: ready / needs work / bad tactic / not enough evidence.
- Highest-impact fixes: 3-7 prioritized actions.
- Keep doing: what already aligns with Google guidance.
- Avoid: hype tactics or policy-risky moves.
- Evidence gaps: data needed before making stronger claims.

For deeper audits, group findings by:

- Content quality
- Technical search eligibility
- Local/ecommerce surfaces
- Media and page experience
- Agentic experience readiness
- Measurement and follow-up

## Core Guidance

- Treat generative AI search optimization as SEO for Google Search, not a separate hack stack.
- Prioritize helpful, reliable, people-first content with unique expertise or first-hand perspective.
- Favor non-commodity content over generic listicles or pages that merely restate common knowledge.
- Keep content crawlable, indexable, and eligible for snippets; Google AI features draw from Search index and ranking systems.
- Use semantic HTML, clear headings, accessible structure, high-quality images/video, and good page experience because they help users and search systems.
- For JavaScript-heavy sites, verify rendered content is accessible to Google and follow JavaScript SEO basics.
- For local businesses and ecommerce, review Merchant Center, product data, feeds, and Google Business Profile completeness where relevant.
- Structured data remains useful for rich results, but it is not a special requirement for generative AI search.

## Tactics To Reject Or Deprioritize

Call these out plainly when they appear:

- Creating llms.txt or special AI-only machine-readable files for Google AI Overviews visibility.
- Chunking content solely for AI systems.
- Rewriting content only to target AI-generated answers.
- Creating scaled pages for query fan-out variants when the main purpose is ranking manipulation.
- Seeking inauthentic mentions across the web.
- Overfocusing on structured data as if schema alone unlocks AI visibility.
- Treating AEO/GEO as a separate discipline that bypasses normal Google Search quality systems.

## Gotchas

- Do not promise inclusion in AI Overviews or AI Mode; crawling, indexing, serving, and AI feature selection are never guaranteed.
- Do not recommend scaled content generation if the value is only query coverage; that risks Google's scaled content abuse policy.
- Do not treat full automation or AI-written content as bad by default; judge whether the final content satisfies Search Essentials and spam policies.
- If a user asks for Google Search Console analysis, use the google-search-console skill when available.
- If a user asks for a full website crawl or webpage extraction, use the relevant Firecrawl skill/tool before auditing.
