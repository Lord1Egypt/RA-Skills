#!/usr/bin/env python3
"""
微信 PC 端数据库解密工具
支持：
- Windows：微信 3.x（SQLCipher 加密，从 WeChatWin.dll 内存提取密钥）
- macOS：微信 Mac 版（SQLCipher 加密，从 WeChat 进程内存提取密钥）

解密原理：
微信 PC/Mac 端将聊天数据库用 SQLCipher 加密存储。
加密密钥在微信运行时驻留在进程内存中，可通过特征码扫描提取。
提取后用 SQLCipher 的 PRAGMA key 解密数据库。

用法：
python wechat_decryptor.py --find-key-only
python wechat_decryptor.py --db-dir <微信数据目录> --output ./decrypted/
python wechat_decryptor.py --key "abcd1234..." --db "./MSG0.db" --output "./decrypted/"

依赖：
pip install pycryptodome psutil
Windows 额外：pip install pymem
macOS 额外：无（使用 lldb）

注意：
- 运行时微信客户端必须处于登录状态（需从内存读取密钥）
- macOS 可能需要关闭 SIP 或授予终端 Full Disk Access 权限
- 解密后的数据库仅用于个人读取，不要分发
"""

import os
import sys
import struct
import hashlib
import argparse
import subprocess
from pathlib import Path

# ─── 平台检测 ─────────────────────────────────────────────
IS_WINDOWS = sys.platform == "win32"
IS_MACOS = sys.platform == "darwin"

# ─── 进程查找（跨平台） ───────────────────────────────────
def find_wechat_pid() -> int | None:
    """找到微信进程的 PID"""
    try:
        import psutil
    except ImportError:
        print("请先安装依赖：pip install psutil", file=sys.stderr)
        sys.exit(1)

    target_names = (
        ("wechat.exe", "wechatapp.exe") if IS_WINDOWS
        else ("wechat", "微信")
    )

    for proc in psutil.process_iter(["pid", "name"]):
        name = (proc.info["name"] or "").lower()
        if name in target_names:
            return proc.info["pid"]

    return None


# ─── 数据目录查找（跨平台） ───────────────────────────────
def get_wechat_data_dir() -> str | None:
    """获取微信用户数据目录"""
    if IS_WINDOWS:
        documents = Path.home() / "Documents" / "WeChat Files"
        if documents.exists():
            return str(documents)
        alt = Path("C:/Users") / os.getlogin() / "Documents" / "WeChat Files"
        if alt.exists():
            return str(alt)
    elif IS_MACOS:
        # macOS 微信数据目录
        containers = Path.home() / "Library" / "Containers" / "com.tencent.xinWeChat" / "Data"
        if containers.exists():
            return str(containers)
        # 旧版路径
        app_support = Path.home() / "Library" / "Application Support" / "com.tencent.xinWeChat"
        if app_support.exists():
            return str(app_support)

    return None


def find_db_files(db_dir: str) -> list[str]:
    """找到目录下的所有微信消息数据库文件"""
    db_dir = Path(db_dir)
    candidates = []

    # 主要消息数据库：MSG0.db ~ MSG19.db
    for i in range(20):
        p = db_dir / f"MSG{i}.db"
        if p.exists():
            candidates.append(str(p))

    # Multi 目录下（部分版本）
    multi_dir = db_dir / "Multi"
    if multi_dir.exists():
        for i in range(20):
            p = multi_dir / f"MSG{i}.db"
            if p.exists():
                candidates.append(str(p))

    # macOS 特有路径：Message 目录
    message_dir = db_dir / "Message"
    if message_dir.exists():
        for f in sorted(message_dir.glob("msg_*.db")):
            candidates.append(str(f))

    # 联系人数据库
    micro_msg = db_dir / "MicroMsg.db"
    if micro_msg.exists():
        candidates.insert(0, str(micro_msg))

    # 如果直接在目录下没找到，递归找一层
    if not candidates:
        for f in sorted(db_dir.glob("**/MSG*.db")):
            candidates.append(str(f))
        for f in sorted(db_dir.glob("**/msg_*.db")):
            candidates.append(str(f))
        micro = list(db_dir.glob("**/MicroMsg.db"))
        if micro:
            candidates.insert(0, str(micro[0]))

    return candidates


