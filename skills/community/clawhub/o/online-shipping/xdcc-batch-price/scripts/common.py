#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
common.py — 小递查查「快递报价查询」技能共用模块

集中存放：
  - 兜底提示文案（会话内自助排查 + 助手协助，不做外部联系渠道）
  - 网页登录 token 的读写（报价接口唯一需要的凭据）

注意（合规约束）：
  技能包内**不内置任何外部联系渠道**——不写第三方即时通讯账号、电子邮箱、
  电话、外部站点地址，也不夹带任何推广。兜底提示一律落在会话内，由助手
  继续协助排查。如需接入部署方自有支持渠道，请自行扩展 price_hint()，
  不要把这些账号写回本技能包（selftest 的零外部联系渠道扫描会拦截）。
"""

import os
import stat

# 报价接口唯一需要的凭据键（网页登录 token）
TOKEN_KEY = "XDCC_USER_TOKEN"


# --------------------------------------------------------------------------- #
# 兜底提示（统一出口）
#
# 设计原则：只给「下一步做什么」，不给「去哪里找人」。
# 原因：技能发布审核禁止带外部联系渠道；提示里出现即时通讯账号、电子邮箱
# 或外部站点地址会被判为违规内容而驳回。
# --------------------------------------------------------------------------- #
def price_hint(reason: str = "") -> str:
    """生成统一的兜底提示。reason 为可选的原因说明。"""
    lines = []
    if reason:
        lines.append(f"⚠️ 遇到问题：{reason}")
    lines.append("建议按以下顺序自助排查：")
    lines.append("  1. 执行 `web_login.py --check` 确认网页登录 token 是否存在")
    lines.append("  2. 若已过期，执行 `web_login.py --force` 重新登录"
                 "（登录页只有用户名+密码，给了账号就全自动）")
    lines.append("  3. 确认发件/收件的省市区填写完整（区县级缺失最容易导致查不到渠道）")
    lines.append("  4. 把这段报错原文发回会话，助手会带着上下文继续协助处理")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# 凭据读写
#
# 报价查询只用网页登录 token（存在浏览器 localStorage 里，会过期）。
# 写入时必须保留文件里已有的其他键，避免覆盖掉别的配置。
# --------------------------------------------------------------------------- #
def load_creds(path: str) -> dict:
    """从 .env 风格文件读取凭据（仅取 XDCC_ 前缀的键）。"""
    creds = {}
    if not os.path.isfile(path):
        return creds
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k, v = k.strip(), v.strip().strip('"').strip("'")
            if k.startswith("XDCC_"):
                creds[k] = v
    return creds


def update_creds(path: str, updates: dict) -> None:
    """就地更新凭据文件中的若干键，**保留其余键与注释**。"""
    lines = []
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            lines = f.read().split("\n")
    seen = set()
    out = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and "=" in stripped:
            k = stripped.split("=", 1)[0].strip()
            if k in updates:
                out.append(f"{k}={updates[k]}")
                seen.add(k)
                continue
        out.append(line)
    for k, v in updates.items():
        if k not in seen:
            out.append("")
            out.append("# 网页登录 token（JWT，会过期；报价接口 GetFreightPredictList 需要）")
            out.append(f"{k}={v}")
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out).rstrip("\n") + "\n")
    _tighten_creds_perm(path)


def get_token(creds_or_path) -> str:
    """从凭据 dict 或凭据文件路径取网页登录 token。"""
    creds = creds_or_path if isinstance(creds_or_path, dict) else load_creds(creds_or_path)
    return (creds.get(TOKEN_KEY) or "").strip()


def _tighten_creds_perm(path: str) -> None:
    """凭据含登录密钥，Unix 下收紧为仅本人可读写；Windows 无该语义，忽略。"""
    try:
        if os.name == "posix":
            os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass
