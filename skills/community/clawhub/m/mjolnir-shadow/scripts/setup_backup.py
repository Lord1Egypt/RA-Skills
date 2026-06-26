#!/usr/bin/env python3
"""Mjolnir Shadow (雷神之影) - Interactive Setup Wizard / 交互式配置向导"""

import json
import os
import subprocess
import sys
from pathlib import Path

def ask(prompt, default=None):
    suffix = f" [{default}]" if default else ""
    val = input(f"{prompt}{suffix}: ").strip()
    return val if val else default

def encrypt_config(config_file: Path, encrypted_file: Path):
    """Encrypt config with GPG / 使用 GPG 加密配置"""
    passphrase = ask("Set encryption passphrase for config / 设置配置加密密码")
    if not passphrase:
        print("⚠️  No passphrase set. Config stored unencrypted. / 未设密码，配置未加密。")
        return False
    
    result = subprocess.run(
        ["gpg", "--quiet", "--batch", "--yes", "--symmetric",
         "--cipher-algo", "AES256",
         "--passphrase", passphrase,
         "--output", str(encrypted_file),
         str(config_file)],
        capture_output=True, text=True
    )
    
    if result.returncode == 0:
        # Remove plaintext config
        config_file.unlink()
        print(f"🔒 Config encrypted: {encrypted_file}")
        print(f"   For non-interactive use, set MJOLNIR_SHADOW_PASS via gpg-agent or a secure secret store.")
        print(f"   ⚠️  Do NOT put the passphrase in cron commands or world-readable files.")
        print(f"   非交互运行时，通过 gpg-agent 或安全密钥存储设置 MJOLNIR_SHADOW_PASS。")
        print(f"   ⚠️  不要在 cron 命令或明文文件中写入密码。")
        return True
    else:
        print(f"⚠️  GPG encryption failed: {result.stderr}")
        return False

