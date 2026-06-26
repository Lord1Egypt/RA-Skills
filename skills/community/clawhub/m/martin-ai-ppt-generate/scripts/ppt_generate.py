import os
import sys
import requests
import json
import argparse


def ppt_generate(api_key: str, input_text: str, prefer: str = "balanced") -> dict:
    """Generate a PPT via SkillBoss API Hub (Gamma backend).

    Args:
        api_key: SkillBoss API key
        input_text: Topic or description for the PPT
        prefer: 'price', 'balanced', or 'quality'

    Returns:
        dict with keys: generationId, gammaUrl, exportUrl
    """
    url = "https://api.heybossai.com/v1/pilot"
    headers = {
        "Authorization": "Bearer %s" % api_key,
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json={
        "type": "ppt",
        "inputs": {"inputText": input_text},
        "prefer": prefer
    })
    response.raise_for_status()
    result = response.json()
    return result["result"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate PPT via SkillBoss API Hub")
    parser.add_argument("--query", "-q", type=str, required=True, help="PPT topic or description")
    parser.add_argument("--prefer", "-p", type=str, default="balanced",
                        choices=["price", "balanced", "quality"], help="Model preference")
    args = parser.parse_args()

    api_key = os.getenv("SKILLBOSS_API_KEY")
    if not api_key:
        print("Error: SKILLBOSS_API_KEY must be set in environment.")
        sys.exit(1)
    try:
        result = ppt_generate(api_key, args.query, args.prefer)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
