#!/usr/bin/env python3
import sys
from typing import Dict, List

STAGE_RULES = {
    'Home / Landing': ['home', 'homepage', 'landing', 'hero', 'above the fold'],
    'Search / Navigation': ['search', 'navigation', 'menu', 'filter', 'sort'],
    'Product Detail Page': ['pdp', 'product page', 'detail page', 'gallery', 'size guide', 'variant'],
    'Cart': ['cart', 'basket', 'bag'],
    'Checkout': ['checkout', 'payment', 'address', 'form'],
    'Post-purchase / Reorder': ['reorder', 'repeat', 'subscription', 'post-purchase', 'post purchase'],
}

ISSUE_LIBRARY = {
    'Home / Landing': {
        'issue': 'Above-the-fold hierarchy is not focused enough for mobile shoppers.',
        'why': 'Too many competing blocks dilute the main value proposition and CTA.',
        'fix': 'Reduce competing messages, strengthen the primary CTA, and surface one trust cue early.',
        'effort': 'Medium',
    },
    'Search / Navigation': {
        'issue': 'Discovery flow may require too many taps before users reach a viable product set.',
        'why': 'Mobile shoppers abandon when filters, sort logic, or categories feel hard to scan.',
        'fix': 'Simplify top-level navigation and elevate the highest-value filter shortcuts.',
        'effort': 'Medium',
    },
    'Product Detail Page': {
        'issue': 'PDP confidence signals are likely too weak or too buried.',
        'why': 'Mobile buyers need fit, shipping, and trust information near the decision point.',
        'fix': 'Move proof, shipping summary, and product guidance closer to the CTA and variant area.',
        'effort': 'Low-Medium',
    },
    'Cart': {
        'issue': 'Cart may not reinforce urgency, savings logic, or shipping clarity strongly enough.',
        'why': 'Users hesitate when the next-step value and cost transparency are unclear.',
        'fix': 'Highlight shipping thresholds, bundle logic, and checkout benefits above the fold.',
        'effort': 'Low',
    },
    'Checkout': {
        'issue': 'Checkout burden or trust friction is suppressing completion.',
        'why': 'Long forms, weak reassurance, and late surprises create major mobile drop-off.',
        'fix': 'Shorten the form, enable autofill, and place payment, delivery, and return reassurance near action buttons.',
        'effort': 'Medium',
    },
    'Post-purchase / Reorder': {
        'issue': 'The flow likely misses easy repeat-purchase or reorder entry points.',
        'why': 'Without low-friction next actions, retention value leaks after the first order.',
        'fix': 'Add one-tap reorder cues, reorder reminders, and clearer post-purchase benefit framing.',
        'effort': 'Medium',
    },
}

GOAL_RULES = {
    'checkout': ['checkout', 'payment', 'form'],
    'add-to-cart': ['add to cart', 'atc', 'cart'],
    'conversion': ['conversion', 'cvr', 'purchase'],
    'repeat-purchase': ['repeat', 'reorder', 'retention', 'subscription'],
}


class MobileCommerceAuditor:
    def __init__(self, text: str):
        self.text = (text or '').strip()
        self.lower = self.text.lower()
        self.mode = 'deep' if any(word in self.lower for word in ['deep', 'full audit', 'comprehensive', 'full']) else 'quick'
        self.goal = self._detect_goal()
        self.stages = self._detect_stages()

    def _detect_goal(self) -> str:
        for goal, keywords in GOAL_RULES.items():
            if any(word in self.lower for word in keywords):
                return goal
        return 'conversion'

    def _detect_stages(self) -> List[str]:
        stages = [stage for stage, keywords in STAGE_RULES.items() if any(word in self.lower for word in keywords)]
        return stages or ['Home / Landing', 'Product Detail Page', 'Cart', 'Checkout']

    def _severity(self, stage: str) -> str:
        if stage == 'Checkout':
            return 'High'
        if stage == 'Product Detail Page' and self.goal in ('conversion', 'add-to-cart'):
            return 'High'
        if stage == 'Post-purchase / Reorder' and self.goal == 'repeat-purchase':
            return 'High'
        return 'Medium'

    def render(self) -> str:
        lines: List[str] = []
        lines.append('# Mobile Commerce UX Audit')
        lines.append('')
        lines.append(f'**Mode:** {self.mode}')
        lines.append(f'**Primary goal:** {self.goal}')
        lines.append('**Method note:** This audit is heuristic and checklist-based. No real analytics, heatmap, or session-replay tool was accessed.')
        lines.append('')
        lines.append('## Executive Summary')
        lines.append('- The audit focuses on conversion-critical mobile moments where clarity, trust, and tap effort matter most.')
        lines.append('- Findings are prioritized for revenue relevance first, not purely for visual polish.')
        lines.append('')
        lines.append('## Prioritized Findings')
        for stage in self.stages:
            issue = ISSUE_LIBRARY[stage]
            lines.append(f'### {stage}')
            lines.append(f'- Severity: {self._severity(stage)}')
            lines.append(f'- Core issue: {issue["issue"]}')
            lines.append(f'- Why it matters: {issue["why"]}')
            lines.append(f'- Recommended fix: {issue["fix"]}')
            lines.append(f'- Effort: {issue["effort"]}')
            lines.append('')
        lines.append('## Quick Wins')
        quick_wins = [
            'Expose one shipping or returns reassurance block closer to the main CTA.',
            'Reduce competing mobile modules above the first conversion action.',
            'Shorten microcopy where it slows scanning on small screens.',
        ]
        for item in quick_wins:
            lines.append(f'- {item}')
        lines.append('')
        lines.append('## Experiment Backlog')
        lines.append('| Test idea | Expected effect | Effort |')
        lines.append('|---|---|---|')
        lines.append('| Sticky primary CTA with trust cue | Improve click-through to the next step | Low-Medium |')
        lines.append('| Earlier shipping / returns summary | Reduce hesitation near purchase action | Low |')
        lines.append('| Shorter checkout form or autofill emphasis | Lift completion on mobile checkout | Medium |')
        lines.append('| Variant guidance closer to CTA | Improve PDP confidence and add-to-cart rate | Medium |')
        lines.append('')
        lines.append('## Assumptions and Gaps')
        lines.append('- This output assumes the provided notes represent the main mobile path and not an edge-case flow.')
        lines.append('- Real analytics and usability evidence should be used to validate the order of fixes.')
        return '\n'.join(lines)


def handle(user_input: str) -> str:
    return MobileCommerceAuditor(user_input).render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
