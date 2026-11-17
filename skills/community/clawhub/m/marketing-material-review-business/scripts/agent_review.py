#!/usr/bin/env python3
"""Run local fallback review over a normalized marketing review payload.

Host platforms such as OpenClaw or MiniMax should not be called from this
script. They can read the generated payload and prompt, then write an
agent_risks.json file that this repository validates and renders.
"""

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from agents.base import AgentReviewError  # noqa: E402
from agents.manual import ManualAdapter  # noqa: E402


ADAPTERS = {
    "manual": ManualAdapter,
}
LOCAL_AGENT_MODES = ("manual",)
KNOWN_PROVIDERS = LOCAL_AGENT_MODES


def load_payload(payload_path):
    payload = json.loads(Path(payload_path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise AgentReviewError("payload must be a JSON object")
    if "ocr" not in payload or "rule_risks" not in payload:
        raise AgentReviewError("payload must contain ocr and rule_risks")
    return payload


def run_agent_review(payload, provider):
    if provider not in ADAPTERS:
        raise AgentReviewError(
            f"Local agent mode '{provider}' is not implemented. "
            "This script does not call OpenClaw, MiniMax, or other host-platform APIs. "
            "Use 'manual', or let the host agent write agent_risks.json and pass it "
            "with --agent-risks-json."
        )
    adapter = ADAPTERS[provider]()
    return adapter.review(payload)


def main():
    parser = argparse.ArgumentParser(description="运行本地兜底复核，输出 agent_risks.json")
    parser.add_argument("payload_json", help="agent_payload.json 路径")
    parser.add_argument("output_json", help="agent_risks.json 输出路径")
    parser.add_argument("--mode", choices=LOCAL_AGENT_MODES, default=None,
                        help="本地模式。manual 不调用外部模型；宿主 Agent 结果请用 --agent-risks-json。")
    parser.add_argument("--provider", choices=KNOWN_PROVIDERS, default=None,
                        help=argparse.SUPPRESS)
    args = parser.parse_args()
    mode = args.mode or args.provider or "manual"

    try:
        payload = load_payload(args.payload_json)
        result = run_agent_review(payload, mode)
    except Exception as exc:
        print(f"错误: Agent 复核失败：{exc}", file=sys.stderr)
        sys.exit(2)

    Path(args.output_json).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Agent runtime: {result.get('agent_runtime') or result.get('provider')} -> {args.output_json}")
    print(f"Risks: {len(result.get('risks', []))}")


if __name__ == "__main__":
    main()
