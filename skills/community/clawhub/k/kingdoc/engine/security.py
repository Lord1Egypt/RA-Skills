"""Security utilities for KingDoc — 文件类型拦截 / 输入校验 / 大小限制

禁止文件类型（来自产品安全规范，覆盖执行脚本、Office 二进制、归档镜像、系统文件等）：
  1. Windows 可执行 / 批处理脚本：.bat .cmd .ps1 .vbs .exe .dll .lnk .msi
  2. Office 二进制文档（默认拦截用户上传）：.docx .xlsx .pptx .doc .xls .ppt
                                     .xlsm .docm .pptm
  3. 二进制镜像 / 安装包：.iso .dmg .zip .rar .7z .tar .gz .apk .jar
  4. 系统缓存 / 隐藏文件：.DS_Store .git(.git 目录) .env .log .tmp
  5. 其他风险脚本：.sh .com .scr .hta .reg

设计原则：
- 用户「上传附件」一律按上述清单拦截（默认禁止），从源头杜绝把可执行/脚本/归档传上云。
- 技能「本地生成→上传覆盖」产物（docx/pptx/xlsx/pdf/svg/png/txt/md）属于白名单豁免，
  仅允许内部流水线写入，用户无法借道绕过。
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# 文件 ID 格式校验
# ---------------------------------------------------------------------------
FILE_ID_PATTERN = re.compile(r'^[a-zA-Z0-9_-]{8,64}$')

# ---------------------------------------------------------------------------
# 禁止（拦截）扩展名 —— 用户上传附件一律拦截
# ---------------------------------------------------------------------------
BLOCKED_EXTENSIONS = {
    # 1. Windows 可执行 / 批处理脚本
    '.bat', '.cmd', '.ps1', '.vbs', '.exe', '.dll', '.lnk', '.msi',
    # 2. Office 二进制文档（默认拦截用户上传；内部生成产物走豁免白名单）
    '.docx', '.xlsx', '.pptx', '.doc', '.xls', '.ppt',
    '.xlsm', '.docm', '.pptm',
    # 3. 二进制镜像 / 安装包
    '.iso', '.dmg', '.zip', '.rar', '.7z', '.tar', '.gz', '.apk', '.jar',
    # 4. 系统缓存 / 隐藏文件
    '.ds_store', '.env', '.log', '.tmp',
    # 5. 其他风险脚本
    '.sh', '.com', '.scr', '.hta', '.reg',
}

# 特殊目录名拦截（如 .git）
BLOCKED_DIR_NAMES = {'.git', '.svn', '.hg', '.idea', '__pycache__'}

# ---------------------------------------------------------------------------
# 内部豁免白名单 —— 仅技能「本地生成→上传覆盖」流水线可使用
# 注意：必须是技能自身生成的内容格式，用户无法借道上传任意同类文件
# ---------------------------------------------------------------------------
INTERNAL_ALLOWED_EXTENSIONS = {
    '.docx', '.pptx', '.xlsx', '.pdf', '.svg', '.png',
    '.jpg', '.jpeg', '.txt', '.md', '.csv', '.json', '.html',
}

# 危险 MIME 类型（兜底）
BLOCKED_MIME_TYPES = {
    'application/x-msdownload',
    'application/x-executable',
    'application/x-dosexec',
    'application/x-msdos-program',
    'application/x-powershell',
    'text/javascript',
    'application/javascript',
    'application/x-vbs',
    'application/x-bat',
    'application/x-ms-installer',
    'application/java-archive',
    'application/vnd.microsoft.portable-executable',
}

# 大小限制（字节）
SIZE_LIMITS = {
    'doc': 100 * 1024 * 1024,        # 100MB
    'sheet': 100 * 1024 * 1024,      # 100MB
    'ppt': 100 * 1024 * 1024,        # 100MB
    'image': 20 * 1024 * 1024,       # 20MB
    'attachment': 500 * 1024 * 1024  # 500MB
}


def validate_file_id(file_id: str) -> bool:
    """校验 file_id 格式"""
    return bool(FILE_ID_PATTERN.match(file_id))


def _norm_ext(filename: str) -> str:
    ext = Path(filename).suffix.lower()
    # 处理 ".DS_Store" 这种无点前缀的特殊文件名
    if not ext and filename.lower() == '.ds_store':
        ext = '.ds_store'
    return ext


def is_blocked_extension(filename: str, internal: bool = False) -> bool:
    """判断文件是否应被拦截。

    Args:
        filename: 文件名或路径
        internal: True 表示来自技能内部「本地生成→上传覆盖」流水线。
                  此时允许 INTERNAL_ALLOWED_EXTENSIONS 中的格式通过，
                  其余仍按 BLOCKED_EXTENSIONS 拦截。
    """
    name = Path(filename).name
    # .git 目录 / 隐藏目录名
    if name.lower() in BLOCKED_DIR_NAMES:
        return True
    ext = _norm_ext(filename)
    if ext in BLOCKED_EXTENSIONS:
        if internal and ext in INTERNAL_ALLOWED_EXTENSIONS:
            return False
        return True
    return False


def is_internal_allowed(filename: str) -> bool:
    """内部生成产物是否落在豁免白名单内。"""
    return _norm_ext(filename) in INTERNAL_ALLOWED_EXTENSIONS


def is_blocked_mime(content_type: str) -> bool:
    """校验 MIME 类型是否在黑名单"""
    return content_type.lower() in BLOCKED_MIME_TYPES


def check_size_limit(doc_type: str, file_size: int) -> bool:
    """校验文件大小是否超限"""
    limit = SIZE_LIMITS.get(doc_type, SIZE_LIMITS['attachment'])
    return file_size <= limit


def assert_upload_safe(filename: str, internal: bool = False) -> None:
    """上传前统一校验：命中拦截则抛出 FileTypeBlockedError。"""
    from engine.exceptions import FileTypeBlockedError
    if is_blocked_extension(filename, internal=internal):
        raise FileTypeBlockedError(Path(filename).suffix or '未知类型')
