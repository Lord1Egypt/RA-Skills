#!/usr/bin/env python3
"""可视化工具 - 蒸馏过程和结果可视化"""

import json
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # 无GUI环境

from pathlib import Path
from typing import Dict, List, Optional
import numpy as np


def plot_training_curves(loss_history: Dict[str, List[float]],
                        output_path: str,
                        title: str = "Training Progress"):
    """绘制训练曲线"""

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(title, fontsize=14, fontweight='bold')

    # 损失曲线
    ax1 = axes[0, 0]
    if 'train' in loss_history:
        ax1.plot(loss_history['train'], label='Train Loss', linewidth=2)
    if 'eval' in loss_history:
        ax1.plot(loss_history['eval'], label='Eval Loss', linewidth=2)
    ax1.set_xlabel('Step')
    ax1.set_ylabel('Loss')
    ax1.set_title('Loss Curve')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 学习率曲线
    ax2 = axes[0, 1]
    if 'learning_rate' in loss_history:
        ax2.plot(loss_history['learning_rate'], color='green', linewidth=2)
        ax2.set_xlabel('Step')
        ax2.set_ylabel('Learning Rate')
        ax2.set_title('Learning Rate Schedule')
        ax2.set_yscale('log')
        ax2.grid(True, alpha=0.3)

    # 温度调度
    ax3 = axes[1, 0]
    if 'temperature' in loss_history:
        ax3.plot(loss_history['temperature'], color='orange', linewidth=2)
        ax3.set_xlabel('Step')
        ax3.set_ylabel('Temperature')
        ax3.set_title('Temperature Schedule')
        ax3.grid(True, alpha=0.3)

    # Alpha调度
    ax4 = axes[1, 1]
    if 'alpha' in loss_history:
        ax4.plot(loss_history['alpha'], color='purple', linewidth=2)
        ax4.set_xlabel('Step')
        ax4.set_ylabel('Alpha (Soft Label Weight)')
        ax4.set_title('Alpha Schedule')
        ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"训练曲线已保存: {output_path}")


def plot_capability_radar(evaluation_results: Dict, output_path: str):
    """绘制能力雷达图"""

    categories = [
        'Capability\nRetention',
        'Style\nSimilarity',
        'Generalization',
        'Efficiency\nSpeedup',
        'Memory\nReduction'
    ]

    # 提取数值
    retention = evaluation_results.get('capability_retention', {})
    style = evaluation_results.get('style_similarity', {})
    gen = evaluation_results.get('generalization', {})
    eff = evaluation_results.get('efficiency', {})

    values = [
        retention.get('retention_rate', 0) * 100,
        (1 - style.get('kl_divergence', 0.5)) * 100,  # KL越小越好
        (1 - gen.get('drop', 0.1)) * 100,
        min(eff.get('speedup', 1) / 5 * 100, 100),  # 归一化到5x
        min(eff.get('memory_reduction', 1) / 5 * 100, 100)
    ]

    # 闭合雷达图
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    values_plot = values + values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    ax.plot(angles, values_plot, 'o-', linewidth=2, color='#2196F3')
    ax.fill(angles, values_plot, alpha=0.25, color='#2196F3')

    # 设置标签
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, size=10)
    ax.set_ylim(0, 100)
    ax.set_title('蒸馏评估雷达图', fontsize=14, fontweight='bold', pad=20)

    # 添加数值标签
    for angle, value, cat in zip(angles[:-1], values, categories):
        ax.text(angle, value + 10, f'{value:.1f}', ha='center', va='center', fontsize=9)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"雷达图已保存: {output_path}")


