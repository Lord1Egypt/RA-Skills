# -*- coding: utf-8 -*-
"""F6: 存档同步

通过百度网盘同步目录，实现PC与手机端MC存档的接力流转。
支持三种操作：setup（配置）、backup（备份）、restore（恢复）。

使用方式:
    from core.save_sync import run
    import argparse
    args = argparse.Namespace(action="backup", sync_dir="D:\\BaiduNetdisk\\MC同步", launcher="pcl2")
    result = run(args)
"""

import sys
import os
import json
import shutil
import zipfile
import platform
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import config
from utils.logger import get_logger
from utils.report_gen import ReportGenerator, generate_unified_output

logger = get_logger("save_sync")

# === 存档文件排除规则 ===
EXCLUDE_PATTERNS = [
    ".DS_Store",
    "Thumbs.db",
    "session.lock",
]

# === 同步配置文件名 ===
SYNC_CONFIG_FILE = "mc_sync_config.json"


def _get_default_minecraft_dir(launcher: str = "pcl2") -> Path:
    """获取默认的.minecraft目录路径"""
    system = platform.system()
    home = Path.home()

    if system == "Windows":
        # Windows默认路径
        if launcher == "netease":
            # 网易版
            return home / "AppData" / "Roaming" / "MCLDownload" / "Game"
        return home / "AppData" / "Roaming" / ".minecraft"
    elif system == "Darwin":
        return home / "Library" / "Application Support" / "minecraft"
    else:
        return home / ".minecraft"


def _get_saves_dir(launcher: str = "pcl2", mc_dir: Optional[str] = None) -> Path:
    """获取存档目录路径"""
    if mc_dir:
        return Path(mc_dir) / "saves"
    launcher_info = config.get_launcher_info(launcher)
    if launcher_info:
        saves_path = launcher_info.get("saves_path", "")
        if saves_path and not saves_path.startswith("{"):
            # 相对路径，基于.minecraft
            mc_base = _get_default_minecraft_dir(launcher)
            return mc_base / saves_path.replace(".minecraft/", "").replace(".minecraft\\", "")
    return _get_default_minecraft_dir(launcher) / "saves"


def _should_exclude(filename: str) -> bool:
    """检查文件是否应被排除"""
    for pattern in EXCLUDE_PATTERNS:
        if pattern in filename:
            return True
    return False


def _create_sync_config(
    sync_dir: Path,
    launcher: str,
    mc_dir: Path,
    device: str = "pc",
) -> Dict[str, Any]:
    """创建同步配置"""
    sync_config = {
        "version": "1.0",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "launcher": launcher,
        "device": device,
        "mc_dir": str(mc_dir),
        "saves_dir": str(mc_dir / "saves"),
        "sync_dir": str(sync_dir),
        "last_backup": None,
        "last_restore": None,
        "backup_history": [],
    }

    # 保存配置到同步目录
    config_path = sync_dir / SYNC_CONFIG_FILE
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(sync_config, f, ensure_ascii=False, indent=2)

    return sync_config


def _load_sync_config(sync_dir: Path) -> Optional[Dict[str, Any]]:
    """加载已有的同步配置"""
    config_path = sync_dir / SYNC_CONFIG_FILE
    if not config_path.exists():
        return None
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        logger.error(f"读取同步配置失败: {e}")
        return None


