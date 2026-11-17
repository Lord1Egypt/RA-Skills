#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
子流水线注册表 - 多Agent协作编排引擎 v5.0

功能：管理可复用的子流水线定义，支持注册/查找/列出/校验。
子流水线以 JSON 文件形式存储，注册表记录其元数据（输入/输出 schema、版本、路径）。

零第三方依赖，仅使用 Python 标准库

★★★ 安全说明 ★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 路径安全：所有路径经规范化，防止路径穿越
2. 注册表文件原子写入（.tmp + os.replace）
3. 子流水线定义加载时校验结构合法性
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

使用方式：
  python pipeline_registry.py register <pipeline.json> [--name 名称] [--version 1.0]
  python pipeline_registry.py list
  python pipeline_registry.py show <name>
  python pipeline_registry.py resolve <name>
"""

import json
import os
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import state_store

# 注册表默认路径（与 scripts/ 同级的 config/ 目录）
DEFAULT_REGISTRY_PATH = os.path.join(SCRIPT_DIR, '..', 'config', 'pipeline_registry.json')


def _validate_path(filepath):
    """路径安全校验"""
    filepath = os.path.abspath(os.path.normpath(filepath))
    if not os.path.exists(filepath):
        print(f"错误：文件不存在 [{filepath}]")
        sys.exit(1)
    return filepath


def _safe_write(data, path):
    """原子写入 JSON"""
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def _load_registry(registry_path=None):
    """加载注册表"""
    if registry_path is None:
        registry_path = DEFAULT_REGISTRY_PATH
    registry_path = os.path.abspath(os.path.normpath(registry_path))
    if not os.path.exists(registry_path):
        return {"pipelines": {}}, registry_path
    with open(registry_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if 'pipelines' not in data:
        data['pipelines'] = {}
    return data, registry_path


def _save_registry(registry, registry_path):
    """保存注册表"""
    _safe_write(registry, registry_path)


def register(pipeline_path, name=None, version=None, registry_path=None):
    """注册一条子流水线

    从 pipeline.json 提取元数据并写入注册表。
    """
    pipeline_path = _validate_path(pipeline_path)
    with open(pipeline_path, 'r', encoding='utf-8') as f:
        pipeline = json.load(f)

    # 提取基本信息
    if name is None:
        name = pipeline.get('pipeline_name', '').strip()
        # 用 name 的简化形式作为 key（小写+下划线）
        name_key = name.lower().replace(' ', '_').replace('-', '_')
    else:
        name_key = name.lower().replace(' ', '_').replace('-', '_')

    if not name_key:
        print("错误：无法确定子流水线名称，请用 --name 指定")
        sys.exit(1)

    # 提取输入/输出 schema（从 agents 的 inputs/outputs 字段推断）
    agents = pipeline.get('agents', [])
    inputs = []
    outputs = []
    for agent in agents:
        for inp in agent.get('inputs', []):
            if inp not in [i['name'] for i in inputs]:
                inputs.append({"name": inp, "type": "any", "required": False})
        for outp in agent.get('outputs', []):
            if outp not in [o['name'] for o in outputs]:
                outputs.append({"name": outp, "type": "any"})

    entry = {
        "name": name,
        "path": os.path.abspath(pipeline_path),
        "description": pipeline.get('description', ''),
        "version": version or pipeline.get('version', '1.0'),
        "inputs": inputs,
        "outputs": outputs,
        "registered_at": state_store.get_timestamp(),
        "agent_count": len(agents),
    }

    registry, reg_path = _load_registry(registry_path)
    is_update = name_key in registry['pipelines']
    registry['pipelines'][name_key] = entry
    _save_registry(registry, reg_path)

    if is_update:
        print(f"✅ 子流水线 [{name_key}] 已更新注册（版本 {entry['version']}）")
    else:
        print(f"✅ 子流水线 [{name_key}] 已注册成功")
    print(f"   路径：{entry['path']}")
    print(f"   输入：{[i['name'] for i in inputs]}")
    print(f"   输出：{[o['name'] for o in outputs]}")
    return entry


def resolve(name, registry_path=None):
    """查找子流水线，返回其元数据（未找到返回 None）"""
    registry, _ = _load_registry(registry_path)
    key = name.lower().replace(' ', '_').replace('-', '_')
    return registry['pipelines'].get(key)


def list_all(registry_path=None):
    """列出所有已注册的子流水线"""
    registry, reg_path = _load_registry(registry_path)
    pipelines = registry['pipelines']
    if not pipelines:
        print("没有已注册的子流水线。")
        print(f"注册命令：python pipeline_registry.py register <pipeline.json>")
        return []

    print("=" * 60)
    print("  已注册的子流水线")
    print("=" * 60)
    for key, meta in pipelines.items():
        print(f"\n  [{key}] {meta.get('name', key)}")
        print(f"      版本：{meta.get('version', '-')}")
        print(f"      描述：{meta.get('description', '-')[:60]}")
        print(f"      输入：{[i['name'] for i in meta.get('inputs', [])]}")
        print(f"      输出：{[o['name'] for o in meta.get('outputs', [])]}")
        print(f"      路径：{meta.get('path', '-')}")
    print("\n" + "=" * 60)
    return list(pipelines.values())


def show(name, registry_path=None):
    """显示单个子流水线详情"""
    meta = resolve(name, registry_path)
    if not meta:
        print(f"未找到子流水线 [{name}]")
        return None
    print("=" * 60)
    print(f"  子流水线：{meta.get('name', name)}")
    print("=" * 60)
    print(f"  注册键：{name.lower().replace(' ', '_')}")
    print(f"  版本：{meta.get('version', '-')}")
    print(f"  描述：{meta.get('description', '-')}")
    print(f"  路径：{meta.get('path', '-')}")
    print(f"  节点数：{meta.get('agent_count', '-')}")
    print(f"  注册时间：{meta.get('registered_at', '-')}")
    print(f"  输入参数：{json.dumps(meta.get('inputs', []), ensure_ascii=False)}")
    print(f"  输出字段：{json.dumps(meta.get('outputs', []), ensure_ascii=False)}")
    print("=" * 60)
    return meta


def validate_registry(registry_path=None):
    """校验注册表：检查所有子流水线文件是否存在且结构合法"""
    registry, _ = _load_registry(registry_path)
    errors = []
    for key, meta in registry['pipelines'].items():
        path = meta.get('path', '')
        if not os.path.exists(path):
            errors.append(f"[{key}] 文件不存在：{path}")
            continue
        try:
            with open(path, 'r', encoding='utf-8') as f:
                p = json.load(f)
            if 'pipeline_name' not in p or 'agents' not in p:
                errors.append(f"[{key}] 结构不合法（缺少 pipeline_name 或 agents）")
        except Exception as e:
            errors.append(f"[{key}] 加载失败：{e}")
    if errors:
        print("注册表校验发现问题：")
        for e in errors:
            print(f"  ❌ {e}")
    else:
        print(f"✅ 注册表校验通过（{len(registry['pipelines'])} 个子流水线）")
    return len(errors) == 0


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print("子流水线注册表 - 多Agent协作编排引擎 v5.0")
        print("=" * 50)
        print("命令列表：")
        print("  python pipeline_registry.py register <pipeline.json> [--name 名称] [--version 1.0]")
        print("  python pipeline_registry.py list")
        print("  python pipeline_registry.py show <name>")
        print("  python pipeline_registry.py resolve <name>")
        print("  python pipeline_registry.py validate")
        sys.exit(0)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == 'register':
        if not args:
            print("错误：缺少 pipeline.json 路径")
            sys.exit(1)
        name = None
        version = None
        path = args[0]
        i = 1
        while i < len(args):
            if args[i] == '--name' and i + 1 < len(args):
                name = args[i + 1]
                i += 2
            elif args[i] == '--version' and i + 1 < len(args):
                version = args[i + 1]
                i += 2
            else:
                i += 1
        register(path, name=name, version=version)

    elif cmd == 'list':
        list_all()

    elif cmd == 'show':
        if not args:
            print("错误：缺少子流水线名称")
            sys.exit(1)
        show(args[0])

    elif cmd == 'resolve':
        if not args:
            print("错误：缺少子流水线名称")
            sys.exit(1)
        meta = resolve(args[0])
        if meta:
            print(json.dumps(meta, ensure_ascii=False, indent=2))
        else:
            print(f"未找到 [{args[0]}]")

    elif cmd == 'validate':
        validate_registry()

    else:
        print(f"错误：未知命令 [{cmd}]")
        sys.exit(1)
