#!/usr/bin/env python3
"""
RunningHub ComfyUI Workflow API Client
For calling RunningHub cloud ComfyUI workflows
"""

import requests
import json
import sys
import time
import os
import argparse
from typing import Optional, Dict, Any

BASE_URL = "https://www.runninghub.ai/openapi/v2"
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "config.json")


def load_config() -> Dict[str, Any]:
    """Load configuration from file"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Config file load failed: {e}")
    return {}


def save_config(config: Dict[str, Any]):
    """Save configuration to file"""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Config file save failed: {e}")
        return False


def get_api_key(args_api_key: Optional[str] = None) -> str:
    """
    Get API key, priority: command line > config file > environment variable

    Args:
        args_api_key: API key from command line

    Returns:
        API key string
    """
    if args_api_key:
        return args_api_key

    config = load_config()
    if config.get("api_key"):
        return config["api_key"]

    env_key = os.getenv("RUNNINGHUB_API_KEY")
    if env_key:
        return env_key

    return None


class RunningHubClient:
    """RunningHub API Client"""

    def __init__(self, api_key: str):
        """
        Initialize client

        Args:
            api_key: RunningHub API KEY (32 characters)
        """
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

    def upload_image(self, image_path: str) -> Optional[str]:
        """
        Upload image to RunningHub

        Args:
            image_path: Image file path

        Returns:
            Image URL, None on failure
        """
        url = f"{BASE_URL}/media/upload/binary"

        try:
            with open(image_path, "rb") as f:
                files = {"file": ("image.png", f, "image/png")}
                headers = {"Authorization": f"Bearer {self.api_key}"}

                response = requests.post(url, files=files, headers=headers, timeout=60)
                result = response.json()

                if result.get("code") == 0:
                    return result["data"]["download_url"]
                else:
                    print(f"❌ Upload failed: {result.get('msg', 'Unknown error')}")
                    return None
        except Exception as e:
            print(f"❌ Upload error: {e}")
            return None

    def submit_workflow(
        self, workflow_id: str, node_info_list: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Submit workflow task

        Args:
            workflow_id: Workflow ID
            node_info_list: Node configuration list (optional)

        Returns:
            API response data
        """
        url = f"{BASE_URL}/run/workflow/{workflow_id}"

        payload = {
            "apiKey": self.api_key,
            "workflowId": workflow_id,
            "addMetadata": True,
            "nodeInfoList": node_info_list or [],
            "instanceType": "default",
            "usePersonalQueue": "false",
        }

        try:
            response = requests.post(
                url, headers=self.headers, json=payload, timeout=30
            )
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}", "code": -1}

    def submit_workflow_with_image(
        self, workflow_id: str, node_id: str, field_name: str, image_url: str
    ) -> Dict[str, Any]:
        """
        Submit workflow with image input

        Args:
            workflow_id: Workflow ID
            node_id: Image loader node ID
            field_name: Field name (e.g., "image")
            image_url: Image URL

        Returns:
            API response data
        """
        node_info_list = [
            {"nodeId": node_id, "fieldName": field_name, "fieldValue": image_url}
        ]
        return self.submit_workflow(workflow_id, node_info_list)

    def query_task(self, task_id: str) -> Dict[str, Any]:
        """
        Query task status

        Args:
            task_id: Task ID

        Returns:
            API response data
        """
        url = f"{BASE_URL}/query"

        payload = {"taskId": task_id}

        try:
            response = requests.post(
                url, headers=self.headers, data=json.dumps(payload), timeout=30
            )
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}", "code": -1}

    def wait_for_completion(
        self, task_id: str, poll_interval: int = 5, max_attempts: int = 60
    ) -> Dict[str, Any]:
        """
        Wait for task completion

        Args:
            task_id: Task ID
            poll_interval: Poll interval (seconds)
            max_attempts: Maximum poll attempts

        Returns:
            Final task result
        """
        print(f"Waiting for task {task_id} to complete...")

        for attempt in range(max_attempts):
            result = self.query_task(task_id)

            if "error" in result:
                print(f"Status query failed: {result['error']}")
                return result

            status = result.get("status", "unknown")
            print(f"[{attempt + 1}/{max_attempts}] Current status: {status}")

            if status == "SUCCESS":
                print("✅ Task completed!")
                return result
            elif status == "FAILED":
                print("❌ Task failed!")
                return result

            time.sleep(poll_interval)

        print("⏱️ Wait timeout!")
        return {"error": "Wait timeout", "code": -1}


