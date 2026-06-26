#!/usr/bin/env python3
"""
Social Media Autopilot — OpenClaw ClawHub Skill
Generates a 7-day social media content calendar with Instagram-ready captions.
Powered by Gemini API.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv

# Load env
load_dotenv(Path("/Users/edwin/.openclaw/workspace/dreams-arts/.env"))

try:
    import google.generativeai as genai
except ImportError:
    print(json.dumps({"error": "google-generativeai not installed. Run: pip install google-generativeai"}), file=sys.stderr)
    sys.exit(1)


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("GEMINI_API_KEY not found in environment", file=sys.stderr)
    sys.exit(1)

genai.configure(api_key=GEMINI_API_KEY)

# Content mix ratios
DEFAULT_CONTENT_MIX = {
    "educational": 20,
    "promotional": 25,
    "engagement": 25,
    "behind_the_scenes": 20,
    "social_proof": 10,
}

# Optimal posting times (PR/EST timezone)
OPTIMAL_TIMES = {
    "instagram": ["9:00 AM", "12:00 PM", "5:30 PM"],
    "facebook": ["9:00 AM", "1:00 PM", "6:00 PM"],
    "twitter": ["8:00 AM", "12:00 PM", "5:00 PM"],
}

WEEKLY_THEMES = {
    "Monday": "Motivation / Behind the Scenes",
    "Tuesday": "Educational / Tips & Tricks",
    "Wednesday": "Work-in-Progress / Process",
    "Thursday": "Throwback / Testimonial",
    "Friday": "Product Spotlight / Feature",
    "Saturday": "Showcase / Portfolio",
    "Sunday": "Engagement / Fun & Community",
}

DAY_CONTENT_TYPES = {
    "Monday": "behind_the_scenes",
    "Tuesday": "educational",
    "Wednesday": "behind_the_scenes",
    "Thursday": "social_proof",
    "Friday": "promotional",
    "Saturday": "promotional",
    "Sunday": "engagement",
}


class SocialMediaAutopilot:
    """Generates 7-day social media content calendars."""

    def __init__(self, model_name: str = "gemini-2.0-flash"):
        self.model = genai.GenerativeModel(model_name)

    def _build_prompt(
        self,
        brand: str,
        niche: str,
        audience: str,
        tone: str,
        day_name: str,
        date_str: str,
        content_type: str,
        theme: str,
        platform: str,
    ) -> str:
        return f"""You are a world-class social media strategist. Generate ONE Instagram post for the following brand.

BRAND: {brand}
NICHE: {niche}
TARGET AUDIENCE: {audience}
TONE: {tone}
PLATFORM: {platform}

TODAY: {day_name}, {date_str}
THEME: {theme}
CONTENT TYPE: {content_type}

RULES:
- Caption must be 3-5 short paragraphs with line breaks between them
- Use 1-2 relevant emojis per paragraph (tasteful, not excessive)
- End with a clear CTA (DM, comment, tap link in bio, share, etc.)
- Include 15-20 hashtags after the caption (mix of high-volume and niche)
- Suggest a visual direction (what photo/video to post) — be SPECIFIC
- The caption must sound human and authentic, NOT corporate or AI-generated
- If the brand is bilingual, naturally mix English and Spanish

