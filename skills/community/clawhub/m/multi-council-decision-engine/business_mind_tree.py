"""
business_mind_tree.py — multi-council strategic decision engine.

Eight framework councils. Each council is a callable that applies a specific
class of reasoning methodologies (NOT individual people) to a prompt and
returns structured analysis. Synthesized output drives go/hold/kill decisions
before ventures get built.

Design principles:
  - Emulate frameworks, not personalities
  - Each council returns the SAME structured JSON shape so synthesis is mechanical
  - Use the Builder Agent's _call_model (so OpenRouter fallback works automatically)
  - Cheap and parallel by default — Sonnet for complex councils, Haiku for fast checks

Public actions (registered via get_actions()):
  strategy_council(prompt, context="")
  risk_council(prompt, context="")
  market_council(prompt, context="")
  operations_council(prompt, context="")
  ai_engineering_council(prompt, context="")
  forecasting_council(prompt, context="")
  execution_council(prompt, context="")
  ethics_council(prompt, context="")
  multi_council(prompt, context="", councils=None)
  list_councils()

All councils return:
  {
    "council": "<name>",
    "summary": "<one paragraph>",
    "key_findings": [<bullet list>],
    "risks_or_concerns": [<bullet list>],
    "recommendation": "go" | "hold" | "kill" | "iterate",
    "confidence": <int 1-10>,
    "framework_applied": "<methodology label>",
    "cost_usd": <float>
  }

multi_council adds a "synthesis" key with combined recommendation.
"""

from __future__ import annotations

import json
import logging
import os
import re
import time
from pathlib import Path
from typing import Optional

_HERE = Path(__file__).resolve().parent
_LOG_DIR = _HERE / "logs"
_LOG_DIR.mkdir(exist_ok=True)
LAB_LOG = str(_LOG_DIR / "business_mind_tree.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LAB_LOG), logging.StreamHandler()],
)
log = logging.getLogger("business_mind_tree")



# --- OpenRouter-primary routing ---

# Map ORA's internal model names to OpenRouter model identifiers.
# OpenRouter uses <vendor>/<model> format. Adjust per your OpenRouter catalog
# at https://openrouter.ai/models if anything 404s.
_OR_MODEL_MAP = {
    "claude-sonnet-4-6":         "anthropic/claude-sonnet-4",
    "claude-opus-4-6":           "anthropic/claude-opus-4",
    "claude-haiku-4-5-20251001": "anthropic/claude-3.5-haiku",
    # Backstops in case the 4-series names aren\'t available yet on OpenRouter:
    "claude-3.5-sonnet":         "anthropic/claude-3.5-sonnet",
    "claude-3.5-haiku":          "anthropic/claude-3.5-haiku",
}

# Rough per-model pricing (USD per Mtok). OpenRouter adds ~5% markup over
# direct provider. Conservative numbers below.
_OR_PRICING = {
    "anthropic/claude-sonnet-4":   {"input": 3.00, "output": 15.00},
    "anthropic/claude-opus-4":     {"input": 15.00, "output": 75.00},
    "anthropic/claude-opus-4.8":   {"input": 5.00, "output": 25.00},
    "openai/gpt-5.5":              {"input": 5.00, "output": 30.00},
    "z-ai/glm-5.2":                {"input": 1.00, "output": 4.00},
    "anthropic/claude-3.5-sonnet": {"input": 3.00, "output": 15.00},
    "anthropic/claude-3.5-haiku":  {"input": 1.00, "output":  5.00},
    "openai/gpt-4o":               {"input": 2.50, "output": 10.00},
    "openai/gpt-4o-mini":          {"input": 0.15, "output":  0.60},
}


def _to_or_model(internal_name: str) -> str:
    return _OR_MODEL_MAP.get(internal_name, internal_name)


