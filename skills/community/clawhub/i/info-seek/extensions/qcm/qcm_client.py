#!/usr/bin/env python3
"""qcm_client.py — Infoseek 端协同点：反向调用 QCM 客户端（任务1）

Infoseek 端协同点（infoseek/extensions/qcm/ 唯一必要文件）：
  - 供 Infoseek 的 qcm_query 工具使用（反向调用 QCM MCP server）
  - 支持本地 stdio（QCM 已安装）或远程 HTTP+OAuth（跨设备）

用法（Infoseek 端）：
  import sys; sys.path.insert(0, '<infoseek>/extensions/qcm')
  from qcm_client import QCMClient

  client = QCMClient()                        # 本地 stdio
  result = client.research("焊接虚焊客诉")      # qcm_research
  result = client.validate(text="...")        # qcm_validate

  # 跨设备（远程 QCM + OAuth）
  client = QCMClient(remote_url="https://qcm.example.com",
                     client_id="infoseek", client_secret="xxx")
  result = client.research("半导体封装虚焊")
"""
import json
import os
from paths import SCRIPTS
import subprocess
from typing import Dict, Any, Optional

DEFAULT_QCM_SERVER = os.environ.get(
    "QCM_SERVER",
    str(SCRIPTS / "mcp_server.py"),
)


class QCMClient:
    """Infoseek → QCM 反向调用客户端"""

    def __init__(self, qcm_server: str = DEFAULT_QCM_SERVER,
                 remote_url: Optional[str] = None,
                 client_id: Optional[str] = None,
                 client_secret: Optional[str] = None,
                 timeout_s: int = 60):
        self.qcm_server = qcm_server
        self.remote_url = remote_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.timeout_s = timeout_s
        self._token: Optional[str] = None

    # ============ 本地 stdio 调用 ============
    def _stdio_call(self, tool_name: str, arguments: Dict) -> Dict:
        """通过 stdio subprocess 调用 QCM MCP server"""
        if not os.path.exists(self.qcm_server):
            return {"status": "degraded",
                    "error": f"QCM 未安装: {self.qcm_server}",
                    "hint": "安装 QCM 或配置 QCM_SERVER 环境变量"}

        request = {
            "jsonrpc": "2.0", "id": 1, "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments},
        }
        try:
            proc = subprocess.Popen(
                ["python3", self.qcm_server],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, text=True,
            )
            proc.stdin.write(json.dumps(request, ensure_ascii=False) + "\n")
            proc.stdin.flush()
            proc.stdin.close()
            response = proc.stdout.readline().strip()
            proc.wait(timeout=self.timeout_s)
        except Exception as e:
            return {"status": "failed", "error": str(e)[:200], "tool": tool_name}

        if not response:
            return {"status": "failed", "error": "QCM no response", "tool": tool_name}

        try:
            parsed = json.loads(response)
        except json.JSONDecodeError:
            return {"status": "failed", "error": "QCM invalid response", "tool": tool_name}

        if "error" in parsed:
            return {"status": "failed", "error": parsed["error"], "tool": tool_name}

        result = parsed.get("result", {})
        content = result.get("content", [])
        if content and isinstance(content, list):
            try:
                return json.loads(content[0]["text"])
            except (KeyError, IndexError, json.JSONDecodeError):
                pass
        return result

    # ============ 远程 HTTP + OAuth 调用 ============
    def _oauth_token(self) -> str:
        """获取 OAuth JWT（client_credentials）"""
        if self._token:
            return self._token
        import urllib.request
        import urllib.parse
        data = urllib.parse.urlencode({
            "client_id": self.client_id or "",
            "client_secret": self.client_secret or "",
            "scope": "tools/call",
        }).encode()
        req = urllib.request.Request(
            f"{self.remote_url}/oauth/token",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        self._token = body.get("access_token", "")
        return self._token

    def _http_call(self, tool_name: str, arguments: Dict) -> Dict:
        """通过 HTTP + OAuth 调用远程 QCM"""
        import urllib.request
        import urllib.error
        token = self._oauth_token()
        request = {
            "jsonrpc": "2.0", "id": 1, "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments},
        }
        req = urllib.request.Request(
            f"{self.remote_url}/rpc",
            data=json.dumps(request, ensure_ascii=False).encode(),
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {token}"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout_s) as resp:
                parsed = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            return {"status": "failed", "error": f"HTTP {e.code}", "tool": tool_name}
        except Exception as e:
            return {"status": "failed", "error": str(e)[:200], "tool": tool_name}

        if "error" in parsed:
            return {"status": "failed", "error": parsed["error"], "tool": tool_name}
        result = parsed.get("result", {})
        content = result.get("content", [])
        if content and isinstance(content, list):
            try:
                return json.loads(content[0]["text"])
            except (KeyError, IndexError, json.JSONDecodeError):
                pass
        return result

    # ============ 统一入口 ============
    def call(self, tool_name: str, arguments: Dict) -> Dict:
        """统一调用（远程优先 → 本地 stdio）"""
        if self.remote_url:
            return self._http_call(tool_name, arguments)
        return self._stdio_call(tool_name, arguments)

    # ============ 常用工具封装 ============
    def research(self, query: str, level_hint: str = "T2") -> Dict:
        """QCM 端到端质量调研（4 形态输出）"""
        return self.call("qcm_research", {"query": query, "level_hint": level_hint})

    def validate(self, text: str, form: str = "quick-response") -> Dict:
        """QCM 输出校验（4 形态 40 检查）"""
        return self.call("qcm_validate", {"text": text, "form": form})

    def gap_detect(self, case: Dict) -> Dict:
        """QCM 5 维缺口检测"""
        return self.call("qcm_gap_detect", {"case": case})


if __name__ == "__main__":
    # Demo
    client = QCMClient()
    r = client.research("焊接虚焊客诉", level_hint="T2")
    print(f"QCM research: status={r.get('status', 'ok')} form={r.get('form', '?')} version={r.get('version', '?')}")
