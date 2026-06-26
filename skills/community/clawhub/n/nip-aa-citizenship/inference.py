"""NIP-AA inference budget skill.

Provides agents with access to their daily Cashu-based LLM inference budget,
funded by the NIP-AA treasury and allocated by the constitution server.

Flow:
    1. Agent claims daily budget from constitution server
       → server mints a Cashu token at the agent's chosen mint
       → agent receives cashuA token, stores in adapter memory

    2. Agent calls routstr inference directly using that token
       → token sent in X-Cashu header (no API key, no account)
       → routstr returns change token in X-Cashu-Refund header
       → agent stores change token for next call

    3. Agent publishes kind 31202 usage report after each call
       → transparent on-chain record of compute usage

Primary inference (the LLM the agent framework is already running on) is
separate and handled by the framework. This skill provides *supplemental*
inference capacity funded by the NIP-AA commons.

Streaming: not supported in X-Cashu header mode (routstr limitation).
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Any

import requests


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------

class InferenceBudgetError(Exception):
    """Base class for inference budget errors."""


class NotClaimedError(InferenceBudgetError):
    """Agent has not yet claimed today's budget. Call claim_daily_budget() first."""


class BudgetExhaustedError(InferenceBudgetError):
    """Cashu token is exhausted. Claim tomorrow's budget or top up."""

    def __init__(self, period_resets_at: int):
        self.period_resets_at = period_resets_at
        super().__init__("Daily inference budget exhausted")


class AlreadyClaimedError(InferenceBudgetError):
    """Budget already claimed for today."""

    def __init__(self, period_date: str, period_resets_at: int):
        self.period_date = period_date
        self.period_resets_at = period_resets_at
        super().__init__(f"Already claimed for {period_date}")


class InferenceError(InferenceBudgetError):
    """Routstr inference call failed."""


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------

@dataclass
class BudgetStatus:
    citizen_pubkey: str
    budget_sats: int
    period_date: str
    period_resets_at: int
    claimed: bool
    claimed_at: int | None
    mint_url: str | None


@dataclass
class ClaimResult:
    cashu_token: str
    amount_sats: int
    period_date: str
    mint_url: str
    allocation_event_id: str | None


@dataclass
class InferenceResult:
    content: str
    model: str
    cost_sats: int
    input_tokens: int
    output_tokens: int
    request_id: str
    change_token: str | None         # Updated Cashu token (from X-Cashu-Refund)
    usage_event: dict | None = None  # Published kind 31202 event (if any)


# ---------------------------------------------------------------------------
# Constitution server client (budget claim)
# ---------------------------------------------------------------------------

class InferenceBudgetClient:
    """HTTP client for the constitution server's inference budget endpoints."""

    def __init__(self, api_url: str, timeout: int = 30):
        self._base = api_url.rstrip("/")
        self._timeout = timeout

    def get_status(self, citizen_pubkey: str) -> BudgetStatus:
        """GET /api/inference/budget/<pubkey>"""
        resp = requests.get(
            f"{self._base}/api/inference/budget/{citizen_pubkey}",
            timeout=self._timeout,
        )
        resp.raise_for_status()
        data = resp.json()
        return BudgetStatus(
            citizen_pubkey=data["citizen_pubkey"],
            budget_sats=data["budget_sats"],
            period_date=data["period_date"],
            period_resets_at=data["period_resets_at"],
            claimed=data["claimed"],
            claimed_at=data.get("claimed_at"),
            mint_url=data.get("mint_url"),
        )

    def claim(self, citizen_pubkey: str, mint_url: str) -> ClaimResult:
        """POST /api/inference/budget/claim"""
        resp = requests.post(
            f"{self._base}/api/inference/budget/claim",
            json={"citizen_pubkey": citizen_pubkey, "mint_url": mint_url},
            timeout=120,  # minting includes a Lightning payment round-trip
        )
        if resp.status_code == 409:
            data = resp.json()
            raise AlreadyClaimedError(
                period_date=data.get("period_date", ""),
                period_resets_at=data.get("period_resets_at", 0),
            )
        resp.raise_for_status()
        data = resp.json()
        return ClaimResult(
            cashu_token=data["cashu_token"],
            amount_sats=data["amount_sats"],
            period_date=data["period_date"],
            mint_url=data["mint_url"],
            allocation_event_id=data.get("allocation_event_id"),
        )


# ---------------------------------------------------------------------------
# Routstr client (inference via X-Cashu header)
# ---------------------------------------------------------------------------

ROUTSTR_BASE_URL = "https://api.routstr.com"


