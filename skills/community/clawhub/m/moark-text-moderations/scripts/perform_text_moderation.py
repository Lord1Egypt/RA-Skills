#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "openai"
# ]
# ///

"""
Perform text moderation using Gitee AI API.

Usage:
    python perform_text_moderation.py --text "User-specified input text" [--api-key KEY]
"""

import argparse
import os
import sys
from openai import OpenAI


def get_api_key(provided_key: str | None) -> str | None:
    """Get API key from argument, config, or environment."""
    if provided_key:
        return provided_key
    return os.environ.get("GITEEAI_API_KEY")


def main():
    parser = argparse.ArgumentParser(
        description="Perform text moderation using Gitee AI API"
    )
    parser.add_argument(
        "--text", "-t",
        required=True,
        help="User-specified input text to moderate"
    )
    parser.add_argument(
        "--api-key", "-k",
        help="Gitee AI API key (overrides GITEEAI_API_KEY env var)"
    )

    args = parser.parse_args()

    # Get API key
    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: No API key provided.", file=sys.stderr)
        print("Please either:", file=sys.stderr)
        print("  1. Provide --api-key argument", file=sys.stderr)
        print("  2. Set GITEEAI_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    # Initialize OpenAI client
    client = OpenAI(
        base_url="https://ai.gitee.com/v1",
        api_key=api_key,
    )

    print(f"Performing text moderation...")
    print(f"Input Text: {args.text}")

    try:
        response = client.moderations.create(
        	input=[
        		{
        			"type": "text",
        			"text": args.text
        		}
        	],
        	model="moark-text-moderation",
        )

        # Extract the result and format it as JSON for the LLM to summarize
        if response.results:
            result_json = response.results[0].model_dump_json(indent=2)
            print(f"\nMODERATION_RESULT:\n{result_json}")
        else:
            print("\nMODERATION_RESULT:\nNo results returned from API.")


    except Exception as e:
        print(f"Error performing text moderation: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()