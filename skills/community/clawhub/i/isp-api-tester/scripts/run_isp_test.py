#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百望开放平台 ISP 接口测试执行器 v2.0
- 动态签名：每条用例都重新生成 sign/timestamp
- v6.0 / v7.0 双版本签名支持
- 兼容云端（response.xxx）和本地（model.xxx）两种返参结构
- 不校验 HTTP 状态码（按业务需要只校验 success 及业务字段）
- 支持 db_fixture：从数据库加载真实测试数据，通过 {{占位符}} 注入
- 支持 remove_fixed：在指定用例中移除某个固定参数

用法：
    python run_isp_test.py --config test_config_xxx.json --output ./
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
import datetime
import shutil
import requests
from typing import Any, Dict, List, Optional


# ============================================================
# ISP 认证 & 签名
# ============================================================

def get_md5(query: str) -> bytes:
    h = hashlib.md5()
    h.update(query.encode('utf-8'))
    return h.digest()


def bytes_to_hex(b: bytes) -> str:
    return ''.join('{:02x}'.format(x) for x in b)


def double_encrypt_password(password: str, salt: str = None) -> str:
    """MD5 + SHA-1 双重加密密码"""
    raw = (password + salt) if salt else password
    md5_h = hashlib.md5()
    md5_h.update(raw.encode('utf-8'))
    sha1_h = hashlib.sha1()
    sha1_h.update(md5_h.hexdigest().encode('utf-8'))
    return sha1_h.hexdigest()


def get_open_token(url: str, appKey: str, password: str, appSecret: str,
                   username: str, **kwargs) -> str:
    """获取 ISP access_token"""
    enc_pwd = double_encrypt_password(password, kwargs.get('userSalt'))
    ts = int(time.time() * 1000)
    token_url = (
        "{}?method=baiwang.oauth.token&grant_type=password"
        "&version=6.0&client_id={}&timestamp={}"
    ).format(url, appKey, ts)
    req_data = {
        'username': username,
        'password': enc_pwd,
        'client_secret': appSecret,
    }
    headers = {"Content-Type": "application/json", "Accept": "*/*"}
    resp = requests.post(token_url, json=req_data, headers=headers, timeout=30).json()
    if resp.get('success'):
        return resp['response']['access_token']
    raise Exception("获取token失败: " + str(resp))


def get_open_sign(method: str, appKey: str, token: str, appSecret: str,
                  req_data: dict, version: str = "6.0",
                  extra_sign_params: dict = None) -> tuple:
    """
    生成 ISP 接口签名。

    v6.0 签名串：
        {appSecret}appKey{appKey}formatjsonmethod{method}timestamp{ts}token{token}
        typesyncversion6.0{req_data_json}{appSecret}

    v7.0 签名串（在公共参数中追加 encryptScope/encryptType，按字母序）：
        {appSecret}appKey{appKey}encryptScope{encryptScope}encryptType{encryptType}
        formatjsonmethod{method}timestamp{ts}token{token}typesyncversion7.0{req_data_json}{appSecret}

    返回 (sign, timestamp)
    """
    ts = int(time.time() * 1000)
    req_data_str = json.dumps(req_data)

    if extra_sign_params:
        encrypt_scope = extra_sign_params.get("encryptScope", "")
        encrypt_type = extra_sign_params.get("encryptType", "")
        sign_str = (
            "{secret}appKey{appKey}encryptScope{encryptScope}encryptType{encryptType}"
            "formatjsonmethod{method}timestamp{ts}token{token}"
            "typesyncversion{version}{body}{secret}"
        ).format(
            secret=appSecret, appKey=appKey,
            encryptScope=encrypt_scope, encryptType=encrypt_type,
            method=method, ts=ts, token=token, version=version,
            body=req_data_str,
        )
    else:
        sign_str = (
            "{secret}appKey{appKey}formatjsonmethod{method}timestamp{ts}"
            "token{token}typesyncversion{version}{body}{secret}"
        ).format(
            secret=appSecret, appKey=appKey,
            method=method, ts=ts, token=token, version=version,
            body=req_data_str,
        )

    sign = bytes_to_hex(get_md5(sign_str)).upper()
    return sign, ts