Return ONLY valid JSON with this exact structure (no markdown, no explanation):
{{
    "time": "the best posting time for this type of content (e.g. 9:00 AM)",
    "type": "{content_type}",
    "visual_direction": "specific description of what photo/video to create or use",
    "caption": "the full caption with \\n for line breaks",
    "hashtags": ["#tag1", "#tag2", "..."],
    "cta": "the call-to-action phrase used in the caption",
    "content_pillar": "{content_type}"
}}"""

    def _generate_post(
        self,
        brand: str,
        niche: str,
        audience: str,
        tone: str,
        day_name: str,
        date_str: str,
        content_type: str,
        theme: str,
        platform: str,
    ) -> dict:
        """Generate a single post using Gemini."""
        prompt = self._build_prompt(
            brand, niche, audience, tone, day_name, date_str, content_type, theme, platform
        )

        for attempt in range(3):
            try:
                response = self.model.generate_content(
                    prompt,
                    generation_config=genai.GenerationConfig(
                        temperature=0.8,
                        max_output_tokens=1024,
                    ),
                )

                text = response.text.strip()
                # Strip markdown fences if present
                if text.startswith("```"):
                    text = text.split("\n", 1)[1]
                    if text.endswith("```"):
                        text = text[:-3]
                    elif "```" in text:
                        text = text[: text.rfind("```")]
                    text = text.strip()

                return json.loads(text)

            except (json.JSONDecodeError, Exception) as e:
                print(f"Attempt {attempt + 1} failed for {day_name}: {e}", file=sys.stderr)
                if attempt == 2:
                    # Return a fallback post
                    return {
                        "time": "9:00 AM",
                        "type": content_type,
                        "visual_direction": f"High-quality photo related to {niche} - {theme}",
                        "caption": f"Happy {day_name}! More great things coming from {brand}.\n\nStay tuned!\n\n#Business #Local",
                        "hashtags": [f"#{brand.replace(' ', '')}", f"#{niche.replace(' ', '')}"],
                        "cta": "Stay tuned!",
                        "content_pillar": content_type,
                    }

    def generate(
        self,
        brand: str,
        niche: str,
        audience: str,
        tone: str = "engaging, authentic",
        platforms: str = "instagram",
        start_date: str | None = None,
    ) -> dict:
        """Generate a complete 7-day content calendar."""

        if start_date:
            start = datetime.strptime(start_date, "%Y-%m-%d")
        else:
            start = datetime.now() + timedelta(days=1)

        platform = platforms.split(",")[0].strip()  # Primary platform

        calendar = []
        for i in range(7):
            current_date = start + timedelta(days=i)
            day_name = current_date.strftime("%A")
            date_str = current_date.strftime("%Y-%m-%d")
            theme = WEEKLY_THEMES.get(day_name, "General")
            content_type = DAY_CONTENT_TYPES.get(day_name, "engagement")

            print(f"Generating {day_name} ({date_str}) — {theme}...", file=sys.stderr)

            post = self._generate_post(
                brand=brand,
                niche=niche,
                audience=audience,
                tone=tone,
                day_name=day_name,
                date_str=date_str,
                content_type=content_type,
                theme=theme,
                platform=platform,
            )

            calendar.append({
                "day": day_name,
                "date": date_str,
                "theme": theme,
                "posts": [post],
            })

        result = {
            "brand": brand,
            "niche": niche,
            "audience": audience,
            "tone": tone,
            "platforms": platforms,
            "strategy": {
                "content_mix": {k: f"{v}%" for k, v in DEFAULT_CONTENT_MIX.items()},
                "posting_frequency": "1 post/day",
                "best_times": OPTIMAL_TIMES.get(platform, OPTIMAL_TIMES["instagram"]),
                "weekly_themes": WEEKLY_THEMES,
            },
            "calendar": calendar,
            "generated_at": datetime.now().isoformat(),
        }

        return result


def main():
    parser = argparse.ArgumentParser(description="Social Media Autopilot — 7-day content calendar generator")
    parser.add_argument("--brand", required=True, help="Brand name")
    parser.add_argument("--niche", required=True, help="Business niche/industry")
    parser.add_argument("--audience", required=True, help="Target audience description")
    parser.add_argument("--tone", default="engaging, authentic", help="Brand voice/tone")
    parser.add_argument("--platforms", default="instagram", help="Target platforms (comma-separated)")
    parser.add_argument("--start-date", default=None, help="Calendar start date (YYYY-MM-DD)")
    parser.add_argument("--output", default=None, help="Output file path (default: stdout)")

    args = parser.parse_args()

    autopilot = SocialMediaAutopilot()
    result = autopilot.generate(
        brand=args.brand,
        niche=args.niche,
        audience=args.audience,
        tone=args.tone,
        platforms=args.platforms,
        start_date=args.start_date,
    )

    output = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Calendar saved to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
