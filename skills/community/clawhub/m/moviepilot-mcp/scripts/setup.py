#!/usr/bin/env python3
"""MoviePilot MCP 配置向导

Usage:
  python3 setup.py
  python3 setup.py '{"base_url":"http://your-server:3001","apikey":"your-api-key"}'
"""

import sys, json, os, subprocess

SKILL_DIR = os.path.dirname(os.path.abspath(__file__)).rsplit("/scripts", 1)[0]
CONFIG_PATH = os.path.join(SKILL_DIR, "config.json")


def save_config(base_url: str, apikey: str):
    base_url = base_url.rstrip("/")
    config = {"base_url": base_url, "apikey": apikey}
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    masked = apikey[:4] + "*" * (len(apikey) - 4) if len(apikey) > 4 else "***"
    print(f"✓ 配置已写入 {CONFIG_PATH}")
    print(f"  服务器: {base_url}")
    print(f"  API Key: {masked}")


def validate_connection(base_url: str, apikey: str):
    """Try listing tools — uses curl subprocess for Unicode-safe URL handling."""
    url = f"{base_url}/api/v1/mcp/tools?apikey={apikey}"
    try:
        proc = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url],
            capture_output=True, text=True, timeout=15
        )
        http_code = proc.stdout.strip()
        if http_code == "200":
            # Get actual tool count
            proc2 = subprocess.run(
                ["curl", "-s", url],
                capture_output=True, text=True, timeout=15
            )
            try:
                data = json.loads(proc2.stdout)
                if isinstance(data, list):
                    print(f"✓ 连接成功！检测到 {len(data)} 个可用工具")
                    return True
            except json.JSONDecodeError:
                pass
            print("✓ 连接成功")
            return True
        elif http_code == "401":
            print("✗ 认证失败 (HTTP 401)，API Key 无效")
            return False
        else:
            print(f"✗ HTTP {http_code}")
            return False
    except subprocess.TimeoutExpired:
        print(f"✗ 连接超时 — 无法访问 {base_url}")
        print("  请确认服务是否运行、地址及端口是否正确")
        return False
    except FileNotFoundError:
        print("✗ 未找到 curl 命令，请安装 curl")
        return False
    except Exception as e:
        print(f"✗ 连接失败: {e}")
        return False


def interactive_setup():
    print("=" * 50)
    print("  MoviePilot MCP 技能 — 配置向导")
    print("=" * 50)
    print()

    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, encoding="utf-8") as f:
            existing = json.load(f)
        existing_url = existing.get("base_url", "?")
        print(f"已有配置：{existing_url}")
        use = input("使用已有配置？[Y/n] ").strip().lower()
        if use in ("", "y", "yes"):
            base_url = existing.get("base_url", "")
            apikey = existing.get("apikey", "")
            if base_url and apikey:
                validate_connection(base_url, apikey)
                return
        print()

    # Step 1
    print("— 第 1 步：MoviePilot 服务器地址 —")
    print("  格式：http://IP:端口  (默认端口 3001)")
    print("  示例：http://192.168.1.100:3001 或 http://nas.local:3001")
    print()
    while True:
        base_url = input("  服务器地址: ").strip()
        if not base_url:
            print("  ⚠ 地址不能为空"); continue
        if not base_url.startswith("http"):
            base_url = f"http://{base_url}"
        break

    print()
    print("— 第 2 步：API 密钥（API_TOKEN）—")
    print("  到哪里找？")
    print("    A. MoviePilot Web UI → 系统设定 → API_TOKEN")
    print("    B. 容器环境变量：docker inspect <容器> | grep API_TOKEN")
    print("    C. docker-compose.yml 中的 environment.API_TOKEN")
    print("    D. 容器启动日志：docker logs <容器> | grep -i token")
    print("    E. V1 默认值：moviepilot（强烈建议改掉）")
    print("    F. V2 要求 ≥16 个字符，不满足则自动重新生成")
    print("  详见 references/setup-guide.md")
    print()
    while True:
        apikey = input("  API Key: ").strip()
        if not apikey:
            print("  ⚠ API Key 不能为空"); continue
        break

    print()
    print("正在验证连接…")
    ok = validate_connection(base_url, apikey)
    print()

    if ok:
        save = input("保存配置？[Y/n] ").strip().lower()
        if save in ("", "y", "yes"):
            save_config(base_url, apikey)
        else:
            print("已取消。")
    else:
        print("验证失败。仍然保存？")
        save = input("保存？[y/N] ").strip().lower()
        if save in ("y", "yes"):
            save_config(base_url, apikey)
        else:
            print("已取消。")


def main():
    if len(sys.argv) > 1:
        try:
            cfg = json.loads(sys.argv[1])
        except json.JSONDecodeError:
            print("Error: JSON 格式不正确", file=sys.stderr)
            print('  示例: python3 setup.py \'{"base_url":"http://IP:3001","apikey":"my-key"}\'',
                  file=sys.stderr)
            sys.exit(1)

        base_url = cfg.get("base_url", "")
        apikey = cfg.get("apikey", "")
        if not base_url or not apikey:
            print("Error: 需要 base_url 和 apikey", file=sys.stderr)
            sys.exit(1)

        print(f"服务器: {base_url}")
        ok = validate_connection(base_url, apikey)
        if ok:
            save_config(base_url, apikey)
        elif sys.stdout.isatty():
            print("验证失败，是否仍然保存？[y/N] ", end="")
            if input().strip().lower() in ("y", "yes"):
                save_config(base_url, apikey)
            else:
                print("已取消。", file=sys.stderr)
                sys.exit(1)
        else:
            # Non-interactive → save anyway, server may be temporarily down
            print("⚠ 验证未通过，但已保存配置。网络恢复后可正常使用。")
            save_config(base_url, apikey)
    else:
        interactive_setup()


if __name__ == "__main__":
    main()
