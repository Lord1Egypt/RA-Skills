#!/usr/bin/env python3
"""切换当前 accessKey 绑定的项目：POST /openapi/session/change-project

兼容旧用法（无参数即调 API）。新用法推荐使用 manage_project.py。
"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _common import change_project, build_project_url, record_project, safe_run


def main():
    parser = argparse.ArgumentParser(
        description="调用 LibTV change-project API 创建并切换到新项目（兼容旧版；新版推荐 manage_project.py switch）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "环境变量:\n  LIBTV_ACCESS_KEY  必填\n\n"
            "示例:\n  python3 change_project.py\n"
        ),
    )
    parser.parse_args()
    data = change_project()
    project_uuid = data.get("projectUuid", "")

    if not project_uuid:
        print("错误：未返回 projectUuid", file=sys.stderr)
        sys.exit(1)

    record_project(project_uuid, set_current=True)
    project_url = build_project_url(project_uuid)
    out = {
        "projectUuid": project_uuid,
        "projectUrl": project_url,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    safe_run(main)