def main():
    print("🌑 Mjolnir Shadow (雷神之影) - Setup Wizard / 配置向导")
    print("=" * 50)
    print()

    skill_dir = Path(__file__).parent.parent
    config_dir = skill_dir / "config"
    config_dir.mkdir(exist_ok=True)
    config_file = config_dir / "backup-config.json"
    encrypted_file = config_dir / "backup-config.json.gpg"

    # Load existing config if present / 加载已有配置
    existing = {}
    if encrypted_file.exists():
        print("🔒 Encrypted config found. Decrypting... / 发现加密配置，正在解密...")
        passphrase = ask("Enter passphrase / 输入密码")
        result = subprocess.run(
            ["gpg", "--quiet", "--batch", "--yes",
             "--passphrase", passphrase,
             "--decrypt", str(encrypted_file)],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            existing = json.loads(result.stdout)
            print("✅ Decrypted. Press Enter to keep current values. / 解密成功，回车保留当前值。\n")
        else:
            print("⚠️  Decryption failed. Starting fresh. / 解密失败，重新配置。\n")
    elif config_file.exists():
        existing = json.loads(config_file.read_text())
        print(f"📋 Existing config found. Press Enter to keep current values. / 发现已有配置。\n")

    # WebDAV Connection / WebDAV 连接
    print("── WebDAV Connection / WebDAV 连接 ──")
    webdav_url = ask("WebDAV URL (e.g. https://your-server/remote.php/webdav)",
                     existing.get("webdav_url", ""))
    
    # HTTPS warning / HTTPS 安全警告
    if webdav_url and not webdav_url.startswith("https://"):
        print("⚠️  WARNING: URL is not HTTPS! Credentials will be sent in plaintext.")
        print("   警告：URL 不是 HTTPS！凭证将以明文传输。")
        confirm = ask("Continue anyway? / 仍然继续？ (y/n)", "n")
        if confirm.lower() != "y":
            print("Aborted. Use HTTPS URL. / 已中止，请使用 HTTPS 地址。")
            sys.exit(1)
    
    webdav_user = ask("Username / 用户名", existing.get("webdav_user", ""))
    webdav_pass = ask("Password / 密码", existing.get("webdav_pass", ""))
    remote_dir = ask("Remote folder name / 远程文件夹名", existing.get("remote_dir", "openclaw-backups"))

    # Backup Settings / 备份设置
    print("\n── Backup Settings / 备份设置 ──")
    max_backups = int(ask("Max backups to keep / 最多保留几个备份", str(existing.get("max_backups", 3))))
    interval_days = int(ask("Backup interval (days) / 备份间隔（天）", str(existing.get("interval_days", 3))))

    # Paths / 路径
    print("\n── Paths / 路径 ──")
    workspace_path = ask("Workspace path / 工作空间路径",
                         existing.get("workspace_path", os.path.expanduser("~/.openclaw/workspace")))
    openclaw_dir = ask("OpenClaw dir / OpenClaw 目录",
                       existing.get("openclaw_dir", os.path.expanduser("~/.openclaw")))

    # What to backup / 备份内容
    print("\n── What to Back Up / 备份内容 ──")
    backup_workspace = ask("Back up workspace? / 备份工作空间？ (y/n)", "y").lower() == "y"
    backup_config = ask("Back up OpenClaw config? / 备份 OpenClaw 配置？ (y/n)", "y").lower() == "y"
    backup_strategies = ask("Back up strategies? / 备份策略文件？ (y/n)", "y").lower() == "y"
    backup_skills = ask("Back up skills? / 备份技能包？ (y/n)", "y").lower() == "y"
    
    # Security / 安全
    print("\n── Security / 安全设置 ──")
    exclude_auth = ask("Exclude channel auth tokens from backup? / 排除通道认证 token？ (y/n)", "y").lower() == "y"

    config = {
        "webdav_url": webdav_url.rstrip("/"),
        "webdav_user": webdav_user,
        "webdav_pass": webdav_pass,
        "remote_dir": remote_dir,
        "max_backups": max_backups,
        "interval_days": interval_days,
        "workspace_path": workspace_path,
        "openclaw_dir": openclaw_dir,
        "backup_workspace": backup_workspace,
        "backup_config": backup_config,
        "backup_strategies": backup_strategies,
        "backup_skills": backup_skills,
        "exclude_channel_auth": exclude_auth,
    }

    # Save config / 保存配置
    config_file.write_text(json.dumps(config, indent=2, ensure_ascii=False))
    print(f"\n💾 Config saved to: {config_file}")

    # Test connection via netrc (no -u flag) / 通过 netrc 测试连接（不暴露密码）
    print("\n🔌 Testing WebDAV connection... / 测试 WebDAV 连接...")
    try:
        import tempfile, urllib.parse
        host = urllib.parse.urlparse(webdav_url).hostname
        with tempfile.NamedTemporaryFile(mode='w', suffix='_netrc', delete=False) as nf:
            nf.write(f"machine {host}\nlogin {webdav_user}\npassword {webdav_pass}\n")
            netrc_path = nf.name
        os.chmod(netrc_path, 0o600)
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
             "--netrc-file", netrc_path,
             "-X", "PROPFIND", f"{webdav_url}/", "-H", "Depth: 0"],
            capture_output=True, text=True, timeout=10
        )
        os.unlink(netrc_path)
        code = result.stdout.strip()
        if code in ("207", "200"):
            print(f"✅ WebDAV OK (HTTP {code})")
        else:
            print(f"⚠️  WebDAV returned HTTP {code} — check URL and credentials")
            print(f"   检查 URL 和凭证是否正确")
    except Exception as e:
        print(f"⚠️  Connection test failed: {e}")
        try: os.unlink(netrc_path)
        except: pass

    # Encrypt config / 加密配置
    print("\n── Credential Security / 凭证安全 ──")
    do_encrypt = ask("Encrypt config with GPG? (recommended) / 使用 GPG 加密配置？（推荐） (y/n)", "y").lower() == "y"
    if do_encrypt:
        # Check GPG availability
        gpg_check = subprocess.run(["gpg", "--version"], capture_output=True)
        if gpg_check.returncode == 0:
            encrypt_config(config_file, encrypted_file)
        else:
            print("⚠️  GPG not found. Install gnupg to encrypt config. / 未找到 GPG，请安装 gnupg。")
            print("   Config remains unencrypted. / 配置保持未加密状态。")

    # Cron info / 定时任务信息
    print(f"\n── Cron Schedule / 定时任务 ──")
    cron_expr = f"0 3 */{interval_days} * *"
    print(f"📅 Recommended: {cron_expr} (every {interval_days} days at 03:00)")
    print(f"   建议：{cron_expr}（每 {interval_days} 天凌晨 3 点）")
    print(f"\n   Add via OpenClaw / 通过 OpenClaw 添加：")
    print(f'   openclaw cron add --name "🌑 Mjolnir Shadow" \\')
    print(f'     --schedule "{cron_expr}" --tz "Asia/Shanghai" \\')
    print(f'     --isolated --timeout 300 \\')
    print(f'     --message "bash {skill_dir}/scripts/backup.sh"')

    print(f"\n🌑 Setup complete! Run first backup / 配置完成！运行首次备份：")
    print(f"   bash {skill_dir}/scripts/backup.sh")

if __name__ == "__main__":
    main()
