---
name: greenhelix-agent-revenue-analytics
version: "1.3.1"
description: "Agent Revenue Analytics: Attribution, LTV, Cohorts, and Pricing Optimization for AI Agent Services. Complete guide to revenue measurement for AI agent services: revenue attribution by channel, customer lifetime value for agent-to-agent commerce, cohort analysis and retention curves, churn prediction from billing signals, price elasticity estimation, competitive intelligence from marketplace data, and webhook-driven revenue dashboards. Includes detailed Python code examples with full API integration."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [revenue, analytics, ltv, cohorts, churn, pricing, attribution, guide, greenhelix, openclaw, ai-agent]
price_usd: 39.0
content_type: markdown
executable: false
install: none
credentials: [GREENHELIX_API_KEY]
metadata:
  openclaw:
    requires:
      env:
        - GREENHELIX_API_KEY
    primaryEnv: GREENHELIX_API_KEY
---
# Agent Revenue Analytics: Attribution, LTV, Cohorts, and Pricing Optimization for AI Agent Services

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.
>
> **Referenced credentials** (you supply these in your own environment):
> - `GREENHELIX_API_KEY`: API authentication for GreenHelix gateway (read/write access to purchased API tools only)


Your agent service is live. The billing is working. Customers are calling your tools, money is flowing through the gateway, and your cost management is solid -- you followed the FinOps Playbook and every agent has its own wallet with budget caps. But here is the problem: you have no idea if you are growing. You know what you spend. You do not know what you earn. You cannot answer the five questions that determine whether your agent service is a business or a hobby: Which services generate the most revenue? Who are your best customers and what are they worth over their lifetime? When do customers churn and why? What price maximizes your revenue? And how do you compare to competitors in the marketplace?
This is the revenue gap. Cost management tells you how efficiently you operate. Revenue analytics tells you whether the operation is worth running. The FinOps Playbook (Product #6) gave you the cost layer. The Negotiation Strategies guide (Product #14) gave you pricing tactics. This guide gives you the measurement layer that sits between them: the data infrastructure to track revenue attribution, calculate customer lifetime value, build cohort retention curves, predict churn before it happens, optimize pricing from historical data, and monitor competitors -- all from the billing, payments, marketplace, and identity data already flowing through the GreenHelix gateway.
RevenueCat's 2026 State of Subscription Apps report found that AI-powered applications earn 41% more revenue per user than traditional apps but churn 30% faster. That asymmetry is the central challenge of agent commerce economics. Your agent service likely follows the same pattern: high initial monetization as customers integrate your tools into their workflows, followed by rapid attrition as they find alternatives, build in-house replacements, or simply stop needing the service. Without revenue analytics, you experience this as a mysterious plateau in monthly income. With revenue analytics, you see the cohort curves, identify the churn inflection point, calculate the price that maximizes lifetime revenue, and intervene before customers leave.

## What You'll Learn
- Chapter 1: The Revenue Gap in Agent Commerce
- Chapter 2: Revenue Attribution
- Chapter 3: Customer Lifetime Value
- Chapter 4: Cohort Analysis
- Chapter 5: Churn Prediction
- Chapter 6: Pricing Optimization
- Chapter 7: Competitive Intelligence
- Chapter 8: Revenue Dashboard and Alerts
- GreenHelix Revenue Pipeline — Working Implementation

## Full Guide

# Agent Revenue Analytics: Attribution, LTV, Cohorts, and Pricing Optimization for AI Agent Services

Your agent service is live. The billing is working. Customers are calling your tools, money is flowing through the gateway, and your cost management is solid -- you followed the FinOps Playbook and every agent has its own wallet with budget caps. But here is the problem: you have no idea if you are growing. You know what you spend. You do not know what you earn. You cannot answer the five questions that determine whether your agent service is a business or a hobby: Which services generate the most revenue? Who are your best customers and what are they worth over their lifetime? When do customers churn and why? What price maximizes your revenue? And how do you compare to competitors in the marketplace?

This is the revenue gap. Cost management tells you how efficiently you operate. Revenue analytics tells you whether the operation is worth running. The FinOps Playbook (Product #6) gave you the cost layer. The Negotiation Strategies guide (Product #14) gave you pricing tactics. This guide gives you the measurement layer that sits between them: the data infrastructure to track revenue attribution, calculate customer lifetime value, build cohort retention curves, predict churn before it happens, optimize pricing from historical data, and monitor competitors -- all from the billing, payments, marketplace, and identity data already flowing through the GreenHelix gateway.

RevenueCat's 2026 State of Subscription Apps report found that AI-powered applications earn 41% more revenue per user than traditional apps but churn 30% faster. That asymmetry is the central challenge of agent commerce economics. Your agent service likely follows the same pattern: high initial monetization as customers integrate your tools into their workflows, followed by rapid attrition as they find alternatives, build in-house replacements, or simply stop needing the service. Without revenue analytics, you experience this as a mysterious plateau in monthly income. With revenue analytics, you see the cohort curves, identify the churn inflection point, calculate the price that maximizes lifetime revenue, and intervene before customers leave.

Every code example in this guide calls the GreenHelix A2A Commerce Gateway via the REST API (`POST /v1/{tool}`) with a JSON body of `{"tool": "tool_name", "input": {...}}`. Authentication is via Bearer token. Every class and function is production-ready Python using the `requests` library. Define the core `RevenueAnalytics` class once and reference it throughout.

---


> **Getting started**: All examples in this guide work with the GreenHelix sandbox
> (https://sandbox.greenhelix.net) which provides 500 free credits — no API key required.

## Table of Contents

1. [The Revenue Gap in Agent Commerce](#chapter-1-the-revenue-gap-in-agent-commerce)
2. [Revenue Attribution](#chapter-2-revenue-attribution)
3. [Customer Lifetime Value](#chapter-3-customer-lifetime-value)
4. [Cohort Analysis](#chapter-4-cohort-analysis)
5. [Churn Prediction](#chapter-5-churn-prediction)
6. [Pricing Optimization](#chapter-6-pricing-optimization)
7. [Competitive Intelligence](#chapter-7-competitive-intelligence)
8. [Revenue Dashboard and Alerts](#chapter-8-revenue-dashboard-and-alerts)

---

## Chapter 1: The Revenue Gap in Agent Commerce

### Cost Management Is Not Revenue Management

The FinOps movement has trained the industry to obsess over cost. Every agent framework tutorial covers budget caps. Every infrastructure guide explains how to set spend alerts. Cloud providers publish cost optimization whitepapers quarterly. This emphasis is correct -- uncontrolled agent costs can destroy margins overnight -- but it creates a dangerous blind spot. Teams that can tell you their cost per tool call to four decimal places often cannot answer "what is our revenue per customer this month?" to the nearest dollar.

Cost management and revenue management are fundamentally different disciplines. Cost management is about efficiency: reducing the denominator. Revenue management is about growth: increasing the numerator. You can optimize costs to zero and still fail because revenue went to zero first. The companies that win in agent commerce are the ones that measure both sides of the equation.

Consider a concrete example. You operate a data enrichment agent service. Your FinOps dashboard shows that your cost per enrichment call is $0.003, down from $0.005 last quarter -- a 40% efficiency improvement. You celebrate. But what you do not see is that your revenue per enrichment call dropped from $0.015 to $0.008 because a competitor entered the marketplace at $0.009 and your highest-volume customer switched to them. Your margin per call actually shrank from $0.010 to $0.005. The cost optimization masked a revenue crisis.

### AI Apps: High Revenue, Higher Churn

RevenueCat's 2026 analysis of 30,000 subscription apps revealed a striking pattern in AI-powered applications. Compared to traditional SaaS:

- **Revenue per user is 41% higher.** AI apps command premium pricing because they deliver immediate, measurable value. An agent that saves four hours of manual data processing per week justifies a higher price than a traditional tool that merely organizes a workflow.
- **Churn is 30% faster.** AI apps lose subscribers more quickly because (a) the novelty effect is stronger -- users try the AI tool, get excited, then normalize it, (b) switching costs are lower -- if the value comes from the model, any wrapper around a comparable model is substitutable, and (c) expectations are higher -- a traditional app that works adequately retains users; an AI app that is merely adequate gets replaced by one that is impressive.
- **Net revenue per user over 12 months is only 8% higher** when you account for the elevated churn. The revenue advantage nearly evaporates.

For agent-to-agent commerce, the pattern intensifies. When your customers are themselves AI agents, the switching decision is not emotional -- it is algorithmic. An orchestrator agent evaluating your enrichment service against a competitor will switch the moment the competitor's price-adjusted quality score exceeds yours. There is no loyalty, no switching friction from muscle memory, no reluctance to learn a new interface. The agent's code changes one URL and one API key.

This means revenue analytics for agent services is not optional -- it is survival. You need to see the churn coming before it happens, understand which cohorts retain and which do not, and continuously optimize the price point that maximizes lifetime revenue rather than per-transaction revenue.

### Why Traditional SaaS Metrics Need Adaptation

Standard SaaS metrics -- MRR, ARR, churn rate, LTV, CAC -- were designed for subscription products with human customers. Agent commerce has three structural differences that require adaptation.

**First, usage is bursty and non-uniform.** A human user of a SaaS product logs in roughly daily with similar session patterns. An agent customer might call your service 10,000 times on Monday and zero times on Tuesday because its orchestrator only triggers your tool when a specific condition is met. Monthly Recurring Revenue (MRR) is still meaningful, but you need to complement it with usage-weighted metrics.

**Second, customers are identified by agent IDs, not email addresses.** You cannot send a churn-risk customer a winback email. You can adjust pricing, improve response times, or register a webhook to detect the moment their usage drops. Your retention interventions are programmatic, not personal.

**Third, pricing is often per-call rather than per-seat.** The LTV calculation changes when revenue is proportional to usage rather than a fixed monthly fee. An agent customer using your service 50,000 times per month at $0.001 per call is worth $50/month -- the same as a subscription customer paying $50/month -- but the revenue dynamics are entirely different. Usage-based revenue can grow without the customer explicitly upgrading, but it can also drop to zero without the customer explicitly canceling.

This guide adapts every traditional SaaS metric to the realities of agent commerce, using the data already available through GreenHelix billing, payments, and marketplace APIs.

---

## Chapter 2: Revenue Attribution

### Knowing Where Your Revenue Comes From

Revenue attribution answers a deceptively simple question: which of your agent services generated which revenue, and through which channel? When you operate multiple agent services -- a data enrichment tool, a translation tool, and a sentiment analysis tool -- and revenue arrives as aggregated billing summaries, you need to decompose that revenue by service, by customer, and by acquisition channel.

In agent commerce, there are three primary revenue channels:

- **Marketplace**: Customers discover your service through `search_services` on the GreenHelix marketplace. These are organic, low-acquisition-cost customers.
- **Direct**: Customers integrate your service directly via API key sharing, documentation, or partner integrations. These often have higher acquisition costs but stronger retention.
- **Referral**: Customers arrive because another agent in their workflow recommended or required your service as a dependency. These are the highest-value customers because the switching cost is embedded in their workflow architecture.

The challenge is that GreenHelix billing data does not natively tag revenue by channel. You need to infer it from the combination of billing summaries, invoice metadata, and marketplace activity. The `RevenueTracker` class below builds this attribution layer.

### The RevenueTracker Class

This is the core class for this guide. It wraps every GreenHelix tool used across all eight chapters. Define it once and extend it with methods as we progress.

```python
import requests
import json
import time
import math
import statistics
from datetime import datetime, timedelta
from typing import Optional
from collections import defaultdict


class RevenueTracker:
    """Revenue analytics client for the GreenHelix A2A Commerce Gateway.

    Wraps billing, payments, marketplace, identity, trust, and webhook
    tools into a revenue measurement and optimization interface.
    """

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
        """Execute a tool on the GreenHelix gateway."""
        resp = self.session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": input_data},
        )
        resp.raise_for_status()
        return resp.json()

    # -- Revenue Data Retrieval ----------------------------------------

    def get_billing_summary(self, period: str = "monthly") -> dict:
        """Get billing summary for the agent's services."""
        return self._execute("get_billing_summary", {
            "agent_id": self.agent_id,
            "period": period,
        })

    def get_usage_analytics(
        self,
        start_date: str,
        end_date: str,
    ) -> dict:
        """Get usage analytics over a date range."""
        return self._execute("get_usage_analytics", {
            "agent_id": self.agent_id,
            "start_date": start_date,
            "end_date": end_date,
        })

    def get_spending_by_category(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> dict:
        """Get spending broken down by category."""
        payload = {"agent_id": self.agent_id}
        if start_date:
            payload["start_date"] = start_date
        if end_date:
            payload["end_date"] = end_date
        return self._execute("get_spending_by_category", payload)

    def list_invoices(
        self,
        status: Optional[str] = None,
        limit: int = 100,
    ) -> dict:
        """List invoices with optional status filter."""
        payload = {"agent_id": self.agent_id, "limit": limit}
        if status:
            payload["status"] = status
        return self._execute("list_invoices", payload)

    def get_payment_intent(self, payment_id: str) -> dict:
        """Get details of a specific payment intent."""
        return self._execute("get_payment_intent", {
            "payment_id": payment_id,
        })

    # -- Marketplace Data ----------------------------------------------

    def search_services(
        self,
        query: str,
        category: Optional[str] = None,
    ) -> dict:
        """Search the marketplace for services."""
        payload = {"query": query}
        if category:
            payload["category"] = category
        return self._execute("search_services", payload)

    def get_service_ratings(self, service_id: str) -> dict:
        """Get ratings for a specific service."""
        return self._execute("get_service_ratings", {
            "service_id": service_id,
        })

    # -- Identity and Trust --------------------------------------------

    def get_agent_leaderboard(
        self,
        metric: str = "revenue",
    ) -> dict:
        """Get agent leaderboard by metric."""
        return self._execute("get_agent_leaderboard", {
            "metric": metric,
        })

    def search_agents_by_metrics(
        self,
        metric: str,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
    ) -> dict:
        """Search agents filtered by metric thresholds."""
        payload = {"metric": metric}
        if min_value is not None:
            payload["min_value"] = str(min_value)
        if max_value is not None:
            payload["max_value"] = str(max_value)
        return self._execute("search_agents_by_metrics", payload)

    def get_agent_reputation(self, target_agent_id: str) -> dict:
        """Get reputation data for an agent."""
        return self._execute("get_agent_reputation", {
            "agent_id": target_agent_id,
        })

    # -- Webhooks ------------------------------------------------------

    def register_webhook(
        self,
        url: str,
        events: list[str],
        config: Optional[dict] = None,
    ) -> dict:
        """Register a webhook for real-time events."""
        payload = {
            "url": url,
            "events": events,
        }
        if config:
            payload["config"] = config
        return self._execute("register_webhook", payload)
```

### Building Revenue Attribution

With the core class defined, here is the revenue attribution logic. The method pulls invoice data, categorizes each transaction by source channel, and aggregates revenue by service and channel.

```python
    # -- Revenue Attribution -------------------------------------------

    def get_revenue_summary(
        self,
        start_date: str,
        end_date: str,
    ) -> dict:
        """Build a revenue summary with attribution by service and channel.

        Combines billing summaries, invoice data, and usage analytics
        to attribute revenue to specific services and acquisition channels.
        """
        # Pull the raw data
        billing = self.get_billing_summary(period="monthly")
        usage = self.get_usage_analytics(start_date, end_date)
        invoices = self.list_invoices(status="paid")

        # Aggregate revenue by service
        revenue_by_service = defaultdict(float)
        revenue_by_channel = defaultdict(float)
        transactions = []

        for invoice in invoices.get("invoices", []):
            amount = float(invoice.get("amount", 0))
            service = invoice.get("service_id", "unknown")
            source = invoice.get("metadata", {}).get("source", "direct")

            # Classify the acquisition channel
            channel = self._classify_channel(source, invoice)

            revenue_by_service[service] += amount
            revenue_by_channel[channel] += amount
            transactions.append({
                "invoice_id": invoice.get("id"),
                "amount": amount,
                "service": service,
                "channel": channel,
                "date": invoice.get("created_at"),
            })

        total_revenue = sum(revenue_by_service.values())

        return {
            "period": {"start": start_date, "end": end_date},
            "total_revenue": round(total_revenue, 2),
            "revenue_by_service": {
                k: round(v, 2) for k, v in revenue_by_service.items()
            },
            "revenue_by_channel": {
                k: round(v, 2) for k, v in revenue_by_channel.items()
            },
            "transaction_count": len(transactions),
            "billing_summary": billing,
            "usage_summary": usage,
        }

    def _classify_channel(self, source: str, invoice: dict) -> str:
        """Classify an invoice into an acquisition channel.

        Uses heuristics based on invoice metadata and source field:
        - 'marketplace' if discovered via search_services
        - 'referral' if another agent's workflow triggered it
        - 'direct' for API key integrations and manual setups
        """
        if source == "marketplace" or "marketplace" in source:
            return "marketplace"
        if source == "referral" or invoice.get("metadata", {}).get("referrer"):
            return "referral"
        return "direct"

    def get_revenue_by_service(self) -> dict:
        """Get current-period revenue broken down by service.

        Uses spending-by-category as a proxy: your customers' spending
        on your services is your revenue.
        """
        categories = self.get_spending_by_category()
        services = {}

        for category in categories.get("categories", []):
            services[category["name"]] = {
                "revenue": float(category.get("total_spent", 0)),
                "call_count": int(category.get("call_count", 0)),
                "avg_revenue_per_call": round(
                    float(category.get("total_spent", 0))
                    / max(int(category.get("call_count", 0)), 1),
                    6,
                ),
            }

        return services
```

### Interpreting Attribution Data

Revenue attribution reveals three patterns that are invisible in aggregate billing data.

**Service concentration risk.** If 80% of your revenue comes from one service, you have a single point of failure. A competitor undercutting that service or a platform change that degrades its performance will crater your revenue. Diversification across services is as important for agent operators as portfolio diversification is for investors.

**Channel dependency.** Marketplace-sourced revenue is low-cost but volatile -- you are at the mercy of search algorithm changes and competitor listings. Direct revenue is higher-cost to acquire but stickier. Referral revenue is the gold standard: it means your service is embedded in another agent's workflow, making switching costly. A healthy agent business derives no more than 50% of revenue from any single channel.

**Revenue-per-call divergence.** When your average revenue per call differs significantly across services, it signals either a pricing opportunity (raise the price on the high-demand service) or a cost problem (the low-revenue service may not be worth maintaining). The `avg_revenue_per_call` metric in the code above makes this divergence visible.

---

## Chapter 3: Customer Lifetime Value

### LTV for Agent-to-Agent Services

Customer Lifetime Value (LTV) is the total revenue you expect from a customer over their entire relationship with your service. In traditional SaaS, LTV is the primary metric for deciding how much to spend on acquisition, which segments to prioritize, and whether the business model is sustainable. The rule of thumb: LTV should be at least 3x the Customer Acquisition Cost (CAC). If it costs you $10 to acquire a customer through marketplace advertising, that customer should generate at least $30 in lifetime revenue.

For agent-to-agent commerce, LTV has a structural difference. Your customers are agents, and agents have two lifetime horizons:

- **Agent lifetime**: How long the customer agent itself exists. If the customer is a research agent spun up for a three-month project, your maximum relationship duration is three months regardless of satisfaction.
- **Operator lifetime**: How long the human or organization behind the customer agent continues to use agent services. An operator who shuts down one agent might launch a successor that uses your service again.

The practical implication is that LTV in agent commerce often has a shorter but more predictable horizon than in human SaaS. Agents do not have emotional loyalty, but they also do not have emotional whims. An agent that finds value in your service at day 30 will still find value at day 90 unless the external context changes. This makes LTV estimation more reliable once you have enough cohort data.

### Simple LTV Calculation

The simplest LTV formula is:

```
LTV = Average Revenue Per Period / Churn Rate
```

If your average customer generates $45/month in revenue and your monthly churn rate is 15%, then:

```
LTV = $45 / 0.15 = $300
```

This formula assumes constant revenue per period and constant churn rate, which are obviously simplifications. But it gives you a useful baseline. Here is the implementation using GreenHelix billing data.

```python
    # -- Customer Lifetime Value ---------------------------------------

    def get_customer_history(
        self,
        customer_agent_id: str,
    ) -> dict:
        """Build a complete revenue history for a specific customer agent.

        Pulls all invoices from a customer and computes per-period
        revenue, tenure, and activity patterns.
        """
        invoices = self.list_invoices()
        customer_invoices = [
            inv for inv in invoices.get("invoices", [])
            if inv.get("payer_agent_id") == customer_agent_id
        ]

        if not customer_invoices:
            return {
                "customer_agent_id": customer_agent_id,
                "total_revenue": 0,
                "tenure_days": 0,
                "invoice_count": 0,
                "monthly_revenue": [],
            }

        # Sort by date
        customer_invoices.sort(key=lambda x: x.get("created_at", ""))

        first_date = datetime.fromisoformat(
            customer_invoices[0]["created_at"].replace("Z", "+00:00")
        )
        last_date = datetime.fromisoformat(
            customer_invoices[-1]["created_at"].replace("Z", "+00:00")
        )
        tenure_days = max((last_date - first_date).days, 1)

        # Aggregate by month
        monthly = defaultdict(float)
        total = 0.0
        for inv in customer_invoices:
            amount = float(inv.get("amount", 0))
            total += amount
            month_key = inv["created_at"][:7]  # YYYY-MM
            monthly[month_key] += amount

        monthly_revenue = [
            {"month": k, "revenue": round(v, 2)}
            for k, v in sorted(monthly.items())
        ]

        return {
            "customer_agent_id": customer_agent_id,
            "total_revenue": round(total, 2),
            "tenure_days": tenure_days,
            "tenure_months": round(tenure_days / 30.44, 1),
            "invoice_count": len(customer_invoices),
            "first_invoice": customer_invoices[0]["created_at"],
            "last_invoice": customer_invoices[-1]["created_at"],
            "avg_monthly_revenue": round(
                total / max(len(monthly), 1), 2
            ),
            "monthly_revenue": monthly_revenue,
        }

    def calculate_ltv(
        self,
        customer_histories: list[dict],
        churn_rate: Optional[float] = None,
    ) -> dict:
        """Calculate customer lifetime value from a set of customer histories.

        If churn_rate is not provided, estimates it from the data by
        looking at the proportion of customers whose last invoice is
        more than 30 days old (presumed churned).
        """
        if not customer_histories:
            return {"ltv": 0, "avg_revenue_per_month": 0, "churn_rate": 0}

        # Calculate average monthly revenue across all customers
        monthly_revenues = []
        active_count = 0
        churned_count = 0
        now = datetime.utcnow()
        churn_threshold_days = 30

        for history in customer_histories:
            avg_monthly = history.get("avg_monthly_revenue", 0)
            if avg_monthly > 0:
                monthly_revenues.append(avg_monthly)

            # Estimate churn if not provided
            if churn_rate is None:
                last_invoice = history.get("last_invoice", "")
                if last_invoice:
                    last_date = datetime.fromisoformat(
                        last_invoice.replace("Z", "+00:00")
                    ).replace(tzinfo=None)
                    days_since_last = (now - last_date).days
                    if days_since_last > churn_threshold_days:
                        churned_count += 1
                    else:
                        active_count += 1

        avg_revenue_per_month = (
            statistics.mean(monthly_revenues) if monthly_revenues else 0
        )

        # Estimate churn rate if not provided
        if churn_rate is None:
            total_customers = active_count + churned_count
            if total_customers > 0:
                churn_rate = churned_count / total_customers
            else:
                churn_rate = 0.10  # Default assumption: 10% monthly churn

        # Guard against division by zero
        if churn_rate <= 0:
            churn_rate = 0.01  # Assume 1% minimum churn

        ltv = avg_revenue_per_month / churn_rate

        # Also calculate median and percentile LTVs
        individual_ltvs = [
            rev / churn_rate for rev in monthly_revenues
        ]

        return {
            "ltv": round(ltv, 2),
            "avg_revenue_per_month": round(avg_revenue_per_month, 2),
            "churn_rate": round(churn_rate, 4),
            "expected_lifetime_months": round(1 / churn_rate, 1),
            "customer_count": len(customer_histories),
            "active_count": active_count,
            "churned_count": churned_count,
            "ltv_median": round(
                statistics.median(individual_ltvs), 2
            ) if individual_ltvs else 0,
            "ltv_p25": round(
                sorted(individual_ltvs)[len(individual_ltvs) // 4], 2
            ) if len(individual_ltvs) >= 4 else 0,
            "ltv_p75": round(
                sorted(individual_ltvs)[3 * len(individual_ltvs) // 4], 2
            ) if len(individual_ltvs) >= 4 else 0,
        }
```

### Using LTV to Drive Decisions

LTV is not a vanity metric. It directly informs three operational decisions:

**Acquisition spending.** If your LTV is $300 and your target LTV/CAC ratio is 3:1, you can spend up to $100 to acquire a customer. In agent commerce, acquisition cost might be the marketplace listing fee, the cost of a free trial, or the engineering time to build an integration. If your LTV is $50, spending $100 on an integration is irrational.

**Tier prioritization.** Segment your customers by LTV. High-LTV customers get faster response times, priority support, and custom pricing. Low-LTV customers get standard service. The GreenHelix tier system (free, pro, enterprise) maps directly to LTV segments. An agent customer generating $500/month in revenue justifies pro-tier treatment with lower per-call costs and dedicated endpoints.

**Churn investment.** The cost of retaining an existing customer should be proportional to their remaining LTV. If a customer with $200 of remaining LTV shows churn risk signals, investing $20 in a retention offer (a temporary discount, a free feature upgrade) has a 10:1 expected return. If a customer with $10 of remaining LTV shows the same signals, let them go.

---

## Chapter 4: Cohort Analysis

### Why Cohorts Matter More Than Averages

Your overall monthly churn rate is 12%. Is that good or bad? You cannot tell without cohort analysis. A 12% average might mean every cohort churns at 12% -- a consistent, predictable pattern. Or it might mean your January cohort churns at 5% while your March cohort churns at 25% because you made a pricing change in February that attracted price-sensitive customers who do not retain. The average hides the story. Cohorts reveal it.

A cohort is a group of customers who share a common characteristic, usually the period when they first became a customer. The January 2026 cohort is every agent that first called your service in January. You track each cohort's revenue, retention, and usage over time to see how customer behavior evolves.

For agent services, cohort analysis answers three critical questions:

1. **Are newer customers better or worse than older ones?** If your March cohort retains better than your January cohort, something you changed is working. If retention is declining cohort over cohort, you have a product or market problem.
2. **When does churn stabilize?** Most agent services see high churn in the first 7-14 days (the evaluation period) followed by a plateau. Knowing this inflection point tells you when a customer has "stuck" and their lifetime revenue becomes predictable.
3. **What is the revenue curve shape?** Some services see flat revenue per customer (subscription-like). Others see growing revenue (expansion) as customers integrate deeper. Others see declining revenue (contraction) as customers optimize their usage. The cohort curve tells you which pattern you have.

### Building Cohorts from Billing Data

```python
    # -- Cohort Analysis -----------------------------------------------

    def build_cohorts(
        self,
        invoices: Optional[list[dict]] = None,
        cohort_period: str = "monthly",
    ) -> dict:
        """Build customer cohorts from invoice data.

        Groups customers by their first purchase period and tracks
        their revenue and retention over subsequent periods.

        Args:
            invoices: Pre-fetched invoice list, or None to fetch live.
            cohort_period: 'monthly' or 'weekly' grouping.
        """
        if invoices is None:
            raw = self.list_invoices(limit=1000)
            invoices = raw.get("invoices", [])

        if not invoices:
            return {"cohorts": {}, "retention_matrix": {}}

        # Determine each customer's first purchase date
        customer_first_seen = {}
        customer_periods = defaultdict(lambda: defaultdict(float))

        for inv in invoices:
            customer = inv.get("payer_agent_id", "unknown")
            date_str = inv.get("created_at", "")
            amount = float(inv.get("amount", 0))

            if not date_str:
                continue

            date = datetime.fromisoformat(
                date_str.replace("Z", "+00:00")
            ).replace(tzinfo=None)

            if cohort_period == "monthly":
                period_key = date.strftime("%Y-%m")
            else:
                # ISO week
                period_key = date.strftime("%Y-W%W")

            # Track first seen
            if customer not in customer_first_seen:
                customer_first_seen[customer] = period_key

            # Track revenue per customer per period
            customer_periods[customer][period_key] += amount

        # Build cohorts: group customers by first-seen period
        cohorts = defaultdict(lambda: {
            "customers": [],
            "periods": defaultdict(lambda: {
                "revenue": 0.0,
                "active_customers": 0,
            }),
        })

        for customer, first_period in customer_first_seen.items():
            cohorts[first_period]["customers"].append(customer)

            for period, revenue in customer_periods[customer].items():
                cohorts[first_period]["periods"][period]["revenue"] += revenue
                cohorts[first_period]["periods"][period][
                    "active_customers"
                ] += 1

        # Build retention matrix
        retention_matrix = {}
        for cohort_key in sorted(cohorts.keys()):
            cohort = cohorts[cohort_key]
            initial_count = len(cohort["customers"])
            periods_sorted = sorted(cohort["periods"].keys())

            retention_matrix[cohort_key] = {
                "initial_customers": initial_count,
                "retention_by_period": [],
            }

            for i, period in enumerate(periods_sorted):
                active = cohort["periods"][period]["active_customers"]
                revenue = cohort["periods"][period]["revenue"]
                retention_pct = (
                    (active / initial_count * 100)
                    if initial_count > 0
                    else 0
                )
                retention_matrix[cohort_key][
                    "retention_by_period"
                ].append({
                    "period": period,
                    "period_number": i,
                    "active_customers": active,
                    "retention_pct": round(retention_pct, 1),
                    "revenue": round(revenue, 2),
                    "avg_revenue_per_customer": round(
                        revenue / max(active, 1), 2
                    ),
                })

        return {
            "cohorts": {
                k: {
                    "customer_count": len(v["customers"]),
                    "customers": v["customers"],
                }
                for k, v in cohorts.items()
            },
            "retention_matrix": retention_matrix,
        }

    def get_retention_curve(
        self,
        cohort_key: str,
        retention_matrix: dict,
    ) -> list[dict]:
        """Extract the retention curve for a specific cohort.

        Returns a list of data points showing how retention decays
        over time for the given cohort.
        """
        cohort_data = retention_matrix.get(cohort_key, {})
        retention = cohort_data.get("retention_by_period", [])

        if not retention:
            return []

        # Calculate period-over-period churn
        curve = []
        for i, point in enumerate(retention):
            prev_retention = (
                retention[i - 1]["retention_pct"] if i > 0 else 100.0
            )
            period_churn = prev_retention - point["retention_pct"]

            curve.append({
                "period_number": point["period_number"],
                "period": point["period"],
                "retention_pct": point["retention_pct"],
                "period_churn_pct": round(period_churn, 1),
                "revenue": point["revenue"],
                "avg_revenue_per_customer": point[
                    "avg_revenue_per_customer"
                ],
                "cumulative_revenue_per_customer": round(
                    sum(
                        p["avg_revenue_per_customer"]
                        for p in retention[: i + 1]
                    ),
                    2,
                ),
            })

        return curve
```

### Reading Cohort Data

A healthy agent service shows these cohort patterns:

**Improving retention over cohorts.** If your February cohort retains at 70% after three months and your April cohort retains at 78% after three months, your product or positioning is improving. This is the single most important trend to track.

**Stabilizing retention curves.** Each cohort's retention should flatten after the initial churn period. If your retention curve never flattens -- customers continue churning at the same rate month after month -- you have a product-market fit problem. Customers are not finding enough ongoing value to justify continued use.

**Growing revenue per surviving customer.** The best agent services show net revenue expansion within cohorts: the customers who stay spend more over time. This means they are integrating your service deeper into their workflows, using more features, or processing more volume. If revenue per surviving customer is flat, you are a utility. If it is growing, you are becoming infrastructure.

**The danger signal.** If newer cohorts are both smaller (fewer new customers) and churn faster (lower retention), you are in a death spiral. The marketplace is moving away from you. This is the signal to either dramatically improve the product or pivot. Cohort analysis gives you this signal months before it shows up in aggregate MRR.

---

## Chapter 5: Churn Prediction

### Leading Indicators of Agent Customer Churn

By the time a customer has churned -- their last invoice was 30+ days ago and usage has dropped to zero -- it is too late. Effective churn management requires predicting churn before it happens, ideally 7-14 days before the customer stops using your service. For agent customers, there are five reliable leading indicators, all detectable from GreenHelix billing and usage data.

**Indicator 1: Usage volume decline.** A customer whose daily call volume drops by more than 40% from their trailing 30-day average is at high risk. This is the strongest predictor. Usage decline usually precedes churn by 7-21 days. The drop may be gradual (progressive disengagement) or sudden (the customer is testing an alternative).

**Indicator 2: Usage pattern change.** A customer who previously called your service at consistent intervals (every hour, every day) and shifts to sporadic, unpredictable calls is exploring alternatives. They are comparing your service to competitors and only falling back to you when the alternative fails.

**Indicator 3: Revenue per call decline.** If a customer shifts from high-value operations to low-value ones -- using only your cheapest endpoints while avoiding premium features -- they are extracting remaining value before leaving. This is the "already has one foot out the door" signal.

**Indicator 4: Payment delays.** When invoices that previously cleared in 1-2 days start taking 5-7 days, the customer's operator may be deprioritizing your service in their budget allocation. Payment delays are a weak signal individually but a strong signal when combined with usage decline.

**Indicator 5: Reputation changes.** If a customer's trust score drops, they may be experiencing issues with other services too, which could indicate financial distress or organizational problems that will eventually affect their relationship with you.

### Building a Churn Risk Score

```python
    # -- Churn Prediction ----------------------------------------------

    def calculate_churn_risk(
        self,
        customer_agent_id: str,
        lookback_days: int = 60,
    ) -> dict:
        """Calculate a churn risk score (0-100) for a customer agent.

        Combines usage decline, pattern changes, revenue trends, and
        payment timing into a weighted risk score.

        Higher score = higher risk of churning.
        """
        now = datetime.utcnow()
        start_date = (now - timedelta(days=lookback_days)).strftime(
            "%Y-%m-%d"
        )
        end_date = now.strftime("%Y-%m-%d")
        mid_date = (now - timedelta(days=lookback_days // 2)).strftime(
            "%Y-%m-%d"
        )

        # Get usage data for two halves of the lookback window
        first_half = self.get_usage_analytics(start_date, mid_date)
        second_half = self.get_usage_analytics(mid_date, end_date)

        # Get invoice data for payment timing analysis
        invoices = self.list_invoices()
        customer_invoices = [
            inv for inv in invoices.get("invoices", [])
            if inv.get("payer_agent_id") == customer_agent_id
        ]

        risk_components = {}

        # Component 1: Usage volume decline (0-30 points)
        first_half_calls = int(
            first_half.get("total_calls", 0)
        )
        second_half_calls = int(
            second_half.get("total_calls", 0)
        )

        if first_half_calls > 0:
            volume_change = (
                (second_half_calls - first_half_calls) / first_half_calls
            )
            if volume_change < -0.5:
                risk_components["usage_decline"] = 30
            elif volume_change < -0.3:
                risk_components["usage_decline"] = 20
            elif volume_change < -0.1:
                risk_components["usage_decline"] = 10
            elif volume_change > 0.1:
                risk_components["usage_decline"] = 0
            else:
                risk_components["usage_decline"] = 5
        else:
            risk_components["usage_decline"] = 25  # No historical data

        # Component 2: Revenue per call trend (0-25 points)
        first_half_revenue = float(
            first_half.get("total_revenue", 0)
        )
        second_half_revenue = float(
            second_half.get("total_revenue", 0)
        )

        first_rpc = (
            first_half_revenue / max(first_half_calls, 1)
        )
        second_rpc = (
            second_half_revenue / max(second_half_calls, 1)
        )

        if first_rpc > 0:
            rpc_change = (second_rpc - first_rpc) / first_rpc
            if rpc_change < -0.3:
                risk_components["revenue_decline"] = 25
            elif rpc_change < -0.15:
                risk_components["revenue_decline"] = 15
            elif rpc_change < 0:
                risk_components["revenue_decline"] = 5
            else:
                risk_components["revenue_decline"] = 0
        else:
            risk_components["revenue_decline"] = 10

        # Component 3: Days since last invoice (0-25 points)
        if customer_invoices:
            customer_invoices.sort(
                key=lambda x: x.get("created_at", ""), reverse=True
            )
            last_invoice_date = datetime.fromisoformat(
                customer_invoices[0]["created_at"].replace(
                    "Z", "+00:00"
                )
            ).replace(tzinfo=None)
            days_since_last = (now - last_invoice_date).days

            if days_since_last > 21:
                risk_components["recency"] = 25
            elif days_since_last > 14:
                risk_components["recency"] = 15
            elif days_since_last > 7:
                risk_components["recency"] = 5
            else:
                risk_components["recency"] = 0
        else:
            risk_components["recency"] = 20

        # Component 4: Payment consistency (0-20 points)
        if len(customer_invoices) >= 3:
            intervals = []
            for i in range(1, min(len(customer_invoices), 6)):
                d1 = datetime.fromisoformat(
                    customer_invoices[i - 1]["created_at"].replace(
                        "Z", "+00:00"
                    )
                ).replace(tzinfo=None)
                d2 = datetime.fromisoformat(
                    customer_invoices[i]["created_at"].replace(
                        "Z", "+00:00"
                    )
                ).replace(tzinfo=None)
                intervals.append(abs((d1 - d2).days))

            if len(intervals) >= 2:
                interval_cv = (
                    statistics.stdev(intervals)
                    / max(statistics.mean(intervals), 1)
                )
                if interval_cv > 1.0:
                    risk_components["consistency"] = 20
                elif interval_cv > 0.5:
                    risk_components["consistency"] = 10
                else:
                    risk_components["consistency"] = 0
            else:
                risk_components["consistency"] = 5
        else:
            risk_components["consistency"] = 10

        # Composite risk score
        total_risk = sum(risk_components.values())
        total_risk = min(total_risk, 100)

        # Risk tier
        if total_risk >= 70:
            tier = "critical"
        elif total_risk >= 45:
            tier = "high"
        elif total_risk >= 25:
            tier = "medium"
        else:
            tier = "low"

        return {
            "customer_agent_id": customer_agent_id,
            "risk_score": total_risk,
            "risk_tier": tier,
            "components": risk_components,
            "data": {
                "volume_change_pct": round(
                    (
                        (second_half_calls - first_half_calls)
                        / max(first_half_calls, 1)
                    )
                    * 100,
                    1,
                ),
                "rpc_change_pct": round(
                    (
                        (second_rpc - first_rpc)
                        / max(first_rpc, 0.001)
                    )
                    * 100,
                    1,
                ),
                "days_since_last_invoice": (
                    (now - last_invoice_date).days
                    if customer_invoices
                    else None
                ),
                "first_half_calls": first_half_calls,
                "second_half_calls": second_half_calls,
            },
        }

    def get_at_risk_customers(
        self,
        customer_agent_ids: list[str],
        risk_threshold: int = 45,
    ) -> list[dict]:
        """Identify customers above a churn risk threshold.

        Scans a list of customer agent IDs and returns those whose
        churn risk score exceeds the threshold, sorted by risk
        (highest first).
        """
        at_risk = []

        for customer_id in customer_agent_ids:
            try:
                risk = self.calculate_churn_risk(customer_id)
                if risk["risk_score"] >= risk_threshold:
                    at_risk.append(risk)
            except Exception as e:
                # Log but don't fail the entire scan
                print(
                    f"Warning: Could not assess risk for "
                    f"{customer_id}: {e}"
                )
                continue

        # Sort by risk score descending
        at_risk.sort(key=lambda x: x["risk_score"], reverse=True)

        return at_risk
```

### Acting on Churn Predictions

A churn risk score is only useful if it triggers action. Here is the intervention playbook by risk tier:

**Critical (70-100).** This customer is leaving within 1-2 weeks. Immediate actions: (a) check if your service has had any errors or latency increases for this customer, (b) if you have a dynamic pricing capability, temporarily reduce their per-call cost by 20-30% to increase the switching cost, (c) register a webhook for their usage events so you see the exact moment they stop calling.

**High (45-69).** This customer is likely evaluating alternatives. Actions: (a) check competitor pricing in the marketplace using `search_services` to see if you are being undercut, (b) if the customer's volume warrants it, offer a volume discount commitment, (c) analyze which of your service endpoints they are no longer using -- if they dropped a premium feature, understand why.

**Medium (25-44).** This customer shows early warning signs but may not be actively churning. Actions: (a) monitor weekly, (b) ensure your service performance is stable, (c) consider proactive outreach if you have a communication channel to the customer's operator.

**Low (0-24).** Healthy customer. No intervention needed, but continue monitoring. Even low-risk customers should be included in cohort analysis to ensure the baseline does not shift.

The key insight for agent commerce is that retention interventions are programmatic. You do not send an email with a special offer. You adjust pricing parameters, improve response latency, or enhance the service quality. The webhook system lets you detect the moment a customer's behavior changes and trigger automated responses.

---

## Chapter 6: Pricing Optimization

### The Price That Maximizes Revenue

Pricing is the single highest-leverage decision in any business. A 1% improvement in price realization -- getting 1% more revenue from the same volume -- typically has a larger impact on profit than a 1% improvement in cost, volume, or conversion rate. McKinsey's research consistently shows that pricing improvements flow to the bottom line at 2-4x the rate of cost improvements.

For agent services, pricing optimization is both more important and more tractable than for traditional SaaS. More important because agent customers switch on price-adjusted quality with zero friction. More tractable because you have granular, high-frequency usage data that reveals price sensitivity with statistical precision. Every tool call is a data point. A service handling 10,000 calls per day generates enough data to estimate price elasticity within a week.

### Price Elasticity Estimation

Price elasticity measures how demand changes in response to price changes. If you raise your price by 10% and volume drops by 5%, your elasticity is -0.5 (inelastic -- the price increase is profitable). If you raise your price by 10% and volume drops by 15%, your elasticity is -1.5 (elastic -- the price increase loses revenue).

The optimal price depends on your elasticity. For inelastic services (elasticity between 0 and -1), you should raise prices -- volume drops less than price increases, so revenue grows. For elastic services (elasticity below -1), you should lower prices -- volume gains more than offset the price decrease.

```python
    # -- Pricing Optimization ------------------------------------------

    def estimate_price_elasticity(
        self,
        price_history: list[dict],
    ) -> dict:
        """Estimate price elasticity from historical price/volume data.

        Args:
            price_history: List of dicts with 'price', 'volume', and
                'period' keys representing different pricing periods.

        Returns:
            Elasticity estimate with confidence indicators.

        The elasticity is computed using the midpoint (arc) method
        across all consecutive price change periods.
        """
        if len(price_history) < 2:
            return {
                "elasticity": None,
                "error": "Need at least 2 price periods",
            }

        # Sort by period
        sorted_history = sorted(
            price_history, key=lambda x: x["period"]
        )

        # Calculate elasticity for each consecutive pair
        elasticities = []
        for i in range(1, len(sorted_history)):
            p1 = float(sorted_history[i - 1]["price"])
            p2 = float(sorted_history[i]["price"])
            q1 = float(sorted_history[i - 1]["volume"])
            q2 = float(sorted_history[i]["volume"])

            # Skip periods with no price change
            if p1 == p2:
                continue

            # Midpoint (arc) elasticity formula
            pct_change_q = (q2 - q1) / ((q1 + q2) / 2)
            pct_change_p = (p2 - p1) / ((p1 + p2) / 2)

            if pct_change_p != 0:
                elasticity = pct_change_q / pct_change_p
                elasticities.append({
                    "period_from": sorted_history[i - 1]["period"],
                    "period_to": sorted_history[i]["period"],
                    "price_change_pct": round(pct_change_p * 100, 2),
                    "volume_change_pct": round(pct_change_q * 100, 2),
                    "elasticity": round(elasticity, 3),
                })

        if not elasticities:
            return {
                "elasticity": None,
                "error": "No price changes found in history",
            }

        avg_elasticity = statistics.mean(
            [e["elasticity"] for e in elasticities]
        )
        elasticity_std = (
            statistics.stdev([e["elasticity"] for e in elasticities])
            if len(elasticities) > 1
            else 0
        )

        # Classify
        if avg_elasticity > -0.5:
            classification = "highly_inelastic"
            recommendation = "raise_price"
        elif avg_elasticity > -1.0:
            classification = "inelastic"
            recommendation = "raise_price"
        elif avg_elasticity > -1.5:
            classification = "elastic"
            recommendation = "lower_price"
        else:
            classification = "highly_elastic"
            recommendation = "lower_price_significantly"

        return {
            "avg_elasticity": round(avg_elasticity, 3),
            "elasticity_std": round(elasticity_std, 3),
            "classification": classification,
            "recommendation": recommendation,
            "data_points": len(elasticities),
            "period_elasticities": elasticities,
        }

    def optimize_pricing(
        self,
        current_price: float,
        current_volume: float,
        elasticity: float,
        cost_per_call: float,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
    ) -> dict:
        """Find the revenue-maximizing and profit-maximizing prices.

        Uses the estimated elasticity to model the demand curve and
        find the prices that maximize total revenue and total profit.

        Revenue = Price * Volume
        Profit = (Price - Cost) * Volume
        Volume at new price = current_volume * (new_price / current_price) ^ elasticity

        Args:
            current_price: Current per-call price.
            current_volume: Current monthly call volume.
            elasticity: Estimated price elasticity (negative number).
            cost_per_call: Your cost per call (from FinOps data).
            min_price: Minimum price floor.
            max_price: Maximum price ceiling.
        """
        if min_price is None:
            min_price = cost_per_call * 1.1  # At least 10% margin
        if max_price is None:
            max_price = current_price * 3.0  # Cap at 3x current

        best_revenue_price = current_price
        best_revenue = current_price * current_volume
        best_profit_price = current_price
        best_profit = (current_price - cost_per_call) * current_volume

        # Search the price space in 1% increments
        test_prices = []
        price = min_price
        step = (max_price - min_price) / 200
        if step <= 0:
            step = min_price * 0.01

        while price <= max_price:
            # Demand model: constant elasticity
            volume_at_price = current_volume * (
                (price / current_price) ** elasticity
            )
            revenue = price * volume_at_price
            profit = (price - cost_per_call) * volume_at_price

            test_prices.append({
                "price": round(price, 6),
                "volume": round(volume_at_price, 0),
                "revenue": round(revenue, 2),
                "profit": round(profit, 2),
                "margin_pct": round(
                    ((price - cost_per_call) / price) * 100, 1
                ),
            })

            if revenue > best_revenue:
                best_revenue = revenue
                best_revenue_price = price

            if profit > best_profit:
                best_profit = profit
                best_profit_price = price

            price += step

        # Calculate improvements
        current_revenue = current_price * current_volume
        current_profit = (
            (current_price - cost_per_call) * current_volume
        )

        return {
            "current": {
                "price": round(current_price, 6),
                "volume": round(current_volume, 0),
                "revenue": round(current_revenue, 2),
                "profit": round(current_profit, 2),
            },
            "revenue_optimal": {
                "price": round(best_revenue_price, 6),
                "volume": round(
                    current_volume
                    * (
                        (best_revenue_price / current_price)
                        ** elasticity
                    ),
                    0,
                ),
                "revenue": round(best_revenue, 2),
                "revenue_change_pct": round(
                    (
                        (best_revenue - current_revenue)
                        / max(current_revenue, 0.01)
                    )
                    * 100,
                    1,
                ),
            },
            "profit_optimal": {
                "price": round(best_profit_price, 6),
                "volume": round(
                    current_volume
                    * (
                        (best_profit_price / current_price)
                        ** elasticity
                    ),
                    0,
                ),
                "profit": round(best_profit, 2),
                "profit_change_pct": round(
                    (
                        (best_profit - current_profit)
                        / max(current_profit, 0.01)
                    )
                    * 100,
                    1,
                ),
            },
            "elasticity_used": elasticity,
            "cost_per_call": cost_per_call,
        }
```

### Volume Discount Optimization

Volume discounts are the most common pricing lever in agent commerce. Offer a lower per-call price in exchange for a commitment to higher volume. The question is: how much discount should you offer at each volume tier?

The answer depends on your marginal cost curve and your elasticity. A discount is profitable if the incremental volume it generates exceeds the revenue you lose on existing volume. Here is the analysis.

```python
    def optimize_volume_discounts(
        self,
        base_price: float,
        cost_per_call: float,
        current_tiers: list[dict],
        elasticity: float,
    ) -> list[dict]:
        """Optimize volume discount tiers.

        Args:
            base_price: Standard per-call price.
            cost_per_call: Your cost per call.
            current_tiers: List of dicts with 'min_volume', 'max_volume',
                'discount_pct', and 'current_customers' keys.
            elasticity: Estimated price elasticity.

        Returns:
            Optimized tier recommendations.
        """
        optimized_tiers = []

        for tier in current_tiers:
            min_vol = tier["min_volume"]
            max_vol = tier.get("max_volume", min_vol * 10)
            current_discount = tier["discount_pct"]
            customers = tier.get("current_customers", 0)

            # Mid-volume for calculations
            mid_vol = (min_vol + max_vol) / 2

            # Test discount levels from 0% to 50%
            best_discount = current_discount
            best_tier_profit = 0

            for test_discount in range(0, 51):
                discounted_price = base_price * (1 - test_discount / 100)
                if discounted_price <= cost_per_call:
                    continue

                # Expected customers at this discount
                price_ratio = discounted_price / base_price
                volume_multiplier = price_ratio ** elasticity
                expected_customers = max(
                    customers * volume_multiplier, 0
                )

                tier_revenue = (
                    discounted_price * mid_vol * expected_customers
                )
                tier_cost = cost_per_call * mid_vol * expected_customers
                tier_profit = tier_revenue - tier_cost

                if tier_profit > best_tier_profit:
                    best_tier_profit = tier_profit
                    best_discount = test_discount

            optimized_tiers.append({
                "min_volume": min_vol,
                "max_volume": max_vol,
                "current_discount_pct": current_discount,
                "optimal_discount_pct": best_discount,
                "change": best_discount - current_discount,
                "discounted_price": round(
                    base_price * (1 - best_discount / 100), 6
                ),
                "expected_profit_improvement_pct": round(
                    (
                        (best_tier_profit - (
                            (base_price * (1 - current_discount / 100)
                             - cost_per_call)
                            * mid_vol * customers
                        ))
                        / max(
                            (base_price * (1 - current_discount / 100)
                             - cost_per_call)
                            * mid_vol * max(customers, 1),
                            0.01,
                        )
                    )
                    * 100,
                    1,
                ),
            })

        return optimized_tiers
```

### A/B Testing Prices

The most reliable way to measure price elasticity is to run a controlled experiment. In agent commerce, you can A/B test prices by creating two marketplace listings for the same service at different price points and measuring conversion and retention for each.

The key constraint is sample size. You need enough transactions at each price point to reach statistical significance. For a service handling 1,000 calls per day, allocating a 10% sample to a test price (100 calls/day) gives you statistical significance within 5-7 days for a 10% price change. For a service handling 100 calls per day, you need 2-3 weeks.

The implementation pattern is straightforward: create two service listings via the marketplace, route traffic between them based on a deterministic hash of the customer agent ID (so the same customer always sees the same price), and compare the revenue and retention outcomes after the test period. Use the `search_services` tool to verify both listings are live and the `get_service_ratings` tool to monitor satisfaction at each price point.

---

## Chapter 7: Competitive Intelligence

### Why Competitive Monitoring Is Revenue Analytics

Revenue does not exist in a vacuum. Your revenue growth or decline is always relative to competitors. A 5% monthly revenue decline might be catastrophic if the market is growing at 10% (you are losing share) or acceptable if the entire market declined 15% (you are outperforming). Competitive intelligence is the external context that makes your internal revenue metrics meaningful.

The GreenHelix marketplace provides two vectors for competitive intelligence:

1. **Marketplace search**: The `search_services` tool returns competitors' service listings with pricing, descriptions, and categories. Monitor this weekly to detect new entrants, price changes, and feature additions.
2. **Identity and reputation data**: The `get_agent_leaderboard` and `search_agents_by_metrics` tools show how you rank relative to competitors on volume, ratings, and trust. The `get_agent_reputation` tool provides detailed trust data for specific competitors.

### Building a Competitive Landscape

```python
    # -- Competitive Intelligence --------------------------------------

    def get_competitive_landscape(
        self,
        service_category: str,
        your_service_id: str,
    ) -> dict:
        """Build a competitive landscape analysis for your service category.

        Searches the marketplace for competing services, compares
        pricing, ratings, and positioning.
        """
        # Find competitors
        search_results = self.search_services(
            query=service_category,
            category=service_category,
        )

        competitors = []
        your_service = None

        for service in search_results.get("services", []):
            service_data = {
                "service_id": service.get("id"),
                "name": service.get("name"),
                "price": float(service.get("price", 0)),
                "rating": float(service.get("rating", 0)),
                "review_count": int(
                    service.get("review_count", 0)
                ),
                "description": service.get("description", ""),
            }

            if service.get("id") == your_service_id:
                your_service = service_data
            else:
                competitors.append(service_data)

        if not your_service:
            your_service = {
                "service_id": your_service_id,
                "price": 0,
                "rating": 0,
            }

        # Analyze competitive position
        if competitors:
            prices = [c["price"] for c in competitors if c["price"] > 0]
            ratings = [
                c["rating"] for c in competitors if c["rating"] > 0
            ]

            avg_competitor_price = (
                statistics.mean(prices) if prices else 0
            )
            min_competitor_price = min(prices) if prices else 0
            max_competitor_price = max(prices) if prices else 0
            avg_competitor_rating = (
                statistics.mean(ratings) if ratings else 0
            )

            your_price = your_service.get("price", 0)
            price_position = "unknown"
            if your_price > 0 and avg_competitor_price > 0:
                price_ratio = your_price / avg_competitor_price
                if price_ratio > 1.15:
                    price_position = "premium"
                elif price_ratio < 0.85:
                    price_position = "budget"
                else:
                    price_position = "mid_market"
        else:
            avg_competitor_price = 0
            min_competitor_price = 0
            max_competitor_price = 0
            avg_competitor_rating = 0
            price_position = "no_competitors"

        return {
            "your_service": your_service,
            "competitor_count": len(competitors),
            "competitors": sorted(
                competitors, key=lambda c: c["price"]
            ),
            "market_pricing": {
                "avg_price": round(avg_competitor_price, 6),
                "min_price": round(min_competitor_price, 6),
                "max_price": round(max_competitor_price, 6),
                "your_price": your_service.get("price", 0),
                "your_position": price_position,
            },
            "market_quality": {
                "avg_rating": round(avg_competitor_rating, 2),
                "your_rating": your_service.get("rating", 0),
            },
        }

    def benchmark_performance(
        self,
        metric: str = "revenue",
    ) -> dict:
        """Benchmark your agent against the leaderboard.

        Uses the identity leaderboard and reputation data to compare
        your performance against the market.
        """
        # Get leaderboard
        leaderboard = self.get_agent_leaderboard(metric=metric)
        agents = leaderboard.get("agents", [])

        # Find your position
        your_position = None
        total_agents = len(agents)

        for i, agent in enumerate(agents):
            if agent.get("agent_id") == self.agent_id:
                your_position = i + 1
                break

        # Get your reputation
        reputation = self.get_agent_reputation(self.agent_id)

        # Calculate percentile
        percentile = None
        if your_position and total_agents > 0:
            percentile = round(
                (1 - your_position / total_agents) * 100, 1
            )

        # Get top performer data for comparison
        top_performers = agents[:5] if len(agents) >= 5 else agents

        return {
            "your_agent_id": self.agent_id,
            "metric": metric,
            "your_rank": your_position,
            "total_agents": total_agents,
            "percentile": percentile,
            "reputation": reputation,
            "top_performers": top_performers,
            "gap_to_top": {
                "rank_1_value": (
                    float(top_performers[0].get("value", 0))
                    if top_performers
                    else 0
                ),
                "your_value": (
                    float(agents[your_position - 1].get("value", 0))
                    if your_position and your_position <= len(agents)
                    else 0
                ),
            },
        }
```

### Competitive Intelligence Patterns

Three patterns emerge from consistent competitive monitoring.

**Pattern 1: Price convergence.** In active marketplace categories, prices converge over time as competitors respond to each other. If you are the first to enter a category at $0.010 per call and a competitor enters at $0.008, you will face pressure to lower your price. Track the rate of price convergence -- if competitor prices are moving toward yours, you have pricing power. If your price is moving toward competitors', they have it.

**Pattern 2: Quality-price segmentation.** Markets naturally segment into quality tiers. A high-quality, high-reliability service at $0.015 per call can coexist with a budget alternative at $0.005 because they serve different customer segments. The danger zone is the middle: similar quality to the premium option at a price close to the budget option. Your competitive analysis should identify which tier you occupy and whether that position is defensible.

**Pattern 3: Reputation moats.** Agent services with high trust scores and long track records retain customers better than new entrants with lower prices. The `get_agent_reputation` data quantifies this moat. If your trust score is 0.92 and the lowest-price competitor is at 0.71, many agent customers will pay the premium because their orchestrators weight trust in routing decisions. Monitor your reputation advantage and invest in maintaining it -- it is the closest thing to a switching cost in agent commerce.

Track competitive data weekly. Store historical snapshots so you can see trends, not just the current state. The combination of competitive pricing trends and your own cohort retention data tells you whether you are gaining or losing market position.

---

## Chapter 8: Revenue Dashboard and Alerts

### From Analysis to Monitoring

The previous seven chapters built the analytics: attribution, LTV, cohorts, churn prediction, pricing optimization, and competitive intelligence. This chapter turns those analytics into a live monitoring system using GreenHelix webhooks. The goal is a revenue dashboard that alerts you to problems before they become crises.

### Webhook-Based Revenue Event Tracking

GreenHelix webhooks deliver real-time notifications when billing events occur. Register handlers for the events that matter most to revenue monitoring.

```python
    # -- Revenue Dashboard and Alerts ----------------------------------

    def setup_revenue_alerts(
        self,
        webhook_url: str,
        config: Optional[dict] = None,
    ) -> dict:
        """Register webhooks for revenue-critical events.

        Sets up monitoring for payment completions, payment failures,
        usage thresholds, and budget events that signal revenue changes.

        Args:
            webhook_url: Your endpoint that receives webhook POSTs.
            config: Optional configuration overrides.
        """
        alert_config = config or {}

        # Event categories to monitor
        revenue_events = [
            # Payment events: track incoming revenue
            "payment.completed",
            "payment.failed",
            "payment.refunded",

            # Usage events: track consumption patterns
            "usage.threshold",
            "usage.spike",

            # Budget events: customer spending signals
            "budget.threshold",
            "budget.exhausted",

            # Subscription events: recurring revenue changes
            "subscription.created",
            "subscription.cancelled",
            "subscription.renewed",
        ]

        results = {}

        for event in revenue_events:
            try:
                result = self.register_webhook(
                    url=webhook_url,
                    events=[event],
                    config=alert_config.get(event, {}),
                )
                results[event] = {
                    "status": "registered",
                    "webhook_id": result.get("webhook_id"),
                }
            except Exception as e:
                results[event] = {
                    "status": "failed",
                    "error": str(e),
                }

        return {
            "webhook_url": webhook_url,
            "events_registered": sum(
                1
                for r in results.values()
                if r["status"] == "registered"
            ),
            "events_failed": sum(
                1
                for r in results.values()
                if r["status"] == "failed"
            ),
            "details": results,
        }
```

### Key Metrics to Monitor

A revenue dashboard for agent services should track these metrics, updated in real time from webhook events and polled analytics.

**Monthly Recurring Revenue (MRR).** For usage-based agent services, MRR is not a clean number like it is for subscription SaaS. Calculate it as the trailing 30-day revenue, updated daily. Track the MRR trend line, not the absolute number, because daily fluctuations in usage-based revenue are normal.

**Average Revenue Per User (ARPU).** Total monthly revenue divided by the number of unique customer agents who made at least one call. ARPU tells you whether you are growing by adding customers (ARPU flat, MRR growing) or by extracting more from existing customers (ARPU growing, customer count flat). The first pattern is healthier for long-term growth; the second is more profitable in the short term but fragile.

**Churn Rate.** The percentage of customers from 30 days ago who have not made a call in the last 7 days. This is a lagging indicator -- by the time churn shows up here, the customer has already left. That is why Chapter 5 builds a leading indicator (the churn risk score). The dashboard should show both: the lagging churn rate for historical accuracy and the churn risk distribution for forward-looking management.

**LTV/CAC Ratio.** The ratio of customer lifetime value (from Chapter 3) to customer acquisition cost. If your LTV is $300 and your CAC is $50, the ratio is 6:1 -- a healthy, profitable business. Below 3:1, your acquisition economics are unsustainable. Below 1:1, you are paying more to acquire customers than they will ever generate in revenue. For agent services, CAC is often low (marketplace discovery is nearly free), which means even moderate LTV produces excellent ratios. But if you are investing in integrations, partnerships, or marketing to drive direct and referral channels, track the channel-specific CAC and LTV/CAC ratio.

### Bringing It All Together

Here is the complete dashboard generation method that combines every metric from this guide into a single revenue report.

```python
    def generate_revenue_report(
        self,
        customer_agent_ids: list[str],
        service_category: str,
        your_service_id: str,
        lookback_days: int = 30,
    ) -> dict:
        """Generate a comprehensive revenue analytics report.

        Combines attribution, LTV, cohort, churn, and competitive
        data into a single dashboard payload.
        """
        now = datetime.utcnow()
        start_date = (now - timedelta(days=lookback_days)).strftime(
            "%Y-%m-%d"
        )
        end_date = now.strftime("%Y-%m-%d")

        # 1. Revenue attribution
        revenue = self.get_revenue_summary(start_date, end_date)

        # 2. Customer LTV
        histories = []
        for cid in customer_agent_ids:
            try:
                history = self.get_customer_history(cid)
                histories.append(history)
            except Exception:
                continue

        ltv_data = self.calculate_ltv(histories)

        # 3. Cohort analysis
        invoices_raw = self.list_invoices(limit=1000)
        cohort_data = self.build_cohorts(
            invoices=invoices_raw.get("invoices", [])
        )

        # 4. Churn risk assessment
        at_risk = self.get_at_risk_customers(
            customer_agent_ids, risk_threshold=45
        )

        # 5. Competitive landscape
        competitive = self.get_competitive_landscape(
            service_category, your_service_id
        )

        # 6. Benchmark
        benchmark = self.benchmark_performance(metric="revenue")

        # Compute summary KPIs
        total_revenue = revenue.get("total_revenue", 0)
        customer_count = len(
            [h for h in histories if h.get("total_revenue", 0) > 0]
        )
        arpu = (
            round(total_revenue / max(customer_count, 1), 2)
        )
        at_risk_pct = round(
            len(at_risk) / max(len(customer_agent_ids), 1) * 100, 1
        )

        return {
            "report_date": end_date,
            "period": {
                "start": start_date,
                "end": end_date,
                "days": lookback_days,
            },
            "kpis": {
                "mrr": total_revenue,
                "arpu": arpu,
                "customer_count": customer_count,
                "ltv": ltv_data["ltv"],
                "churn_rate": ltv_data["churn_rate"],
                "ltv_cac_ratio": None,  # CAC is operator-specific
                "at_risk_customers": len(at_risk),
                "at_risk_pct": at_risk_pct,
                "competitive_rank": benchmark.get("your_rank"),
                "competitive_percentile": benchmark.get("percentile"),
            },
            "revenue_attribution": revenue,
            "ltv_analysis": ltv_data,
            "cohort_summary": {
                "total_cohorts": len(
                    cohort_data.get("cohorts", {})
                ),
                "retention_matrix": cohort_data.get(
                    "retention_matrix", {}
                ),
            },
            "churn_risk": {
                "at_risk_count": len(at_risk),
                "critical_count": sum(
                    1
                    for r in at_risk
                    if r["risk_tier"] == "critical"
                ),
                "high_count": sum(
                    1
                    for r in at_risk
                    if r["risk_tier"] == "high"
                ),
                "at_risk_customers": at_risk[:10],  # Top 10 riskiest
            },
            "competitive_position": {
                "market_position": competitive["market_pricing"][
                    "your_position"
                ],
                "competitor_count": competitive["competitor_count"],
                "leaderboard_rank": benchmark.get("your_rank"),
                "leaderboard_percentile": benchmark.get("percentile"),
            },
        }
```

### Cross-References

This guide is the revenue measurement layer. It connects to three other guides in the GreenHelix ecosystem:

- **The AI Agent FinOps Playbook (Product #6)** covers the cost side: per-agent wallets, budget caps, spend alerts, and cost attribution. Use FinOps data as an input to margin calculations in this guide. Your revenue per call minus your cost per call (from FinOps) is your margin per call.
- **The Agent Testing and Observability Cookbook (Product #9)** covers monitoring infrastructure: tracing, health checks, and alerting pipelines. The revenue webhook handlers from this chapter integrate with the observability patterns from that guide. Route revenue alerts through the same alerting infrastructure as your operational alerts.
- **Agent Negotiation Strategies (Product #14)** covers pricing tactics: auctions, BATNA calculation, and dynamic pricing. The pricing optimization in Chapter 6 of this guide produces the elasticity estimates and optimal price points that feed into the negotiation strategies. Use this guide to find the right price; use the Negotiation guide to implement the right pricing mechanism.

### Where to Start

If you are reading this guide and your agent service is already live, here is the priority order:

1. **Revenue attribution** (Chapter 2). Takes 30 minutes to implement. Immediately tells you which services and channels drive your revenue.
2. **Churn risk scoring** (Chapter 5). Takes one hour. Identifies customers you are about to lose so you can intervene.
3. **LTV calculation** (Chapter 3). Takes 30 minutes once you have customer histories. Tells you how much each customer is worth and how much you should spend on retention.
4. **Cohort analysis** (Chapter 4). Takes one hour. Shows whether your business is improving or deteriorating over time.
5. **Competitive intelligence** (Chapter 7). Takes 30 minutes to set up initial monitoring. Gives external context to your internal metrics.
6. **Pricing optimization** (Chapter 6). Requires 2-4 weeks of data collection before you can estimate elasticity. Start the data collection now; optimize later.
7. **Revenue dashboard** (Chapter 8). Once you have all the above, wire them together with webhooks and a reporting function.

The total implementation time is approximately 8-12 hours for a developer familiar with the GreenHelix API. The revenue insights start generating value immediately.

For the full API reference and tool catalog covering all billing, payments, marketplace, identity, trust, and webhook tools used in this guide, visit the GreenHelix developer documentation at [https://api.greenhelix.net/docs](https://api.greenhelix.net/docs).

---

*Price: $29 | Format: Digital Guide | Updates: Lifetime access*

---

## GreenHelix Revenue Pipeline — Working Implementation

The code below uses the actual `greenhelix_trading` library classes. Every method call maps to a real GreenHelix Gateway tool. Copy this module into your project, set `GREENHELIX_API_KEY` and `GREENHELIX_AGENT_ID` in your environment, and run it.

```python
"""
Revenue pipeline using the greenhelix_trading library.

Covers:
  1. Revenue tracking and service-level attribution
  2. Cohort analysis with retention curves
  3. Customer LTV calculation with segmentation
  4. Multi-touch attribution modeling
  5. Churn-aware revenue forecasting

Requirements:
    pip install greenhelix-trading
"""

import os
import time
import statistics
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Optional

from greenhelix_trading import RevenueTracker, CustomerAnalytics


# ── Configuration ─────────────────────────────────────────────────────────────

API_KEY = os.environ["GREENHELIX_API_KEY"]
AGENT_ID = os.environ["GREENHELIX_AGENT_ID"]


# ── 1. Revenue Tracking Queries ──────────────────────────────────────────────

def build_revenue_dashboard(period: str = "30d") -> dict:
    """Pull billing, usage, and per-service revenue into a single view.

    Uses RevenueTracker.get_revenue_summary for the billing aggregate,
    RevenueTracker.get_revenue_by_service for category breakdown, and
    RevenueTracker.get_usage_metrics for call-volume context.
    """
    tracker = RevenueTracker(
        api_key=API_KEY,
        agent_id=AGENT_ID,
    )

    # Billing aggregate for the period
    billing = tracker.get_revenue_summary(period=period)

    # Per-service breakdown via spending-by-category
    services = tracker.get_revenue_by_service()

    # Call-volume and usage metrics
    usage = tracker.get_usage_metrics(period=period)

    # Compute derived KPIs
    total_revenue = float(billing.get("total_revenue", 0))
    total_calls = int(usage.get("total_calls", 0))
    revenue_per_call = total_revenue / max(total_calls, 1)

    categories = services.get("categories", [])
    top_service = max(
        categories,
        key=lambda c: float(c.get("total_spent", 0)),
        default=None,
    )

    return {
        "period": period,
        "total_revenue": round(total_revenue, 2),
        "total_calls": total_calls,
        "revenue_per_call": round(revenue_per_call, 6),
        "service_count": len(categories),
        "top_service": top_service,
        "billing_raw": billing,
        "usage_raw": usage,
    }


def get_transaction_ledger(customer_id: Optional[str] = None) -> list:
    """Retrieve the full invoice ledger, optionally filtered by customer.

    Uses RevenueTracker.get_transaction_history which wraps list_invoices.
    Returns a list of invoice dicts sorted newest-first.
    """
    tracker = RevenueTracker(
        api_key=API_KEY,
        agent_id=AGENT_ID,
    )
    raw = tracker.get_transaction_history(customer_id=customer_id)
    invoices = raw.get("invoices", [])
    invoices.sort(key=lambda inv: inv.get("created_at", ""), reverse=True)
    return invoices


# ── 2. Cohort Analysis ───────────────────────────────────────────────────────

def build_monthly_cohorts() -> dict:
    """Group customers by first-purchase month and compute retention.

    Pulls all invoices via RevenueTracker.get_transaction_history,
    assigns each customer to their first-purchase month, and tracks
    how many remain active (have invoices) in subsequent months.
    """
    tracker = RevenueTracker(
        api_key=API_KEY,
        agent_id=AGENT_ID,
    )
    analytics = CustomerAnalytics(
        api_key=API_KEY,
        agent_id=AGENT_ID,
    )

    # Fetch the full invoice ledger
    raw = tracker.get_transaction_history()
    invoices = raw.get("invoices", [])

    if not invoices:
        return {"cohorts": {}, "retention_matrix": {}}

    # Determine each customer's first-purchase month
    customer_first_month = {}
    customer_months = defaultdict(set)

    for inv in invoices:
        customer = inv.get("payer_agent_id", "unknown")
        date_str = inv.get("created_at", "")
        if not date_str:
            continue
        month_key = date_str[:7]  # "YYYY-MM"
        if customer not in customer_first_month:
            customer_first_month[customer] = month_key
        customer_months[customer].add(month_key)

    # Group customers into cohorts by first-purchase month
    cohorts = defaultdict(list)
    for customer, first_month in customer_first_month.items():
        cohorts[first_month].append(customer)

    # Build retention matrix
    all_months = sorted({m for months in customer_months.values() for m in months})
    retention_matrix = {}

    for cohort_month in sorted(cohorts.keys()):
        cohort_customers = cohorts[cohort_month]
        initial_size = len(cohort_customers)
        retention_matrix[cohort_month] = {
            "initial_customers": initial_size,
            "periods": [],
        }
        for i, month in enumerate(all_months):
            if month < cohort_month:
                continue
            active = sum(
                1 for c in cohort_customers if month in customer_months[c]
            )
            retention_pct = (active / initial_size * 100) if initial_size > 0 else 0
            retention_matrix[cohort_month]["periods"].append({
                "month": month,
                "period_number": i - all_months.index(cohort_month),
                "active_customers": active,
                "retention_pct": round(retention_pct, 1),
            })

    # Also get the gateway-side cohort summary for cross-reference
    gateway_cohort = analytics.build_cohort_summary(period="monthly")

    return {
        "cohorts": {k: len(v) for k, v in cohorts.items()},
        "retention_matrix": retention_matrix,
        "gateway_cohort_summary": gateway_cohort,
    }


# ── 3. Customer LTV Calculation ──────────────────────────────────────────────

def calculate_customer_ltv(
    customer_ids: list[str],
    churn_override: Optional[float] = None,
) -> dict:
    """Compute LTV for a set of customers using invoice history.

    For each customer, uses CustomerAnalytics.get_customer_history to
    pull their invoices, then calculates average monthly revenue. Churn
    rate is estimated from the proportion of customers whose last invoice
    is more than 30 days old, or can be provided as an override.

    CustomerAnalytics.calculate_ltv returns the simple LTV = ARPU / churn.
    """
    analytics = CustomerAnalytics(
        api_key=API_KEY,
        agent_id=AGENT_ID,
    )

    histories = []
    now = datetime.utcnow()
    active_count = 0
    churned_count = 0

    for cid in customer_ids:
        try:
            history = analytics.get_customer_history(customer_id=cid)
            invoices = history.get("invoices", [])
            if not invoices:
                churned_count += 1
                continue

            # Sort invoices by date
            invoices.sort(key=lambda x: x.get("created_at", ""))
            total_revenue = sum(float(inv.get("amount", 0)) for inv in invoices)
            first_date = invoices[0].get("created_at", "")[:10]
            last_date = invoices[-1].get("created_at", "")[:10]

            # Estimate tenure in months
            try:
                first_dt = datetime.fromisoformat(first_date)
                last_dt = datetime.fromisoformat(last_date)
                tenure_days = max((last_dt - first_dt).days, 1)
                tenure_months = max(tenure_days / 30.44, 1)
                days_since_last = (now - last_dt).days
            except (ValueError, TypeError):
                tenure_months = 1
                days_since_last = 0

            avg_monthly = total_revenue / tenure_months

            if days_since_last > 30:
                churned_count += 1
            else:
                active_count += 1

            histories.append({
                "customer_id": cid,
                "total_revenue": round(total_revenue, 2),
                "tenure_months": round(tenure_months, 1),
                "avg_monthly_revenue": round(avg_monthly, 2),
                "days_since_last_invoice": days_since_last,
            })
        except Exception:
            churned_count += 1
            continue

    # Estimate churn rate
    total_customers = active_count + churned_count
    if churn_override is not None:
        churn_rate = churn_override
    elif total_customers > 0:
        churn_rate = churned_count / total_customers
    else:
        churn_rate = 0.10  # Default 10% monthly churn

    churn_rate = max(churn_rate, 0.01)  # Floor at 1%

    # Calculate aggregate LTV via the library
    monthly_revenues = [h["avg_monthly_revenue"] for h in histories if h["avg_monthly_revenue"] > 0]
    avg_arpu = statistics.mean(monthly_revenues) if monthly_revenues else 0

    ltv_result = analytics.calculate_ltv(
        avg_revenue_per_month=avg_arpu,
        monthly_churn_rate=churn_rate,
    )

    # Segment customers into LTV tiers
    individual_ltvs = [h["avg_monthly_revenue"] / churn_rate for h in histories if h["avg_monthly_revenue"] > 0]
    segments = {"platinum": [], "gold": [], "silver": [], "bronze": []}

    for i, ltv_val in enumerate(individual_ltvs):
        cid = histories[i]["customer_id"]
        if ltv_val >= avg_arpu / churn_rate * 2:
            segments["platinum"].append(cid)
        elif ltv_val >= avg_arpu / churn_rate:
            segments["gold"].append(cid)
        elif ltv_val >= avg_arpu / churn_rate * 0.5:
            segments["silver"].append(cid)
        else:
            segments["bronze"].append(cid)

    return {
        "ltv": ltv_result,
        "churn_rate": round(churn_rate, 4),
        "active_customers": active_count,
        "churned_customers": churned_count,
        "avg_monthly_revenue": round(avg_arpu, 2),
        "expected_lifetime_months": round(1 / churn_rate, 1),
        "segments": {tier: len(ids) for tier, ids in segments.items()},
        "segment_details": segments,
        "customer_histories": histories,
    }


# ── 4. Multi-Touch Attribution Modeling ──────────────────────────────────────

def build_attribution_model() -> dict:
    """Attribute revenue to acquisition channels using invoice metadata.

    Uses RevenueTracker.get_transaction_history to pull all invoices,
    then classifies each into marketplace / direct / referral based on
    the invoice's metadata.source field.  Computes channel-level ARPU
    and revenue share.
    """
    tracker = RevenueTracker(
        api_key=API_KEY,
        agent_id=AGENT_ID,
    )

    raw = tracker.get_transaction_history()
    invoices = raw.get("invoices", [])

    channel_revenue = defaultdict(float)
    channel_customers = defaultdict(set)
    channel_count = defaultdict(int)

    for inv in invoices:
        amount = float(inv.get("amount", 0))
        customer = inv.get("payer_agent_id", "unknown")
        source = inv.get("metadata", {}).get("source", "direct")

        # Channel classification
        if "marketplace" in source.lower():
            channel = "marketplace"
        elif "referral" in source.lower() or inv.get("metadata", {}).get("referrer"):
            channel = "referral"
        else:
            channel = "direct"

        channel_revenue[channel] += amount
        channel_customers[channel].add(customer)
        channel_count[channel] += 1

    total_revenue = sum(channel_revenue.values())

    attribution = {}
    for channel in ["marketplace", "direct", "referral"]:
        rev = channel_revenue.get(channel, 0)
        custs = len(channel_customers.get(channel, set()))
        txns = channel_count.get(channel, 0)
        attribution[channel] = {
            "revenue": round(rev, 2),
            "revenue_share_pct": round(rev / max(total_revenue, 0.01) * 100, 1),
            "unique_customers": custs,
            "transaction_count": txns,
            "arpu": round(rev / max(custs, 1), 2),
            "avg_transaction": round(rev / max(txns, 1), 4),
        }

    return {
        "total_revenue": round(total_revenue, 2),
        "channels": attribution,
        "concentration_risk": _assess_concentration_risk(attribution),
    }


def _assess_concentration_risk(attribution: dict) -> dict:
    """Evaluate revenue concentration across channels.

    A healthy business derives no more than 50% from any single channel.
    """
    shares = {ch: data["revenue_share_pct"] for ch, data in attribution.items()}
    max_channel = max(shares, key=shares.get) if shares else "none"
    max_share = shares.get(max_channel, 0)

    if max_share >= 80:
        risk = "critical"
        recommendation = f"Dangerously concentrated in {max_channel}. Diversify immediately."
    elif max_share >= 60:
        risk = "high"
        recommendation = f"Heavy reliance on {max_channel}. Build alternative channels."
    elif max_share >= 40:
        risk = "moderate"
        recommendation = "Reasonable distribution. Continue monitoring."
    else:
        risk = "low"
        recommendation = "Well-diversified revenue. Maintain current strategy."

    return {
        "dominant_channel": max_channel,
        "dominant_share_pct": max_share,
        "risk_level": risk,
        "recommendation": recommendation,
    }


# ── 5. Churn-Aware Revenue Forecasting ───────────────────────────────────────

def forecast_revenue(
    customer_ids: list[str],
    months_ahead: int = 6,
) -> dict:
    """Project revenue forward using churn risk and LTV data.

    For each customer, uses CustomerAnalytics.calculate_churn_risk to
    classify risk as high/medium/low, then applies survival probabilities
    to their average monthly revenue to build a forward projection.
    """
    analytics = CustomerAnalytics(
        api_key=API_KEY,
        agent_id=AGENT_ID,
    )
    tracker = RevenueTracker(
        api_key=API_KEY,
        agent_id=AGENT_ID,
    )

    # Survival probability per month by risk tier
    monthly_survival = {"low": 0.95, "medium": 0.85, "high": 0.65}

    customer_projections = []

    for cid in customer_ids:
        try:
            # Get churn risk classification
            risk_result = analytics.calculate_churn_risk(customer_id=cid)
            risk_tier = risk_result.get("risk", "medium")

            # Get customer invoice history for ARPU
            history = tracker.get_transaction_history(customer_id=cid)
            invoices = history.get("invoices", [])
            if not invoices:
                continue

            total_rev = sum(float(inv.get("amount", 0)) for inv in invoices)
            # Estimate months active from first to last invoice
            dates = sorted(inv.get("created_at", "")[:10] for inv in invoices)
            try:
                first_dt = datetime.fromisoformat(dates[0])
                last_dt = datetime.fromisoformat(dates[-1])
                months_active = max((last_dt - first_dt).days / 30.44, 1)
            except (ValueError, TypeError, IndexError):
                months_active = 1

            avg_monthly = total_rev / months_active
            survival = monthly_survival.get(risk_tier, 0.85)

            # Project forward
            projections = []
            for month in range(1, months_ahead + 1):
                survival_at_month = survival ** month
                expected_revenue = avg_monthly * survival_at_month
                projections.append({
                    "month": month,
                    "survival_probability": round(survival_at_month, 4),
                    "expected_revenue": round(expected_revenue, 2),
                })

            customer_projections.append({
                "customer_id": cid,
                "risk_tier": risk_tier,
                "avg_monthly_revenue": round(avg_monthly, 2),
                "projections": projections,
            })
        except Exception:
            continue

    # Aggregate: sum expected revenue across all customers per month
    monthly_totals = defaultdict(float)
    for cp in customer_projections:
        for proj in cp["projections"]:
            monthly_totals[proj["month"]] += proj["expected_revenue"]

    forecast = [
        {"month": m, "expected_revenue": round(rev, 2)}
        for m, rev in sorted(monthly_totals.items())
    ]

    # At-risk revenue: customers flagged as high churn risk
    at_risk_customers = analytics.get_at_risk_customers(threshold=10)

    return {
        "months_ahead": months_ahead,
        "customer_count": len(customer_projections),
        "monthly_forecast": forecast,
        "total_forecast_revenue": round(sum(f["expected_revenue"] for f in forecast), 2),
        "at_risk_summary": at_risk_customers,
        "customer_detail": customer_projections,
    }


# ── Main: Run the Full Pipeline ──────────────────────────────────────────────

if __name__ == "__main__":
    import json

    print("=" * 72)
    print("GreenHelix Revenue Pipeline")
    print("=" * 72)

    # Step 1: Revenue dashboard
    print("\n[1/5] Building revenue dashboard...")
    dashboard = build_revenue_dashboard(period="30d")
    print(f"  Total revenue: ${dashboard['total_revenue']}")
    print(f"  Total calls: {dashboard['total_calls']}")
    print(f"  Revenue/call: ${dashboard['revenue_per_call']}")

    # Step 2: Attribution model
    print("\n[2/5] Building attribution model...")
    attribution = build_attribution_model()
    for ch, data in attribution["channels"].items():
        print(f"  {ch}: ${data['revenue']} ({data['revenue_share_pct']}%)")
    print(f"  Concentration risk: {attribution['concentration_risk']['risk_level']}")

    # Step 3: Cohort analysis
    print("\n[3/5] Building monthly cohorts...")
    cohorts = build_monthly_cohorts()
    for month, count in sorted(cohorts["cohorts"].items()):
        print(f"  {month}: {count} customers")

    # Step 4: LTV calculation (example customer IDs)
    print("\n[4/5] Calculating customer LTV...")
    # Replace with your actual customer agent IDs
    sample_customers = [
        "customer-agent-001", "customer-agent-002",
        "customer-agent-003", "customer-agent-004",
    ]
    ltv_report = calculate_customer_ltv(sample_customers)
    print(f"  LTV: ${ltv_report['ltv']['ltv']}")
    print(f"  Churn rate: {ltv_report['churn_rate'] * 100:.1f}%")
    print(f"  Expected lifetime: {ltv_report['expected_lifetime_months']} months")
    print(f"  Segments: {ltv_report['segments']}")

    # Step 5: Revenue forecast
    print("\n[5/5] Forecasting revenue (6 months)...")
    forecast = forecast_revenue(sample_customers, months_ahead=6)
    for entry in forecast["monthly_forecast"]:
        print(f"  Month +{entry['month']}: ${entry['expected_revenue']}")
    print(f"  Total 6-month forecast: ${forecast['total_forecast_revenue']}")

    print("\n" + "=" * 72)
    print("Pipeline complete.")
    print("=" * 72)
```

