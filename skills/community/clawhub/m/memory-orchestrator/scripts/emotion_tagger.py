#!/usr/bin/env python3
"""
记忆系统情感分析器
使用 qwen2.5:7b 进行零样本情感分类，为记忆添加情感标签和价值评分

功能:
- 零样本情感分类（兴奋、沮丧、启发、中性、困惑）
- 价值评分（1-5分）
- 批量处理记忆文件
- 更新 FAISS 索引元数据

依赖:
- ollama (qwen2.5:7b)
- 现有记忆系统基础设施
"""

import os
import sys
import json
import re
import hashlib
import logging
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass, asdict, field
import argparse

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 路径配置
WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_DIR = WORKSPACE / "memory"
MEMORY_MD = WORKSPACE / "MEMORY.md"
INDEX_DIR = WORKSPACE / "index"
EMOTION_INDEX_FILE = INDEX_DIR / "emotion_index.json"

# 情感标签定义
EMOTION_LABELS = {
    "兴奋": {"color": "#FFD700", "weight": 1.2, "keywords": ["成功", "完成", "上线", "突破", "搞定", "✅"]},
    "沮丧": {"color": "#808080", "weight": 0.8, "keywords": ["失败", "错误", "问题", "❌", "bug", "失败"]},
    "启发": {"color": "#00CED1", "weight": 1.1, "keywords": ["发现", "学到", "理解", "启发", "灵感", "💡"]},
    "中性": {"color": "#A9A9A9", "weight": 1.0, "keywords": []},
    "困惑": {"color": "#FFA500", "weight": 0.9, "keywords": ["疑惑", "不确定", "为什么", "怎么", "?"]}
}

# Ollama 模型配置
OLLAMA_MODEL = "qwen2.5:7b"
OLLAMA_TIMEOUT = 60  # 秒


@dataclass
class EmotionTag:
    """情感标签数据结构"""
    emotion: str  # 兴奋、沮丧、启发、中性、困惑
    confidence: float  # 0.0 - 1.0
    value_score: int  # 1-5
    keywords_matched: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class MemoryEntry:
    """记忆条目数据结构"""
    id: str
    source: str
    content: str
    emotion_tag: Optional[EmotionTag] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    reference_count: int = 0  # 引用次数，用于价值评分


def call_ollama(prompt: str, model: str = OLLAMA_MODEL) -> Optional[str]:
    """
    调用 Ollama API 进行推理
    使用 subprocess 调用 ollama run 命令
    """
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            timeout=OLLAMA_TIMEOUT
        )
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            logger.error(f"Ollama error: {result.stderr}")
            return None
            
    except subprocess.TimeoutExpired:
        logger.error(f"Ollama timeout after {OLLAMA_TIMEOUT}s")
        return None
    except Exception as e:
        logger.error(f"Failed to call Ollama: {e}")
        return None


def classify_emotion_zero_shot(text: str) -> Tuple[str, float]:
    """
    使用 qwen2.5:7b 进行零样本情感分类
    
    返回: (情感标签, 置信度)
    """
    prompt = f"""分析以下文本的情感，从以下五个选项中选择最合适的一个：
【兴奋】、【沮丧】、【启发】、【中性】、【困惑】

文本：
{text[:500]}

请只输出一个情感标签和置信度（0.0-1.0），格式如下：
情感: XXX
置信度: 0.XX

不要输出其他内容。"""

    response = call_ollama(prompt)
    
    if response is None:
        return "中性", 0.5
    
    # 解析响应
    emotion = "中性"
    confidence = 0.5
    
    try:
        # 提取情感
        emotion_match = re.search(r"情感[：:]\s*([^\n]+)", response)
        if emotion_match:
            detected = emotion_match.group(1).strip()
            # 匹配已知标签
            for label in EMOTION_LABELS.keys():
                if label in detected:
                    emotion = label
                    break
        
        # 提取置信度
        conf_match = re.search(r"置信度[：:]\s*([\d.]+)", response)
        if conf_match:
            confidence = float(conf_match.group(1))
            confidence = max(0.0, min(1.0, confidence))
            
    except Exception as e:
        logger.warning(f"Failed to parse emotion response: {e}")
    
    return emotion, confidence


