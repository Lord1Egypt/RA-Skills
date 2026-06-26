#!/usr/bin/env python3
"""
PaperMC插件升级框架
基于ViaVersion升级经验抽象的两个通用方法
"""

import json
import requests
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

# 配置
SERVER_DIR = Path("/home/yan/projects/P_3.10.12/paperMC_RGFV_1.21.8")
PLUGINS_DIR = SERVER_DIR / "plugins"
PLUGIN_BACKUP_DIR = SERVER_DIR / "plugin_backup"
LOG_DIR = Path.home() / ".openclaw" / "logs"
HANGAR_API_BASE = "https://hangar.papermc.io/api/v1"

# 代理绕过配置（基于经验）
NO_PROXY_DOMAINS = [
    "localhost", "127.0.0.1", "192.168.8.165",
    "hangar.papermc.io", "papermc.io", "hangarcdn.papermc.io"
]

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "plugin_upgrade.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class PluginUpgradeFramework:
    """PaperMC插件升级框架"""
    
    def __init__(self):
        self.session = self._create_session()
        self.ensure_dirs()
    
    def _create_session(self):
        """创建HTTP会话，配置代理绕过"""
        session = requests.Session()
        # 设置请求头模拟浏览器
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; PaperMC-Updater/1.0)',
            'Accept': 'application/json'
        })
        return session
    
    def ensure_dirs(self):
        """确保目录存在"""
        for directory in [PLUGINS_DIR, PLUGIN_BACKUP_DIR, LOG_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def get_server_info(self) -> Dict:
        """获取服务器信息"""
        info = {
            "server_dir": str(SERVER_DIR),
            "paper_version": self._detect_paper_version(),
            "plugins_count": len(list(PLUGINS_DIR.glob("*.jar"))),
            "last_updated": datetime.now().isoformat()
        }
        return info
    
    def _detect_paper_version(self) -> str:
        """检测PaperMC版本"""
        try:
            # 从日志中提取版本信息
            log_file = SERVER_DIR / "logs" / "latest.log"
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        if "Paper version" in line:
                            # 提取版本号
                            import re
                            match = re.search(r'Paper version (\S+)', line)
                            if match:
                                return match.group(1)
            return "unknown"
        except Exception as e:
            logger.warning(f"检测Paper版本失败: {e}")
            return "unknown"
    
    def method1_specific_plugin_upgrade(self, plugin_name: str, target_version: str = None) -> Dict:
        """
        方法1: 针对具体插件的升级（基于ViaVersion经验）
        
        参数:
            plugin_name: 插件名称（如ViaVersion）
            target_version: 目标版本（可选，默认最新版）
        
        返回: 升级结果报告
        """
        logger.info(f"开始执行方法1: 具体插件升级 - {plugin_name}")
        
        result = {
            "plugin": plugin_name,
            "method": "specific_upgrade",
            "start_time": datetime.now().isoformat(),
            "steps": [],
            "success": False,
            "error": None
        }
        
        try:
            # 步骤1: 检查当前插件
            current_file = self._find_plugin_file(plugin_name)
            if not current_file:
                raise FileNotFoundError(f"未找到插件: {plugin_name}")
            
            current_version = self._extract_version_from_filename(current_file.name)
            result["current_version"] = current_version
            result["steps"].append({
                "step": "check_current",
                "status": "success",
                "message": f"找到当前版本: {current_version}"
            })
            
            # 步骤2: 获取插件信息
            plugin_info = self._get_plugin_info(plugin_name)
            if not plugin_info:
                raise ValueError(f"无法获取插件信息: {plugin_name}")
            
            # 步骤3: 确定目标版本
            if not target_version:
                target_version = plugin_info.get("latest_version")
            
            if current_version == target_version:
                result["success"] = True
                result["message"] = "已是最新版本，无需升级"
                return result
            
            result["target_version"] = target_version
            result["steps"].append({
                "step": "determine_target",
                "status": "success", 
                "message": f"目标版本: {target_version}"
            })
            
            # 步骤4: 风险评估
            risk_assessment = self._assess_upgrade_risk(plugin_name, current_version, target_version)
            result["risk_assessment"] = risk_assessment
            result["steps"].append({
                "step": "risk_assessment",
                "status": "success",
                "message": f"风险评估完成: {risk_assessment['risk_level']}"
            })
            
            # 步骤5: 备份当前版本
            backup_file = self._backup_plugin(current_file)
            result["backup_file"] = str(backup_file)
            result["steps"].append({
                "step": "backup",
                "status": "success",
                "message": f"备份完成: {backup_file.name}"
            })
            
            # 步骤6: 获取下载URL
            download_url = self._get_download_url(plugin_name, target_version)
            if not download_url:
                raise ValueError(f"无法获取下载URL")
            
            result["steps"].append({
                "step": "get_download_url",
                "status": "success",
                "message": f"获取下载URL成功"
            })
            
            # 步骤7: 下载新版本
            new_filename = f"{plugin_name}-{target_version}.jar"
            new_file = PLUGINS_DIR / new_filename
            self._download_file(download_url, new_file)
            
            result["new_file"] = str(new_file)
            result["steps"].append({
                "step": "download",
                "status": "success",
                "message": f"下载完成: {new_filename}"
            })
            
            # 步骤8: 删除旧版本
            current_file.unlink()
            result["steps"].append({
                "step": "remove_old",
                "status": "success",
                "message": f"删除旧版本: {current_file.name}"
            })
            
            # 步骤9: 生成重启建议
            restart_plan = self._generate_restart_plan()
            result["restart_plan"] = restart_plan
            result["steps"].append({
                "step": "generate_restart_plan",
                "status": "success",
                "message": "生成重启计划完成"
            })
            
            result["success"] = True
            result["message"] = f"插件升级准备完成: {current_version} → {target_version}"
            result["end_time"] = datetime.now().isoformat()
            
            logger.info(f"方法1执行成功: {plugin_name} {current_version} → {target_version}")
            
        except Exception as e:
            result["success"] = False
            result["error"] = str(e)
            result["end_time"] = datetime.now().isoformat()
            logger.error(f"方法1执行失败: {e}")
        
        return result
    
    def method2_scan_and_assess_upgrades(self, limit: int = 20) -> Dict:
        """
        方法2: 扫描并评估可升级插件
        
        参数:
            limit: 扫描插件数量限制
        
        返回: 升级评估报告
        """
        logger.info(f"开始执行方法2: 扫描并评估插件升级")
        
        result = {
            "method": "scan_and_assess",
            "start_time": datetime.now().isoformat(),
            "scanned_plugins": 0,
            "upgrade_candidates": [],
            "no_upgrade_needed": [],
            "failed_checks": [],
            "summary": {}
        }
        
        try:
            # 步骤1: 获取已安装插件列表
            installed_plugins = self._get_installed_plugins()
            result["installed_count"] = len(installed_plugins)
            
            # 步骤2: 获取热门插件列表
            popular_plugins = self._get_popular_plugins(limit)
            result["scanned_plugins"] = len(popular_plugins)
            
            # 步骤3: 交叉检查并评估
            for plugin in popular_plugins:
                plugin_name = plugin.get("name")
                
                # 检查是否已安装
                installed_info = installed_plugins.get(plugin_name)
                if not installed_info:
                    continue  # 未安装，跳过
                
                # 获取插件详细信息
                try:
                    plugin_details = self._get_plugin_info(plugin_name)
                    if not plugin_details:
                        result["failed_checks"].append({
                            "plugin": plugin_name,
                            "reason": "无法获取插件信息"
                        })
                        continue
                    
                    current_version = installed_info["version"]
                    latest_version = plugin_details.get("latest_version")
                    
                    if not latest_version or current_version == latest_version:
                        result["no_upgrade_needed"].append({
                            "plugin": plugin_name,
                            "current": current_version,
                            "latest": latest_version or "unknown",
                            "status": "up_to_date"
                        })
                        continue
                    
                    # 评估升级
                    assessment = self._assess_upgrade_risk(
                        plugin_name, current_version, latest_version
                    )
                    
                    candidate = {
                        "plugin": plugin_name,
                        "current_version": current_version,
                        "latest_version": latest_version,
                        "assessment": assessment,
                        "recommendation": self._generate_recommendation(assessment),
                        "download_url": plugin_details.get("download_url"),
                        "changelog": plugin_details.get("changelog", "无更新日志")
                    }
                    
                    result["upgrade_candidates"].append(candidate)
                    
                except Exception as e:
                    result["failed_checks"].append({
                        "plugin": plugin_name,
                        "reason": f"检查失败: {str(e)}"
                    })
            
            # 步骤4: 生成摘要
            result["summary"] = {
                "total_candidates": len(result["upgrade_candidates"]),
                "high_risk": len([c for c in result["upgrade_candidates"] 
                                 if c["assessment"]["risk_level"] == "high"]),
                "medium_risk": len([c for c in result["upgrade_candidates"] 
                                   if c["assessment"]["risk_level"] == "medium"]),
                "low_risk": len([c for c in result["upgrade_candidates"] 
                                if c["assessment"]["risk_level"] == "low"]),
                "recommended": len([c for c in result["upgrade_candidates"] 
                                   if c["recommendation"] == "recommended"])
            }
            
            result["success"] = True
            result["end_time"] = datetime.now().isoformat()
            logger.info(f"方法2执行成功: 找到{len(result['upgrade_candidates'])}个可升级插件")
            
        except Exception as e:
            result["success"] = False
            result["error"] = str(e)
            result["end_time"] = datetime.now().isoformat()
            logger.error(f"方法2执行失败: {e}")
        
        return result
    
    # ========== 辅助方法 ==========
    
    def _find_plugin_file(self, plugin_name: str) -> Optional[Path]:
        """查找插件文件"""
        # 尝试精确匹配
        patterns = [
            f"{plugin_name}-*.jar",
            f"*{plugin_name}*.jar",
            f"{plugin_name.lower()}-*.jar",
            f"*{plugin_name.lower()}*.jar"
        ]
        
        for pattern in patterns:
            for file in PLUGINS_DIR.glob(pattern):
                if file.is_file():
                    return file
        
        return None
    
    def _extract_version_from_filename(self, filename: str) -> str:
        """从文件名提取版本号"""
        import re
        # 匹配常见的版本格式
        patterns = [
            r'(\d+\.\d+\.\d+)',  # 1.2.3
            r'(\d+\.\d+)',       # 1.2
            r'v?(\d+\.\d+\.\d+[-\w]*)',  # v1.2.3-beta
        ]
        
        for pattern in patterns:
            match = re.search(pattern, filename)
            if match:
                return match.group(1)
        
        return "unknown"
    
    def _get_plugin_info(self, plugin_name: str) -> Optional[Dict]:
        """从Hangar获取插件信息"""
        try:
            # 获取插件基本信息
            url = f"{HANGAR_API_BASE}/projects/{plugin_name}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200:
                logger.warning(f"无法获取插件信息: {plugin_name}, 状态码: {response.status_code}")
                return None
            
            data = response.json()
            
            # 获取版本信息
            versions_url = f"{url}/versions"
            versions_response = self.session.get(versions_url, timeout=10)
            
            latest_version = None
            download_url = None
            
            if versions_response.status_code == 200:
                versions_data = versions_response.json()
                if versions_data.get("result") and len(versions_data["result"]) > 0:
                    latest = versions_data["result"][0]
                    latest_version = latest.get("name")
                    
                    # 尝试获取下载URL
                    if latest.get("downloads") and latest["downloads"].get("PAPER"):
                        download_info = latest["downloads"]["PAPER"]
                        download_url = download_info.get("externalUrl") or download_info.get("downloadUrl")
            
            return {
                "name": data.get("name"),
                "description": data.get("description"),
                "latest_version": latest_version,
                "download_url": download_url,
                "author": data.get("owner"),
                "created_at": data.get("createdAt"),
                "stars": data.get("stars", 0)
            }
            
        except Exception as e:
            logger.error(f"获取插件信息失败 {plugin_name}: {e}")
            return None
    
    def _assess_upgrade_risk(self, plugin_name: str, current: str, target: str) -> Dict:
        """评估升级风险"""
        risk_level = "medium"  # 默认中等风险
        
        # 基于ViaVersion经验的风险评估逻辑
        risk_factors = []
        
        # 因素1: 版本跳跃大小
        current_parts = current.split('.')
        target_parts = target.split('.')
        
        if len(current_parts) >= 2 and len(target_parts) >= 2:
            current_major = int(current_parts[0]) if current_parts[0].isdigit() else 0
            target_major = int(target_parts[0]) if target_parts[0].isdigit() else 0
            
            if target_major > current_major:
                risk_factors.append("主要版本升级")
                risk_level = "high"
            elif target_parts[1] > current_parts[1]:
                risk_factors.append("次要版本升级")
                risk_level = "medium"
            else:
                risk_factors.append("补丁版本升级")
                risk_level = "low"
        
        # 因素2: 插件重要性（基于经验）
        critical_plugins = ["ViaVersion", "ProtocolLib", "WorldEdit", "Essentials"]
        if plugin_name in critical_plugins:
            risk_factors.append("核心插件")
            risk_level = max(risk_level, "medium")  # 至少中等风险
        
        # 因素3: 发布时间（基于经验判断稳定性）
        # 这里可以添加更复杂的时间分析
        
        return {
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "backup_required": True,
            "restart_required": True,
            "testing_recommended": risk_level in ["high", "medium"]
        }
    
    def _backup_plugin(self, plugin_file: Path) -> Path:
        """备份插件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{plugin_file.stem}_{timestamp}{plugin_file.suffix}"
        backup_file = PLUGIN_BACKUP_DIR / backup_name
        
        import shutil
        shutil.copy2(plugin_file, backup_file)
        
        logger.info(f"插件备份完成: {backup_file}")
        return backup_file
    
    def _get_download_url(self, plugin_name: str, version: str) -> Optional[str]:
        """获取下载URL"""
        try:
            # 尝试从Hangar获取
            url = f"{HANGAR_API_BASE}/projects/{plugin_name}/versions/{version}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("downloads") and data["downloads"].get("PAPER"):
                    download_info = data["downloads"]["PAPER"]
                    return download_info.get("externalUrl") or download_info.get("downloadUrl")
            
            # 备用方案：构建标准URL（基于经验）
            return f"https://hangarcdn.papermc.io/plugins/{plugin_name}/{plugin_name}/versions/{version}/PAPER/{plugin_name}-{version}.jar"
            
        except Exception as e:
            logger.error(f"获取下载URL失败: {e}")
            return None
    
    def _download_file(self, url: str, destination: Path):
        """下载文件"""
        try:
            # 设置代理绕过环境
            import os
            original_no_proxy = os.environ.get("NO_PROXY", "")
            os.environ["NO_PROXY"] = ",".join(NO_PROXY_DOMAINS)
            
            response = self.session.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(destination, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # 进度日志
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            if int(percent) % 25 == 0:  # 每25%记录一次
                                logger.info(f"下载进度: {percent:.1f}% ({downloaded}/{total_size} bytes)")
            
            # 恢复原始NO_PROXY设置
            os.environ["NO_PROXY"] = original_no_proxy
            
            logger.info(f"文件下载完成: {destination.name} ({downloaded} bytes)")
            
        except Exception as e:
            logger.error(f"文件下载失败: {e}")
            raise
    
    def _get_installed_plugins(self) -> Dict:
        """获取已安装插件列表"""
        plugins = {}
        
        for jar_file in PLUGINS_DIR.glob("*.jar"):
            plugin_name = self._extract_plugin_name(jar_file.name)
            version = self._extract_version_from_filename(jar_file.name)
            
            plugins[plugin_name] = {
                "filename": jar_file.name,
                "version": version,
                "size": jar_file.stat().st_size,
                "modified": datetime.fromtimestamp(jar_file.stat().st_mtime).isoformat()
            }
        
        return plugins
    
    def _extract_plugin_name(self, filename: str) -> str:
        """从文件名提取插件名称"""
        import re
        
        # 移除版本号和.jar扩展名
        name = filename.replace(".jar", "")
        
        # 移除版本号（如 -1.2.3, -v1.2.3等）
        patterns = [
            r'-\d+\.\d+\.\d+.*$',
            r'-v\d+\.\d+\.\d+.*$',
            r'-\d+\.\d+.*$'
        ]
        
        for pattern in patterns:
            name = re.sub(pattern, '', name)
        
        return name
    
    def _get_popular_plugins(self, limit: int = 20) -> List[Dict]:
        """获取热门插件列表"""
        try:
            url = f"{HANGAR_API_BASE}/projects"
            params = {
                "platform": "PAPER",
                "sort": "-stars",
                "limit": limit
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            plugins = []
            
            for item in data.get("result", []):
                plugins.append({
                    "name": item.get("name"),
                    "stars": item.get("stars", 0),
                    "description": item.get("description", ""),
                    "owner": item.get("owner")
                })
            
            return plugins
            
        except Exception as e:
            logger.error(f"获取热门插件列表失败: {e}")
            return []
    
    def _generate_recommendation(self, assessment: Dict) -> str:
        """生成升级建议"""
        risk_level = assessment.get("risk_level", "medium")
        
        recommendations = {
            "low": "recommended",  # 低风险，推荐升级
            "medium": "consider",  # 中等风险，考虑升级
            "high": "caution"      # 高风险，谨慎升级
        }
        
        return recommendations.get(risk_level, "consider")
    
    def _generate_restart_plan(self) -> Dict:
        """生成重启计划"""
        return {
            "recommended_time": "低峰时段（如凌晨）",
            "estimated_downtime": "2-3分钟",
            "steps": [
                "1. 通知玩家服务器即将重启",
                "2. 执行停止命令",
                "3. 等待所有玩家退出",
                "4. 确认进程停止",
                "5. 执行启动命令",
                "6. 验证服务恢复"
            ],
            "rollback_plan": [
                "1. 停止服务器",
                "2. 恢复备份文件",
                "3. 删除新版本文件",
                "4. 重启服务器"
            ]
        }
    
    def execute_upgrade(self, plugin_name: str, auto_restart: bool = False) -> Dict:
        """执行完整升级流程（包含重启）"""
        logger.info(f"开始执行完整升级流程: {plugin_name}")
        
        result = {
            "plugin": plugin_name,
            "auto_restart": auto_restart,
            "phases": [],
            "success": False
        }
        
        try:
            # 阶段1: 准备升级
            prep_result = self.method1_specific_plugin_upgrade(plugin_name)
            result["phases"].append({
                "phase": "preparation",
                "result": prep_result
            })
            
            if not prep_result["success"]:
                raise ValueError(f"准备阶段失败: {prep_result.get('error')}")
            
            # 阶段2: 执行重启（如果启用）
            if auto_restart:
                restart_result = self._restart_server()
                result["phases"].append({
                    "phase": "restart",
                    "result": restart_result
                })
                
                if not restart_result["success"]:
                    raise ValueError(f"重启阶段失败: {restart_result.get('error')}")
            
            result["success"] = True
            result["message"] = f"插件升级{'并重启' if auto_restart else ''}完成"
            
        except Exception as e:
            result["success"] = False
            result["error"] = str(e)
            logger.error(f"完整升级流程失败: {e}")
        
        return result
    
    def _restart_server(self) -> Dict:
        """重启服务器（基于经验的安全重启）"""
        result = {
            "success": False,
            "steps": [],
            "error": None
        }
        
        try:
            # 步骤1: 查找服务器进程
            import psutil
            server_process = None
            
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = proc.info['cmdline']
                    if cmdline and 'papermc.jar' in ' '.join(cmdline):
                        server_process = proc
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if not server_process:
                result["steps"].append({
                    "step": "find_process",
                    "status": "warning",
                    "message": "未找到运行中的服务器进程"
                })
                # 直接启动
                return self._start_server()
            
            pid = server_process.info['pid']
            result["steps"].append({
                "step": "find_process",
                "status": "success",
                "message": f"找到服务器进程: PID {pid}"
            })
            
            # 步骤2: 优雅停止
            logger.info(f"停止服务器进程: PID {pid}")
            server_process.terminate()
            
            try:
                server_process.wait(timeout=30)  # 等待30秒
                result["steps"].append({
                    "step": "stop_server",
                    "status": "success",
                    "message": "服务器已优雅停止"
                })
            except psutil.TimeoutExpired:
                logger.warning("优雅停止超时，强制终止")
                server_process.kill()
                result["steps"].append({
                    "step": "stop_server",
                    "status": "warning",
                    "message": "优雅停止超时，已强制终止"
                })
            
            # 步骤3: 等待确保进程结束
            import time
            time.sleep(5)
            
            # 步骤4: 启动服务器
            start_result = self._start_server()
            result["steps"].extend(start_result.get("steps", []))
            
            if start_result["success"]:
                result["success"] = True
                result["message"] = "服务器重启成功"
            else:
                result["error"] = start_result.get("error")
            
        except Exception as e:
            result["error"] = str(e)
            logger.error(f"服务器重启失败: {e}")
        
        return result
    
    def _start_server(self) -> Dict:
        """启动服务器"""
        result = {
            "success": False,
            "steps": [],
            "error": None
        }
        
        try:
            start_script = SERVER_DIR / "start.sh"
            if not start_script.exists():
                raise FileNotFoundError(f"启动脚本不存在: {start_script}")
            
            # 执行启动命令
            import subprocess
            process = subprocess.Popen(
                [str(start_script)],
                cwd=str(SERVER_DIR),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            result["steps"].append({
                "step": "execute_start",
                "status": "success",
                "message": f"启动命令已执行，PID: {process.pid}"
            })
            
            # 等待一段时间检查进程
            import time
            time.sleep(10)
            
            # 检查进程是否仍在运行
            if process.poll() is None:
                result["success"] = True
                result["message"] = "服务器启动成功"
                result["pid"] = process.pid
            else:
                # 读取错误输出
                stdout, stderr = process.communicate()
                error_msg = stderr.strip() if stderr else "进程意外退出"
                raise RuntimeError(f"服务器启动失败: {error_msg}")
            
        except Exception as e:
            result["error"] = str(e)
            logger.error(f"服务器启动失败: {e}")
        
        return result


def main():
    """主函数：演示两种方法的使用"""
    import argparse
    
    parser = argparse.ArgumentParser(description="PaperMC插件升级框架")
    parser.add_argument("--method", choices=["1", "2", "both"], default="both",
                       help="执行方法：1=具体插件升级，2=扫描评估，both=两者")
    parser.add_argument("--plugin", help="插件名称（方法1使用）")
    parser.add_argument("--version", help="目标版本（方法1使用，可选）")
    parser.add_argument("--scan-limit", type=int, default=20,
                       help="扫描插件数量限制（方法2使用）")
    parser.add_argument("--auto-restart", action="store_true",
                       help="自动重启服务器（方法1使用）")
    parser.add_argument("--output", help="输出结果文件路径")
    
    args = parser.parse_args()
    
    # 创建框架实例
    framework = PluginUpgradeFramework()
    
    results = {}
    
    # 执行方法1：具体插件升级
    if args.method in ["1", "both"] and args.plugin:
        print(f"\n{'='*60}")
        print("执行方法1: 具体插件升级")
        print(f"插件: {args.plugin}")
        if args.version:
            print(f"目标版本: {args.version}")
        print('='*60)
        
        result = framework.method1_specific_plugin_upgrade(
            args.plugin, args.version
        )
        
        if args.auto_restart and result["success"]:
            print("\n执行自动重启...")
            restart_result = framework.execute_upgrade(args.plugin, True)
            result["auto_restart_result"] = restart_result
        
        results["method1"] = result
        
        # 打印结果
        print(f"\n升级结果: {'成功' if result['success'] else '失败'}")
        if result.get("message"):
            print(f"消息: {result['message']}")
        if result.get("error"):
            print(f"错误: {result['error']}")
    
    # 执行方法2：扫描评估
    if args.method in ["2", "both"]:
        print(f"\n{'='*60}")
        print("执行方法2: 扫描并评估插件升级")
        print(f"扫描限制: {args.scan_limit} 个插件")
        print('='*60)
        
        result = framework.method2_scan_and_assess_upgrades(args.scan_limit)
        results["method2"] = result
        
        # 打印摘要
        summary = result.get("summary", {})
        print(f"\n扫描摘要:")
        print(f"  已安装插件: {result.get('installed_count', 0)}")
        print(f"  扫描插件: {result.get('scanned_plugins', 0)}")
        print(f"  可升级候选: {summary.get('total_candidates', 0)}")
        print(f"  推荐升级: {summary.get('recommended', 0)}")
        
        if result.get("upgrade_candidates"):
            print(f"\n升级候选列表:")
            for candidate in result["upgrade_candidates"][:5]:  # 显示前5个
                print(f"  - {candidate['plugin']}: {candidate['current_version']} → {candidate['latest_version']}")
                print(f"    风险评估: {candidate['assessment']['risk_level']}")
                print(f"    建议: {candidate['recommendation']}")
    
    # 输出到文件
    if args.output:
        import json
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n结果已保存到: {args.output}")
    
    return results


if __name__ == "__main__":
    main()