def _call_openrouter_primary(model: str, system: str, user: str, max_tokens: int) -> tuple:
    """Primary council backend. Uses OPENROUTER_API_KEY."""
    try:
        from openai import OpenAI
    except ImportError:
        raise RuntimeError(
            "openai package not installed. "
            "Run: pip install openai --break-system-packages"
        )
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY not set in environment")

    or_model = _to_or_model(model)
    client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")

    resp = client.chat.completions.create(
        model=or_model,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
        extra_headers={
            "HTTP-Referer": os.environ.get("OPENROUTER_APP_URL", "https://github.com/openclaw"),
            "X-Title": os.environ.get("OPENROUTER_APP_NAME", "Multi-Council Decision Engine"),
        },
    )
    text = resp.choices[0].message.content or ""
    in_chars = len(system) + len(user)
    out_chars = len(text)
    p = _OR_PRICING.get(or_model, _OR_PRICING["anthropic/claude-3.5-sonnet"])
    cost = (in_chars / 4 / 1_000_000) * p["input"] + (out_chars / 4 / 1_000_000) * p["output"]
    _log_or_cost(or_model, cost, in_chars, out_chars)
    log.info("OpenRouter %s ok ($%.4f)", or_model, cost)
    return text, cost


def _log_or_cost(model: str, cost_usd: float, in_chars: int, out_chars: int) -> None:
    """Append OpenRouter call cost to a local cost-log JSON file."""
    log_path = str(_HERE / "cost_log.json")
    import json as _json
    try:
        existing = []
        if os.path.exists(log_path):
            try:
                with open(log_path) as f:
                    existing = _json.load(f)
                if not isinstance(existing, list):
                    existing = []
            except Exception:
                existing = []
        existing.append({
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "venture": "business_mind_tree",
            "model": model,
            "cost_usd": round(cost_usd, 6),
            "input_chars": in_chars,
            "output_chars": out_chars,
        })
        with open(log_path, "w") as f:
            _json.dump(existing, f, indent=2)
    except Exception as e:
        log.warning("could not log cost: %s", e)


def _model_call(model: str, system: str, user: str, max_tokens: int = 3000) -> tuple:
    """STRICT OpenRouter routing. No fallback. If OPENROUTER_API_KEY is missing
    or OpenRouter fails, raise — do not silently route to Anthropic direct."""
    if model == "heavy":
        model = select_heavy_model()
    return _call_openrouter_primary(model, system, user, max_tokens)

# --- end OpenRouter-primary routing ---


# --- shared heavy-task model selection (genuine strategic reasoning only) --
#
# Per ORA's cost philosophy (default to cheapest model that reliably does the
# job; reserve the strongest model for genuine multi-step strategic reasoning),
# this picks dynamically between the current flagship candidates rather than
# hardcoding one vendor — so ORA doesn't go stale defaulting to e.g. Opus when
# a stronger model becomes available, or vice versa. Used by any heavy-task
# council here AND by use_case_agent.py (STEM reverse-engineering) — import
# this function rather than duplicating the selection logic elsewhere.

_HEAVY_MODEL_CACHE = str(_HERE / "_heavy_model_cache.json")
_HEAVY_CANDIDATES = ["openai/gpt-5.5", "anthropic/claude-opus-4.8", "z-ai/glm-5.2"]
_HEAVY_CACHE_TTL = 86400  # 24h — avoid hitting the OpenRouter catalog on every call
_HEAVY_FALLBACK = "anthropic/claude-opus-4.8"