def plot_comparison_bar(baseline_acc: float,
                       distilled_acc: float,
                       teacher_acc: float,
                       output_path: str):
    """绘制准确率对比柱状图"""

    models = ['Baseline\n(未蒸馏)', 'Distilled\n(蒸馏后)', 'Teacher\n(教师模型)']
    accuracies = [baseline_acc * 100, distilled_acc * 100, teacher_acc * 100]
    colors = ['#FF5722', '#4CAF50', '#2196F3']

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(models, accuracies, color=colors, edgecolor='black', linewidth=1.5)

    # 添加数值标签
    for bar, acc in zip(bars, accuracies):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{acc:.1f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

    # 添加保持率标注
    retention = (distilled_acc - baseline_acc) / (teacher_acc - baseline_acc) * 100
    ax.axhline(y=teacher_acc * 100, color='blue', linestyle='--', alpha=0.5, label='Teacher Level')
    ax.text(1, distilled_acc * 100 + 5, f'保持率: {retention:.1f}%',
            ha='center', fontsize=11, color='green', fontweight='bold')

    ax.set_ylabel('Accuracy (%)', fontsize=12)
    ax.set_title('模型准确率对比', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 105)
    ax.legend()
    ax.grid(True, axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"对比图已保存: {output_path}")


def plot_curriculum_distribution(level_counts: Dict[str, int], output_path: str):
    """绘制课程难度分布饼图"""

    labels = list(level_counts.keys())
    sizes = list(level_counts.values())
    colors = ['#4CAF50', '#FFC107', '#F44336']
    explode = (0.02, 0.02, 0.05)

    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels,
                                       colors=colors, autopct='%1.1f%%',
                                       shadow=True, startangle=90)

    # 美化
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(12)
        autotext.set_fontweight('bold')

    ax.set_title('课程数据难度分布', fontsize=14, fontweight='bold')

    # 添加图例说明
    legend_labels = [
        f'Level 1 (基础): {level_counts.get("LEVEL_1", 0)}',
        f'Level 2 (进阶): {level_counts.get("LEVEL_2", 0)}',
        f'Level 3 (挑战): {level_counts.get("LEVEL_3", 0)}'
    ]
    ax.legend(wedges, legend_labels, title="难度级别", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"课程分布图已保存: {output_path}")


def plot_adversarial_heatmap(confusion_matrix: np.ndarray,
                             labels: List[str],
                             output_path: str):
    """绘制对抗样本热力图"""

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(confusion_matrix, cmap='YlOrRd')

    # 设置刻度
    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)

    # 旋转x轴标签
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    # 添加数值
    for i in range(len(labels)):
        for j in range(len(labels)):
            text = ax.text(j, i, int(confusion_matrix[i, j]),
                          ha="center", va="center", color="black", fontsize=12)

    ax.set_xlabel("教师模型预测", fontsize=12)
    ax.set_ylabel("学生模型预测", fontsize=12)
    ax.set_title("对抗样本混淆矩阵", fontsize=14, fontweight='bold')

    fig.colorbar(im, ax=ax, label='样本数')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"热力图已保存: {output_path}")


def generate_full_report(evaluation_file: str,
                        training_log: Optional[str],
                        output_dir: str):
    """生成完整可视化报告"""

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # 加载评估结果
    with open(evaluation_file) as f:
        eval_results = json.load(f)

    # 雷达图
    plot_capability_radar(eval_results, f"{output_dir}/radar.png")

    # 对比图
    cap = eval_results.get('capability_retention', {})
    plot_comparison_bar(
        cap.get('baseline_accuracy', 0.65),
        cap.get('distilled_accuracy', 0.82),
        cap.get('teacher_accuracy', 0.95),
        f"{output_dir}/comparison.png"
    )

    # 训练曲线
    if training_log and Path(training_log).exists():
        with open(training_log) as f:
            train_data = json.load(f)
        plot_training_curves(train_data, f"{output_dir}/training_curves.png")

    print(f"\n✅ 完整报告已生成: {output_dir}/")
    print("包含文件:")
    print("  - radar.png: 能力评估雷达图")
    print("  - comparison.png: 准确率对比")
    if training_log:
        print("  - training_curves.png: 训练过程曲线")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-file", required=True, help="评估结果JSON")
    parser.add_argument("--train-log", help="训练日志JSON")
    parser.add_argument("--output-dir", default="outputs/visualization")
    args = parser.parse_args()

    generate_full_report(args.eval_file, args.train_log, args.output_dir)