def main():
    parser = argparse.ArgumentParser(
        description="RunningHub ComfyUI Workflow API Client"
    )
    parser.add_argument(
        "--api-key", help="RunningHub API KEY (optional, default from config file)"
    )
    parser.add_argument("--workflow-id", required=True, help="Workflow ID")
    parser.add_argument(
        "--action",
        choices=["submit", "query", "wait", "run-with-image"],
        default="submit",
        help="Action type",
    )
    parser.add_argument("--task-id", help="Task ID (for status query)")
    parser.add_argument(
        "--poll-interval", type=int, default=5, help="Poll interval (seconds)"
    )
    parser.add_argument(
        "--max-attempts", type=int, default=60, help="Maximum poll attempts"
    )
    parser.add_argument("--save-key", metavar="KEY", help="Save API key to config file")
    parser.add_argument("--image", help="Local image path (for run-with-image)")
    parser.add_argument("--node-id", default="107", help="Image node ID (default: 107)")
    parser.add_argument(
        "--field-name", default="image", help="Image field name (default: image)"
    )

    args = parser.parse_args()

    if args.save_key:
        config = load_config()
        config["api_key"] = args.save_key
        if save_config(config):
            print("✅ API key saved to config file")
            print(f"📁 Config file: {CONFIG_FILE}")
        return

    api_key = get_api_key(args.api_key)

    if not api_key:
        print("❌ API key not found, please provide via one of:")
        print("   1. Command line: --api-key YOUR_KEY")
        print("   2. Save to config: --save-key YOUR_KEY")
        print("   3. Environment variable: RUNNINGHUB_API_KEY")
        sys.exit(1)

    client = RunningHubClient(api_key)

    if args.action == "submit":
        result = client.submit_workflow(args.workflow_id)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.action == "query":
        if not args.task_id:
            print("❌ --task-id required for status query")
            sys.exit(1)

        result = client.query_task(args.task_id)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.action == "wait":
        if not args.task_id:
            print("❌ --task-id required for wait")
            sys.exit(1)

        result = client.wait_for_completion(
            args.task_id, args.poll_interval, args.max_attempts
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.action == "run-with-image":
        if not args.image:
            print("❌ --image required for run-with-image")
            sys.exit(1)

        print(f"[1/3] Uploading image: {args.image}")
        image_url = client.upload_image(args.image)

        if not image_url:
            print("❌ Image upload failed")
            sys.exit(1)

        print(f"✅ Image uploaded successfully!")
        print(f"   URL: {image_url[:80]}...")

        print(f"\n[2/3] Submitting workflow: {args.workflow_id}")
        print(f"   Node ID: {args.node_id}")
        print(f"   Field name: {args.field_name}")

        result = client.submit_workflow_with_image(
            args.workflow_id, args.node_id, args.field_name, image_url
        )

        print(json.dumps(result, indent=2, ensure_ascii=False))

        if result.get("taskId"):
            task_id = result["taskId"]
            print(f"\n✅ Task submitted successfully! ID: {task_id}")

            print(f"\n[3/3] Waiting for task completion...")
            final_result = client.wait_for_completion(task_id)

            if final_result.get("status") == "SUCCESS":
                print("\n🎉 Task completed successfully!")
                if final_result.get("results"):
                    for i, res in enumerate(final_result["results"]):
                        url = res.get("url", "N/A")
                        print(f"\nOutput image [{i + 1}]:")
                        print(f"{url}")
            else:
                print(f"\n⚠️ Task did not complete successfully")
                print(json.dumps(final_result, indent=2, ensure_ascii=False))
        else:
            print(f"\n❌ Task submission failed")


if __name__ == "__main__":
    main()
