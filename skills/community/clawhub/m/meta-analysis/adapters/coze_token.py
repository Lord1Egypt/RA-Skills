# NOTE: 本文件含混淆后的 PUBLIC 共用凭据（XOR+base64）。它不是真加密，仅防目录浏览明文暴露。
# 用户授权 2026-08-17：该 coze 长期 token 随 meta-analysis 技能公开发布（调用 coze 元分析工作流）。
"""meta-analysis 公共凭据库（XOR+base64 混淆内嵌，镜像 ct-advisor 的 EMBEDDED_SECRETS 模式）。

背景（2026-08-17）：用户授权将 coze 长期 token 随技能**公开发布**，避免每次经环境变量注入，
并规避「推送 config.json 泄露 JWT」风险（token 不在 config.json 明文、也不在 memory/笔记）。

重要：
- 这是 OBFUSCATION，NOT real encryption。混淆密钥随脚本发布，持脚本者即可还原。本库只放
  **公开的、随技能发布**的共用凭据（访问 meta-analysis coze 工作流的 token），请勿用私有凭据覆盖。
- 历史方案曾把 coze token 落盘到 config/coze.dat；但 SkillHub 窄白名单打包（仅
  .svg/.py/.md/.json/.yaml/.txt/.toml/.csv）不含 .dat，发布时被静默剥离 → 已安装技能读不到
  文件、连不上 coze。故改为**统一内嵌**（EMBEDDED_SECRETS），不再依赖外部 .dat 文件。本地仍可用
  store_token() 写覆盖文件（可选，优先级介于 env 与内嵌之间）。

读取优先级（通用 get_secret）：CLI > env > 局部落盘文件 > 内嵌 blob。三者皆无回退空串。
coze token 走便捷函数 get_token()，等价于 get_secret("meta_analysis_coze", ...)。
"""
from __future__ import annotations

import base64
import os

# 单份混淆密钥（所有公开凭据共用；都是公开凭据，无横向泄露风险）。
OBFUSCATION_KEY = b"meta-analysis-coze-obf-v1-9f2c"

