#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
huawei-cloud-cci-query — 华为云 CCI（云容器实例）只读查询脚本。

通过 KooCLI (hcloud) 执行 CCI 只读查询命令（list/read/get）。
覆盖命名空间、Pod（容器实例）、Deployment、StatefulSet、Job、
Service、Network、ConfigMap、Secret、PVC、Event 等资源的查询。

用法:
    python3 cci_query.py <subcommand> [--region=...] [--namespace=...] [--name=...] [...]

子命令:
    list-namespaces        列出所有命名空间
    list-pods              列出命名空间下 Pod
    list-all-pods          跨命名空间列出所有 Pod
    show-pod               查询指定 Pod 详情
    list-deployments       列出 Deployment
    show-deployment        查询 Deployment 详情
    list-statefulsets      列出 StatefulSet
    show-statefulset       查询 StatefulSet 详情
    list-jobs              列出 Job
    show-job               查询 Job 详情
    list-services          列出 Service
    show-service           查询 Service 详情
    list-networks          列出 CCI Network
    show-network           查询 Network 详情
    list-configmaps        列出 ConfigMap
    list-secrets           列出 Secret
    list-pvcs              列出 PVC
    list-events            列出 Event
    capability-list        列出脚本支持的全部子命令

退出码:
    0  成功
    2  参数错误
    3  凭据缺失
    4  hcloud 不可用
    5  API 调用失败（含 403/超时）
