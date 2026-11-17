#!/usr/bin/env python3
# Copyright 2026 深圳市原点参数信息技术有限公司
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""OPD 数据接口通用查询脚本（OpenClaw opd-data 技能）。

用法:
    python opd_query.py ENDPOINT --fields 字段1,字段2 [--过滤参数 值 ...] [--limit N] [--offset N]

    ENDPOINT 为接口短名（如 co_info）或完整路径（/api/v1/data/co_info）。
    除 --fields/--limit/--offset 外，任意 `--参数名 值` 均作为查询过滤参数透传，
    参数含义与可选值见 references/ 下对应分类文档。

示例:
    python opd_query.py co_info --fields sec_code,sec_name,chairman --sec_code 000001
    python opd_query.py daily_quote_hist --fields trade_date,close --sec_code 000001 \
        --trade_date 2024-01-01,2024-12-31 --limit 100

环境变量:
    OPD_API_KEY    可选。API Key（形如 opd_xxx），以 X-API-Key 请求头发送。
                   未设置时自动读取配置文件 ~/.opd/api_key
    OPD_BASE_URL   可选。API 地址，默认 https://api.originp.com。
                   出于安全仅接受 https 且主机名为 *.originp.com 的地址，
                   防止 API Key 被发往未知服务器（调试内部环境用）

配置文件:
    ~/.opd/api_key  保存一行 API Key。用 `--set-key` 写入，脚本自动读取，无需重启。

Key 读取优先级: --api-key 参数 > 环境变量 OPD_API_KEY > 配置文件 ~/.opd/api_key

退出码: 0=成功；1=网络/HTTP 错误；2=业务错误（响应 code != 0）
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_BASE_URL = "https://api.originp.com"
KEY_FILE = os.path.join(os.path.expanduser("~"), ".opd", "api_key")


def resolve_api_key(args):
    """Key 读取优先级: --api-key 参数 > 环境变量 OPD_API_KEY > 配置文件 ~/.opd/api_key"""
    if args.api_key:
        return args.api_key
    env_key = os.environ.get("OPD_API_KEY", "").strip()
    if env_key:
        return env_key
    if os.path.exists(KEY_FILE):
        try:
            with open(KEY_FILE, encoding="utf-8-sig") as f:
                return f.read().strip().lstrip("\ufeff")
        except OSError:
            pass
    return ""


def key_source(args):
    """返回当前 Key 的来源描述（用于 --check 输出）"""
    if args.api_key:
        return "--api-key 参数"
    if os.environ.get("OPD_API_KEY", "").strip():
        return "环境变量 OPD_API_KEY"
    return "配置文件 {}".format(KEY_FILE)


def mask_key(key):
    if len(key) >= 8:
        return "{}…{}".format(key[:4], key[-4:])
    return "***"


def main():
    ap = argparse.ArgumentParser(
        description="OPD 数据接口通用查询脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="过滤参数（如 --sec_code 000001）按接口文档透传为 query 参数。")
    ap.add_argument("endpoint", nargs="?", default=None,
                    help="接口短名（如 co_info）或完整路径（/api/v1/data/co_info）")
    ap.add_argument("--fields", default=None, help="返回字段列表，逗号分隔（必填）")
    ap.add_argument("--limit", type=int, default=None, help="单次返回行数上限（默认 20，最大 5000）")
    ap.add_argument("--offset", type=int, default=None, help="分页位移（默认 0）")
    ap.add_argument("--api-key", default=None, help="临时指定 API Key（优先级最高）")
    ap.add_argument("--set-key", nargs="?", const=True, metavar="KEY",
                    help="保存 API Key 到 ~/.opd/api_key（不带值则从标准输入读取，避免留在命令历史）")
    ap.add_argument("--check", action="store_true", help="检查 API Key 是否已配置（不发起请求）")
    args, unknown = ap.parse_known_args()

    if args.set_key is not None:
        key = "" if args.set_key is True else args.set_key
        if not key:
            key = sys.stdin.readline()
        key = key.strip().lstrip("\ufeff")
        if not key:
            sys.exit("错误: API Key 不能为空。")
        try:
            os.makedirs(os.path.dirname(KEY_FILE), exist_ok=True)
            with open(KEY_FILE, "w", encoding="utf-8") as f:
                f.write(key + "\n")
        except OSError as e:
            sys.exit("错误: 无法写入配置文件 {}: {}".format(KEY_FILE, e))
        print("已保存 API Key 到 {}".format(KEY_FILE))
        print("配置完成，无需重启，可直接查询。")
        sys.exit(0)

    # 解析动态过滤参数: --name value 成对出现，重复同名参数以逗号拼接
    filters = {}
    it = iter(unknown)
    for tok in it:
        if not tok.startswith("--"):
            sys.exit("错误: 无法识别的参数 '{}'（过滤参数应为 --参数名 值 形式）".format(tok))
        key = tok[2:]
        val = next(it, None)
        if val is None:
            sys.exit("错误: 参数 --{} 缺少值".format(key))
        filters[key] = filters[key] + "," + val if key in filters else val

    api_key = resolve_api_key(args)
    if not api_key:
        sys.exit("错误: 未配置 API Key。请在本地终端运行 `{} --set-key` 按提示粘贴配置"
                 "（标准输入读取，不进入命令历史），或设置环境变量 OPD_API_KEY。"
                 "请勿将 API Key 粘贴到对话消息中发送。".format(os.path.basename(__file__)))

    if args.check:
        print("API Key 已配置：{}（来源：{}）".format(mask_key(api_key), key_source(args)))
        sys.exit(0)

    if not args.endpoint:
        sys.exit("错误: 缺少接口名。用法: {} ENDPOINT --fields 字段,逗号分隔".format(os.path.basename(__file__)))
    if not args.fields:
        sys.exit("错误: 缺少 --fields。用法: {} ENDPOINT --fields 字段,逗号分隔".format(os.path.basename(__file__)))

    base = os.environ.get("OPD_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    parsed = urllib.parse.urlparse(base)
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https" or not (host == "originp.com" or host.endswith(".originp.com")):
        sys.exit("错误: OPD_BASE_URL 仅接受 https 且主机名为 *.originp.com 的地址"
                 "（防止 API Key 被发往未知服务器），当前值: {}".format(base))
    path = args.endpoint if args.endpoint.startswith("/") else "/api/v1/data/" + args.endpoint.lstrip("/")

    query = {"fields": args.fields}
    query.update(filters)
    if args.limit is not None:
        query["limit"] = str(args.limit)
    if args.offset is not None:
        query["offset"] = str(args.offset)

    url = "{}{}?{}".format(base, path, urllib.parse.urlencode(query))
    req = urllib.request.Request(url, headers={
        "X-API-Key": api_key,
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        print("HTTP {} {}".format(e.code, url), file=sys.stderr)
        print(body)
        sys.exit(1)
    except urllib.error.URLError as e:
        sys.exit("网络错误: {}".format(e.reason))

    print(body)
    try:
        result = json.loads(body)
    except json.JSONDecodeError:
        sys.exit(1)
    if result.get("code") not in (0, None):
        sys.exit(2)


if __name__ == "__main__":
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    main()