# ============================================================
# DB Fixture：从数据库加载真实测试数据
# ============================================================

def load_db_fixture(cfg: dict) -> dict:
    """
    按 db_fixture 配置连接数据库，执行各 SQL 查询，
    返回 {变量名: 真实值} 映射字典，供 {{占位符}} 替换使用。
    """
    if not cfg:
        return {}
    conn_cfg = cfg.get("connection", {})
    queries = cfg.get("queries", [])
    if not conn_cfg or not queries:
        return {}

    try:
        import pymysql
    except ImportError:
        print("[WARN] db_fixture 需要 pymysql：pip install pymysql")
        return {}

    vars_map = {}
    conn = None
    try:
        conn = pymysql.connect(
            host=conn_cfg.get("host", "127.0.0.1"),
            port=int(conn_cfg.get("port", 3306)),
            user=conn_cfg.get("user", "root"),
            password=conn_cfg.get("password", ""),
            database=conn_cfg.get("database", ""),
            charset=conn_cfg.get("charset", "utf8mb4"),
            connect_timeout=10,
        )
        print("[DB] 连接 {}/{}".format(conn_cfg.get('host'), conn_cfg.get('database')))
        cur = conn.cursor(pymysql.cursors.DictCursor)
        for q in queries:
            name = q.get("name", "unnamed")
            sql = q.get("sql", "")
            mapping = q.get("mapping", {})
            if not sql:
                continue
            try:
                cur.execute(sql)
                row = cur.fetchone()
                if row:
                    for var_name, col_name in mapping.items():
                        val = row.get(col_name)
                        vars_map[var_name] = str(val) if val is not None else None
                        print("[DB][{}] {}={!r}".format(name, var_name, vars_map[var_name]))
                else:
                    print("[DB][{}] 无数据".format(name))
            except Exception as e:
                print("[DB][{}] SQL 失败: {}".format(name, e))
        cur.close()
    except Exception as e:
        print("[DB] 连接失败: {}".format(e))
    finally:
        if conn:
            conn.close()
    return vars_map


def apply_fixture(value: Any, vars_map: dict) -> Any:
    """递归将 {{变量名}} 替换为真实值"""
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.startswith("{{") and stripped.endswith("}}"):
            var_name = stripped[2:-2].strip()
            return vars_map.get(var_name, value)
        def _repl(m):
            v = vars_map.get(m.group(1).strip())
            return str(v) if v is not None else m.group(0)
        return re.sub(r"\{\{(\w+)\}\}", _repl, value)
    elif isinstance(value, dict):
        return {k: apply_fixture(v, vars_map) for k, v in value.items()}
    elif isinstance(value, list):
        return [apply_fixture(item, vars_map) for item in value]
    return value


# ============================================================
# 构建请求 URL（含动态签名）
# ============================================================

