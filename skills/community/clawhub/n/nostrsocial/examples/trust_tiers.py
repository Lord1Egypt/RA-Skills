"""Explore trust tier behavioral rules."""

from nostrsocial import Tier
from nostrsocial.behavior import TIER_BEHAVIORS, BLOCK_BEHAVIOR, GRAY_BEHAVIOR, NEUTRAL_BEHAVIOR


def main():
    print("Trust Tier Behaviors")
    print("=" * 70)

    for tier in Tier:
        rules = TIER_BEHAVIORS[tier]
        print(f"\n{tier.value.upper()} (capacity: {tier.name})")
        print(f"  Token budget:    {rules.token_budget}")
        print(f"  Memory depth:    {rules.memory_depth}")
        print(f"  Warmth:          {rules.warmth}")
        print(f"  Can interrupt:   {rules.can_interrupt}")
        print(f"  Response priority: {rules.response_priority}")
        print(f"  Share context:   {rules.share_context}")
        print(f"  Proactive:       {rules.proactive_contact}")

    print(f"\nBLOCK: warmth={BLOCK_BEHAVIOR.warmth}, budget={BLOCK_BEHAVIOR.token_budget}")
    print(f"GRAY:  warmth={GRAY_BEHAVIOR.warmth}, budget={GRAY_BEHAVIOR.token_budget}")
    print(f"NEUTRAL: warmth={NEUTRAL_BEHAVIOR.warmth}, budget={NEUTRAL_BEHAVIOR.token_budget}")


if __name__ == "__main__":
    main()
