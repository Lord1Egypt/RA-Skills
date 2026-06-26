#!/usr/bin/env python3
"""
SEO Content Engine — OpenClaw ClawHub Skill
Researches competitors via web search and generates fully SEO-optimized blog posts.
Uses Playwright for research + Gemini API for content generation.
"""

import argparse
import asyncio
import json
import os
import re
import sys
import urllib.parse
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# Load env
load_dotenv(Path("/Users/edwin/.openclaw/workspace/dreams-arts/.env"))

try:
    import google.generativeai as genai
except ImportError:
    print("google-generativeai not installed. Run: pip install google-generativeai", file=sys.stderr)
    sys.exit(1)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("GEMINI_API_KEY not found in environment", file=sys.stderr)
    sys.exit(1)

genai.configure(api_key=GEMINI_API_KEY)

CDP_URL = "http://localhost:9222"
REQUEST_TIMEOUT = 15_000


class SEOContentEngine:
    """Researches competitors and generates SEO-optimized blog posts."""

    def __init__(self, model_name: str = "gemini-2.0-flash"):
        self.model = genai.GenerativeModel(model_name)
        self.browser = None
        self.context = None

    async def _connect_browser(self):
        """Connect to existing Chrome via CDP."""
        try:
            from playwright.async_api import async_playwright
            pw = await async_playwright().start()
            self.browser = await pw.chromium.connect_over_cdp(CDP_URL)
            self.context = self.browser.contexts[0] if self.browser.contexts else await self.browser.new_context()
            return True
        except Exception as e:
            print(f"Could not connect to browser: {e}", file=sys.stderr)
            return False

    async def _new_page(self):
        page = await self.context.new_page()
        page.set_default_timeout(REQUEST_TIMEOUT)
        return page

    # ── Competitor Research ───────────────────────────────────────────────

    async def research_serp(self, keyword: str) -> list[dict]:
        """Search Google and extract top 10 organic results."""
        if not self.browser:
            if not await self._connect_browser():
                return []

        page = await self._new_page()
        try:
            query = urllib.parse.quote_plus(keyword)
            url = f"https://www.google.com/search?q={query}&num=10"

            await page.goto(url, wait_until="domcontentloaded", timeout=REQUEST_TIMEOUT)
            await asyncio.sleep(2)

            results = await page.evaluate("""() => {
                const results = [];

                // Organic results
                document.querySelectorAll('#search .g, #rso .g').forEach(el => {
                    const titleEl = el.querySelector('h3');
                    const linkEl = el.querySelector('a[href^="http"]');
                    const snippetEl = el.querySelector('[data-sncf], .VwiC3b, [style*="-webkit-line-clamp"]');

                    if (titleEl && linkEl) {
                        results.push({
                            title: titleEl.textContent.trim(),
                            url: linkEl.getAttribute('href'),
                            snippet: snippetEl ? snippetEl.textContent.trim() : ''
                        });
                    }
                });

                return results.slice(0, 10);
            }""")

            return results

        except Exception as e:
            print(f"SERP research error: {e}", file=sys.stderr)
            return []
        finally:
            await page.close()

    async def research_paa(self, keyword: str) -> list[str]:
        """Extract 'People Also Ask' questions from Google."""
        if not self.browser:
            if not await self._connect_browser():
                return []

        page = await self._new_page()
        try:
            query = urllib.parse.quote_plus(keyword)
            url = f"https://www.google.com/search?q={query}"

            await page.goto(url, wait_until="domcontentloaded", timeout=REQUEST_TIMEOUT)
            await asyncio.sleep(2)

            questions = await page.evaluate("""() => {
                const questions = [];
                // PAA questions
                document.querySelectorAll('[data-q], [jsname="Cpkphb"] [role="heading"], .related-question-pair span').forEach(el => {
                    const q = el.getAttribute('data-q') || el.textContent.trim();
                    if (q && q.length > 10 && q.endsWith('?')) {
                        questions.push(q);
                    }
                });

                // Also try aria-expanded buttons in PAA
                if (questions.length === 0) {
                    document.querySelectorAll('[aria-expanded] [role="heading"]').forEach(el => {
                        const text = el.textContent.trim();
                        if (text.length > 10) questions.push(text);
                    });
                }

                return [...new Set(questions)].slice(0, 8);
            }""")

            return questions

        except Exception as e:
            print(f"PAA research error: {e}", file=sys.stderr)
            return []
        finally:
            await page.close()

    async def research_competitor_headings(self, urls: list[str], max_articles: int = 5) -> list[dict]:
        """Visit top articles and extract their heading structure."""
        if not self.browser:
            return []

        articles = []
        for url in urls[:max_articles]:
            page = await self._new_page()
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=REQUEST_TIMEOUT)
                await asyncio.sleep(1)

                data = await page.evaluate("""() => {
                    const headings = [];
                    document.querySelectorAll('h1, h2, h3').forEach(h => {
                        headings.push({
                            level: h.tagName.toLowerCase(),
                            text: h.textContent.trim().substring(0, 200)
                        });
                    });

                    // Estimate word count
                    const article = document.querySelector('article, main, [role="main"], .post-content, .entry-content');
                    const text = (article || document.body).innerText;
                    const wordCount = text.split(/\\s+/).length;

                    return {headings, word_count: wordCount};
                }""")

                articles.append({
                    "url": url,
                    "headings": data.get("headings", []),
                    "word_count": data.get("word_count", 0),
                })

            except Exception as e:
                print(f"Could not analyze {url}: {e}", file=sys.stderr)
            finally:
                await page.close()

        return articles

    # ── Content Generation ───────────────────────────────────────────────

    def _build_generation_prompt(
        self,
        keyword: str,
        serp_results: list[dict],
        paa_questions: list[str],
        competitor_headings: list[dict],
        tone: str,
        word_count: int,
        brand: str | None,
        location: str | None,
    ) -> str:
        # Build competitor analysis section
        serp_section = ""
        if serp_results:
            serp_section = "## Top Competing Articles\n"
            for i, r in enumerate(serp_results[:10], 1):
                serp_section += f"{i}. **{r['title']}** — {r['url']}\n   Snippet: {r.get('snippet', 'N/A')}\n"

        headings_section = ""
        if competitor_headings:
            headings_section = "\n## Competitor Article Structures\n"
            for art in competitor_headings:
                headings_section += f"\n### {art['url']} (~{art['word_count']} words)\n"
                for h in art["headings"][:15]:
                    indent = "  " if h["level"] == "h3" else ""
                    headings_section += f"{indent}- [{h['level'].upper()}] {h['text']}\n"

        paa_section = ""
        if paa_questions:
            paa_section = "\n## People Also Ask\n"
            for q in paa_questions:
                paa_section += f"- {q}\n"

        brand_instruction = ""
        if brand:
            brand_instruction = f"\n- Naturally mention the brand '{brand}' 2-3 times where relevant (not forced)"
        if location:
            brand_instruction += f"\n- Include local SEO references to '{location}' where natural"

        return f"""You are a world-class SEO content strategist and writer. Generate a complete, publication-ready blog post.

# TARGET KEYWORD: {keyword}

{serp_section}
{headings_section}
{paa_section}

# REQUIREMENTS

## Content
- Write a comprehensive blog post of at least {word_count} words
- Tone: {tone}
- Cover the topic MORE thoroughly than any competitor above
- Include unique angles and insights competitors missed
- Add practical, actionable advice{brand_instruction}

## SEO Optimization
- Target keyword in H1 title, first paragraph, and 2-3 H2 headings
- Keyword density 1-2% (natural, not stuffed)
- Use related/LSI keywords throughout
- Meta description under 160 characters with keyword and CTA
- H2/H3 heading hierarchy (never skip levels)
- Short paragraphs (2-4 sentences max)
- Use bullet points and bold for scanability

## Structure
- YAML frontmatter with: title, meta_description, target_keyword, secondary_keywords (array), word_count, reading_time, internal_links_suggested (array of {{anchor, target}})
- H1 title (compelling, keyword-rich, under 60 chars for SERP)
- Introduction with hook + keyword in first 100 words
- 4-7 H2 sections with H3 subsections where appropriate
- FAQ section with 4-6 questions (use People Also Ask data above + generate additional relevant ones)
- Conclusion with CTA

## Format
- Output as clean Markdown
- YAML frontmatter wrapped in ---
- Use ** for bold, - for bullet lists
- No fluff, no filler, every sentence adds value

Write the COMPLETE article now. Do NOT truncate or summarize. Write every section in full."""

    def _generate_article(self, prompt: str) -> str:
        """Generate the article using Gemini."""
        for attempt in range(3):
            try:
                response = self.model.generate_content(
                    prompt,
                    generation_config=genai.GenerationConfig(
                        temperature=0.7,
                        max_output_tokens=8192,
                    ),
                )
                return response.text.strip()
            except Exception as e:
                print(f"Generation attempt {attempt + 1} failed: {e}", file=sys.stderr)
                if attempt == 2:
                    raise

    # ── Main Pipeline ────────────────────────────────────────────────────

    async def generate(
        self,
        keyword: str,
        tone: str = "informative, engaging",
        word_count: int = 2000,
        brand: str | None = None,
        location: str | None = None,
        skip_research: bool = False,
    ) -> str:
        """Full pipeline: research competitors, then generate optimized article."""

        serp_results = []
        paa_questions = []
        competitor_headings = []

        if not skip_research:
            print(f"Researching SERP for '{keyword}'...", file=sys.stderr)

            # Run SERP and PAA research in parallel
            serp_task = self.research_serp(keyword)
            paa_task = self.research_paa(keyword)
            serp_results, paa_questions = await asyncio.gather(serp_task, paa_task)

            print(f"Found {len(serp_results)} SERP results, {len(paa_questions)} PAA questions", file=sys.stderr)

            # Analyze top competitor articles
            if serp_results:
                urls = [r["url"] for r in serp_results if r.get("url")]
                print(f"Analyzing top {min(5, len(urls))} competitor articles...", file=sys.stderr)
                competitor_headings = await self.research_competitor_headings(urls)
                print(f"Analyzed {len(competitor_headings)} articles", file=sys.stderr)

        # Generate the article
        print("Generating SEO-optimized article...", file=sys.stderr)
        prompt = self._build_generation_prompt(
            keyword=keyword,
            serp_results=serp_results,
            paa_questions=paa_questions,
            competitor_headings=competitor_headings,
            tone=tone,
            word_count=word_count,
            brand=brand,
            location=location,
        )

        article = self._generate_article(prompt)

        # Clean up any markdown code fences wrapping the entire output
        if article.startswith("```markdown"):
            article = article[len("```markdown"):].strip()
        if article.startswith("```"):
            article = article[3:].strip()
        if article.endswith("```"):
            article = article[:-3].strip()

        return article


async def main():
    parser = argparse.ArgumentParser(description="SEO Content Engine — Generate optimized blog posts")
    parser.add_argument("keyword", help="Target keyword or topic")
    parser.add_argument("--tone", default="informative, engaging", help="Writing tone/style")
    parser.add_argument("--word-count", type=int, default=2000, help="Target word count")
    parser.add_argument("--brand", default=None, help="Brand name to weave in naturally")
    parser.add_argument("--location", default=None, help="Location for local SEO")
    parser.add_argument("--output", default=None, help="Output file path (default: stdout)")
    parser.add_argument("--skip-research", action="store_true", help="Skip web research, use keyword only")

    args = parser.parse_args()

    engine = SEOContentEngine()
    article = await engine.generate(
        keyword=args.keyword,
        tone=args.tone,
        word_count=args.word_count,
        brand=args.brand,
        location=args.location,
        skip_research=args.skip_research,
    )

    if args.output:
        Path(args.output).write_text(article, encoding="utf-8")
        print(f"Article saved to {args.output}", file=sys.stderr)
    else:
        print(article)


if __name__ == "__main__":
    asyncio.run(main())
