"""
workflow_templates.py — Workflow templates

Responsibilities:
- Maintain workflow templates (first batch: AI Coding Tech Radar, Content Creation Materials, Knowledge Base Capture, Product Opportunity Scan, Investment/Strategy Brief)
- Select template based on user intent
- Merge template with user preferences into content organization intent
- Provide template context for artifact_renderer
- Output executable integration requests to host_platform_adapters or other Agent tools when host tools are visible
- Templates only express scenarios, default focus areas, and output constraints; specific content organization is done by Agent LLM

Design Principles:
- First batch of templates prioritizes serving developers, product managers, content creators, and power users
- Workflow templates define content organization methods; automation intent defines time, frequency, timezone, artifact type, and target destination
- Can generate stable artifacts suitable for downstream tool consumption, and continue assisting with sending, saving, writing, or creating tasks when host capabilities are available
"""

from typing import List, Dict, Any, Optional

# Workflow template definitions
WORKFLOW_TEMPLATES = [
    {
        "id": "ai_coding_radar",
        "title": "AI Coding Tech Radar",
        "description": "Continuously track AI Coding, Agent, open source models, and developer tools. Suitable for engineers, technical leads, and AI Infra practitioners.",
        "allow_emoji": False,
        "default_topics": ["agent", "ai_coding", "open_source", "infrastructure"],
        "target_roles": ["engineer", "founder"],
        "focus_fields": [
            "title_normalized", "summary_normalized", "categories",
            "strategic_explainer", "source_type", "secondary_class_l1",
        ],
        "section_structure": [
            {"name": "Key Breakthroughs", "filter": "research_breakthrough"},
            {"name": "Tool Updates", "filter": "developer_tools"},
            {"name": "Agent Progress", "filter": "agent_framework"},
            {"name": "Open Source News", "filter": "open_source"},
            {"name": "Trend Observations", "filter": "industry_trend"},
        ],
        "output_format": "knowledge_ready_note",
        "tags": ["Technology", "Development", "AI Coding", "Agent"],
    },
    {
        "id": "content_creation_materials",
        "title": "Content Creation Materials",
        "description": "Organize daily AI news into materials suitable for blogs, newsletters, communities, or short content scripts. Suitable for content creators, media, and operations.",
        "allow_emoji": True,
        "default_topics": ["product", "trend", "announcement"],
        "target_roles": ["creator", "general"],
        "focus_fields": [
            "title_normalized", "summary_normalized", "ranking_rationale",
            "strategic_explainer", "categories",
        ],
        "section_structure": [
            {"name": "Today's Hot Topics", "filter": "top_news"},
            {"name": "Title Suggestions", "filter": "title_ideas"},
            {"name": "Key Insights", "filter": "key_insights"},
            {"name": "Further Reading", "filter": "further_reading"},
        ],
        "output_format": "markdown_briefing",
        "tags": ["Content", "Creation", "Media", "Operations"],
    },
    {
        "id": "knowledge_base_capture",
        "title": "Knowledge Base Capture",
        "description": "Organize valuable AI news into summaries suitable for knowledge bases, note systems, or research libraries. Suitable for researchers, analysts, and lifelong learners.",
        "allow_emoji": True,
        "default_topics": ["research", "safety", "alignment", "breakthrough"],
        "target_roles": ["researcher", "investor"],
        "focus_fields": [
            "title_normalized", "summary_normalized", "strategic_explainer",
            "ranking_rationale", "categories", "source_type",
        ],
        "section_structure": [
            {"name": "Research Progress", "filter": "research"},
            {"name": "Key Insights", "filter": "insights"},
            {"name": "Source Traceability", "filter": "sources"},
            {"name": "Related Topics", "filter": "related_topics"},
        ],
        "output_format": "knowledge_ready_note",
        "tags": ["Research", "Knowledge Base", "Notes", "Learning"],
    },
    {
        "id": "product_opportunity_scan",
        "title": "Product Opportunity Scan",
        "description": "Extract product opportunities, competitor changes, and user demand signals from daily news. Suitable for product managers, entrepreneurs, and product leads.",
        "allow_emoji": False,
        "default_topics": ["product", "launch", "competition", "user_need"],
        "target_roles": ["product", "founder"],
        "focus_fields": [
            "title_normalized", "summary_normalized", "categories",
            "strategic_explainer", "secondary_class_l1", "secondary_class_l2",
        ],
        "section_structure": [
            {"name": "New Product Launches", "filter": "product_launch"},
            {"name": "Competitor News", "filter": "competition"},
            {"name": "User Demand", "filter": "user_need"},
            {"name": "Market Opportunities", "filter": "market_opportunity"},
            {"name": "Risk Alerts", "filter": "risks"},
        ],
        "output_format": "structured_summary",
        "tags": ["Product", "Opportunity", "Competition", "Market"],
    },
    {
        "id": "investment_strategy_brief",
        "title": "Investment/Strategy Brief",
        "description": "Focus on fundraising, M&A, company news, commercialization, and regulation. Suitable for investors, strategy analysts, and corporate decision-makers.",
        "allow_emoji": False,
        "default_topics": ["fundraising", "partnership", "regulation", "market"],
        "target_roles": ["investor", "founder"],
        "focus_fields": [
            "title_normalized", "summary_normalized", "categories",
            "strategic_explainer", "ranking_rationale", "source_type",
        ],
        "section_structure": [
            {"name": "Fundraising News", "filter": "fundraising"},
            {"name": "M&A & Partnerships", "filter": "partnership"},
            {"name": "Regulatory Policy", "filter": "regulation"},
            {"name": "Market Trends", "filter": "market_trend"},
            {"name": "Strategic Insights", "filter": "strategic_insights"},
        ],
        "output_format": "markdown_briefing",
        "tags": ["Investment", "Strategy", "Fundraising", "Regulation"],
    },
]


