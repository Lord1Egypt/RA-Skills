#!/usr/bin/env python3
import sys
from typing import Any, Dict, List, Union

REVIEW_MODE_RULES = {
    'Daily Watchlist': ['daily', 'today', 'watchlist', 'monitor', 'health check'],
    'Replenishment Planning': ['replenishment', 'reorder', 'restock', 'days of cover', 'cover', 'buy plan'],
    'Pre-Promo Risk Review': ['promo', 'promotion', 'campaign', 'holiday', 'launch', 'event'],
    'Cash-Risk Review': ['cash', 'aging', 'overstock', 'markdown', 'month-end', 'cashflow'],
}

RISK_RULES = {
    'Stockout Risk': {
        'keywords': ['stockout', 'oos', 'out of stock', 'run out', 'low stock', 'cover'],
        'why': 'The best sellers can lose demand quickly when available stock falls below realistic lead-time protection.',
        'check': 'Review days of cover, top-SKU share, and whether inbound timing really protects the promo window.',
        'action': 'Reorder, expedite, or reduce exposure before demand turns into lost revenue.',
    },
    'Overstock Risk': {
        'keywords': ['overstock', 'excess', 'slow moving', 'storage', 'too much stock'],
        'why': 'Too much stock can trap cash, reduce flexibility, and force discounting later.',
        'check': 'Compare stock depth against recent velocity, margin quality, and storage pressure.',
        'action': 'Slow buying, rebalance channels, or build a controlled sell-down plan.',
    },
    'Aging Inventory Risk': {
        'keywords': ['aging', 'aged', 'dead stock', 'markdown', 'expiry', 'expiring'],
        'why': 'Older inventory often turns into cash drag, quality risk, or forced markdown exposure.',
        'check': 'Review aging buckets, repeat markdown history, and which SKUs no longer have a healthy sell-through story.',
        'action': 'Bundle, liquidate, or deliberately deprioritize future buys for the affected SKUs.',
    },
    'Inbound Delay Risk': {
        'keywords': ['inbound', 'eta', 'delay', 'lead time', 'supplier', 'purchase order', 'po'],
        'why': 'A stable stock position can become fragile quickly when supplier timing is unreliable.',
        'check': 'Inspect vendor reliability, ETA confidence, and whether alternative supply exists.',
        'action': 'Escalate supplier follow-up, pull forward reorders, or line up backup supply options.',
    },
    'Promo Readiness Risk': {
        'keywords': ['promo', 'promotion', 'campaign', 'launch', 'event', 'peak'],
        'why': 'Promotions magnify existing inventory weaknesses and can turn a manageable issue into a visible miss.',
        'check': 'Stress test hero SKUs, substitute options, and channel allocation before spend increases.',
        'action': 'Adjust promo intensity, shift spend, or protect inventory for the highest-value channels.',
    },
}

SIGNAL_RULES = {
    'On-hand / Available Stock': ['on-hand', 'on hand', 'available', 'reserved', 'stock'],
    'Inbound / PO Status': ['inbound', 'po', 'purchase order', 'eta', 'backorder'],
    'Sales Velocity': ['velocity', 'sales', 'sell-through', 'sell through', 'demand'],
    'Lead Time / Supplier Reliability': ['lead time', 'supplier', 'vendor', 'factory'],
    'Margin / Cash Pressure': ['margin', 'cash', 'storage', 'markdown'],
}

RadarInput = Union[str, Dict[str, Any]]


def _score_rules(text: str, rules: Dict[str, List[str]]) -> Dict[str, int]:
    return {name: sum(1 for keyword in keywords if keyword in text) for name, keywords in rules.items()}


def _join(items: List[str]) -> str:
    return ', '.join(items) if items else 'None explicitly provided'


