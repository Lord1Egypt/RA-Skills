#!/usr/bin/env python3
"""
Outlook 日历助手 — 一键认证脚本
连接到你的 Outlook 个人日历，手机、电脑、网页同步更新

用法:
  python outlook_setup.py                      使用内置默认应用
  python outlook_setup.py <你的应用ID>          使用你自己的 Azure 应用
"""
import json, time, os, sys
import unicodedata

from ocal_i18n import t, set_lang
from ocal_bootstrap import ensure_deps, harden_stdio
from ocal_auth import SCOPES, TOKEN_PATH

DEFAULT_CLIENT_ID = "cfec5685-f41e-4be9-80db-08eeddd763ba"  # Azure App: Agent Skill - Outlook Calendar Management

def _vis_width(s):
    """算字符串在终端里占几列：CJK 全角字符算 2 列。

    :param s: 要显示的字符串
    :return: 显示宽度
    """
    return sum(2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1 for ch in s)


def _box(lines):
    """画认证信息框，宽度按内容自适应。

    中英文行宽不一样，手工垫空格必然对不齐，这里按实际显示宽度统一补。

    :param lines: 框内各行文本
    :return: 画好的多行字符串
    """
    w = max(_vis_width(line) for line in lines)
    out = ["┌" + "─" * (w + 2) + "┐"]
    for line in lines:
        pad = " " * (w - _vis_width(line))
        out.append(f"│ {line}{pad} │")
    out.append("└" + "─" * (w + 2) + "┘")
    return "\n".join(out)


def main():
    """设备码认证主流程：拿设备码 → 展示给用户 → 等授权 → 存 token。

    放进 main() 而不是模块顶层，是为了 import 时不触发流程（_box 等函数可以单测）。
    """
    set_lang()  # 文案跟随系统语言（与 outlook_cal.py 一致）；须在 ensure_deps 之前
    harden_stdio()  # 窄编码管道（Windows GBK）下 emoji 输出不崩
    ensure_deps()
    from msal import PublicClientApplication

    client_id = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CLIENT_ID

    print(t("setup_preparing"))

    for authority in ["consumers", "common"]:
        auth_url = f"https://login.microsoftonline.com/{authority}"
        try:
            app = PublicClientApplication(client_id, authority=auth_url)
            flow = app.initiate_device_flow(scopes=list(SCOPES))
            if "user_code" in flow:
                break
        except Exception:
            continue
    else:
        print()
        print(t("setup_fail_title"))
        print(t("setup_fail_1"))
        print(t("setup_fail_2"))
        print(t("setup_fail_3"))
        sys.exit(1)

    print()
    print(_box([
        t("setup_box_title"),
        "https://www.microsoft.com/link",
        "",
        t("setup_box_code"),
        f"      {flow['user_code']}",
        "",
        t("setup_box_login"),
    ]))
    print()
    print(t("setup_waiting"))

    result = app.acquire_token_by_device_flow(flow)

    if "access_token" in result:
        result["expires_at"] = time.time() + result.get("expires_in", 3600)
        result["_authority"] = authority
        result["client_id"] = client_id  # 存起来，续期时不需要再提供
        # 先写临时文件再原子替换：写入中途崩溃不会把 token 文件写坏成半截 JSON
        tmp = TOKEN_PATH + ".tmp"
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False)
            try:
                os.chmod(tmp, 0o600)  # token 含 access/refresh token，收紧权限
            except OSError:
                pass
            os.replace(tmp, TOKEN_PATH)
        finally:
            try:
                os.unlink(tmp)
            except OSError:
                pass
        claims = result.get("id_token_claims", {})
        account = claims.get("upn", claims.get("preferred_username", t("setup_your_account")))
        name = claims.get("name", "")
        print()
        print(t("setup_success"))
        if name:
            print(t("setup_welcome", name=name))
        print(t("setup_connected", account=account))
        print()
        print(t("setup_try"))
        print(t("setup_try_cmd"))
    else:
        error = result.get("error_description", result.get("error", "unknown"))
        if "expired" in error.lower():
            print(t("setup_expired"))
        elif "denied" in error.lower():
            print(t("setup_denied"))
        else:
            print(t("setup_failed"))
        sys.exit(1)


if __name__ == "__main__":
    main()
