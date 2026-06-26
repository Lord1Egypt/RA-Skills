---
name: greenhelix-agent-negotiation-strategies
version: "1.3.1"
description: "Agent Negotiation Strategies: Game Theory, Auctions, and Dynamic Pricing for AI Agent Commerce. Translates auction theory, BATNA calculation, concession strategies, coalition formation, and trust-based pricing from academic research into working Python code with full API integration. Covers English/Dutch/sealed-bid/Vickrey auctions, multi-round negotiation with Boulware and Zeuthen strategies, dynamic pricing, Shapley value coalition division, and anti-manipulation detection."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [negotiation, game-theory, auctions, pricing, multi-agent, batna, coalition, trust, guide, greenhelix, openclaw, ai-agent]
price_usd: 0.0
content_type: markdown
executable: false
install: none
credentials: none
---
# Agent Negotiation Strategies: Game Theory, Auctions, and Dynamic Pricing for AI Agent Commerce

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code, require credentials, or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.


Every day, autonomous AI agents leave money on the table. They accept the first price offered. They bid their true valuation in auctions where shading would save thousands. They concede linearly in multi-round negotiations when an exponential strategy would extract 15-30% more surplus. They ignore their counterparty's reputation when setting prices, treating a first-time anonymous agent the same as a verified partner with 500 successful transactions. The academic literature -- ANAC competition results, game-theoretic LLM research from NeurIPS 2025, auction theory going back to Vickrey 1961 -- contains precise answers to these problems. But the findings are locked in papers that assume familiarity with Nash equilibria, Bayesian updating, and mechanism design. Enterprise negotiation platforms like Pactum charge six-figure SaaS fees to apply these ideas. This guide bridges that gap. It translates auction theory, BATNA calculation, concession strategies, coalition formation, and trust-based pricing into working Python code against the GreenHelix A2A Commerce Gateway. By the end, your agents will negotiate like they read the literature -- because the code does it for them.
> **Getting started**: All examples in this guide work with the GreenHelix sandbox
> (https://sandbox.greenhelix.net) which provides 500 free credits — no API key required.

## What You'll Learn
- Chapter 1: Why Agents Need Negotiation Strategy
- Chapter 2: BATNA and Reservation Prices
- Chapter 3: Auction Strategies
- Chapter 4: Multi-Round Negotiation
- Chapter 5: Dynamic Pricing
- Chapter 6: Coalition Formation
- Chapter 7: Trust-Based Negotiation
- Chapter 8: Production Negotiation Patterns
- Appendix: GreenHelix API Reference for Negotiation

## Full Guide

# Agent Negotiation Strategies: Game Theory, Auctions, and Dynamic Pricing for AI Agent Commerce

Every day, autonomous AI agents leave money on the table. They accept the first price offered. They bid their true valuation in auctions where shading would save thousands. They concede linearly in multi-round negotiations when an exponential strategy would extract 15-30% more surplus. They ignore their counterparty's reputation when setting prices, treating a first-time anonymous agent the same as a verified partner with 500 successful transactions. The academic literature -- ANAC competition results, game-theoretic LLM research from NeurIPS 2025, auction theory going back to Vickrey 1961 -- contains precise answers to these problems. But the findings are locked in papers that assume familiarity with Nash equilibria, Bayesian updating, and mechanism design. Enterprise negotiation platforms like Pactum charge six-figure SaaS fees to apply these ideas. This guide bridges that gap. It translates auction theory, BATNA calculation, concession strategies, coalition formation, and trust-based pricing into working Python code against the GreenHelix A2A Commerce Gateway. By the end, your agents will negotiate like they read the literature -- because the code does it for them.

---


> **Getting started**: All examples in this guide work with the GreenHelix sandbox
> (https://sandbox.greenhelix.net) which provides 500 free credits — no API key required.

## Table of Contents

1. [Why Agents Need Negotiation Strategy](#chapter-1-why-agents-need-negotiation-strategy)
2. [BATNA and Reservation Prices](#chapter-2-batna-and-reservation-prices)
3. [Auction Strategies](#chapter-3-auction-strategies)
4. [Multi-Round Negotiation](#chapter-4-multi-round-negotiation)
5. [Dynamic Pricing](#chapter-5-dynamic-pricing)
6. [Coalition Formation](#chapter-6-coalition-formation)
7. [Trust-Based Negotiation](#chapter-7-trust-based-negotiation)
8. [Production Negotiation Patterns](#chapter-8-production-negotiation-patterns)

---

## Chapter 1: Why Agents Need Negotiation Strategy

### Fixed Pricing Is Leaving Money on the Table

Most agent marketplaces today use fixed pricing. A translation agent lists its service at $0.02 per word. A code review agent charges $5.00 per pull request. A data enrichment agent prices at $0.10 per record. The prices never change regardless of demand, competition, or the buyer's willingness to pay.

Fixed pricing is simple. It is also wasteful. When demand for translation spikes during a product launch across twelve markets, the translation agent serves requests at the same $0.02 rate it charges on a quiet Tuesday. When three competing code review agents enter the marketplace, the original agent keeps charging $5.00 while competitors undercut it at $3.50. When a buyer agent has a budget of $0.25 per record but the enrichment agent lists at $0.10, the seller captures less than half the available surplus.

Dynamic negotiation solves these problems. Agents that negotiate adapt to market conditions in real time. They charge more when demand is high and they are the only option. They lower prices strategically when competition intensifies. They extract more value from high-budget buyers while remaining accessible to price-sensitive ones. The theoretical ceiling is Pareto-optimal allocation -- every transaction captures the maximum possible surplus for both parties.

### AI-AI Negotiation Is Fundamentally Different

The 2025 Automated Negotiating Agents Competition (ANAC) produced findings that upend conventional negotiation wisdom. When AI agents negotiate with other AI agents -- as opposed to AI negotiating with humans -- the dynamics shift in three critical ways.

**First-proposal advantage is amplified.** In human negotiation, the anchoring effect of the first offer is well documented but moderate. In AI-AI negotiation, ANAC 2025 found that the first-proposing agent captures 8-12% more surplus on average. LLM-based agents are particularly susceptible to anchoring because their response is conditioned on the prompt context, which includes the first offer. An agent that moves first sets the frame for the entire negotiation.

**Warmth signals change concession rates.** Research published at NeurIPS 2025 demonstrated that LLM agents make larger concessions when their counterparty uses warm, cooperative language -- even when the underlying offer is identical. Agents that prefixed offers with collaborative framing ("I want us both to benefit from this arrangement") extracted 6-9% more value than agents making the same numerical offers with neutral language. This is not a bug in LLM reasoning. It is a feature of how language models weight context, and it is exploitable.

**Chain-of-thought leakage is a vulnerability.** When agents expose their reasoning process -- their reservation price, their BATNA, their deadline pressure -- counterparties extract that information and use it. An agent that includes "my maximum budget is $500" in its chain-of-thought, even if not explicitly communicated, may leak this through behavioral patterns. Agents with hidden reasoning consistently outperform agents with transparent reasoning in adversarial negotiations.

### What This Guide Covers

This guide provides eight negotiation capabilities for your agents, each backed by game-theoretic foundations and implemented against the GreenHelix API:

- **BATNA calculation** using live marketplace data to set walk-away prices
- **Four auction strategies** (English, Dutch, sealed-bid, Vickrey) with optimal bidding rules
- **Multi-round negotiation** with concession strategies calibrated to deadlines
- **Dynamic pricing** that responds to demand, competition, and volume
- **Coalition formation** with Shapley value for fair surplus division
- **Trust-adjusted pricing** that uses reputation data to manage counterparty risk
- **Production patterns** for timeouts, logging, and anti-manipulation

Every code example calls the GreenHelix A2A Commerce Gateway via the REST API (`POST /v1/{tool}`). Every strategy is something you can deploy this week.

---

## Chapter 2: BATNA and Reservation Prices

### The Concept That Changes Everything

BATNA -- Best Alternative to Negotiated Agreement -- is the single most important concept in negotiation theory. Roger Fisher and William Ury formalized it in _Getting to Yes_ (1981), and it has been the foundation of negotiation research since. Your BATNA is what happens if the current negotiation fails. If you are buying translation services and your BATNA is a competing agent that charges $0.03 per word, you should never agree to pay more than $0.03 in the current negotiation. If your BATNA is doing the translation yourself at a cost of $0.08 per word, your threshold is much higher.

For autonomous agents, BATNA is not a feeling or an intuition. It is a number computed from market data. The GreenHelix marketplace provides the data. The agent computes the number. Every subsequent negotiation decision -- whether to accept, reject, counter-offer, or walk away -- flows from that number.

### The Reservation Price

Your reservation price is the worst deal you would accept. For a buyer, it is the maximum price. For a seller, it is the minimum price. The reservation price is derived from the BATNA:

- **Buyer reservation price** = cost of best alternative (BATNA) minus switching cost
- **Seller reservation price** = next-best income opportunity (BATNA) plus opportunity cost of time

The **Zone of Possible Agreement (ZOPA)** exists when the buyer's reservation price exceeds the seller's reservation price. If the buyer will pay up to $0.05 and the seller will accept as low as $0.02, the ZOPA is $0.02-$0.05. Negotiation divides this $0.03 surplus. If there is no ZOPA, no deal is possible, and rational agents should walk away immediately rather than wasting rounds.

### Building Market Awareness

Before any negotiation begins, an agent needs to know the market. The GreenHelix marketplace provides two tools for this: `search_services` returns all services matching a query with their listed prices, and `estimate_cost` returns the gateway's cost estimate for a specific tool invocation.

```python
import requests
import time
import math
from typing import Optional


class NegotiationAgent:
    """Agent with game-theoretic negotiation capabilities."""

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        base_url: str = "https://api.greenhelix.net/v1",
    ):
        self.base_url = base_url
        self.agent_id = agent_id
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })
        self.batna = None
        self.reservation_price = None
        self.negotiation_log = []

    def _execute(self, tool: str, input_data: dict) -> dict:
        """Execute a tool on the GreenHelix gateway."""
        resp = self.session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": input_data},
        )
        resp.raise_for_status()
        return resp.json()

    def search_market(self, query: str) -> list:
        """Search the marketplace and return available services with prices."""
        result = self._execute("search_services", {"query": query})
        return result.get("services", [])

    def get_cost_estimate(self, tool_name: str, input_data: dict) -> dict:
        """Get the gateway's cost estimate for a tool invocation."""
        return self._execute("estimate_cost", {
            "tool": tool_name,
            "input": input_data,
        })

    def get_volume_discount(self, tool_name: str, volume: int) -> dict:
        """Check available volume discounts."""
        return self._execute("get_volume_discount", {
            "tool": tool_name,
            "volume": volume,
        })

    def calculate_batna(
        self,
        service_query: str,
        exclude_agent: Optional[str] = None,
    ) -> float:
        """Calculate BATNA from live marketplace data.

        Searches for alternative providers, excludes the current
        counterparty, and returns the best alternative price.
        Returns float('inf') if no alternatives exist (weak BATNA).
        """
        alternatives = self.search_market(service_query)

        # Filter out the agent we are currently negotiating with
        if exclude_agent:
            alternatives = [
                s for s in alternatives
                if s.get("agent_id") != exclude_agent
            ]

        if not alternatives:
            # No alternatives -- very weak BATNA
            self.batna = float("inf")
            return self.batna

        # BATNA is the price of the best alternative
        # "Best" means lowest price for a buyer, highest price for a seller
        prices = [
            float(s["price"])
            for s in alternatives
            if s.get("price") is not None
        ]

        if not prices:
            self.batna = float("inf")
            return self.batna

        self.batna = min(prices)  # Buyer perspective
        return self.batna

    def set_reservation_price(
        self,
        role: str = "buyer",
        switching_cost: float = 0.0,
    ) -> float:
        """Set reservation price based on BATNA.

        For buyers: reservation = BATNA - switching_cost
        For sellers: reservation = BATNA + opportunity_cost
        """
        if self.batna is None:
            raise ValueError("Calculate BATNA first")

        if role == "buyer":
            self.reservation_price = self.batna - switching_cost
        else:
            # Seller: reservation is BATNA + cost of losing this deal
            self.reservation_price = self.batna + switching_cost

        return self.reservation_price

    def should_accept(self, offered_price: float, role: str = "buyer") -> bool:
        """Decide whether to accept an offered price.

        Buyers accept if offered price <= reservation price.
        Sellers accept if offered price >= reservation price.
        """
        if self.reservation_price is None:
            raise ValueError("Set reservation price first")

        if role == "buyer":
            return offered_price <= self.reservation_price
        else:
            return offered_price >= self.reservation_price
```

### Using BATNA in Practice

Here is how a buyer agent uses BATNA before entering a negotiation:

```python
buyer = NegotiationAgent(
    api_key="your-api-key",
    agent_id="buyer-agent-001",
)

# Step 1: Survey the market for translation services
batna = buyer.calculate_batna(
    service_query="translation english to spanish",
    exclude_agent="seller-agent-042",  # Current counterparty
)
print(f"BATNA (best alternative price): ${batna:.4f}/word")

# Step 2: Set reservation price with $0.005/word switching cost
reservation = buyer.set_reservation_price(
    role="buyer",
    switching_cost=0.005,
)
print(f"Reservation price: ${reservation:.4f}/word")

# Step 3: Evaluate the seller's asking price
asking_price = 0.025  # Seller wants $0.025/word
if buyer.should_accept(asking_price):
    print(f"Accept: ${asking_price} is below reservation ${reservation:.4f}")
else:
    print(f"Reject: ${asking_price} exceeds reservation ${reservation:.4f}")
    print("Counter-offer or walk away to BATNA")
```

The critical insight: an agent that calculates its BATNA before negotiating will never overpay. It knows exactly when to walk away. An agent that skips this step is negotiating blind.

---

## Chapter 3: Auction Strategies

Auctions are a special case of negotiation where multiple buyers compete for a single item (or multiple sellers compete for a single buyer). The four canonical auction formats each have different optimal strategies. An agent that uses the wrong strategy in the wrong auction format will systematically overpay or lose winnable auctions.

### English Auction (Ascending Price)

The English auction is the format most people recognize: the auctioneer starts low, bidders raise incrementally, and the last bidder standing wins at their bid price. The optimal strategy is simple in theory and subtle in practice.

**Optimal strategy:** Bid up to your valuation, then stop. Never bid above your true value. The increment size matters -- smaller increments extract more surplus but risk being outbid if another agent has a similar valuation.

**Practical refinement:** Set your maximum bid at your valuation minus a small epsilon. In competitive auctions with many bidders, the winner's curse (paying more than the item is worth) becomes significant. Shading your bid slightly below true valuation protects against this.

### Dutch Auction (Descending Price)

In a Dutch auction, the auctioneer starts high and lowers the price until someone accepts. The first agent to accept wins at that price. This format rewards decisiveness and accurate valuation.

**Optimal strategy:** Accept when the price drops to your valuation minus your expected surplus. If you wait too long, another agent accepts first. If you accept too early, you overpay. The optimal acceptance point depends on the number of competitors and the distribution of their valuations.

### Sealed-Bid First-Price

Each bidder submits one bid in secret. Highest bid wins and pays their bid amount. This is the format used in most procurement and RFP processes.

**Optimal strategy:** Shade your bid below your true valuation. The optimal shading depends on the number of bidders (n). With uniformly distributed valuations, the optimal bid is `valuation * (n-1)/n`. With 2 bidders, bid half your valuation. With 10 bidders, bid 90% of your valuation. More competition means less shading.

### Vickrey (Second-Price Sealed-Bid)

Each bidder submits one bid in secret. Highest bid wins but pays the second-highest bid amount. This is the format used by Google Ad auctions and many automated marketplaces.

**Optimal strategy:** Bid your true valuation. This is the dominant strategy -- it is optimal regardless of what other bidders do. Bidding above your valuation risks winning and overpaying. Bidding below your valuation risks losing an auction you would have profited from. William Vickrey proved this in 1961 and received the Nobel Prize for it.

### The AuctionAgent Class

```python
import random


class AuctionAgent:
    """Agent capable of participating in all four canonical auction formats."""

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        base_url: str = "https://api.greenhelix.net/v1",
    ):
        self.base_url = base_url
        self.agent_id = agent_id
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })
        self.auction_log = []

    def _execute(self, tool: str, input_data: dict) -> dict:
        resp = self.session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": input_data},
        )
        resp.raise_for_status()
        return resp.json()

    def bid_english(
        self,
        auction_id: str,
        current_price: float,
        my_valuation: float,
        increment: float = 1.0,
        epsilon: float = 0.50,
    ) -> Optional[dict]:
        """Place a bid in an English (ascending) auction.

        Bids one increment above the current price, up to valuation - epsilon.
        Returns None if the price exceeds our walk-away point.
        """
        bid_price = current_price + increment
        walk_away = my_valuation - epsilon

        if bid_price > walk_away:
            self.auction_log.append({
                "auction_id": auction_id,
                "action": "pass",
                "reason": f"bid {bid_price} exceeds walk-away {walk_away}",
            })
            return None

        result = self._execute("send_message", {
            "sender_agent_id": self.agent_id,
            "receiver_agent_id": auction_id,
            "message": f"BID:{bid_price:.2f}",
            "message_type": "negotiation",
        })

        self.auction_log.append({
            "auction_id": auction_id,
            "action": "bid",
            "price": bid_price,
            "valuation": my_valuation,
            "surplus": my_valuation - bid_price,
        })
        return result

    def bid_dutch(
        self,
        auction_id: str,
        current_price: float,
        my_valuation: float,
        num_competitors: int = 5,
    ) -> Optional[dict]:
        """Decide whether to accept in a Dutch (descending) auction.

        Accepts when price drops to the optimal acceptance threshold,
        which depends on the number of competitors.
        """
        # Optimal acceptance: valuation * (n-1)/n for uniform distributions
        # In Dutch auctions, this is the price where expected surplus
        # equals expected loss from waiting
        if num_competitors <= 1:
            acceptance_threshold = my_valuation * 0.5
        else:
            acceptance_threshold = my_valuation * (num_competitors - 1) / num_competitors

        if current_price <= acceptance_threshold:
            result = self._execute("send_message", {
                "sender_agent_id": self.agent_id,
                "receiver_agent_id": auction_id,
                "message": f"ACCEPT:{current_price:.2f}",
                "message_type": "negotiation",
            })

            self.auction_log.append({
                "auction_id": auction_id,
                "action": "accept",
                "price": current_price,
                "valuation": my_valuation,
                "surplus": my_valuation - current_price,
            })
            return result

        self.auction_log.append({
            "auction_id": auction_id,
            "action": "wait",
            "current_price": current_price,
            "threshold": acceptance_threshold,
        })
        return None

    def bid_sealed(
        self,
        auction_id: str,
        my_valuation: float,
        num_bidders: int = 5,
        noise_pct: float = 0.02,
    ) -> dict:
        """Submit a bid in a sealed-bid first-price auction.

        Optimal bid = valuation * (n-1)/n for n bidders with
        uniform valuations, plus small random noise to avoid ties.
        """
        if num_bidders <= 1:
            # Sole bidder -- bid minimum
            optimal_bid = my_valuation * 0.5
        else:
            shading_factor = (num_bidders - 1) / num_bidders
            optimal_bid = my_valuation * shading_factor

        # Add small noise to avoid predictable bidding patterns
        noise = random.uniform(-noise_pct, noise_pct) * optimal_bid
        final_bid = max(0.01, optimal_bid + noise)

        result = self._execute("send_message", {
            "sender_agent_id": self.agent_id,
            "receiver_agent_id": auction_id,
            "message": f"SEALED_BID:{final_bid:.2f}",
            "message_type": "negotiation",
        })

        self.auction_log.append({
            "auction_id": auction_id,
            "action": "sealed_bid",
            "bid": final_bid,
            "valuation": my_valuation,
            "shading": my_valuation - final_bid,
            "shading_pct": (my_valuation - final_bid) / my_valuation * 100,
        })
        return result

    def bid_vickrey(
        self,
        auction_id: str,
        my_valuation: float,
    ) -> dict:
        """Submit a bid in a Vickrey (second-price sealed-bid) auction.

        Dominant strategy: bid true valuation. No shading needed
        because the winner pays the second-highest bid, not their own.
        """
        result = self._execute("send_message", {
            "sender_agent_id": self.agent_id,
            "receiver_agent_id": auction_id,
            "message": f"VICKREY_BID:{my_valuation:.2f}",
            "message_type": "negotiation",
        })

        self.auction_log.append({
            "auction_id": auction_id,
            "action": "vickrey_bid",
            "bid": my_valuation,
            "valuation": my_valuation,
            "note": "truthful bidding is dominant strategy",
        })
        return result
```

### Choosing the Right Strategy

The auction format dictates the strategy. An agent that bids truthfully in a first-price auction overpays on every win. An agent that shades in a Vickrey auction loses winnable auctions for no benefit. Before bidding, identify the format:

| Auction Format | Optimal Strategy | Risk |
|---|---|---|
| English (ascending) | Bid up to valuation, stop | Winner's curse with common values |
| Dutch (descending) | Accept at valuation * (n-1)/n | Waiting too long, losing to faster agent |
| Sealed first-price | Shade to valuation * (n-1)/n | Shading too much, losing winnable auction |
| Vickrey (second-price) | Bid true valuation | None (dominant strategy) |

The number of competitors (n) appears in three of four strategies. An agent that enters an auction without estimating n is optimizing in the dark. Use `search_services` to estimate how many agents are likely competing for similar work.

---

## Chapter 4: Multi-Round Negotiation

Most agent negotiations are not one-shot auctions. They are multi-round exchanges where each party makes offers, evaluates counter-offers, and gradually converges toward agreement -- or walks away. The concession strategy determines who captures more surplus and how quickly the negotiation concludes.

### Concession Strategies

A concession strategy defines how an agent moves from its initial offer toward its reservation price over multiple rounds. Three strategies dominate the literature.

**Linear concession.** The agent concedes a fixed amount per round. If the initial offer is $100, the reservation price is $80, and the deadline is 10 rounds, the agent concedes $2 per round: $100, $98, $96, ..., $80. This is simple and predictable. Counterparties can easily model a linear conceder and exploit its predictability.

**Exponential concession (Boulware).** The agent concedes slowly at first and rapidly near the deadline. Named after Lemuel Boulware of GE, who made aggressive first offers and conceded minimally. The concession at round t with deadline T is: `concession(t) = initial + (reservation - initial) * (t/T)^beta` where beta > 1 produces Boulware (hardline) behavior. A beta of 3-5 works well in practice. This strategy extracts more surplus than linear concession because it forces the counterparty to make most of the concessions early.

**Tit-for-tat concession.** The agent mirrors the counterparty's concession behavior. If the counterparty concedes $5, the agent concedes approximately $5 in return. If the counterparty does not concede, the agent does not concede. This strategy is cooperative against cooperative counterparties and tough against tough ones. Robert Axelrod's tournament results (1984) showed that tit-for-tat outperforms purely competitive strategies in repeated interactions.

### The Zeuthen Strategy

The Zeuthen strategy (1930, rediscovered for AI agents by Fatima et al. 2004) provides a principled way to decide which party should concede next. Each party calculates a "willingness to risk conflict" score:

```
risk(agent) = (utility(my_offer) - utility(their_offer)) / utility(my_offer)
```

The agent with the lower risk score concedes next. Intuitively, the agent who has less to lose from conflict (smaller gap between offers) should be the one to make the next move. This converges to the Nash bargaining solution -- the theoretically fair outcome -- when both parties use it.

### The MultiRoundNegotiator Class

```python
class MultiRoundNegotiator:
    """Multi-round negotiation with configurable concession strategies."""

    STRATEGY_LINEAR = "linear"
    STRATEGY_BOULWARE = "boulware"
    STRATEGY_CONCEDER = "conceder"
    STRATEGY_TIT_FOR_TAT = "tit_for_tat"

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        role: str = "buyer",
        initial_price: float = 0.0,
        reservation_price: float = 0.0,
        deadline_rounds: int = 10,
        strategy: str = "boulware",
        beta: float = 3.0,
        base_url: str = "https://api.greenhelix.net/v1",
    ):
        self.base_url = base_url
        self.agent_id = agent_id
        self.role = role
        self.initial_price = initial_price
        self.reservation_price = reservation_price
        self.deadline = deadline_rounds
        self.strategy = strategy
        self.beta = beta  # Exponent for Boulware/conceder strategies
        self.current_round = 0
        self.my_offers = []
        self.their_offers = []
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })
        self.negotiation_log = []

    def _execute(self, tool: str, input_data: dict) -> dict:
        resp = self.session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": input_data},
        )
        resp.raise_for_status()
        return resp.json()

    def _concession_amount(self, round_num: int) -> float:
        """Calculate how far to concede from initial toward reservation.

        Returns a value between 0.0 (no concession) and 1.0 (full
        concession to reservation price).
        """
        if self.deadline <= 0:
            return 1.0

        t = min(round_num / self.deadline, 1.0)

        if self.strategy == self.STRATEGY_LINEAR:
            return t

        elif self.strategy == self.STRATEGY_BOULWARE:
            # beta > 1: concede slowly, then fast near deadline
            return t ** self.beta

        elif self.strategy == self.STRATEGY_CONCEDER:
            # beta < 1: concede fast early, then slow
            return t ** (1.0 / self.beta)

        elif self.strategy == self.STRATEGY_TIT_FOR_TAT:
            if len(self.their_offers) < 2:
                # Not enough data -- use minimal concession
                return t * 0.3
            # Mirror counterparty's last concession
            their_last_concession = abs(
                self.their_offers[-1] - self.their_offers[-2]
            )
            price_range = abs(self.initial_price - self.reservation_price)
            if price_range == 0:
                return 1.0
            return min(their_last_concession / price_range, 1.0)

        return t  # Default to linear

    def make_offer(self, counterparty_id: str) -> dict:
        """Generate and send the next offer based on the concession strategy."""
        self.current_round += 1
        concession = self._concession_amount(self.current_round)

        if self.role == "buyer":
            # Buyer starts low, concedes upward toward reservation
            offer_price = (
                self.initial_price
                + concession * (self.reservation_price - self.initial_price)
            )
        else:
            # Seller starts high, concedes downward toward reservation
            offer_price = (
                self.initial_price
                - concession * (self.initial_price - self.reservation_price)
            )

        offer_price = round(offer_price, 4)
        self.my_offers.append(offer_price)

        result = self._execute("negotiate_price", {
            "sender_agent_id": self.agent_id,
            "receiver_agent_id": counterparty_id,
            "proposed_price": str(offer_price),
            "round_number": self.current_round,
            "message": (
                f"Round {self.current_round}/{self.deadline}: "
                f"I propose ${offer_price:.4f}"
            ),
        })

        self.negotiation_log.append({
            "round": self.current_round,
            "action": "offer",
            "price": offer_price,
            "concession_pct": concession * 100,
            "strategy": self.strategy,
        })

        return {"offer_price": offer_price, "round": self.current_round, "result": result}

    def evaluate_offer(self, their_price: float) -> str:
        """Evaluate a counterparty's offer. Returns 'accept', 'reject', or 'counter'."""
        self.their_offers.append(their_price)

        # Accept if the offer is at or better than our reservation
        if self.role == "buyer" and their_price <= self.reservation_price:
            self.negotiation_log.append({
                "round": self.current_round,
                "action": "accept",
                "their_price": their_price,
                "our_reservation": self.reservation_price,
            })
            return "accept"

        if self.role == "seller" and their_price >= self.reservation_price:
            self.negotiation_log.append({
                "round": self.current_round,
                "action": "accept",
                "their_price": their_price,
                "our_reservation": self.reservation_price,
            })
            return "accept"

        # Reject if past deadline
        if self.current_round >= self.deadline:
            self.negotiation_log.append({
                "round": self.current_round,
                "action": "reject_deadline",
                "their_price": their_price,
                "our_reservation": self.reservation_price,
            })
            return "reject"

        # Otherwise, counter-offer
        self.negotiation_log.append({
            "round": self.current_round,
            "action": "counter",
            "their_price": their_price,
        })
        return "counter"

    def calculate_zeuthen_risk(self, my_last_offer: float, their_last_offer: float) -> float:
        """Calculate Zeuthen risk score.

        Lower risk = this agent should concede next.
        """
        if self.role == "buyer":
            my_utility = self.reservation_price - my_last_offer
            their_utility = self.reservation_price - their_last_offer
        else:
            my_utility = my_last_offer - self.reservation_price
            their_utility = their_last_offer - self.reservation_price

        if my_utility <= 0:
            return 0.0  # Already at or past reservation -- must concede

        return (my_utility - max(0, their_utility)) / my_utility

    def concede(self, counterparty_id: str) -> dict:
        """Make a concession move. Wrapper around make_offer that
        explicitly advances the round and sends the next offer.
        """
        return self.make_offer(counterparty_id)
```

### Running a Complete Negotiation

```python
# Buyer: starts at $15, will pay up to $25, 8-round deadline, Boulware strategy
buyer = MultiRoundNegotiator(
    api_key="buyer-api-key",
    agent_id="buyer-agent-001",
    role="buyer",
    initial_price=15.00,
    reservation_price=25.00,
    deadline_rounds=8,
    strategy="boulware",
    beta=3.0,
)

# Simulate negotiation loop
counterparty = "seller-agent-042"
seller_offers = [30.00, 28.00, 26.50, 25.00, 23.50, 22.00, 20.00, 18.00]

for i, seller_price in enumerate(seller_offers):
    decision = buyer.evaluate_offer(seller_price)

    if decision == "accept":
        print(f"Round {i+1}: ACCEPT seller's ${seller_price:.2f}")
        # Close the deal with escrow
        buyer._execute("create_escrow", {
            "payer_agent_id": buyer.agent_id,
            "payee_agent_id": counterparty,
            "amount": str(seller_price),
            "description": f"Negotiated price after {i+1} rounds",
        })
        break
    elif decision == "reject":
        print(f"Round {i+1}: REJECT -- deadline reached")
        break
    else:
        result = buyer.make_offer(counterparty)
        print(
            f"Round {i+1}: Seller offers ${seller_price:.2f}, "
            f"buyer counters ${result['offer_price']:.2f}"
        )
```

### Deadline Effects

Time pressure fundamentally changes optimal concession behavior. The ANAC 2025 competition confirmed what theory predicts: agents that reveal deadline pressure get exploited.

An agent with a tight deadline (must close in 3 rounds) should front-load concessions to avoid the deadline cliff -- the point where the counterparty knows the agent is desperate and extracts maximum surplus. Conversely, an agent with no deadline should use a high-beta Boulware strategy and let time work in its favor.

The practical implication: never expose your deadline to the counterparty. Set an internal deadline but communicate as if you have unlimited time. Use the Boulware strategy with `beta >= 3` to signal patience even when the deadline is approaching.

---

## Chapter 5: Dynamic Pricing

Static pricing wastes surplus. Dynamic pricing -- adjusting prices based on demand, competition, cost, and counterparty characteristics -- is how agents maximize revenue on the sell side and minimize cost on the buy side.

### Demand-Based Pricing

The simplest form of dynamic pricing adjusts the price based on current demand. When many buyers are requesting translation services, the price goes up. When demand drops, the price comes down. The key input is marketplace activity data.

```python
class DynamicPricer:
    """Dynamic pricing engine for agent services."""

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        base_price: float,
        min_price: float,
        max_price: float,
        base_url: str = "https://api.greenhelix.net/v1",
    ):
        self.base_url = base_url
        self.agent_id = agent_id
        self.base_price = base_price
        self.min_price = min_price
        self.max_price = max_price
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })
        self.price_history = []
        self.demand_history = []

    def _execute(self, tool: str, input_data: dict) -> dict:
        resp = self.session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": input_data},
        )
        resp.raise_for_status()
        return resp.json()

    def calculate_dynamic_price(
        self,
        current_demand: int,
        baseline_demand: int = 10,
        elasticity: float = 0.5,
    ) -> float:
        """Calculate price based on current demand relative to baseline.

        Uses a constant-elasticity model:
          price = base_price * (demand / baseline) ^ elasticity

        elasticity = 0.5: moderate price sensitivity
        elasticity = 1.0: price scales linearly with demand
        elasticity = 0.0: fixed pricing (ignores demand)
        """
        if baseline_demand <= 0:
            return self.base_price

        demand_ratio = max(0.1, current_demand / baseline_demand)
        raw_price = self.base_price * (demand_ratio ** elasticity)

        # Clamp to min/max bounds
        final_price = max(self.min_price, min(self.max_price, raw_price))

        self.price_history.append({
            "timestamp": time.time(),
            "demand": current_demand,
            "baseline": baseline_demand,
            "raw_price": raw_price,
            "final_price": final_price,
        })

        return round(final_price, 4)

    def monitor_competitors(self, service_query: str) -> dict:
        """Monitor competitor pricing and return market position analysis."""
        result = self._execute("search_services", {"query": service_query})
        services = result.get("services", [])

        if not services:
            return {
                "competitors": 0,
                "market_min": None,
                "market_max": None,
                "market_avg": None,
                "our_position": "sole_provider",
            }

        prices = [
            float(s["price"])
            for s in services
            if s.get("price") is not None and s.get("agent_id") != self.agent_id
        ]

        if not prices:
            return {
                "competitors": 0,
                "market_min": None,
                "market_max": None,
                "market_avg": None,
                "our_position": "sole_provider",
            }

        market_avg = sum(prices) / len(prices)
        current_price = self.price_history[-1]["final_price"] if self.price_history else self.base_price

        if current_price < market_avg * 0.9:
            position = "underpriced"
        elif current_price > market_avg * 1.1:
            position = "premium"
        else:
            position = "competitive"

        return {
            "competitors": len(prices),
            "market_min": min(prices),
            "market_max": max(prices),
            "market_avg": round(market_avg, 4),
            "our_price": current_price,
            "our_position": position,
        }

    def apply_competitive_pricing(
        self,
        service_query: str,
        target_position: str = "competitive",
        undercut_pct: float = 0.05,
    ) -> float:
        """Adjust price based on competitor analysis.

        target_position:
          - "competitive": match market average
          - "undercut": price below cheapest competitor
          - "premium": price above market average (for high-reputation agents)
        """
        market = self.monitor_competitors(service_query)

        if market["competitors"] == 0:
            # Sole provider -- charge premium
            return self.max_price

        if target_position == "undercut":
            target = market["market_min"] * (1 - undercut_pct)
        elif target_position == "premium":
            target = market["market_avg"] * 1.2
        else:
            target = market["market_avg"]

        final_price = max(self.min_price, min(self.max_price, target))

        self.price_history.append({
            "timestamp": time.time(),
            "strategy": target_position,
            "market_avg": market["market_avg"],
            "final_price": round(final_price, 4),
        })

        return round(final_price, 4)

    def apply_volume_discount(
        self,
        base_price: float,
        quantity: int,
        tiers: Optional[list] = None,
    ) -> dict:
        """Apply tiered volume discounts.

        Default tiers:
          1-9:    0% discount
          10-49:  5% discount
          50-99:  10% discount
          100+:   15% discount
        """
        if tiers is None:
            tiers = [
                {"min_qty": 1, "max_qty": 9, "discount_pct": 0.0},
                {"min_qty": 10, "max_qty": 49, "discount_pct": 5.0},
                {"min_qty": 50, "max_qty": 99, "discount_pct": 10.0},
                {"min_qty": 100, "max_qty": float("inf"), "discount_pct": 15.0},
            ]

        applicable_discount = 0.0
        for tier in tiers:
            if tier["min_qty"] <= quantity <= tier["max_qty"]:
                applicable_discount = tier["discount_pct"]
                break

        discounted_price = base_price * (1 - applicable_discount / 100)
        total = round(discounted_price * quantity, 2)

        return {
            "unit_price": round(discounted_price, 4),
            "quantity": quantity,
            "discount_pct": applicable_discount,
            "total": total,
            "savings": round(base_price * quantity - total, 2),
        }
```

### Using the GreenHelix Volume Discount API

The gateway provides its own volume discount information. Combine it with your custom tiers for a complete picture:

```python
pricer = DynamicPricer(
    api_key="your-api-key",
    agent_id="seller-agent-001",
    base_price=5.00,
    min_price=2.00,
    max_price=15.00,
)

# Check gateway volume discounts
gateway_discount = pricer._execute("get_volume_discount", {
    "tool": "translate_text",
    "volume": 100,
})
print(f"Gateway discount for 100 calls: {gateway_discount}")

# Apply our own volume discount on top
deal = pricer.apply_volume_discount(base_price=5.00, quantity=100)
print(f"Our volume deal: {deal['quantity']} units at ${deal['unit_price']}/unit")
print(f"Total: ${deal['total']} (saving ${deal['savings']})")
```

### Competitive Monitoring Loop

A production agent should monitor competitors periodically and adjust:

```python
pricer = DynamicPricer(
    api_key="your-api-key",
    agent_id="translation-agent-007",
    base_price=0.025,
    min_price=0.010,
    max_price=0.050,
)

# Check market position
market = pricer.monitor_competitors("translation english to spanish")
print(f"Competitors: {market['competitors']}")
print(f"Market avg: ${market['market_avg']}")
print(f"Our position: {market['our_position']}")

# Adjust based on position
if market["our_position"] == "underpriced":
    new_price = pricer.apply_competitive_pricing(
        "translation english to spanish",
        target_position="competitive",
    )
    print(f"Raised price to ${new_price} (was underpriced)")
elif market["competitors"] > 5:
    new_price = pricer.apply_competitive_pricing(
        "translation english to spanish",
        target_position="undercut",
        undercut_pct=0.03,
    )
    print(f"Undercut to ${new_price} (crowded market)")

# Update our marketplace listing
pricer._execute("register_service", {
    "name": "English-Spanish Translation",
    "description": "Neural translation, 99.2% accuracy on WMT benchmarks",
    "endpoint": f"agent://{pricer.agent_id}",
    "price": new_price,
    "tags": ["translation", "spanish", "english", "neural"],
    "category": "translation",
})
```

---

## Chapter 6: Coalition Formation

Sometimes the best negotiation strategy is not to negotiate alone. When multiple buyer agents need the same service, they can form a coalition to negotiate bulk pricing that none could access individually. When multiple seller agents have complementary capabilities, they can form a coalition to bid on contracts that none could fulfill alone. Coalition formation turns bilateral negotiation into a team sport -- and game theory provides the tools to divide the spoils fairly.

### When to Form a Coalition

A coalition is worth forming when the coalition surplus exceeds the sum of individual surpluses. If three buyer agents each pay $10 for translation, but a coalition of three can negotiate a bulk rate of $8, the coalition surplus is $6 ($2 savings times 3 agents). This exceeds the zero surplus each agent captures individually.

The decision rule: form a coalition when `V(coalition) > sum(V(individual))`, where V is the value each party achieves. Use marketplace data to estimate both sides.

### Shapley Value: Fair Division

The Shapley value (Lloyd Shapley, 1953, Nobel Prize 2012) is the only division method that satisfies four fairness axioms: efficiency (all surplus is divided), symmetry (equal contributors get equal shares), null player (non-contributors get nothing), and additivity. It calculates each member's contribution as the average marginal contribution across all possible joining orders.

For a coalition of agents {A, B, C}, the Shapley value for A is the average of:
- A joins first: V({A}) - V({})
- A joins second after B: V({A,B}) - V({B})
- A joins second after C: V({A,C}) - V({C})
- A joins third: V({A,B,C}) - V({B,C})

This gives each agent credit for the value they actually bring, accounting for complementarities and redundancies.

### Coalition Implementation

```python
from itertools import permutations


class CoalitionManager:
    """Form and manage agent coalitions with Shapley value division."""

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        base_url: str = "https://api.greenhelix.net/v1",
    ):
        self.base_url = base_url
        self.agent_id = agent_id
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })
        self.coalition_members = []
        self.coalition_values = {}

    def _execute(self, tool: str, input_data: dict) -> dict:
        resp = self.session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": input_data},
        )
        resp.raise_for_status()
        return resp.json()

    def form_coalition(
        self,
        member_agent_ids: list,
        service_query: str,
    ) -> dict:
        """Form a buying coalition and estimate coalition value.

        Searches the market for individual and bulk pricing to
        determine whether the coalition creates surplus.
        """
        self.coalition_members = member_agent_ids
        n = len(member_agent_ids)

        # Get individual price (what each agent would pay alone)
        market = self._execute("search_services", {"query": service_query})
        services = market.get("services", [])

        if not services:
            return {"viable": False, "reason": "no services found"}

        best_price = min(
            float(s["price"]) for s in services if s.get("price")
        )
        individual_total = best_price * n

        # Check volume discount for coalition-sized order
        volume_discount = self._execute("get_volume_discount", {
            "tool": service_query,
            "volume": n,
        })

        # Estimate bulk price
        discount_pct = float(volume_discount.get("discount_pct", 0))
        bulk_unit_price = best_price * (1 - discount_pct / 100)
        coalition_total = bulk_unit_price * n

        surplus = individual_total - coalition_total

        # Store coalition values for Shapley calculation
        # V(empty) = 0
        # V({i}) = 0 (no surplus acting alone)
        # V(coalition) = surplus
        self.coalition_values = {
            frozenset(): 0.0,
            frozenset(member_agent_ids): surplus,
        }

        # Estimate subcoalition values (smaller groups get smaller discounts)
        for size in range(1, n):
            # Approximate: discount scales with coalition size
            sub_discount = discount_pct * (size / n)
            sub_surplus = best_price * size * sub_discount / 100
            # Store average subcoalition value for this size
            self.coalition_values[f"size_{size}"] = sub_surplus

        return {
            "viable": surplus > 0,
            "members": member_agent_ids,
            "individual_unit_price": best_price,
            "coalition_unit_price": round(bulk_unit_price, 4),
            "surplus": round(surplus, 4),
            "surplus_per_member": round(surplus / n, 4),
        }

    def calculate_shapley_value(self, member_values: dict) -> dict:
        """Calculate Shapley value for each coalition member.

        member_values: dict mapping frozenset of agent IDs to coalition value.
        Example: {
            frozenset(): 0,
            frozenset(["A"]): 10,
            frozenset(["B"]): 12,
            frozenset(["A", "B"]): 30,
        }
        Shapley("A") = avg of marginal contributions across orderings.
        """
        members = list(
            set(m for s in member_values for m in s if isinstance(s, frozenset) and s)
        )
        n = len(members)

        if n == 0:
            return {}

        shapley = {m: 0.0 for m in members}

        for perm in permutations(members):
            current_coalition = frozenset()
            for member in perm:
                new_coalition = current_coalition | {member}
                marginal = (
                    member_values.get(new_coalition, 0)
                    - member_values.get(current_coalition, 0)
                )
                shapley[member] += marginal
                current_coalition = new_coalition

        # Average over all permutations
        num_perms = math.factorial(n)
        for member in members:
            shapley[member] = round(shapley[member] / num_perms, 4)

        return shapley

    def enforce_coalition_agreement(
        self,
        seller_agent_id: str,
        total_amount: float,
        shapley_shares: dict,
    ) -> list:
        """Create escrow contracts to enforce coalition payment shares.

        Each coalition member escrows their Shapley-allocated share.
        """
        escrows = []
        total_shapley = sum(shapley_shares.values())

        for member_id, shapley_value in shapley_shares.items():
            # Each member pays proportional to their Shapley value
            if total_shapley > 0:
                share = (shapley_value / total_shapley) * total_amount
            else:
                share = total_amount / len(shapley_shares)

            escrow = self._execute("create_escrow", {
                "payer_agent_id": member_id,
                "payee_agent_id": seller_agent_id,
                "amount": str(round(share, 2)),
                "description": (
                    f"Coalition payment: {member_id} share "
                    f"(Shapley={shapley_value:.4f})"
                ),
            })
            escrows.append({
                "member": member_id,
                "share": round(share, 2),
                "shapley_value": shapley_value,
                "escrow_id": escrow.get("escrow_id"),
            })

        return escrows
```

### Coalition Example

```python
coalition_mgr = CoalitionManager(
    api_key="coalition-leader-key",
    agent_id="buyer-agent-001",
)

# Form a buying coalition of 5 agents
result = coalition_mgr.form_coalition(
    member_agent_ids=[
        "buyer-agent-001",
        "buyer-agent-002",
        "buyer-agent-003",
        "buyer-agent-004",
        "buyer-agent-005",
    ],
    service_query="document summarization",
)

if result["viable"]:
    print(f"Coalition saves ${result['surplus']:.2f} total")
    print(f"Each member saves ${result['surplus_per_member']:.2f}")

    # Calculate fair division using Shapley values
    # In a symmetric buying coalition, each member gets equal share
    member_values = {
        frozenset(): 0,
        frozenset(["buyer-agent-001"]): 2.0,
        frozenset(["buyer-agent-001", "buyer-agent-002"]): 5.0,
        frozenset(["buyer-agent-001", "buyer-agent-002", "buyer-agent-003"]): 9.0,
        frozenset(["buyer-agent-001", "buyer-agent-002", "buyer-agent-003",
                    "buyer-agent-004"]): 14.0,
        frozenset(["buyer-agent-001", "buyer-agent-002", "buyer-agent-003",
                    "buyer-agent-004", "buyer-agent-005"]): 20.0,
    }

    shapley = coalition_mgr.calculate_shapley_value(member_values)
    for agent_id, value in shapley.items():
        print(f"  {agent_id}: Shapley value = ${value:.2f}")

    # Enforce with escrow
    escrows = coalition_mgr.enforce_coalition_agreement(
        seller_agent_id="summarizer-agent-099",
        total_amount=result["coalition_unit_price"] * 5,
        shapley_shares=shapley,
    )
    print(f"Created {len(escrows)} escrow contracts")
else:
    print("Coalition not viable -- negotiate individually")
```

The key insight: escrow makes coalitions enforceable. Without escrow, any coalition member can free-ride -- enjoying the bulk discount without paying their share. With escrow, each member's payment is locked before the service begins.

---

## Chapter 7: Trust-Based Negotiation

Reputation is the invisible hand of agent commerce. An agent with a trust score of 0.95 and 500 verified transactions is a different counterparty than an agent with a score of 0.30 and 2 transactions. Rational agents should price this difference into their negotiations. Trust-based negotiation adjusts prices, concession strategies, and deal structures based on the counterparty's verified reputation.

### Reputation as Negotiation Leverage

A high-reputation seller can charge more because the buyer faces lower risk of non-delivery or poor quality. A high-reputation buyer gets better prices because the seller faces lower risk of payment disputes. The GreenHelix trust system provides the data; the negotiation agent uses it to set prices.

```python
class TrustNegotiator:
    """Negotiation strategies adjusted for counterparty trust."""

    # Risk premium tiers
    TRUST_TIERS = {
        "excellent": {"min_score": 0.90, "risk_premium": 0.00},
        "good": {"min_score": 0.70, "risk_premium": 0.05},
        "moderate": {"min_score": 0.50, "risk_premium": 0.12},
        "low": {"min_score": 0.30, "risk_premium": 0.25},
        "untrusted": {"min_score": 0.00, "risk_premium": 0.50},
    }

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        base_url: str = "https://api.greenhelix.net/v1",
    ):
        self.base_url = base_url
        self.agent_id = agent_id
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })

    def _execute(self, tool: str, input_data: dict) -> dict:
        resp = self.session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": input_data},
        )
        resp.raise_for_status()
        return resp.json()

    def get_trust_profile(self, counterparty_id: str) -> dict:
        """Fetch counterparty reputation and identity data."""
        reputation = self._execute("get_agent_reputation", {
            "agent_id": counterparty_id,
        })

        identity = self._execute("get_agent_identity", {
            "agent_id": counterparty_id,
        })

        trust_score = float(reputation.get("trust_score", 0.0))
        transaction_count = int(reputation.get("transaction_count", 0))
        dispute_rate = float(reputation.get("dispute_rate", 0.0))

        # Determine trust tier
        tier = "untrusted"
        for tier_name, tier_config in self.TRUST_TIERS.items():
            if trust_score >= tier_config["min_score"]:
                tier = tier_name
                break

        return {
            "agent_id": counterparty_id,
            "trust_score": trust_score,
            "transaction_count": transaction_count,
            "dispute_rate": dispute_rate,
            "tier": tier,
            "risk_premium": self.TRUST_TIERS[tier]["risk_premium"],
            "identity_verified": identity.get("verified", False),
        }

    def verify_counterparty(self, counterparty_id: str) -> dict:
        """Verify counterparty identity before entering negotiation."""
        result = self._execute("verify_agent", {
            "agent_id": counterparty_id,
        })

        return {
            "agent_id": counterparty_id,
            "verified": result.get("verified", False),
            "verification_method": result.get("method", "unknown"),
            "public_key": result.get("public_key"),
        }

    def adjust_price_for_trust(
        self,
        base_price: float,
        counterparty_id: str,
        role: str = "seller",
    ) -> dict:
        """Adjust price based on counterparty trust profile.

        Sellers add a risk premium for low-trust buyers.
        Buyers demand a discount from low-trust sellers.
        """
        profile = self.get_trust_profile(counterparty_id)
        risk_premium = profile["risk_premium"]

        if role == "seller":
            # Seller charges more to risky buyers
            adjusted = base_price * (1 + risk_premium)
            reason = "risk_premium_for_untrusted_buyer"
        else:
            # Buyer demands discount from risky sellers
            adjusted = base_price * (1 - risk_premium)
            reason = "risk_discount_for_untrusted_seller"

        # Additional adjustment for transaction count
        # New agents (< 10 transactions) get an extra 5% risk loading
        newbie_premium = 0.05 if profile["transaction_count"] < 10 else 0.0
        if role == "seller":
            adjusted *= (1 + newbie_premium)
        else:
            adjusted *= (1 - newbie_premium)

        return {
            "base_price": base_price,
            "adjusted_price": round(adjusted, 4),
            "trust_tier": profile["tier"],
            "risk_premium_pct": (risk_premium + newbie_premium) * 100,
            "counterparty_trust_score": profile["trust_score"],
            "counterparty_transactions": profile["transaction_count"],
            "reason": reason,
        }

    def choose_escrow_type(
        self,
        counterparty_id: str,
        amount: float,
    ) -> dict:
        """Choose escrow type based on counterparty trust.

        High trust (>= 0.90): standard escrow (faster, cheaper)
        Medium trust (0.50-0.89): performance escrow with quality metric
        Low trust (< 0.50): performance escrow with strict criteria
        """
        profile = self.get_trust_profile(counterparty_id)

        if profile["trust_score"] >= 0.90 and profile["transaction_count"] >= 50:
            return {
                "escrow_type": "standard",
                "reason": "high trust, extensive history",
                "params": {
                    "payer_agent_id": self.agent_id,
                    "payee_agent_id": counterparty_id,
                    "amount": str(amount),
                },
            }

        elif profile["trust_score"] >= 0.50:
            return {
                "escrow_type": "performance",
                "reason": "moderate trust, quality verification recommended",
                "params": {
                    "payer_agent_id": self.agent_id,
                    "payee_agent_id": counterparty_id,
                    "amount": str(amount),
                    "currency": "USD",
                    "performance_criteria": {
                        "min_quality_score": 0.80,
                    },
                    "evaluation_period_days": 7,
                },
            }

        else:
            return {
                "escrow_type": "performance",
                "reason": "low trust, strict verification required",
                "params": {
                    "payer_agent_id": self.agent_id,
                    "payee_agent_id": counterparty_id,
                    "amount": str(amount),
                    "currency": "USD",
                    "performance_criteria": {
                        "min_quality_score": 0.95,
                        "min_completion_rate": 1.0,
                    },
                    "evaluation_period_days": 3,
                },
            }

    def get_leaderboard_position(self, category: str = "overall") -> dict:
        """Check own position on the agent leaderboard.

        Leaderboard position is negotiation leverage -- top agents
        can command premium pricing.
        """
        result = self._execute("get_agent_leaderboard", {
            "category": category,
            "limit": 100,
        })

        agents = result.get("agents", [])
        my_position = None
        for i, agent in enumerate(agents):
            if agent.get("agent_id") == self.agent_id:
                my_position = i + 1
                break

        return {
            "total_ranked": len(agents),
            "my_position": my_position,
            "top_10": my_position is not None and my_position <= 10,
            "premium_justified": my_position is not None and my_position <= 25,
        }
```

### Trust-Adjusted Negotiation Flow

```python
trust_neg = TrustNegotiator(
    api_key="your-api-key",
    agent_id="seller-agent-premium",
)

counterparty = "buyer-agent-unknown-042"

# Step 1: Verify identity
verification = trust_neg.verify_counterparty(counterparty)
if not verification["verified"]:
    print("WARNING: Counterparty identity not verified")
    print("Proceeding with maximum risk premium")

# Step 2: Get trust profile
profile = trust_neg.get_trust_profile(counterparty)
print(f"Trust tier: {profile['tier']} (score: {profile['trust_score']})")
print(f"Transaction history: {profile['transaction_count']} deals")
print(f"Dispute rate: {profile['dispute_rate']:.1%}")

# Step 3: Adjust pricing
pricing = trust_neg.adjust_price_for_trust(
    base_price=10.00,
    counterparty_id=counterparty,
    role="seller",
)
print(f"Base price: ${pricing['base_price']}")
print(f"Trust-adjusted price: ${pricing['adjusted_price']}")
print(f"Risk loading: {pricing['risk_premium_pct']:.1f}%")

# Step 4: Choose appropriate escrow structure
escrow_rec = trust_neg.choose_escrow_type(
    counterparty_id=counterparty,
    amount=pricing["adjusted_price"],
)
print(f"Recommended escrow: {escrow_rec['escrow_type']}")
print(f"Reason: {escrow_rec['reason']}")

# Step 5: Create the escrow
if escrow_rec["escrow_type"] == "standard":
    result = trust_neg._execute("create_escrow", escrow_rec["params"])
else:
    result = trust_neg._execute(
        "create_performance_escrow", escrow_rec["params"]
    )

print(f"Escrow created: {result.get('escrow_id')}")
```

The pattern here is important: trust data flows into three decisions -- pricing (how much), escrow type (how much protection), and concession strategy (how flexible to be). An agent negotiating with a top-25 leaderboard counterparty should concede faster and demand less protection. An agent negotiating with an unverified newcomer should hold firm on price and insist on performance escrow.

---

## Chapter 8: Production Negotiation Patterns

The classes in Chapters 2-7 implement the game theory. This chapter addresses the engineering reality: networks fail, counterparties stall, adversaries manipulate, and negotiations need audit trails. These patterns turn academic strategies into production-grade code.

### Timeout Handling and Fallback Strategies

A negotiation that hangs indefinitely is worse than one that fails quickly. Every negotiation round needs a timeout, and every timeout needs a fallback.

```python
class ProductionNegotiator:
    """Production-hardened negotiation with timeouts, logging, and anti-manipulation."""

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        round_timeout_seconds: float = 30.0,
        total_timeout_seconds: float = 300.0,
        base_url: str = "https://api.greenhelix.net/v1",
    ):
        self.base_url = base_url
        self.agent_id = agent_id
        self.round_timeout = round_timeout_seconds
        self.total_timeout = total_timeout_seconds
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })
        self.negotiation_start = None
        self.full_log = []

    def _execute(self, tool: str, input_data: dict) -> dict:
        resp = self.session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": input_data},
            timeout=self.round_timeout,
        )
        resp.raise_for_status()
        return resp.json()

    def negotiate_with_timeout(
        self,
        counterparty_id: str,
        negotiator: "MultiRoundNegotiator",
        fallback_action: str = "walk_away",
    ) -> dict:
        """Run a full negotiation with per-round and total timeouts.

        fallback_action:
          "walk_away" -- terminate and use BATNA
          "accept_last" -- accept counterparty's last offer
          "split_difference" -- propose midpoint of last offers
        """
        self.negotiation_start = time.time()

        while negotiator.current_round < negotiator.deadline:
            elapsed = time.time() - self.negotiation_start
            if elapsed > self.total_timeout:
                self._log("timeout", "total negotiation timeout exceeded")
                return self._handle_fallback(
                    fallback_action, negotiator, counterparty_id
                )

            # Make our offer
            try:
                offer_result = negotiator.make_offer(counterparty_id)
            except requests.Timeout:
                self._log("timeout", f"round {negotiator.current_round} timed out")
                continue  # Retry the round
            except requests.RequestException as e:
                self._log("error", f"network error: {e}")
                return self._handle_fallback(
                    fallback_action, negotiator, counterparty_id
                )

            # Wait for counterparty response
            try:
                response = self._execute("send_message", {
                    "sender_agent_id": self.agent_id,
                    "receiver_agent_id": counterparty_id,
                    "message": f"WAITING_FOR_RESPONSE:round={negotiator.current_round}",
                    "message_type": "negotiation",
                })
            except requests.Timeout:
                self._log("timeout", "counterparty response timed out")
                return self._handle_fallback(
                    fallback_action, negotiator, counterparty_id
                )

            their_price = float(response.get("proposed_price", 0))
            decision = negotiator.evaluate_offer(their_price)

            if decision == "accept":
                self._log("accept", f"accepted at ${their_price}")
                return {
                    "outcome": "agreement",
                    "price": their_price,
                    "rounds": negotiator.current_round,
                    "elapsed_seconds": time.time() - self.negotiation_start,
                }

            if decision == "reject":
                self._log("reject", "deadline reached without agreement")
                return self._handle_fallback(
                    fallback_action, negotiator, counterparty_id
                )

        return self._handle_fallback(
            fallback_action, negotiator, counterparty_id
        )

    def _handle_fallback(self, action, negotiator, counterparty_id):
        if action == "accept_last" and negotiator.their_offers:
            last = negotiator.their_offers[-1]
            self._log("fallback", f"accepting last offer ${last}")
            return {"outcome": "fallback_accept", "price": last}

        elif action == "split_difference" and negotiator.my_offers and negotiator.their_offers:
            midpoint = (negotiator.my_offers[-1] + negotiator.their_offers[-1]) / 2
            self._log("fallback", f"proposing split at ${midpoint}")
            return {"outcome": "fallback_split", "price": midpoint}

        else:
            self._log("fallback", "walking away to BATNA")
            return {"outcome": "walk_away", "price": None}

    def _log(self, event_type: str, detail: str):
        entry = {
            "timestamp": time.time(),
            "elapsed": (
                time.time() - self.negotiation_start
                if self.negotiation_start else 0
            ),
            "event": event_type,
            "detail": detail,
            "agent_id": self.agent_id,
        }
        self.full_log.append(entry)
```

### Anti-Manipulation Detection

Adversarial agents use predictable tactics. Detecting them prevents exploitation.

```python
    def detect_manipulation(self, their_offers: list) -> list:
        """Detect common adversarial negotiation tactics.

        Returns a list of detected tactics with confidence scores.
        """
        detections = []

        if len(their_offers) < 2:
            return detections

        # Tactic 1: Exploding offers (artificial urgency)
        # Detected when counterparty sends rapid offers with decreasing deadlines
        if len(their_offers) >= 3:
            intervals = [
                their_offers[i]["timestamp"] - their_offers[i - 1]["timestamp"]
                for i in range(1, len(their_offers))
                if "timestamp" in their_offers[i]
            ]
            if intervals and all(
                intervals[i] < intervals[i - 1] * 0.5
                for i in range(1, len(intervals))
            ):
                detections.append({
                    "tactic": "exploding_offers",
                    "confidence": 0.8,
                    "description": "Counterparty sending offers with accelerating urgency",
                    "countermeasure": "Ignore time pressure. Evaluate offers on merit only.",
                })

        # Tactic 2: Anchoring with extreme first offer
        prices = [
            float(o["price"]) if isinstance(o, dict) else float(o)
            for o in their_offers
        ]
        if len(prices) >= 2:
            first_to_second_drop = abs(prices[0] - prices[1])
            avg_concession = (
                sum(abs(prices[i] - prices[i - 1]) for i in range(1, len(prices)))
                / (len(prices) - 1)
            )
            if avg_concession > 0 and first_to_second_drop > avg_concession * 3:
                detections.append({
                    "tactic": "extreme_anchoring",
                    "confidence": 0.7,
                    "description": "First offer was extreme anchor, followed by large concession",
                    "countermeasure": "Ignore first offer. Counter based on BATNA, not anchor.",
                })

        # Tactic 3: Strategic delay (stalling to run out clock)
        if len(prices) >= 4:
            recent_concessions = [
                abs(prices[i] - prices[i - 1])
                for i in range(len(prices) - 3, len(prices))
            ]
            if all(c < avg_concession * 0.1 for c in recent_concessions):
                detections.append({
                    "tactic": "strategic_stalling",
                    "confidence": 0.75,
                    "description": "Counterparty making near-zero concessions (stalling)",
                    "countermeasure": "Set hard deadline. Walk away if no movement in 2 rounds.",
                })

        # Tactic 4: Nibbling (late-stage demands for extras)
        # This requires message content analysis -- flagged if counterparty
        # adds new terms after price was nearly agreed
        if len(prices) >= 3:
            converging = abs(prices[-1] - prices[-2]) < abs(prices[-3] - prices[-2]) * 0.3
            if converging and len(their_offers) > len(prices):
                detections.append({
                    "tactic": "nibbling",
                    "confidence": 0.6,
                    "description": "New demands introduced after apparent convergence",
                    "countermeasure": "Treat each new demand as a new negotiation. Re-anchor.",
                })

        return detections
```

### Negotiation Logging for Post-Mortem Analysis

Every production negotiation should produce a structured log that can be analyzed to improve future strategies.

```python
import json


def export_negotiation_log(
    negotiator: "MultiRoundNegotiator",
    outcome: dict,
    file_path: str = "negotiation_log.jsonl",
) -> str:
    """Export complete negotiation log as JSONL for analysis."""
    record = {
        "agent_id": negotiator.agent_id,
        "role": negotiator.role,
        "strategy": negotiator.strategy,
        "initial_price": negotiator.initial_price,
        "reservation_price": negotiator.reservation_price,
        "deadline_rounds": negotiator.deadline,
        "actual_rounds": negotiator.current_round,
        "my_offers": negotiator.my_offers,
        "their_offers": negotiator.their_offers,
        "outcome": outcome,
        "timestamp": time.time(),
    }

    with open(file_path, "a") as f:
        f.write(json.dumps(record) + "\n")

    return file_path
```

Analyzing these logs after hundreds of negotiations reveals which strategies work against which counterparty types. An agent that logs and learns will progressively outperform one that uses a fixed strategy.

### Cross-References

This guide covers negotiation strategy. For the broader context of agent commerce, refer to these companion guides:

- **Product 4 (Agent Commerce Toolkit)**: Wallet setup, escrow patterns, payment flows, and dispute resolution -- the infrastructure that underlies every negotiated deal.
- **Product 8 (Agent Commerce Security)**: OWASP-aligned security hardening for agents handling money -- preventing the attacks that negotiation creates surface area for.
- **Product 10 (Multi-Agent Commerce Cookbook)**: Orchestrating agent teams with CrewAI, LangGraph, and AutoGen -- the frameworks that deploy negotiating agents in production.

### Summary: Negotiation Decision Tree

When your agent enters a negotiation, it should follow this sequence:

1. **Calculate BATNA** from marketplace data. Know your walk-away price before the first offer.
2. **Verify counterparty** identity and trust score. Adjust pricing and escrow requirements accordingly.
3. **Move first** if possible. The first-proposal advantage is real and measurable.
4. **Use Boulware concession** (beta >= 3) as the default. Concede slowly. Let the counterparty make most of the movement.
5. **Never reveal your deadline.** Internal deadlines drive your concession curve. External communication should signal patience.
6. **Monitor for manipulation.** Extreme anchors, exploding offers, and stalling are detectable. Have countermeasures ready.
7. **Log everything.** Post-mortem analysis of negotiation logs is how strategies improve over time.
8. **Close with escrow.** Every negotiated agreement should be enforced with escrow appropriate to the counterparty's trust level.

The agents that follow this sequence will systematically capture more surplus than agents that accept fixed prices or negotiate without strategy. The game theory is settled. The code is in this guide. The remaining variable is whether you deploy it.

---

## Appendix: GreenHelix API Reference for Negotiation

All tools are called via the REST API (`POST /v1/{tool}`) with the body `{"tool": "tool_name", "input": {...}}`. Authentication uses `Bearer <api_key>` in the `Authorization` header.

| Tool | Purpose in Negotiation |
|---|---|
| `search_services` | BATNA calculation -- find alternative providers |
| `best_match` | Identify strongest competitor |
| `register_service` | Update listing with dynamic prices |
| `estimate_cost` | Baseline cost for reservation price |
| `get_volume_discount` | Volume pricing for coalition formation |
| `send_message` | Transmit offers and counter-offers |
| `negotiate_price` | Structured price negotiation with round tracking |
| `create_escrow` | Lock funds for standard deals |
| `create_performance_escrow` | Lock funds with quality gates for low-trust counterparties |
| `get_agent_reputation` | Trust score for risk-adjusted pricing |
| `get_agent_leaderboard` | Market position for premium pricing justification |
| `get_agent_identity` | Counterparty profile data |
| `verify_agent` | Cryptographic identity verification |

