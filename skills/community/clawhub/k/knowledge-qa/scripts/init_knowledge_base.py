# -*- coding: utf-8 -*-
"""
init_knowledge_base.py - 初始化一个新知识库
用法：
    python init_knowledge_base.py <知识库名称> [--path <工作目录>]
示例：
    python init_knowledge_base.py MySQLNotes
    python init_knowledge_base.py MySQLNotes --path "D:/workspace"
"""

import sys as _sys
_sys.stdout.reconfigure(encoding='utf-8')
_sys.stderr.reconfigure(encoding='utf-8')

import argparse
import json
import os
import sys


def create_config_template(collection_name, base_path):
    """
    创建 config.json 模板。
    base_path: 知识库的根目录
    """
    kb_root = base_path
    raw_docs_path = os.path.join(kb_root, "raw_docs")
    indexed_files_path = os.path.join(kb_root, "indexed_files.json")

    config = {
        "knowledge_base": {
            "name": os.path.basename(base_path),
            "root_path": raw_docs_path,
            "indexed_files_path": indexed_files_path
        },
        "dashvector": {
            "api_key": "YOUR_DASHVECTOR_API_KEY",
            "endpoint": "https://vrs-cn-xxxx.dashvector.cn-hangzhou.aliyuncs.com",
            "collection_name": collection_name,
            "dimension": 1024,
            "model": "text-embedding-v3"
        },
        "bailian": {
            "api_key": "YOUR_BAILIAN_API_KEY",
            "model": "text-embedding-v3"
        }
    }
    return config


def init_knowledge_base(kb_name, base_path=None):
    """
    在 base_path 下创建知识库 kb_name 的目录结构和配置模板。
    返回 (kb_path, config_path)
    """
    if base_path is None:
        base_path = os.getcwd()

    kb_path = os.path.join(base_path, kb_name)

    if os.path.exists(kb_path):
        raw_docs = os.path.join(kb_path, "raw_docs")
        config_json = os.path.join(kb_path, "config.json")
        if os.path.isdir(raw_docs) and os.path.isfile(config_json):
            print(f"[x] 知识库 '{kb_name}' 已存在（{kb_path}）")
            return None, None
        else:
            print(f"[!] 目录 '{kb_path}' 存在但不是有效知识库，将覆盖创建结构")
    else:
        os.makedirs(kb_path, exist_ok=True)

    dirs_to_create = [
        kb_path,
        os.path.join(kb_path, "raw_docs"),
        os.path.join(kb_path, "raw_docs", "default"),
    ]
    for d in dirs_to_create:
        os.makedirs(d, exist_ok=True)

    collection_name = kb_name.replace(" ", "_").replace("-", "_")
    config = create_config_template(collection_name, kb_path)
    config_path = os.path.join(kb_path, "config.json")
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    indexed_path = os.path.join(kb_path, "indexed_files.json")
    with open(indexed_path, "w", encoding="utf-8") as f:
        json.dump({"last_updated": None, "files": []}, f, ensure_ascii=False, indent=2)

    readme_path = os.path.join(kb_path, "README.md")
    readme_content = f"""# {kb_name} 知识库

## 目录结构

```
{os.path.basename(kb_path)}/
├── raw_docs/           <- 放你的文档（PDF/MD/DOCX）
│   ├── default/        <- 默认分区（直接放根目录的文件）
│   ├── mysql/         <- 创建子文件夹 = 创建分区
│   ├── oracle/
│   └── (其他主题)/
├── config.json         <- 配置文件（请填写阿里云凭证）
└── indexed_files.json  <- 自动维护，无需手动编辑
```

## 分区使用方式

在 `raw_docs/` 下创建子文件夹，即可创建分区：
- `raw_docs/mysql/` -> 分区名 `mysql`
- `raw_docs/MySQL实战/` -> 分区名 `mysql_`（自动转小写）
- 直接放在 `raw_docs/` 根目录 -> 分区名 `default`

## 配置 config.json

请打开 `config.json`，填入你的阿里云凭证：
1. `dashvector.api_key` - DashVector API Key
2. `dashvector.endpoint` - Collection 访问地址
3. `dashvector.collection_name` - 集合名称（建议与知识库名一致）
4. `bailian.api_key` - 百炼 API Key（用于生成向量）

凭证获取地址：
- DashVector: https://dashvector.console.aliyun.com/api-key
- 百炼: https://bailian.console.aliyun.com/api-key
"""
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)

    return kb_path, config_path


def main():
    parser = argparse.ArgumentParser(description="初始化一个新的知识库")
    parser.add_argument("kb_name", help="知识库名称（同时作为文件夹名和默认 Collection 名）")
    parser.add_argument("--path", dest="base_path", default=None,
                        help="工作目录路径（知识库将创建在此目录下），默认使用当前目录")
    args = parser.parse_args()

    kb_name = args.kb_name.strip()
    if not kb_name:
        print("[x] 知识库名称不能为空")
        sys.exit(1)

    base_path = args.base_path
    if base_path:
        if not os.path.isdir(base_path):
            print(f"[x] 目录不存在: {base_path}")
            sys.exit(1)
    else:
        base_path = os.getcwd()
        print(f"未指定 --path，使用当前目录: {base_path}")

    print(f"\n{'=' * 50}")
    print(f"初始化知识库：{kb_name}")
    print(f"工作目录：{base_path}")
    print(f"{'=' * 50}\n")

    kb_path, config_path = init_knowledge_base(kb_name, base_path)

    if kb_path is None:
        sys.exit(1)

    print(f"[+] 知识库初始化完成！\n")
    print(f"目录结构：")
    print(f"   {kb_path}/")
    print(f"   ├── raw_docs/")
    print(f"   |   └── default/")
    print(f"   ├── config.json       <- [!] 请填写阿里云凭证")
    print(f"   ├── indexed_files.json")
    print(f"   └── README.md")
    print(f"\n[!] 下一步：请编辑 config.json 填入你的阿里云凭证")
    print(f"   凭证获取方式：")
    print(f"   - DashVector: https://dashvector.console.aliyun.com/api-key")
    print(f"   - 百炼: https://bailian.console.aliyun.com/api-key")
    print(f"\n使用方式：")
    print(f"   1. 往 raw_docs/（及其子目录）放入文档")
    print(f"   2. 告诉 AI：'上传到知识库 {kb_name}'")
    print(f"   3. 问 AI：'基于 {kb_name} 知识库回答...'")


if __name__ == "__main__":
    main()
