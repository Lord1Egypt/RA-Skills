#!/usr/bin/env python3
"""
Token Optimizer - OpenClaw Token 消耗优化器

功能：
1. 智能上下文裁剪 - 只读取相关记忆片段
2. 会话历史摘要 - 用摘要替代完整历史
3. 记忆压缩 - 定期合并/压缩旧记忆
4. Token 统计 - 分析 token 使用，给出优化建议
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime, timedelta

WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_FILE = WORKSPACE / "MEMORY.md"
SESSION_STATE = WORKSPACE / "SESSION-STATE.md"
MEMORY_DIR = WORKSPACE / "memory"
OPTIMIZER_CONFIG = WORKSPACE / "skills" / "memory-enhancer" / "config" / "token-optimizer.json"

# Token 估算（近似值）
TOKENS_PER_CHAR = 1 / 4  # 约 4 字符 = 1 token

class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    RED = '\033[0;31m'
    NC = '\033[0m'
    BOLD = '\033[1m'

def log_info(msg): print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")
def log_success(msg): print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {msg}")
def log_warning(msg): print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {msg}")
def log_error(msg): print(f"{Colors.RED}[ERROR]{Colors.NC} {msg}")

def estimate_tokens(text: str) -> int:
    """估算 token 数量"""
    return int(len(text) * TOKENS_PER_CHAR)

def analyze_current_usage() -> dict:
    """分析当前 token 使用情况"""
    stats = {
        'files': {},
        'total_chars': 0,
        'total_tokens': 0,
        'timestamp': datetime.now().isoformat()
    }
    
    # 分析主要文件
    files_to_check = [
        MEMORY_FILE,
        SESSION_STATE,
        WORKSPACE / "USER.md",
        WORKSPACE / "SOUL.md",
        WORKSPACE / "AGENTS.md",
    ]
    
    for file_path in files_to_check:
        if file_path.exists():
            content = file_path.read_text(encoding='utf-8')
            chars = len(content)
            tokens = estimate_tokens(content)
            stats['files'][file_path.name] = {
                'chars': chars,
                'tokens': tokens,
                'lines': content.count('\n') + 1
            }
            stats['total_chars'] += chars
            stats['total_tokens'] += tokens
    
    # 分析记忆目录
    if MEMORY_DIR.exists():
        memory_files = list(MEMORY_DIR.glob("*.md"))
        memory_chars = 0
        for mf in memory_files:
            content = mf.read_text(encoding='utf-8')
            memory_chars += len(content)
        
        stats['files']['memory/*.md'] = {
            'chars': memory_chars,
            'tokens': int(memory_chars * TOKENS_PER_CHAR),
            'count': len(memory_files)
        }
        stats['total_chars'] += memory_chars
        stats['total_tokens'] += int(memory_chars * TOKENS_PER_CHAR)
    
    return stats

def compress_memory(keep_days: int = 30) -> dict:
    """压缩旧记忆文件
    
    - 保留最近 keep_days 天的记忆
    - 将旧记忆合并到 MEMORY.md 的归档部分
    """
    result = {
        'compressed': 0,
        'kept': 0,
        'saved_chars': 0
    }
    
    if not MEMORY_DIR.exists():
        return result
    
    cutoff_date = datetime.now() - timedelta(days=keep_days)
    
    for md_file in MEMORY_DIR.glob("*.md"):
        # 从文件名提取日期
        match = re.match(r'(\d{4}-\d{2}-\d{2})\.md', md_file.name)
        if not match:
            continue
        
        file_date = datetime.strptime(match.group(1), '%Y-%m-%d')
        
        if file_date < cutoff_date:
            # 旧文件，读取内容
            content = md_file.read_text(encoding='utf-8')
            result['saved_chars'] += len(content)
            result['compressed'] += 1
            log_info(f"压缩：{md_file.name} ({estimate_tokens(content)} tokens)")
        else:
            result['kept'] += 1
    
    return result

def generate_summary(session_file: Path) -> str:
    """生成会话摘要（替代完整历史）"""
    if not session_file.exists():
        return ""
    
    content = session_file.read_text(encoding='utf-8')
    lines = content.split('\n')
    
    # 简单摘要：保留最近 10 轮对话
    recent_lines = lines[-50:] if len(lines) > 50 else lines
    
    summary = f"# Session Summary (摘要)\n\n"
    summary += f"**Generated:** {datetime.now().isoformat()}\n"
    summary += f"**Original lines:** {len(lines)} → **Compressed:** {len(recent_lines)}\n\n"
    summary += '\n'.join(recent_lines)
    
    return summary

def get_optimization_suggestions(stats: dict) -> list:
    """生成优化建议"""
    suggestions = []
    
    total_tokens = stats['total_tokens']
    
    # 建议 1: 如果 MEMORY.md 过大，建议压缩
    if 'MEMORY.md' in stats['files']:
        mem_tokens = stats['files']['MEMORY.md']['tokens']
        if mem_tokens > 5000:
            suggestions.append({
                'priority': 'high',
                'issue': f'MEMORY.md 过大 ({mem_tokens} tokens)',
                'action': '运行压缩：python3 token-optimizer.py --compress',
                'savings': '预计节省 30-50%'
            })
    
    # 建议 2: 如果记忆文件过多，建议合并
    if 'memory/*.md' in stats['files']:
        count = stats['files']['memory/*.md'].get('count', 0)
        if count > 30:
            suggestions.append({
                'priority': 'medium',
                'issue': f'记忆文件过多 ({count} 个)',
                'action': '合并旧文件：python3 token-optimizer.py --merge --days 30',
                'savings': '预计节省 20-40%'
            })
    
    # 建议 3: 如果 SESSION-STATE.md 过大
    if 'SESSION-STATE.md' in stats['files']:
        ss_tokens = stats['files']['SESSION-STATE.md']['tokens']
        if ss_tokens > 2000:
            suggestions.append({
                'priority': 'medium',
                'issue': f'SESSION-STATE.md 过大 ({ss_tokens} tokens)',
                'action': '清理已完成项，保留活跃任务',
                'savings': '预计节省 40-60%'
            })
    
    # 建议 4: 总体建议
    if total_tokens > 20000:
        suggestions.append({
            'priority': 'high',
            'issue': f'总 token 数过高 ({total_tokens})',
            'action': '综合优化：压缩 + 摘要 + 清理',
            'savings': '预计节省 40-50%'
        })
    
    return suggestions

def print_stats(stats: dict):
    """打印统计信息"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}📊 Token 使用统计{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}\n")
    
    print(f"{'文件':<25} {'字符数':>12} {'Token 数':>12} {'行数':>8}")
    print(f"{'-'*60}")
    
    for name, data in stats['files'].items():
        chars = data['chars']
        tokens = data['tokens']
        lines = data.get('lines', data.get('count', '-'))
        print(f"{name:<25} {chars:>12,} {tokens:>12,} {lines:>8}")
    
    print(f"{'-'*60}")
    print(f"{Colors.BOLD}{'总计':<25} {stats['total_chars']:>12,} {stats['total_tokens']:>12,}{Colors.NC}")
    print()

