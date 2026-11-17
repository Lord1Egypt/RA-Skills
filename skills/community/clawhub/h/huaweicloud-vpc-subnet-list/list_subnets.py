#!/usr/bin/env python3
"""查询华为云 VPC 下子网列表（输出子网名称 + ID 精简列表）。

读取配置文件中的 AK/SK（region 默认 cn-north-4 可配置），通过华为云
ListSubnets 接口查询指定 Region 下某 VPC 的子网列表，仅输出 name 与 id。

用法:
    python3 list_subnets.py -v <vpc_id> [-c 配置文件路径] [-r region]

配置文件（config.json / config.example.json 见模板）:
    {
      "ak": "你的 Access Key ID",
      "sk": "你的 Secret Access Key",
      "region": "cn-north-4",
      "project_id": ""   # 可选，缺省时自动通过 IAM 解析
    }
"""

import argparse
import hashlib
import hmac
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

DEFAULT_REGION = "cn-north-4"
DEFAULT_CONFIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
ALGORITHM = "SDK-HMAC-SHA256"
SUBNET_ENDPOINT = "https://vpc.{region}.myhuaweicloud.com/v1/{project_id}/subnets"
IAM_PROJECTS_ENDPOINT = "https://iam.myhuaweicloud.com/v3/projects"
PAGE_LIMIT = "1000"


class SubnetListError(Exception):
    """子网查询错误基类。"""


class ConfigError(SubnetListError):
    """配置错误（凭证缺失、配置文件异常等）。"""


class AuthError(SubnetListError):
    """认证失败（AK/SK 无效或无权访问）。"""


class ApiError(SubnetListError):
    """接口调用异常（网络错误、服务端错误等）。"""


def _sha256_hex(data):
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def _canonical_query(query_string):
    """将 query string 参数排序后规范化为签名用 query。"""
    if not query_string:
        return ""
    params = urllib.parse.parse_qsl(query_string, keep_blank_values=True)
    items = sorted(
        (
            urllib.parse.quote(str(k), safe="-_.~"),
            urllib.parse.quote(str(v), safe="-_.~"),
        )
        for k, v in params
    )
    return "&".join(f"{k}={v}" for k, v in items)


def _canonical_uri(path):
    """规范化 URI：逐段 URL 编码并保证以 / 结尾（华为云 SDK-HMAC-SHA256 规范）。"""
    parts = [
        urllib.parse.quote(urllib.parse.unquote(p), safe="~")
        for p in path.split("/")
    ]
    uri = "/".join(parts)
    if not uri.endswith("/"):
        uri += "/"
    return uri


def _canonical_request(method, path, query_string, headers, payload_hash):
    canonical_headers = "".join(
        f"{name}:{headers[name].strip()}\n" for name in sorted(headers)
    )
    signed_headers = ";".join(sorted(headers))
    return "\n".join(
        [method, path, query_string, canonical_headers, signed_headers, payload_hash]
    )


def sign_request(ak, sk, method, url, headers, payload=None):
    """计算 SDK-HMAC-SHA256 签名，返回 Authorization 请求头值。"""
    parsed = urllib.parse.urlsplit(url)
    path = _canonical_uri(parsed.path)
    query_string = _canonical_query(parsed.query)
    payload_hash = _sha256_hex(payload) if payload else _sha256_hex("")
    canonical_request = _canonical_request(
        method, path, query_string, headers, payload_hash
    )
    request_date = headers["x-sdk-date"]
    string_to_sign = "\n".join([ALGORITHM, request_date, _sha256_hex(canonical_request)])
    signature = hmac.new(
        sk.encode("utf-8"), string_to_sign.encode("utf-8"), hashlib.sha256
    ).hexdigest()
    signed_headers = ";".join(sorted(headers))
    return f"{ALGORITHM} Access={ak}, SignedHeaders={signed_headers}, Signature={signature}"


def _build_url(base, params):
    if not params:
        return base
    sep = "&" if "?" in base else "?"
    return base + sep + urllib.parse.urlencode(params)


def _extract_next_marker(data):
    """从 ListSubnets 响应的 subnets_links 中解析下一页 marker（OpenStack 风格分页）。

    真实响应为 subnets_links 列表，每项形如 {"href": "...?marker=xxx", "rel": "next"}，
    通过 href 中的 marker 参数继续翻页；无下一页时返回 None。
    """
    for link in data.get("subnets_links") or []:
        if link.get("rel") == "next":
            query = urllib.parse.urlsplit(link.get("href", "")).query
            markers = urllib.parse.parse_qs(query).get("marker")
            if markers:
                return markers[0]
    return None


