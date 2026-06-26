"""
模板文件管理工具

提供模板文件的统一管理能力：
1. 在技能内部的 assets/template 目录下查找模板文件
2. 当本地没有模板文件时（如从 clawhub 等市场安装的 skill），
   自动从配置的互联网地址下载模板文件到本地

模板文件映射表（系统 -> 本地文件名 + 互联网 URL）
"""

import os
import sys
import logging
import shutil
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


# 模板文件映射表
# - local_name: 本地文件名（位于 skills/<skill-name>/assets/template/ 目录下）
# - url: 互联网地址（当本地不存在时从此地址下载）
# - target_system: 目标系统标识
TEMPLATE_REGISTRY: Dict[str, Dict[str, str]] = {
    'BIPV5': {
        'local_name': 'YYBIPV5_banktransaction.xlsx',
        'url': 'https://jreadstone.oss-cn-chengdu.aliyuncs.com/openclaw/20260605T013845-416575f8-yy_BIPV5.xlsx',
        'description': '用友BIPV5 银行流水处理 Excel 模板',
    },
    'EAS_YXH': {
        'local_name': 'eas_yxh_banktransaction.xlsx',
        'url': 'https://jreadstone.oss-cn-chengdu.aliyuncs.com/openclaw/20260605T013752-6cc346ac-eas_yxh_banktransaction.xlsx',
        'description': '金蝶云星瀚 离线明细导入 xlsx 模板',
    },
    'FINGARD': {
        'local_name': 'fingard_banktransaction.xls',
        'url': 'https://jreadstone.oss-cn-chengdu.aliyuncs.com/openclaw/20260605T013816-658ef205-fingard_banktransaction.xls',
        'description': '保融ATS 离线信息 xls 模板',
    },
    'NSTC': {
        'local_name': 'nstc_banktransaction.xls',
        'url': 'https://jreadstone.oss-cn-chengdu.aliyuncs.com/openclaw/20260605T013823-812632e0-nstc_banktransaction.xls',
        'description': '九恒星司库 批量导入银行明细格式 xls 模板',
    },
    'YYNCC': {
        'local_name': 'yyncc_banktransaction.xls',
        'url': 'https://jreadstone.oss-cn-chengdu.aliyuncs.com/openclaw/20260605T013834-1fbf67a8-yyncc_banktransaction.xls',
        'description': '用友NCC 数据页签 xls 模板',
    },
}


def get_skill_root() -> str:
    """获取技能根目录（包含 assets/template 的目录）

    模板文件位于 <skill_root>/assets/template/ 目录下。
    优先通过 SKILL.md 所在目录推断技能根目录。
    """
    # 当前文件: <skill_root>/scripts/core/template_manager.py
    current = os.path.abspath(__file__)
    # scripts/core/template_manager.py -> skill_root
    skill_root = os.path.dirname(os.path.dirname(os.path.dirname(current)))
    return skill_root


def get_template_dir() -> str:
    """获取模板目录绝对路径"""
    skill_root = get_skill_root()
    return os.path.join(skill_root, 'assets', 'template')


def ensure_template_dir() -> str:
    """确保模板目录存在，不存在则创建"""
    template_dir = get_template_dir()
    if not os.path.exists(template_dir):
        os.makedirs(template_dir, exist_ok=True)
        logger.info(f"已创建模板目录: {template_dir}")
    return template_dir


def get_template_path(target_system: str) -> Optional[str]:
    """获取目标系统对应的模板文件本地路径

    Args:
        target_system: 目标系统标识 (BIPV5, EAS_YXH, FINGARD, NSTC, YYNCC)

    Returns:
        模板文件的绝对路径；如果系统未注册则返回 None
    """
    target_upper = (target_system or '').upper()
    if target_upper not in TEMPLATE_REGISTRY:
        return None

    info = TEMPLATE_REGISTRY[target_upper]
    template_dir = ensure_template_dir()
    return os.path.join(template_dir, info['local_name'])