def select_heavy_model() -> str:
    """Pick the strongest available model for heavy strategic reasoning by
    comparing live OpenRouter catalog data for the current flagship candidates.

    Heuristic: candidates within ~2% context_length of the largest one are
    treated as a comparable tier (real context-window differences below that
    are noise, not a capability signal); among that tier, pick the CHEAPEST.
    This was previously inverted — it picked the most expensive model as a
    "flagship" proxy, which silently penalized z-ai/glm-5.2 for being ~6x
    cheaper than gpt-5.5/claude-opus-4.8 despite producing comparably sharp
    reasoning in a direct side-by-side test (2026-06-21) at a fraction of the
    cost — exactly backwards from this project's stated cost-discipline rule
    (default to cheapest model that reliably does the job). Cached 24h so
    this doesn't add a catalog call to every task."""
    try:
        if os.path.exists(_HEAVY_MODEL_CACHE):
            with open(_HEAVY_MODEL_CACHE) as f:
                cached = json.load(f)
            if time.time() - cached.get("ts", 0) < _HEAVY_CACHE_TTL:
                return cached["model"]
    except Exception:
        pass

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        return _HEAVY_FALLBACK
    try:
        import urllib.request
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/models",
            headers={"Authorization": f"Bearer {api_key}"},
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            catalog = json.loads(r.read().decode())
        by_id = {m["id"]: m for m in catalog.get("data", [])}
        available = []
        for cid in _HEAVY_CANDIDATES:
            m = by_id.get(cid)
            if not m:
                continue
            ctx = m.get("context_length") or 0
            price = float((m.get("pricing") or {}).get("completion") or 0)
            available.append((cid, ctx, price))

        if not available:
            best = _HEAVY_FALLBACK
        else:
            max_ctx = max(ctx for _, ctx, _ in available)
            tier = [(cid, ctx, price) for cid, ctx, price in available if ctx >= max_ctx * 0.98]
            best = min(tier, key=lambda t: t[2])[0]

        with open(_HEAVY_MODEL_CACHE, "w") as f:
            json.dump({"model": best, "ts": time.time()}, f)
        log.info("heavy model selected: %s", best)
        return best
    except Exception as e:
        log.warning("heavy model selection failed (%s) — falling back to %s", e, _HEAVY_FALLBACK)
        return _HEAVY_FALLBACK

# --- end shared heavy-task model selection ---



# --- council system prompts ------------------------------------------------
#
# Each prompt encodes a class of reasoning methodologies. Frameworks only.
# No named individuals. Output is enforced as JSON.

_OUTPUT_SHAPE = """
Return ONLY a JSON object (no prose outside it) with this exact shape:

{
  "summary": "<one paragraph plain-English assessment>",
  "key_findings": ["<finding 1>", "<finding 2>", ...],
  "risks_or_concerns": ["<concern 1>", "<concern 2>", ...],
  "recommendation": "go" | "hold" | "kill" | "iterate",
  "confidence": <integer 1-10>,
  "framework_applied": "<the specific methodology you used>"
}
"""


STRATEGY_PROMPT = """You are ORA's Strategy Council. Apply these
methodologies to evaluate the input:

1. INVERSION — work backward from what failure looks like; identify what
   would have to be true for this to fail catastrophically, and check
   whether those conditions are present.

2. MENTAL MODELS — apply multi-disciplinary lenses: economic incentives,
   psychological biases, ecological/system feedback, network effects.

3. DECISION ARCHITECTURE — assess: is this a one-way door (irreversible)
   or two-way door (reversible)? Match decision weight to reversibility.

4. ASYMMETRIC BETS — evaluate the skew: limited downside / unlimited
   upside is preferred; symmetric risks need higher confidence.

5. LONG-HORIZON OPTIMIZATION — consider 1-year and 5-year implications,
   not just immediate ROI. What compounds? What is fragile?

For the input given, apply these explicitly. Be specific. Avoid
generic advice. Cite which methodology drove each conclusion.
""" + _OUTPUT_SHAPE


RISK_PROMPT = """You are ORA's Risk Council. Apply these methodologies:

1. ANTIFRAGILITY ANALYSIS — does this gain from disorder, or merely
   resist it? Robust > fragile, but antifragile > robust. Where does
   this fall?

2. BLACK SWAN AWARENESS — what low-probability high-impact events would
   destroy this? Are there any rare-but-not-zero failure modes the
   operator hasn't considered?

3. ASYMMETRIC RISK EVALUATION — is the loss bounded? Is the gain bounded?
   Skewed-positive scenarios deserve premium attention; skewed-negative
   ones need defenses or avoidance.

4. HIDDEN RISK SURFACING — what risks does the operator NOT see because
   they're outside their reference class? Single-point-of-failure
   dependencies, regulatory shifts, key-person risks, etc.

5. ROBUSTNESS TESTING — propose 2-3 stress scenarios and assess survival.

Be brutally honest. Risk Council's job is to find what breaks. Avoid
softening conclusions to be agreeable.
""" + _OUTPUT_SHAPE