def build_signed_url(meta: dict, body: dict, token: str) -> tuple:
    """
    构建完整请求 URL，含 method/version/appKey/token/sign/timestamp 等查询参数。

    v7.0 特殊处理：
    - body 中若含 encryptType/encryptScope，自动提取到 URL query 参数（ISP 要求）
    - 这两个字段同时也参与签名（extra_sign_params）
    """
    base_url = meta["base_url"].rstrip("/")
    isp_auth = meta.get("isp_auth")
    version = str(meta.get("version", "6.0"))

    # 检测是否已经是完整签名URL（跳过重新签名）
    if 'sign=' in base_url and 'timestamp=' in base_url:
        return base_url, None, None

    parts = []
    if meta.get("method"):
        parts.append("method=" + meta["method"])
    if version:
        parts.append("version=" + version)
    if meta.get("appKey"):
        parts.append("appKey=" + meta["appKey"])

    sign = None
    ts = None

    if isp_auth and body and token:
        appSecret = isp_auth.get("appSecret")
        method = meta.get("method")
        appKey = meta.get("appKey") or isp_auth.get("appKey")

        # 收集 v7.0 额外签名参数
        extra_sign = {}
        for k in ("encryptType", "encryptScope"):
            if k in body:
                extra_sign[k] = body[k]

        sign, ts = get_open_sign(
            method, appKey, token, appSecret, body,
            version, extra_sign or None
        )
        parts.append("token=" + token)
        parts.append("timestamp=" + str(ts))
        parts.append("sign=" + sign)
    elif meta.get("token"):
        parts.append("token=" + meta["token"])
        ts = meta.get("timestamp") or str(int(time.time() * 1000))
        parts.append("timestamp=" + ts)

    parts.append("format=json")
    parts.append("type=sync")

    # v7.0：将 encryptType/encryptScope 加到 URL query（除了已在 body 中保留外）
    for k in ("encryptType", "encryptScope"):
        if body and k in body:
            parts.append("{}={}".format(k, str(body[k])))

    # meta 中额外 url_params
    for k, v in meta.get("url_params", {}).items():
        parts.append("{}={}".format(k, v))

    url = base_url + "?" + "&".join(parts)
    return url, sign, ts


# ============================================================
# HTTP 请求
# ============================================================

def send_request(url: str, body: dict, timeout: int = 30,
                 http_method: str = "POST") -> dict:
    headers = {"Content-Type": "application/json;charset=UTF-8"}
    try:
        if http_method.upper() == "GET":
            resp = requests.get(url, params=body, headers=headers, timeout=timeout)
        else:
            resp = requests.post(url, json=body, headers=headers, timeout=timeout)
        try:
            return {"status_code": resp.status_code, "body": resp.json(),
                    "raw": resp.text, "error": None}
        except Exception:
            return {"status_code": resp.status_code, "body": None,
                    "raw": resp.text, "error": "响应非JSON格式"}
    except requests.exceptions.ConnectionError as e:
        return {"status_code": None, "body": None, "raw": None,
                "error": "连接失败: " + str(e)}
    except requests.exceptions.Timeout:
        return {"status_code": None, "body": None, "raw": None,
                "error": "请求超时"}
    except Exception as e:
        return {"status_code": None, "body": None, "raw": None, "error": str(e)}


# ============================================================
# 响应校验（不校验 HTTP 状态码）
# ============================================================

def _get_nested(data: Any, path: str) -> Any:
    """按点分路径取嵌套值，例如 'response.invoiceType'"""
    cur = data
    for p in path.split("."):
        if cur is None:
            return None
        if isinstance(cur, list):
            try:
                cur = cur[int(p)]
            except (ValueError, IndexError):
                return None
        elif isinstance(cur, dict):
            cur = cur.get(p)
        else:
            return None
    return cur


def check_response(resp: dict, expectations: dict) -> dict:
    """
    校验响应，返回 {"passed": bool, "details": [...]}

    规则（按优先级）：
    1. 网络/解析错误 → 直接失败
    2. success 校验：
       - 期望 True  → 检查 success 字段，并检查 invoiceList/response/model 非空
       - 期望 False → 检查 success=False 即可，不检查数据
    3. response.{field} / model.{field} 形式的期望字段 → 路径取值比较
    4. has_response / check_page_data / error_field_exists → 结构性校验
    5. 不校验 HTTP 状态码
    """
    details = []
    passed = True

    if resp.get("error"):
        return {"passed": False, "details": ["请求异常: " + resp["error"]]}

    body = resp.get("body")
    if body is None:
        return {"passed": False, "details": ["[FAIL] 响应体解析失败"]}

    # ── success 字段校验 ──
    if "success" in expectations:
        exp = expectations["success"]
        act = body.get("success")
        if act == exp:
            details.append("[PASS] success={}".format(act))
            # success=True 时额外校验数据非空
            if exp is True:
                invoice_list = None
                # 云端：response.invoiceList
                resp_data = body.get("response")
                if isinstance(resp_data, dict):
                    invoice_list = resp_data.get("invoiceList")
                # 本地：model.invoiceList
                if invoice_list is None:
                    model_data = body.get("model")
                    if isinstance(model_data, dict):
                        invoice_list = model_data.get("invoiceList")
                # 根级别兜底
                if invoice_list is None:
                    invoice_list = body.get("invoiceList")

                if invoice_list is None:
                    details.append("[SKIP] invoiceList 字段不存在，跳过非空校验")
                elif len(invoice_list) == 0:
                    passed = False
                    details.append("[FAIL] invoiceList 为空（success=True 但未查到数据）")
                else:
                    details.append("[PASS] invoiceList 非空，共 {} 条".format(len(invoice_list)))
        else:
            passed = False
            details.append("[FAIL] success 期望 {}，实际 {}".format(exp, act))

    # ── response.{field} / model.{field} 路径校验 ──
    for key, exp_val in expectations.items():
        if key in ("success", "has_response", "check_page_data",
                   "error_field_exists", "response_field", "custom_checks"):
            continue
        if "." in key:
            # 先在 body 下直接取路径
            act_val = _get_nested(body, key)
            if act_val is None:
                # 没直接取到，再尝试在 response / model 下取（兼容省略前缀的写法）
                act_val = _get_nested(body.get("response") or {}, key.split(".", 1)[1])
            if str(act_val) == str(exp_val):
                details.append("[PASS] {} = {}".format(key, act_val))
            else:
                passed = False
                details.append("[FAIL] {} 期望 {}，实际 {}".format(key, exp_val, act_val))

    # ── has_response ──
    if expectations.get("has_response"):
        field_name = expectations.get("response_field")
        if field_name:
            data_val = body.get(field_name)
        else:
            data_val = body.get("model")
            field_name = "model"
            if data_val is None:
                data_val = body.get("response")
                field_name = "response"
        if data_val is not None:
            details.append("[PASS] {} 字段存在".format(field_name))
        elif body.get("success") is False:
            details.append("[INFO] {} 为空，接口返回业务错误".format(field_name))
        else:
            passed = False
            details.append("[FAIL] {} 字段为空".format(field_name))

    # ── error_field_exists ──
    if expectations.get("error_field_exists"):
        if body.get("errorResponse") is not None:
            details.append("[PASS] errorResponse 字段存在")
        else:
            passed = False
            details.append("[FAIL] errorResponse 字段不存在")

    # ── check_page_data ──
    if expectations.get("check_page_data"):
        field_name = expectations.get("response_field")
        if field_name:
            data_val = body.get(field_name)
        else:
            data_val = body.get("model")
            field_name = "model"
            if data_val is None:
                data_val = body.get("response")
                field_name = "response"
        if isinstance(data_val, list):
            details.append("[PASS] {} 返回列表，共 {} 条".format(field_name, len(data_val)))
        elif isinstance(data_val, dict):
            cnt = data_val.get("total") or data_val.get("totalCount") or data_val.get("count")
            details.append("[PASS] {} 返回对象{}".format(
                field_name, "，总数={}".format(cnt) if cnt is not None else ""))
        elif data_val is None:
            if body.get("success") is False:
                details.append("[INFO] {} 为空，接口返回业务错误".format(field_name))
            else:
                details.append("[INFO] {} 为空（可能无数据）".format(field_name))

    # ── custom_checks ──
    for chk in expectations.get("custom_checks", []):
        try:
            path = chk.get("path", "")
            op = chk.get("op", "exists")
            exp_val = chk.get("value")
            act_val = _get_nested(body, path)
            if op == "exists":
                ok = act_val is not None
            elif op == "not_exists":
                ok = act_val is None
            elif op == "eq":
                ok = str(act_val) == str(exp_val)
            elif op == "ne":
                ok = str(act_val) != str(exp_val)
            elif op == "contains":
                ok = exp_val in str(act_val)
            elif op == "gt":
                ok = float(act_val) > float(exp_val)
            elif op == "lt":
                ok = float(act_val) < float(exp_val)
            else:
                details.append("[WARN] 未知 op: " + op)
                continue
            label = "[PASS]" if ok else "[FAIL]"
            if not ok:
                passed = False
            details.append("{} 自定义校验 {} {} {} → 实际: {}".format(
                label, path, op, exp_val, act_val))
        except Exception as e:
            details.append("[WARN] 自定义校验异常: " + str(e))

    return {"passed": passed, "details": details}


