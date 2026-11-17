"""AISQL API 客户端模块

本模块封装了 MEC 平台所有 AISQL 相关的 HTTP API 调用，
供 CLI 命令和 AI Bot 程序化调用。

== AI Bot 使用指南 ==

所有 API 方法返回统一的 ``Dict[str, Any]`` 格式::

    {
      "success": bool,       # 请求是否成功
      "message": str,        # 提示信息
      "data": dict | list,   # 返回数据 (成功时)
      "code": str,           # 错误码 (失败时, 如 "AUTH_TOKEN_EXPIRED")
    }

核心机制:
  - Token 自动管理: 登录后保存到 ``~/.minglue/tokens.json``, 所有请求自动携带
  - 401 自动刷新: Token 过期时自动调用 refresh-token 接口, 无需重新登录
  - 指数退避重试: 网络错误时自动重试 (最多 max_retries 次), 间隔 1s/2s/4s
  - 响应归一化: 后端返回的 PascalCase 字段自动转为 camelCase

API 方法分类:
  - 认证:   get_token / refresh_token_api
  - 生成:   gen_aisql / translate_sql
  - 任务:   create_aisql_task / perform_aisql_task
  - 查询:   get_aisql_agent_status / list_aisql_tasks / get_aisql_detail
  - 校验:   validate_aisql
  - 协议:   check_aisql_agreement / sign_aisql_agreement
  - 模型:   get_aisql_models
  - 控制:   retry_aisql_task / stop_aisql_task
  - 下载:   download_result_file
"""
import json
import os
import time
from typing import Dict, Optional, Any

import requests

from mec_aisql_cli.datetime_utils import normalize_datetimefw


def _normalize_datetimefw_in_data(
    data: Dict, required: bool = True, fmt: str = "slash"
) -> None:
    """就地归一化 data["datetimefw"] 为后端期望的格式

    供 gen_aisql / create_aisql_task / validate_aisql 在出口统一调用,
    保证发往后端的 datetimefw 始终是后端可解析的格式。

    Args:
        data:     请求体字典 (会被就地修改)
        required: datetimefw 是否必填 (gen/create 必填, validate 可选)
        fmt:      输出格式:
                  - "slash" (默认): "YYYY-MM-DD/YYYY-MM-DD" 字符串
                    用于 gen/validate (datetimefw 仅拼进 prompt 或做正则匹配)
                  - "array": '["YYYY-MM-DD","YYYY-MM-DD"]' JSON 数组字符串
                    用于 create (后端直接落库, 库中保存数组格式)
    """
    raw = data.get("datetimefw")
    if not raw:
        if required:
            raise ValueError("datetimefw 不能为空, 期望格式如 '2026-03-01/2026-03-31'")
        return
    parsed = normalize_datetimefw(raw)
    if fmt == "array":
        # create 任务落库需保存为 ["YYYY-MM-DD","YYYY-MM-DD"] 数组格式
        data["datetimefw"] = json.dumps(parsed, separators=(",", ":"))
    else:
        # gen/validate: 后端按字符串解析, 斜杠分隔即可
        data["datetimefw"] = f"{parsed[0]}/{parsed[1]}"


# Token 存储路径: ~/.minglue/tokens.json
DEFAULT_TOKEN_DIR = os.path.expanduser("~/.minglue")
DEFAULT_TOKEN_PATH = os.path.join(DEFAULT_TOKEN_DIR, "tokens.json")