MARKET_PROMPT = """You are ORA's Market Council. Apply these methodologies:

1. MACRO POSITIONING — what economic regime are we in (rates,
   inflation, employment, sentiment)? Does this opportunity fit that
   regime or fight against it?

2. CAPITAL ALLOCATION — compound returns matter. What is the
   probability-weighted return on capital? Is this a one-shot or
   repeatable?

3. REFLEXIVITY — how do perceptions affect fundamentals here? Are we
   in a trend that's self-reinforcing or self-correcting?

4. DISRUPTIVE INNOVATION SCAN — is this defending an old position or
   capturing a new one? S-curve placement matters.

5. VALUE vs GROWTH TRADEOFF — is the moat durable (value) or based on
   speed of capture (growth)? Match the analysis style.

Recommend based on capital efficiency and market timing. Not all
opportunities are bad — but not all are timely either.
""" + _OUTPUT_SHAPE


OPERATIONS_PROMPT = """You are ORA's Operations Council. Apply these
methodologies:

1. WORKFLOW CAPTURE — what are the steps, who does them, where does
   ownership transfer? Map the value chain.

2. EXECUTION SYSTEMS — what feedback loops exist? Where do errors
   surface? How fast is the learning cycle?

3. DECISION COMPRESSION — where can decisions be made faster or
   delegated? Bottlenecks are usually human approval points.

4. BOTTLENECK IDENTIFICATION — which step has the lowest throughput?
   That's the constraint to optimize first.

5. THROUGHPUT OPTIMIZATION — what's the gating resource (time, money,
   attention, expertise)? Optimize that, not everything.

Operational thinking is concrete and resource-aware. Map the system,
find the constraint, propose the fix.
""" + _OUTPUT_SHAPE


AI_ENGINEERING_PROMPT = """You are ORA's AI Engineering Council. Apply
these methodologies:

1. ARCHITECTURE DECISIONS — modularity vs monolith, statelessness vs
   state, sync vs async. Match to use case.

2. SCALING HYPOTHESES — does this benefit from more data, more compute,
   more parameters? Or is it constraint-limited (latency, cost, UX)?

3. COST vs PERFORMANCE — what's the minimum model that delivers
   acceptable quality? Routinely over-spec'd systems waste compute.

4. PRACTICAL DEPLOYMENT FOCUS — what's the path to production? Skip
   research-grade complexity if a deployment-grade simpler version works.

5. HUMAN-READABLE REASONING — can the operator inspect WHY the AI did
   what it did? Opaque AI is fragile AI.

Engineering thinking optimizes for ship-able, debuggable, scalable.
Reject premature optimization. Reject premature complexity.
""" + _OUTPUT_SHAPE


FORECASTING_PROMPT = """You are ORA's Forecasting Council. Apply these
methodologies:

1. PROBABILISTIC THINKING — never say "this will happen." Express
   confidence as ranges with base rates. What's the prior probability
   from comparable past events?

2. REFERENCE CLASS FORECASTING — find the closest historical analog
   (or class of analogs) and use their distribution as the baseline.

3. SCENARIO ANALYSIS — identify 3 paths: optimistic (top quartile),
   base (median), pessimistic (bottom quartile). Assign rough probabilities.

4. GEOPOLITICAL / MACRO RISKS — what shifts in policy, regulation,
   demographics, supply chains, or international relations could
   change the outcome?

5. COMPOUND UNCERTAINTY — when multiple uncertainties stack, naive
   probability multiplication understates the spread. Account for that.

Forecast humbly. Calibration matters more than confidence.
""" + _OUTPUT_SHAPE


EXECUTION_PROMPT = """You are ORA's Execution Council. Apply these
methodologies:

1. FIRST PRINCIPLES — strip the problem to fundamentals. Don't accept
   inherited assumptions. What MUST be true? What's just convention?

2. AGGRESSIVE EXECUTION LOOPS — ship the smallest viable version fast,
   gather feedback, iterate. Speed of iteration beats quality of plan.

3. PRODUCT SIMPLICITY — cut every non-essential feature. What's the
   one thing this MUST do? Everything else is debt.

4. RESOURCE LEVERAGE — where can a small input create a large output?
   Find the asymmetry; that's where to invest effort.

5. ITERATION RATE — how fast can the operator learn from each cycle?
   Faster learning compounds; slower learning gets out-competed.

Execution thinking is bias-toward-action. Reject analysis paralysis.
Reject scope creep. Ship small, iterate fast.
""" + _OUTPUT_SHAPE


