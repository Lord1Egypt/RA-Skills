#!/usr/bin/env python3
"""Optional LangChain + Jev patterns.

Install the official integration before importing this example:

    python -m pip install "langchain-typesafe[experimental]"

This file intentionally does not execute a model call by itself. Import the
functions into an application and supply the model/tool implementations that
match that application's policy.
"""

from __future__ import annotations

from typing import Any

from langchain.agents import create_agent
from langchain_typesafe import Choice, Noul, Score, TypeSafeClassifier
from langchain_typesafe.experimental.middleware import (
    AutoModeMiddleware,
    ModelChoice,
    ModelRouterMiddleware,
)


def classify_ticket(state: Any) -> dict[str, Any]:
    """Return typed routing signals for a ticket or agent state."""
    response = TypeSafeClassifier(model="jev-latest").invoke(
        {
            "state": state,
            "questions": {
                "urgent": Noul(
                    instructions="Does this request need immediate attention?"
                ),
                "team": Choice(
                    instructions="Which team should handle this request?",
                    criteria={
                        "technical": "Bugs, outages, or integration failures.",
                        "billing": "Charges, refunds, or subscriptions.",
                        "other": "None of the listed teams fits.",
                    },
                ),
                "severity": Score(
                    instructions="How severe is the user impact?",
                    criteria=["Minor", "Material", "Critical"],
                ),
            },
        }
    )
    return {
        "urgent_probability": response.nouls["urgent"].noul,
        "team": response.choices["team"].choice,
        "team_confidence": response.choices["team"].confidence,
        "severity": response.scores["severity"].score,
    }


def build_agent(
    *,
    default_model: str,
    fast_model: str,
    strong_model: str,
    tools: list[Any],
    guarded_tools: list[str],
) -> Any:
    """Build a routed agent with an explicit pre-tool risk gate.

    The model strings are passed to LangChain's provider registry. The guard
    advises on risk; application code must still enforce authorization,
    allowlists, and irreversible-action policy.
    """
    router = ModelRouterMiddleware(
        choices={
            "fast": ModelChoice(
                model=fast_model,
                criteria="Simple lookups, extraction, and localized changes.",
            ),
            "strong": ModelChoice(
                model=strong_model,
                criteria="Complex debugging, architecture, or high-impact work.",
            ),
        },
        instructions="Choose the least costly model that can safely complete the task.",
    )
    guard = AutoModeMiddleware(tools=guarded_tools)
    return create_agent(
        default_model,
        tools=tools,
        middleware=[router, guard],
    )


if __name__ == "__main__":
    print("Import classify_ticket() or build_agent() from this optional example.")