class InventoryRiskRadar:
    def __init__(self, user_input: RadarInput):
        self.raw = user_input
        self.text = self._normalize_input(user_input)
        self.lower = self.text.lower()
        self.review_mode = self._detect_review_mode()
        self.risk_types = self._detect_risk_types()
        self.signals = self._detect_signals()

    def _normalize_input(self, user_input: RadarInput) -> str:
        if isinstance(user_input, dict):
            chunks: List[str] = []
            for key in ['review_mode', 'inventory', 'demand', 'supply', 'constraints', 'notes']:
                value = user_input.get(key)
                if not value:
                    continue
                if isinstance(value, list):
                    value = ', '.join(str(item) for item in value)
                chunks.append(f'{key}: {value}')
            return ' | '.join(chunks)
        return str(user_input or '').strip()

    def _detect_review_mode(self) -> str:
        scores = _score_rules(self.lower, REVIEW_MODE_RULES)
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else 'Daily Watchlist'

    def _detect_risk_types(self) -> List[str]:
        matched = [name for name, data in RISK_RULES.items() if any(keyword in self.lower for keyword in data['keywords'])]
        ordered = []
        for name in ['Stockout Risk', 'Inbound Delay Risk', 'Promo Readiness Risk', 'Overstock Risk', 'Aging Inventory Risk']:
            if name in matched and name not in ordered:
                ordered.append(name)
        defaults = ['Stockout Risk', 'Overstock Risk', 'Inbound Delay Risk']
        for name in defaults:
            if name not in ordered:
                ordered.append(name)
        return ordered[:4]

    def _detect_signals(self) -> List[str]:
        matched = [name for name, keywords in SIGNAL_RULES.items() if any(keyword in self.lower for keyword in keywords)]
        return matched or ['On-hand / Available Stock', 'Sales Velocity', 'Lead Time / Supplier Reliability']

    def _dashboard_rows(self) -> List[Dict[str, str]]:
        rows = []
        for risk in self.risk_types:
            info = RISK_RULES[risk]
            rows.append({
                'risk': risk,
                'why': info['why'],
                'check': info['check'],
                'action': info['action'],
            })
        return rows

    def _coverage_notes(self) -> List[str]:
        notes = [
            'Separate hero SKUs from the rest of the catalog before discussing average days of cover.',
            'Treat inbound stock as protected only when ETA confidence is high enough to matter operationally.',
            'Review whether the team is using one consistent definition for available, reserved, inbound, and backorder stock.',
        ]
        if self.review_mode == 'Pre-Promo Risk Review':
            notes.insert(0, 'Stress test cover using a promo uplift assumption rather than recent average demand alone.')
        return notes[:4]

    def _watchlist(self) -> List[str]:
        items = [
            'Critical: SKUs with thin cover, high strategic importance, or unreliable inbound protection.',
            'Warning: SKUs with acceptable current stock but visible supplier, lead-time, or promo exposure.',
            'Watch: Slow movers, aged stock, or channel-specific inventory pockets that can become cash drag.',
            'Owner note: assign one owner for demand, one for supply, and one for promo or markdown decisions when risk crosses teams.',
        ]
        return items

    def _scenario_notes(self) -> List[str]:
        notes = [
            'If demand spikes, review whether the top sellers have substitutes that can absorb overflow without hurting margin too badly.',
            'If inbound slips by 7 to 14 days, identify which SKUs move from manageable risk to immediate action territory.',
            'If the promo goes live as planned, protect inventory for the channels with the cleanest economics first.',
        ]
        if self.review_mode == 'Cash-Risk Review':
            notes[2] = 'If current velocity stays flat, estimate how much cash remains tied up and how soon markdown pressure becomes unavoidable.'
        return notes

    def _action_ladder(self) -> List[str]:
        actions = [
            'Reorder now for the highest-confidence stockout risks only after checking lead time and true available stock.',
            'Expedite, transfer, or rebalance inventory before expanding paid demand against a fragile SKU.',
            'Slow buying or pause replenishment for SKUs that show overstock or aging without a convincing recovery path.',
            'Use bundle, markdown, liquidation, or channel-shift plays deliberately instead of waiting for passive sell-through.',
        ]
        if self.review_mode == 'Pre-Promo Risk Review':
            actions[1] = 'Reduce promo intensity or reroute spend if hero inventory cannot safely support the planned demand spike.'
        return actions

    def _assumptions(self) -> List[str]:
        notes = [
            'This brief is heuristic and depends on the stock, velocity, and supply notes the user provided.',
            'Revenue-at-risk and cash-at-risk framing is directional unless the inputs are complete and clean.',
            'PO, transfer, markdown, liquidation, and media decisions should remain human-approved.',
        ]
        missing = [signal for signal in ['Inbound / PO Status', 'Margin / Cash Pressure'] if signal not in self.signals]
        if missing:
            notes.append(f'Missing or lightly referenced signals: {_join(missing)}.')
        return notes

    def render(self) -> str:
        lines: List[str] = []
        lines.append('# Inventory Risk Radar')
        lines.append('')
        lines.append(f'**Review mode:** {self.review_mode}')
        lines.append(f'**Signals referenced:** {_join(self.signals)}')
        lines.append(f'**Priority risk types:** {_join(self.risk_types)}')
        lines.append('**Method note:** This is a heuristic inventory-risk brief. No live ERP, WMS, supplier portal, or forecasting engine was accessed.')
        lines.append('')
        lines.append('## Inventory Risk Dashboard')
        lines.append('| Risk type | Why it matters | First check | Default action path |')
        lines.append('|---|---|---|---|')
        for row in self._dashboard_rows():
            lines.append(f'| {row["risk"]} | {row["why"]} | {row["check"]} | {row["action"]} |')
        lines.append('')
        lines.append('## Days of Cover Summary')
        for note in self._coverage_notes():
            lines.append(f'- {note}')
        lines.append('')
        lines.append('## SKU Action Watchlist')
        for item in self._watchlist():
            lines.append(f'- {item}')
        lines.append('')
        lines.append('## Scenario Notes')
        for item in self._scenario_notes():
            lines.append(f'- {item}')
        lines.append('')
        lines.append('## Action Ladder')
        for idx, item in enumerate(self._action_ladder(), 1):
            lines.append(f'{idx}. {item}')
        lines.append('')
        lines.append('## Assumptions and Limits')
        for note in self._assumptions():
            lines.append(f'- {note}')
        return '\n'.join(lines)


def handle(user_input: RadarInput) -> str:
    return InventoryRiskRadar(user_input).render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