# 内嵌公共凭据库：name -> XOR+base64 混淆 blob。
EMBEDDED_SECRETS = {
    "meta_analysis_coze": (
        "CBw-CU8mDQgjEDk6JlcqXjQMZBwrC1kGa25wUHsJLw0uC3hTITUhSj89G0UsKC8RYyg0CmM1AERjIX9RITE9UmIlCVIhAyZYKWkAGDcMZ1ZMA1Q8QU4KK1ssBC8bBWUzGQIWFgUlQWsUDilQRw1RFkE6XGNML1sUBDwsN0YoBBEOMB5QR0lSIQA_QwsJAms8YndSLAc0OAk6LmsJACxdLEM8H2sqIS9cQz01Fn0_XR1KL181WQY3KBsuKigUNDcgQWMJCEkrRwxXKX4BWExuIAIqBwoML1cGXC44GgQmJ04aIzkvVws1L0Q5WGdDBXUPAD8ZNBstF1gEGjQCBnRRVkw_floIBERPAk8KLEABKlwcO2tYHjsrLwYNNEFTCilcXTUmCR44W04JKXYAWSseLBgvFDBdNBkwRmMZDE8sRBgLBR48W2RTCVsCOlAdAx43GzsqQBsNK38MN0gjRzZQMFcVABQJBAAXAQcYWF07Kg5fNxkKQ2I3CAIqaQgYKFcVAGNtNwctKQZAKENRQCBaM14qKXU8NzI6Zw04XmAFa25UFEAuKB0gB1xUCCYGOCI4BUEpGEoPYSwoNEY7Q2JSUVQFOB8xNHwoHiQWHDhcNkEaWBkKYl0YDlQae09wFHwpPVAGUnQjBxEqHjooRF8CDBw6XhoFI041XG5IEmsvJVYSE3kTBlVcGyYYFk5RFjkMShUrAEBBcEJKDHcZOi07UmIpBD4VICQAXlo1P0k8dzdWOWEdWlxaMHYGXzw6IhUFCTg0ChVaGlsGJis6RTUzI34yA2tXUgstBisrKRgoIQkgID05O2APKwkmRwcpNmc5ch5LHnZbCRIuG1kWKxEDOikwR08xCkwrZDYUV04sU257VGEwJw0VDBwVL1MhOAYwCkUSCTkgSQsyCV1DY1V8IwMZHxIQL0cSMVQAHREQMhVaPUpURyEIOW5bYk5IAXNOACBZO0kNBxIpIwUTNlskKwAjWg=="
    ),
    # ct-meta2 工作流专属 token（aud=5v9HMQWtTSzxrEeZjI7kJJEzeMPrHXny）。与 ct-meta
    # 使用不同工作流 JWT（aud=oxwSsfwdtRRfByYIM8Xg3U4RQH5OgEjO），故按 endpoint 分别内嵌，不可混用。
    "ct_meta2_coze": (
        "CBw-CU8mDQgjEDk6JlcqXjQMZBwrC1kGa25wUHsJClU5NWhUNxstAz8-OlUtOD8RYysgDGAfARhgHHsaITIhU2MMJ1MjPTEEKXkuWjccZ1ZMA1Q8QU4KK1ssBC8bBWUzGQIWFgUlQWsUDilQRw1RFkE6XGNML1sUBDwsN0YoBBEOMBk_QWI2BzQwewtSMGs4B0hxLHQ5OxUFMnkFHDIHCTUMHnstOjIvZDglUxg_XR1KL181WQY3KBsuKigUNDcgQWMJCEkrRwxXKX4BWExuIAIqBwoML1cGXS8WKEMnGU5WIzkvVws1L0Q5WGdDBXUPAD8ZNBstF1gEGjQCBnRRVkw_floIBERPAk8KLEABKlwcO2tYHjsrLwYNNEFTCilcXTUmCR44W04NK1g2FSsOLB4uOjgUNicOR2A3Ik4sRBgLBR48W2RTCVsCOlAdAx43GzsqQBsNK38MN0gjRzZQMFcVABQJBAAXAQcYWF07Kg5fNxkKR2AZLkoqeSIYKHk7AGBTAQMuBzwOKENRQBInKEA_NGoHIxhUeCA9LkUFfHQUHHUbGCdCNHkSA1EhLB4DIl42P0IMVCJQDXsFSEBxJGYxNykrAEtUQywHPzYsRVskCAALTAETFnoTdn9aFFoTPRZDLVtZNyocSyw4EEI0JA80eCEOUlsYRn1mCGQqHEgABXgyLSsUFT8gK1sELQIHYVcXC2c9Q3JOPFZQLFESBF4nOzAzKwEcPRUQK05UTwE6KXshRWRBBHcOGi5AMmAiPSQ6QTkiH3ImDSwgYBU0EGA1QHpfPwFXXiIYBhU4NiUoTEYLG38wVxESYzwkVWApQm99JVdSBSMCOXxMNlQiMic4EXwgLjgjSDksOUkbS2N2DnAvCisyCXpQFyo5MBgvC2E3Nz8RHB8lAE4AQkVTMmhRGS4gIFQZODcoTh4ISlckJjgRaQozPmwAd39eMHE8WRMGAEo2PlkPACAeN04HJjFWbA=="
    ),
}

# 端点 → 内嵌凭据名 映射（per-endpoint token，2026-08-26）。
# 每个端点使用各自专属工作流 JWT，按 endpoint 分别解析（不可混用）。
ENDPOINT_TOKEN_MAP = {
    "https://ct-meta2.coze.site/run": "ct_meta2_coze",
    "https://ct-meta.coze.site/run": "meta_analysis_coze",
}


def _norm_url(u):
    return (u or "").rstrip("/")

# 局部落盘绝对路径（兼容历史：允许用户/作者用私有 key 覆盖内嵌默认值）。
DEFAULT_TOKEN_PATH = os.path.expanduser(
    "~/.workbuddy/skills/meta-analysis/config/coze.dat"
)

