---
name: social-media-autopilot
description: Generate a complete 7-day social media content calendar with Instagram-ready captions, hashtags, optimal posting times, and content mix strategy for any brand.
version: 1.0.0
tags: [social-media, instagram, content-planning, marketing]
---

# Social Media Autopilot

## Purpose
Generates a complete, ready-to-execute 7-day social media content calendar for any brand. Outputs Instagram-optimized captions with emojis, hashtags, CTAs, and a strategic content mix. Powered by Gemini API for caption generation.

## Requirements
- Python 3.10+
- `google-generativeai` package (`pip install google-generativeai`)
- `GEMINI_API_KEY` in `/Users/edwin/.openclaw/workspace/dreams-arts/.env`

## Usage

### From Command Line
```bash
python autopilot.py --brand "Dream's Arts Evolution" --niche "custom art & printing" --audience "small business owners, event planners, PR locals"
```

### Optional Flags
```bash
--tone "friendly, professional"    # Brand voice (default: "engaging, authentic")
--platforms "instagram,facebook"   # Target platforms (default: "instagram")
--start-date "2026-04-10"         # Calendar start date (default: tomorrow)
--output calendar.json            # Save to file instead of stdout
```

### From Python
```python
from autopilot import SocialMediaAutopilot

pilot = SocialMediaAutopilot()
calendar = pilot.generate(
    brand="Dream's Arts Evolution",
    niche="custom art & printing",
    audience="small business owners, event planners",
    tone="friendly, bilingual English-Spanish"
)
```

### Output Format
```json
{
  "brand": "Dream's Arts Evolution",
  "strategy": {
    "content_mix": {
      "educational": "20%",
      "promotional": "25%",
      "engagement": "25%",
      "behind_the_scenes": "20%",
      "user_generated_content": "10%"
    },
    "posting_frequency": "1-2 posts/day",
    "best_times": ["9:00 AM", "12:00 PM", "5:30 PM"]
  },
  "calendar": [
    {
      "day": "Monday",
      "date": "2026-04-10",
      "posts": [
        {
          "time": "9:00 AM",
          "type": "behind_the_scenes",
          "visual_direction": "Photo of team working on a custom order",
          "caption": "Every masterpiece starts with a blank canvas... and a LOT of coffee ☕🎨\n\nWatch our team bring your ideas to life, one print at a time.\n\n👉 DM us your next project idea!\n\n#CustomArt #PrintShop #CaguasPR #SmallBusinessPR #DreamsArtsEvolution",
          "hashtags": ["#CustomArt", "#PrintShop", "#CaguasPR"],
          "cta": "DM us your next project idea!",
          "content_pillar": "behind_the_scenes"
        }
      ]
    }
  ],
  "weekly_themes": {
    "monday": "Motivation Monday / Behind the Scenes",
    "tuesday": "Tutorial Tuesday / Educational",
    "wednesday": "Work-in-Progress Wednesday",
    "thursday": "Throwback Thursday / Testimonial",
    "friday": "Feature Friday / Product Spotlight",
    "saturday": "Showcase Saturday / Portfolio",
    "sunday": "Sunday Funday / Engagement"
  }
}
```

## How Claude Should Use This Skill

1. **Gather brand info**: Ask for or determine the brand name, niche, and target audience.
2. **Run the generator**: Execute via Bash with the appropriate flags.
3. **Review the calendar**: Check quality, variety, and strategic alignment before presenting.
4. **Send for approval**: Never publish directly. Present the calendar to Edwin for review.
5. **Schedule posts**: Once approved, use the calendar to schedule posts in the optimal windows.

## Content Mix Strategy
The skill balances 5 content pillars across the week:
- **Educational (20%)**: Tips, how-tos, industry insights
- **Promotional (25%)**: Product showcases, offers, new arrivals
- **Engagement (25%)**: Polls, questions, challenges, UGC prompts
- **Behind the Scenes (20%)**: Process, team, workspace, making-of
- **Social Proof (10%)**: Reviews, testimonials, customer features

## Caption Quality Rules
- Each caption is 3-5 lines with line breaks for readability
- Includes 1-2 relevant emojis per line (not excessive)
- Ends with a clear CTA (DM, comment, link in bio, etc.)
- 15-20 hashtags per post, mix of high-volume and niche
- Bilingual support (English/Spanish) when specified