def download_template(target_system: str, force: bool = False) -> Optional[str]:
    """从互联网下载模板文件到本地

    Args:
        target_system: 目标系统标识
        force: 如果本地已存在，是否强制重新下载（默认 False）

    Returns:
        下载后的本地文件路径，下载失败返回 None
    """
    target_upper = (target_system or '').upper()
    if target_upper not in TEMPLATE_REGISTRY:
        logger.error(f"未注册的目标系统: {target_system}")
        return None

    info = TEMPLATE_REGISTRY[target_upper]
    template_dir = ensure_template_dir()
    local_path = os.path.join(template_dir, info['local_name'])
    url = info['url']

    # 已存在且不强制重下，直接返回
    if os.path.exists(local_path) and not force:
        logger.debug(f"模板文件已存在: {local_path}")
        return local_path

    # 尝试多种下载方式
    if _download_with_urllib(url, local_path):
        logger.info(f"已下载模板文件 [{target_upper}]: {local_path}")
        return local_path

    if _download_with_requests(url, local_path):
        logger.info(f"已下载模板文件 [{target_upper}]: {local_path}")
        return local_path

    logger.error(f"下载模板文件失败 [{target_upper}]: {url}")
    return None


def _download_with_urllib(url: str, dest_path: str, timeout: int = 60) -> bool:
    """使用 urllib 下载（标准库，无需额外依赖）"""
    try:
        import urllib.request
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'BIPPI-imp-trm-accstmt/1.0 (template-manager)'}
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
        if not data:
            return False
        with open(dest_path, 'wb') as f:
            f.write(data)
        return True
    except Exception as e:
        logger.debug(f"urllib 下载失败: {e}")
        return False


def _download_with_requests(url: str, dest_path: str, timeout: int = 60) -> bool:
    """使用 requests 下载（优先于 urllib）"""
    try:
        import requests
    except ImportError:
        return False
    try:
        resp = requests.get(url, timeout=timeout, stream=True)
        resp.raise_for_status()
        with open(dest_path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return True
    except Exception as e:
        logger.debug(f"requests 下载失败: {e}")
        return False


def resolve_template(target_system: str) -> Optional[str]:
    """解析模板路径：先在本地查找，不存在则自动从互联网下载

    这是模板加载的统一入口。
    优先级：
    1. 显式传入的 template_path（由调用方控制）
    2. 本地 assets/template/<local_name>
    3. 互联网 URL 下载到本地

    Args:
        target_system: 目标系统标识

    Returns:
        模板文件绝对路径；获取失败返回 None
    """
    target_upper = (target_system or '').upper()
    if target_upper not in TEMPLATE_REGISTRY:
        logger.error(f"未注册的目标系统: {target_system}")
        return None

    info = TEMPLATE_REGISTRY[target_upper]
    template_dir = ensure_template_dir()
    local_path = os.path.join(template_dir, info['local_name'])

    # 1) 本地存在 -> 直接返回
    if os.path.exists(local_path):
        return local_path

    # 2) 本地不存在 -> 从互联网下载
    logger.info(
        f"本地模板文件不存在 [{target_upper}]: {local_path}，"
        f"尝试从互联网下载..."
    )
    downloaded = download_template(target_upper)
    return downloaded


def list_registered_templates() -> Dict[str, Dict[str, str]]:
    """列出所有已注册的模板信息（用于诊断和展示）"""
    result = {}
    for sys_name, info in TEMPLATE_REGISTRY.items():
        local_path = os.path.join(get_template_dir(), info['local_name'])
        result[sys_name] = {
            **info,
            'local_path': local_path,
            'exists': os.path.exists(local_path),
        }
    return result


if __name__ == '__main__':
    # 命令行诊断工具
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    print("=" * 60)
    print(f"技能根目录: {get_skill_root()}")
    print(f"模板目录:   {get_template_dir()}")
    print("=" * 60)
    print("\n已注册模板列表:\n")
    for sys_name, info in list_registered_templates().items():
        exists_str = "✓ 存在" if info['exists'] else "✗ 缺失（将自动下载）"
        print(f"  [{sys_name}] {exists_str}")
        print(f"    本地文件: {info['local_name']}")
        print(f"    远程URL:  {info['url']}")
        print(f"    说明:     {info['description']}")
        print()
