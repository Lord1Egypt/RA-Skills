import argparse
from mss_client import api_get


def search(query):
    data = api_get("/targets/search", params={"q": query})
    results = data.get("results", [])

    if not results:
        print(f"No targets found matching: {query}")
        return

    print(f"Found {len(results)} target(s):\n")
    for t in results:
        print(f"  [{t['id']}] Type: {t['type']} | Status: {t['status']} | Grid: {t['grid']} | Threat: {t['threat_level']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    args = parser.parse_args()
    search(args.query)
