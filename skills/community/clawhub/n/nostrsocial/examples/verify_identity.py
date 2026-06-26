"""Identity verification flow for contacts."""

from nostrsocial import SocialEnclave, Tier

def main():
    enclave = SocialEnclave.create()

    # Add a contact with just an email (proxy identity)
    enclave.add("alice@example.com", "email", Tier.CLOSE, display_name="Alice")

    # Check who needs upgrading
    print("Contacts that would benefit from npub verification:")
    for contact in enclave.get_upgradeable():
        print(f"  {contact.display_name} ({contact.identity_state.value}): {contact.upgrade_hint}")

    # Alice provides her npub — add with claimed identity
    enclave.remove("alice@example.com", "email")
    enclave.add(
        "alice@example.com", "email", Tier.CLOSE,
        display_name="Alice",
        claimed_npub="npub1aliceexamplepubkey",
    )

    # Create a verification challenge
    challenge = enclave.create_challenge("npub1aliceexamplepubkey")
    print(f"\nChallenge created for Alice:")
    print(f"  Nonce: {challenge.nonce}")
    print(f"  Expires: {challenge.expires_at}")
    print(f"  Ask Alice to sign this nonce with her nsec")

    # Full verification via relay ships in 0.2.0
    try:
        enclave.verify(challenge, "fake_signature")
    except NotImplementedError as e:
        print(f"\n  (Expected) {e}")


if __name__ == "__main__":
    main()