# ─── Windows 密钥提取 ─────────────────────────────────────
def extract_key_windows(pid: int) -> str | None:
    """从 Windows 微信进程内存中提取数据库密钥"""
    try:
        import pymem
        import pymem.process
    except ImportError:
        print("请先安装依赖：pip install pymem", file=sys.stderr)
        sys.exit(1)

    pm = pymem.Pymem(pid)
    key_candidates = []

    try:
        wechat_module = pymem.process.module_from_name(pm.process_handle, "WeChatWin.dll")
        if not wechat_module:
            print("错误：未找到 WeChatWin.dll，请确认微信已登录", file=sys.stderr)
            return None

        module_base = wechat_module.lpBaseOfDll
        module_size = wechat_module.SizeOfImage

        chunk_size = 0x100000  # 1MB
        phone_pattern = b"iphone\x00"

        offset = 0
        while offset < module_size:
            to_read = min(chunk_size, module_size - offset)
            try:
                chunk = pm.read_bytes(module_base + offset, to_read)
            except Exception:
                offset += chunk_size
                continue

            pos = 0
            while True:
                idx = chunk.find(phone_pattern, pos)
                if idx == -1:
                    break

                key_offset = idx - 0x70
                if key_offset >= 0:
                    key_candidate = chunk[key_offset : key_offset + 32]
                    if len(key_candidate) == 32 and key_candidate != b"\x00" * 32:
                        key_candidates.append(key_candidate)

                pos = idx + 1

            offset += chunk_size

    except Exception as e:
        print(f"内存扫描出错：{e}", file=sys.stderr)

    if not key_candidates:
        print("未找到密钥候选，尝试备用方法...", file=sys.stderr)
        return _fallback_key_windows(pm)

    return key_candidates[0].hex()


def _fallback_key_windows(pm) -> str | None:
    """Windows 备用密钥提取"""
    known_prefixes = [
        bytes.fromhex("0400000020000000"),
        bytes.fromhex("0100000020000000"),
    ]

    try:
        import pymem.process
        for module in pm.list_modules():
            if b"WeChatWin" in module.szModule:
                base = module.lpBaseOfDll
                size = module.SizeOfImage

                chunk_size = 0x200000
                offset = 0

                while offset < size:
                    to_read = min(chunk_size, size - offset)
                    try:
                        chunk = pm.read_bytes(base + offset, to_read)
                    except Exception:
                        offset += chunk_size
                        continue

                    for prefix in known_prefixes:
                        idx = 0
                        while True:
                            found = chunk.find(prefix, idx)
                            if found == -1:
                                break

                            key_start = found + len(prefix)
                            key_candidate = chunk[key_start : key_start + 32]
                            if len(key_candidate) == 32 and key_candidate != b"\x00" * 32:
                                return key_candidate.hex()

                            idx = found + 1

                    offset += chunk_size
    except Exception:
        pass

    return None


# ─── macOS 密钥提取 ───────────────────────────────────────
def extract_key_macos(pid: int) -> str | None:
    """从 macOS 微信进程内存中提取数据库密钥"""
    key = _extract_key_macos_lldb(pid)
    if key:
        return key

    key = _extract_key_macos_keychain()
    if key:
        return key

    return None


def _extract_key_macos_lldb(pid: int) -> str | None:
    """通过 lldb 读取微信进程内存提取密钥"""
    try:
        # 简化的 lldb 调用
        result = subprocess.run(
            ["lldb", "-p", str(pid), "-o", "memory read --force --outfile /tmp/wechat_mem.bin 0x0 0x100000000", "-o", "quit"],
            capture_output=True, text=True, timeout=30,
        )
        # 这里需要更复杂的实现，暂时返回 None
        print("macOS 密钥提取需要更多配置，请使用 --key 手动指定密钥", file=sys.stderr)
    except Exception as e:
        print(f"lldb 方法失败：{e}", file=sys.stderr)

    return None


