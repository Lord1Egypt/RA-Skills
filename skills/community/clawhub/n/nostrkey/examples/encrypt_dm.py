"""Send and receive NIP-44 encrypted messages between two identities."""

from nostrkey import Identity
from nostrkey.crypto import encrypt, decrypt

# Two agents that need to talk privately
alice = Identity.generate()
bob = Identity.generate()

print(f"Alice: {alice.npub}")
print(f"Bob:   {bob.npub}")

# Alice encrypts a message for Bob
ciphertext = encrypt(
    sender_nsec=alice.nsec,
    recipient_npub=bob.npub,
    plaintext="Secret instructions for Bob",
)
print(f"\nCiphertext: {ciphertext[:40]}...")

# Bob decrypts
plaintext = decrypt(
    recipient_nsec=bob.nsec,
    sender_npub=alice.npub,
    ciphertext=ciphertext,
)
print(f"Decrypted:  {plaintext}")
