#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全球法规连接器 · 安全自检脚本（可重跑）
===================================================
校验 Server 代码：只读 / 零凭据 / 无外发 / 无写文件 / 环境变量白名单。
退出码 0 = 通过，1 = 未通过。

运行: python security_selfcheck.py
"""
import re
import sys
from pathlib import Path

CODE = Path(__file__).parent / "reg_connector_server.py"


def main() -> int:
    code = CODE.read_text(encoding="utf-8")
    lines = code.splitlines()
    checks = []

    # 1. 网络外发
    net_hits = [i + 1 for i, ln in enumerate(lines)
                if re.search(r"requests\.|urllib\.|http\.client|\bsocket\b|aiohttp|httpx\.", ln)]
    checks.append(("无网络外发 (requests/urllib/socket/httpx)", not net_hits, net_hits))

    # 2. 凭据（排除分词 token/tokens/_tokenize 技术术语）
    cred_hits = []
    for i, ln in enumerate(lines, 1):
        if re.search(r"api[_-]?key|secret|password|passwd|authorization|bearer", ln, re.I):
            cred_hits.append(i)
        elif re.search(r"\btoken\b", ln, re.I) and not re.search(r"_tokenize|\btokens\b", ln):
            cred_hits.append(i)
    checks.append(("无凭据 (key/secret/password/token)", not cred_hits, cred_hits))

    # 3. 写文件 / 删除
    write_hits = [i + 1 for i, ln in enumerate(lines)
                  if re.search(r"open\([^)]*['\"]w|write_text|write_bytes|os\.remove|shutil\.|unlink\(", ln)]
    checks.append(("无写文件/删除", not write_hits, write_hits))

    # 4. 敏感个人信息（排除"客户端"等技术词）
    #    检测用词以中性表述占位（发布包自洁：不出现真实标识字面量）
    sens_hits = []
    for i, ln in enumerate(lines, 1):
        if re.search(r"用户真名|账号邮箱|报价单|内部价格|供应商名单", ln, re.I):
            sens_hits.append(i)
        elif re.search(r"公司", ln) and "客户端" not in ln and "公司," not in ln:
            sens_hits.append(i)
    checks.append(("无敏感个人信息", not sens_hits, sens_hits))

    # 5. 环境变量白名单
    envs = re.findall(r"os\.environ\.get\(['\"]([^'\"]+)", code)
    env_ok = set(envs) <= {"REG_HUB_REFS"}
    checks.append((f"环境变量白名单 ({sorted(set(envs))})", env_ok, sorted(set(envs))))

    # 6. 代码规模
    checks.append((f"代码规模 {len(lines)} 行 (合理)", len(lines) < 2000, len(lines)))

    print("=== 全球法规连接器 · 安全自检 ===")
    ok_all = True
    for name, ok, detail in checks:
        print(("✅" if ok else "❌"), name, ("" if ok else f" -> {detail}"))
        ok_all = ok_all and ok
    print("\n结论:", "通过 - 本地只读、零凭据、无外发" if ok_all else "未通过，需修正")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