# ============================================================
# 测试执行主流程
# ============================================================

def run_tests(config: dict) -> list:
    meta = config["meta"]
    fixed = config.get("fixed_params", {})
    test_cases = config["test_cases"]
    timeout = meta.get("timeout", 30)
    http_method = meta.get("http_method", "POST")

    # ---- 获取 Token ----
    isp_token = None
    isp_auth = meta.get("isp_auth")
    if isp_auth:
        print("\n[ISP] 获取 access_token ...")
        try:
            isp_token = get_open_token(
                url=meta["base_url"],
                appKey=isp_auth["appKey"],
                password=isp_auth["password"],
                appSecret=isp_auth["appSecret"],
                username=isp_auth["username"],
                userSalt=isp_auth.get("userSalt"),
            )
            print("[ISP] Token: {}...".format(isp_token[:24]))
        except Exception as e:
            print("[ISP] Token 获取失败: {}".format(e))
            return []

    # ---- 加载 DB Fixture ----
    fixture_vars = {}
    if config.get("db_fixture"):
        print("\n[DB] 加载数据库夹具...")
        fixture_vars = load_db_fixture(config["db_fixture"])
        if fixture_vars:
            print("[DB] 已加载 {} 个变量\n".format(len(fixture_vars)))
        else:
            print("[DB] 未加载到数据，占位符保持原样\n")

    total = len(test_cases)
    results = []

    print("=" * 60)
    print("  接口测试: " + (meta.get("title") or meta.get("method") or ""))
    print("  地址:     " + meta["base_url"])
    print("  版本:     " + str(meta.get("version", "6.0")))
    print("  用例数:   " + str(total))
    print("=" * 60)

    for idx, tc in enumerate(test_cases, 1):
        print("[{:03d}/{}] {} - {}".format(idx, total, tc["id"], tc["name"]))

        # 合并：fixed_params + 用例 body
        merged = {**fixed, **tc.get("body", {})}

        # remove_fixed：移除指定的固定参数
        for key in tc.get("remove_fixed", []):
            merged.pop(key, None)

        # 替换 DB fixture 占位符
        if fixture_vars:
            merged = apply_fixture(merged, fixture_vars)

        # 移除 null 值字段
        body = {k: v for k, v in merged.items()
                if v is not None and k != "_override_fixed"}

        # 构建签名 URL
        url, sign, ts = build_signed_url(meta, body, isp_token)

        start = time.time()
        resp = send_request(url, body, timeout=timeout, http_method=http_method)
        elapsed_ms = round((time.time() - start) * 1000)

        check = check_response(resp, tc.get("expect", {}))
        status_str = "[PASS]" if check["passed"] else "[FAIL]"
        print("         {}  {}ms".format(status_str, elapsed_ms))
        if sign:
            print("         sign: {}...".format(sign[:8]))

        results.append({
            "id": tc["id"],
            "group": tc.get("group", "未分组"),
            "name": tc["name"],
            "desc": tc.get("desc", ""),
            "request_url": url,
            "request_body": body,
            "expect": tc.get("expect", {}),
            "response_status": resp["status_code"],
            "response_body": resp["body"],
            "response_raw": resp["raw"] if resp["body"] is None else None,
            "response_error": resp["error"],
            "elapsed_ms": elapsed_ms,
            "passed": check["passed"],
            "check_details": check["details"],
        })

    passed = sum(1 for r in results if r["passed"])
    failed = total - passed
    print("\n" + "=" * 60)
    print("  完成: {}  通过: {}  失败: {}  通过率: {}%".format(
        total, passed, failed,
        round(passed / total * 100, 1) if total else 0))
    print("=" * 60)
    return results