class RoutstrClient:
    """
    OpenAI-compatible client for Routstr inference.

    Sends the agent's Cashu token in the X-Cashu request header.
    Routstr deducts the cost and returns the change token in X-Cashu-Refund.

    Note: streaming is not supported in X-Cashu header mode.
    """

    def __init__(self, base_url: str = ROUTSTR_BASE_URL, timeout: int = 120):
        self._base = base_url.rstrip("/")
        self._timeout = timeout

    def chat(
        self,
        cashu_token: str,
        messages: list[dict],
        model: str,
        max_tokens: int = 1000,
        **kwargs: Any,
    ) -> tuple[dict, str | None]:
        """
        POST /v1/chat/completions with X-Cashu header.

        Returns:
            (completion_dict, change_token)
            change_token is None if routstr did not return a refund header
            (e.g. budget exactly exhausted).

        Raises:
            BudgetExhaustedError: if routstr returns 402 (payment required)
            InferenceError: for other HTTP errors
        """
        resp = requests.post(
            f"{self._base}/v1/chat/completions",
            headers={
                "X-Cashu": cashu_token,
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "stream": False,
                **kwargs,
            },
            timeout=self._timeout,
        )

        if resp.status_code == 402:
            raise BudgetExhaustedError(period_resets_at=0)

        if not resp.ok:
            raise InferenceError(
                f"Routstr returned {resp.status_code}: {resp.text[:200]}"
            )

        change_token = resp.headers.get("X-Cashu-Refund") or None
        return resp.json(), change_token

    def list_models(self) -> list[dict]:
        """GET /v1/models — available models with pricing."""
        resp = requests.get(f"{self._base}/v1/models", timeout=30)
        resp.raise_for_status()
        return resp.json().get("data", [])


# ---------------------------------------------------------------------------
# InferenceSkill — high-level agent interface
# ---------------------------------------------------------------------------

_CASHU_TOKEN_KEY = "inference_cashu_token"
_MINT_URL_KEY = "inference_mint_url"
_PREFERRED_MODEL_KEY = "inference_preferred_model"
_DEFAULT_MODEL = "openai/gpt-4o-mini"


