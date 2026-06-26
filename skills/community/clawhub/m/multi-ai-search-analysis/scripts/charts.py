#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
charts.py - 多 AI 搜索分析技能图表生成模块

功能：
- 生成数据对比柱状图
- 生成质量评分雷达图
- 生成时间趋势折线图
- 生成词云图（可选）

依赖：
- matplotlib
- numpy
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from pathlib import Path
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ChartGenerator:
    """图表生成器"""
    
    def __init__(self, output_dir: str = None, font_path: str = None):
        """
        初始化图表生成器
        
        Args:
            output_dir: 输出目录，默认为 reports/charts
            font_path: 中文字体路径，用于支持中文显示
        """
        self.output_dir = Path(output_dir) if output_dir else Path(__file__).parent.parent / "reports" / "charts"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 配置中文字体
        self._setup_chinese_font(font_path)
        
        # 配置样式
        plt.style.use('seaborn-v0_8-whitegrid')
        
    def _setup_chinese_font(self, font_path: str = None):
        """配置中文字体支持"""
        # 尝试使用指定字体
        if font_path and Path(font_path).exists():
            font_prop = fm.FontProperties(fname=font_path)
            plt.rcParams['font.family'] = font_prop.get_name()
            logger.info(f"使用自定义字体：{font_path}")
            return
        
        # 尝试系统常见中文字体
        common_chinese_fonts = [
            'SimHei',           # 黑体 (Windows)
            'Microsoft YaHei',  # 微软雅黑 (Windows)
            'SimSun',           # 宋体 (Windows)
            'Arial Unicode MS', # macOS
            'Heiti TC',         # macOS
            'WenQuanYi Micro Hei', # Linux
        ]
        
        for font_name in common_chinese_fonts:
            try:
                font_prop = fm.FontProperties(family=font_name)
                plt.rcParams['font.family'] = font_name
                plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
                logger.info(f"使用中文字体：{font_name}")
                return
            except:
                continue
        
        # 如果没有中文字体，使用默认字体并警告
        logger.warning("未找到中文字体，中文可能显示为方框。建议安装 SimHei 或 Microsoft YaHei 字体")
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['axes.unicode_minus'] = False
    
    def generate_comparison_bar_chart(self, data: dict, title: str = "数据对比", 
                                       ylabel: str = "数值", filename: str = None) -> str:
        """
        生成数据对比柱状图
        
        Args:
            data: 数据字典，格式如 {"指标 1": {"DeepSeek": 100, "Qwen": 105}, "指标 2": {...}}
            title: 图表标题
            ylabel: Y 轴标签
            filename: 输出文件名（不含扩展名）
        
        Returns:
            输出文件路径
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"comparison_{timestamp}"
        
        # 准备数据
        ai_names = list(data[list(data.keys())[0]].keys())
        metrics = list(data.keys())
        x = np.arange(len(metrics))
        width = 0.8 / len(ai_names)
        
        # 创建图表
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 绘制柱状图
        for i, ai_name in enumerate(ai_names):
            values = [data[metric].get(ai_name, 0) for metric in metrics]
            offset = (i - len(ai_names) / 2 + 0.5) * width
            ax.bar(x + offset, values, width, label=ai_name, alpha=0.8)
        
        # 配置图表
        ax.set_xlabel('指标', fontsize=12, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(metrics, rotation=15, ha='right')
        ax.legend(loc='best')
        ax.grid(axis='y', alpha=0.3)
        
        # 添加数值标签
        for i, ai_name in enumerate(ai_names):
            values = [data[metric].get(ai_name, 0) for metric in metrics]
            offset = (i - len(ai_names) / 2 + 0.5) * width
            for j, v in enumerate(values):
                ax.text(j + offset, v, str(v), ha='center', va='bottom', fontsize=8)
        
        # 保存图表
        output_path = self.output_dir / f"{filename}.png"
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info(f"柱状图已保存：{output_path}")
        return str(output_path)
    
    def generate_quality_radar_chart(self, scores: dict, title: str = "AI 质量评分对比", 
                                      filename: str = None) -> str:
        """
        生成质量评分雷达图
        
        Args:
            scores: 评分字典，格式如 {"DeepSeek": {"字数": 80, "数据点": 90, "结构": 85, "引用": 70, "具体性": 75}, ...}
            title: 图表标题
            filename: 输出文件名（不含扩展名）
        
        Returns:
            输出文件路径
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"quality_radar_{timestamp}"
        
        # 准备数据
        ai_names = list(scores.keys())
        dimensions = list(scores[ai_names[0]].keys())
        num_vars = len(dimensions)
        
        # 计算角度
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]  # 闭合
        
        # 创建图表
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
        
        # 颜色映射
        colors = plt.cm.Set3(np.linspace(0, 1, len(ai_names)))
        
        # 绘制每个 AI 的雷达图
        for i, ai_name in enumerate(ai_names):
            values = [scores[ai_name][dim] for dim in dimensions]
            values += values[:1]  # 闭合
            
            ax.plot(angles, values, 'o-', linewidth=2, label=ai_name, color=colors[i])
            ax.fill(angles, values, alpha=0.15, color=colors[i])
        
        # 配置图表
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_thetagrids(np.degrees(angles[:-1]), dimensions, fontsize=11, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_rlabel_position(0)
        ax.set_ylim(0, 100)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        ax.grid(True)
        
        # 保存图表
        output_path = self.output_dir / f"{filename}.png"
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info(f"雷达图已保存：{output_path}")
        return str(output_path)
    
    def generate_trend_line_chart(self, trend_data: dict, title: str = "趋势分析", 
                                   xlabel: str = "时间", ylabel: str = "数值",
                                   filename: str = None) -> str:
        """
        生成时间趋势折线图
        
        Args:
            trend_data: 趋势数据，格式如 {"DeepSeek": {"2024-01": 100, "2024-02": 105}, ...}
            title: 图表标题
            xlabel: X 轴标签
            ylabel: Y 轴标签
            filename: 输出文件名（不含扩展名）
        
        Returns:
            输出文件路径
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"trend_{timestamp}"
        
        # 准备数据
        ai_names = list(trend_data.keys())
        time_points = list(trend_data[ai_names[0]].keys())
        
        # 创建图表
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 颜色映射
        colors = plt.cm.Set2(np.linspace(0, 1, len(ai_names)))
        
        # 绘制折线图
        for i, ai_name in enumerate(ai_names):
            values = [trend_data[ai_name].get(t, 0) for t in time_points]
            ax.plot(time_points, values, marker='o', linewidth=2, label=ai_name, color=colors[i])
        
        # 配置图表
        ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        # 旋转 X 轴标签
        plt.xticks(rotation=45, ha='right')
        
        # 保存图表
        output_path = self.output_dir / f"{filename}.png"
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info(f"折线图已保存：{output_path}")
        return str(output_path)
    
    def generate_multi_chart_report(self, comparison_data: dict = None, 
                                     quality_scores: dict = None,
                                     trend_data: dict = None,
                                     report_title: str = "多 AI 分析报告") -> list:
        """
        生成综合图表报告（包含多种图表）
        
        Args:
            comparison_data: 对比数据（用于柱状图）
            quality_scores: 质量评分（用于雷达图）
            trend_data: 趋势数据（用于折线图）
            report_title: 报告标题
        
        Returns:
            生成的图表文件路径列表
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        charts = []
        
        # 生成柱状图
        if comparison_data:
            chart_path = self.generate_comparison_bar_chart(
                comparison_data, 
                title=f"{report_title} - 数据对比",
                filename=f"report_comparison_{timestamp}"
            )
            charts.append(chart_path)
        
        # 生成雷达图
        if quality_scores:
            chart_path = self.generate_quality_radar_chart(
                quality_scores,
                title=f"{report_title} - 质量评分",
                filename=f"report_quality_{timestamp}"
            )
            charts.append(chart_path)
        
        # 生成折线图
        if trend_data:
            chart_path = self.generate_trend_line_chart(
                trend_data,
                title=f"{report_title} - 趋势分析",
                filename=f"report_trend_{timestamp}"
            )
            charts.append(chart_path)
        
        logger.info(f"共生成 {len(charts)} 张图表")
        return charts


# 测试代码
if __name__ == "__main__":
    # 测试数据
    test_comparison_data = {
        "油价预测": {"DeepSeek": 103, "Qwen": 105, "豆包": 104, "Kimi": 102, "Gemini": 106},
        "通胀率": {"DeepSeek": 3.8, "Qwen": 4.1, "豆包": 3.9, "Kimi": 4.0, "Gemini": 4.2},
        "GDP 影响": {"DeepSeek": -0.5, "Qwen": -0.7, "豆包": -0.6, "Kimi": -0.8, "Gemini": -0.65}
    }
    
    test_quality_scores = {
        "DeepSeek": {"字数": 85, "数据点": 90, "结构": 80, "引用": 75, "具体性": 85},
        "Qwen": {"字数": 80, "数据点": 85, "结构": 90, "引用": 70, "具体性": 80},
        "豆包": {"字数": 90, "数据点": 80, "结构": 75, "引用": 85, "具体性": 90},
        "Kimi": {"字数": 75, "数据点": 95, "结构": 85, "引用": 90, "具体性": 75},
        "Gemini": {"字数": 88, "数据点": 88, "结构": 88, "引用": 80, "具体性": 88}
    }
    
    # 生成图表
    generator = ChartGenerator()
    
    print("生成对比柱状图...")
    generator.generate_comparison_bar_chart(test_comparison_data, "伊朗局势 - 关键数据对比")
    
    print("生成质量评分雷达图...")
    generator.generate_quality_radar_chart(test_quality_scores, "五家 AI 质量评分对比")
    
    print("完成！图表保存在 reports/charts/ 目录")
