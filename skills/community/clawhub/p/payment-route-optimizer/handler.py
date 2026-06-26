#!/usr/bin/env python3
import sys
from typing import List

OBJECTIVE_RULES = {
    'Approval-first': ['approval', 'authorization', 'success rate', 'acceptance'],
    'Cost-first': ['cost', 'fee', 'mdr', 'cheaper', 'processing cost'],
    'Risk-first': ['fraud', 'chargeback', '3ds', 'risk'],
    'Balanced': ['balanced', 'tradeoff', 'blend', 'both'],
}

MODE_RULES = {
    'Failover Planning': ['failover', 'fallback', 'outage', 'downtime', 'peak season', 'resilience'],
    'Market Launch Planning': ['launch', 'new market', 'new country', 'expansion'],
    'Baseline Route Review': ['route', 'routing', 'psp', 'acquirer', 'authorization', 'cost'],
}

MARKET_RULES = {
    'US': ['us', 'usa', 'united states'],
    'EU': ['eu', 'europe', 'european'],
    'Brazil': ['brazil', 'br'],
    'UK': ['uk', 'united kingdom', 'britain'],
    'Mexico': ['mexico', 'mx'],
    'APAC': ['apac', 'asia', 'singapore', 'japan', 'australia'],
}

METHOD_RULES = {
    'Card': ['card', 'visa', 'mastercard', 'amex', 'credit card', 'debit card'],
    'Wallet': ['wallet', 'paypal', 'apple pay', 'google pay'],
    'Local Method': ['pix', 'ideal', 'klarna', 'bank transfer', 'local method'],
}


