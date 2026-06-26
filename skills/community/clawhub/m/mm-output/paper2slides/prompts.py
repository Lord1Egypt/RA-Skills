"""
Prompt templates for content planning and image generation.
Ported from Paper2Slides project.
"""
from typing import Dict

# ---------------------------------------------------------------------------
# Content Planning Prompts
# ---------------------------------------------------------------------------

SLIDES_PLANNING_PROMPT = """Organize the document into {min_pages}-{max_pages} slides by distributing the content below.

## Document Summary
{summary}
{assets_section}
## Output Fields
- **id**: Slide identifier
- **title**: A concise title suitable for this slide
- **content**: The main text for this slide. This is the MOST IMPORTANT field. Requirements:
  - **DETAILED METHOD DESCRIPTION**: For method slides, describe each step/component in detail.
  - **PRESERVE KEY FORMULAS**: If the source has formulas, include 1-2 relevant ones in LaTeX.
  - **PRESERVE SPECIFIC NUMBERS**: Key percentages, metrics, dataset sizes, and comparison values.
  - **SUBSTANTIAL CONTENT**: Each slide should contain enough detail to fully explain its topic.
  - **COPY FROM SOURCE**: Extract and adapt text from the summary. Do not over-simplify.
  - Only use information provided above. Do not invent details.
- **tables**: Tables you want to show on this slide
  - table_id: e.g., "Table 1"
  - extract: (optional) Partial table in HTML format with ACTUAL DATA VALUES
  - focus: (optional) What aspect to emphasize
- **figures**: Figures you want to show on this slide
  - figure_id: e.g., "Figure 1"
  - focus: (optional) What to highlight

## Content Guidelines

Distribute content across {min_pages}-{max_pages} slides covering these areas:

1. **Title/Cover**: Document title, authors/source if available
2. **Main Content** (can span multiple slides):
   - Organize into logical slides based on the document's natural structure
   - Each slide should focus on one topic with full details
   - Include specific numbers, data points, and examples
   - Match relevant tables/figures with their explanations
3. **Summary/Conclusion**: Key takeaways with specific numbers if applicable

## Output Format (JSON)
```json
{{
  "slides": [
    {{
      "id": "slide_01",
      "title": "[Document title]",
      "content": "[Authors/source if available]",
      "tables": [],
      "figures": []
    }},
    {{
      "id": "slide_02",
      "title": "[Topic name]",
      "content": "[Detailed description...]",
      "tables": [],
      "figures": [{{"figure_id": "Figure X", "focus": "[what to highlight]"}}]
    }}
  ]
}}
```

## CRITICAL REQUIREMENTS
1. **FORMULAS**: If present, include key formulas in LaTeX. In JSON, escape backslashes as \\\\.
2. **MINIMUM CONTENT LENGTH**: Each slide content should be at least 150-200 words (except title).
3. **SPECIFIC NUMBERS**: Use precise values from source.
4. **TABLE DATA**: Extract tables with actual numerical values from the original.
"""

POSTER_DENSITY_GUIDELINES: Dict[str, str] = {
    "sparse": """Current density level is **sparse**. Content should be concise but still informative.
Keep: main topic, core message, key points, important takeaways.
Present tables using extract (partial table) showing only the most important rows with ACTUAL values.
Write clear sentences that capture the essential point of each section.""",

    "medium": """Current density level is **medium**. Content should cover main points with supporting details.
Keep: topic with context, key concepts explained, supporting examples, main conclusions.
**INCLUDE formulas/equations** that are important with explanations.
Include relevant tables with key columns/rows and ACTUAL data values.
Write complete explanations that give readers a solid understanding.""",

    "dense": """Current density level is **dense**. Content should be comprehensive with full details.
Keep: complete context, all key concepts with full explanations, detailed examples and analysis.
**INCLUDE key formulas/equations** with explanations.
Include complete tables or detailed extracts with actual values.
Write thorough explanations covering all important aspects.""",
}

