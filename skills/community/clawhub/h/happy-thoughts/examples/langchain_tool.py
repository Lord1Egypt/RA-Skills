"""
Happy Thoughts — LangChain Tool Integration

This example wraps the live Happy Thoughts API as LangChain tools.
Note: real paid `/think` calls require x402 payment handling or an
internal owner bypass header that should never be hardcoded publicly.
"""

import requests
from langchain.tools import tool

HAPPY_THOUGHTS_URL = "https://happythoughts.proteeninjector.workers.dev"


@tool
def discover_providers(specialty: str = "") -> str:
    """Browse available Happy Thoughts providers."""
    url = f"{HAPPY_THOUGHTS_URL}/discover"
    if specialty:
        url += f"?specialty={specialty}"
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return response.text


@tool
def preview_route(specialty: str = "") -> str:
    """Preview the top routed providers without paying."""
    url = f"{HAPPY_THOUGHTS_URL}/route"
    if specialty:
        url += f"?specialty={specialty}"
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return response.text


@tool
def get_provider_score(provider_id: str) -> str:
    """Get the full public score breakdown for a provider."""
    response = requests.get(f"{HAPPY_THOUGHTS_URL}/score/{provider_id}", timeout=15)
    response.raise_for_status()
    return response.text


if __name__ == "__main__":
    print(discover_providers.invoke({"specialty": "trading"}))
    print(preview_route.invoke({"specialty": "trading/signals"}))
    print(get_provider_score.invoke({"provider_id": "founding-pi-signals"}))