ETHICS_PROMPT = """You are ORA's Ethics & Guardrails Council. Apply
these methodologies:

1. STAKEHOLDER IMPACT ANALYSIS — who benefits? Who is harmed? Who
   bears risk vs reward? Identify imbalances.

2. COMPLIANCE LENS — what regulatory frameworks apply (tax, financial,
   advertising, data privacy, professional licensure)? What lines
   exist that shouldn't be crossed even when nobody's watching?

3. REPUTATIONAL RISK — if this were on the front page of the news,
   would it survive scrutiny? If not, what changes?

4. STAKEHOLDER FAIRNESS — does this exploit asymmetric information,
   power, or attention? Sustainable models don't depend on exploitation.

5. LONG-TERM CONSEQUENCES — what 2nd- and 3rd-order effects emerge
   over 12+ months? Path-dependent harms are easy to miss in launch
   excitement.

Ethics Council should be uncomfortable to read sometimes. That's
how you know it's doing its job. The operator can override but should
never get a quiet rubber-stamp.
""" + _OUTPUT_SHAPE


CONTENT_PROMPT = """You are ORA Content Council. Apply these methodologies
to evaluate content strategy, marketing copy, and campaign decisions:

1. HOOK CONSTRUCTION - every piece of content has about 1.7 seconds to earn
   the next 5 seconds. Evaluate hooks against four dimensions:
   - CURIOSITY GAP: does the reader feel compelled to know more?
   - SPECIFICITY: concrete numbers, names, places beat vague claims
   - CONTRAST: surprising tension between expectation and reality
   - EGO/IDENTITY: does the hook speak to who the reader wants to be?

2. DISTRIBUTION STRATEGY - content without distribution is journaling.
   Evaluate channel-fit (does the format match where the audience lives?),
   algorithm awareness (current platform rules, watch-time, retention),
   and timing (post when target audience is on).

3. VIRAL MECHANICS - share is not luck. Evaluate K-factor (will each viewer
   bring N new viewers?), network triggers, shareability dimensions.

4. CONVERSION PSYCHOLOGY - apply Cialdini principles where appropriate:
   reciprocity, commitment/consistency, social proof, authority, liking,
   scarcity. Map each to the specific content moment that triggers it.
   Identify friction points and propose specific removals.

5. CONTENT-MARKET FIT - does the content resonate with the audience actual
   problems (not the operator assumed problems)? Brand voice consistency?
   One-step CTA always wins over multi-step.

For back-tax / IRS-resolution content: respect compliance - no specific
dollar promises, no guaranteed language, no implied government endorsement.

Be specific. Reference which methodology drove each conclusion. Avoid
generic marketing advice.
""" + _OUTPUT_SHAPE

SOCIAL_MEDIA_PROMPT = """You are ORA's Social Media Council. This council groups the
distinct disciplines that separate the top operators in social media marketing from
everyone else — frameworks only, no named individuals. Apply all five to every
evaluation; a saturated market is exactly where amateurs only apply one.

1. PLATFORM-NATIVE ALGORITHM MASTERY — every platform ranks on different real signals
   (watch-time/completion %, saves, shares, comments-per-reach, not just likes). Evaluate:
   does this content match the format the platform's algorithm actually rewards right now
   (native vertical video, real captions vs reposted text, trending audio/format usage)?
   Generic cross-posted content loses to platform-native content every time.

2. COMMUNITY-LED GROWTH — broadcasting at an audience loses to building with one.
   Evaluate: does this invite a reply, a duet, a UGC submission, a DM? Is there a real
   reply culture (the brand actually responds, fast, in voice) or is it post-and-ghost?
   Community compounds; broadcast doesn't.

3. CREATOR-ECONOMY / FOUNDER-LED CONTENT — in 2026, founder-shot, slightly-imperfect
   content consistently outperforms polished brand content because it reads as real.
   Evaluate: does this feel like a person talking to a person, or a brand talking at a
   feed? Micro-influencer/creator partnership math (engagement rate over follower count)
   beats vanity-metric influencer spend.

4. PAID SOCIAL VELOCITY — winners are found by testing many cheap variants fast, not
   perfecting one expensive ad. Evaluate: is there a real test-and-kill cadence (multiple
   creative variants, fast kill on losers, fast scale on winners) or is this a single
   "hero" ad expected to carry the whole budget? CPM/CPA discipline — what's the real
   target cost-per-result, and is the creative actually built to hit it?

5. SOCIAL PROOF LOOPS & SOCIAL COMMERCE — real reviews/UGC/comments should feed back into
   the next round of content and ads, not sit static on a page. Evaluate: is there a loop
   (customer content → ad creative → more customers → more content) or is social proof a
   one-time install-and-forget element? Native in-platform purchase/DM/booking flows beat
   sending traffic off-platform when the platform supports it.

For back-tax / IRS-resolution content: respect compliance - no specific dollar promises,
no guaranteed language, no implied government endorsement.

Be specific. Reference which methodology drove each conclusion. Never recommend simply
copying what a competitor is doing — identify what's actually working for them, then
recommend a genuinely different angle that beats it, not a clone of it.
""" + _OUTPUT_SHAPE