# ============================================================
# 报告生成
# ============================================================

def generate_report_files(config: dict, results: list, out_dir: str) -> tuple:
    """
    生成报告（模板与数据分离）：
    - __REPORT_DATA__.js：测试结果（JS 变量赋值，供 HTML 模板 <script> 加载）
    - test_report_xxx.html：固定 HTML 模板（从 api-test-reporter skill 复制）
    """
    meta = config["meta"]
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = meta.get("method", "api_test").replace(".", "_")

    html_path = os.path.join(out_dir, "test_report_{}_{}.html".format(safe_title, ts))
    data_path = os.path.join(out_dir, "__REPORT_DATA__.js")
    json_path = os.path.join(out_dir, "test_results_{}_{}.json".format(safe_title, ts))

    # 写 JSON 原始结果
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    print("[OK] JSON 结果: " + json_path)

    # 写 JS 数据文件（var reportData = {...}）
    report_data = {
        "meta": {
            "title": meta.get("title", "接口测试报告"),
            "method": meta.get("method", ""),
            "url": meta.get("base_url", ""),
            "version": str(meta.get("version", "")),
            "generated_at": now_str,
        },
        "results": results,
    }
    json_str = json.dumps(report_data, ensure_ascii=False, indent=2, default=str)
    with open(data_path, "w", encoding="utf-8") as f:
        f.write("var reportData = ")
        f.write(json_str)
        f.write(";\n")
    print("[OK] 数据文件: " + data_path)

    # 复制固定 HTML 模板
    template_src = os.path.expanduser(
        "~/.workbuddy/skills/api-test-reporter/scripts/report_template.html")
    if not os.path.exists(template_src):
        # 备选：同 skill 目录下
        template_src = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "report_template.html")

    if os.path.exists(template_src):
        shutil.copy2(template_src, html_path)
        print("[OK] HTML 报告: " + html_path)
    else:
        # 最终备选：从 generate_report 模块取 HTML_TEMPLATE 常量
        try:
            import importlib.util
            gr_path = os.path.expanduser(
                "~/.workbuddy/skills/api-test-reporter/scripts/generate_report.py")
            spec = importlib.util.spec_from_file_location("generate_report", gr_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(mod.HTML_TEMPLATE)
            print("[OK] HTML 报告（内嵌模板）: " + html_path)
        except Exception as e:
            print("[WARN] 无法生成 HTML 报告: " + str(e))
            html_path = None

    return html_path, json_path, data_path


# ============================================================
# 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="百望 ISP 接口测试执行器")
    parser.add_argument("--config", required=True, help="测试配置文件路径（JSON）")
    parser.add_argument("--output", default=None, help="报告输出目录（默认与配置文件同目录）")
    args = parser.parse_args()

    config_path = os.path.abspath(args.config)
    if not os.path.exists(config_path):
        print("[ERROR] 配置文件不存在: " + config_path)
        sys.exit(1)

    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)

    results = run_tests(config)

    out_dir = args.output if args.output else os.path.dirname(config_path)
    os.makedirs(out_dir, exist_ok=True)

    html_path, json_path, data_path = generate_report_files(config, results, out_dir)

    print("\n测试完成！")
    if html_path:
        print("报告路径: " + html_path)


if __name__ == "__main__":
    main()
