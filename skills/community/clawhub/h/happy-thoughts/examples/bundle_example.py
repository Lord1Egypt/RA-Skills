"""
Happy Thoughts — bundle example

The live `/bundle` endpoint currently purchases prepaid bundles such as
starter, builder, pro, and whale. It does not accept an array of prompts.
"""

import requests

BASE = "https://happythoughts.proteeninjector.workers.dev"


def purchase_bundle(tier: str, buyer_wallet: str, locked_specialty: str | None = None):
    payload = {
        "tier": tier,
        "buyer_wallet": buyer_wallet,
    }
    if locked_specialty:
        payload["locked_specialty"] = locked_specialty

    response = requests.post(f"{BASE}/bundle", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    print("This call will require x402 payment handling in a real client.")
    print(
        purchase_bundle(
            tier="starter",
            buyer_wallet="0xYOURWALLET",
            locked_specialty="trading",
        )
    )
