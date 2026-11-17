# -*- coding: utf-8 -*-
"""F8.1 自动修复 - 模组版本自动升级

当 F8 分析检测到模组版本问题时，本模块可自动下载推荐版本并替换旧文件。

安全机制：
- 操作前强制备份旧版本
- 支持回滚到修复前状态
- 详细日志记录每一步操作
"""

import json
import logging
import os
import shutil
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.error import URLError
from urllib.request import Request, urlopen

from core.i18n import t

logger = logging.getLogger(__name__)


class AutoFixResult:
    """自动修复结果"""

    def __init__(self):
        self.total_checked: int = 0
        self.fixed_count: int = 0
        self.skipped_count: int = 0
        self.failed_count: int = 0
        self.items: List[Dict[str, Any]] = []
        self.backup_dir: Optional[str] = None
        self.errors: List[str] = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_checked": self.total_checked,
            "fixed_count": self.fixed_count,
            "skipped_count": self.skipped_count,
            "failed_count": self.failed_count,
            "items": self.items,
            "backup_dir": self.backup_dir,
            "errors": self.errors,
        }


def _download_file(url: str, dest_path: Path, timeout: int = 30) -> bool:
    """下载文件

    Args:
        url: 下载 URL
        dest_path: 目标文件路径
        timeout: 超时时间（秒）

    Returns:
        是否成功
    """
    try:
        req = Request(url, headers={
            "User-Agent": "MC-Skill-AutoFix/1.0",
            "Accept": "*/*",
        })
        with urlopen(req, timeout=timeout) as resp:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            with open(dest_path, "wb") as f:
                shutil.copyfileobj(resp, f)
        return True
    except URLError as e:
        logger.error(f"下载失败 {url}: {e}")
        return False
    except Exception as e:
        logger.error(f"下载异常 {url}: {e}")
        return False


def _find_mod_jar(mods_dir: Path, mod_id: str, current_version: str) -> Optional[Path]:
    """在 mods 目录中查找指定模组的 JAR 文件

    Args:
        mods_dir: mods 目录路径
        mod_id: 模组 ID
        current_version: 当前版本号（可选，用于精确匹配）

    Returns:
        找到的 JAR 文件路径，或 None
    """
    if not mods_dir.exists():
        return None

    # 规范化模组 ID 的可能变体
    id_variants = {mod_id}
    # 尝试常见变体：小写、下划线/连字符替换
    id_variants.add(mod_id.lower())
    id_variants.add(mod_id.replace("_", "-").lower())
    id_variants.add(mod_id.replace("-", "_").lower())
    # 如果含下划线，尝试合并（如 create_addition -> createaddition）
    if "_" in mod_id:
        id_variants.add(mod_id.replace("_", "").lower())

    for jar_file in mods_dir.glob("*.jar"):
        jar_name = jar_file.name.lower()
        # 检查文件名是否包含模组 ID 的任何变体
        for variant in id_variants:
            if variant in jar_name:
                # 如果有版本号，尝试精确匹配
                if current_version and current_version.lower() in jar_name:
                    return jar_file
                # 如果文件名包含 "modid-version" 格式
                if variant in jar_name and (f"-{current_version}" in jar_name or f"_{current_version}" in jar_name):
                    return jar_file

    # 宽匹配：只按模组 ID 找
    for jar_file in mods_dir.glob("*.jar"):
        jar_name = jar_file.name.lower()
        for variant in id_variants:
            # 尝试匹配 "modid-" 或 "modid_" 开头
            if jar_name.startswith(f"{variant}-") or jar_name.startswith(f"{variant}_"):
                return jar_file
            # 或者文件名包含该变体
            if variant in jar_name:
                return jar_file

    return None


