#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests",
#     "requests-toolbelt"
# ]
# ///

"""
Perform document extraction using Gitee AI Async API.

Usage:
    python perform_doc_extraction.py --file /path/to/document.pdf [--api-key KEY]
"""

import argparse
import os
import sys
import time
import contextlib
import mimetypes
import requests
from requests_toolbelt import MultipartEncoder


def get_api_key(provided_key: str | None) -> str | None:
    """Get API key from argument, config, or environment."""
    if provided_key:
        return provided_key
    return os.environ.get("GITEEAI_API_KEY")


def submit_task(filepath: str, api_key: str) -> dict:
    """Submit the document parsing task to the API."""
    API_URL = "https://ai.gitee.com/v1/async/documents/parse"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    fields = [
        ("model", "PaddleOCR-VL-1.5"),
        ("include_image", "true"),
        ("include_image_base64", "true"),
        ("output_format", "md"),
    ]
    
    with contextlib.ExitStack() as stack:
        name = os.path.basename(filepath)
        
        # Support both local file paths and URLs
        if filepath.startswith(("http://", "https://")):
            response = requests.get(filepath, timeout=10)
            response.raise_for_status()
            fields.append(("file", (name, response.content, response.headers.get("Content-Type", "application/octet-stream"))))
        else:
            if not os.path.exists(filepath):
                print(f"Error: File not found at {filepath}", file=sys.stderr)
                sys.exit(1)
            mime_type, _ = mimetypes.guess_type(filepath)
            fields.append(("file", (name, stack.enter_context(open(filepath, "rb")), mime_type or "application/octet-stream")))
        
        encoder = MultipartEncoder(fields)
        headers["Content-Type"] = encoder.content_type
        
        response = requests.post(API_URL, headers=headers, data=encoder)
        response.raise_for_status()
        return response.json()


def poll_task(task_id: str, api_key: str) -> dict:
    """Poll the task status until it completes or fails."""
    status_url = f"https://ai.gitee.com/v1/task/{task_id}"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    timeout = 5 * 60  # 5 minutes max
    retry_interval = 5 # Check every 5 seconds
    attempts = 0
    max_attempts = int(timeout / retry_interval)
    
    while attempts < max_attempts:
        attempts += 1
        print(f"Checking task status [{attempts}]...", file=sys.stderr)
        
        response = requests.get(status_url, headers=headers, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if result.get("error"):
            raise ValueError(f"{result['error']}: {result.get('message', 'Unknown error')}")
            
        status = result.get("status", "unknown")
        
        if status == "success":
            return result
        elif status in ["failed", "cancelled"]:
            raise RuntimeError(f"Task ended with status: {status}")
        else:
            time.sleep(retry_interval)
            continue
            
    raise TimeoutError(f"Maximum attempts reached ({max_attempts})")


def main():
    parser = argparse.ArgumentParser(
        description="Extract text from documents using Gitee AI"
    )
    parser.add_argument(
        "--file", "-f",
        required=True,
        help="Path to the document file (e.g., .pdf, .docx) or URL"
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

    print(f"Processing document extraction...")
    print(f"File: {args.file}")

    try:
        # 1. Submit the task
        submit_result = submit_task(args.file, api_key)
        task_id = submit_result.get("task_id")
        if not task_id:
            raise ValueError("Task ID not found in the response")
            
        print(f"Task created successfully. Task ID: {task_id}", file=sys.stderr)
        
        # 2. Poll for completion
        task_result = poll_task(task_id, api_key)
        
        # 3. Extract the final content
        final_text = ""
        if "output" in task_result:
            output_data = task_result["output"]
            
            # Extract key "segments" if available
            if "segments" in output_data:
                segments = output_data["segments"]
                # Sort segments by index if available to maintain order
                segments.sort(key=lambda x: x.get("index", 0))
                # Concatenate the content of all segments
                final_text = "\n\n".join(seg.get("content", "") for seg in segments)
                
            elif "file_url" in output_data:
                file_url = output_data["file_url"]
                print(f"Downloading result from: {file_url}", file=sys.stderr)
                doc_response = requests.get(file_url)
                doc_response.raise_for_status()
                final_text = doc_response.text
            elif "text_result" in output_data:
                final_text = output_data["text_result"]
        
        if not final_text:
            final_text = "No text extracted or unknown output format."

        # 4. Print the result in the required format
        print("\nEXTRACTION_RESULT:")
        print(final_text.strip())

    except Exception as e:
        print(f"\nError performing document extraction: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()