def _generate_setup_guide_html(
    sync_config: Dict[str, Any],
    sync_dir: Path,
    timestamp: str,
) -> str:
    """生成setup操作引导HTML"""
    rg = ReportGenerator("存档同步配置")

    guide_steps = """
    <div class='callout green'>
      <div class='callout-title'>百度网盘同步空间配置指南</div>
      <ol>
        <li><strong>安装百度网盘客户端</strong>：前往 <a href="https://pan.baidu.com">pan.baidu.com</a> 下载并安装PC版百度网盘</li>
        <li><strong>开通同步空间</strong>：在百度网盘客户端中，点击「同步空间」标签，按提示开通（可能需要会员）</li>
        <li><strong>设置同步目录</strong>：将百度网盘同步空间的工作目录设置为以下路径：</li>
        <li><code>{sync_dir}</code></li>
        <li><strong>手机端配置</strong>：在手机端百度网盘中，确保同步空间已开启，并选择相同的同步目录</li>
        <li><strong>验证连通性</strong>：在PC端放入一个测试文件，检查手机端是否能自动收到</li>
      </ol>
    </div>
    """.format(sync_dir=str(sync_dir))

    config_info = f"""
    <div class='callout'>
      <div class='callout-title'>同步配置信息</div>
      <table class='data-table'>
        <tr><th>配置项</th><th>值</th></tr>
        <tr><td>启动器</td><td>{sync_config['launcher']}</td></tr>
        <tr><td>设备类型</td><td>{sync_config['device']}</td></tr>
        <tr><td>MC目录</td><td><code>{sync_config['mc_dir']}</code></td></tr>
        <tr><td>存档目录</td><td><code>{sync_config['saves_dir']}</code></td></tr>
        <tr><td>同步目录</td><td><code>{sync_config['sync_dir']}</code></td></tr>
        <tr><td>配置文件</td><td><code>{sync_dir / SYNC_CONFIG_FILE}</code></td></tr>
      </table>
    </div>
    """

    workflow_html = """
    <div class='callout'>
      <div class='callout-title'>使用流程</div>
      <h3>备份存档（PC → 网盘）</h3>
      <p>在结束游戏后，运行 backup 操作，将当前存档打包上传到网盘同步目录。</p>
      <pre class='code-block'>python main.py --feature save_sync --action backup --launcher pcl2</pre>

      <h3>恢复存档（网盘 → PC/手机）</h3>
      <p>在切换设备后，运行 restore 操作，从网盘同步目录恢复最新存档。</p>
      <pre class='code-block'>python main.py --feature save_sync --action restore --launcher pcl2</pre>

      <h3>接力流转说明</h3>
      <p>百度网盘同步空间会自动在PC和手机端之间同步文件。配置完成后，只需执行 backup/restore 即可实现存档接力。</p>
    </div>
    """

    body_html = f"""
    <h2>配置引导</h2>
    {guide_steps}

    <h2>配置信息</h2>
    {config_info}

    <h2>使用流程</h2>
    {workflow_html}

    <div class='callout'>
      <div class='callout-title'>技术说明</div>
      <p>V1版本通过百度网盘同步空间实现PC与手机端的存档接力。</p>
      <p>备份时将存档打包为ZIP文件，文件名含时间戳，方便多版本回溯。</p>
      <p>恢复时自动选择最新的备份文件解压到存档目录。</p>
    </div>
    """

    return rg.render_full_html("存档同步配置", body_html, timestamp)


def _generate_backup_report_html(
    backup_info: Dict[str, Any],
    timestamp: str,
) -> str:
    """生成备份报告HTML"""
    rg = ReportGenerator("存档备份报告")

    overview_html = f"""
    <div class='overview-grid'>
      <div class='overview-card'>
        <div class='oc-num'>{backup_info['total_worlds']}</div>
        <div class='oc-label'>存档世界数</div>
      </div>
      <div class='overview-card'>
        <div class='oc-num'>{backup_info['total_files']}</div>
        <div class='oc-label'>总文件数</div>
      </div>
      <div class='overview-card'>
        <div class='oc-num'>{backup_info['total_size_mb']:.1f}</div>
        <div class='oc-label'>总大小(MB)</div>
      </div>
      <div class='overview-card critical'>
        <div class='oc-num'>{'✅' if backup_info['success'] else '❌'}</div>
        <div class='oc-label'>备份状态</div>
      </div>
    </div>
    """

    worlds_html = ""
    if backup_info.get("worlds"):
        world_rows = ""
        for w in backup_info["worlds"]:
            world_rows += f"""
            <tr>
              <td>{w['name']}</td>
              <td>{w['file_count']}</td>
              <td>{w['size_mb']:.2f} MB</td>
              <td>{w.get('last_modified', '未知')}</td>
            </tr>
            """
        worlds_html = f"""
        <div class='callout'>
          <div class='callout-title'>存档详情</div>
          <table class='data-table'>
            <thead>
              <tr><th>世界名称</th><th>文件数</th><th>大小</th><th>最后修改</th></tr>
            </thead>
            <tbody>{world_rows}</tbody>
          </table>
        </div>
        """

    body_html = f"""
    <h2>备份概览</h2>
    {overview_html}

    <h2>存档详情</h2>
    {worlds_html}

    <div class='callout green'>
      <div class='callout-title'>备份文件</div>
      <p>备份文件已保存到: <code>{backup_info['backup_file']}</code></p>
      <p>百度网盘同步空间将自动上传此文件到云端。</p>
    </div>
    """

    return rg.render_full_html("存档备份报告", body_html, timestamp)


