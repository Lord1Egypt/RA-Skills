#!/usr/bin/env python3
import sys
from typing import Any, Dict, List, Sequence, Union

ShowInput = Union[str, Dict[str, Any]]

SHOW_TYPE_RULES = {
    'Product Launch Live': ['launch', 'new product', 'debut', 'drop'],
    'Promo / Clearance Push': ['clearance', 'promo', 'promotion', 'discount', 'markdown', 'flash sale', '618', '11.11'],
    'Education / Demo Session': ['demo', 'education', 'tutorial', 'how to use', 'explain'],
    'Guest / Co-host Session': ['guest', 'co-host', 'creator', 'expert', 'influencer', 'collab'],
    'VIP / Community Session': ['vip', 'member', 'community', 'loyalty', 'private'],
}

CHANNEL_RULES = {
    'Douyin Live': ['douyin', '抖音'],
    'TikTok Shop Live': ['tiktok', 'tiktok shop'],
    'Taobao Live': ['taobao', 'taobao live', '淘宝'],
    'Kuaishou Live': ['kuaishou', '快手'],
    'Amazon Live': ['amazon live', 'amazon'],
    'Instagram Live': ['instagram live', 'instagram'],
}

OBJECTIVE_RULES = {
    'Launch Conversion': ['launch', 'new product', 'debut', 'conversion', 'sell'],
    'Inventory Clearance': ['clearance', 'markdown', 'old stock', 'inventory', 'stock'],
    'Education / Trust Building': ['education', 'demo', 'tutorial', 'trust'],
    'Audience Growth': ['followers', 'reach', 'traffic', 'audience', 'new viewers'],
}

RISK_RULES = {
    'Traffic uncertainty': ['traffic', 'viewers', 'reach', 'low traffic'],
    'Inventory pressure': ['inventory', 'stock', 'oos', 'out of stock', 'sell out'],
    'Offer complexity': ['bundle', 'coupon', 'offer', 'discount stack', 'voucher'],
    'Host confidence gap': ['host', 'rookie', 'script', 'confidence', 'training'],
    'Technical / moderation load': ['comment', 'chat', 'lag', 'audio', 'mic', 'camera', 'tech'],
    'Compliance sensitivity': ['claim', 'compliance', 'policy', 'regulated'],
}


def _normalize_input(user_input: ShowInput) -> str:
    if isinstance(user_input, dict):
        chunks: List[str] = []
        for key in ['channel', 'objective', 'products', 'offers', 'team', 'risks', 'notes']:
            value = user_input.get(key)
            if not value:
                continue
            if isinstance(value, list):
                value = ', '.join(str(item) for item in value)
            chunks.append(f'{key}: {value}')
        return ' | '.join(chunks)
    return str(user_input or '').strip()


def _match_one(text: str, rules: Dict[str, Sequence[str]], default: str) -> str:
    for label, keywords in rules.items():
        if any(keyword in text for keyword in keywords):
            return label
    return default


def _match_many(text: str, rules: Dict[str, Sequence[str]], default: List[str], limit: int = 4) -> List[str]:
    found = [label for label, keywords in rules.items() if any(keyword in text for keyword in keywords)]
    ordered: List[str] = []
    for item in found + default:
        if item not in ordered:
            ordered.append(item)
    return ordered[:limit]


def _join(items: List[str]) -> str:
    return ', '.join(items) if items else 'None explicitly provided'


