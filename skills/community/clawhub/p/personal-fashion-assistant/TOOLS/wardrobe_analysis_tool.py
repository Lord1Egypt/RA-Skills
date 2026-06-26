# -*- coding: utf-8 -*-
"""
Smart Wardrobe Analysis Tool
============================
读取用户衣橱偏好设定 (USER.md 中 smart_wardrobe_preference) 
及原始衣服数据 (inventory.md)，整合提示词准备大模型调用。
"""

import os
import re
import json
from datetime import datetime

class WardrobeAnalysisManager:
    """智能衣橱看板分析管理器"""

    def __init__(self, base_dir="./smart_wardrobe", prompt_path=None):
        # ── 路径约定 ──
        self.base_dir = base_dir
        self.data_dir = os.path.join(self.base_dir, "wardrobe_data")
        self.temp_dir = os.path.join(self.base_dir, "temp_upload")
        self.inventory_file = os.path.join(self.base_dir, "inventory.md")
        self.dashboard_dir = os.path.join(self.base_dir, "wardrobe_dashboard")
        self.user_file = os.path.join(self.base_dir, "USER.md")
        
        self.prompt_path = prompt_path or os.path.join(
            ".", "skills", "wardrobe_manager", "wardrobe_analysis_prompt.md"
        )
        
        # 为了兼容在TOOLS文件夹下直接运行的相对路径测试，加入智能回退
        if not os.path.exists(self.prompt_path):
            _SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
            fallback = os.path.join(os.path.dirname(_SCRIPT_DIR), "PROMPT", "wardrobe_analysis_prompt.md")
            if os.path.exists(fallback):
                self.prompt_path = fallback

    def _load_prompt_template(self) -> str:
        """读取指定路径的提示词模版文件"""
        if not os.path.exists(self.prompt_path):
            raise FileNotFoundError(f"提示词模板文件未找到: {self.prompt_path}")
            
        with open(self.prompt_path, "r", encoding="utf-8") as f:
            return f.read()

    def generate_analysis_prompt(self, preferences: dict, inventory_md: str) -> str:
        """
        生成衣橱分析提示词
        
        参数:
            preferences (dict): 用户衣橱管理偏好 (来源于 USER.md 中的 smart_wardrobe_preference)
                                包含键如 'custom_item_limit', 'custom_color_ratio', 'up_down_ratio'
            inventory_md (str): 衣橱记录表格文本 (来源于 inventory.md)
            
        返回:
            str: 填充完整的诊断提示词
        """
        prompt_template = self._load_prompt_template()
        
        # 提取默认或偏好设定
        item_limit = preferences.get("custom_item_limit", "35")
        color_ratio = preferences.get("custom_color_ratio", "60%主色/30%辅助色/10%提亮色")
        up_down_ratio = preferences.get("up_down_ratio", "1:2")
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # 替换模版中的占位符
        prompt = prompt_template.replace("{{35}}", str(item_limit))
        prompt = prompt.replace("{{60%主色/30%辅助色/10%提亮色}}", str(color_ratio))
        prompt = prompt.replace("{{1:2}}", str(up_down_ratio))
        prompt = prompt.replace("{{此处粘贴你的衣橱列表，如表格内容}}", f"\n{inventory_md}\n")
        
        # 支持替换模板里的特定日期，或使用正则匹配动态日期
        prompt = re.sub(r"\{\{\d{4}-\d{2}-\d{2}\}\}", current_date, prompt)
        
        # 兼容直接使用的字面常量
        prompt = prompt.replace("{{2026-03-31}}", current_date)
        
        return prompt

    def build_analysis_payload(self, preferences: dict, inventory_md: str, model: str = "MiniMax-M2.7", max_tokens: int = 4000) -> dict:
        """
        构建衣橱诊断分析的 MiniMax 模型请求 payload
        
        参数:
            preferences (dict): 用户衣橱管理偏好
            inventory_md (str): 序列化的 inventory.md 原文文本
            model (str):        模型名称（默认 MiniMax-M2.7）
            max_tokens (int):   最大输出 token 数（默认 4000，HTML面板需要较大量token）
            
        返回:
            dict: {
                'status':   'success',
                'payload':  dict,
                'prompt':   str
            }
        """
        if not inventory_md or not inventory_md.strip():
            return {
                "status": "error",
                "message": "衣橱原始数据为空，无法进行分析"
            }
            
        try:
            prompt = self.generate_analysis_prompt(preferences, inventory_md)
        except Exception as e:
            return {
                "status": "error",
                "message": f"生成提示词失败: {str(e)}"
            }
            
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": max_tokens,
        }
        
        return {
            "status": "success",
            "payload": payload,
            "prompt": prompt
        }

    def save_html_dashboard(self, llm_response: str, preferences: dict = None) -> dict:
        """
        获取大模型返回的 HTML 代码，并保存为 .html 文件
        
        参数:
            llm_response (str): 大模型返回的包含 HTML 代码的字符串
            preferences (dict): 用户衣橱管理偏好 (来源于 USER.md 中的 smart_wardrobe_preference)，可选
            
        返回:
            dict: 包含保存状态和文件路径
        """
        # 确保保存目录存在
        os.makedirs(self.dashboard_dir, exist_ok=True)
            
        html_content = llm_response
        
        # 清理可能包含的 Markdown 代码块标记
        if "```html" in html_content:
            match = re.search(r"```html\s*(.*?)\s*```", html_content, re.DOTALL | re.IGNORECASE)
            if match:
                html_content = match.group(1)
        elif "```" in html_content:
             match = re.search(r"```\s*(.*?)\s*```", html_content, re.DOTALL)
             if match:
                 html_content = match.group(1)
                 
        # 进一步确保以 <!DOCTYPE html> 开头
        start_idx = html_content.find("<!DOCTYPE html>")
        if start_idx != -1:
            html_content = html_content[start_idx:]
            
        current_date = datetime.now().strftime("%Y-%m-%d")
        filename = f"{current_date}个人电子衣橱看板.html"
        filepath = os.path.join(self.dashboard_dir, filename)
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html_content.strip())
            
            # 尝试提取并保存统计数据至 USER.md
            stats_match = re.search(r'<script\s+type="application/json"\s+id="wardrobe-stats">\s*(.*?)\s*</script>', html_content, re.DOTALL | re.IGNORECASE)
            if stats_match:
                try:
                    stats_data = json.loads(stats_match.group(1))
                    self._update_user_stats(stats_data, preferences)
                except Exception as e:
                    print(f"[警告] 解析或写入统计数据失败: {str(e)}")

            return {
                "status": "success",
                "message": "HTML 看板保存成功",
                "filepath": filepath
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"保存 HTML 看板失败: {str(e)}"
            }

    def _update_user_stats(self, stats_data: dict, preferences: dict = None):
        """将统计的实际色彩比例、实际总件数以及各目标写入 USER.md"""
        if not os.path.exists(self.user_file):
            return
            
        with open(self.user_file, "r", encoding="utf-8") as f:
            content = f.read()
            
        actual_total = stats_data.get("actual_total_items", "-")
        actual_color = stats_data.get("actual_color_ratio", "-")
        
        preferences = preferences or {}
        item_limit = preferences.get("custom_item_limit", "35")
        color_ratio = preferences.get("custom_color_ratio", "60%主色/30%辅助色/10%提亮色")
        target_limit = item_limit
        target_color = color_ratio
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        stats_section = f"\n\n## 衣橱实时统计与目标 (Dashboard Stats)\n\n> 最后更新：{current_date}\n\n"
        stats_section += "| 指标项 | 实际当前值 | 设定的管理目标 |\n"
        stats_section += "|---|---|---|\n"
        stats_section += f"| **总件数** | {actual_total} 件 | {target_limit} 件 |\n"
        stats_section += f"| **色彩矩阵比例** | {actual_color} | {target_color} |\n"
        
        if "## 衣橱实时统计与目标 (Dashboard Stats)" in content:
            content = re.sub(r"\n*## 衣橱实时统计与目标 \(Dashboard Stats\).*?(?=\n## |\Z)", stats_section, content, flags=re.DOTALL)
        else:
            content += stats_section
            
        with open(self.user_file, "w", encoding="utf-8") as f:
            f.write(content)

