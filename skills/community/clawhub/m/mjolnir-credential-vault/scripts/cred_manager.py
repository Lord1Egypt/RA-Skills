#!/usr/bin/env python3
"""
🔐 Credential Vault / 凭证加密管理模块 v1.3.0

GPG AES-256 symmetric encryption for centralized credential management.
GPG AES-256 对称加密，所有密码/Token 集中管理。

Dependencies / 依赖: Python 3.8+, GPG (gnupg)

Usage / 用法:
    from cred_manager import get_credential, add_credential

    # Get credential / 获取凭证
    password = get_credential('yizhan', 'pass')
    token = get_credential('github', 'token')

    # Get full service config / 获取完整服务配置
    config = get_service('yizhan')

    # Add/update credential / 添加/更新凭证
    add_credential('my_service', {'user': 'xxx', 'pass': 'yyy'})

First use / 首次使用:
    python3 cred_manager.py init
"""

import subprocess
import json
import os
import sys
import getpass
import tempfile
import stat

# ═══════════════════════════════════════════════════════════
# Config / 配置 — modify these to fit your environment
# 修改以下两项适配你的环境
# ═══════════════════════════════════════════════════════════

# Encrypted file path / 加密文件路径
CRED_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials.json.gpg')

# Master password: read from env var, never hardcode
# 主密码：从环境变量读取，不硬编码
# Set / 设置: export CRED_MASTER_PASS="your_password"
MASTER_PASS = os.environ.get('CRED_MASTER_PASS', '')

# ═══════════════════════════════════════════════════════════

_cache = None


def _get_master_pass():
    """Get master password. Env var first, otherwise interactive prompt.
    获取主密码，优先环境变量，否则交互输入。"""
    if MASTER_PASS:
        return MASTER_PASS
    return getpass.getpass('🔑 Enter master password / 输入主密码: ')