"""

import argparse
import json
import os
import shutil
import subprocess
import sys

# ---------------------------------------------------------------------------
# 退出码
# ---------------------------------------------------------------------------
EXIT_OK = 0
EXIT_ARG_ERROR = 2
EXIT_CRED_MISSING = 3
EXIT_HCLOUD_MISSING = 4
EXIT_API_FAILURE = 5

# hcloud 调用超时（秒）
HCLOUD_TIMEOUT = 30

# ---------------------------------------------------------------------------
# 子命令 → hcloud CCI Operation 映射
# 每项: (operation, required_params[list of (cli_flag, attr_name)], list_op[bool])
# ---------------------------------------------------------------------------
# required_params: 必填的 hcloud 参数（除 --cli-region/--cli-profile 外）
# list_op: True=列表查询; False=详情查询
SUBCOMMANDS = {
    "list-namespaces": {
        "operation": "listNamespaces",
        "required": [],
        "list_op": True,
        "desc": "列出用户所有 CCI 命名空间",
    },
    "list-pods": {
        "operation": "listCoreV1NamespacedPod",
        "required": [("namespace", "namespace")],
        "list_op": True,
        "desc": "列出指定命名空间下的 Pod（CCI 容器实例列表）",
    },
    "list-all-pods": {
        "operation": "listCoreV1PodForAllNamespaces",
        "required": [],
        "list_op": True,
        "desc": "跨所有命名空间列出 Pod",
    },
    "show-pod": {
        "operation": "readCoreV1NamespacedPod",
        "required": [("namespace", "namespace"), ("name", "name")],
        "list_op": False,
        "desc": "查询指定 Pod 详情（CCI 实例详情）",
    },
    "list-deployments": {
        "operation": "listAppsV1NamespacedDeployment",
        "required": [("namespace", "namespace")],
        "list_op": True,
        "desc": "列出指定命名空间下的 Deployment",
    },
    "show-deployment": {
        "operation": "readAppsV1NamespacedDeployment",
        "required": [("namespace", "namespace"), ("name", "name")],
        "list_op": False,
        "desc": "查询指定 Deployment 详情",
    },
    "list-statefulsets": {
        "operation": "listAppsV1NamespacedStatefulSet",
        "required": [("namespace", "namespace")],
        "list_op": True,
        "desc": "列出指定命名空间下的 StatefulSet",
    },
    "show-statefulset": {
        "operation": "readAppsV1NamespacedStatefulSet",
        "required": [("namespace", "namespace"), ("name", "name")],
        "list_op": False,
        "desc": "查询指定 StatefulSet 详情",
    },
    "list-jobs": {
        "operation": "listBatchV1NamespacedJob",
        "required": [("namespace", "namespace")],
        "list_op": True,
        "desc": "列出指定命名空间下的 Job",
    },
    "show-job": {
        "operation": "readBatchV1NamespacedJob",
        "required": [("namespace", "namespace"), ("name", "name")],
        "list_op": False,
        "desc": "查询指定 Job 详情",
    },
    "list-services": {
        "operation": "listCoreV1NamespacedService",
        "required": [("namespace", "namespace")],
        "list_op": True,
        "desc": "列出指定命名空间下的 Service",
    },
    "show-service": {
        "operation": "readCoreV1NamespacedService",
        "required": [("namespace", "namespace"), ("name", "name")],
        "list_op": False,
        "desc": "查询指定 Service 详情",
    },
    "list-networks": {
        "operation": "listNetworkingCciIoV1beta1NamespacedNetwork",
        "required": [("namespace", "namespace")],
        "list_op": True,
        "desc": "列出指定命名空间下的 CCI Network",
    },
    "show-network": {
        "operation": "readNetworkingCciIoV1beta1NamespacedNetwork",
        "required": [("namespace", "namespace"), ("name", "name")],
        "list_op": False,
        "desc": "查询指定 CCI Network 详情",
    },
    "list-configmaps": {
        "operation": "listCoreV1NamespacedConfigMap",
        "required": [("namespace", "namespace")],
        "list_op": True,
        "desc": "列出指定命名空间下的 ConfigMap",
    },
    "list-secrets": {
        "operation": "listCoreV1NamespacedSecret",
        "required": [("namespace", "namespace")],
        "list_op": True,
        "desc": "列出指定命名空间下的 Secret",
    },
    "list-pvcs": {
        "operation": "listCoreV1NamespacedPersistentVolumeClaim",
        "required": [("namespace", "namespace")],
        "list_op": True,
        "desc": "列出指定命名空间下的 PersistentVolumeClaim",
    },
    "list-events": {
        "operation": "listCoreV1NamespacedEvent",
        "required": [("namespace", "namespace")],
        "list_op": True,
        "desc": "列出指定命名空间下的 Event",
    },
}


def _load_credentials():
    """动态扫描环境变量获取 AK/SK，不依赖固定变量名。"""
    ak, sk = "", ""
    for key, value in os.environ.items():
        upper = key.upper()
        if not (upper.startswith("HUAWEI") or upper.startswith("HW") or upper.startswith("HWC")):
            continue
        if "ACCESS_KEY" in upper or upper.endswith("_AK") or upper == "AK":
            ak = value or ak
        if "SECRET_KEY" in upper or upper.endswith("_SK") or upper == "SK":
            sk = value or sk
    return ak, sk


def _ensure_hcloud():
    """确认 hcloud CLI 可用。"""
    if shutil.which("hcloud") is None:
        print("[ERROR] hcloud CLI 未安装。请参考 references/cli-installation-guide.md 安装 KooCLI。", file=sys.stderr)
        sys.exit(EXIT_HCLOUD_MISSING)


def _configure_profile(ak, sk):
    """配置 hcloud default profile（幂等）。"""
    cmd = [
        "hcloud", "configure", "set",
        "--cli-profile=default",
        "--cli-access-key=" + ak,
        "--cli-secret-key=" + sk,
    ]
    proc = subprocess.run(
        cmd, input="y\n", capture_output=True, text=True, timeout=HCLOUD_TIMEOUT
    )
    if proc.returncode != 0:
        print("[ERROR] hcloud configure set 失败: " + (proc.stderr or proc.stdout).strip(), file=sys.stderr)
        sys.exit(EXIT_API_FAILURE)


def _run_hcloud(operation, params):
    """执行 hcloud CCI <operation> 命令，返回 (returncode, stdout, stderr)。"""
    cmd = ["hcloud", "CCI", operation]
    # region / profile 固定追加
    cmd.append("--cli-region=" + params["region"])
    cmd.append("--cli-profile=default")
    # 必填路径参数
    for flag, attr in [("namespace", "namespace"), ("name", "name")]:
        value = params.get(attr)
        if value:
            cmd.append("--" + flag + "=" + value)
    # 可选查询参数
    optional_map = {
        "label_selector": "--label-selector",
        "field_selector": "--field-selector",
        "limit": "--limit",
        "continue_token": "--continue",
    }
    for attr, flag in optional_map.items():
        value = params.get(attr)
        if value:
            cmd.append(flag + "=" + str(value))
    if params.get("watch"):
        cmd.append("--watch=true")
    if params.get("pretty"):
        cmd.append("--pretty=true")

    try:
        proc = subprocess.run(
            cmd, input="y\n", capture_output=True, text=True, timeout=HCLOUD_TIMEOUT
        )
    except subprocess.TimeoutExpired:
        print("[ERROR] hcloud 调用超时（%ds）: %s" % (HCLOUD_TIMEOUT, " ".join(cmd)), file=sys.stderr)
        sys.exit(EXIT_API_FAILURE)
    return proc.returncode, proc.stdout, proc.stderr


def _print_result(stdout, stderr, returncode, pretty):
    """解析并输出结果。"""
    text = (stdout or "").strip()
    # 尝试解析为 JSON
    parsed = None
    if text:
        try:
            parsed = json.loads(text)
        except (ValueError, json.JSONDecodeError):
            parsed = None

    if returncode == 0 and parsed is not None:
        if pretty:
            _print_table(parsed)
        else:
            print(json.dumps(parsed, ensure_ascii=False, indent=2))
        return

    # 错误处理
    combined = (text + "\n" + (stderr or "")).strip()
    if "403" in combined or "CCI.01.403122" in combined or "no agency to cci" in combined:
        print("[ERROR] 403: 该区域未完成 CCI 服务授权委托。", file=sys.stderr)
        print("        请登录华为云 CCI 控制台 → 选择区域 → 「服务授权」点击同意。", file=sys.stderr)
        print(json.dumps({"error": "403", "message": "CCI service agency authorization required"}, ensure_ascii=False, indent=2))
        sys.exit(EXIT_API_FAILURE)

    if "USE_ERROR" in combined:
        print("[ERROR] hcloud 命令错误: " + combined.split("\n")[0], file=sys.stderr)
        print("        请运行 `hcloud CCI --help` 核对操作名与参数。", file=sys.stderr)
        sys.exit(EXIT_API_FAILURE)

    if returncode == 0 and text and parsed is None:
        # 非 JSON 文本但退出码 0（如纯文本提示）
        print(text)
        return

    print("[ERROR] API 调用失败 (exit=%d):" % returncode, file=sys.stderr)
    if text:
        print(text, file=sys.stderr)
    if stderr:
        print(stderr, file=sys.stderr)
    sys.exit(EXIT_API_FAILURE)


def _print_table(parsed):
    """简易表格输出：从 List 资源中提取关键字段。"""
    if not isinstance(parsed, dict):
        print(json.dumps(parsed, ensure_ascii=False, indent=2))
        return
    kind = parsed.get("kind", "")
    items = parsed.get("items")
    if items is None:
        # 单资源详情
        meta = parsed.get("metadata", {}) or {}
        print("+----------+----------------------+")
        print("| 字段     | 值                   |")
        print("+----------+----------------------+")
        print("| name     | %-20s |" % meta.get("name", "-"))
        print("| namespace| %-20s |" % meta.get("namespace", "-"))
        print("| kind     | %-20s |" % kind)
        print("+----------+----------------------+")
        return
    if not items:
        print("(无资源) kind=%s items 为空" % kind)
        return
    print("+----+----------------------+----------------------+")
    print("| #  | name                 | namespace            |")
    print("+----+----------------------+----------------------+")
    for idx, item in enumerate(items, 1):
        meta = item.get("metadata", {}) or {}
        print("| %-2d | %-20s | %-20s |" % (idx, meta.get("name", "-"), meta.get("namespace", "-")))
    print("+----+----------------------+----------------------+")
    print("(共 %d 条)" % len(items))


def build_parser():
    """构建 argparse。"""
    parser = argparse.ArgumentParser(
        prog="cci_query.py",
        description="华为云 CCI（云容器实例）只读查询脚本（基于 KooCLI hcloud）",
        epilog="示例:\n"
               "  python3 cci_query.py list-namespaces --region=cn-north-4\n"
               "  python3 cci_query.py list-pods --region=cn-north-4 --namespace=default\n"
               "  python3 cci_query.py show-pod --region=cn-north-4 --namespace=default --name=my-pod\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="subcommand", metavar="<subcommand>")

    for name, spec in SUBCOMMANDS.items():
        sp = sub.add_parser(name, help=spec["desc"])
        sp.add_argument("--region", required=True, help="区域 ID，如 cn-north-4")
        for flag, attr in spec["required"]:
            sp.add_argument("--" + flag.replace("_", "-"), dest=attr, required=True,
                            help="%s（必填）" % flag)
        if spec["list_op"]:
            sp.add_argument("--label-selector", dest="label_selector", default=None,
                            help="标签选择器，如 app=nginx")
            sp.add_argument("--field-selector", dest="field_selector", default=None,
                            help="字段选择器，如 status.phase=Running")
            sp.add_argument("--limit", type=int, default=None, help="返回数量上限")
            sp.add_argument("--continue-token", dest="continue_token", default=None,
                            help="分页续传 token")
            sp.add_argument("--watch", action="store_true", help="是否监听变更")
        sp.add_argument("--pretty", action="store_true", help="格式化表格输出")

    # capability-list
    sp_cap = sub.add_parser("capability-list", help="列出脚本支持的全部子命令")
    sp_cap.add_argument("--region", required=False, default=None, help="(忽略)")

    return parser


def main():
    if len(sys.argv) < 2:
        print("用法: python3 cci_query.py <subcommand> [--help]", file=sys.stderr)
        print("运行 `python3 cci_query.py --help` 查看全部子命令。", file=sys.stderr)
        sys.exit(EXIT_ARG_ERROR)

    parser = build_parser()
    args = parser.parse_args()

    if args.subcommand is None:
        parser.print_help()
        sys.exit(EXIT_ARG_ERROR)

    # capability-list：仅打印子命令清单，无需凭据
    if args.subcommand == "capability-list":
        print("支持的子命令（共 %d 个）：" % len(SUBCOMMANDS))
        for name, spec in SUBCOMMANDS.items():
            req = ",".join(f for f, _ in spec["required"]) or "(无额外必填)"
            print("  %-20s %s  [必填参数: %s]" % (name, spec["desc"], req))
        sys.exit(EXIT_OK)

    spec = SUBCOMMANDS[args.subcommand]

    # 前置：hcloud 可用
    _ensure_hcloud()

    # 凭据
    ak, sk = _load_credentials()
    if not ak or not sk:
        print("[ERROR] 未找到 AK/SK 环境变量。", file=sys.stderr)
        print("        请设置华为云密钥，变量名含 HUAWEI/HW/HWC 前缀 + ACCESS_KEY/_AK / SECRET_KEY/_SK。", file=sys.stderr)
        print("        例如: export HUAWEICLOUD_SDK_AK=...; export HUAWEICLOUD_SDK_SK=...", file=sys.stderr)
        sys.exit(EXIT_CRED_MISSING)

    # 配置 profile（幂等）
    _configure_profile(ak, sk)

    # 组装参数
    params = {
        "region": args.region,
        "namespace": getattr(args, "namespace", None),
        "name": getattr(args, "name", None),
        "label_selector": getattr(args, "label_selector", None),
        "field_selector": getattr(args, "field_selector", None),
        "limit": getattr(args, "limit", None),
        "continue_token": getattr(args, "continue_token", None),
        "watch": getattr(args, "watch", False),
        "pretty": getattr(args, "pretty", False),
    }

    # 执行
    rc, stdout, stderr = _run_hcloud(spec["operation"], params)
    _print_result(stdout, stderr, rc, params["pretty"])
    sys.exit(EXIT_OK if rc == 0 else EXIT_API_FAILURE)


if __name__ == "__main__":
    main()