def _http_request(ak, sk, method, url, params=None):
    """发送带 AK/SK 签名的 HTTP 请求并返回解析后的 JSON 字典。"""
    full_url = _build_url(url, params)
    parsed = urllib.parse.urlsplit(full_url)
    request_date = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    sign_headers = {
        "content-type": "application/json",
        "host": parsed.netloc,
        "x-sdk-date": request_date,
    }
    authorization = sign_request(ak, sk, method, full_url, sign_headers)
    req_headers = {
        "Host": parsed.netloc,
        "X-Sdk-Date": request_date,
        "Content-Type": "application/json",
        "Authorization": authorization,
    }
    req = urllib.request.Request(full_url, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            if not body:
                return {}
            try:
                return json.loads(body)
            except json.JSONDecodeError as exc:
                raise ApiError(f"接口返回非 JSON 响应，无法解析：{exc}")
    except urllib.error.HTTPError as exc:
        detail = ""
        try:
            detail = exc.read().decode("utf-8", "replace")
        except Exception:
            pass
        if exc.code in (401, 403):
            raise AuthError(
                f"认证失败（HTTP {exc.code}）：AK/SK 无效或无权访问，请检查配置。{detail}"
            )
        raise ApiError(f"接口返回 HTTP {exc.code}：{detail}")
    except urllib.error.URLError as exc:
        raise ApiError(f"网络错误，无法访问华为云接口：{exc.reason}")


def resolve_project_id(ak, sk, region, project_id=None):
    """解析 Region 对应的 project_id；配置中已提供则直接返回。"""
    if project_id:
        return project_id
    url = IAM_PROJECTS_ENDPOINT + "?" + urllib.parse.urlencode({"name": region})
    data = _http_request(ak, sk, "GET", url)
    projects = data.get("projects") or []
    if not projects:
        raise ApiError(f"未找到 Region {region} 对应的项目 ID（IAM 返回空列表）")
    return projects[0].get("id")


def list_subnets(ak, sk, region, vpc_id, project_id=None):
    """查询指定 Region 下某 VPC 的子网列表，返回 [{'name':..., 'id':...}, ...]。"""
    if not vpc_id:
        raise ConfigError("未提供 VPC ID，请通过 -v / --vpc-id 指定要查询的 VPC。")
    pid = resolve_project_id(ak, sk, region, project_id)
    base = SUBNET_ENDPOINT.format(region=region, project_id=pid)
    subnets = []
    marker = None
    while True:
        params = {"vpc_id": vpc_id, "limit": PAGE_LIMIT}
        if marker:
            params["marker"] = marker
        data = _http_request(ak, sk, "GET", base, params)
        subnets.extend(data.get("subnets") or [])
        marker = _extract_next_marker(data)
        if not marker:
            break
    return [
        {"name": s.get("name", ""), "id": s.get("id", "")}
        for s in subnets
        if s.get("id")
    ]


def load_config(config_path):
    """读取并校验配置文件，返回 ak/sk/region/project_id。"""
    if not os.path.exists(config_path):
        raise ConfigError(
            f"未找到配置文件 {config_path}，请先复制 config.example.json 为 config.json 并填写 AK/SK。"
        )
    try:
        with open(config_path, "r", encoding="utf-8") as fh:
            cfg = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigError(f"读取配置文件失败：{exc}")
    ak = (cfg.get("ak") or "").strip()
    sk = (cfg.get("sk") or "").strip()
    if not ak or not sk:
        raise ConfigError("配置文件中缺少 AK/SK 凭证，请在 config.json 中填写。")
    region = (cfg.get("region") or "").strip() or DEFAULT_REGION
    project_id = (cfg.get("project_id") or "").strip() or None
    return {"ak": ak, "sk": sk, "region": region, "project_id": project_id}


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="查询华为云 VPC 下子网列表，输出子网名称 + ID。"
    )
    parser.add_argument(
        "-v", "--vpc-id", help="要查询子网的 VPC ID（必填）"
    )
    parser.add_argument(
        "-c", "--config", default=DEFAULT_CONFIG, help="配置文件路径（默认同目录 config.json）"
    )
    parser.add_argument("-r", "--region", help="覆盖配置中的 Region（默认 cn-north-4）")
    args = parser.parse_args(argv)
    if not args.vpc_id:
        print(
            "[错误] 未指定 VPC ID。用法：python3 list_subnets.py -v <vpc_id> [-r region] [-c config.json]",
            file=sys.stderr,
        )
        return 1
    try:
        cfg = load_config(args.config)
        region = args.region or cfg["region"]
        subnets = list_subnets(cfg["ak"], cfg["sk"], region, args.vpc_id, cfg["project_id"])
    except SubnetListError as exc:
        print(f"[错误] {exc}", file=sys.stderr)
        return 1
    if not subnets:
        print(f"Region {region} 下 VPC {args.vpc_id} 暂无子网。")
        return 0
    print(f"Region {region} 下 VPC {args.vpc_id} 的子网列表（共 {len(subnets)} 个）：")
    for subnet in subnets:
        print(f"- {subnet['name']}  {subnet['id']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