class LiveCommerceShowrunner:
    def __init__(self, user_input: ShowInput):
        self.raw = user_input
        self.text = _normalize_input(user_input)
        self.lower = self.text.lower()
        self.show_type = _match_one(self.lower, SHOW_TYPE_RULES, 'Product Launch Live')
        self.channels = _match_many(self.lower, CHANNEL_RULES, ['Douyin Live', 'TikTok Shop Live'], limit=4)
        self.objective = _match_one(self.lower, OBJECTIVE_RULES, 'Launch Conversion')
        self.risks = _match_many(self.lower, RISK_RULES, ['Traffic uncertainty', 'Technical / moderation load'], limit=4)

    def _run_of_show(self) -> List[List[str]]:
        opening = 'Open with one clear reason to stay, one hero product angle, and one timed incentive.'
        if self.show_type == 'Education / Demo Session':
            opening = 'Open with the problem statement, who the product is for, and the learning promise for the session.'
        elif self.show_type == 'Promo / Clearance Push':
            opening = 'Open with urgency, inventory reality, and the first easy-to-understand deal.'

        middle = 'Demonstrate proof, compare options, answer objections, then stack offers without confusing the viewer.'
        if self.show_type == 'Guest / Co-host Session':
            middle = 'Use the guest for social proof or expertise, then hand back to the host for the sell-through and CTA.'

        closing = 'Summarize the hero offer, restate urgency, and direct viewers to the checkout path before ending.'
        return [
            ['0-3 min', 'Hook and room setup', opening],
            ['3-12 min', 'Proof and demonstration', middle],
            ['12-22 min', 'Offer stack and objection handling', 'Rotate between proof, price logic, coupon clarity, and live Q&A.'],
            ['22-30 min', 'Conversion push', 'Bring back hero SKUs, reinforce scarcity, and isolate one checkout CTA at a time.'],
            ['30 min+', 'Close or extension', closing],
        ]

    def _offer_notes(self) -> List[str]:
        notes = [
            'Limit the number of simultaneous incentives so viewers can understand the buy path quickly.',
            'Pair each hero SKU with one proof point, one price anchor, and one action cue.',
            'Keep one rescue offer in reserve in case traffic or conversion starts soft.',
        ]
        if self.objective == 'Inventory Clearance':
            notes[1] = 'Use bundle or clear-out logic that moves stock decisively without turning the offer explanation into chaos.'
        if 'Compliance sensitivity' in self.risks:
            notes.append('Remove any benefit claim or urgency line that cannot be defended by policy or product fact.')
        return notes

    def render(self) -> str:
        lines: List[str] = []
        lines.append('# Live Commerce Showrunner Brief')
        lines.append('')
        lines.append(f'**Show type:** {self.show_type}')
        lines.append(f'**Channels in scope:** {_join(self.channels)}')
        lines.append(f'**Primary objective:** {self.objective}')
        lines.append(f'**Risk flags:** {_join(self.risks)}')
        lines.append('**Method note:** This is a heuristic show plan. No live traffic, GMV, comment, or inventory system was accessed.')
        lines.append('')
        lines.append('## Show Strategy Summary')
        lines.append('- Build the session around one commercial story, not a pile of disconnected product moments.')
        lines.append('- Keep the host, moderator, and operator aligned on what counts as the hero SKU, rescue offer, and escalation trigger.')
        lines.append(f'- Because the main objective is **{self.objective.lower()}**, the show should simplify the next buyer action instead of maximizing noise.')
        lines.append('')
        lines.append('## Run of Show')
        lines.append('| Segment | Focus | Operator note |')
        lines.append('|---|---|---|')
        for segment, focus, note in self._run_of_show():
            lines.append(f'| {segment} | {focus} | {note} |')
        lines.append('')
        lines.append('## Offer and Merch Plan')
        for item in self._offer_notes():
            lines.append(f'- {item}')
        lines.append('')
        lines.append('## Host and Crew Checklist')
        lines.append('- **Host:** own the story arc, product proof, CTA clarity, and energy pacing.')
        lines.append('- **Moderator:** surface real buyer objections, repeat the checkout path, and keep comments usable.')
        lines.append('- **Operator:** track timing, price or coupon readiness, and risk triggers like lag or stock pressure.')
        lines.append('- **Product support:** prepare proof assets, comparison points, and a fast answer bank for likely objections.')
        lines.append('')
        lines.append('## Comment Moderation and Conversion Plays')
        lines.append('- Answer repeat objections with short, consistent replies so the host does not need to restart the explanation every minute.')
        lines.append('- Pin the current CTA and replace it only when the offer or hero SKU changes.')
        lines.append('- Escalate payment, stock, or policy confusion immediately instead of improvising inaccurate answers on stream.')
        lines.append('')
        lines.append('## Failure Modes and Backup Plan')
        lines.append('- If traffic starts soft, shorten the intro, bring forward proof, and trigger one easy-to-understand offer earlier.')
        lines.append('- If comments get chaotic, reduce the number of offers on screen and return to one SKU plus one CTA.')
        lines.append('- If a product sells out or becomes risky, pivot to the backup SKU and explicitly reset the viewer expectation.')
        lines.append('- If audio, lag, or moderation breaks, the operator should have a stop-or-reset threshold instead of hoping the issue disappears.')
        lines.append('')
        lines.append('## Metrics and Debrief')
        lines.append('- Review traffic quality, add-to-cart or click intent, objection frequency, and where attention dropped.')
        lines.append('- Compare the planned offer ladder to what actually created response or confusion.')
        lines.append('- Note the three moments to keep, change, and remove before the next live session.')
        lines.append('')
        lines.append('## Assumptions and Limits')
        lines.append('- This plan is only as strong as the offer, product, and host context provided by the user.')
        lines.append('- Conversion and GMV outcomes depend on traffic quality, compliance, inventory, execution, and platform conditions.')
        lines.append('- Final pricing, legal, moderation, and inventory decisions remain human-approved.')
        return "\n".join(lines)


def handle(user_input: ShowInput) -> str:
    return LiveCommerceShowrunner(user_input).render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
