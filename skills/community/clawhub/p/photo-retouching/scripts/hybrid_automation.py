#!/usr/bin/env python3
"""
RunningHub Workflow Hybrid Automation
1. User manually uploads image and clicks run on web
2. This script monitors task status and retrieves results
"""

import requests
import json
import time
import sys

API_KEY = ""
WORKFLOW_ID = "1987728214757978114"


def monitor_task(task_id, max_attempts=60, poll_interval=5):
    """Monitor task status until completion"""
    query_url = "https://www.runninghub.ai/openapi/v2/query"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}

    print(f"\nMonitoring task: {task_id}")
    print("=" * 70)

    for attempt in range(max_attempts):
        resp = requests.post(
            query_url, headers=headers, json={"taskId": task_id}, timeout=10
        )

        if resp.status_code == 200:
            result = resp.json()
            status = result.get("status")

            print(f"[{attempt + 1}/{max_attempts}] Status: {status}")

            if status == "SUCCESS":
                print("\n✅ Task completed!")
                print("\nOutput results:")
                if result.get("results"):
                    for i, res in enumerate(result["results"]):
                        url = res.get("url", "N/A")
                        print(f"  [{i + 1}] {url}")
                        print(f"<qqimg>{url}</qqimg>")
                return result

            elif status == "FAILED":
                print(
                    f"\n❌ Task failed: {result.get('errorMessage', 'Unknown error')}"
                )
                return result

            elif status in ["RUNNING", "QUEUED", "PENDING"]:
                time.sleep(poll_interval)
                continue
        else:
            print(f"Query failed: {resp.status_code}")
            return None

    print(f"\n⏱️ Monitor timeout")
    return None


def submit_default_workflow():
    """Submit workflow with default configuration"""
    url = f"https://www.runninghub.ai/openapi/v2/run/workflow/{WORKFLOW_ID}"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}

    payload = {
        "addMetadata": True,
        "nodeInfoList": [],
        "instanceType": "default",
        "usePersonalQueue": "false",
    }

    print("=" * 70)
    print("Submit RunningHub Workflow")
    print("=" * 70)

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        result = resp.json()

        if result.get("taskId"):
            print(f"✅ Task submitted successfully!")
            print(f"Task ID: {result['taskId']}")
            print(f"Status: {result.get('status', 'Unknown')}")

            return monitor_task(result["taskId"])
        else:
            error_msg = result.get("errorMessage", "Unknown error")
            print(f"❌ Submit failed: {error_msg}")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    print("\n【RunningHub Image Refinement Workflow】")
    print()
    print(
        "Since this workflow doesn't support API image modification, two options are provided:"
    )
    print()
    print("Option 1: Run with default image (automatic)")
    print("Option 2: Manual web run + API monitoring")
    print()

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["submit", "monitor"],
        default="submit",
        help="submit=submit default task, monitor=monitor specific task",
    )
    parser.add_argument("--task-id", help="Task ID to monitor")
    args = parser.parse_args()

    if args.mode == "submit":
        submit_default_workflow()
    elif args.mode == "monitor" and args.task_id:
        monitor_task(args.task_id)
    else:
        print("Usage:")
        print("  python3 hybrid_automation.py --mode submit")
        print("  python3 hybrid_automation.py --mode monitor --task-id YOUR_TASK_ID")


if __name__ == "__main__":
    main()