def _gpg_decrypt(password: str, input_file: str) -> str:
    """
    GPG decrypt via --passphrase-fd (stdin pipe).
    Avoids password appearing in command-line args (visible via ps aux).

    GPG 解密，通过 --passphrase-fd 从 stdin 传入密码。
    避免密码出现在命令行参数中。
    """
    proc = subprocess.Popen(
        ['gpg', '--batch', '--yes', '--passphrase-fd', '0',
         '--decrypt', input_file],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = proc.communicate(input=password.encode('utf-8'))
    if proc.returncode != 0:
        raise RuntimeError(f"Decryption failed (wrong password?) / 解密失败（密码错误？）: {stderr.decode()}")
    return stdout.decode('utf-8')


def _gpg_encrypt(password: str, input_file: str, output_file: str):
    """
    GPG encrypt via --passphrase-fd (stdin pipe).
    GPG 加密，通过 --passphrase-fd 从 stdin 传入密码。
    """
    proc = subprocess.Popen(
        ['gpg', '--batch', '--yes', '--passphrase-fd', '0',
         '--symmetric', '--cipher-algo', 'AES256',
         '-o', output_file, input_file],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    _, stderr = proc.communicate(input=password.encode('utf-8'))
    if proc.returncode != 0:
        raise RuntimeError(f"Encryption failed / 加密失败: {stderr.decode()}")


def _secure_write_temp(data: str) -> str:
    """
    Securely write to temp file:
    1. Set 600 permissions on creation (owner-only read/write)
    2. Use mkstemp for better control

    安全写入临时文件：
    1. 创建时设置 600 权限（仅 owner 可读写）
    2. 使用 mkstemp（更可控）

    Returns temp file path. Caller is responsible for deletion.
    返回临时文件路径，调用方负责删除。
    """
    fd, tmp_path = tempfile.mkstemp(suffix='.json', prefix='cred_')
    try:
        os.fchmod(fd, stat.S_IRUSR | stat.S_IWUSR)  # 600
        os.write(fd, data.encode('utf-8'))
    finally:
        os.close(fd)
    return tmp_path


def _secure_delete(path: str):
    """Securely delete temp file: overwrite then unlink.
    安全删除临时文件：先覆写再删除。"""
    try:
        size = os.path.getsize(path)
        with open(path, 'wb') as f:
            f.write(b'\x00' * size)  # zero overwrite / 零覆写
            f.flush()
            os.fsync(f.fileno())
        os.unlink(path)
    except OSError:
        # Worst case: at least try to delete / 最坏情况：至少尝试删除
        try:
            os.unlink(path)
        except OSError:
            pass


def _load_credentials():
    """Decrypt and load credentials (with in-memory cache).
    解密并加载凭证（带内存缓存）。"""
    global _cache
    if _cache is not None:
        return _cache

    if not os.path.exists(CRED_FILE):
        raise FileNotFoundError(
            f"Encrypted credential file not found / 加密凭证文件不存在: {CRED_FILE}\n"
            f"Run first / 请先运行: python3 cred_manager.py init"
        )

    password = _get_master_pass()
    plaintext = _gpg_decrypt(password, CRED_FILE)
    _cache = json.loads(plaintext)
    return _cache


def _save_credentials(creds: dict):
    """Encrypt and save credentials (temp file 600 + secure delete).
    加密并保存凭证（临时文件权限 600 + 安全删除）。"""
    password = _get_master_pass()
    json_str = json.dumps(creds, indent=2, ensure_ascii=False)

    tmp_path = _secure_write_temp(json_str)
    try:
        _gpg_encrypt(password, tmp_path, CRED_FILE)
        global _cache
        _cache = creds
    finally:
        _secure_delete(tmp_path)


def get_credential(service: str, key: str) -> str:
    """Get a specific field for a service / 获取指定服务的指定字段"""
    creds = _load_credentials()
    if service not in creds:
        raise KeyError(f"Service not found / 未找到服务: {service}, available / 可用: {list(creds.keys())}")
    if key not in creds[service]:
        raise KeyError(f"Field not found / 未找到字段: {key} in {service}, available / 可用: {list(creds[service].keys())}")
    return creds[service][key]


def get_service(service: str) -> dict:
    """Get full config for a service / 获取指定服务的完整配置"""
    creds = _load_credentials()
    if service not in creds:
        raise KeyError(f"Service not found / 未找到服务: {service}")
    return creds[service]


def list_services() -> list:
    """List all service names / 列出所有服务名"""
    creds = _load_credentials()
    return list(creds.keys())


def add_credential(service: str, data: dict):
    """Add or update a credential / 添加或更新凭证"""
    try:
        creds = _load_credentials()
    except FileNotFoundError:
        creds = {}
    creds[service] = data
    _save_credentials(creds)
    print(f"✅ Saved / 已保存: {service} ({', '.join(data.keys())})")


def remove_credential(service: str):
    """Remove a service's credentials / 删除一个服务的凭证"""
    creds = _load_credentials()
    if service not in creds:
        raise KeyError(f"Service not found / 未找到服务: {service}")
    del creds[service]
    _save_credentials(creds)
    print(f"🗑️ Removed / 已删除: {service}")


def init_credentials():
    """First-time init: set master password, create empty encrypted file.
    首次初始化：设置主密码，创建空的加密文件。"""
    if os.path.exists(CRED_FILE):
        print(f"⚠️  Encrypted file already exists / 加密文件已存在: {CRED_FILE}")
        confirm = input("Overwrite? / 覆盖？(y/N): ")
        if confirm.lower() != 'y':
            return

    print("🔐 Initializing Credential Vault / 初始化凭证管理系统")
    print("=" * 50)

    password = getpass.getpass("Set master password / 设置主密码: ")
    password2 = getpass.getpass("Confirm master password / 确认主密码: ")
    if password != password2:
        print("❌ Passwords don't match / 两次密码不一致")
        return

    if len(password) < 8:
        print("⚠️  Warning: password < 8 chars, consider a stronger one / 警告: 主密码少于 8 位，建议使用更强的密码")

    json_str = json.dumps({})
    tmp_path = _secure_write_temp(json_str)
    try:
        _gpg_encrypt(password, tmp_path, CRED_FILE)
    finally:
        _secure_delete(tmp_path)

    # Set .gpg file permissions to 600 / 设置 .gpg 文件权限为 600
    os.chmod(CRED_FILE, stat.S_IRUSR | stat.S_IWUSR)

    print(f"✅ Credential file created / 凭证文件已创建: {CRED_FILE}")
    print()
    print("📌 Next steps / 下一步:")
    print(f'  1. Set env var / 设置环境变量:')
    print(f'     Option A: export CRED_MASTER_PASS="your_password" (current terminal / 当前终端)')
    print(f'     Option B: Use a secrets manager / 使用密钥管理器')
    print(f'  2. Add credentials / 添加凭证: python3 cred_manager.py add <service>')
    print(f'  3. List credentials / 查看凭证: python3 cred_manager.py list')
    print()
    print("⚠️  Security notes / 安全提示:")
    print("  • Remember your master password — unrecoverable if lost / 主密码请牢记，丢失无法恢复")
    print("  • Back up .gpg file to a secure location / .gpg 文件请定期备份到安全位置")
    print("  • Don't store .gpg file and master password together / 不要将 .gpg 文件和主密码存放在同一处")


# ═══════════════════════════════════════════════════════════
# CLI Entry / 命令行入口
# ═══════════════════════════════════════════════════════════

def _cli():
    usage = """
🔐 Credential Vault / 凭证加密管理工具 v1.3.0

Commands / 命令:
  python3 cred_manager.py init                 Initialize / 首次初始化
  python3 cred_manager.py list                 List services / 列出所有服务
  python3 cred_manager.py get <svc> [field]    Get credential / 查看凭证
  python3 cred_manager.py add <svc>            Add (interactive) / 交互式添加
  python3 cred_manager.py remove <svc>         Remove service / 删除服务

Environment / 环境变量:
  CRED_MASTER_PASS    Master password (prompts if unset) / 主密码（不设置则交互输入）

Dependencies / 依赖:
  Python 3.8+, GPG (gnupg) — usually pre-installed on Linux/macOS
  Check / 检查: gpg --version
"""

    if len(sys.argv) < 2:
        print(usage)
        return

    cmd = sys.argv[1]

    if cmd == 'init':
        # Check GPG availability / 检查 GPG 是否可用
        try:
            subprocess.run(['gpg', '--version'], capture_output=True, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            print("❌ GPG not found. Please install first / 未找到 GPG，请先安装:")
            print("   Linux (Debian/Ubuntu): sudo apt install gnupg")
            print("   Linux (RHEL/CentOS):   sudo yum install gnupg2")
            print("   macOS:                 brew install gnupg")
            print("   Windows:               https://gpg4win.org")
            return
        init_credentials()

    elif cmd == 'list':
        services = list_services()
        print(f"📋 {len(services)} services stored / 已存储 {len(services)} 个服务:")
        for s in services:
            svc = get_service(s)
            print(f"  • {s} ({', '.join(svc.keys())})")

    elif cmd == 'get':
        if len(sys.argv) == 3:
            print(json.dumps(get_service(sys.argv[2]), indent=2, ensure_ascii=False))
        elif len(sys.argv) == 4:
            print(get_credential(sys.argv[2], sys.argv[3]))
        else:
            print("Usage / 用法: python3 cred_manager.py get <service> [field]")

    elif cmd == 'add':
        if len(sys.argv) < 3:
            print("Usage / 用法: python3 cred_manager.py add <service>")
            return
        service = sys.argv[2]
        print(f"Adding credential for / 添加凭证: {service}")
        print("Enter fields (format: key=value), empty line to finish / 输入字段 (格式: key=value)，空行结束:")
        data = {}
        while True:
            line = input("  > ").strip()
            if not line:
                break
            if '=' not in line:
                print("  Bad format, use key=value / 格式错误，用 key=value")
                continue
            k, v = line.split('=', 1)
            data[k.strip()] = v.strip()
        if data:
            add_credential(service, data)

    elif cmd == 'remove':
        if len(sys.argv) < 3:
            print("Usage / 用法: python3 cred_manager.py remove <service>")
            return
        remove_credential(sys.argv[2])

    elif cmd in ('--help', '-h', 'help'):
        print(usage)

    else:
        print(f"Unknown command / 未知命令: {cmd}")
        print(usage)


if __name__ == '__main__':
    _cli()