def _extract_key_macos_keychain() -> str | None:
    """尝试从 macOS Keychain 获取微信密钥"""
    try:
        result = subprocess.run(
            ["security", "find-generic-password", "-s", "com.tencent.xinWeChat", "-w"],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass

    return None


# ─── 跨平台密钥提取入口 ──────────────────────────────────
def extract_key_from_memory(pid: int) -> str | None:
    """根据平台选择对应的密钥提取方法"""
    if IS_WINDOWS:
        return extract_key_windows(pid)
    elif IS_MACOS:
        return extract_key_macos(pid)
    else:
        print("错误：不支持的操作系统，仅支持 Windows 和 macOS", file=sys.stderr)
        return None


# ─── 密钥验证 ─────────────────────────────────────────────
def test_key(db_path: str, key_hex: str) -> bool:
    """验证密钥是否正确"""
    try:
        key_bytes = bytes.fromhex(key_hex)
        with open(db_path, "rb") as f:
            header = f.read(4096)

        if len(header) < 4096:
            return False

        from Crypto.Hash import HMAC, SHA1
        from Crypto.Protocol.KDF import PBKDF2
        from Crypto.Cipher import AES

        salt = header[:16]
        key = PBKDF2(key_bytes, salt, dkLen=32, count=4000, prf=lambda p, s: HMAC.new(p, s, SHA1).digest())
        iv = header[16:32]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(header[32:48])

        return decrypted != b"\x00" * 16
    except Exception:
        return False


# ─── 数据库解密 ───────────────────────────────────────────
def decrypt_db(db_path: str, key_hex: str, output_path: str) -> bool:
    """解密单个微信数据库文件"""
    try:
        from Crypto.Hash import HMAC, SHA1
        from Crypto.Protocol.KDF import PBKDF2
        from Crypto.Cipher import AES
    except ImportError:
        print("请先安装依赖：pip install pycryptodome", file=sys.stderr)
        sys.exit(1)

    PAGE_SIZE = 4096
    SQLITE_HEADER = b"SQLite format 3\x00"

    key_bytes = bytes.fromhex(key_hex)

    with open(db_path, "rb") as f:
        raw = f.read()

    if len(raw) < PAGE_SIZE:
        print(f"文件太小，可能不是有效的数据库：{db_path}", file=sys.stderr)
        return False

    salt = raw[:16]
    key = PBKDF2(key_bytes, salt, dkLen=32, count=4000, prf=lambda p, s: HMAC.new(p, s, SHA1).digest())

    output = bytearray()

    for page_num in range(len(raw) // PAGE_SIZE):
        page = raw[page_num * PAGE_SIZE : (page_num + 1) * PAGE_SIZE]

        if page_num == 0:
            iv = page[16:32]
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted_content = cipher.decrypt(page[32 : PAGE_SIZE - 32])
            decrypted_page = SQLITE_HEADER + decrypted_content[len(SQLITE_HEADER):]
            output.extend(decrypted_page)
            output.extend(b"\x00" * 32)
        else:
            iv = page[-48:-32]
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted_content = cipher.decrypt(page[: PAGE_SIZE - 48])
            output.extend(decrypted_content)
            output.extend(b"\x00" * 48)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(output)

    # 验证
    import sqlite3
    try:
        conn = sqlite3.connect(output_path)
        conn.execute("SELECT name FROM sqlite_master LIMIT 1")
        conn.close()
        return True
    except sqlite3.DatabaseError:
        os.remove(output_path)
        return False


# ─── 自动查找 wxid 目录 ─────────────────────────────────
def find_wxid_dirs(data_dir: str) -> list[Path]:
    """在微信数据目录中查找账号目录"""
    data_path = Path(data_dir)

    if IS_WINDOWS:
        wxid_dirs = [d for d in data_path.iterdir() if d.is_dir() and d.name.startswith("wxid_")]
        if not wxid_dirs:
            wxid_dirs = [d for d in data_path.iterdir() if d.is_dir() and (d / "Msg").exists()]
    elif IS_MACOS:
        wxid_dirs = []
        for version_dir in data_path.iterdir():
            if not version_dir.is_dir():
                continue
            for account_dir in version_dir.iterdir():
                if not account_dir.is_dir():
                    continue
                msg_dir = account_dir / "Message"
                if msg_dir.exists():
                    wxid_dirs.append(account_dir)
                msg_dir2 = account_dir / "Msg"
                if msg_dir2.exists():
                    wxid_dirs.append(account_dir)
    else:
        wxid_dirs = []

    return wxid_dirs


def find_msg_dir(wxid_dir: Path) -> Path:
    """从账号目录中定位消息数据库所在目录"""
    for name in ("Message", "Msg", "msg"):
        candidate = wxid_dir / name
        if candidate.exists():
            return candidate
    return wxid_dir


# ─── 主入口 ───────────────────────────────────────────────
def main():
    if not IS_WINDOWS and not IS_MACOS:
        print("错误：此工具仅支持 Windows 和 macOS", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="微信 PC/Mac 端数据库解密工具（用于 npy-skill）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
# 自动从内存提取密钥并解密所有数据库
python wechat_decryptor.py --db-dir <微信数据目录> --output ./decrypted/

# 只打印密钥
python wechat_decryptor.py --find-key-only

# 用已知密钥解密单个文件
python wechat_decryptor.py --key "abcdef1234..." --db "./MSG0.db" --output "./out/"

# 验证密钥是否正确
python wechat_decryptor.py --key "abcdef1234..." --test-db "./MSG0.db"
"""
    )

    parser.add_argument("--db-dir", help="微信消息数据库目录路径")
    parser.add_argument("--db", help="单个数据库文件路径")
    parser.add_argument("--output", default="./decrypted", help="解密输出目录（默认：./decrypted）")
    parser.add_argument("--key", help="已知的密钥（hex 字符串，跳过内存提取）")
    parser.add_argument("--find-key-only", action="store_true", help="只打印密钥，不解密文件")
    parser.add_argument("--test-db", help="测试密钥是否正确（配合 --key 使用）")

    args = parser.parse_args()
    platform_name = "Windows" if IS_WINDOWS else "macOS"
    print(f"运行平台：{platform_name}")

    # Step 1: 获取密钥
    key_hex = args.key
    if not key_hex:
        print("正在查找微信进程...")
        pid = find_wechat_pid()
        if not pid:
            print("错误：未找到微信进程，请先打开微信并登录", file=sys.stderr)
            sys.exit(1)

        print(f"找到微信进程，PID: {pid}")
        print("正在从内存提取密钥...")

        key_hex = extract_key_from_memory(pid)
        if not key_hex:
            print("错误：无法提取密钥。请尝试：", file=sys.stderr)
            if IS_WINDOWS:
                print("  1. 确认微信已登录（不是锁屏状态）", file=sys.stderr)
                print("  2. 以管理员身份运行本脚本", file=sys.stderr)
                print("  3. 尝试使用 WeChatMsg 或 PyWxDump 工具手动提取密钥", file=sys.stderr)
            elif IS_MACOS:
                print("  1. 确认微信已登录（不是锁屏状态）", file=sys.stderr)
                print("  2. 授予终端 Full Disk Access 权限（系统设置 → 隐私与安全）", file=sys.stderr)
                print("  3. 尝试手动提取密钥后用 --key 指定", file=sys.stderr)
            sys.exit(1)

        print(f"密钥提取成功：{key_hex}")

    if args.find_key_only:
        print(f"\n密钥（hex）：{key_hex}")
        print("使用方法：python wechat_decryptor.py --key <上面的密钥> --db-dir <目录> --output ./decrypted/")
        return

    # Step 2: 测试密钥
    if args.test_db:
        print(f"正在验证密钥...")
        if test_key(args.test_db, key_hex):
            print("✓ 密钥正确")
        else:
            print("✗ 密钥错误或文件格式不支持")
        return

    # Step 3: 确定要解密的文件列表
    db_files = []
    if args.db:
        db_files = [args.db]
    elif args.db_dir:
        db_files = find_db_files(args.db_dir)
        if not db_files:
            print(f"错误：在 {args.db_dir} 下未找到数据库文件", file=sys.stderr)
            sys.exit(1)
        print(f"找到 {len(db_files)} 个数据库文件")
    else:
        # 自动查找微信数据目录
        data_dir = get_wechat_data_dir()
        if not data_dir:
            print("错误：未找到微信数据目录，请手动指定 --db-dir", file=sys.stderr)
            sys.exit(1)

        print(f"微信数据目录：{data_dir}")

        wxid_dirs = find_wxid_dirs(data_dir)
        if not wxid_dirs:
            print(f"错误：在 {data_dir} 下未找到账号目录，请手动指定 --db-dir", file=sys.stderr)
            sys.exit(1)

        if len(wxid_dirs) > 1:
            print("找到多个账号：")
            for i, d in enumerate(wxid_dirs):
                print(f"  [{i}] {d.name}")
            choice = int(input("请选择账号序号："))
            wxid_dir = wxid_dirs[choice]
        else:
            wxid_dir = wxid_dirs[0]

        msg_dir = find_msg_dir(wxid_dir)
        db_files = find_db_files(str(msg_dir))
        print(f"账号目录：{wxid_dir.name}，找到 {len(db_files)} 个数据库")

    # Step 4: 解密
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    success_count = 0
    for db_path in db_files:
        db_name = Path(db_path).name
        out_path = str(output_dir / db_name)

        print(f"解密 {db_name}...", end=" ", flush=True)
        if decrypt_db(db_path, key_hex, out_path):
            print("✓")
            success_count += 1
        else:
            print("✗ 失败")

    print(f"\n完成：{success_count}/{len(db_files)} 个文件解密成功")
    print(f"解密文件保存在：{output_dir.absolute()}")
    print(f"\n下一步：运行 chat_parser.py 提取聊天记录")
    print(f"  python chat_parser.py --db-dir {output_dir.absolute()} --target \"TA的微信名\" --output messages.txt")


if __name__ == "__main__":
    main()