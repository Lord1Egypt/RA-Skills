"""Manage contacts in a social graph."""

from nostrsocial import SocialEnclave, Tier

def main():
    # Create a social graph
    enclave = SocialEnclave.create()

    # Add friends at different trust tiers
    enclave.add("alice@example.com", "email", Tier.INTIMATE, display_name="Alice")
    enclave.add("bob@example.com", "email", Tier.CLOSE, display_name="Bob")
    enclave.add("carol@example.com", "email", Tier.FAMILIAR, display_name="Carol")
    enclave.add("dave@example.com", "email", Tier.KNOWN, display_name="Dave")

    # Block someone
    enclave.block("spam@bad.com", "email", notes="Persistent spam")

    # Gray-zone someone
    enclave.gray("meh@example.com", "email", notes="Met once, not sure")

    # Check remaining slots
    print("Slots remaining:")
    for list_name, count in enclave.slots_remaining.items():
        print(f"  {list_name}: {count}")

    # Promote someone
    enclave.promote("dave@example.com", "email", Tier.FAMILIAR)
    print("\nDave promoted to familiar tier")

    # Check behavior for each contact
    for name, email in [("Alice", "alice@example.com"), ("Bob", "bob@example.com"),
                         ("Spam", "spam@bad.com"), ("Stranger", "unknown@example.com")]:
        rules = enclave.get_behavior(email, "email")
        print(f"\n{name}: warmth={rules.warmth}, budget={rules.token_budget}, "
              f"interrupt={rules.can_interrupt}")


if __name__ == "__main__":
    main()
