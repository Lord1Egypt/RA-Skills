#!/usr/bin/env python3
"""
icp_modeler.py — Ideal Customer Profile modeling for mortgage and real estate professionals

For each product, generates:
  1. Full buyer persona (demographics, psychographics, pain points, triggers)
  2. Meta (Facebook/Instagram) ad targeting parameters
  3. Google Ads targeting parameters
  4. Content angle — what to say and how to say it
  5. Platform routing — where this ICP hangs out

Usage:
  python3 icp_modeler.py --product "crypto mortgage"
  python3 icp_modeler.py --product "credit repair" --output json
  python3 icp_modeler.py --product "VA loan" --generate-ad "30s video script"
  python3 icp_modeler.py --list                         # show all known products
  python3 icp_modeler.py --product "crypto mortgage" --generate-content "3 facebook posts"
  python3 icp_modeler.py --demo                         # run all profiles

LLM backend: uses generate.py (local MLX → Haiku fallback)
"""

import argparse
import json
import os
import sys

# ── Pre-built ICP library (no LLM needed for baseline profiles) ───────────────
# These are research-backed starting points, not generic personas.
# The LLM layer DEEPENS these — it doesn't replace them.

ICPS = {
    "crypto-mortgage": {
        "product": "Crypto-Backed Mortgage (Fannie Mae / Coinbase / Better)",
        "headline": "The Crypto Holder Who Won't Sell",
        "demographics": {
            "age": "30-48",
            "gender": "65% male, 35% female",
            "income": "$120K-$400K household",
            "location": "Target metro, tech corridors and growth submarkets",
            "occupation": "Software engineer, finance, entrepreneur, executive",
            "education": "College+ (often technical degree)",
            "home_status": "Renting or owns starter home, wants to upgrade",
        },
        "crypto_profile": {
            "holdings": "BTC, ETH, XRP, SOL — bought 2017-2021",
            "unrealized_gains": "$200K-$2M+",
            "behavior": "Hodler — hasn't sold through multiple cycles",
            "platforms": "Coinbase, Binance, Kraken, self-custody",
            "sentiment": "Believes crypto is long-term, doesn't want to convert to fiat",
        },
        "pain_points": [
            "Doesn't want to sell crypto and trigger $50K-$500K capital gains tax event",
            "Doesn't qualify for traditional mortgage because crypto income isn't W2",
            "Feels stuck — 'I have the wealth but can't access it for real estate'",
            "Worried crypto will keep appreciating while it's locked up",
            "Frustrated that banks don't 'get' crypto as an asset class",
        ],
        "dream_outcome": "Buy a home without selling a single coin. Keep the upside.",
        "trigger_phrases": [
            "don't sell your crypto to buy a house",
            "pledge crypto as collateral",
            "crypto-backed mortgage",
            "no capital gains event",
            "Fannie Mae crypto",
            "keep your BTC and buy a home",
        ],
        "objections": [
            "Is this legit? / Is Fannie Mae really doing this?",
            "What happens if crypto crashes — do I lose the house?",
            "What's the rate premium vs a regular mortgage?",
            "How much crypto do I need to pledge?",
        ],
        "content_tone": "Sophisticated, peer-to-peer, no hype — speaks to someone who already knows crypto",
        "where_they_are": ["X (crypto Twitter)", "Reddit r/Bitcoin r/ethfinance", "Telegram crypto groups", "LinkedIn (tech/finance)", "Coindesk", "The Block"],
        "meta_targeting": {
            "age_range": "28-50",
            "interests": ["Cryptocurrency", "Bitcoin", "Ethereum", "XRP", "DeFi", "Coinbase", "Personal finance", "Real estate investing"],
            "behaviors": ["Engaged shoppers", "Used cryptocurrency exchange app"],
            "income": "Top 25%",
            "custom_audiences": "Upload existing crypto lead list, create lookalike",
            "placement": "Facebook Feed, Instagram Feed, Instagram Stories",
            "exclude": ["people interested in day trading only", "crypto games/NFTs only"],
        },
        "google_targeting": {
            "keywords": [
                "crypto backed mortgage", "bitcoin mortgage", "buy house with crypto",
                "mortgage with cryptocurrency collateral", "fannie mae crypto loan",
                "crypto home loan no capital gains", "XRP mortgage no capital gains"
            ],
            "negative_keywords": ["crypto price prediction", "how to buy crypto", "crypto wallet"],
            "match_type": "Phrase and exact",
            "bid_strategy": "Target CPA — mortgage leads high value",
            "landing_page_signal": "Page must mention Coinbase + Fannie Mae to match intent",
        },
        "hook_formulas": [
            "You don't have to sell your [CRYPTO] to buy a house anymore.",
            "BTC holders: Fannie Mae just changed the game. Here's what it means for you.",
            "The capital gains tax on selling crypto to buy a house could cost you $[X]. There's a better way.",
            "Pledge your crypto. Keep the upside. Get the keys.",
        ],
        "disqualifiers": "Crypto in retirement account (SDIRA), non-liquid NFT holdings, crypto <6 months old",
    },

    "credit-repair": {
        "product": "Credit Repair / Borrower Education",
        "headline": "The Almost-Ready Buyer",
        "demographics": {
            "age": "24-42",
            "gender": "52% female, 48% male",
            "income": "$45K-$90K household",
            "location": "Metro suburbs, working-class and middle-income neighborhoods",
            "occupation": "Healthcare worker, trades, retail management, admin, teacher",
            "education": "High school to some college",
            "home_status": "Renting ($1,200-$1,800/mo), wants to stop throwing money away",
        },
        "credit_profile": {
            "score_range": "540-650",
            "issues": "Medical debt, missed payments 2-3 years ago, high utilization, 1-2 collections",
            "timeline": "Wants to buy in 6-18 months",
            "knowledge": "Knows their score is low, doesn't know how to fix it strategically",
        },
        "pain_points": [
            "Feels embarrassed by credit score, afraid to apply and get rejected",
            "Has been paying rent equal to a mortgage payment for years — furious about it",
            "Tried disputing things before, didn't work or didn't know how",
            "Doesn't trust credit repair companies (had a bad experience or heard horror stories)",
            "Feels like homeownership is for 'other people'",
        ],
        "dream_outcome": "Walk into a bank and get approved. Be done paying someone else's mortgage.",
        "trigger_phrases": [
            "raise credit score fast",
            "how to fix credit to buy a house",
            "remove collections from credit report",
            "credit score to buy a home",
            "what credit score do I need for a mortgage",
            "goodwill letter",
            "pay for delete",
        ],
        "objections": [
            "Will this actually work or is it another scam?",
            "How long will it take?",
            "I don't have money to pay down debt right now",
            "I already tried disputing stuff",
        ],
        "content_tone": "Empathetic, encouraging, practical — not condescending. 'You're closer than you think.'",
        "where_they_are": ["Facebook (groups: local renters, first-time homebuyers)", "TikTok (credit repair content)", "YouTube (search-based)", "Pinterest (home inspiration)"],
        "meta_targeting": {
            "age_range": "22-45",
            "interests": ["First-time home buying", "Personal finance", "Credit score", "Dave Ramsey", "Renting vs buying", "Home ownership"],
            "behaviors": ["Early technology adopters (budget apps)", "Away from family"],
            "income": "25-75th percentile",
            "life_events": ["Recently moved", "New job"],
            "custom_audiences": "Retarget website visitors who viewed credit repair content",
            "placement": "Facebook Feed, Facebook Groups, Instagram Reels, TikTok",
        },
        "google_targeting": {
            "keywords": [
                "how to raise credit score 100 points", "credit score for mortgage",
                "remove collections to buy house", "credit repair before buying home",
                "what credit score do I need to buy a house in Texas",
                "goodwill letter template mortgage"
            ],
            "match_type": "Broad modified + phrase",
            "bid_strategy": "Maximize clicks → optimize for form fills",
        },
        "hook_formulas": [
            "You're paying $1,500/mo in rent. A mortgage payment on a $250K home is $1,400. The only thing stopping you is a credit score.",
            "Most people with a 600 credit score can be mortgage-ready in 90 days. Here's the exact playbook.",
            "Your landlord is getting rich off your rent check. You could be building equity instead.",
            "The goodwill letter is the most underused credit repair tool. Here's how to write one.",
        ],
        "disqualifiers": "Bankruptcy within 2 years, no income, non-US citizen without work authorization",
    },

    "va-loan": {
        "product": "VA Loan (Zero Down, No PMI)",
        "headline": "The Veteran Who Doesn't Know What They Have",
        "demographics": {
            "age": "24-55",
            "gender": "75% male, 25% female",
            "income": "$55K-$120K",
            "location": "Near military bases and installations, Veterans communities",
            "occupation": "Active duty, veteran, National Guard/Reserve, surviving spouse",
            "home_status": "Renting or living on base, wants to build equity",
        },
        "veteran_profile": {
            "service": "Army, Air Force, Navy, Marines, Coast Guard — any branch",
            "knowledge_gap": "Many don't know they qualify, or think VA loans are complicated/slow",
            "misconception_1": "You have to use it immediately after discharge — FALSE",
            "misconception_2": "You can only use it once — FALSE",
            "misconception_3": "It takes forever and sellers don't like VA offers — OUTDATED",
        },
        "pain_points": [
            "Doesn't know the full extent of their VA benefit",
            "Thinks they need 20% down like everyone else",
            "Has been told VA offers are 'weak' or sellers won't accept them",
            "Worried about VA appraisal requirements slowing down a purchase",
            "PMI on a conventional loan is eating $200-400/mo they don't need to pay",
        ],
        "dream_outcome": "Own a home with zero down, no PMI, and a competitive offer — using a benefit they earned.",
        "trigger_phrases": [
            "VA loan zero down",
            "VA home loan benefits",
            "can I buy a house with VA loan",
            "VA loan vs conventional",
            "VA loan [state]",
            "first time homebuyer veteran",
        ],
        "content_tone": "Respectful, direct, patriotic — they earned this, just tell them how to use it. Zero fluff.",
        "where_they_are": ["Facebook (Veterans groups, military spouse groups)", "YouTube", "Base housing bulletin boards / Facebook marketplace", "Veterans Service Organizations"],
        "meta_targeting": {
            "age_range": "22-55",
            "interests": ["US Military", "Veterans benefits", "USAA", "Military OneSource", "American Legion", "VFW", "Home buying"],
            "custom_audiences": "Military email lists if available; Facebook 'Military' interest",
            "life_events": ["Recently discharged", "New job"],
            "placement": "Facebook Feed, Instagram, Facebook Groups (Veterans)",
        },
        "google_targeting": {
            "keywords": [
                "VA loan zero down", "VA home loan", "zero down home loan veteran",
                "VA loan requirements 2026", "how does VA loan work",
                "VA loan vs FHA", "VA loan entitlement"
            ],
            "match_type": "Phrase and exact",
        },
        "hook_formulas": [
            "If you served, you earned a benefit most veterans never use. $0 down. No PMI. It's yours.",
            "Veterans: Your VA loan benefit doesn't expire. Here's how to use it in today's market.",
            "You're paying $300/mo in PMI you don't have to pay. VA loans eliminate it entirely.",
            "Sellers are accepting VA offers. The old stigma is gone. Here's the data.",
        ],
    },

    "realtor-partner": {
        "product": "Realtor Partnership (Preferred Lender / Referral Network)",
        "headline": "The Agent Who Needs a Lender They Can Trust",
        "demographics": {
            "age": "28-50",
            "gender": "60% female, 40% male",
            "income": "Commission-based — $60K-$200K depending on volume",
            "location": "Active local markets — high-volume suburbs with strong resale activity",
            "experience": "2-8 years, 8-25 closings/year",
            "brokerage": "Independent or small-to-mid team (not mega-team with captive lender)",
        },
        "business_pain": [
            "Previous lender blew up a closing — lost a commission and a client relationship",
            "Lender doesn't return buyer calls fast enough — agent looks bad",
            "Can't get pre-approvals quickly — loses clients to faster-moving agents",
            "Lender gives wrong info to buyers — creates expectations problems",
            "Wants a lender who will co-market and send referrals back",
        ],
        "dream_outcome": "A lender who makes them look like a rock star to every buyer. More closings, less stress.",
        "trigger_phrases": [
            "preferred lender",
            "mortgage partner for realtors",
            "lender who closes on time",
            "pre-approval in 24 hours",
            "real estate agent lender referral",
        ],
        "content_tone": "Peer-to-peer, B2B professional — not a sales pitch. 'Here's how we make you more money.'",
        "where_they_are": ["Instagram (real estate agent accounts)", "Facebook (agent groups)", "LinkedIn", "ActiveRain", "Local NTREIS/NAR events", "Inman"],
        "meta_targeting": {
            "age_range": "26-52",
            "interests": ["Real estate", "National Association of Realtors", "Inman News", "Real estate agent", "Zillow", "CINC", "Follow Up Boss"],
            "behaviors": ["Small business owners"],
            "job_title_targeting": "Real estate agent, Realtor, Real estate broker",
            "placement": "LinkedIn (job title targeting strongest here), Facebook Feed, Instagram",
        },
        "google_targeting": {
            "keywords": [
                "mortgage lender for realtors", "preferred lender real estate agent",
                "fast pre-approval mortgage", "lender who closes on time"
            ],
            "match_type": "Phrase",
        },
        "hook_formulas": [
            "Your lender is either making you look good or making you look bad. There's no middle.",
            "I close on time. I answer the phone. I send buyers back. That's the whole pitch.",
            "The #1 complaint buyers have about the home buying process is their lender. Not the agent. Fix that.",
            "Every agent I work with gets: 24-hr pre-approval, daily updates, and buyers sent back. Here's the math on that.",
        ],
    },

    "first-time-buyer": {
        "product": "First-Time Homebuyer Program",
        "headline": "The Overwhelmed First-Timer",
        "demographics": {
            "age": "24-36",
            "gender": "Even split",
            "income": "$60K-$110K household",
            "location": "Metro suburbs transitioning to homeownership",
            "occupation": "Young professional, dual income couples, recently married",
            "home_status": "Renting, lease ending, or living with parents to save",
        },
        "pain_points": [
            "Has no idea where to start — the process feels overwhelming and opaque",
            "Worried they can't afford it — doesn't know about assistance programs",
            "Fear of making the wrong decision on the biggest purchase of their life",
            "Doesn't know what a 'good' rate is or how to compare lenders",
            "Parents bought at 3% — current rates feel impossible to them",
        ],
        "dream_outcome": "A home of their own — with someone guiding them through every step so they don't make an expensive mistake.",
        "trigger_phrases": [
            "first time home buyer tips",
            "how to buy a house first time",
            "first time homebuyer programs Texas",
            "down payment assistance programs",
            "steps to buying a house",
            "can I afford to buy a house",
        ],
        "content_tone": "Reassuring, educational, step-by-step — like a trusted friend who happens to be an expert",
        "where_they_are": ["TikTok (explainer content)", "Instagram Reels", "YouTube", "Pinterest (home inspo)", "Reddit r/FirstTimeHomeBuyer"],
        "meta_targeting": {
            "age_range": "22-38",
            "interests": ["First time home buying", "HGTV", "Home decor", "Personal finance", "Zillow", "Trulia"],
            "life_events": ["Recently engaged", "Recently married", "New job"],
            "income": "30-70th percentile",
            "placement": "Instagram Reels, TikTok, Facebook Feed",
        },
        "hook_formulas": [
            "Nobody teaches you how to buy a house. Here's the 5-step process in plain English.",
            "First-time buyers: there are programs that cover your down payment. Most people don't know they exist.",
            "Stop letting your rent pay your landlord's mortgage. Here's how to make it yours instead.",
            "The rate isn't the most important number in a mortgage. Here's what actually matters.",
        ],
    },
}