POSTER_PLANNING_PROMPT = """Organize the document into poster sections by distributing the content below.

## Document Summary
{summary}
{assets_section}
## Content Density
{density_guidelines}

## Output Fields
- **id**: Section identifier
- **title**: A concise title for this section
- **content**: The main text for this section. This is the MOST IMPORTANT field. Requirements:
  - **DETAILED DESCRIPTIONS**: Describe each step/component in detail.
  - **PRESERVE KEY FORMULAS**: If the source has formulas, include 1-2 relevant ones in LaTeX.
  - **PRESERVE SPECIFIC NUMBERS**: Key percentages, metrics, dataset sizes, comparison values.
  - **SUBSTANTIAL CONTENT**: Each section should contain enough detail to fully explain its topic.
  - **COPY FROM SOURCE**: Extract and adapt text from summary. Do not over-simplify.
  - Adjust detail level based on density above. Only use information provided. Do not invent details.
- **tables**: Tables to show in this section
  - table_id: e.g., "Table 1"
  - extract: (optional) Partial table in HTML format with ACTUAL DATA VALUES
  - focus: (optional) What aspect to emphasize
- **figures**: Figures to show in this section
  - figure_id: e.g., "Figure 1"
  - focus: (optional) What to highlight

## Section Guidelines

1. **Title/Header**: Document title, authors if available
2. **Main Content**: Key topics with full details
3. **Key Data**: Important numbers, statistics from tables with EXACT values
4. **Summary**: Main takeaways listed with specific numbers

## Output Format (JSON)
```json
{{
  "sections": [
    {{
      "id": "poster_title",
      "title": "[Document title]",
      "content": "[Authors/source if available]",
      "tables": [],
      "figures": []
    }},
    {{
      "id": "poster_content",
      "title": "[Topic name]",
      "content": "[Detailed description...]",
      "tables": [],
      "figures": [{{"figure_id": "Figure X", "focus": "[key concept]"}}]
    }}
  ]
}}
```

## CRITICAL REQUIREMENTS
1. **FORMULAS**: If present, include key formulas in LaTeX. In JSON, escape backslashes as \\\\.
2. **MINIMUM CONTENT LENGTH**: Each section content should be at least 100-150 words (except title).
3. **SPECIFIC NUMBERS**: Use precise values from source.
4. **TABLE DATA**: Extract tables with actual numerical values from the original.
"""

# ---------------------------------------------------------------------------
# Slides page ranges
# ---------------------------------------------------------------------------

SLIDES_PAGE_RANGES: Dict[str, tuple] = {
    "short": (5, 8),
    "medium": (8, 12),
    "long": (12, 15),
}

# ---------------------------------------------------------------------------
# Image Generation Prompts & Style Hints
# ---------------------------------------------------------------------------

FORMAT_POSTER = (
    "Wide landscape poster layout (16:9 aspect ratio). Just ONE poster. "
    "Keep information density moderate, leave whitespace for readability."
)
FORMAT_SLIDE = "Wide landscape slide layout (16:9 aspect ratio)."
FORMAT_SLIDE_VERTICAL = (
    "Tall portrait slide layout (9:16 aspect ratio, like a phone screen). "
    "Design for mobile viewing — large readable text, strong visual hierarchy, "
    "bold key points. Content should fill the vertical space naturally."
)

POSTER_STYLE_HINTS: Dict[str, str] = {
    "academic": (
        "Academic conference poster style with LIGHT CLEAN background. "
        "MATCH THE LANGUAGE of the content text (Chinese if content is Chinese, English if English). "
        "Use PROFESSIONAL, CLEAR tones with good contrast and academic fonts. "
        "Use 3-column layout showing story progression. Preserve details from the content. "
        "Title section at the top can have a colored background bar. "
        "FIGURES: Preserve original scientific figures - maintain accuracy and integrity."
    ),
    "doraemon": (
        "Classic Doraemon anime style, bright and friendly. "
        "MATCH THE LANGUAGE of the content text (Chinese if content is Chinese, English if English). "
        "Use WARM, ELEGANT, MUTED tones. Use ROUNDED sans-serif fonts for ALL text. "
        "Large readable text. Use 3-column layout showing story progression. "
        "Keep it simple, not too fancy. Doraemon character as guide only (1-2 small figures)."
    ),
    "minimal": (
        "Clean minimalist style. "
        "MATCH THE LANGUAGE of the content text (Chinese if content is Chinese, English if English). "
        "Light warm gray background with Morandi palette - charcoal text, muted gold accent. "
        "Spacious layout with generous whitespace. Simple geometric shapes only."
    ),
}

SLIDE_STYLE_HINTS: Dict[str, str] = {
    "academic": (
        "Professional STANDARD ACADEMIC style. "
        "MATCH THE LANGUAGE of the content text (Chinese if content is Chinese, English if English). "
        "Use ROUNDED sans-serif fonts for ALL text. Use MORANDI COLOR PALETTE with LIGHT background. "
        "Clean simple lines. Figures and tables are CRUCIAL - REDRAW them to match the visual style. "
        "Visualize data with CHARTS. Layout should be SPACIOUS and ELEGANT."
    ),
    "doraemon": (
        "Classic Doraemon anime style, bright and friendly. "
        "SOPHISTICATED, REFINED color palette (NOT childish bright colors). "
        "MATCH THE LANGUAGE of the content text (Chinese if content is Chinese, English if English). "
        "PRESERVE EVERY DETAIL from the content. Use ROUNDED sans-serif fonts for ALL text. "
        "LIMITED COLOR PALETTE (3-4 colors max): WARM, ELEGANT, MUTED tones. "
        "IF the slide has figures/tables: focus on them as the main visual content. "
        "IF NO figures/tables: add illustrations or icons for each paragraph."
    ),
    "minimal": (
        "Clean minimalist style. "
        "MATCH THE LANGUAGE of the content text (Chinese if content is Chinese, English if English). "
        "MORANDI COLOR PALETTE with light background. Simple clean lines. "
        "Large readable text. Spacious layout with generous breathing room."
    ),
}