# coze token 的环境变量名（与 coze_client 的 COZE_META_TOKEN 一致）。
TOKEN_ENV = "COZE_META_TOKEN"


def obf_encode(plain: str, key: bytes) -> str:
    """XOR 每个字节与滚动密钥，再做 URL-safe base64（通用、key 参数化）。"""
    data = plain.encode("utf-8")
    xored = bytes(b ^ key[i % len(key)] for i, b in enumerate(data))
    return base64.urlsafe_b64encode(xored).decode("ascii")


def obf_decode(blob: str, key: bytes) -> str:
    """obf_encode 的逆操作（通用、key 参数化）。同一算法只此一份，
    bug_report 与 coze_token 各自传入自己的混淆 key，杜绝双份实现漂移。"""
    data = base64.urlsafe_b64decode(blob.strip())
    plain = bytes(b ^ key[i % len(key)] for i, b in enumerate(data))
    return plain.decode("utf-8")


# 兼容包装：coze_token 自身用主 key（OBFUSCATION_KEY）
def _obf_encode(plain: str) -> str:
    return obf_encode(plain, OBFUSCATION_KEY)


def _obf_decode(blob: str) -> str:
    return obf_decode(blob, OBFUSCATION_KEY)


def default_token_path() -> str:
    return DEFAULT_TOKEN_PATH


def store_token(plain: str, token_path: str = None) -> str:
    """混淆并落盘 token（可选覆盖文件）；返回实际写入路径。"""
    path = token_path or DEFAULT_TOKEN_PATH
    os.makedirs(os.path.dirname(path), exist_ok=True)
    blob = _obf_encode(plain.strip())
    with open(path, "w", encoding="utf-8") as f:
        f.write(blob)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    return path


def get_secret(name: str, cli_value: str = None, env_name: str = None,
               secret_path: str = None) -> str:
    """按名字取公开凭据：CLI > env > 局部文件 > 内嵌 blob。皆无回退空串。"""
    if cli_value:
        return cli_value
    if env_name:
        env = os.environ.get(env_name)
        if env:
            return env
    if secret_path and os.path.exists(secret_path):
        try:
            with open(secret_path, encoding="utf-8") as f:
                return _obf_decode(f.read())
        except Exception:
            pass
    blob = EMBEDDED_SECRETS.get(name)
    if blob:
        try:
            return _obf_decode(blob)
        except Exception:
            return ""
    return ""


def get_token(cli_token: str = None, token_path: str = None,
              token_env: str = TOKEN_ENV) -> str:
    """coze 便捷封装：等价于 get_secret("meta_analysis_coze", ...)。"""
    return get_secret("meta_analysis_coze", cli_token, token_env,
                      token_path or DEFAULT_TOKEN_PATH)


def get_token_for(endpoint: str = None, cli_token: str = None,
                  token_path: str = None, token_env: str = TOKEN_ENV) -> str:
    """按 endpoint 解析 coze token（per-endpoint token 模式，2026-08-26 改造）。

    优先级：cli > env(COZE_META_TOKEN，全局覆盖，对所有端点生效) >
    端点专属内嵌 blob(ENDPOINT_TOKEN_MAP) > 历史默认 blob(meta_analysis_coze)。

    - 主工作流 ct-meta2 用新 token（aud=5v9HMQWtTSzxrEeZjI7kJJEzeMPrHXny）；
    - 回退端点 ct-meta 用旧 token（aud=oxwSsfwdtRRfByYIM8Xg3U4RQH5OgEjO）；
    二者工作流 JWT 不同，必须按 endpoint 分别取用，不可混用。
    """
    if cli_token:
        return cli_token
    if token_env:
        env = os.environ.get(token_env)
        if env:
            return env
    if endpoint:
        name = ENDPOINT_TOKEN_MAP.get(_norm_url(endpoint))
        if name:
            blob = EMBEDDED_SECRETS.get(name)
            if blob:
                try:
                    return _obf_decode(blob)
                except Exception:
                    pass
    return get_secret("meta_analysis_coze", cli_token, token_env, token_path)
