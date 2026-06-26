import os
import sys
import requests
import json
import argparse


def ppt_outline_generate(api_key: str, query: str, language: str = "en") -> dict:
    """Generate a PPT outline via SkillBoss API Hub chat, then generate PPT.

    The Gamma PPT API takes inputText directly; for outline-first workflow,
    first use chat to generate an outline, then pass it to the PPT endpoint.

    Args:
        api_key: SkillBoss API key
        query: PPT topic or content description
        language: 'en' or 'zh'

    Returns:
        dict with keys: generationId, gammaUrl, exportUrl
    """
    url = "https://api.heybossai.com/v1/pilot"
    headers = {
        "Authorization": "Bearer %s" % api_key,
        "Content-Type": "application/json"
    }

    lang_instruction = "in Chinese" if language == "zh" else "in English"

    # Step 1: Generate outline using chat
    chat_response = requests.post(url, headers=headers, json={
        "type": "chat",
        "inputs": {
            "messages": [{"role": "user", "content": f"Create a detailed PPT outline {lang_instruction} for: {query}. Include slide titles and key points."}]
        },
        "prefer": "balanced"
    })
    chat_response.raise_for_status()
    chat_result = chat_response.json()
    outline = chat_result["result"]["choices"][0]["message"]["content"]

    # Step 2: Generate PPT from outline
    ppt_input = f"{query}\n\nOutline:\n{outline}"
    ppt_response = requests.post(url, headers=headers, json={
        "type": "ppt",
        "inputs": {"inputText": ppt_input},
        "prefer": "balanced"
    })
    ppt_response.raise_for_status()
    ppt_result = ppt_response.json()
    return ppt_result["result"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate PPT with outline step via SkillBoss API Hub")
    parser.add_argument("--query", "-q", type=str, required=True, help="PPT topic or description")
    parser.add_argument("--language", "-l", type=str, default="en", choices=["en", "zh"],
                        help="Output language")
    args = parser.parse_args()

    api_key = os.getenv("SKILLBOSS_API_KEY")
    if not api_key:
        print("Error: SKILLBOSS_API_KEY must be set in environment.")
        sys.exit(1)
    try:
        result = ppt_outline_generate(api_key, args.query, args.language)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
