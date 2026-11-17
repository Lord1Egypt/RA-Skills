#!/usr/bin/env python3
"""
HF Daily Deep Researcher - 报告管理模块

功能：
1. 报告命名与路径管理（按周期命名）
2. 同一周期版本控制（只保留最新一份）
3. 本地报告清理（自动删除旧版）
4. 云空间报告清理（按需调用）
5. 上传控制（默认本地，按需上传）

命名规范：
- 报告名：Agentic_RL_Credit_Assignment_调研_YYYYMMDD.md
- 同一周期多次运行 → 先删旧版，再写新版
- 不同周期 → 各自保留
"""

import json
import os
import re
import glob
from datetime import datetime
from typing import Optional, Tuple


class ReportManager:
    """报告管理器：负责报告命名、保存、版本控制、上传"""
    
    def __init__(self, skill_dir: str = None):
        if skill_dir is None:
            # 从脚本位置推导，适配任意安装路径
            skill_dir = os.path.dirname(os.path.abspath(__file__))
        self.skill_dir = skill_dir
        
        # 加载配置
        config_path = os.path.join(skill_dir, "config.json")
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.output_cfg = self.config.get("output", {})
        self.vm_cfg = self.output_cfg.get("version_management", {})
        self.cloud_cfg = self.output_cfg.get("cloud_upload", {})
    
    def _expand_path(self, path: str) -> str:
        """展开 ~ 为实际路径"""
        return os.path.expanduser(path) if path.startswith("~") else path
    
    def get_local_save_dir(self) -> str:
        """获取本地保存目录"""
        raw_dir = self.output_cfg.get("local_save_dir",
            "./reports")
        return self._expand_path(raw_dir)
    
    def generate_report_path(self, date: datetime = None, mode: str = "scan", days: int = None) -> Tuple[str, str]:
        """
        生成报告文件名和完整路径
        
        Args:
            date: 报告日期，默认今天
            mode: 运行模式 scan/deep/compare
            days: 追踪天数（用于推断周期 Daily/Weekly/Monthly）
        
        Returns:
            (filename, full_path)
        """
        if date is None:
            date = datetime.now()
        
        date_str = date.strftime(self.vm_cfg.get("period_format", "%Y%m%d"))
        
        # 命名模板
        pattern = self.output_cfg.get("report_naming_pattern", 
            "Agentic_RL_Credit_Assignment_调研_{date}.md")
        
        # 替换占位符
        filename = pattern.replace("{date}", date_str).replace("{mode}", mode)
        
        # 替换 {focus} 为研究方向（如 "agentic_RL_credit_assignment"）
        if "{focus}" in filename:
            focus_areas = self.config.get("user_profile", {}).get("research_focus", [])
            if focus_areas:
                focus_str = "_".join(focus_areas).replace(" ", "_").replace(",", "").replace("/", "_")
                filename = filename.replace("{focus}", focus_str)
            else:
                filename = filename.replace("{focus}_", "").replace("_{focus}", "")
        
        # 替换 {source} 为渠道（优先 HF，因为本 Skill 主要面向 HuggingFace Daily Papers）
        if "{source}" in filename:
            sources = self.config.get("tracking", {}).get("sources", ["hf_papers"])
            # 渠道缩写映射
            source_map = {
                "hf_papers": "HF",
                "huggingface": "HF",
                "arxiv": "arXiv",
                "google_scholar": "GS"
            }
            # 优先使用 HF，如果没有则按顺序取第一个
            if "hf_papers" in sources or "huggingface" in sources:
                source_str = "HF"
            elif sources:
                source_str = source_map.get(sources[0], sources[0].upper())
            else:
                source_str = "HF"
            filename = filename.replace("{source}", source_str)
        
        # 替换 {period} 为周期（Daily/Weekly/Monthly + 日期范围）
        if "{period}" in filename:
            # 根据 days 参数推断周期
            if days is not None:
                if days == 1:
                    period_str = f"Daily_{date.strftime('%Y%m%d')}"
                elif days <= 7:
                    # 计算周数
                    week_num = date.isocalendar()[1]
                    period_str = f"Weekly_{date.strftime('%Y')}W{week_num}"
                elif days <= 14:
                    period_str = f"Biweekly_{date.strftime('%Y%m%d')}"
                elif days <= 31:
                    period_str = f"Monthly_{date.strftime('%Y%m')}"
                else:
                    # 大范围扫描，显示具体日期范围
                    start_date = date - __import__('datetime').timedelta(days=days)
                    period_str = f"{days}days_{start_date.strftime('%Y%b')}-{date.strftime('%Y%b')}"
            else:
                # 从配置读取
                freq = self.config.get("tracking", {}).get("base_frequency", "weekly")
                week_num = date.isocalendar()[1]
                period_map = {
                    "daily": f"Daily_{date.strftime('%Y%m%d')}",
                    "every_3_days": f"3Day_{date.strftime('%Y%m%d')}",
                    "weekly": f"Weekly_{date.strftime('%Y')}W{week_num}",
                    "biweekly": f"Biweekly_{date.strftime('%Y%m%d')}"
                }
                period_str = period_map.get(freq, f"Weekly_{date.strftime('%Y')}W{week_num}")
            filename = filename.replace("{period}", period_str)
        
        # 确保 .md 后缀
        if not filename.endswith(".md"):
            filename += ".md"
        
        save_dir = self.get_local_save_dir()
        os.makedirs(save_dir, exist_ok=True)
        
        full_path = os.path.join(save_dir, filename)
        return filename, full_path
    
    def find_reports_in_period(self, date: datetime = None) -> list:
        """
        查找同一周期内的所有报告文件
        
        Returns:
            文件路径列表
        """
        if date is None:
            date = datetime.now()
        
        date_str = date.strftime(self.vm_cfg.get("period_format", "%Y%m%d"))
        save_dir = self.get_local_save_dir()
        
        if not os.path.exists(save_dir):
            return []
        
        # 构建匹配模式：文件名包含日期字符串
        pattern = os.path.join(save_dir, f"*_{date_str}*.md")
        matches = glob.glob(pattern)
        
        # 更精确匹配：检查文件名中是否包含日期部分
        # 排除历史报告（如 _v1, _v2 后缀）
        results = []
        for f in matches:
            basename = os.path.basename(f)
            # 匹配 *_YYYYMMDD.md 或 *_YYYYMMDD_*.md
            if re.search(rf'_{re.escape(date_str)}(?:_[^_]*)?\.md$', basename):
                results.append(f)
        
        return sorted(results)
    
    def clean_local_old_reports(self, date: datetime = None) -> list:
        """
        清理本地同一周期的旧报告（只保留最新）
        
        Returns:
            被删除的文件列表
        """
        if not self.vm_cfg.get("enabled", True):
            return []
        
        old_reports = self.find_reports_in_period(date)
        deleted = []
        
        for f in old_reports:
            try:
                os.remove(f)
                deleted.append(f)
                print(f"🗑️  已删除旧报告: {os.path.basename(f)}")
            except Exception as e:
                print(f"⚠️  删除失败: {f} - {e}")
        
        return deleted
    
    def save_report(self, content: str, date: datetime = None, mode: str = "scan", days: int = None) -> str:
        """
        保存报告（先清理旧版，再写新版）
        
        Args:
            content: 报告内容
            date: 报告日期
            mode: 运行模式
            days: 追踪天数（用于命名中的周期推断）
        
        Returns:
            保存的文件路径
        """
        # 1. 清理旧版
        self.clean_local_old_reports(date)
        
        # 2. 生成新路径（传递 days 用于周期推断）
        filename, full_path = self.generate_report_path(date, mode, days)
        
        # 3. 写入文件
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"💾 报告已保存: {full_path}")
        return full_path
    
    def should_upload_to_cloud(self) -> bool:
        """
        判断是否应上传到云空间
        
        逻辑：
        - cloud_upload.enabled = false → 不上传
        - cloud_upload.on_demand = true → 需要显式调用才上传
        - 否则按 enabled 设置
        """
        if not self.cloud_cfg.get("enabled", False):
            return False
        
        if self.cloud_cfg.get("on_demand", True):
            # 按需模式：默认不上传，需显式调用
            return False
        
        return True
    
    def get_cloud_folder_token(self) -> Optional[str]:
        """获取云空间文件夹 token（用于 parent_node 参数）"""
        return self.cloud_cfg.get("folder_token")
    
    def cloud_cleanup_candidates(self, date: datetime = None) -> list:
        """
        查找云空间中需要清理的旧报告
        
        注意：此函数仅返回候选文件名，实际删除需通过 feishu_drive_file 工具执行
        
        Returns:
            候选文件名列表（供外部调用删除）
        """
        if not self.vm_cfg.get("enabled", True):
            return []
        
        if date is None:
            date = datetime.now()
        
        date_str = date.strftime(self.vm_cfg.get("period_format", "%Y%m%d"))
        
        # 云空间中匹配该日期的文件
        pattern = self.output_cfg.get("report_naming_pattern", 
            "Agentic_RL_Credit_Assignment_调研_{date}.md")
        
        # 提取文件名模板（不含日期）
        base_pattern = pattern.replace("_{date}", "").replace("{date}", "")
        base_pattern = base_pattern.replace("_{mode}", "").replace("{mode}", "")
        base_pattern = base_pattern.replace(".md", "")
        
        # 可能的云文件名
        candidates = [
            f"{base_pattern}_{date_str}.md",
            f"{base_pattern.replace('_', ' ')} {date_str}.md",
        ]
        
        return candidates
    
    def list_local_reports(self) -> list:
        """
        列出本地所有报告文件
        
        Returns:
            文件信息列表 (path, size, mtime)
        """
        save_dir = self.get_local_save_dir()
        if not os.path.exists(save_dir):
            return []
        
        reports = []
        for f in glob.glob(os.path.join(save_dir, "*.md")):
            stat = os.stat(f)
            reports.append({
                "path": f,
                "filename": os.path.basename(f),
                "size": stat.st_size,
                "mtime": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
            })
        
        return sorted(reports, key=lambda x: x["mtime"], reverse=True)
    
    def get_report_metadata(self, filepath: str) -> dict:
        """获取报告元数据"""
        if not os.path.exists(filepath):
            return {}
        
        stat = os.stat(filepath)
        basename = os.path.basename(filepath)
        
        # 尝试提取日期
        date_match = re.search(r'_(\d{8})', basename)
        period = date_match.group(1) if date_match else "unknown"
        
        return {
            "filename": basename,
            "path": filepath,
            "size": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
            "period": period
        }


def main():
    """测试用例"""
    import sys
    
    manager = ReportManager()
    
    print("📁 本地报告目录:", manager.get_local_save_dir())
    print()
    
    print("📋 现有报告列表:")
    reports = manager.list_local_reports()
    if reports:
        for r in reports:
            print(f"  {r['filename']} ({r['size']} bytes, {r['mtime']})")
    else:
        print("  (无)")
    print()
    
    # 测试生成路径
    today = datetime.now()
    filename, path = manager.generate_report_path(today)
    print(f"📝 今日报告路径: {path}")
    print()
    
    # 测试云清理候选
    candidates = manager.cloud_cleanup_candidates(today)
    print(f"☁️  云清理候选: {candidates}")
    print()
    
    print(f"☁️  默认上传?: {manager.should_upload_to_cloud()}")
    print(f"☁️  云文件夹 token: {manager.get_cloud_folder_token() or '(未配置)'}")


if __name__ == "__main__":
    main()
