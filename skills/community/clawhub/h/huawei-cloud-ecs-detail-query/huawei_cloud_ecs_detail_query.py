#!/usr/bin/env python3
"""
华为云 ECS 详情查询脚本
支持：
  - 列出 ECS 实例列表 (list)
  - 查询单个 ECS 实例详情 (show)
  - 查看 capability-list (capability-list)

退出码：
  0: 成功
  3: AK/SK 未配置
  4: 实例不存在
  5: 参数错误
  6: CLI 执行失败
  7: 输入校验失败
  8: 网络超时
"""

import argparse
import json
import os
import re
import subprocess
import sys

SKILL_NAME = "huawei-cloud-ecs-detail-query"
_DEFAULT_REGION = "cn-north-4"
_MAX_LIMIT = 1000
_MIN_LIMIT = 1


def _load_credentials():
    ak, sk = "", ""
    for k, v in os.environ.items():
        u = k.upper()
        if not (u.startswith("HUAWEI") or u.startswith("HW") or u.startswith("HWC")):
            continue
        if "ACCESS_KEY" in u or u.endswith("_AK") or u == "AK":
            ak = v or ak
        if "SECRET_KEY" in u or u.endswith("_SK") or u == "SK":
            sk = v or sk
    return ak, sk


def _check_credentials():
    ak, sk = _load_credentials()
    if not ak or not sk:
        print("错误：未找到华为云 AK/SK，请设置环境变量。")
        sys.exit(3)


def _validate_server_id(server_id):
    if not server_id:
        print("错误：server_id 不能为空")
        sys.exit(7)
    pattern = r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$"
    if not re.match(pattern, server_id, re.I):
        print(f"错误：server_id 格式无效：{server_id}")
        sys.exit(7)


def _validate_limit(limit):
    if limit < _MIN_LIMIT or limit > _MAX_LIMIT:
        print(f"错误：limit 超出范围（{_MIN_LIMIT}-{_MAX_LIMIT}）：{limit}")
        sys.exit(5)


def _run_hcli(args, timeout=30):
    try:
        result = subprocess.run(["hcloud"] + args, capture_output=True, text=True, timeout=timeout)
        raw = result.stdout.strip()
        brace_start = raw.find("{")
        brace_end = raw.rfind("}")
        if brace_start >= 0 and brace_end > brace_start:
            raw = raw[brace_start:brace_end+1]
        data = json.loads(raw)
        if "error" in data:
            err_msg = data["error"].get("message", str(data["error"]))
            print(f"错误：{err_msg}")
            sys.exit(6)
        if result.returncode != 0:
            err = result.stderr.strip() or result.stdout.strip()
            print(f"错误：CLI 执行失败：{err}")
            sys.exit(6)
        return data
    except subprocess.TimeoutExpired:
        print("错误：API 请求超时")
        sys.exit(8)
    except json.JSONDecodeError as e:
        err = result.stderr.strip() if hasattr(result, "stderr") else ""
        if not err:
            err = result.stdout.strip() if hasattr(result, "stdout") else ""
        if err:
            print(f"错误：API 调用失败：{err}")
        else:
            print(f"错误：解析 API 返回数据失败：{e}")
        sys.exit(6)