def calculate_value_score(entry: MemoryEntry, emotion_tag: EmotionTag) -> int:
    """
    计算记忆价值评分 (1-5)
    
    评分因素：
    - 情感强度 (置信度)
    - 情感类型权重
    - 引用频率
    - 时间衰减
    - 关键词匹配
    """
    base_score = 3  # 基础分
    
    # 情感强度加成 (置信度 0-1 映射到 -1 到 +1)
    emotion_bonus = (emotion_tag.confidence - 0.5) * 2
    
    # 情感类型权重
    emotion_weight = EMOTION_LABELS.get(emotion_tag.emotion, {}).get("weight", 1.0)
    
    # 关键词匹配加成
    keyword_bonus = min(len(emotion_tag.keywords_matched) * 0.3, 1.0)
    
    # 引用频率加成
    ref_bonus = min(entry.reference_count * 0.2, 1.0)
    
    # 综合评分
    final_score = base_score + emotion_bonus + (emotion_weight - 1) * 2 + keyword_bonus + ref_bonus
    
    # 限制在 1-5 范围
    return max(1, min(5, round(final_score)))


def extract_keywords(text: str, emotion: str) -> List[str]:
    """提取匹配的情感关键词"""
    keywords = EMOTION_LABELS.get(emotion, {}).get("keywords", [])
    matched = []
    
    text_lower = text.lower()
    for kw in keywords:
        if kw.lower() in text_lower:
            matched.append(kw)
    
    return matched


def split_memory_sections(content: str) -> List[Dict[str, str]]:
    """
    将记忆文件拆分为独立段落
    返回段落列表，每个段落包含标题和内容
    """
    sections = []
    
    # 按标题拆分
    lines = content.split('\n')
    current_section = {"title": "", "content": "", "level": 0}
    current_content = []
    
    for line in lines:
        # 检测 Markdown 标题
        header_match = re.match(r'^(#{1,3})\s+(.+)$', line)
        
        if header_match:
            # 保存当前段落
            if current_content:
                current_section["content"] = '\n'.join(current_content).strip()
                if current_section["content"]:
                    sections.append(current_section)
            
            # 开始新段落
            level = len(header_match.group(1))
            title = header_match.group(2)
            current_section = {"title": title, "content": "", "level": level}
            current_content = []
        else:
            current_content.append(line)
    
    # 保存最后一个段落
    if current_content:
        current_section["content"] = '\n'.join(current_content).strip()
        if current_section["content"]:
            sections.append(current_section)
    
    # 如果没有标题，将整个内容作为一个段落
    if not sections and content.strip():
        sections.append({"title": "主内容", "content": content.strip(), "level": 0})
    
    return sections


def generate_entry_id(source: str, section_title: str, content_preview: str) -> str:
    """生成记忆条目唯一 ID"""
    hash_input = f"{source}:{section_title}:{content_preview[:50]}"
    hash_val = hashlib.md5(hash_input.encode()).hexdigest()[:8]
    timestamp = datetime.now().strftime('%Y%m%d')
    return f"mem_{timestamp}_{hash_val}"


def process_memory_file(file_path: Path, file_type: str) -> List[MemoryEntry]:
    """
    处理单个记忆文件
    
    返回记忆条目列表
    """
    entries = []
    
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        logger.error(f"Failed to read {file_path}: {e}")
        return entries
    
    # 拆分段落
    sections = split_memory_sections(content)
    
    for section in sections:
        if len(section["content"].strip()) < 20:  # 跳过过短段落
            continue
        
        # 创建记忆条目
        entry = MemoryEntry(
            id=generate_entry_id(file_path.name, section["title"], section["content"]),
            source=file_path.name,
            content=section["content"],
            metadata={
                "title": section["title"],
                "level": section["level"],
                "type": file_type,
                "file_path": str(file_path)
            }
        )
        
        entries.append(entry)
    
    return entries


