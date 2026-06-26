#!/usr/bin/env python3
"""
和风天气 API 配置脚本
用于配置和风天气 API 的认证信息
"""

import argparse
import os
import sys


def main():
    parser = argparse.ArgumentParser(
        description="配置和风天气API认证信息",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # API KEY 方式(推荐)
  python configure.py --api-host "your-domain.qweatherapi.com" --api-key "your_key"

  # JWT 方式
  python configure.py --api-host "your-domain.qweatherapi.com" \\
    --project-id "your_project_id" \\
    --key-id "your_key_id" \\
    --private-key-path "./ed25519-private.pem"
        """
    )

    parser.add_argument("--api-host", required=True, help="API主机地址")
    parser.add_argument("--api-key", help="API KEY(推荐方式)")
    parser.add_argument("--project-id", help="项目ID(JWT方式)")
    parser.add_argument("--key-id", help="密钥ID(JWT方式)")
    parser.add_argument("--private-key-path", help="私钥文件路径(JWT方式)")
    parser.add_argument("--private-key", help="私钥内容字符串(JWT方式)")
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="不保存到配置文件（推荐：使用环境变量更安全）"
    )

    args = parser.parse_args()

    # 验证认证方式
    if args.api_key:
        auth_method = "api_key"
    elif args.project_id and args.key_id and (args.private_key_path or args.private_key):
        auth_method = "jwt"
    else:
        print("错误: 认证配置不完整", file=sys.stderr)
        print("\n请提供以下其中一种配置:", file=sys.stderr)
        print("  1. API KEY方式: --api-host + --api-key", file=sys.stderr)
        print("  2. JWT方式: --api-host + --project-id + --key-id + --private-key-path/--private-key", file=sys.stderr)
        sys.exit(1)

    # 设置环境变量
    os.environ["HEFENG_API_HOST"] = args.api_host
    if args.api_key:
        os.environ["HEFENG_API_KEY"] = args.api_key
    if args.project_id:
        os.environ["HEFENG_PROJECT_ID"] = args.project_id
    if args.key_id:
        os.environ["HEFENG_KEY_ID"] = args.key_id
    if args.private_key_path:
        os.environ["HEFENG_PRIVATE_KEY_PATH"] = args.private_key_path
    if args.private_key:
        os.environ["HEFENG_PRIVATE_KEY"] = args.private_key

    # 保存到文件
    if not args.no_save:
        config_dir = os.path.expanduser("~/.config/qweather")
        os.makedirs(config_dir, exist_ok=True, mode=0o700)
        config_file = os.path.join(config_dir, ".env")

        lines = [f"HEFENG_API_HOST={args.api_host}"]
        if args.api_key:
            lines.append(f"HEFENG_API_KEY={args.api_key}")
        if args.project_id:
            lines.append(f"HEFENG_PROJECT_ID={args.project_id}")
        if args.key_id:
            lines.append(f"HEFENG_KEY_ID={args.key_id}")
        if args.private_key_path:
            lines.append(f"HEFENG_PRIVATE_KEY_PATH={args.private_key_path}")
        if args.private_key:
            lines.append(f"HEFENG_PRIVATE_KEY={args.private_key}")

        try:
            # 创建文件并设置权限（仅所有者可读写）
            fd = os.open(config_file, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o600)
            with os.fdopen(fd, "w") as f:
                f.write("\n".join(lines))
            print(f"✓ 配置已保存到: {config_file}")
            print(f"  文件权限已设置为 600 (仅所有者可读写)")
        except Exception as e:
            print(f"✗ 保存配置文件失败: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("✓ 配置未保存到文件（使用 --no-save 选项）")

    print(f"✓ 配置成功 (认证方式: {auth_method})")
    print(f"\n现在可以使用其他查询脚本了!")


if __name__ == "__main__":
    main()