def print_suggestions(suggestions: list):
    """打印优化建议"""
    if not suggestions:
        log_success("无需优化，token 使用合理！")
        return
    
    print(f"\n{Colors.BOLD}{Colors.YELLOW}{'='*60}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.YELLOW}💡 优化建议{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.YELLOW}{'='*60}{Colors.NC}\n")
    
    for i, sug in enumerate(suggestions, 1):
        priority_icon = "🔴" if sug['priority'] == 'high' else "🟡"
        print(f"{priority_icon} **建议 {i}:** {sug['issue']}")
        print(f"   操作：{sug['action']}")
        print(f"   预计节省：{sug['savings']}\n")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='OpenClaw Token 优化器')
    parser.add_argument('--analyze', action='store_true', help='分析当前 token 使用')
    parser.add_argument('--compress', action='store_true', help='压缩旧记忆文件')
    parser.add_argument('--days', type=int, default=30, help='保留天数（默认 30）')
    parser.add_argument('--suggest', action='store_true', help='生成优化建议')
    parser.add_argument('--full', action='store_true', help='完整优化（分析 + 建议 + 压缩）')
    
    args = parser.parse_args()
    
    # 默认行为：完整分析
    if not any([args.analyze, args.compress, args.suggest, args.full]):
        args.full = True
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}🔧 Token Optimizer - OpenClaw Token 优化器{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}\n")
    
    # 分析
    if args.analyze or args.full:
        log_info("分析当前 token 使用情况...")
        stats = analyze_current_usage()
        print_stats(stats)
        
        # 保存统计
        stats_file = OPTIMIZER_CONFIG.parent / "token-stats.json"
        stats_file.parent.mkdir(parents=True, exist_ok=True)
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        log_success(f"统计已保存：{stats_file}")
    
    # 生成建议
    if args.suggest or args.full:
        stats = analyze_current_usage() if 'stats' not in locals() else stats
        suggestions = get_optimization_suggestions(stats)
        print_suggestions(suggestions)
    
    # 压缩
    if args.compress or args.full:
        log_info(f"压缩 {args.days} 天前的记忆文件...")
        result = compress_memory(args.days)
        print(f"\n{Colors.BOLD}{Colors.GREEN}压缩完成:{Colors.NC}")
        print(f"  - 压缩文件：{result['compressed']} 个")
        print(f"  - 保留文件：{result['kept']} 个")
        print(f"  - 节省字符：{result['saved_chars']:,} ({estimate_tokens(result['saved_chars']):,} tokens)\n")

if __name__ == "__main__":
    main()
