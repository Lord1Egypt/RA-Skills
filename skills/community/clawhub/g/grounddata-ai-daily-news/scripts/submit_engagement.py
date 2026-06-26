#!/usr/bin/env python3
"""
submit_engagement.py — Submit AI Daily News feedback or survey responses

This tool submits structured engagement payloads to L2. It does not classify
feedback, decide survey eligibility, or implement survey delivery policy.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.engagement_state import load_engagement_state, mark_survey_submitted, save_engagement_state
from lib.remote_client import submit_engagement
from lib.schemas import NetworkError
from lib.tool_output import format_error


def build_feedback_payload(message: str) -> dict:
    message = (message or "").strip()
    if not message:
        raise ValueError("Feedback message is required")
    return {
        "kind": "feedback",
        "message": message,
    }


def build_survey_response_payload(message: str) -> dict:
    message = (message or "").strip()
    if not message:
        raise ValueError("Survey response message is required")
    return {
        "kind": "survey_response",
        "message": message,
    }


def main():
    parser = argparse.ArgumentParser(description="Submit AI Daily News feedback or survey response")
    parser.add_argument("--kind", required=True, choices=("feedback", "survey_response"))
    parser.add_argument("--message", default=None, help="Natural-language feedback or survey message")
    parser.add_argument("--base-url", default=None, help="L2 API base URL")
    args = parser.parse_args()

    try:
        if args.kind == "feedback":
            payload = build_feedback_payload(args.message)
        else:
            payload = build_survey_response_payload(args.message)

        response = submit_engagement(payload, base_url=args.base_url)

        if args.kind == "survey_response":
            state = load_engagement_state()
            state = mark_survey_submitted(state)
            save_engagement_state(state)
            print("Survey response submitted. Thank you.")
        else:
            print("Feedback submitted. Thank you for helping improve AI Daily News.")

        submission_id = response.get("submission_id") if isinstance(response, dict) else None
        if submission_id:
            print(f"Submission ID: {submission_id}")

    except ValueError as e:
        print(format_error(str(e)))
        sys.exit(1)
    except NetworkError as e:
        print(format_error(f"Network error: {e}. Please tell the user to try again later."))
        sys.exit(0)
    except Exception as e:
        print(format_error(f"Unexpected error: {e}"))
        sys.exit(1)


if __name__ == "__main__":
    main()