def cmd_list(args):
    _check_credentials()
    region = args.region or _DEFAULT_REGION
    limit = args.limit or 20
    _validate_limit(limit)

    cli_args = ["ECS", "ListServersDetails", f"--cli-region={region}", f"--limit={limit}"]
    if args.name:
        cli_args.append(f"--name={args.name}")
    if args.ip:
        cli_args.append(f"--ip={args.ip}")
    if args.offset is not None:
        cli_args.append(f"--offset={args.offset}")

    data = _run_hcli(cli_args)
    servers = data.get("servers", [])
    count = data.get("count", len(servers))

    if not servers:
        print("未找到 ECS 实例。")
        return

    print(f"\n共 {count} 个 ECS 实例：\n")
    print(f"{'名称':<40} {'状态':<12} {'规格':<16} {'私有IP':<16} {'实例ID':<40}")
    print("-" * 124)
    for s in servers:
        name = s.get("name", "")
        status = s.get("status", "")
        flavor = (s.get("flavor") or {}).get("name", "")
        addresses = s.get("addresses", {})
        private_ip = ""
        for net in addresses.values():
            for addr in net:
                if addr.get("OS-EXT-IPS:type") == "fixed":
                    private_ip = addr.get("addr", "")
                    break
            if private_ip:
                break
        server_id = s.get("id", "")
        print(f"{name:<40} {status:<12} {flavor:<16} {private_ip:<16} {server_id:<40}")


def cmd_show(args):
    _check_credentials()
    server_id = args.server_id
    _validate_server_id(server_id)
    region = args.region or _DEFAULT_REGION

    cli_args = ["ECS", "ShowServer", f"--cli-region={region}", f"--server_id={server_id}"]
    data = _run_hcli(cli_args)
    server = data.get("server")
    if not server:
        print(f"未找到实例：{server_id}")
        sys.exit(4)

    print(f"\n{'='*60}")
    print(f"  ECS 实例详情")
    print(f"{'='*60}\n")
    print(f"  实例名称：   {server.get('name', '')}")
    print(f"  实例 ID：     {server.get('id', '')}")
    print(f"  状态：        {server.get('status', '')}")
    print(f"  规格：        {(server.get('flavor') or {}).get('name', '')}")
    print(f"  vCPU：        {(server.get('flavor') or {}).get('vcpus', '')}")
    print(f"  内存：        {(server.get('flavor') or {}).get('ram', '')} MB")
    print(f"  创建时间：   {server.get('created', '')}")
    print(f"  更新时间：   {server.get('updated', '')}")
    print(f"  可用区：     {server.get('OS-EXT-AZ:availability_zone', '')}")
    print(f"  密钥对：     {server.get('key_name', '')}")
    print(f"  镜像名称：   {(server.get('metadata') or {}).get('image_name', '')}")
    print(f"  系统类型：   {(server.get('metadata') or {}).get('os_type', '')}")

    addresses = server.get("addresses", {})
    if addresses:
        print("\n  网络信息：")
        for net_name, addr_list in addresses.items():
            for addr in addr_list:
                atype = addr.get("OS-EXT-IPS:type", "")
                ip = addr.get("addr", "")
                print(f"    {net_name} ({atype}): {ip}")

    volumes = server.get("os-extended-volumes:volumes_attached", [])
    if volumes:
        print("\n  云硬盘：")
        for v in volumes:
            print(f"    挂载点: {v.get('device', '')}    卷ID: {v.get('id', '')}")

    print()


def cmd_capability_list():
    caps = [
        f"{SKILL_NAME}:list -- 列出 ECS 实例",
        f"{SKILL_NAME}:show -- 查询 ECS 实例详情",
    ]
    for cap in caps:
        print(cap)


def main():
    parser = argparse.ArgumentParser(description="华为云 ECS 详情查询工具")
    parser.add_argument("command", nargs="?", choices=["list", "show", "capability-list"], help="子命令")
    parser.add_argument("--region", default=None, help="华为云区域")
    parser.add_argument("--server-id", dest="server_id", default=None, help="ECS实例 ID")
    parser.add_argument("--limit", type=int, default=None, help="列表分页大小")
    parser.add_argument("--offset", type=int, default=None, help="列表分页偏移")
    parser.add_argument("--name", default=None, help="ECS名称")
    parser.add_argument("--ip", default=None, help="私有IP地址")

    args = parser.parse_args()

    if args.command == "list":
        cmd_list(args)
    elif args.command == "show":
        cmd_show(args)
    elif args.command == "capability-list":
        cmd_capability_list()
    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()
