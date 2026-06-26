#!/usr/bin/env python3
"""
Instagram Marketing Product Extractor

Extracts product information from e-commerce URLs for Instagram content generation.
Supports: Amazon, Shopify, Taobao, JD, and generic e-commerce sites.

Uses SkillBoss API Hub (https://api.heybossai.com/v1/pilot) for web scraping
and AI-powered structured data extraction.

Usage:
    python extract_product.py <url>

Environment:
    SKILLBOSS_API_KEY  — SkillBoss API Hub key

Output:
    JSON object with product details for content generation
"""

import sys
import json
import os
import requests
from typing import Dict

SKILLBOSS_API_KEY = os.environ["SKILLBOSS_API_KEY"]
API_BASE = "https://api.heybossai.com/v1"


def pilot(body: dict) -> dict:
    r = requests.post(
        f"{API_BASE}/pilot",
        headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    return r.json()


class ProductExtractor:
    """Extract product information from e-commerce URLs via SkillBoss API Hub."""

    def __init__(self, url: str):
        self.url = url

    def extract(self) -> Dict:
        """Extract product info using SkillBoss scraping + chat."""
        try:
            # Step 1: Scrape the product page via SkillBoss API Hub
            scrape_result = pilot({
                "type": "scraper",
                "inputs": {"url": self.url},
                "prefer": "balanced"
            })
            page_content = scrape_result["result"]["data"]["markdown"]

            # Step 2: Use SkillBoss LLM to extract structured product data
            extraction_prompt = f"""Extract product information from this page content and return a JSON object with exactly these fields:
- name: product name (string)
- price: product price (string)
- description: brief product description, max 200 characters (string)
- features: list of up to 5 key product features (array of strings)
- target_audience: who this product is for, e.g. Men/Women/Kids/Gamers/Fitness Enthusiasts/Homeowners/General Consumers (string)
- usp: unique selling proposition in one sentence (string)
- platform: e-commerce platform name, one of Amazon/Shopify/Taobao/JD/Generic (string)

Page URL: {self.url}
Page Content:
{page_content[:3000]}

Return ONLY valid JSON with no markdown fences."""

            chat_result = pilot({
                "type": "chat",
                "inputs": {
                    "messages": [{"role": "user", "content": extraction_prompt}]
                },
                "prefer": "balanced"
            })
            text = chat_result["result"]["choices"][0]["message"]["content"]

            product_data = json.loads(text)
            product_data["url"] = self.url
            product_data["content_type"] = self._suggest_content_type(product_data)
            return product_data

        except Exception as e:
            return {
                "error": f"Extraction failed: {str(e)}",
                "manual_extraction_needed": True,
                "url": self.url,
                "extraction_guide": {
                    "product_name": "Copy from page title or h1",
                    "price": "Find price display on page",
                    "features": "Look for bullet points or product highlights (3-5 items)",
                    "description": "Copy product description (first paragraph)",
                    "target_audience": "Who would buy this? (Men/Women/Kids/etc)",
                    "brand_tone": "Is it luxury, playful, minimal, or bold?",
                    "existing_images": "Note if there are product photos to reference"
                }
            }

    def _suggest_content_type(self, data: Dict) -> str:
        """Suggest best Instagram content format."""
        name = data.get("name", "").lower()
        features = data.get("features", [])

        if any(w in name for w in ["fashion", "clothing", "shoe"]):
            return "Carousel (Lifestyle + Details + Fit)"
        elif any(w in name for w in ["video", "camera", "audio", "speaker"]):
            return "Reel (Demo + Usage Scenes)"
        elif len(features) >= 3:
            return "Carousel (Feature-by-feature breakdown)"
        else:
            return "Feed Post (High-quality product shot)"


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: python extract_product.py <url>",
            "example": "python extract_product.py https://www.amazon.com/dp/B08N5WRWNW"
        }, indent=2))
        sys.exit(1)

    url = sys.argv[1]
    extractor = ProductExtractor(url)
    result = extractor.extract()

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
