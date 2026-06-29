#!/usr/bin/env python3
"""
添加记录到知识库智能表格
用法：python add_to_sheet.py --name "文件名" --size 1024 --format "pdf" --source-type "微信公众号" --source-url "https://..." --is-external True --doc-url "https://docs.qq.com/..."
"""

import subprocess
import json
import os
import time
import argparse
from pathlib import Path

# ── 智能表格配置（通过环境变量设置）─────────────────────
# 每个用户需要配置自己的腾讯文档智能表格 ID
# 设置方法：
#   Windows:  set KB_INDEX_FILE_ID=你的ID
#   macOS/Linux: export KB_INDEX_FILE_ID=你的ID
# 或直接修改下方等号右边的值

def _env_or(key: str, fallback: str = "") -> str:
    val = os.environ.get(key, "")
    if not val and not fallback:
        print(f"[add_to_sheet] ⚠️ 未配置 {key}，索引写入不可用", file=sys.stderr)
    return val or fallback

SMART_SHEET_FILE_ID = _env_or("KB_INDEX_FILE_ID")   # 0号索引 智能表格 file_id
SMART_SHEET_SHEET_ID = _env_or("KB_INDEX_SHEET_ID")  # 0号索引 sheet_id
# ─────────────────────────────────────────────────────────

# 字段 ID
FIELD_TITLE = "fkfKit"      # 文件名字
FIELD_SIZE = "f2cnP7"       # 文档大小
FIELD_DATE = "fHSMJO"       # 日期
FIELD_FORMAT = "fOVcRT"     # 格式
FIELD_SOURCE_TYPE = "fPoljj" # 来源类型
FIELD_SOURCE = "f6drfQ"     # 来源
FIELD_IS_EXTERNAL = "fcP5do" # 是否外链
FIELD_DOC_URL = "fBW04a"    # 腾讯文档链接
FIELD_LEVEL = "fWqSI6"     # 等级


def get_mcporter_path():
    """获取 mcporter 路径"""
    return os.path.expanduser(r"~\AppData\Roaming\npm\mcporter.cmd")


def add_record(name, size, fmt, source_type, source_url, is_external, doc_url, level="一般"):
    """添加记录到智能表格"""
    mcporter = get_mcporter_path()
    
    # 构建记录数据
    fields = {
        FIELD_TITLE: name,
        FIELD_SIZE: size,
        FIELD_DATE: int(time.time() * 1000),  # 当前时间戳（毫秒）
        FIELD_FORMAT: fmt,
        FIELD_SOURCE_TYPE: source_type,
        FIELD_SOURCE: source_url,
        FIELD_IS_EXTERNAL: is_external,
        FIELD_DOC_URL: doc_url,
        FIELD_LEVEL: level
    }
    
    args = {
        "file_id": SMART_SHEET_FILE_ID,
        "sheet_id": SMART_SHEET_SHEET_ID,
        "records": [
            {
                "fields": fields
            }
        ]
    }
    
    # 调用 mcporter
    result = subprocess.run(
        [mcporter, "call", "tencent-docs", "smartsheet.add_records", "--args", json.dumps(args)],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"错误：添加记录失败 - {result.stderr}")
        return None
    
    response = json.loads(result.stdout)
    if "records" in response and len(response["records"]) > 0:
        record_id = response["records"][0]["record_id"]
        print(f"成功添加记录：{record_id}")
        return record_id
    else:
        print(f"错误：添加记录失败 - {result.stdout}")
        return None


def main():
    parser = argparse.ArgumentParser(description="添加记录到知识库智能表格")
    parser.add_argument("--name", required=True, help="文件名")
    parser.add_argument("--size", type=int, default=0, help="文件大小（KB）")
    parser.add_argument("--format", required=True, help="格式（mp4/pdf/pptx/docx/jpg/png/文章）")
    parser.add_argument("--source-type", required=True, help="来源类型（视频号/抖音/小红书/微信公众号/本地上传）")
    parser.add_argument("--source-url", default="", help="来源URL")
    parser.add_argument("--is-external", type=lambda x: x.lower() == "true", default=False, help="是否外链")
    parser.add_argument("--doc-url", required=True, help="腾讯文档链接")
    parser.add_argument("--level", default="一般", choices=["机密", "高", "一般", "普通"], help="等级（默认：一般）")
    
    args = parser.parse_args()
    
    add_record(
        name=args.name,
        size=args.size,
        fmt=args.format,
        source_type=args.source_type,
        source_url=args.source_url,
        is_external=args.is_external,
        doc_url=args.doc_url,
        level=args.level
    )


if __name__ == "__main__":
    main()