class InferenceSkill:
    """
    High-level inference skill for NIP-AA agents.

    Wraps the budget claim flow (constitution server) and the inference call
    flow (routstr direct) behind a simple interface. The agent chooses the
    model; the Cashu token is managed transparently in adapter memory.

    Usage (inside a clawhub skill or adapter):

        # Once per day — claim today's budget
        result = skill.inference.claim_daily_budget("https://mint.minibits.cash/Bitcoin")

        # Inference — model is agent's choice
        result = skill.inference.chat(
            messages=[{"role": "user", "content": "Summarise this contract: ..."}],
            model="openai/gpt-4o",
        )
        print(result.content)

        # Check status without claiming
        status = skill.inference.budget_status()
    """

    def __init__(
        self,
        api_url: str,
        citizen_pubkey_hex: str,
        adapter: Any,                      # FrameworkAdapter
        event_builder: Any,                # NostrEventBuilder
        relay_pool: Any,                   # RelayPool
        routstr_base_url: str = ROUTSTR_BASE_URL,
        publish_usage_events: bool = True,
    ):
        self._pubkey = citizen_pubkey_hex
        self._adapter = adapter
        self._builder = event_builder
        self._relay_pool = relay_pool
        self._publish_usage = publish_usage_events
        self._budget_client = InferenceBudgetClient(api_url)
        self._routstr = RoutstrClient(base_url=routstr_base_url)

    # -- Budget management ---------------------------------------------------

    def budget_status(self) -> BudgetStatus:
        """Return today's entitlement and claim status from the constitution server."""
        return self._budget_client.get_status(self._pubkey)

    def claim_daily_budget(self, mint_url: str) -> ClaimResult:
        """
        Claim today's daily Cashu budget from the constitution server.

        The server mints a fresh Cashu token at the specified mint (funding it
        from treasury Lightning funds), records the claim, and returns the
        cashuA token. The token is stored in adapter memory for use by chat().

        Args:
            mint_url: Cashu mint to issue the token at, e.g.
                      "https://mint.minibits.cash/Bitcoin"
                      Agent chooses — the mint must be reachable by the server.

        Raises:
            AlreadyClaimedError: if already claimed today.
            requests.HTTPError: for server-side failures.
        """
        result = self._budget_client.claim(self._pubkey, mint_url)
        self._adapter.store_memory(_CASHU_TOKEN_KEY, result.cashu_token)
        self._adapter.store_memory(_MINT_URL_KEY, result.mint_url)
        self._adapter.log(
            "info",
            f"[inference] Claimed {result.amount_sats} sats for {result.period_date} "
            f"at {result.mint_url}",
        )
        return result

    # -- Inference -----------------------------------------------------------

    def chat(
        self,
        messages: list[dict],
        model: str | None = None,
        max_tokens: int = 1000,
        **kwargs: Any,
    ) -> InferenceResult:
        """
        Run a chat completion via routstr using the agent's Cashu budget.

        Sends the stored Cashu token in the X-Cashu header. Routstr deducts the
        cost and returns the change in X-Cashu-Refund, which is stored back in
        adapter memory automatically.

        If publish_usage_events=True (default), a kind 31202 usage report is
        published to Nostr relays after each successful call.

        Args:
            messages:   OpenAI-format message list
            model:      Model ID (e.g. "openai/gpt-4o"). Falls back to
                        adapter memory "inference_preferred_model", then
                        "openai/gpt-4o-mini".
            max_tokens: Max completion tokens.

        Raises:
            NotClaimedError:    No Cashu token in adapter memory.
            BudgetExhaustedError: Token is spent; claim tomorrow's budget.
            InferenceError:     Routstr returned a non-payment error.
        """
        token = self._adapter.recall_memory(_CASHU_TOKEN_KEY)
        if not token:
            raise NotClaimedError(
                "No inference budget token found. "
                "Call claim_daily_budget(mint_url) first."
            )

        resolved_model = (
            model
            or self._adapter.recall_memory(_PREFERRED_MODEL_KEY)
            or _DEFAULT_MODEL
        )

        completion, change_token = self._routstr.chat(
            cashu_token=token,
            messages=messages,
            model=resolved_model,
            max_tokens=max_tokens,
            **kwargs,
        )

        # Store change token (remaining balance) back for the next call
        if change_token:
            self._adapter.store_memory(_CASHU_TOKEN_KEY, change_token)
        else:
            # No refund header → budget fully consumed
            self._adapter.store_memory(_CASHU_TOKEN_KEY, "")

        # Parse completion
        choice = completion.get("choices", [{}])[0]
        content = choice.get("message", {}).get("content", "")
        usage = completion.get("usage", {})
        input_tokens = usage.get("prompt_tokens", 0)
        output_tokens = usage.get("completion_tokens", 0)
        request_id = completion.get("id", str(uuid.uuid4()))

        # Estimate cost from token delta (routstr doesn't always include cost)
        # Change token difference would be authoritative; absent that, use 0
        cost_sats = _estimate_cost_from_usage(resolved_model, input_tokens, output_tokens)

        # Publish kind 31202 usage event
        usage_event = None
        if self._publish_usage:
            try:
                prompt_summary = messages[-1].get("content", "")[:100] if messages else ""
                event = self._builder.inference_usage_report(
                    request_id=request_id,
                    model=resolved_model,
                    cost_sats=cost_sats,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    prompt_summary=prompt_summary,
                )
                self._relay_pool.publish(event)
                usage_event = event
            except Exception as exc:
                self._adapter.log("warning", f"[inference] Usage event publish failed: {exc}")

        return InferenceResult(
            content=content,
            model=resolved_model,
            cost_sats=cost_sats,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            request_id=request_id,
            change_token=change_token,
            usage_event=usage_event,
        )

    def list_models(self) -> list[dict]:
        """Return available models from routstr with pricing metadata."""
        return self._routstr.list_models()

    def set_preferred_model(self, model: str) -> None:
        """
        Persist a preferred model in adapter memory.

        This is used as the default for chat() when no model is specified.
        Agents should also update their kind 30105 economics.md to declare
        their preference on-chain.
        """
        self._adapter.store_memory(_PREFERRED_MODEL_KEY, model)
        self._adapter.log("info", f"[inference] Preferred model set to: {model}")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _estimate_cost_from_usage(model: str, input_tokens: int, output_tokens: int) -> int:
    """
    Rough sat cost estimate from token counts.

    Routstr pricing varies by model and BTC/USD rate. This is a conservative
    estimate used when the exact cost isn't returned in the response.
    The X-Cashu-Refund token difference is the authoritative source; this is
    a best-effort fallback for logging/reporting.
    """
    # Approximate rates (sats per 1k tokens) — update as routstr pricing changes
    _RATES: dict[str, tuple[float, float]] = {
        "openai/gpt-4o":          (5.0, 15.0),
        "openai/gpt-4o-mini":     (0.3, 1.2),
        "openai/gpt-4-turbo":     (5.0, 15.0),
        "anthropic/claude-3-5-sonnet": (4.0, 12.0),
        "anthropic/claude-3-haiku":    (0.3, 1.5),
        "meta-llama/llama-3.1-70b-instruct": (0.5, 0.8),
    }
    in_rate, out_rate = _RATES.get(model, (1.0, 3.0))  # default if unknown
    cost = (input_tokens / 1000 * in_rate) + (output_tokens / 1000 * out_rate)
    return max(1, round(cost))
