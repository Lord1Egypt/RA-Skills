#!/usr/bin/env python3
import sys
from typing import Any, Dict, List, Union

OBJECTIVE_RULES = {
    'Acquire First Orders': ['first orders', 'go live', 'launch', 'rollout', 'sell now'],
    'Validate Demand': ['validate', 'test demand', 'demand test', 'pilot', 'soft launch'],
    'Increase AOV': ['aov', 'bundle', 'upsell', 'premium tier', 'higher basket'],
    'Build Waitlist': ['waitlist', 'prelaunch', 'pre-launch', 'lead capture', 'collect leads'],
    'Seasonal Campaign Support': ['seasonal', 'holiday', 'mother\'s day', 'gift', 'campaign', 'collection'],
}

CHANNEL_RULES = {
    'Shopify / DTC Store': ['shopify', 'dtc', 'storefront', 'pdp'],
    'Amazon': ['amazon', 'listing'],
    'Email / CRM': ['email', 'crm', 'klaviyo'],
    'Meta Ads': ['meta', 'facebook', 'instagram', 'paid social'],
    'TikTok Shop / Short Video': ['tiktok', 'douyin', 'short video'],
    'Xiaohongshu / Creator Seeding': ['xiaohongshu', 'rednote', 'creator', 'ugc', 'influencer'],
}

ASSET_RULES = {
    'PDP / Listing Copy': ['pdp', 'listing', 'product page', 'title', 'bullets', 'description'],
    'Images / Video': ['image', 'images', 'photo', 'photos', 'video', 'creative', 'demo'],
    'UGC / Social Proof': ['ugc', 'review', 'reviews', 'testimonial', 'creator'],
    'FAQ / Support': ['faq', 'support', 'customer support', 'chat', 'objection'],
    'Tracking / Analytics': ['tracking', 'analytics', 'pixel', 'utm', 'measurement'],
    'Inventory / Packaging': ['inventory', 'stock', 'packaging', 'warehouse', 'fulfillment'],
}

LaunchInput = Union[str, Dict[str, Any]]


def _score_rules(text: str, rules: Dict[str, List[str]]) -> Dict[str, int]:
    return {name: sum(1 for keyword in keywords if keyword in text) for name, keywords in rules.items()}


def _join(items: List[str]) -> str:
    return ', '.join(items) if items else 'None explicitly provided'