def auto_fix_mods(
    mods_dir: str,
    version_recommendations: List[Dict[str, Any]],
    backup_dir: Optional[str] = None,
    auto_confirm: bool = False,
) -> AutoFixResult:
    """执行模组自动修复

    Args:
        mods_dir: Minecraft 实例的 mods 目录路径
        version_recommendations: 版本推荐列表（来自 crash_analyzer）
        backup_dir: 备份目录（可选，默认在 mods_dir 同级创建）
        auto_confirm: 是否跳过确认提示

    Returns:
        AutoFixResult 结果对象
    """
    result = AutoFixResult()
    mods_path = Path(mods_dir)

    if not mods_path.exists():
        result.errors.append(f"mods 目录不存在: {mods_dir}")
        logger.error(result.errors[-1])
        return result

    # 确定需要升级的模组
    need_upgrade = []
    for rec in version_recommendations:
        status = rec.get("status", "")
        if status in ("outdated", "online_outdated", "recommend_update", "online_found"):
            download_url = rec.get("download_url", "")
            if download_url:
                need_upgrade.append(rec)
            elif rec.get("source") == "local":
                # 本地推荐的模组需要通过 Modrinth 再查一次
                need_upgrade.append(rec)

    if not need_upgrade:
        logger.info("没有需要升级的模组")
        return result

    logger.info(f"准备升级 {len(need_upgrade)} 个模组")

    # 处理确认
    if not auto_confirm:
        print(t("autofix.will_upgrade", count=len(need_upgrade)), flush=True)
        for rec in need_upgrade:
            mod_id = rec.get("mod_id", "?")
            current = rec.get("current_version", "?")
            recommended = rec.get("recommended_version", "?")
            status = rec.get("status", "?")
            print(t("autofix.mod_upgrade_info", mod=mod_id, current=current, recommended=recommended, status=status), flush=True)

        try:
            confirm = input(t("autofix.confirm_prompt")).strip().lower()
        except (EOFError, KeyboardInterrupt):
            confirm = "n"

        if confirm != "y":
            logger.info("用户取消自动修复")
            for rec in need_upgrade:
                item = {
                    "mod_id": rec.get("mod_id", ""),
                    "status": "cancelled",
                    "reason": "用户取消操作",
                }
                result.items.append(item)
                result.skipped_count += 1
            return result

    # 创建备份目录
    if backup_dir is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = str(mods_path.parent / f"backup_mods_{timestamp}")
    backup_path = Path(backup_dir)
    backup_path.mkdir(parents=True, exist_ok=True)
    result.backup_dir = backup_dir
    logger.info(f"备份目录: {backup_dir}")

    # 执行每个模组的升级
    for rec in need_upgrade:
        mod_id = rec.get("mod_id", "")
        current_version = rec.get("current_version", "")
        recommended_version = rec.get("recommended_version", "")
        download_url = rec.get("download_url", "")
        item = {
            "mod_id": mod_id,
            "name_cn": rec.get("name_cn", mod_id),
            "current_version": current_version,
            "recommended_version": recommended_version,
            "status": "pending",
            "backup_path": "",
            "new_path": "",
            "message": "",
        }

        # 如果没有下载链接，尝试通过 Modrinth 获取
        if not download_url:
            logger.info(f"[{mod_id}] 无直接下载链接，尝试联网查询...")
            try:
                from core.modrinth_client import get_latest_recommended_version
                mc_version = rec.get("mc_version", "")
                loader = rec.get("loader", "")
                if mc_version and loader:
                    online_result = get_latest_recommended_version(mod_id, mc_version, loader)
                    if online_result and online_result.get("download_url"):
                        download_url = online_result["download_url"]
                        item["download_filename"] = online_result.get("download_filename", "")
                        logger.info(f"  获取到下载链接: {download_url[:60]}...")
            except Exception as e:
                logger.warning(f"  Modrinth 查询失败: {e}")

        if not download_url:
            item["status"] = "skipped"
            item["message"] = "无可用下载链接，请手动下载"
            result.skipped_count += 1
            result.items.append(item)
            continue

        # 1. 查找旧文件
        old_jar = _find_mod_jar(mods_path, mod_id, current_version)
        if old_jar:
            logger.info(f"[{mod_id}] 找到旧版本: {old_jar.name}")
        else:
            logger.warning(f"[{mod_id}] 未找到旧版本 JAR 文件")
            # 即使找不到旧文件，仍然下载新版本
            item["message"] = "未找到旧版本文件，直接安装新版本"

        # 2. 备份旧文件
        if old_jar:
            backup_file = backup_path / old_jar.name
            try:
                shutil.copy2(old_jar, backup_file)
                item["backup_path"] = str(backup_file)
                logger.info(f"  已备份: {backup_file.name}")
            except Exception as e:
                logger.error(f"  备份失败: {e}")
                item["status"] = "failed"
                item["message"] = f"备份失败: {str(e)}"
                result.failed_count += 1
                result.items.append(item)
                continue

        # 3. 下载新版本
        filename = rec.get("download_filename", "")
        if not filename:
            # 从 URL 推断文件名
            from urllib.parse import urlparse
            path = urlparse(download_url).path
            filename = Path(path).name
            if not filename.endswith(".jar"):
                filename += ".jar"

        new_jar = mods_path / filename
        logger.info(f"[{mod_id}] 下载新版本: {filename}")

        success = _download_file(download_url, new_jar)
        if not success:
            item["status"] = "failed"
            item["message"] = "下载失败"
            result.failed_count += 1
            result.items.append(item)
            continue

        # 4. 删除旧版本（备份成功后）
        if old_jar and old_jar.exists():
            try:
                old_jar.unlink()
                logger.info(f"  已删除旧版本: {old_jar.name}")
            except Exception as e:
                logger.warning(f"  删除旧版本失败: {e}")
                # 不阻止继续，新版本已经下载

        # 5. 完成
        item["status"] = "fixed"
        item["new_path"] = str(new_jar)
        item["message"] = "升级成功"
        result.fixed_count += 1
        result.items.append(item)
        logger.info(f"[{mod_id}] ✅ 升级完成: {current_version} → {recommended_version}")

        # 短暂延迟，避免下载过快
        time.sleep(0.5)

    result.total_checked = len(need_upgrade)
    result.errors = [
        item["message"] for item in result.items
        if item["status"] == "failed"
    ]

    logger.info(
        f"自动修复完成: 修复{result.fixed_count}, "
        f"跳过{result.skipped_count}, 失败{result.failed_count}"
    )
    return result


