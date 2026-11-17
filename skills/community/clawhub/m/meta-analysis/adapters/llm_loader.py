#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ct-base · 后台大模型 key 安全加载器（共用）
==========================================
发布为应用后，后台若需调用大模型（家族统一 LongCat-2.0，2026-09-25 起；
旧 deepseek v4-flash 约定作废），一律通过本模块取 key，
**禁止在代码或配置里硬编码明文 key（sk- / ak_ 前缀）**。

加载优先级（env > 混淆文件）：
  1. 环境变量（默认 LONGCAT_API_KEY）—— 最高优先，部署时注入，明文不落盘
  2. 混淆 .py 文件（默认 config/llm_key.py）—— 其中的 LLM_API_KEY_BLOB 为
     XOR+base64 混淆 blob，防目录扫描/明文命中（非加密，等同 coze.dat 公用凭据）

⚠️ 发布安全规则：发布平台（GitHub / SkillHub / ClawHub）拒绝 .dat 文件，
   故家族凭据**一律用 .py 承载**，禁止落 .dat。

安全约束：
  - 本模块**绝不**把 key 明文打印到日志/异常/回显；异常只报「缺失/格式错误」，不泄露内容。

用法：
  from llm_loader import load_llm_key
  key = load_llm_key()                          # 读 LONGCAT_API_KEY，否则读 config/llm_key.py
  key = load_llm_key(key_path="config/llm_key.py")
"""
import os
import base64
import importlib.util

# 固定混淆密钥：公用凭据场景（非机器绑定），仅防目录浏览与扫描命中明文
_LLM_XOR_KEY = b"ct-base-llm-shared-v1"


def _xor_decode(blob: str) -> str:
    raw = base64.b64decode(blob.strip())
    return bytes(
        c ^ _LLM_XOR_KEY[i % len(_LLM_XOR_KEY)] for i, c in enumerate(raw)
    ).decode("utf-8")


def _xor_encode(plain: str) -> str:
    b = plain.encode("utf-8")
    x = bytes(c ^ _LLM_XOR_KEY[i % len(_LLM_XOR_KEY)] for i, c in enumerate(b))
    return base64.b64encode(x).decode("ascii")


def _read_blob_from_py(py_path: str) -> str:
    """动态加载 .py 模块，取其中的 LLM_API_KEY_BLOB 常量（不执行其它副作用代码外的导入）。"""
    try:
        spec = importlib.util.spec_from_file_location("_ct_llm_key", py_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return getattr(mod, "LLM_API_KEY_BLOB", "") or ""
    except Exception:
        raise RuntimeError(
            "加载 %s 失败：请确认其为本模块生成的混淆 .py（含 LLM_API_KEY_BLOB 常量）" % py_path
        )


def load_llm_key(env_name: str = "LONGCAT_API_KEY", key_path: str | None = None,
                 dat_path: str | None = None) -> str:
    """按 env > .py 混淆文件 优先级返回后台大模型 key（家族统一 LongCat-2.0）。缺失时抛 RuntimeError（不含明文）。"""
    v = (os.environ.get(env_name) or "").strip()
    if v:
        return v
    path = key_path or dat_path or "config/llm_key.py"
    if path.endswith(".py"):
        blob = _read_blob_from_py(path)
        if blob:
            return _xor_decode(blob)
        raise RuntimeError(
            "未在 %s 找到 LLM_API_KEY_BLOB 常量；请用 `python llm_loader.py gen <key>` 生成" % path
        )
    # 兼容 legacy .dat 文本读取（不推荐：发布平台会拒绝 .dat）
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return _xor_decode(f.read())
        except Exception:
            raise RuntimeError("llm key 文件解码失败：请检查 %s 是否为本模块生成的 XOR+base64 blob" % path)
    raise RuntimeError(
        "未找到后台大模型 key：请设置环境变量 %s，或在 %s 放置本模块生成的混淆 .py 文件"
        % (env_name, path)
    )


def encode_to_blob(plain: str) -> str:
    """将明文 key 生成为可写入 llm_key.py 的混淆 blob（CLI/本地一次性生成用，勿提交明文）。"""
    if not (plain.startswith("ak_") or plain.startswith("sk-")):
        raise ValueError("key 前缀异常（LongCat 应为 ak_；DeepSeek 旧 key 为 sk-）")
    return _xor_encode(plain)


if __name__ == "__main__":
    # 仅用于本地生成/校验 llm_key.py，不参与运行时
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "gen":
        if len(sys.argv) < 3:
            print("用法: python llm_loader.py gen <明文key>  -> 输出混淆 blob（请写入 config/llm_key.py 的 LLM_API_KEY_BLOB）")
        else:
            print(encode_to_blob(sys.argv[2]))
    else:
        print("llm_loader: 运行时请用 load_llm_key()。本地生成 blob 用 `python llm_loader.py gen <key>`")