PRODUCT_ALIASES = {
    "crypto": "crypto-mortgage",
    "crypto mortgage": "crypto-mortgage",
    "fannie mae": "crypto-mortgage",
    "bitcoin mortgage": "crypto-mortgage",
    "credit": "credit-repair",
    "credit repair": "credit-repair",
    "credit score": "credit-repair",
    "va": "va-loan",
    "va loan": "va-loan",
    "veteran": "va-loan",
    "veterans": "va-loan",
    "realtor": "realtor-partner",
    "agent": "realtor-partner",
    "realtor partner": "realtor-partner",
    "partnership": "realtor-partner",
    "first time": "first-time-buyer",
    "first-time buyer": "first-time-buyer",
    "first time buyer": "first-time-buyer",
    "fthb": "first-time-buyer",
}


def resolve_product(name: str) -> str:
    key = name.lower().strip()
    return PRODUCT_ALIASES.get(key, key)


def get_icp(product_key: str) -> dict:
    key = resolve_product(product_key)
    if key not in ICPS:
        available = ", ".join(ICPS.keys())
        print(f"ERROR: Unknown product '{product_key}'. Available: {available}")
        sys.exit(1)
    return ICPS[key]


def print_icp(icp: dict, fmt: str = "text"):
    if fmt == "json":
        print(json.dumps(icp, indent=2))
        return

    bar = "━" * 55
    print(f"\n{bar}")
    print(f"ICP: {icp['product']}")
    print(f"     \"{icp['headline']}\"")
    print(bar)

    d = icp["demographics"]
    print(f"\nDEMOGRAPHICS")
    for k, v in d.items():
        print(f"  {k:20} {v}")

    print(f"\nPAIN POINTS")
    for p in icp.get("pain_points", icp.get("business_pain", [])):
        print(f"  • {p}")

    print(f"\nDREAM OUTCOME")
    print(f"  {icp['dream_outcome']}")

    print(f"\nTRIGGER PHRASES (what they search / say)")
    for t in icp["trigger_phrases"]:
        print(f"  \"{t}\"")

    print(f"\nCONTENT TONE")
    print(f"  {icp['content_tone']}")

    print(f"\nWHERE THEY ARE")
    for w in icp.get("where_they_are", []):
        print(f"  • {w}")

    mt = icp.get("meta_targeting", {})
    if mt:
        print(f"\nMETA AD TARGETING")
        print(f"  Ages:      {mt.get('age_range','')}")
        print(f"  Interests: {', '.join(mt.get('interests',[])[:5])}...")
        print(f"  Placement: {mt.get('placement','')}")
        if mt.get("life_events"):
            print(f"  Life events: {', '.join(mt['life_events'])}")
        if mt.get("income"):
            print(f"  Income:    {mt['income']}")

    gt = icp.get("google_targeting", {})
    if gt:
        print(f"\nGOOGLE AD TARGETING")
        kw = gt.get("keywords", [])
        for k in kw[:5]:
            print(f"  \"{k}\"")
        if len(kw) > 5:
            print(f"  ... +{len(kw)-5} more")

    print(f"\nHOOK FORMULAS")
    for i, h in enumerate(icp.get("hook_formulas", []), 1):
        print(f"  {i}. {h}")

    print(f"\n{bar}\n")


def generate_content_with_llm(icp: dict, content_request: str) -> str:
    """Use generate.py backend to produce personalized content for this ICP."""
    try:
        sys.path.insert(0, os.path.dirname(__file__))
        from generate import complete
    except ImportError:
        # generate.py is in the openclaw-skills parent dir
        gen_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "..",
            "tier1-implementations", "openclaw-skills"
        )
        sys.path.insert(0, os.path.abspath(gen_path))
        try:
            from generate import complete
        except ImportError:
            return "[generate.py not found — set LLM_BACKEND=haiku and ensure generate.py is in path]"

    system = f"""You are a direct-response marketing expert specializing in mortgage and real estate.
You are writing content for a SPECIFIC ideal customer profile:

Product: {icp['product']}
ICP Name: {icp['headline']}
Age: {icp['demographics']['age']}
Pain points: {'; '.join(icp['pain_points'][:3])}
Dream outcome: {icp['dream_outcome']}
Tone: {icp['content_tone']}
Hook formulas to draw from: {'; '.join(icp.get('hook_formulas',[])[:2])}

Write ONLY for this specific person. Use their language. Address their exact pain.
Never write generic mortgage content. Every word must be aimed at this ICP.
Brand: [Your Brand] | [Your Name], Mortgage Professional."""

    user = f"Create the following for this ICP:\n\n{content_request}"
    return complete(system=system, user=user, quality="auto", max_tokens=2048, verbose=True)


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="ICP Modeler — ideal customer profiles for mortgage and real estate"
    )
    parser.add_argument("--product", "-p", default="",
                        help="Product name (e.g. 'crypto mortgage', 'VA loan', 'credit repair')")
    parser.add_argument("--list", action="store_true", help="List all available ICPs")
    parser.add_argument("--demo", action="store_true", help="Print crypto-mortgage ICP profile (no API needed)")
    parser.add_argument("--version", action="version", version="icp-modeler v1.0.0")
    parser.add_argument("--generate-content", "-g", default="",
                        metavar="REQUEST",
                        help="Generate personalized content for this ICP (requires LLM backend)")
    parser.add_argument("--output", "-o", default="text",
                        choices=["text", "json"], help="Output format")
    args = parser.parse_args()

    if args.list:
        print("\nAvailable ICPs:")
        for key, icp in ICPS.items():
            print(f"  {key:25} — {icp['headline']}")
        print("\nAliases: crypto, va, credit, realtor, first-time")
        return

    if args.demo:
        print("[DEMO] Showing crypto-mortgage ICP (run --list for all profiles)\n")
        print_icp(ICPS["crypto-mortgage"], args.output)
        return

    if not args.product:
        parser.print_help()
        sys.exit(1)

    icp = get_icp(args.product)
    print_icp(icp, args.output)

    if args.generate_content:
        print(f"GENERATED CONTENT ({args.generate_content.upper()})")
        print("━" * 55)
        result = generate_content_with_llm(icp, args.generate_content)
        print(result)
        print("━" * 55)


if __name__ == "__main__":
    main()
