#!/usr/bin/env python3
"""切换当前 accessKey 绑定的项目：POST /openapi/session/change-project"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _common import change_project, build_project_url
from _logger import error_exit, print_json


def main():
    parser = argparse.ArgumentParser(
        description="切换当前 accessKey 绑定的项目",
        epilog="""
环境变量:
  LIBTV_ACCESS_KEY  必填，Bearer 鉴权
  OPENAPI_IM_BASE 或 IM_BASE_URL  可选，默认 https://im.liblib.tv

示例:
  python3 change_project.py
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.parse_args()

    data = change_project()
    project_uuid = data.get("projectUuid", "")

    if not project_uuid:
        error_exit("未返回 projectUuid")

    project_url = build_project_url(project_uuid)
    out = {
        "projectUuid": project_uuid,
        "projectUrl": project_url,
    }
    print_json(out)


if __name__ == "__main__":
    main()