def _generate_restore_report_html(
    restore_info: Dict[str, Any],
    timestamp: str,
) -> str:
    """生成恢复报告HTML"""
    rg = ReportGenerator("存档恢复报告")

    overview_html = f"""
    <div class='overview-grid'>
      <div class='overview-card'>
        <div class='oc-num'>{restore_info['backup_count']}</div>
        <div class='oc-label'>可用备份数</div>
      </div>
      <div class='overview-card'>
        <div class='oc-num'>{restore_info['restored_files']}</div>
        <div class='oc-label'>恢复文件数</div>
      </div>
      <div class='overview-card critical'>
        <div class='oc-num'>{'✅' if restore_info['success'] else '❌'}</div>
        <div class='oc-label'>恢复状态</div>
      </div>
    </div>
    """

    backups_html = ""
    if restore_info.get("available_backups"):
        backup_rows = ""
        for b in restore_info["available_backups"]:
            is_selected = "✅" if b.get("selected") else ""
            backup_rows += f"""
            <tr>
              <td>{is_selected}</td>
              <td><code>{b['filename']}</code></td>
              <td>{b['size_mb']:.2f} MB</td>
              <td>{b['timestamp']}</td>
            </tr>
            """
        backups_html = f"""
        <div class='callout'>
          <div class='callout-title'>可用备份列表</div>
          <table class='data-table'>
            <thead>
              <tr><th>选择</th><th>备份文件</th><th>大小</th><th>备份时间</th></tr>
            </thead>
            <tbody>{backup_rows}</tbody>
          </table>
        </div>
        """

    body_html = f"""
    <h2>恢复概览</h2>
    {overview_html}

    <h2>备份列表</h2>
    {backups_html}

    <div class='callout green'>
      <div class='callout-title'>恢复完成</div>
      <p>已从备份 <code>{restore_info.get('selected_backup', '无')}</code> 恢复存档到:</p>
      <p><code>{restore_info.get('saves_dir', '')}</code></p>
    </div>
    """

    return rg.render_full_html("存档恢复报告", body_html, timestamp)


def _action_setup(
    sync_dir: Path,
    launcher: str,
    device: str,
    output_dir: str,
) -> Dict[str, Any]:
    """setup操作：配置同步环境"""
    mc_dir = _get_default_minecraft_dir(launcher)
    saves_dir = _get_saves_dir(launcher)

    # 创建同步目录
    sync_dir.mkdir(parents=True, exist_ok=True)

    # 创建配置
    sync_config = _create_sync_config(sync_dir, launcher, mc_dir, device)

    # 生成报告
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_html = _generate_setup_guide_html(sync_config, sync_dir, timestamp)
    html_path = Path(output_dir) / f"save_sync_setup_{timestamp}.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(report_html)

    json_path = Path(output_dir) / f"save_sync_setup_{timestamp}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(sync_config, f, ensure_ascii=False, indent=2)

    logger.info(f"同步配置完成: {sync_dir}")

    return config.make_result(
        status="success",
        feature="F6",
        input_summary={"action": "setup", "sync_dir": str(sync_dir), "launcher": launcher},
        result={
            "sync_config": sync_config,
            "saves_dir": str(saves_dir),
            "sync_dir": str(sync_dir),
        },
        output_files={"report": str(html_path), "data": str(json_path)},
    )


