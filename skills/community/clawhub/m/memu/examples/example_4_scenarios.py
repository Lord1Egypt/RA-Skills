"""
Example 4: Real-World Scenario Code
====================================
Three use-case demonstrations:
  A) Research assistant — learns user preferences from interactions
  B) Email triage — learns priority patterns over time
  C) System monitoring — learns normal vs. anomalous patterns

Each scenario is self-contained. Run any one individually.

Requirements:
    pip install memu-py
    export OPENAI_API_KEY=sk-your-key

Usage:
    python example_4_scenarios.py
"""

import asyncio
import os
from memu import MemoryService


def get_service() -> MemoryService:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("Set OPENAI_API_KEY environment variable.")
    return MemoryService(
        llm_profiles={
            "default": {
                "provider": "openai",
                "base_url": "https://api.openai.com/v1",
                "api_key": api_key,
                "chat_model": "gpt-4o-mini",
                "embed_model": "text-embedding-3-small",
            }
        }
    )


# ─── Scenario A: Research Assistant ───────────────────────────

async def research_assistant():
    """
    The agent learns which papers the user finds interesting,
    then proactively suggests relevant new papers.
    """
    service = get_service()
    print("=== Scenario A: Research Assistant ===\n")

    # Week 1: User discusses papers with the agent
    await service.memorize(
        resource_payload=[
            {"role": "user", "content": "This paper on coral reef adaptation in Southeast Asia is exactly what I needed."},
            {"role": "assistant", "content": "I see you're focused on adaptation strategies in tropical regions."},
            {"role": "user", "content": "Yes, especially mixed-methods studies. Pure modeling papers are too abstract for my thesis."},
            {"role": "assistant", "content": "Noted: you prefer mixed-methods over pure modeling approaches."},
        ],
        modality="conversation",
        user={"user_id": "researcher-01"},
    )

    # Week 2: User asks for reading suggestions
    memories = await service.retrieve(
        query=[{"role": "user", "content": "Find me something new to read on climate adaptation."}],
        method="embedding",
    )

    print("Retrieved preferences for paper recommendation:")
    for m in memories:
        print(f"  [{m.category}] {m.content}")
    print()


# ─── Scenario B: Email Triage ─────────────────────────────────

async def email_triage():
    """
    The agent learns which emails the user considers urgent
    and builds a priority model over time.
    """
    service = get_service()
    print("=== Scenario B: Email Triage ===\n")

    # Teach the agent priority patterns
    await service.memorize(
        resource_payload=[
            {"role": "user", "content": "Emails from the CEO are always top priority, even if they look casual."},
            {"role": "assistant", "content": "Understood — CEO emails get highest priority regardless of tone."},
            {"role": "user", "content": "Marketing newsletters can wait. I check those on Fridays."},
            {"role": "assistant", "content": "Got it, marketing newsletters are low priority, reviewed on Fridays."},
            {"role": "user", "content": "Anything with 'incident' or 'outage' in the subject is urgent."},
            {"role": "assistant", "content": "Flagging emails with incident/outage keywords as urgent."},
        ],
        modality="conversation",
        user={"user_id": "exec-01"},
    )

    # New email arrives — retrieve priority rules
    memories = await service.retrieve(
        query=[{"role": "user", "content": "I got an email from marketing about Q2 campaigns. How urgent is this?"}],
        method="embedding",
    )

    print("Retrieved priority rules:")
    for m in memories:
        print(f"  [{m.category}] {m.content}")
    print()


# ─── Scenario C: System Monitoring ────────────────────────────

async def system_monitoring():
    """
    The agent learns which system events are normal and which
    require human intervention, reducing false alerts.
    """
    service = get_service()
    print("=== Scenario C: System Monitoring ===\n")

    # Train with annotated system events
    await service.memorize(
        resource_payload=[
            {"role": "user", "content": "The CPU spike on auth-service every Sunday at 2am is the backup job. Ignore it."},
            {"role": "assistant", "content": "Noted: Sunday 2am CPU spikes on auth-service are expected (backup job)."},
            {"role": "user", "content": "Memory usage above 85% on payment-service IS a problem. Page me immediately."},
            {"role": "assistant", "content": "Payment-service memory >85% triggers immediate page."},
            {"role": "user", "content": "The 5xx error rate on api-gateway sometimes spikes during deploys. If it lasts <5min, it's normal."},
            {"role": "assistant", "content": "api-gateway 5xx spikes under 5 minutes during deploys are expected."},
        ],
        modality="conversation",
        user={"user_id": "sre-01"},
    )

    # New alert: should the agent escalate?
    memories = await service.retrieve(
        query=[{"role": "user", "content": "auth-service CPU at 92% right now, it's Sunday 2:15am."}],
        method="embedding",
    )

    print("Retrieved alert context:")
    for m in memories:
        print(f"  [{m.category}] {m.content}")
    print("  → Agent decision: Suppress alert (matches known backup job pattern)")
    print()


async def main():
    await research_assistant()
    await email_triage()
    await system_monitoring()


if __name__ == "__main__":
    asyncio.run(main())
