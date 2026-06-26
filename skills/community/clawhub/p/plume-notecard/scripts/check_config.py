#!/usr/bin/env python3
"""
检查 PLUME_API_KEY 是否已配置
支持多源检查：环境变量 → EXTEND.md → OpenClaw 配置
输出: CONFIGURED / NOT_CONFIGURED
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config


def main():
    key = config.get_api_key()

    if key:
        print("CONFIGURED")
        sys.exit(0)
    else:
        env = config.detect_agent_env()
        print("NOT_CONFIGURED")
        if env["agent"] == "openclaw":
            print("Error: PLUME_API_KEY must be set. Configure it in ~/.openclaw/openclaw.json env.PLUME_API_KEY or set the PLUME_API_KEY environment variable.", file=sys.stderr)
        else:
            print("Error: PLUME_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
