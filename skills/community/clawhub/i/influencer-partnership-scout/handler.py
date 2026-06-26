#!/usr/bin/env python3
import sys

PLATFORM_RULES = {
    'tiktok': ('short-form demo', 'nano / micro creators'),
    'instagram': ('visual lifestyle storytelling', 'micro / mid-tier creators'),
    'youtube': ('deeper product education', 'mid-tier creators'),
    'xiaohongshu': ('trust-led recommendation style', 'nano / micro creators'),
}

GOAL_MODES = {
    'awareness': 'Paid post or gifting with repost rights',
    'ugc': 'Gifting + usage-based creator brief',
    'affiliate': 'Affiliate-first with tracked code',
    'conversion': 'Micro creator seeding plus affiliate or paid hybrid',
}

RISK_NOTES = [
    'High follower count does not guarantee audience-brand fit.',
    'Overly commercial feeds may underperform for trust-sensitive products.',
    'Heuristic creator fit should be validated with manual content review before outreach.',
]

class ScoutEngine:
    def __init__(self, text: str):
        self.text = text.strip()
        self.lower = self.text.lower()
        self.platform = self._detect_platform()
        self.goal = self._detect_goal()
        self.tier = self._detect_tier()
        self.category = self._detect_category()

    def _detect_platform(self):
        for p in PLATFORM_RULES:
            if p in self.lower:
                return p
        if '小红书' in self.text:
            return 'xiaohongshu'
        return 'tiktok'

    def _detect_goal(self):
        for g in GOAL_MODES:
            if g in self.lower:
                return g
        if 'ugc' in self.lower:
            return 'ugc'
        if 'awareness' in self.lower:
            return 'awareness'
        if 'affiliate' in self.lower:
            return 'affiliate'
        if '转化' in self.text:
            return 'conversion'
        return 'conversion'

    def _detect_tier(self):
        if 'nano' in self.lower or '1k' in self.lower:
            return 'nano'
        if 'micro' in self.lower or '10k' in self.lower or '80k' in self.lower:
            return 'micro'
        if 'mid' in self.lower or '100k' in self.lower:
            return 'mid-tier'
        return 'micro'

    def _detect_category(self):
        for c in ['skincare', 'pet', 'home', 'beauty', 'fashion', 'supplement', 'organizer']:
            if c in self.lower:
                return c
        if '护肤' in self.text:
            return 'skincare'
        if '宠物' in self.text:
            return 'pet'
        if '收纳' in self.text:
            return 'home organization'
        return 'ecommerce brand'

    def fit_analysis(self):
        content_style, default_tier = PLATFORM_RULES[self.platform]
        audience_fit = 'High' if self.category in ['skincare', 'pet', 'beauty', 'home organization'] else 'Medium'
        conversion_likelihood = 'Medium-High' if self.goal in ['ugc', 'conversion', 'affiliate'] else 'Medium'
        return content_style, default_tier, audience_fit, conversion_likelihood

    def render(self):
        content_style, default_tier, audience_fit, conversion_likelihood = self.fit_analysis()
        mode = GOAL_MODES[self.goal]
        lines = [
            '# Influencer Partnership Scout Brief', '',
            f'**Campaign goal:** {self.goal}',
            f'**Platform focus:** {self.platform}',
            f'**Category:** {self.category}',
            '**Method note:** This shortlist is heuristic and template-based. No real social platform data was accessed.', '',
            '## Influencer Shortlist Framework',
            f'- **High fit tier:** {self.tier} creators with strong {self.category} relevance and authentic {content_style}',
            f'- **Test fit tier:** adjacent niche creators who can translate the product into a problem-solution or lifestyle use case',
            f'- **Low priority tier:** large creators with weak audience overlap or overly generic sponsorship patterns', '',
            '## Partnership Fit Analysis',
            f'- Brand alignment: **High** if creator tone feels educational, believable, and consistent with {self.category}',
            f'- Audience alignment: **{audience_fit}**',
            f'- Content compatibility: **High** on {self.platform} for {content_style}',
            f'- Conversion likelihood: **{conversion_likelihood}**',
            f'- Suggested creator baseline: **{self.tier or default_tier}**', '',
            '## Recommended Partnership Mode',
            f'- Primary mode: **{mode}**',
            '- Secondary mode: test one backup offer structure to compare response quality', '',
            '## Contact Brief',
            '- Opening angle: lead with why the product fits the creator’s audience and content rhythm',
            '- What to mention first: category relevance, creator-audience fit, and the simplest partnership ask',
            '- What to avoid: generic praise, vague CTA, and asking for a full campaign before validating fit', '',
            '## Outreach Recommendation',
            '1. Start with a small high-fit batch, not a broad list blast.',
            '2. Separate gifting candidates from paid-post candidates.',
            '3. Track reply quality, content authenticity, and audience resonance before scaling.', '',
            '## Risk Notes'
        ]
        for note in RISK_NOTES:
            lines.append(f'- {note}')
        return '\n'.join(lines)

def handle(user_input: str) -> str:
    return ScoutEngine(user_input).render()

if __name__ == '__main__':
    print(handle(sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()))