class PaymentRouteOptimizer:
    def __init__(self, text: str):
        self.text = (text or '').strip()
        self.lower = self.text.lower()
        self.objective = self._detect_objective()
        self.mode = self._detect_mode()
        self.markets = self._detect_markets()
        self.methods = self._detect_methods()

    def _detect_objective(self) -> str:
        for objective in ['Approval-first', 'Cost-first', 'Risk-first', 'Balanced']:
            if any(keyword in self.lower for keyword in OBJECTIVE_RULES[objective]):
                return objective
        return 'Balanced'

    def _detect_mode(self) -> str:
        for mode in ['Failover Planning', 'Market Launch Planning', 'Baseline Route Review']:
            if any(keyword in self.lower for keyword in MODE_RULES[mode]):
                return mode
        return 'Baseline Route Review'

    def _detect_markets(self) -> List[str]:
        markets = [name for name, keywords in MARKET_RULES.items() if any(keyword in self.lower for keyword in keywords)]
        return markets or ['Core markets']

    def _detect_methods(self) -> List[str]:
        methods = [name for name, keywords in METHOD_RULES.items() if any(keyword in self.lower for keyword in keywords)]
        return methods or ['Card']

    def _baseline_findings(self) -> List[str]:
        findings = ['Quantify loss by segment before changing the routing policy so the team knows where approval or cost is leaking.']
        if self.objective == 'Approval-first':
            findings.append('Treat issuer, BIN, 3DS friction, and local-acquirer coverage as the first suspects.')
        elif self.objective == 'Cost-first':
            findings.append('Verify where the lowest-fee path still clears a safe approval floor before shifting volume.')
        elif self.objective == 'Risk-first':
            findings.append('Prioritize fraud exposure, chargeback tolerance, and 3DS support over raw approval lift.')
        else:
            findings.append('Balance approval, cost, and risk together so one metric is not optimized at the expense of the business.')
        if self.mode == 'Failover Planning':
            findings.append('Map provider outage, timeout, and soft-decline scenarios separately because they require different fallback logic.')
        return findings

    def _segment_pairs(self) -> List[str]:
        pairs: List[str] = []
        for market in self.markets[:2]:
            for method in self.methods[:2]:
                pairs.append(f'{market} | {method}')
                if len(pairs) >= 3:
                    return pairs
        return pairs or ['Core markets | Card']

    def _primary_path(self, pair: str) -> str:
        market, method = [part.strip() for part in pair.split('|')]
        if method == 'Local Method':
            return 'Use the strongest local-method provider first, with a backup only where the method supports it.'
        if self.objective == 'Approval-first':
            return f'Use the provider with the strongest issuer coverage and local acceptance signals for {market}.'
        if self.objective == 'Cost-first':
            return f'Use the lowest-fee acceptable provider for {market}, provided approval stays above the agreed floor.'
        if self.objective == 'Risk-first':
            return f'Use the provider with stronger 3DS, fraud controls, and manual-review hooks for {market}.'
        return f'Use the best local performer as primary and reserve the cheaper or lower-risk path as conditional backup for {market}.'

    def _backup_path(self, pair: str) -> str:
        if self.mode == 'Failover Planning':
            return 'Immediate backup on provider outage or timeout, with idempotency checks and rollback visibility.'
        return 'Secondary PSP or acquirer for approved fallback cases only, not as a blanket retry rule.'

    def _rationale(self, pair: str) -> str:
        market, method = [part.strip() for part in pair.split('|')]
        if method == 'Wallet':
            return f'Wallet flows usually need low-friction continuity and a clear timeout or provider-failure plan in {market}.'
        if method == 'Local Method':
            return f'Local method performance often depends on country-specific coverage and settlement practicality in {market}.'
        return f'Card performance in {market} usually needs issuer-level analysis instead of one global routing rule.'

    def _retry_policy(self) -> List[str]:
        return [
            'Retry only soft declines or recoverable technical failures, not hard declines or suspected fraud cases.',
            'Use at most one carefully scoped retry per segment unless data clearly supports a second attempt.',
            'For failover on timeout, require idempotency-safe design and clear ownership of duplicate-payment risk.',
        ]

    def _rollout_plan(self) -> List[str]:
        return [
            'Simulate the candidate policy on recent historical samples before any production change is proposed.',
            'Start with one market, method, or amount band instead of a global flip.',
            'Review authorization rate, fee delta, 3DS completion, and chargeback early signals before expanding volume.',
            'Keep an explicit rollback trigger and named approver for each rollout phase.',
        ]

    def render(self) -> str:
        lines: List[str] = []
        lines.append('# Payment Routing Optimization Brief')
        lines.append('')
        lines.append(f'**Primary objective:** {self.objective}')
        lines.append(f'**Planning mode:** {self.mode}')
        lines.append(f'**Markets referenced:** {", ".join(self.markets)}')
        lines.append(f'**Methods referenced:** {", ".join(self.methods)}')
        lines.append('**Method note:** This is an offline planning brief. No live routing engine or production traffic was touched.')
        lines.append('')
        lines.append('## Baseline Diagnostic')
        for item in self._baseline_findings():
            lines.append(f'- {item}')
        lines.append('')
        lines.append('## Suggested Route Matrix')
        lines.append('| Segment | Primary path | Backup path | Why this segment matters |')
        lines.append('|---|---|---|---|')
        for pair in self._segment_pairs():
            lines.append(f'| {pair} | {self._primary_path(pair)} | {self._backup_path(pair)} | {self._rationale(pair)} |')
        lines.append('')
        lines.append('## Retry and Failover Policy')
        for idx, item in enumerate(self._retry_policy(), 1):
            lines.append(f'{idx}. {item}')
        lines.append('')
        lines.append('## Rollout Plan')
        for idx, item in enumerate(self._rollout_plan(), 1):
            lines.append(f'{idx}. {item}')
        lines.append('')
        lines.append('## Monitoring and Guardrails')
        lines.append('- Track authorization rate, provider timeout rate, fee basis points, 3DS completion, and chargeback trend by segment.')
        lines.append('- Compare the new policy against a control baseline so success is not judged on anecdotes alone.')
        lines.append('- Keep market-specific notes because a rule that works in one country may be harmful in another.')
        lines.append('')
        lines.append('## Compliance and Limits')
        lines.append('- Assume only masked or tokenized payment data is in scope.')
        lines.append('- PCI, fraud review, scheme rules, and legal approval are outside this skill and must be handled separately.')
        lines.append('- Human approval is required before any routing, retry, or failover rule is adopted in production.')
        return '\n'.join(lines)


def handle(user_input: str) -> str:
    return PaymentRouteOptimizer(user_input).render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