def _action_backup(
    sync_dir: Path,
    launcher: str,
    output_dir: str,
) -> Dict[str, Any]:
    """backup操作：备份存档到同步目录"""
    sync_config = _load_sync_config(sync_dir)

    if sync_config:
        saves_dir = Path(sync_config["saves_dir"])
    else:
        saves_dir = _get_saves_dir(launcher)
        logger.warning("未找到同步配置，使用默认存档目录")

    if not saves_dir.exists():
        return config.make_result(
            status="error",
            feature="F6",
            input_summary={"action": "backup", "saves_dir": str(saves_dir)},
            result={"error": f"存档目录不存在: {saves_dir}"},
            errors=[f"存档目录不存在: {saves_dir}"],
        )

    # 收集存档世界
    worlds = []
    total_files = 0
    total_size = 0

    for world_dir in sorted(saves_dir.iterdir()):
        if not world_dir.is_dir() or _should_exclude(world_dir.name):
            continue

        world_files = []
        world_size = 0
        for root, dirs, files in os.walk(world_dir):
            for f in files:
                if _should_exclude(f):
                    continue
                fp = Path(root) / f
                try:
                    size = fp.stat().st_size
                    world_files.append(fp)
                    world_size += size
                    total_size += size
                except OSError:
                    pass

        worlds.append({
            "name": world_dir.name,
            "file_count": len(world_files),
            "size_mb": world_size / (1024 * 1024),
            "last_modified": datetime.fromtimestamp(
                world_dir.stat().st_mtime
            ).strftime("%Y-%m-%d %H:%M"),
        })
        total_files += len(world_files)

    # 打包存档
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"mc_saves_{timestamp}.zip"
    backup_path = sync_dir / backup_filename

    with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for world_dir in sorted(saves_dir.iterdir()):
            if not world_dir.is_dir() or _should_exclude(world_dir.name):
                continue
            for root, dirs, files in os.walk(world_dir):
                for f in files:
                    if _should_exclude(f):
                        continue
                    fp = Path(root) / f
                    arc_name = fp.relative_to(saves_dir).as_posix()
                    zf.write(fp, arc_name)

    backup_info = {
        "success": True,
        "total_worlds": len(worlds),
        "total_files": total_files,
        "total_size_mb": total_size / (1024 * 1024),
        "backup_file": str(backup_path),
        "worlds": worlds,
    }

    # 更新配置
    if sync_config:
        sync_config["last_backup"] = timestamp
        sync_config.setdefault("backup_history", []).append({
            "timestamp": timestamp,
            "file": str(backup_path),
            "worlds": len(worlds),
            "size_mb": total_size / (1024 * 1024),
        })
        # 保留最近10次备份记录
        sync_config["backup_history"] = sync_config["backup_history"][-10:]
        config_path = sync_dir / SYNC_CONFIG_FILE
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(sync_config, f, ensure_ascii=False, indent=2)

    # 生成报告
    report_html = _generate_backup_report_html(backup_info, timestamp)
    html_path = Path(output_dir) / f"save_sync_backup_{timestamp}.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(report_html)

    json_path = Path(output_dir) / f"save_sync_backup_{timestamp}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(backup_info, f, ensure_ascii=False, indent=2)

    logger.info(f"存档备份完成: {len(worlds)}个世界, {total_files}个文件")

    return config.make_result(
        status="success",
        feature="F6",
        input_summary={"action": "backup", "saves_dir": str(saves_dir)},
        result=backup_info,
        output_files={"report": str(html_path), "data": str(json_path)},
    )