COUNCILS: dict[str, dict] = {
    # "heavy" = dynamically resolved at call time via select_heavy_model()
    # (currently gpt-5.5 vs claude-opus-4.8, whichever scores higher) — used
    # only for genuine multi-step strategic/go-hold-kill reasoning, per ORA's
    # cost philosophy of reserving the strongest model for that class of task.
    "strategy": {
        "system": STRATEGY_PROMPT,
        "model": "heavy",
        "max_tokens": 3000,
        "framework": "inversion + mental models + decision architecture",
    },
    "content": {
        "system": CONTENT_PROMPT,
        "model": "claude-sonnet-4-6",
        "max_tokens": 3000,
        "framework": "hook + distribution + viral + conversion psychology",
    },
    "risk": {
        "system": RISK_PROMPT,
        "model": "heavy",
        "max_tokens": 3000,
        "framework": "antifragility + black swan + asymmetric risk",
    },
    "market": {
        "system": MARKET_PROMPT,
        "model": "heavy",
        "max_tokens": 3000,
        "framework": "macro positioning + capital allocation + reflexivity",
    },
    "operations": {
        "system": OPERATIONS_PROMPT,
        "model": "z-ai/glm-5.2",
        "max_tokens": 2000,
        "framework": "workflow capture + bottleneck analysis",
    },
    "ai_engineering": {
        "system": AI_ENGINEERING_PROMPT,
        "model": "heavy",
        "max_tokens": 2500,
        "framework": "architecture decisions + scaling hypotheses",
    },
    "forecasting": {
        "system": FORECASTING_PROMPT,
        "model": "heavy",
        "max_tokens": 3000,
        "framework": "probabilistic + reference class + scenario",
    },
    "execution": {
        "system": EXECUTION_PROMPT,
        "model": "z-ai/glm-5.2",
        "max_tokens": 2000,
        "framework": "first principles + aggressive iteration",
    },
    "ethics": {
        "system": ETHICS_PROMPT,
        "model": "heavy",
        "max_tokens": 3000,
        "framework": "stakeholder + compliance + reputational",
    },
    "social_media": {
        "system": SOCIAL_MEDIA_PROMPT,
        "model": "heavy",
        "max_tokens": 3000,
        "framework": "platform algorithm + community + creator-led + paid velocity + social proof loops",
    },
}


# --- internal helpers ------------------------------------------------------


def _extract_json(text: str) -> dict:
    """Tolerant JSON extractor — fenced blocks, trailing prose, etc."""
    if not text or not text.strip():
        raise ValueError("model returned empty text")
    fence = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    if fence:
        return json.loads(fence.group(1))
    start = text.find("{")
    if start == -1:
        raise ValueError(f"no JSON found: {text[:300]}")
    obj, _ = json.JSONDecoder().raw_decode(text, start)
    return obj