class AisqlApiClient:
    """MEC AISQL API 客户端

    封装了所有 AISQL 相关的 HTTP API 调用。

    Features:
        - Automatic token loading/saving  — Token 自动加载和持久化
        - Token refresh on 401            — 401 时自动刷新 Token
        - Configurable timeout and retry  — 可配置超时和重试
        - Debug mode for troubleshooting   — 调试模式

    Attributes:
        base_url:      API 根地址 (如 https://mec.miaozhen.com/taskmng)
        token:         当前访问 Token (从 ~/.minglue/tokens.json 加载)
        refresh_token: 刷新 Token (用于 401 时自动续期)
        debug:         调试模式 (打印请求/响应详情)
        timeout:       HTTP 请求超时秒数 (默认 120)
        max_retries:   最大重试次数 (默认 2, 即最多 3 次请求)
    """

    def __init__(
        self,
        base_url: str = "https://mec.miaozhen.com/taskmng",
        debug: bool = False,
        timeout: int = 120,
        max_retries: int = 2,
    ):
        self.base_url = base_url.rstrip("/")
        self.token = None
        self.refresh_token = None
        self.debug = debug
        self.timeout = timeout
        self.max_retries = max_retries
        self._load_tokens()  # 启动时自动加载已保存的 Token

    # --------------- Token Management (Token 管理) ---------------

    def _load_tokens(self):
        """从 ~/.minglue/tokens.json 加载已保存的 Token (文件不存在时静默跳过)"""
        if self.debug:
            print(f"[DEBUG] Loading tokens from: {DEFAULT_TOKEN_PATH}")
        if not os.path.exists(DEFAULT_TOKEN_PATH):
            return
        try:
            with open(DEFAULT_TOKEN_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.token = data.get("token")
                self.refresh_token = data.get("refresh_token")
            if self.debug and self.token:
                print(f"[DEBUG] Token loaded: {self.token[:20]}...")
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] Failed to load tokens: {e}")

    def _save_tokens(self, token: str, refresh_token: str):
        """持久化 Token 到 ~/.minglue/tokens.json"""
        os.makedirs(DEFAULT_TOKEN_DIR, exist_ok=True)
        with open(DEFAULT_TOKEN_PATH, "w", encoding="utf-8") as f:
            json.dump({"token": token, "refresh_token": refresh_token}, f)
        if self.debug:
            print(f"[DEBUG] Tokens saved to: {DEFAULT_TOKEN_PATH}")

    def _load_token(self) -> Optional[str]:
        """加载 Token (用于 download 等非标准请求)"""
        if not self.token:
            self._load_tokens()
        return self.token

    def clear_tokens(self):
        """清除已保存的 Token (登出时调用)"""
        self.token = None
        self.refresh_token = None
        if os.path.exists(DEFAULT_TOKEN_PATH):
            os.remove(DEFAULT_TOKEN_PATH)

    def is_authenticated(self) -> bool:
        """检查是否已登录 (Token 是否存在)

        Returns:
            True 如已有 Token, False 如未登录
        """
        return bool(self.token)

    # --------------- HTTP Core (HTTP 核心) ---------------

    def _get_headers(self) -> Dict[str, str]:
        """构建请求头 (含 Authorization Bearer Token)"""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    @staticmethod
    def normalize_response(result: Dict[str, Any]) -> Dict[str, Any]:
        """将后端 PascalCase 响应归一化为统一格式

        后端可能返回 ``Success`` / ``Message`` / ``Data`` 等 PascalCase 字段,
        此方法将其转为小写 ``success`` / ``message`` / ``data``, 便于统一处理。

        同时处理 ``AskSuccess`` (协议接口) 和 ``TaskMessage`` (任务接口) 等特殊字段。
        """
        if not isinstance(result, dict):
            return {"success": False, "message": "Invalid response", "data": result}
        if "Success" in result and "success" not in result:
            result["success"] = result["Success"]
        if "AskSuccess" in result and "success" not in result:
            result["success"] = result["AskSuccess"]
        if "Message" in result and "message" not in result:
            result["message"] = result["Message"]
        if "TaskMessage" in result and "message" not in result:
            result["message"] = result["TaskMessage"]
        if "Data" in result and "data" not in result:
            result["data"] = result["Data"]
        return result

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        skip_refresh: bool = False,
    ) -> Dict[str, Any]:
        """核心 HTTP 请求方法 (含重试 + Token 刷新)

        流程:
            1. 发送 HTTP 请求 (GET/POST)
            2. 如返回 401 (Token 过期): 自动调用 refresh_token 续期, 然后重试
            3. 如 refresh 失败: 清除 Token, 返回 AUTH_TOKEN_EXPIRED 错误
            4. 如网络异常 (Timeout/ConnectionError): 指数退避重试

        Args:
            method:       HTTP 方法 (GET/POST/PUT/DELETE)
            endpoint:     API 端点路径 (如 /api/open/aisql/gensql)
            data:         请求参数 (GET 时作为 query params, POST 时作为 JSON body)
            skip_refresh: 跳过 Token 自动刷新 (登录/刷新接口本身设为 True)

        Returns:
            归一化的响应 Dict, 包含 success/message/data 字段
        """
        url = f"{self.base_url}{endpoint}"
        if self.debug:
            print(f"[DEBUG] {method} {url}")
            print(f"[DEBUG] Data: {json.dumps(data, ensure_ascii=False)[:500]}")

        attempt = 0
        last_error = None

        while attempt <= self.max_retries:
            try:
                response = self._send_request(method, url, data)

                if self.debug:
                    print(f"[DEBUG] Status: {response.status_code}")

                try:
                    result = response.json()
                except ValueError:
                    # 非 JSON 响应 (可能是 HTML 错误页)
                    result = {
                        "success": False,
                        "message": f"Invalid JSON response (HTTP {response.status_code})",
                        "status_code": response.status_code,
                        "raw": response.text[:500],
                    }
                    return self.normalize_response(result)

                # 处理 401: Token 过期, 尝试自动刷新
                is_unauthorized = (
                    response.status_code == 401
                    or (isinstance(result, dict) and result.get("code") == 401)
                )
                if is_unauthorized and not skip_refresh and self.refresh_token:
                    if self.debug:
                        print("[DEBUG] Token expired, refreshing...")
                    refresh_ok = self._try_refresh_token()
                    if refresh_ok:
                        attempt += 1
                        continue  # 刷新成功, 重试原请求
                    else:
                        # 刷新失败, 清除 Token
                        self.clear_tokens()
                        return self.normalize_response({
                            "success": False,
                            "message": "Token refresh failed. Please login again.",
                            "code": "AUTH_TOKEN_EXPIRED",
                        })

                return self.normalize_response(result)

            except requests.exceptions.Timeout:
                last_error = "Request timeout"
                if self.debug:
                    print(f"[DEBUG] Timeout on attempt {attempt + 1}")
            except requests.exceptions.ConnectionError as e:
                last_error = f"Connection error: {e}"
                if self.debug:
                    print(f"[DEBUG] Connection error on attempt {attempt + 1}: {e}")
            except requests.exceptions.RequestException as e:
                return {"success": False, "message": f"Request failed: {e}"}

            # 指数退避: 1s → 2s → 4s (上限 10s)
            attempt += 1
            if attempt <= self.max_retries:
                wait_time = min(2 ** attempt, 10)
                if self.debug:
                    print(f"[DEBUG] Retrying in {wait_time}s...")
                time.sleep(wait_time)

        return {
            "success": False,
            "message": f"Request failed after {self.max_retries + 1} attempts: {last_error}",
            "code": "NETWORK_ERROR",
        }

    def _send_request(self, method: str, url: str, data: Optional[Dict]) -> requests.Response:
        """发送单次 HTTP 请求 (不含重试逻辑)

        GET 请求: data 作为 query params
        POST 请求: data 作为 JSON body
        """
        headers = self._get_headers()
        kwargs = {"headers": headers, "timeout": self.timeout}

        if method.upper() == "GET":
            kwargs["params"] = data
            return requests.get(url, **kwargs)
        elif method.upper() == "POST":
            kwargs["json"] = data
            return requests.post(url, **kwargs)
        elif method.upper() == "PUT":
            kwargs["json"] = data
            return requests.put(url, **kwargs)
        elif method.upper() == "DELETE":
            kwargs["json"] = data
            return requests.delete(url, **kwargs)
        else:
            raise ValueError(f"Unsupported method: {method}")

    def _try_refresh_token(self) -> bool:
        """尝试刷新 Token, 成功返回 True

        调用 refresh_token_api, 如成功则更新内存中的 Token 并持久化。
        """
        try:
            result = self.refresh_token_api(self.refresh_token)
            if result.get("success"):
                return True
        except Exception:
            pass
        return False

    # --------------- Generic (通用) ---------------

    def request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """通用请求方法 (供高级用户直接调用任意 API)"""
        return self._make_request(method, endpoint, data)

    # --------------- Authentication (认证) ---------------

    def get_token(self, account: str, password: str) -> Dict[str, Any]:
        """登录获取 Token

        API: POST /api/open/get-token
        Args:
            account:  账号
            password: 密码
        Returns:
            成功: {success: true, token: "...", refresh_token: "..."}
            失败: {success: false, message: "错误原因"}
        Token 自动保存到 ~/.minglue/tokens.json
        """
        result = self._make_request("POST", "/api/open/get-token", {
            "Account": account, "Password": password
        }, skip_refresh=True)

        # 兼容后端 PascalCase 和 camelCase 两种返回格式
        if result.get("token"):
            self.token = result["token"]
            self.refresh_token = result.get("refreshToken") or result.get("refresh_token")
            self._save_tokens(self.token, self.refresh_token)
            result["success"] = True
        elif result.get("Success"):
            self.token = result.get("Token") or result.get("token")
            self.refresh_token = result.get("RefreshToken") or result.get("refreshToken") or result.get("refresh_token")
            self._save_tokens(self.token, self.refresh_token)
            result["success"] = True

        return result

    def refresh_token_api(self, refresh_token: str) -> Dict[str, Any]:
        """刷新 Token

        API: POST /api/open/refresh-token
        Args:
            refresh_token: 刷新 Token (登录时获取)
        Returns:
            成功: {success: true, token: "...", refresh_token: "..."}
            失败: {success: false, message: "错误原因"}
        """
        result = self._make_request("POST", "/api/open/refresh-token", {
            "RefreshToken": refresh_token
        }, skip_refresh=True)

        if result.get("token"):
            self.token = result["token"]
            self.refresh_token = result.get("refreshToken") or result.get("refresh_token")
            self._save_tokens(self.token, self.refresh_token)
            result["success"] = True
        elif result.get("Success"):
            self.token = result.get("Token") or result.get("token")
            self.refresh_token = result.get("RefreshToken") or result.get("refreshToken") or result.get("refresh_token")
            self._save_tokens(self.token, self.refresh_token)
            result["success"] = True

        return result

    # --------------- Lookup APIs (按名查 ID, Bot 自动化用) ---------------

    def lookup_client_by_name(self, name: str) -> Dict[str, Any]:
        """按客户名称查找客户 ID (Bot 自动化用)

        Purpose:
            Bot 在创建 AISQL 任务前需要 clientid (32 位 hash ID), 用户通常只提供客户名称。
            本方法调用 Ml_Client 分页接口按名称模糊匹配, 取第一条返回 clientid。

        API: GET /api/ml_client/page?clientName={name}

        Args:
            name: 客户名称 (支持模糊匹配)

        Returns:
            成功: {success: true, data: {clientid: "xxx", clientname: "...", dtsaccount: "..."}}
            失败: {success: false, message: "未找到客户: {name}"}
        """
        result = self._make_request("GET", "/api/ml_client/page", {
            "clientName": name, "page": 1, "pageSize": 10
        })
        if not (result.get("success") or result.get("Success")):
            return result
        rows = (result.get("data") or {}).get("rows") or []
        if not rows:
            return {"success": False, "message": f"未找到客户: {name}"}
        row = rows[0]
        return {
            "success": True,
            "data": {
                "clientid": row.get("clientid", ""),
                "clientname": row.get("clientname", ""),
                "dtsaccount": row.get("dtsaccount", "") or "",
            },
        }

    def lookup_brand_by_name(self, name: str, clientid: str = "") -> Dict[str, Any]:
        """按品牌名称查找品牌 ID (Bot 自动化用)

        Purpose:
            Bot 在创建 AISQL 任务前需要 brandid (32 位 hash ID), 用户通常只提供品牌名称。
            本方法调用 Ml_Brand 分页接口按名称模糊匹配, 取第一条返回 brandid。
            可选传入 clientid 缩小到指定客户下的品牌。

        API: GET /api/ml_brand/page?brandName={name}

        Args:
            name:     品牌名称 (支持模糊匹配)
            clientid: 可选, 限定客户范围

        Returns:
            成功: {success: true, data: {brandid: "xxx", brandname: "...", clientid: "..."}}
            失败: {success: false, message: "未找到品牌: {name}"}
        """
        params = {"brandName": name, "page": 1, "pageSize": 10}
        if clientid:
            params["clientid"] = clientid
        result = self._make_request("GET", "/api/ml_brand/page", params)
        if not (result.get("success") or result.get("Success")):
            return result
        rows = (result.get("data") or {}).get("rows") or []
        if not rows:
            return {"success": False, "message": f"未找到品牌: {name}"}
        row = rows[0]
        return {
            "success": True,
            "data": {
                "brandid": row.get("brandid", ""),
                "brandname": row.get("brandname", ""),
                "clientid": row.get("clientid", ""),
                "dtsaccount": row.get("dtsaccount", "") or "",
                "saleid": row.get("saleid", "") or "",
                "dtspass": row.get("dtspass", "") or "",
            },
        }

    # --------------- AISQL APIs (AISQL 业务接口) ---------------

    def gen_aisql(self, data: Dict) -> Dict[str, Any]:
        """AI 生成 SQL

        API: POST /api/open/aisql/gensql
        Args:
            data: {
                comment: 需求描述,
                client: 客户名称,
                brand: 品牌名称,
                datafrom: 数据来源 (ADM/OTT-OM/...),
                datetimefw: 时间范围, 自动归一化为 "YYYY-MM-DD/YYYY-MM-DD" 字符串,
                contype: 分析类型 (可选),
                model: AI 模型 (可选),
                url: API 地址 (可选)
            }
        Returns:
            成功: {success: true, data: {sql: "SELECT ...", prompt_tokens: N, ...}}
            失败: {success: false, message: "错误原因"}
        """
        _normalize_datetimefw_in_data(data)
        return self._make_request("POST", "/api/open/aisql/gensql", data)

    def translate_sql(self, data: Dict) -> Dict[str, Any]:
        """SQL 翻译成自然语言

        API: POST /api/open/aisql/genbysqltozn
        Args:
            data: {sql: "SELECT ...", model: "AI 模型 (可选)"}
        Returns:
            成功: {success: true, data: {translation: "统计曝光量..."}}
            失败: {success: false, message: "错误原因"}
        """
        return self._make_request("POST", "/api/open/aisql/genbysqltozn", data)

    def create_aisql_task(self, data: Dict) -> Dict[str, Any]:
        """创建 AISQL 任务

        API: POST /api/open/aisql/create
        Args:
            data: {
                taskName: 任务名称,
                client: 客户名称,
                brand: 品牌名称,
                datafrom: 数据来源,
                datetimefw: 时间范围, 自动归一化为 ["YYYY-MM-DD","YYYY-MM-DD"] 数组字符串,
                contype: 分析类型,
                sql: SQL 语句,
                aidocount: AI 预估行数 (可选)
            }
        Returns:
            成功: {success: true, data: {id: 任务ID, aiTaskId: AI任务ID}}
            失败: {success: false, message: "错误原因"}
        """
        _normalize_datetimefw_in_data(data, fmt="array")
        return self._make_request("POST", "/api/open/aisql/create", data)

    def perform_aisql_task(self, data: Dict) -> Dict[str, Any]:
        """执行 AISQL 任务 (创建工单, 提交 DMS 执行)

        API: POST /api/open/aisql/perform
        Args:
            data: {id: 任务ID}
        Returns:
            成功: {success: true, data: {orderid: 工单ID, ...}}
            失败: {success: false, message: "错误原因"}
        """
        return self._make_request("POST", "/api/open/aisql/perform", data)

    def get_aisql_status(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """查询 AISQL 任务状态 (简化版)

        API: GET /api/open/aisql/status
        Args:
            params: {id: 任务ID}
        Returns:
            成功: {success: true, data: {isdosql: 状态码, ...}}
            失败: {success: false, message: "错误原因"}
        """
        return self._make_request("GET", "/api/open/aisql/status", params)

    def get_aisql_agent_status(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """查询 AISQL 任务状态 (完整版, 含 Agent 状态)

        API: GET /api/open/aisql/agent/status
        Args:
            params: {id: 任务ID}
        Returns:
            成功: {success: true, data: {
                id: 任务ID,
                aiTaskName: 任务名称,
                agentStatus: Agent状态 (Pending/Running/Succeeded/Failed/Stopped/...),
                status: 状态描述,
                progress: 进度百分比,
                isTerminal: 是否终态,
                canRetry: 是否可重试,
                canStop: 是否可停止,
                retryCount: 已重试次数,
                maxRetryCount: 最大重试次数,
                orderid: 工单ID,
                sqldmsid: DMS查询ID,
                dmstaskid: DMS任务ID,
                dmscxtaskid: DMS导出ID,
                tableName: 结果表名,
                fileRouter: 结果文件路径,
                sqlcontent: SQL内容,
                createTime: 创建时间,
                lastErrorCode: 最后错误码,
                lastErrorMessage: 最后错误信息,
                nextPollAfterSeconds: 下次轮询建议间隔秒数
            }}
            失败: {success: false, message: "错误原因"}
        """
        return self._make_request("GET", "/api/open/aisql/agent/status", params)

    def validate_aisql(self, data: Dict) -> Dict[str, Any]:
        """校验 SQL 语句是否可执行

        API: POST /api/open/aisql/agent/validate
        Args:
            data: {
                sql: SQL 语句,
                datetimefw: 时间范围 (可选, 自动归一化为 "YYYY-MM-DD/YYYY-MM-DD" 字符串,
                                     SQL 缺少时间过滤时用作回退),
                client: 客户 (可选),
                brand: 品牌 (可选)
            }
        Returns:
            成功: {success: true, data: {valid: true, executable: true, ...}}
            失败: {success: false, message: "校验失败原因"}
        """
        _normalize_datetimefw_in_data(data, required=False)
        return self._make_request("POST", "/api/open/aisql/agent/validate", data)

    def check_aisql_agreement(self) -> Dict[str, Any]:
        """检查 AISQL 使用协议签署状态

        API: GET /api/open/aisql/check-agreement
        Returns:
            成功: {success: true, data: {signed: true/false}}
            失败: {success: false, message: "错误原因"}
        """
        return self._make_request("GET", "/api/open/aisql/check-agreement")

    def sign_aisql_agreement(self) -> Dict[str, Any]:
        """签署 AISQL 使用协议

        API: POST /api/open/aisql/sign-agreement
        Returns:
            成功: {success: true, message: "协议已签署"}
            失败: {success: false, message: "错误原因"}
        """
        return self._make_request("POST", "/api/open/aisql/sign-agreement")

    def get_aisql_models(self) -> Dict[str, Any]:
        """获取可用的 AI 模型列表

        API: GET /api/open/aisql/get-models
        Returns:
            成功: {success: true, data: [{name: "模型名", ...}, ...]}
            失败: {success: false, message: "错误原因"}
        """
        return self._make_request("GET", "/api/open/aisql/get-models")

    # --------------- Retry/Stop (任务控制) ---------------

    def retry_aisql_task(self, task_id: int) -> Dict[str, Any]:
        """重试失败的 AISQL 任务

        API: POST /api/open/aisql/retry
        Args:
            task_id: 任务ID
        Returns:
            成功: {success: true, message: "任务已重新提交"}
            失败: {success: false, message: "错误原因"}
        """
        return self._make_request("POST", "/api/open/aisql/retry", {"id": task_id})

    def stop_aisql_task(self, task_id: int) -> Dict[str, Any]:
        """停止正在执行的 AISQL 任务

        API: POST /api/open/aisql/stop
        Args:
            task_id: 任务ID
        Returns:
            成功: {success: true, message: "任务已停止"}
            失败: {success: false, message: "错误原因"}
        """
        return self._make_request("POST", "/api/open/aisql/stop", {"id": task_id})

    # --------------- List / Detail (列表 / 详情) ---------------

    def list_aisql_tasks(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """查询任务列表 (分页 + 筛选)

        API: GET /api/open/aisql/list
        Args:
            params: {
                page: 页码 (默认1),
                pageSize: 每页条数 (默认20, 最大100),
                status: 状态过滤 (0=全部, 1=草稿, 2=执行中, 3=已完成, 4=失败),
                client: 客户名称 (模糊匹配, 可选),
                brand: 品牌名称 (模糊匹配, 可选),
                keyword: 关键词 (匹配任务名/需求, 可选),
                dateFrom: 创建开始日期 (yyyy-MM-dd, 可选),
                dateTo: 创建结束日期 (yyyy-MM-dd, 可选)
            }
        Returns:
            成功: {success: true, data: {
                total: 总条数,
                page: 当前页,
                pageSize: 每页条数,
                totalPages: 总页数,
                items: [{id, aiTaskName, client, brand, isdosql, orderid, tableName, ...}, ...]
            }}
            失败: {success: false, message: "错误原因"}
        """
        return self._make_request("GET", "/api/open/aisql/list", params)

    def get_aisql_detail(self, task_id: int) -> Dict[str, Any]:
        """查询任务详情 (全字段, 复用 agent/status 接口)

        API: GET /api/open/aisql/agent/status
        Args:
            task_id: 任务ID
        Returns:
            同 get_aisql_agent_status 的返回格式
        """
        return self._make_request("GET", "/api/open/aisql/agent/status", {"id": task_id})

    def download_result_file(self, file_url: str, local_path: str) -> str:
        """下载结果文件到本地

        使用带 Token 的 HTTP 请求下载 fileRouter 指向的结果文件。

        Args:
            file_url:    文件 URL (从任务状态的 fileRouter 字段获取)
            local_path:  本地保存路径
        Returns:
            保存成功返回本地路径
        Raises:
            requests.HTTPError: 下载失败 (HTTP 错误)
        """
        headers = {}
        token = self._load_token()
        if token:
            headers["Authorization"] = f"Bearer {token}"
        # 流式下载, 避免大文件占用内存
        resp = requests.get(file_url, headers=headers, timeout=self.timeout, stream=True)
        resp.raise_for_status()
        with open(local_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        return local_path