def tag_memory_entry(entry: MemoryEntry, use_ollama: bool = True) -> EmotionTag:
    """
    为记忆条目添加情感标签
    
    Args:
        entry: 记忆条目
        use_ollama: 是否使用 Ollama 进行情感分析（否则使用关键词匹配）
    """
    if use_ollama:
        emotion, confidence = classify_emotion_zero_shot(entry.content)
    else:
        # 降级：关键词匹配
        emotion, confidence = "中性", 0.5
        max_matches = 0
        
        for label, config in EMOTION_LABELS.items():
            matches = [kw for kw in config["keywords"] if kw.lower() in entry.content.lower()]
            if len(matches) > max_matches:
                emotion = label
                confidence = min(0.5 + len(matches) * 0.1, 0.9)
                max_matches = len(matches)
    
    # 提取关键词
    keywords_matched = extract_keywords(entry.content, emotion)
    
    # 创建情感标签
    emotion_tag = EmotionTag(
        emotion=emotion,
        confidence=confidence,
        value_score=3,  # 初始值，稍后计算
        keywords_matched=keywords_matched
    )
    
    # 计算价值评分
    emotion_tag.value_score = calculate_value_score(entry, emotion_tag)
    
    return emotion_tag


def load_emotion_index() -> Dict[str, Any]:
    """加载情感索引"""
    if EMOTION_INDEX_FILE.exists():
        try:
            with open(EMOTION_INDEX_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load emotion index: {e}")
    
    return {
        "version": "1.0",
        "created_at": datetime.now().isoformat(),
        "entries": {},
        "statistics": {}
    }


def save_emotion_index(index: Dict[str, Any]):
    """保存情感索引"""
    INDEX_DIR.mkdir(exist_ok=True)
    
    with open(EMOTION_INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Saved emotion index to {EMOTION_INDEX_FILE}")


def update_statistics(index: Dict[str, Any]) -> Dict[str, Any]:
    """更新情感分布统计"""
    stats = {
        "total_entries": 0,
        "emotion_distribution": {label: 0 for label in EMOTION_LABELS.keys()},
        "value_distribution": {str(i): 0 for i in range(1, 6)},
        "avg_confidence": 0.0,
        "avg_value_score": 0.0,
        "last_updated": datetime.now().isoformat()
    }
    
    confidences = []
    value_scores = []
    
    for entry_id, entry_data in index["entries"].items():
        stats["total_entries"] += 1
        
        emotion = entry_data.get("emotion_tag", {}).get("emotion", "中性")
        if emotion in stats["emotion_distribution"]:
            stats["emotion_distribution"][emotion] += 1
        
        value = entry_data.get("emotion_tag", {}).get("value_score", 3)
        value_str = str(value)
        if value_str in stats["value_distribution"]:
            stats["value_distribution"][value_str] += 1
        
        confidences.append(entry_data.get("emotion_tag", {}).get("confidence", 0.5))
        value_scores.append(value)
    
    if confidences:
        stats["avg_confidence"] = sum(confidences) / len(confidences)
        stats["avg_value_score"] = sum(value_scores) / len(value_scores)
    
    return stats


def generate_text_chart(stats: Dict[str, Any]) -> str:
    """生成文字版情感分布图表"""
    lines = []
    lines.append("\n📊 情感分布统计")
    lines.append("=" * 50)
    
    total = stats["total_entries"]
    if total == 0:
        lines.append("暂无数据")
        return '\n'.join(lines)
    
    # 情感分布
    lines.append("\n情感分布:")
    for emotion, count in stats["emotion_distribution"].items():
        percentage = count / total * 100
        bar = "█" * int(percentage / 5)
        color = EMOTION_LABELS[emotion]["color"]
        lines.append(f"  {emotion:4s} [{color}] {bar} {count} ({percentage:.1f}%)")
    
    # 价值分布
    lines.append("\n价值评分分布:")
    for score, count in sorted(stats["value_distribution"].items(), key=lambda x: int(x[0]), reverse=True):
        percentage = count / total * 100
        bar = "★" * int(score) + "☆" * (5 - int(score))
        lines.append(f"  {score}分 {bar} {count} ({percentage:.1f}%)")
    
    # 统计摘要
    lines.append(f"\n统计摘要:")
    lines.append(f"  总条目数: {total}")
    lines.append(f"  平均置信度: {stats['avg_confidence']:.2%}")
    lines.append(f"  平均价值评分: {stats['avg_value_score']:.2f}/5")
    lines.append(f"  最后更新: {stats['last_updated']}")
    
    return '\n'.join(lines)


def generate_png_chart(stats: Dict[str, Any], output_path: Path) -> bool:
    """生成 PNG 图表（如果 matplotlib 可用）"""
    try:
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')  # 非交互式后端
        
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        
        # 情感分布饼图
        emotions = list(stats["emotion_distribution"].keys())
        counts = list(stats["emotion_distribution"].values())
        colors = [EMOTION_LABELS[e]["color"] for e in emotions]
        
        # 过滤零值
        non_zero = [(e, c, col) for e, c, col in zip(emotions, counts, colors) if c > 0]
        if non_zero:
            emotions, counts, colors = zip(*non_zero)
            axes[0].pie(counts, labels=emotions, colors=colors, autopct='%1.1f%%', startangle=90)
        axes[0].set_title('情感分布')
        
        # 价值评分柱状图
        scores = list(range(1, 6))
        values = [stats["value_distribution"].get(str(s), 0) for s in scores]
        axes[1].bar(scores, values, color='#4CAF50', edgecolor='black')
        axes[1].set_xlabel('价值评分')
        axes[1].set_ylabel('条目数')
        axes[1].set_title('价值评分分布')
        axes[1].set_xticks(scores)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Generated chart: {output_path}")
        return True
        
    except ImportError:
        logger.warning("matplotlib not available, skipping PNG chart generation")
        return False
    except Exception as e:
        logger.error(f"Failed to generate PNG chart: {e}")
        return False


def batch_process(use_ollama: bool = True, force_retag: bool = False) -> Dict[str, Any]:
    """
    批量处理所有记忆文件
    
    Args:
        use_ollama: 是否使用 Ollama 进行情感分析
        force_retag: 是否强制重新标注
    """
    logger.info("Starting batch emotion tagging...")
    
    # 加载现有索引
    index = load_emotion_index()
    
    # 收集所有记忆文件
    memory_files = []
    
    # MEMORY.md
    if MEMORY_MD.exists():
        memory_files.append((MEMORY_MD, "long_term"))
    
    # daily logs
    if MEMORY_DIR.exists():
        for daily_file in sorted(MEMORY_DIR.glob("*.md")):
            memory_files.append((daily_file, "daily"))
    
    logger.info(f"Found {len(memory_files)} memory files")
    
    total_entries = 0
    new_tags = 0
    skipped = 0
    
    for file_path, file_type in memory_files:
        logger.info(f"Processing {file_path.name}...")
        
        entries = process_memory_file(file_path, file_type)
        
        for entry in entries:
            total_entries += 1
            
            # 检查是否已标注
            if not force_retag and entry.id in index["entries"]:
                skipped += 1
                continue
            
            # 情感标注
            entry.emotion_tag = tag_memory_entry(entry, use_ollama)
            
            # 存储到索引
            index["entries"][entry.id] = {
                "source": entry.source,
                "content_preview": entry.content[:200] + "..." if len(entry.content) > 200 else entry.content,
                "emotion_tag": asdict(entry.emotion_tag),
                "metadata": entry.metadata,
                "created_at": entry.created_at,
                "reference_count": entry.reference_count
            }
            
            new_tags += 1
    
    # 更新统计
    index["statistics"] = update_statistics(index)
    
    # 保存索引
    save_emotion_index(index)
    
    logger.info(f"Batch processing complete: {total_entries} entries, {new_tags} new tags, {skipped} skipped")
    
    return index


def search_by_emotion(emotion: str, min_value: int = 1, max_value: int = 5) -> List[Dict[str, Any]]:
    """
    按情感和评分搜索记忆
    
    Args:
        emotion: 情感标签
        min_value: 最小价值评分
        max_value: 最大价值评分
    """
    index = load_emotion_index()
    results = []
    
    for entry_id, entry_data in index["entries"].items():
        entry_emotion = entry_data.get("emotion_tag", {}).get("emotion", "中性")
        entry_value = entry_data.get("emotion_tag", {}).get("value_score", 3)
        
        if entry_emotion == emotion and min_value <= entry_value <= max_value:
            results.append({
                "id": entry_id,
                "source": entry_data["source"],
                "content_preview": entry_data["content_preview"],
                "emotion": entry_emotion,
                "value_score": entry_value,
                "confidence": entry_data["emotion_tag"]["confidence"]
            })
    
    # 按价值评分降序排序
    results.sort(key=lambda x: x["value_score"], reverse=True)
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description="记忆系统情感分析器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 批量标注所有记忆
  python emotion_tagger.py batch
  
  # 使用关键词匹配（不调用 Ollama）
  python emotion_tagger.py batch --no-ollama
  
  # 强制重新标注
  python emotion_tagger.py batch --force
  
  # 查看统计
  python emotion_tagger.py stats
  
  # 生成图表
  python emotion_tagger.py chart --output emotion_chart.png
  
  # 按情感搜索
  python emotion_tagger.py search --emotion 兴奋 --min-value 4
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # 批量处理命令
    batch_parser = subparsers.add_parser("batch", help="批量情感标注")
    batch_parser.add_argument("--no-ollama", action="store_true", help="不使用 Ollama，仅关键词匹配")
    batch_parser.add_argument("--force", action="store_true", help="强制重新标注")
    
    # 统计命令
    subparsers.add_parser("stats", help="查看情感分布统计")
    
    # 图表命令
    chart_parser = subparsers.add_parser("chart", help="生成情感分布图表")
    chart_parser.add_argument("--output", default="emotion_chart.png", help="输出文件路径")
    chart_parser.add_argument("--png", action="store_true", help="生成 PNG 图表（需要 matplotlib）")
    
    # 搜索命令
    search_parser = subparsers.add_parser("search", help="按情感搜索记忆")
    search_parser.add_argument("--emotion", required=True, choices=list(EMOTION_LABELS.keys()), help="情感标签")
    search_parser.add_argument("--min-value", type=int, default=1, choices=range(1, 6), help="最小价值评分")
    search_parser.add_argument("--max-value", type=int, default=5, choices=range(1, 6), help="最大价值评分")
    search_parser.add_argument("--top", type=int, default=10, help="返回结果数量")
    
    args = parser.parse_args()
    
    if args.command == "batch":
        index = batch_process(use_ollama=not args.no_ollama, force_retag=args.force)
        print(f"\n✅ 批量标注完成")
        print(f"   总条目: {index['statistics']['total_entries']}")
        print(f"   平均置信度: {index['statistics']['avg_confidence']:.2%}")
        print(f"   平均价值评分: {index['statistics']['avg_value_score']:.2f}/5")
        
    elif args.command == "stats":
        index = load_emotion_index()
        chart = generate_text_chart(index["statistics"])
        print(chart)
        
    elif args.command == "chart":
        index = load_emotion_index()
        
        if args.png:
            output_path = WORKSPACE / args.output
            if generate_png_chart(index["statistics"], output_path):
                print(f"✅ 图表已生成: {output_path}")
            else:
                print("❌ PNG 图表生成失败，显示文字版图表")
                print(generate_text_chart(index["statistics"]))
        else:
            print(generate_text_chart(index["statistics"]))
            
    elif args.command == "search":
        results = search_by_emotion(args.emotion, args.min_value, args.max_value)
        
        print(f"\n🔍 搜索结果: 情感={args.emotion}, 评分={args.min_value}-{args.max_value}")
        print("=" * 60)
        
        if not results:
            print("未找到匹配的记忆")
        else:
            for i, r in enumerate(results[:args.top], 1):
                print(f"\n{i}. [{r['value_score']}★] {r['source']}")
                print(f"   {r['content_preview']}")
                print(f"   置信度: {r['confidence']:.2%}")
                
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
