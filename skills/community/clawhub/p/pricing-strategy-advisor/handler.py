#!/usr/bin/env python3
import sys
from typing import Any, Dict, List, Union

ActionInput = Union[str, Dict[str, Any]]

OBJECTIVE_RULES = {
    'Launch Pricing': ['launch', 'new product', 'intro', 'introduction', 'gtm'],
    'Discount Discipline': ['discount', 'coupon', 'promo', 'markdown', 'sale'],
    'Price Architecture': ['price ladder', 'architecture', 'good better best', 'tier', 'premium', 'entry price'],
    'Margin Recovery': ['margin', 'profit', 'cost', 'gross margin', 'contribution'],
    'Growth Push': ['growth', 'volume', 'share', 'conversion', 'acquisition'],
}

SIGNAL_RULES = {
    'Cost / Margin Pressure': ['cost', 'margin', 'profit', 'contribution'],
    'Elasticity / Conversion': ['conversion', 'cvr', 'elasticity', 'volume', 'sell-through', 'sell through'],
    'Competitor Pressure': ['competitor', 'market', 'benchmark', 'price war', 'marketplace'],
    'Channel Conflict': ['channel', 'retailer', 'amazon', 'marketplace', 'map', 'parity'],
    'Promo Fatigue': ['discount', 'coupon', 'promo', 'markdown', 'sale fatigue'],
    'Bundle / Pack Mix': ['bundle', 'pack', 'multi-buy', 'pack size', 'tier'],
}

GUARDRAIL_RULES = {
    'Minimum margin floor': ['margin floor', 'gross margin', 'contribution'],
    'Brand or MAP protection': ['map', 'brand', 'premium', 'positioning'],
    'Channel parity discipline': ['parity', 'retailer', 'marketplace', 'channel'],
    'Inventory aging pressure': ['aged', 'aging', 'clearance', 'inventory'],
    'Launch learning speed': ['launch', 'test', 'learn', 'pilot'],
}


def _score_rules(text: str, rules: Dict[str, List[str]]) -> Dict[str, int]:
    return {name: sum(1 for keyword in keywords if keyword in text) for name, keywords in rules.items()}


def _join_list(items: List[str]) -> str:
    return ', '.join(items) if items else 'None explicitly provided'