def list_workflow_templates() -> List[Dict[str, Any]]:
    """List all available workflow templates"""
    return list(WORKFLOW_TEMPLATES)


def select_workflow_template(
    intent: str,
    user_role: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Select the most suitable workflow template based on user intent.

    Parameters:
        intent: User's natural language intent, e.g., "I want to write a blog", "create tech radar", etc.
        user_role: User role, e.g., engineer, product, investor, etc.

    Returns:
        Matching template or None
    """
    intent_lower = intent.lower()

    # Keyword matching
    keyword_map = {
        "ai_coding_radar": ["tech radar", "ai coding", "agent", "dev", "code", "engineer", "development", "coding"],
        "content_creation_materials": ["content", "create", "blog", "newsletter", "community", "social", "script", "article", "writing"],
        "knowledge_base_capture": ["knowledge base", "note", "capture", "research", "obsidian", "notion", "ima", "learn", "study"],
        "product_opportunity_scan": ["product", "opportunity", "competitor", "pm", "product manager", "entrepreneur", "startup", "market"],
        "investment_strategy_brief": ["investment", "invest", "strategy", "fundraising", "ma", "m&a", "regulation", "brief"],
    }

    scores: Dict[str, int] = {}
    for template_id, keywords in keyword_map.items():
        score = sum(1 for kw in keywords if kw in intent_lower)
        if score > 0:
            scores[template_id] = score

    # If role information is available, prioritize role matching
    if user_role:
        for template in WORKFLOW_TEMPLATES:
            if user_role in template.get("target_roles", []):
                tid = template["id"]
                scores[tid] = scores.get(tid, 0) + 1

    if not scores:
        return None

    best_id = max(scores.keys(), key=lambda tid: scores[tid])
    for template in WORKFLOW_TEMPLATES:
        if template["id"] == best_id:
            return template

    return None


def render_workflow_template(
    template: Dict[str, Any],
    preferences: Optional[dict] = None,
) -> str:
    """
    Render template as a prompt-style formatting contract.
    """
    allow_emoji = bool(template.get("allow_emoji", False))
    section_divider = "-----"

    lines = [
        f"## Workflow Template: {template['title']}",
        "",
        template["description"],
        "",
        "### Formatting Contract",
        "",
        "- This template is a strong formatting instruction, not a loose suggestion.",
        f"- Use section dividers exactly as `{section_divider}` between major sections.",
        f"- Use the same divider exactly as `{section_divider}` between subsections inside a section.",
        "- Do not add extra dividers inside bullet items or paragraphs.",
        "- The workflow sections below define only the main content body.",
        "- Survey, Feedback, Sponsor, and Update Available are carry-over blocks, not workflow analysis sections.",
        "- Do not merge carry-over blocks into the workflow sections above.",
    ]

    if allow_emoji:
        lines.extend([
            "- Emoji are allowed in headings and section labels for this template.",
            "- Keep emoji sparse and readable; do not decorate every line.",
        ])
    else:
        lines.extend([
            "- Do not use emoji in headings, bullets, or section labels for this template.",
            "- Keep the output restrained and scan-friendly.",
        ])

    lines.extend([
        "",
        "### Applicable Scenarios",
        "",
    ])

    for tag in template.get("tags", []):
        lines.append(f"- {tag}")

    lines.append("")
    lines.append("### Recommended Content Structure")
    lines.append("")

    for section in template.get("section_structure", []):
        lines.append(section_divider)
        lines.append(f"#### {section['name']}")
        lines.append(f"- Filter hint: `{section['filter']}`")
        lines.append("")

    lines.append("")
    lines.append("### Output Format")
    lines.append("")
    lines.append(f"- Default format: `{template['output_format']}`")
    lines.append("- Preserve the section order defined above.")
    lines.append("- Keep subsection content under each heading concise and grouped.")
    lines.append("- After the workflow body is complete, append carry-over blocks in their own standalone sections or footer blocks.")

    lines.append("")
    lines.append("### Required Carry-Over Blocks")
    lines.append("")
    lines.append("- If a `## Survey` section exists in the source input, keep it visible after the workflow body.")
    lines.append("- If a `## Feedback` section exists in the source input, keep it visible after the workflow body.")
    lines.append("- If a `## Update Available` section exists in the source input, keep it visible after the workflow body.")
    lines.append("- If sponsor attribution exists in the source input, keep it as a visible standalone footer at the very end of the output.")
    lines.append("- Do not omit carry-over blocks as optional footer text. If they are missing, the product experience is broken.")

    lines.append("")
    lines.append("### Required Footer")
    lines.append("")
    lines.append("- Sponsor attribution, when present in the source input, must be appended after all workflow sections.")
    lines.append("- Do not absorb sponsor text into summary paragraphs, analysis sections, notes, or bullet lists.")
    lines.append("- Keep the sponsor brand and URL clearly visible in a standalone footer block.")
    lines.append(f"- Place the sponsor footer after the final `{section_divider}` divider.")

    if preferences:
        lines.append("")
        lines.append("### Merged with Your Preferences")
        lines.append("")
        if preferences.get("topics"):
            lines.append(f"- Topics of interest: {', '.join(preferences['topics'])}")
        if preferences.get("roles"):
            lines.append(f"- User perspective: {', '.join(preferences['roles'])}")
        if preferences.get("depth"):
            lines.append(f"- Depth: {preferences['depth']}")

    lines.append("")
    lines.append(section_divider)
    lines.append("")
    lines.append("Next step: organize today's news using this template, then keep the output in the exact structure above.")

    return "\n".join(lines)


def build_workflow_context(
    template: Dict[str, Any],
    preferences: Optional[dict] = None,
) -> Dict[str, Any]:
    """
    Build workflow execution context for use by artifact_renderer.
    """
    # Merge preference topics and template default topics
    template_topics = template.get("default_topics", [])
    pref_topics = preferences.get("topics", []) if preferences else []

    # Deduplicate while preserving order
    all_topics = list(dict.fromkeys(template_topics + pref_topics))

    context = {
        "workflow_id": template["id"],
        "workflow_title": template["title"],
        "focus_topics": all_topics,
        "focus_fields": template.get("focus_fields", []),
        "section_structure": template.get("section_structure", []),
        "output_format": template.get("output_format", "markdown_briefing"),
        "preferences_applied": bool(preferences),
    }

    if preferences:
        context["user_preferences"] = {
            "language": preferences.get("language", "zh-CN"),
            "depth": preferences.get("depth", "standard"),
            "strict_filtering": preferences.get("strict_filtering", False),
        }

    return context


def get_template_by_id(template_id: str) -> Optional[Dict[str, Any]]:
    """Get template by ID"""
    for template in WORKFLOW_TEMPLATES:
        if template["id"] == template_id:
            return template
    return None


def suggest_next_actions(template_id: str) -> List[str]:
    """Suggest next actions based on template"""
    suggestions = {
        "ai_coding_radar": [
            "Generate today's tech radar briefing",
            "Filter to show only Agent and AI Coding related news",
            "Save to knowledge base",
            "Set up weekly tech radar delivery",
        ],
        "content_creation_materials": [
            "Generate today's content material package",
            "Generate 3 blog title suggestions",
            "Organize into Newsletter format",
            "Extract short content suitable for communities",
        ],
        "knowledge_base_capture": [
            "Generate note format suitable for Obsidian",
            "Organize by research domain classification",
            "Add source links and citations",
            "Set up weekly research summary delivery",
        ],
        "product_opportunity_scan": [
            "Generate today's product opportunity scan",
            "Focus on competitor dynamics",
            "Organize into product weekly report format",
            "Set up daily product news delivery",
        ],
        "investment_strategy_brief": [
            "Generate today's investment research brief",
            "Focus on fundraising and M&A dynamics",
            "Organize into strategic decision reference format",
            "Set up daily investment research delivery",
        ],
    }
    return suggestions.get(template_id, ["Generate briefing", "Set up delivery", "Save to file"])