if __name__ == "__main__":
    # 简单测试代码
    manager = WardrobeAnalysisManager()
    
    sample_preferences = {
        "custom_item_limit": 40,
        "custom_color_ratio": "50:30:20 (黑白灰/大地色/亮色)",
        "up_down_ratio": "1:1.5"
    }
    sample_inventory = "| 分类 | 衣物编号 | 主要颜色 | 材质 | 风格 | 适宜的温度 | 适合的场景 | 当日日期 |\n| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n| 上衣 | TEST12345678 | 白色 | 纯棉 | 极简 | 20°C | 休闲 | 2026-03-30 |"
    
    # 为了让测试能直接运行，mock 一下模板加载
    _original_load = manager._load_prompt_template
    def mock_load():
        return "管理目标：单季上限 {{35}} 件；色彩配比目标 {{60%主色/30%辅助色/10%提亮色}}；上下装理想比例 {{1:2}}。\n原始数据：{{此处粘贴你的衣橱列表，如表格内容}}\n季节性缺口：基于当前日期 {{2026-03-31}}"
    
    try:
        prompt_content = _original_load()
    except Exception:
        manager._load_prompt_template = mock_load

    result = manager.build_analysis_payload(sample_preferences, sample_inventory)
    print("="*40)
    print("生成状态:", result["status"])
    if result["status"] == "success":
        print("\n[生成的提示词]")
        print(result["prompt"])
    print("="*40)