class PricingStrategyAdvisor:
    def __init__(self, user_input: ActionInput):
        self.raw = user_input
        self.text = self._normalize_input(user_input)
        self.lower = self.text.lower()
        self.objective = self._detect_objective()
        self.signals = self._detect_signals()
        self.guardrails = self._detect_guardrails()

    def _normalize_input(self, user_input: ActionInput) -> str:
        if isinstance(user_input, dict):
            chunks: List[str] = []
            for key in ['objective', 'prices', 'signals', 'constraints', 'notes']:
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
        return best if scores[best] > 0 else 'Price Architecture'

    def _detect_signals(self) -> List[str]:
        matched = [name for name, keywords in SIGNAL_RULES.items() if any(keyword in self.lower for keyword in keywords)]
        return matched or ['Cost / Margin Pressure', 'Elasticity / Conversion', 'Competitor Pressure']

    def _detect_guardrails(self) -> List[str]:
        matched = [name for name, keywords in GUARDRAIL_RULES.items() if any(keyword in self.lower for keyword in keywords)]
        base = matched or ['Minimum margin floor', 'Brand or MAP protection']
        if 'Minimum margin floor' not in base:
            base.append('Minimum margin floor')
        return base[:4]

    def _moves(self) -> List[str]:
        if self.objective == 'Launch Pricing':
            return [
                'Start with a learnable price band rather than the deepest possible discount at launch.',
                'Use one clean introductory offer and a short review point instead of stacking coupons early.',
                'Protect the premium narrative if the product depends on perceived quality, not just trial volume.',
                'Predefine what evidence would justify a price move after the first demand cycle.',
            ]
        if self.objective == 'Discount Discipline':
            return [
                'Reduce promo sprawl by tightening where and when discounts appear, rather than cutting list price first.',
                'Separate traffic-driving offers from margin-destructive blanket markdowns.',
                'Reserve the deepest discounting for genuinely aged or tactical inventory, not habit-driven cadence.',
                'Use bundles, packs, or threshold offers to preserve unit economics before deeper discounting.',
            ]
        if self.objective == 'Margin Recovery':
            return [
                'Recover margin first through architecture, pack, mix, or selective price moves before blunt across-the-board increases.',
                'Raise prices where differentiation is strongest and conversion is less discount-dependent.',
                'Keep an entry-point option if it protects acquisition while premium or bundle offers recover margin.',
                'Explain the reason for any price change in plain business terms so the team can defend it internally and externally.',
            ]
        if self.objective == 'Growth Push':
            return [
                'Use pricing to sharpen the conversion path, not to subsidize low-quality demand indefinitely.',
                'Anchor volume on the hero offers that create repeatable acquisition or retention value.',
                'Use bundles or tier progression to lift AOV before defaulting to simpler discount depth.',
                'Keep the move reversible so learning arrives before margin damage compounds.',
            ]
        return [
            'Clarify the good-better-best logic so each tier earns its place through clear value separation.',
            'Reduce overlap between nearby price points that confuse buyers or dilute premium progression.',
            'Use pack, bundle, or service differences to support tiering instead of cosmetic SKU inflation.',
            'Make sure the entry offer acquires, the core offer monetizes, and the premium offer signals upside.',
        ]

    def _test_plan(self) -> List[str]:
        return [
            'Run one focused pricing test on a clearly scoped SKU family or offer set, not across the full catalog at once.',
            'Define the primary win metric before launch, such as contribution margin, conversion, AOV, or net revenue per session.',
            'Track new versus returning customer behavior separately so short-term lift is not mistaken for structural improvement.',
            'Set a review checkpoint early enough to reverse the move if channel conflict or margin damage appears quickly.',
        ]

    def _monitoring(self) -> List[str]:
        items = [
            'Monitor gross margin, unit contribution, conversion rate, and AOV together instead of debating only one metric.',
            'Watch refund, cancel, and service signal changes after pricing moves so hidden demand quality problems surface early.',
            'Review channel-level divergence, especially if marketplaces or retail partners react differently than DTC.',
        ]
        if 'Competitor Pressure' in self.signals:
            items.append('Treat competitor references as context, not automatic permission to copy a price war.')
        return items[:4]

    def _assumptions(self) -> List[str]:
        notes = [
            'This brief is heuristic and depends on the user-supplied view of costs, pricing, and channel context.',
            'No live competitor crawling, ERP costing, or analytics feed was accessed.',
            'Elasticity is inferred from context unless the user provides direct experimental evidence.',
        ]
        if 'Channel Conflict' not in self.signals:
            notes.append('Channel conflict appears lightly referenced, so parity and retailer reaction risk may be understated.')
        return notes

    def render(self) -> str:
        lines: List[str] = []
        lines.append('# Pricing Strategy Advisor Brief')
        lines.append('')
        lines.append(f'**Primary objective:** {self.objective}')
        lines.append(f'**Pricing signals referenced:** {_join_list(self.signals)}')
        lines.append(f'**Guardrails:** {_join_list(self.guardrails)}')
        lines.append('**Method note:** This is a heuristic pricing strategy brief. No live competitor, ERP, or analytics data was accessed.')
        lines.append('')
        lines.append('## Pricing Posture Summary')
        lines.append('- Start with the business trade-off that matters most: margin recovery, growth, positioning, or cleaner architecture.')
        lines.append('- Separate structural price problems from temporary inventory, promo, or channel noise.')
        lines.append('- Prefer moves that can be tested and reversed before they become permanent habits.')
        lines.append('')
        lines.append('## Recommended Moves')
        for idx, move in enumerate(self._moves(), 1):
            lines.append(f'{idx}. {move}')
        lines.append('')
        lines.append('## Test Design')
        for bullet in self._test_plan():
            lines.append(f'- {bullet}')
        lines.append('')
        lines.append('## Guardrails and Escalation')
        for guardrail in self.guardrails:
            lines.append(f'- {guardrail}: confirm ownership and escalation before any durable price change.')
        lines.append('')
        lines.append('## Metrics to Monitor')
        for item in self._monitoring():
            lines.append(f'- {item}')
        lines.append('')
        lines.append('## Assumptions and Limits')
        for note in self._assumptions():
            lines.append(f'- {note}')
        return '\n'.join(lines)


def handle(user_input: ActionInput) -> str:
    return PricingStrategyAdvisor(user_input).render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