def generate_fix_report(
    result: AutoFixResult,
    mods_dir: str,
    output_dir: Optional[str] = None,
) -> str:
    """生成修复报告

    Args:
        result: 修复结果
        mods_dir: mods 目录路径
        output_dir: 输出目录

    Returns:
        报告文件路径
    """
    if output_dir is None:
        import config
        output_dir = str(config.OUTPUT_DIR / "reports")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 生成 HTML 报告
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>F8.1 自动修复报告</title>
    <style>
        body {{ font-family: "Microsoft YaHei", Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        .summary {{ display: flex; gap: 20px; margin: 20px 0; }}
        .summary-card {{ flex: 1; padding: 20px; border-radius: 8px; text-align: center; }}
        .card-success {{ background: #d4edda; color: #155724; }}
        .card-warn {{ background: #fff3cd; color: #856404; }}
        .card-error {{ background: #f8d7da; color: #721c24; }}
        .card-info {{ background: #d1ecf1; color: #0c5460; }}
        .card-number {{ font-size: 36px; font-weight: bold; display: block; }}
        .card-label {{ font-size: 14px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
        th, td {{ padding: 10px 12px; text-align: left; border: 1px solid #ddd; }}
        th {{ background: #34495e; color: white; }}
        tr:nth-child(even) {{ background: #f8f9fa; }}
        .badge {{ display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 12px; }}
        .badge-success {{ background: #28a745; color: white; }}
        .badge-warn {{ background: #ffc107; color: #212529; }}
        .badge-error {{ background: #dc3545; color: white; }}
        .badge-info {{ background: #17a2b8; color: white; }}
        .info-box {{ background: #e8f4f8; padding: 15px; border-radius: 6px; margin: 15px 0; }}
        .code {{ font-family: Consolas, monospace; background: #f8f8f8; padding: 2px 5px; border-radius: 3px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>F8.1 自动修复报告</h1>
        <p>生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>

        <div class="info-box">
            <strong>mods 目录:</strong> <span class="code">{mods_dir}</span><br>
            <strong>备份目录:</strong> <span class="code">{result.backup_dir or '无'}</span>
        </div>

        <h2>修复概览</h2>
        <div class="summary">
            <div class="summary-card card-info">
                <span class="card-number">{result.total_checked}</span>
                <span class="card-label">检查总数</span>
            </div>
            <div class="summary-card card-success">
                <span class="card-number">{result.fixed_count}</span>
                <span class="card-label">修复成功</span>
            </div>
            <div class="summary-card card-warn">
                <span class="card-number">{result.skipped_count}</span>
                <span class="card-label">跳过</span>
            </div>
            <div class="summary-card card-error">
                <span class="card-number">{result.failed_count}</span>
                <span class="card-label">失败</span>
            </div>
        </div>

        <h2>修复详情</h2>
        <table>
            <thead>
                <tr>
                    <th>模组</th>
                    <th>版本变化</th>
                    <th>状态</th>
                    <th>说明</th>
                </tr>
            </thead>
            <tbody>
"""

    for item in result.items:
        status = item.get("status", "?")
        if status == "fixed":
            badge_html = '<span class="badge badge-success">✅ 成功</span>'
        elif status == "failed":
            badge_html = '<span class="badge badge-error">❌ 失败</span>'
        elif status == "skipped":
            badge_html = '<span class="badge badge-warn">⏭ 跳过</span>'
        elif status == "cancelled":
            badge_html = '<span class="badge badge-info">🚫 取消</span>'
        else:
            badge_html = f'<span class="badge badge-info">{status}</span>'

        html_content += f"""
                <tr>
                    <td><strong>{item.get('name_cn', item.get('mod_id', ''))}</strong><br><small>{item.get('mod_id', '')}</small></td>
                    <td>{item.get('current_version', '?')} → <strong>{item.get('recommended_version', '?')}</strong></td>
                    <td>{badge_html}</td>
                    <td>{item.get('message', '')}</td>
                </tr>
"""

    html_content += f"""
            </tbody>
        </table>

        <h2>回滚说明</h2>
        <div class="info-box">
            <p>如果修复后游戏出现问题，可从备份目录恢复旧版本:</p>
            <p><strong>备份路径:</strong> <span class="code">{result.backup_dir or '无'}</span></p>
            <p><strong>恢复方法:</strong> 将备份目录中的 JAR 文件复制回 mods 目录即可。</p>
        </div>

        <h2>后续建议</h2>
        <ul>
            <li>重启游戏测试新版本模组是否正常运行</li>
            <li>如果仍有问题，可查看完整的崩溃报告分析</li>
            <li>下次运行前建议先清理缓存</li>
        </ul>

        <p style="margin-top: 30px; color: #888; font-size: 12px;">
            MC 全生态智能适配工程师 V1 - F8.1 自动修复
        </p>
    </div>
</body>
</html>
"""

    report_path = output_path / f"auto_fix_report_{timestamp}.html"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    logger.info(f"修复报告: {report_path}")
    return str(report_path)


def auto_fix_run(args) -> Dict[str, Any]:
    """F8.1 自动修复主入口

    Args:
        args: argparse.Namespace，需包含:
            - crash_log: crash report文件路径（用于分析）
            - mods_dir: Minecraft的mods目录路径
            - output: 输出目录（可选）
            - offline: 是否禁用联网
            - auto_confirm: 是否跳过确认

    Returns:
        统一返回结构
    """
    import config
    from core.crash_analyzer import run as crash_analyzer_run

    mods_dir = getattr(args, "fix_mods_dir", None)
    crash_log = getattr(args, "crash_log", None)
    output_dir = getattr(args, "output", None)
    offline = getattr(args, "offline", False)
    auto_confirm = getattr(args, "auto_confirm", False)

    if not mods_dir:
        return config.make_result(
            status="error",
            feature="F8.1",
            input_summary={"mods_dir": None},
            result={"error": "缺少 --mods-dir 参数"},
            errors=["必须指定 Minecraft 的 mods 目录路径"],
        )

    if not crash_log:
        return config.make_result(
            status="error",
            feature="F8.1",
            input_summary={"mods_dir": mods_dir},
            result={"error": "缺少 --crash-log 参数"},
            errors=["必须指定 crash report 文件路径"],
        )

    mods_path = Path(mods_dir)
    if not mods_path.exists():
        return config.make_result(
            status="error",
            feature="F8.1",
            input_summary={"mods_dir": mods_dir},
            result={"error": f"mods 目录不存在: {mods_dir}"},
            errors=[f"请确认路径正确: {mods_dir}"],
        )

    logger.info(f"开始自动修复: mods_dir={mods_dir}, crash_log={crash_log}")

    # Step 1: 先运行 F8 分析获取版本推荐
    logger.info("Step 1: 运行崩溃分析...")
    analyzer_args = type("Args", (), {
        "crash_log": crash_log,
        "output": output_dir,
        "offline": offline,
    })()
    analysis_result = crash_analyzer_run(analyzer_args)

    if analysis_result.get("status") != "success":
        return config.make_result(
            status="error",
            feature="F8.1",
            input_summary={"mods_dir": mods_dir, "crash_log": crash_log},
            result={"error": "崩溃分析失败，无法执行自动修复", "analysis": analysis_result.get("result", {})},
            errors=["请先查看崩溃分析报告，解决基本错误后再尝试修复"],
        )

    version_recommendations = analysis_result["result"].get("version_recommendations", [])
    if not version_recommendations:
        return config.make_result(
            status="success",
            feature="F8.1",
            input_summary={"mods_dir": mods_dir, "crash_log": crash_log},
            result={
                "message": "未检测到需要升级的模组",
                "version_recommendations": [],
                "fix_result": {"total_checked": 0, "fixed_count": 0},
            },
            output_files=analysis_result.get("output_files", {}),
        )

    # Step 2: 执行自动修复
    logger.info(f"Step 2: 执行自动修复（{len(version_recommendations)} 个候选模组）...")
    fix_result = auto_fix_mods(
        mods_dir=mods_dir,
        version_recommendations=version_recommendations,
        auto_confirm=auto_confirm,
    )

    # Step 3: 生成报告
    logger.info("Step 3: 生成修复报告...")
    report_path = generate_fix_report(
        result=fix_result,
        mods_dir=mods_dir,
        output_dir=output_dir,
    )

    # 汇总结果
    fix_dict = fix_result.to_dict()

    return config.make_result(
        status="success",
        feature="F8.1",
        input_summary={
            "mods_dir": mods_dir,
            "crash_log": crash_log,
        },
        result={
            "fix_result": fix_dict,
            "fixed_items": [
                item for item in fix_dict["items"] if item["status"] == "fixed"
            ],
            "failed_items": [
                item for item in fix_dict["items"] if item["status"] == "failed"
            ],
            "skipped_items": [
                item for item in fix_dict["items"] if item["status"] == "skipped"
            ],
            "backup_dir": fix_dict["backup_dir"],
            "next_steps": [
                "重启 Minecraft 测试新版本模组",
                "如果出现问题，从备份目录恢复旧版本",
                "再次运行 F8 分析确认问题已解决",
            ],
        },
        output_files={
            "analysis_report": analysis_result.get("output_files", {}).get("report", ""),
            "fix_report": report_path,
        },
    )
