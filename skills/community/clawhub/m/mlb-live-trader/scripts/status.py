#!/usr/bin/env python3
"""Show the Simmer portfolio and open MLB positions without trading."""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import asdict, is_dataclass
from typing import Any, Protocol


class ClientFactory(Protocol):
    """Construct the narrow Simmer client needed by the status view."""

    def __call__(self, *, api_key: str, venue: str, live: bool) -> Any:
        """Return a configured Simmer client."""


class StatusViewer:
    """Render a read-only portfolio summary through injected adapters."""

    def __init__(
        self,
        *,
        client_factory: ClientFactory,
        environment: Mapping[str, str],
        output: Callable[[str], None],
        error: Callable[[str], None],
    ) -> None:
        """Initialize the status service.

        Args:
            client_factory: Simmer client constructor or deterministic fake.
            environment: Read-only environment mapping.
            output: Standard-output line writer.
            error: Standard-error line writer.
        """
        self._client_factory = client_factory
        self._environment = environment
        self._output = output
        self._error = error

    def run(self) -> int:
        """Fetch and render current portfolio state.

        Returns:
            Process-style status code. The method never places or changes an
            order.
        """
        api_key = self._environment.get("SIMMER_API_KEY")
        if not api_key:
            self._error("SIMMER_API_KEY is not set")
            return 1

        client = self._client_factory(
            api_key=api_key,
            venue=self._environment.get("TRADING_VENUE", "polymarket"),
            live=False,
        )
        try:
            portfolio = client.get_portfolio()
            positions = client.get_positions(venue=client.venue)
        except Exception as exc:
            self._error(f"Could not fetch portfolio: {exc}")
            return 1

        balance = (
            portfolio.get("balance_usdc", 0) if isinstance(portfolio, Mapping) else 0
        )
        self._output(f"Available balance: ${float(balance):.2f}")
        if not positions:
            self._output("No open positions.")
            return 0

        for position in positions:
            if not is_dataclass(position) or isinstance(position, type):
                self._error("Simmer returned a non-dataclass position")
                return 1
            values = asdict(position)
            title = (
                values.get("question") or values.get("market_id") or "unknown market"
            )
            legs = [
                self._render_leg(label, values.get(field, 0))
                for label, field in (("YES", "shares_yes"), ("NO", "shares_no"))
                if values.get(field, 0) != 0
            ]
            rendered_legs = ", ".join(legs) if legs else "no shares"
            self._output(f"{title}: {rendered_legs}")
        return 0

    @staticmethod
    def _render_leg(label: str, shares: object) -> str:
        """Render one nonzero SDK position leg without losing precision."""
        rendered_shares = (
            f"{shares:g}" if isinstance(shares, (int, float)) else str(shares)
        )
        return f"{label} {rendered_shares} shares"


def main(argv: Sequence[str] | None = None) -> int:
    """Run the read-only status command.

    Args:
        argv: Optional CLI arguments for deterministic callers.

    Returns:
        Process exit status.
    """
    parser = argparse.ArgumentParser(
        description="Show Simmer positions for the MLB live trader."
    )
    parser.parse_args(argv)
    try:
        from simmer_sdk import SimmerClient
    except ImportError:
        print("simmer-sdk is not installed", file=sys.stderr)
        return 1

    return StatusViewer(
        client_factory=SimmerClient.readonly,
        environment=os.environ,
        output=print,
        error=lambda message: print(message, file=sys.stderr),
    ).run()


if __name__ == "__main__":
    raise SystemExit(main())