class NewProductLaunchCopilot:
    def __init__(self, user_input: LaunchInput):
        self.raw = user_input
        self.text = self._normalize_input(user_input)
        self.lower = self.text.lower()
        self.objective = self._detect_objective()
        self.channels = self._detect_channels()
        self.assets = self._detect_assets()

    def _normalize_input(self, user_input: LaunchInput) -> str:
        if isinstance(user_input, dict):
            chunks: List[str] = []
            for key in ['product', 'objective', 'audience', 'channels', 'assets', 'constraints', 'notes']:
                value = user_input.get(key)
                if not value:
                    continue
                if isinstance(value, list):
                    value = ', '.join(str(item) for item in value)
                chunks.append(f'{key}: {value}')
            return ' | '.join(chunks)
        return str(user_input or '').strip()

    def _detect_objective(self) -> str:
        scores = _score_rules(self.lower, OBJECTIVE_RULES)
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else 'Acquire First Orders'

    def _detect_channels(self) -> List[str]:
        matched = [name for name, keywords in CHANNEL_RULES.items() if any(keyword in self.lower for keyword in keywords)]
        return matched or ['Shopify / DTC Store', 'Email / CRM']

    def _detect_assets(self) -> List[str]:
        matched = [name for name, keywords in ASSET_RULES.items() if any(keyword in self.lower for keyword in keywords)]
        base = matched or ['PDP / Listing Copy', 'Images / Video', 'Tracking / Analytics']
        if 'Inventory / Packaging' not in base:
            base.append('Inventory / Packaging')
        return base[:5]

    def _launch_thesis(self) -> List[str]:
        thesis = [
            'Lead with one clear promise tied to a real user problem, not a long list of features.',
            'Translate feature claims into benefits and proof points before writing channel copy.',
            'Make the go-live decision depend on readiness, not only on the calendar date.',
        ]
        if self.objective == 'Validate Demand':
            thesis[2] = 'Keep the launch scoped like a learning test so the team can measure demand quality before scaling.'
        if self.objective == 'Build Waitlist':
            thesis[2] = 'Bias the launch toward lead capture, proof gathering, and opt-in quality before the full sales push.'
        if self.objective == 'Increase AOV':
            thesis[1] = 'Frame the offer around bundle logic, premium step-up value, and objection handling that protects basket size.'
        return thesis

    def _messaging_rows(self) -> List[Dict[str, str]]:
        return [
            {
                'angle': 'Hero Message',
                'benefit': 'What the product solves fastest or most clearly for the target buyer.',
                'proof': 'Ingredient, feature, demo, review, or use-case evidence that reduces disbelief.',
                'channel': 'Homepage hero, PDP headline, launch email subject, creator brief opening.',
            },
            {
                'angle': 'Objection Handling',
                'benefit': 'Address price, fit, complexity, shipping, or trust concerns before they stall action.',
                'proof': 'FAQ, comparison chart, shipping note, guarantee, or support macro.',
                'channel': 'PDP module, support prep, ad comments, retention email.',
            },
            {
                'angle': 'Offer Logic',
                'benefit': 'Explain why the buyer should act now and which option is best for them.',
                'proof': 'Bundle savings, launch-only bonus, tiered pricing, waitlist perk, or stock note.',
                'channel': 'Offer banner, email CTA, paid-social hook, creator talking point.',
            },
        ]

    def _checklist(self) -> List[str]:
        items = [
            'Confirm PDP or listing copy, value hierarchy, pricing, and main objections.',
            'Review images, demo video, UGC, and any claim-sensitive creative before publishing.',
            'Lock FAQ, customer-support macros, and internal escalation notes for launch week.',
            'Verify tracking, UTMs, attribution assumptions, and launch reporting ownership.',
            'Check inventory, packaging, shipping promises, and any constrained components before spend ramps.',
        ]
        if self.objective == 'Build Waitlist':
            items.insert(0, 'Create a clear waitlist capture mechanic and define what happens after sign-up.')
        return items[:6]

    def _timeline(self) -> List[str]:
        return [
            'T-21: finalize positioning, launch objective, and must-have assets.',
            'T-14: review copy, creative, FAQ, tracking plan, and inventory constraints.',
            'T-7: confirm channel sequencing, owner responsibilities, and go/no-go blockers.',
            'T-3: QA the live experience, links, offer logic, support coverage, and stock visibility.',
            'T-0: monitor launch execution, top objections, attribution sanity, and inventory pressure.',
            'T+3: capture early signal quality, channel performance, and urgent fixes.',
            'T+7: document lessons, repeatable assets, and what should scale, pause, or revise.',
        ]

    def _kpis(self) -> List[str]:
        items = [
            'Day-1: traffic quality, CTR, PDP engagement, add-to-cart rate, and support-ticket themes.',
            'Week-1: conversion rate, first-order volume, CAC or ROAS quality, and stock health.',
            'Launch window: contribution quality, refund risk, AOV impact, and repeatable channel signals.',
        ]
        if self.objective == 'Build Waitlist':
            items[0] = 'Day-1: waitlist opt-in rate, landing-page conversion, and source quality.'
        if self.objective == 'Validate Demand':
            items[1] = 'Week-1: sample order quality, conversion by audience, and whether objection patterns repeat.'
        if self.objective == 'Increase AOV':
            items[2] = 'Launch window: bundle take rate, upsell attachment rate, and margin mix quality.'
        return items

    def _risks(self) -> List[str]:
        items = [
            'Weak proof points can make the product message sound interesting but not credible enough to convert.',
            'Asset completeness can hide operational gaps, especially FAQ, support prep, and measurement ownership.',
            'A fixed go-live date can create false urgency if inventory or creative quality is still unstable.',
            'Tracking gaps can make the team overreact to noisy early data.',
        ]
        if 'Inventory / Packaging' not in self.assets:
            items.append('Inventory and packaging assumptions were not clearly referenced, so launch-readiness confidence is lower.')
        return items[:5]

    def _assumptions(self) -> List[str]:
        return [
            'This brief is heuristic and depends on the product, audience, and asset notes the user supplied.',
            'Creative execution quality, legal review, and live media performance still require human ownership.',
            'Stock, claim, pricing, and launch-delay decisions should remain human-approved.',
        ]

    def render(self) -> str:
        lines: List[str] = []
        lines.append('# New Product Launch Brief')
        lines.append('')
        lines.append(f'**Launch objective:** {self.objective}')
        lines.append(f'**Channels referenced:** {_join(self.channels)}')
        lines.append(f'**Assets referenced:** {_join(self.assets)}')
        lines.append('**Method note:** This is a heuristic launch-planning brief. No live storefront, ads account, project-management board, or analytics stack was accessed.')
        lines.append('')
        lines.append('## Launch Brief')
        for bullet in self._launch_thesis():
            lines.append(f'- {bullet}')
        lines.append('')
        lines.append('## Messaging Matrix')
        lines.append('| Angle | Benefit to land | Proof to include | Best-fit channel use |')
        lines.append('|---|---|---|---|')
        for row in self._messaging_rows():
            lines.append(f'| {row["angle"]} | {row["benefit"]} | {row["proof"]} | {row["channel"]} |')
        lines.append('')
        lines.append('## Readiness Checklist')
        for idx, item in enumerate(self._checklist(), 1):
            lines.append(f'{idx}. {item}')
        lines.append('')
        lines.append('## Timeline and Dependencies')
        for item in self._timeline():
            lines.append(f'- {item}')
        lines.append('')
        lines.append('## KPI Framework')
        for item in self._kpis():
            lines.append(f'- {item}')
        lines.append('')
        lines.append('## Risk Watchlist')
        for item in self._risks():
            lines.append(f'- {item}')
        lines.append('')
        lines.append('## Post-Launch Learning Loop')
        lines.append('- Capture what message, channel, offer, and objection pattern created the cleanest demand signal.')
        lines.append('- Save one reusable launch asset set and one reusable checklist improvement for the next launch.')
        lines.append('- Separate signal quality from hype so the next decision is grounded in evidence.')
        lines.append('')
        lines.append('## Assumptions and Limits')
        for note in self._assumptions():
            lines.append(f'- {note}')
        return '\n'.join(lines)


def handle(user_input: LaunchInput) -> str:
    return NewProductLaunchCopilot(user_input).render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
