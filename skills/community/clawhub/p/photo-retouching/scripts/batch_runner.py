#!/usr/bin/env python3
"""
RunningHub Workflow Batch Execution Script
Supports batch processing of multiple tasks
"""

import json
import sys
import time
import os
from typing import List, Dict, Any
from runninghub_client import RunningHubClient, load_config, get_api_key


def run_single_workflow(
    api_key: str, workflow_id: str, inputs: Dict[str, Any], wait: bool = True
) -> Dict[str, Any]:
    """
    Run single workflow

    Args:
        api_key: API KEY
        workflow_id: Workflow ID
        inputs: Input parameters
        wait: Whether to wait for completion

    Returns:
        Execution result
    """
    client = RunningHubClient(api_key)

    print(f"Submitting workflow {workflow_id}...")
    submit_result = client.submit_workflow(workflow_id, inputs)

    if "error" in submit_result:
        print(f"❌ Submit failed: {submit_result['error']}")
        return submit_result

    task_id = submit_result.get("data", {}).get("taskId")
    if not task_id:
        print("❌ Task ID not obtained")
        return submit_result

    print(f"✅ Task submitted, ID: {task_id}")

    if wait:
        return client.wait_for_completion(task_id)

    return submit_result


def run_batch_workflows(
    api_key: str, workflow_id: str, inputs_list: List[Dict[str, Any]], delay: int = 2
) -> List[Dict[str, Any]]:
    """
    Run batch workflows

    Args:
        api_key: API KEY
        workflow_id: Workflow ID
        inputs_list: Input parameters list
        delay: Delay between tasks (seconds)

    Returns:
        All execution results
    """
    results = []

    for i, inputs in enumerate(inputs_list, 1):
        print(f"\n{'=' * 70}")
        print(f"Processing task {i}/{len(inputs_list)}")
        print(f"{'=' * 70}")

        result = run_single_workflow(api_key, workflow_id, inputs, wait=True)
        results.append(result)

        if i < len(inputs_list):
            print(f"Waiting {delay} seconds before next task...")
            time.sleep(delay)

    return results


def main():
    """Command line entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="RunningHub Batch Workflow Execution")
    parser.add_argument(
        "--api-key", help="API KEY (optional, default from config file)"
    )
    parser.add_argument("--workflow-id", required=True, help="Workflow ID")
    parser.add_argument("--inputs", help="Input parameters (JSON)")
    parser.add_argument("--batch-file", help="Batch input file (JSON array)")
    parser.add_argument(
        "--delay", type=int, default=2, help="Delay between tasks (seconds)"
    )
    parser.add_argument(
        "--no-wait", action="store_true", help="Don't wait for completion"
    )
    parser.add_argument("--output", help="Output results to file")

    args = parser.parse_args()

    api_key = get_api_key(args.api_key)

    if not api_key:
        print("❌ API key not found, please provide via one of:")
        print("   1. Command line: --api-key YOUR_KEY")
        print("   2. Config file: run runninghub_client.py --save-key YOUR_KEY")
        print("   3. Environment variable: RUNNINGHUB_API_KEY")
        sys.exit(1)

    if args.batch_file:
        print(f"Reading batch task file: {args.batch_file}")
        with open(args.batch_file, "r", encoding="utf-8") as f:
            inputs_list = json.load(f)

        if not isinstance(inputs_list, list):
            print("❌ Batch file must be JSON array")
            sys.exit(1)

        results = run_batch_workflows(
            api_key, args.workflow_id, inputs_list, args.delay
        )
    else:
        try:
            inputs = json.loads(args.inputs)
        except json.JSONDecodeError as e:
            print(f"❌ Input parameters JSON parse failed: {e}")
            sys.exit(1)

        results = [
            run_single_workflow(
                api_key, args.workflow_id, inputs, wait=not args.no_wait
            )
        ]

    output = {
        "total": len(results),
        "success": sum(1 for r in results if r.get("code") == 0 or "data" in r),
        "failed": sum(1 for r in results if "error" in r or r.get("code") != 0),
        "results": results,
    }

    print(f"\n{'=' * 70}")
    print(f"Execution complete!")
    print(
        f"Total: {output['total']} | Success: {output['success']} | Failed: {output['failed']}"
    )
    print(f"{'=' * 70}")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"Results saved to: {args.output}")
    else:
        print("\nDetailed results:")
        print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