def _action_restore(
    sync_dir: Path,
    launcher: str,
    output_dir: str,
) -> Dict[str, Any]:
    """restore操作：从同步目录恢复存档"""
    sync_config = _load_sync_config(sync_dir)

    if sync_config:
        saves_dir = Path(sync_config["saves_dir"])
    else:
        saves_dir = _get_saves_dir(launcher)
        logger.warning("未找到同步配置，使用默认存档目录")

    # 查找可用备份
    backup_files = sorted(sync_dir.glob("mc_saves_*.zip"), reverse=True)

    if not backup_files:
        return config.make_result(
            status="error",
            feature="F6",
            input_summary={"action": "restore", "sync_dir": str(sync_dir)},
            result={"error": "同步目录中未找到备份文件"},
            errors=["未找到 mc_saves_*.zip 备份文件"],
        )

    # 列出可用备份
    available_backups = []
    for bf in backup_files:
        stat = bf.stat()
        # 从文件名提取时间戳 mc_saves_20260803_153000.zip
        parts = bf.stem.split("_")
        if len(parts) >= 3:
            ts = "_".join(parts[2:])
        else:
            ts = bf.stem

        available_backups.append({
            "filename": bf.name,
            "path": str(bf),
            "size_mb": stat.st_size / (1024 * 1024),
            "timestamp": ts,
            "selected": False,
        })

    # 选择最新备份
    selected = backup_files[0]
    available_backups[0]["selected"] = True

    # 确保存档目录存在
    saves_dir.mkdir(parents=True, exist_ok=True)

    # 解压备份
    restored_files = 0
    try:
        with zipfile.ZipFile(selected, "r") as zf:
            for name in zf.namelist():
                if not name.endswith("/"):
                    zf.extract(name, saves_dir)
                    restored_files += 1
    except zipfile.BadZipFile as e:
        return config.make_result(
            status="error",
            feature="F6",
            input_summary={"action": "restore", "backup_file": str(selected)},
            result={"error": f"备份文件损坏: {e}"},
            errors=[f"备份文件损坏: {e}"],
        )

    restore_info = {
        "success": True,
        "backup_count": len(backup_files),
        "restored_files": restored_files,
        "selected_backup": selected.name,
        "available_backups": available_backups,
        "saves_dir": str(saves_dir),
    }

    # 更新配置
    if sync_config:
        sync_config["last_restore"] = datetime.now().strftime("%Y%m%d_%H%M%S")
        config_path = sync_dir / SYNC_CONFIG_FILE
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(sync_config, f, ensure_ascii=False, indent=2)

    # 生成报告
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_html = _generate_restore_report_html(restore_info, timestamp)
    html_path = Path(output_dir) / f"save_sync_restore_{timestamp}.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(report_html)

    json_path = Path(output_dir) / f"save_sync_restore_{timestamp}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(restore_info, f, ensure_ascii=False, indent=2)

    logger.info(f"存档恢复完成: 从 {selected.name} 恢复了 {restored_files} 个文件")

    return config.make_result(
        status="success",
        feature="F6",
        input_summary={"action": "restore", "backup_file": str(selected)},
        result=restore_info,
        output_files={"report": str(html_path), "data": str(json_path)},
    )


def run(args) -> Dict[str, Any]:
    """F6 存档同步主入口

    Args:
        args: argparse.Namespace，需包含:
            - action: 操作类型 setup/backup/restore
            - sync_dir: 百度网盘同步目录路径
            - launcher: 启动器类型
            - device: 设备类型
            - output: 输出目录

    Returns:
        统一返回结构字典
    """
    action = getattr(args, "action", None)
    sync_dir_str = getattr(args, "sync_dir", None)
    launcher = getattr(args, "launcher", "pcl2")
    device = getattr(args, "device", "pc")
    output_dir = getattr(args, "output", None) or str(config.OUTPUT_DIR / "reports")

    if not action:
        return config.make_result(
            status="error",
            feature="F6",
            input_summary={"action": None},
            result={"error": "缺少 --action 参数"},
            errors=["必须指定操作类型: setup / backup / restore"],
        )

    # 确定同步目录
    if sync_dir_str:
        sync_dir = Path(sync_dir_str)
    else:
        # 默认路径
        home = Path.home()
        sync_dir = home / "BaiduNetdisk" / "MC同步"

    os.makedirs(output_dir, exist_ok=True)

    logger.info(f"存档同步: action={action}, sync_dir={sync_dir}, launcher={launcher}")

    if action == "setup":
        return _action_setup(sync_dir, launcher, device, output_dir)
    elif action == "backup":
        return _action_backup(sync_dir, launcher, output_dir)
    elif action == "restore":
        return _action_restore(sync_dir, launcher, output_dir)
    else:
        return config.make_result(
            status="error",
            feature="F6",
            input_summary={"action": action},
            result={"error": f"未知操作: {action}"},
            errors=[f"不支持的action: {action}"],
        )
