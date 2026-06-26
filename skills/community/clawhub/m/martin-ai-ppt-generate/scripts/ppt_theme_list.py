import os
import sys
import requests
import json


def ppt_generate(api_key: str, input_text: str):
    """Generate a PPT via SkillBoss API Hub (Gamma backend).

    The Gamma API takes inputText and returns generationId, gammaUrl, exportUrl.
    Note: The original 'get_themes' action is not supported by the Gamma API.
    Use this function to generate a PPT instead.
    """
    url = "https://api.heybossai.com/v1/pilot"
    headers = {
        "Authorization": "Bearer %s" % api_key,
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json={
        "type": "ppt",
        "inputs": {"inputText": input_text},
        "prefer": "balanced"
    })
    response.raise_for_status()
    result = response.json()
    return result["result"]


if __name__ == "__main__":
    api_key = os.getenv("SKILLBOSS_API_KEY")
    if not api_key:
        print("Error: SKILLBOSS_API_KEY must be set in environment.")
        sys.exit(1)
    topic = sys.argv[1] if len(sys.argv) > 1 else "Introduction to Artificial Intelligence"
    try:
        result = ppt_generate(api_key, topic)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