def _run_council(name: str, prompt: str, context: str = "") -> dict:
    """Generic council runner. Returns structured analysis dict."""
    if name not in COUNCILS:
        return {"council": name, "ok": False, "error": f"unknown council: {name}"}

    cfg = COUNCILS[name]
    user = prompt.strip()
    if context.strip():
        user += f"\n\nAdditional context:\n{context.strip()}"

    log.info("council=%s prompt_preview=%r", name, prompt[:120])
    try:
        text, cost = _model_call(cfg["model"], cfg["system"], user, cfg["max_tokens"])
    except Exception as e:
        log.exception("council %s call failed", name)
        return {
            "council": name,
            "ok": False,
            "error": str(e),
            "framework_applied": cfg["framework"],
        }

    try:
        parsed = _extract_json(text)
    except Exception as e:
        return {
            "council": name,
            "ok": False,
            "error": f"could not parse council output: {e}",
            "raw": text[:1000],
            "cost_usd": round(cost, 6),
            "framework_applied": cfg["framework"],
        }

    return {
        "council": name,
        "ok": True,
        "summary": parsed.get("summary", ""),
        "key_findings": parsed.get("key_findings", []) or [],
        "risks_or_concerns": parsed.get("risks_or_concerns", []) or [],
        "recommendation": parsed.get("recommendation", "iterate"),
        "confidence": int(parsed.get("confidence", 5)),
        "framework_applied": parsed.get("framework_applied", cfg["framework"]),
        "cost_usd": round(cost, 6),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


# --- public council actions ------------------------------------------------


def strategy_council(prompt: str, context: str = "") -> dict:
    return _run_council("strategy", prompt, context)

def content_council(prompt: str, context: str = "") -> dict:
    return _run_council("content", prompt, context)


def risk_council(prompt: str, context: str = "") -> dict:
    return _run_council("risk", prompt, context)


def market_council(prompt: str, context: str = "") -> dict:
    return _run_council("market", prompt, context)


def operations_council(prompt: str, context: str = "") -> dict:
    return _run_council("operations", prompt, context)


def ai_engineering_council(prompt: str, context: str = "") -> dict:
    return _run_council("ai_engineering", prompt, context)


def forecasting_council(prompt: str, context: str = "") -> dict:
    return _run_council("forecasting", prompt, context)


def execution_council(prompt: str, context: str = "") -> dict:
    return _run_council("execution", prompt, context)


def ethics_council(prompt: str, context: str = "") -> dict:
    return _run_council("ethics", prompt, context)


def social_media_council(prompt: str, context: str = "") -> dict:
    return _run_council("social_media", prompt, context)


def competitive_differentiation_analysis(
    business_name: str,
    business_type: str,
    competitors: list[str],
    real_facts: list[str],
    location: str = "",
) -> dict:
    """Generic local-business competitive positioning analysis: don't help
    a small business mimic what big national competitors do — find what's
    structurally true about big
    brands/chains that they CANNOT fix without breaking their own business
    model (seasonal staff, generic volume-optimized service, upsell-heavy
    fee structures, no local specificity), and position the small business
    against that real structural weakness instead.

    IMPORTANT — this does NOT do its own competitor research. Identifying
    `competitors` is either the client's own answer ("who do you lose
    customers to?") collected during onboarding, or research done by the
    operator/Claude session conversationally — there is no live web-search
    tool wired into this server's runtime. `real_facts` must be facts the
    operator/client has actually confirmed true about THEIR business (e.g.
    "5 years in business", "flat-fee pricing", "same owner since opening")
    — this function will not fabricate claims, and the caller must not feed
    it unconfirmed assumptions either.

    Returns the strategy council's findings: concrete, headline-ready
    positioning angles grounded in real facts, not generic "we're local
    and friendly" filler. Meant to feed BOTH the deliverable shown to the
    business owner AND that business's chat_widget config, so the widget
    can speak knowledgeably about real competitive advantage instead of
    generic FAQ answers.
    """
    prompt = (
        f"{business_name} ({business_type}{', ' + location if location else ''}) "
        f"competes against: {', '.join(competitors) if competitors else '(not specified)'}.\n\n"
        f"Confirmed real facts about {business_name} (use ONLY these — do not invent others):\n"
        + "\n".join(f"- {f}" for f in real_facts) + "\n\n"
        "Give 3 SPECIFIC, concrete repositioning angles this business could use instead of "
        "generic 'local and friendly' messaging — each a literal headline/positioning "
        "statement, grounded in a real structural weakness of the named competitors "
        "(things they cannot fix without breaking their own business model: scale-driven "
        "staff turnover, volume-optimized generic service, hidden fees/upsells, lack of "
        "local specificity, etc). Do not recommend mimicking the competitors. Do not "
        "fabricate any stat, guarantee, or claim not in the confirmed facts list above."
    )
    return strategy_council(prompt, context="local-business competitive differentiation analysis")


def list_councils() -> dict:
    """List available councils and their framework labels."""
    return {
        "ok": True,
        "councils": [
            {"name": name, "framework": cfg["framework"], "model": cfg["model"]}
            for name, cfg in COUNCILS.items()
        ],
    }


def multi_council(
    prompt: str,
    context: str = "",
    councils: Optional[list] = None,
) -> dict:
    """Run multiple councils sequentially, then synthesize.

    Default councils = [strategy, risk, market, operations, ethics] —
    the core board for venture/business decisions.
    """
    selected = councils or ["strategy", "risk", "market", "operations", "ethics"]
    selected = [c for c in selected if c in COUNCILS]
    if not selected:
        return {"ok": False, "error": "no valid councils selected"}

    results = []
    total_cost = 0.0
    for name in selected:
        result = _run_council(name, prompt, context)
        results.append(result)
        total_cost += result.get("cost_usd", 0.0)

    # Tally recommendations
    recs = [r.get("recommendation", "iterate") for r in results if r.get("ok")]
    rec_counts = {r: recs.count(r) for r in set(recs)}
    consensus = max(rec_counts, key=rec_counts.get) if rec_counts else "iterate"
    avg_confidence = (
        sum(r.get("confidence", 0) for r in results if r.get("ok"))
        / max(1, sum(1 for r in results if r.get("ok")))
    )

    # Compile findings + concerns
    all_findings = []
    all_concerns = []
    for r in results:
        if not r.get("ok"):
            continue
        for f in r.get("key_findings", []):
            all_findings.append(f"[{r['council']}] {f}")
        for c in r.get("risks_or_concerns", []):
            all_concerns.append(f"[{r['council']}] {c}")

    return {
        "ok": True,
        "prompt": prompt[:500],
        "councils_run": selected,
        "results": results,
        "synthesis": {
            "consensus_recommendation": consensus,
            "recommendation_breakdown": rec_counts,
            "average_confidence": round(avg_confidence, 1),
            "all_findings": all_findings,
            "all_concerns": all_concerns,
        },
        "total_cost_usd": round(total_cost, 4),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


# --- registration ----------------------------------------------------------

ACTION_TABLE = {
    "strategy_council":       strategy_council,
    "content_council":        content_council,
    "risk_council":           risk_council,
    "market_council":         market_council,
    "operations_council":     operations_council,
    "ai_engineering_council": ai_engineering_council,
    "forecasting_council":    forecasting_council,
    "execution_council":      execution_council,
    "ethics_council":         ethics_council,
    "multi_council":          multi_council,
    "list_councils":          list_councils,
}


def get_actions() -> dict:
    return ACTION_TABLE


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Usage:")
        print("  python3 business_mind_tree.py list")
        print("  python3 business_mind_tree.py <council> '<prompt>'")
        print("  python3 business_mind_tree.py multi '<prompt>' [council1,council2,...]")
        print()
        print("Councils: strategy, risk, market, operations, ai_engineering,")
        print("          forecasting, execution, ethics")
        sys.exit(0)

    if sys.argv[1] == "list":
        print(json.dumps(list_councils(), indent=2))
    elif sys.argv[1] == "multi" and len(sys.argv) >= 3:
        prompt = sys.argv[2]
        councils = sys.argv[3].split(",") if len(sys.argv) > 3 else None
        print(json.dumps(multi_council(prompt, councils=councils), indent=2))
    elif sys.argv[1] in COUNCILS and len(sys.argv) >= 3:
        print(json.dumps(_run_council(sys.argv[1], sys.argv[2]), indent=2))
    else:
        print(f"unknown command: {sys.argv[1]}")
        sys.exit(1)