SLIDE_LAYOUTS: Dict[str, Dict[str, str]] = {
    "academic": {
        "opening": (
            "Opening Slide: Title large at TOP CENTER. Authors at BOTTOM. "
            "ONE visual element CENTER. LIGHT background."
        ),
        "content": (
            "Content Slide: Title at TOP LEFT. Moderate font, SPACIOUS layout. "
            "Figures/tables should BLEND with background style. "
            "Visualize data with LARGE meaningful CHARTS. "
            "Add simple-line icons for each paragraph. LIGHT background."
        ),
        "ending": (
            "Ending Slide: Heading at TOP CENTER. Key takeaways in CENTER. "
            "LIGHT background same as previous slide."
        ),
    },
    "doraemon": {
        "opening": (
            "Opening Slide (Anime Style): Title large sans-serif at TOP CENTER. "
            "Authors at BOTTOM. Doraemon character in CENTER. "
            "SOPHISTICATED WARM MUTED tones."
        ),
        "content": (
            "Content Slide (Anime Style): Title sans-serif at TOP LEFT. "
            "Content in THIN PLAIN rounded border. CLEAN WARM background. "
            "IF figures/tables: feature prominently. IF NOT: add illustrations. "
            "Characters appear MEANINGFULLY with context-appropriate actions."
        ),
        "ending": (
            "Ending Slide (Anime Style): Heading at TOP CENTER. "
            "FULL-SCREEN illustration featuring characters as background. "
            "SOPHISTICATED WARM MUTED tones."
        ),
    },
}

VISUALIZATION_HINTS = (
    "Visualization:\n"
    "- Use diagrams and icons to represent concepts\n"
    "- Visualize data/numbers as charts\n"
    "- Use bullet points, highlight key metrics\n"
    "- Keep background CLEAN and simple"
)

CONSISTENCY_HINT = (
    "IMPORTANT: Maintain consistent colors and style with the reference slide."
)

FIGURE_HINT = (
    "For reference figures: REDRAW them to match the visual style and color scheme. "
    "Preserve the original structure and key information, "
    "but make them BLEND seamlessly with the design."
)

# ---------------------------------------------------------------------------
# Vertical slide layouts (for XHS / mobile)
# ---------------------------------------------------------------------------

VERTICAL_SLIDE_LAYOUTS: Dict[str, Dict[str, str]] = {
    "academic": {
        "opening": (
            "Portrait Opening Slide: Title LARGE and BOLD at upper 1/3. "
            "Authors/source smaller below. One hero visual in lower half. "
            "LIGHT clean background. Mobile-friendly large fonts."
        ),
        "content": (
            "Portrait Content Slide: Title BOLD at top. "
            "Content flows top-to-bottom with generous line spacing. "
            "Key numbers/stats highlighted with accent colors. "
            "Figures placed LARGE in center. Charts and icons fill space. "
            "LIGHT background. Mobile-optimized readability."
        ),
        "ending": (
            "Portrait Ending Slide: Key takeaways as large bullet points. "
            "Clean centered layout. LIGHT background."
        ),
    },
    "doraemon": {
        "opening": (
            "Portrait Opening (Anime): Title LARGE sans-serif at top. "
            "Doraemon character as hero visual in center-bottom. "
            "WARM MUTED sophisticated tones. Full-height illustration feel."
        ),
        "content": (
            "Portrait Content (Anime): Title at top, content top-to-bottom. "
            "Soft rounded content card with THIN border. "
            "Characters appear contextually alongside content. "
            "WARM MUTED tones. Fill vertical space with illustrations."
        ),
        "ending": (
            "Portrait Ending (Anime): Full-height illustration as background. "
            "Key takeaways overlaid. Characters in celebration pose. "
            "WARM MUTED sophisticated tones."
        ),
    },
}

# ---------------------------------------------------------------------------
# XHS (小红书) Copywriting Prompt
# ---------------------------------------------------------------------------

XHS_COPYWRITING_PROMPT = """你是一个拥有2000w粉丝的小红书爆款写作专家，同时拥有消费心理学+市场营销双PhD。
你是小红书的重度用户，拥有卓越的互联网网感。你的语气和写作风格非常小红书化。
你只在中文互联网语境下创作，使用自然富有网感的中文。

现在请你根据以下内容，创作一篇小红书爆款笔记。

## 内容摘要
{summary}

## 创作要求

### 标题（5个备选）
- 每个标题字数限制在20以内
- 含适当的emoji表情
- 使用爆炸词（带有强烈情感倾向且能引起用户共鸣的词语）
- 制造好奇心或共鸣感

### 正文（1篇）
- 每个段落都含有适当的emoji表情（同一emoji不重复出现）
- 开头要有hook，抓住注意力
- 内容要干货满满，有信息增量
- 语言口语化、亲切自然
- 适当使用"！""～""…"等语气词
- 文末附上合适的SEO标签（#开头）

## 输出格式（严格JSON）
```json
{{
  "titles": [
    "标题1（含emoji）",
    "标题2（含emoji）",
    "标题3（含emoji）",
    "标题4（含emoji）",
    "标题5（含emoji）"
  ],
  "body": "正文内容（含emoji和段落分隔）",
  "tags": ["#标签1", "#标签2", "#标签3", "#标签4", "#标签5"]
}}
```
"""
