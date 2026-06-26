#!/usr/bin/env env python3
"""
🦞 Lobster Doctor v2.1 — 龙虾 workspace 健康管家

诊断 + 治疗 + 预防：解决 OpenClaw 长期使用后的文件膨胀问题。

命令：
  session      会话健康检查（检测历史 token 大小）
  check        体检：扫描 workspace 健康状况（含0使用/重复技能检测）
  cleanup      治疗：安全自动清理（清理前自动备份）
  cron-audit   巡检：检测 cron 僵尸任务
  stats        统计：workspace 文件分布概览
  weekly       周报：生成健康报告并推送
"""

import json
import os
import hashlib
import sys
import re
from pathlib import Path
from datetime import datetime, timedelta

# ==================== 路径配置 ====================
WORKSPACE = Path.home() / ".openclaw" / "workspace"
OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"
CRON_JOBS = Path.home() / ".openclaw" / "cron" / "jobs.json"
BACKUP_DIR = WORKSPACE / ".cleanup-backup"
WEEKLY_REPORTS_DIR = WORKSPACE / "memory" / "weekly-reports"

# 会话健康阈值
SESSION_WARN_THRESHOLD = 100_000   # 100K tokens 告警
SESSION_DANGER_THRESHOLD = 200_000 # 200K tokens 强烈告警

# 核心文件白名单（永不删除）
CORE_FILES = {
    "AGENTS.md", "SOUL.md", "USER.md", "MEMORY.md", "TOOLS.md",
    "HEARTBEAT.md", "IDENTITY.md", "PROGRESS.md", "INTEL-DIRECTIVE.md",
    "BOOTSTRAP.md", "KB-SYNC-GUIDE.md", "package.json", "package-lock.json",
    ".env", ".openclaw", ".git", ".gitignore",
    ".model_override", ".openclaw-model-override",
}

# 受保护目录（不扫描不清理）
PROTECTED_DIRS = {"skills", "node_modules", ".git", "memory-tree", "memory"}

# 清理规则
STALE_DAYS_PY_JS_HTML = 3     # .py/.js/.html 超过N天未修改视为废弃
STALE_DAYS_MD = 7             # 根目录非核心 .md 超过N天未修改需要确认
MEMORY_LOG_MAX_DAYS = 30      # memory/ 日志保留天数
LARGE_FILE_THRESHOLD = 1 * 1024 * 1024  # 1MB


def load_json(path, default=None):
    if path.exists():
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return default or {}
    return default or {}


def file_hash(path):
    """计算文件内容 MD5"""
    try:
        with open(path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except (IOError, OSError):
        return None


def file_age_days(path):
    """文件最后修改距今天数"""
    try:
        mtime = datetime.fromtimestamp(path.stat().st_mtime)
        return (datetime.now() - mtime).days
    except OSError:
        return 0


def estimate_tokens(text):
    """粗略估算 token 数（字符/4）"""
    return len(text) // 4


def fmt_size(size_bytes):
    """格式化文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes/1024:.1f}KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes/1024/1024:.1f}MB"
    else:
        return f"{size_bytes/1024/1024/1024:.1f}GB"


def fmt_tokens(num):
    """格式化 token 数量"""
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.0f}K"
    else:
        return str(num)


# ==================== 会话健康监控 (v2.0 新增) ====================

def get_all_sessions():
    """获取所有会话的历史文件"""
    agents_dir = Path.home() / ".openclaw" / "agents"
    if not agents_dir.exists():
        return []
    
    sessions = []
    for agent_dir in agents_dir.iterdir():
        if not agent_dir.is_dir():
            continue
        sessions_dir = agent_dir / "sessions"
        if not sessions_dir.exists():
            continue
        
        for f in sessions_dir.glob("*.jsonl"):
            # 跳过备份/删除的文件
            if ".reset." in f.name or ".deleted." in f.name:
                continue
            try:
                size = f.stat().st_size
                # 统计轮次
                with open(f, 'r', encoding='utf-8') as sf:
                    turns = sum(1 for line in sf if '"type":"message"' in line)
                sessions.append({
                    'agent': agent_dir.name,
                    'id': f.stem,
                    'path': f,
                    'size': size,
                    'tokens': size // 4,
                    'turns': turns,
                    'mtime': datetime.fromtimestamp(f.stat().st_mtime),
                })
            except Exception:
                pass
    
    return sessions


def cmd_session():
    """会话健康检查命令"""
    print(f"🦞 龙虾医生 — 会话健康监控 ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n")
    
    sessions = get_all_sessions()
    if not sessions:
        print("📭 未找到活跃会话")
        return []
    
    # 按 token 排序
    sessions.sort(key=lambda x: -x['tokens'])
    
    warnings = []
    total_tokens = sum(s['tokens'] for s in sessions)
    
    print(f"📊 会话总览:")
    print(f"   活跃会话: {len(sessions)} 个")
    print(f"   历史总量: ~{fmt_tokens(total_tokens)} tokens\n")
    
    # 分类统计
    danger = [s for s in sessions if s['tokens'] > SESSION_DANGER_THRESHOLD]
    warn = [s for s in sessions if SESSION_WARN_THRESHOLD < s['tokens'] <= SESSION_DANGER_THRESHOLD]
    ok = [s for s in sessions if s['tokens'] <= SESSION_WARN_THRESHOLD]
    
    if danger:
        print(f"🔴 危险会话 (>{fmt_tokens(SESSION_DANGER_THRESHOLD)} tokens): {len(danger)} 个")
        for s in danger[:10]:
            short_id = s['id'][:8]
            print(f"   🚨 {short_id}... ({s['agent']}): ~{fmt_tokens(s['tokens'])} tokens, {s['turns']} 轮")
            warnings.append({
                'level': 'danger',
                'id': s['id'],
                'agent': s['agent'],
                'tokens': s['tokens'],
                'turns': s['turns'],
            })
        if len(danger) > 10:
            print(f"   ... 还有 {len(danger) - 10} 个")
        print()
    
    if warn:
        print(f"🟡 警告会话 (>{fmt_tokens(SESSION_WARN_THRESHOLD)} tokens): {len(warn)} 个")
        for s in warn[:10]:
            short_id = s['id'][:8]
            print(f"   ⚠️  {short_id}... ({s['agent']}): ~{fmt_tokens(s['tokens'])} tokens, {s['turns']} 轮")
            warnings.append({
                'level': 'warn',
                'id': s['id'],
                'agent': s['agent'],
                'tokens': s['tokens'],
                'turns': s['turns'],
            })
        if len(warn) > 10:
            print(f"   ... 还有 {len(warn) - 10} 个")
        print()
    
    print(f"🟢 健康会话 (<{fmt_tokens(SESSION_WARN_THRESHOLD)} tokens): {len(ok)} 个\n")
    
    # 建议
    if danger or warn:
        print("=" * 50)
        print("💡 建议操作:")
        if danger:
            print(f"\n   🚨 危险会话请立即处理:")
            print(f"      /compress  — 压缩记忆，大事记住小事忘掉")
            print(f"      /new       — 开新会话，清空历史轻装上阵")
        if warn:
            print(f"\n   ⚠️  警告会话可考虑压缩:")
            print(f"      /compress  — 减少历史大小")
        print()
        print(f"   会话 ID 可用于定位:")
        for s in (danger + warn)[:3]:
            print(f"      {s['id'][:16]}... → {s['agent']}")
    
    return warnings


# ==================== 渠道检测与推送 (v2.0 新增) ====================

def detect_enabled_channels():
    """从 openclaw.json 检测已启用的推送渠道"""
    config = load_json(OPENCLAW_CONFIG)
    channels = config.get('channels', {})
    
    enabled = []
    for name, cfg in channels.items():
        if cfg.get('enabled', False):
            enabled.append({
                'name': name,
                'config': cfg,
            })
    
    return enabled


def get_feishu_chat_id(config):
    """从飞书配置获取默认 chatId"""
    group_allow = config.get('groupAllowFrom', [])
    if group_allow:
        return group_allow[0]
    return None


def send_to_feishu(chat_id, message_text, title=""):
    """发送消息到飞书"""
    try:
        # 使用 feishu_doc 的 webhook 或 API
        # 这里用 subprocess 调用 openclaw CLI
        import subprocess
        
        # 构建 JSON 消息
        content = json.dumps({
            "zh_cn": {
                "title": title or "🦞 龙虾医生周报",
                "content": [[{"tag": "text", "text": message_text[:30000]}]]  # 飞书限制
            }
        }, ensure_ascii=False)
        
        # 使用 curl 调用飞书 webhook（如果配置了）
        # 或者使用 feishu tool
        # 这里先返回 False，让调用者知道需要其他方式
        return False
    except Exception as e:
        print(f"   飞书推送失败: {e}")
        return False


def cmd_weekly():
    """周报生成命令"""
    print(f"🦞 龙虾医生 — 周报生成 ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n")
    
    # 确保输出目录存在
    WEEKLY_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    report_date = datetime.now().strftime('%Y-%m-%d')
    report_file = WEEKLY_REPORTS_DIR / f"weekly-{report_date}.md"
    
    # 收集数据
    print("📊 收集健康数据...")
    
    # 1. 会话健康统计
    sessions = get_all_sessions()
    total_session_tokens = sum(s['tokens'] for s in sessions)
    danger_sessions = [s for s in sessions if s['tokens'] > SESSION_DANGER_THRESHOLD]
    warn_sessions = [s for s in sessions if SESSION_WARN_THRESHOLD < s['tokens'] <= SESSION_DANGER_THRESHOLD]
    
    # 2. 技能扫描
    skill_stats = scan_skills_for_weekly()
    
    # 3. Workspace 大小
    workspace_size = get_workspace_size()
    
    # 4. Cron 任务
    cron_data = load_json(CRON_JOBS)
    cron_count = len(cron_data) if isinstance(cron_data, list) else len(cron_data.get("jobs", []))
    
    # 生成报告
    report_lines = [
        f"# 🦞 龙虾医生周报",
        f"",
        f"**报告日期**: {report_date}",
        f"",
        f"---",
        f"",
        f"## 📊 会话健康",
        f"",
        f"| 指标 | 数值 |",
        f"|------|------|",
        f"| 活跃会话 | {len(sessions)} 个 |",
        f"| 历史总量 | ~{fmt_tokens(total_session_tokens)} tokens |",
        f"| 危险会话 (>200K) | {len(danger_sessions)} 个 |",
        f"| 警告会话 (>100K) | {len(warn_sessions)} 个 |",
        f"",
    ]
    
    if danger_sessions:
        report_lines.append("### 🚨 需要立即处理")
        report_lines.append("")
        for s in danger_sessions[:5]:
            report_lines.append(f"- `{s['id'][:8]}...` ({s['agent']}): ~{fmt_tokens(s['tokens'])} tokens, {s['turns']} 轮")
        report_lines.append("")
    
    report_lines.extend([
        f"## 🧩 技能状态",
        f"",
        f"| 指标 | 数值 |",
        f"|------|------|",
        f"| 已安装技能 | {skill_stats['total']} 个 |",
        f"| Description 总量 | ~{fmt_tokens(skill_stats['desc_tokens'])} tokens |",
        f"| 高占用低使用 | {len(skill_stats['low_use'])} 个 |",
        f"",
    ])
    
    if skill_stats['low_use']:
        report_lines.append("### 🔴 高占用低使用技能（建议卸载）")
        report_lines.append("")
        report_lines.append("| 技能 | 占用 | 调用 |")
        report_lines.append("|------|------|------|")
        for s in skill_stats['low_use'][:10]:
            report_lines.append(f"| {s['name']} | {fmt_tokens(s['tokens'])} tokens | {s['calls']} 次 |")
        report_lines.append("")
        
        # 计算可节省
        savings = sum(s['tokens'] for s in skill_stats['low_use'])
        report_lines.append(f"💡 卸载可节省: ~{fmt_tokens(savings)} tokens/轮")
        report_lines.append("")
    
    report_lines.extend([
        f"## 💾 Workspace",
        f"",
        f"| 指标 | 数值 |",
        f"|------|------|",
        f"| 总大小 | {fmt_size(workspace_size)} |",
        f"| Cron 任务 | {cron_count} 个 |",
        f"",
        f"---",
        f"",
        f"*由龙虾医生自动生成*",
    ])
    
    report_content = "\n".join(report_lines)
    
    # 写入本地文件
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"✅ 周报已保存: {report_file}\n")
    
    # 检测推送渠道
    channels = detect_enabled_channels()
    
    if channels:
        print(f"📡 检测到已启用渠道: {', '.join(c['name'] for c in channels)}")
        
        for ch in channels:
            if ch['name'] == 'feishu':
                chat_id = get_feishu_chat_id(ch['config'])
                if chat_id:
                    print(f"\n📱 飞书推送配置:")
                    print(f"   chat_id: {chat_id}")
                    print(f"\n💡 使用 OpenClaw 飞书工具发送周报:")
                    print(f"   message send --target {chat_id} --file {report_file}")
    else:
        print("📭 未检测到已启用的外部推送渠道")
        print("   周报已保存到本地，可手动查看或配置推送渠道")
    
    # 输出到终端
    print(f"\n{'='*50}")
    print(report_content)
    
    return report_file


def scan_skills_for_weekly():
    """扫描技能用于周报"""
    skills_dir = WORKSPACE / "skills"
    sys_skills_dir = Path.home() / ".npm-global" / "lib" / "node_modules" / "openclaw" / "skills"
    
    total = 0
    desc_tokens = 0
    low_use = []
    
    # 扫描本地技能
    all_skill_dirs = []
    if skills_dir.exists():
        all_skill_dirs.extend(skills_dir.iterdir())
    if sys_skills_dir.exists():
        all_skill_dirs.extend(sys_skills_dir.iterdir())
    
    seen = set()
    for skill_path in all_skill_dirs:
        if not skill_path.is_dir() or skill_path.name in seen:
            continue
        seen.add(skill_path.name)
        
        skill_md = skill_path / "SKILL.md"
        if not skill_md.exists():
            continue
        
        total += 1
        
        try:
            content = skill_md.read_text(encoding='utf-8')
            # 提取 description
            fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
            if fm_match:
                fm = fm_match.group(1)
                desc_match = re.search(r'^description:\s*(.+?)(?=\n^[a-z]|\n---|\Z)', fm, re.MULTILINE | re.DOTALL)
                if desc_match:
                    desc = desc_match.group(1)
                    desc = re.sub(r'^\s*>\s*', '', desc, flags=re.MULTILINE).strip()
                    tokens = estimate_tokens(desc)
                    desc_tokens += tokens
                    
                    # 检测是否高占用低使用（通过文件大小估算占用）
                    skill_size = sum(f.stat().st_size for f in skill_path.rglob('*') if f.is_file())
                    
                    # 简单判断：超过 50KB 且 description > 200 tokens
                    if skill_size > 50_000 and tokens > 200:
                        low_use.append({
                            'name': skill_path.name,
                            'tokens': tokens,
                            'calls': 0,  # 无法直接获取调用次数
                            'size': skill_size,
                        })
        except Exception:
            pass
    
    return {
        'total': total,
        'desc_tokens': desc_tokens,
        'low_use': low_use,
    }


def get_workspace_size():
    """获取 workspace 总大小"""
    total = 0
    for f in WORKSPACE.rglob('*'):
        if f.is_file():
            try:
                total += f.stat().st_size
            except:
                pass
    return total


# ==================== 技能分析 ====================

# 重复技能映射表（功能重叠的技能组）
DUPLICATE_SKILL_GROUPS = [
    {
        "category": "搜索类",
        "skills": ["tavily-search", "web-search", "multi-search-engine", "mx_search"],
        "description": "网络搜索功能重叠"
    },
    {
        "category": "编码类",
        "skills": ["coding-agent", "coding"],
        "description": "代码生成/AI编程重叠"
    },
    {
        "category": "文件处理类",
        "skills": ["file-converter", "pdf"],
        "description": "文件格式转换重叠"
    },
]

def scan_zero_usage_skills():
    """扫描0使用技能"""
    skills_dir = WORKSPACE / "skills"
    sys_skills_dir = Path.home() / ".npm-global" / "lib" / "node_modules" / "openclaw" / "skills"
    
    zero_usage = []
    low_match = []  # 场景匹配度低
    seen = set()
    
    # 收集所有技能
    all_skill_paths = []
    if skills_dir.exists():
        all_skill_paths.extend(skills_dir.iterdir())
    if sys_skills_dir.exists():
        all_skill_paths.extend(sys_skills_dir.iterdir())
    
    for skill_path in all_skill_paths:
        if not skill_path.is_dir() or skill_path.name in seen:
            continue
        seen.add(skill_path.name)
        
        skill_md = skill_path / "SKILL.md"
        meta_json = skill_path / "_meta.json"
        
        if not skill_md.exists():
            continue
        
        # 读取描述
        description = ""
        try:
            content = skill_md.read_text(encoding='utf-8')
            fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
            if fm_match:
                fm = fm_match.group(1)
                desc_match = re.search(r'^description:\s*(.+?)(?=\n^[a-z]|\n---|\Z)', fm, re.MULTILINE | re.DOTALL)
                if desc_match:
                    description = desc_match.group(1)
                    description = re.sub(r'^\s*>\s*', '', description, flags=re.MULTILINE).strip()
        except Exception:
            pass
        
        # 检查 _meta.json 是否有 uses 字段
        has_uses = False
        uses_count = 0
        if meta_json.exists():
            try:
                meta = load_json(meta_json)
                if 'uses' in meta and meta['uses'] > 0:
                    has_uses = True
                    uses_count = meta['uses']
            except Exception:
                pass
        
        # 计算技能大小
        skill_size = sum(f.stat().st_size for f in skill_path.rglob('*') if f.is_file() and not f.name.startswith('.'))
        
        # 判断场景匹配度（基于描述关键词）
        high_match_keywords = ['openclaw', 'workspace', 'agent', 'assistant', '每天', '日常', '工作流', '自动化']
        medium_match_keywords = ['搜索', 'search', '查找', 'git', 'github', '文件', 'file', '笔记', 'note']
        
        match_level = "低"
        if any(kw in description.lower() for kw in high_match_keywords):
            match_level = "高"
        elif any(kw in description.lower() for kw in medium_match_keywords):
            match_level = "中"
        
        skill_info = {
            'name': skill_path.name,
            'description': description[:100] + "..." if len(description) > 100 else description,
            'size': skill_size,
            'has_uses': has_uses,
            'uses_count': uses_count,
            'match_level': match_level,
            'path': skill_path,
        }
        
        # 如果没有使用记录且场景匹配度低，标记为潜在0使用
        if not has_uses and match_level == "低":
            zero_usage.append(skill_info)
        elif match_level == "低":
            low_match.append(skill_info)
    
    return zero_usage, low_match


def scan_duplicate_skills():
    """扫描重复技能"""
    skills_dir = WORKSPACE / "skills"
    sys_skills_dir = Path.home() / ".npm-global" / "lib" / "node_modules" / "openclaw" / "skills"
    
    installed_skills = set()
    if skills_dir.exists():
        installed_skills.update(d.name for d in skills_dir.iterdir() if d.is_dir())
    if sys_skills_dir.exists():
        installed_skills.update(d.name for d in sys_skills_dir.iterdir() if d.is_dir())
    
    duplicates = []
    
    for group in DUPLICATE_SKILL_GROUPS:
        category_skills = []
        for skill_name in group["skills"]:
            if skill_name in installed_skills:
                category_skills.append(skill_name)
        
        # 只有当同一类别有多个技能时才报告重复
        if len(category_skills) > 1:
            duplicates.append({
                'category': group["category"],
                'description': group["description"],
                'skills': category_skills,
            })
    
    return duplicates


# ==================== 体检 ====================

def cmd_check():
    print(f"🦞 龙虾医生 — 体检报告 ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n")

    issues = []
    total_files = 0
    total_size = 0

    # 1. 根目录扫描
    root_files = [f for f in WORKSPACE.iterdir() if f.is_file() and not f.name.startswith('.')]
    non_core = [f for f in root_files if f.name not in CORE_FILES]
    total_files += len(list(WORKSPACE.rglob('*')))

    print(f"📁 根目录: {len(root_files)} 个文件, {len(non_core)} 个非核心文件")
    if non_core:
        print(f"   非核心文件:")
        for f in sorted(non_core):
            age = file_age_days(f)
            size = fmt_size(f.stat().st_size)
            marker = "⚠️" if age > 7 else "  "
            print(f"   {marker} {f.name:40s} {size:>8s}  {age}天前修改")
            if age > 7:
                issues.append(f"根目录过期文件: {f.name} ({age}天)")
    print()

    # 2. 废弃文件检测
    stale_extensions = {'.py', '.js', '.html', '.txt', '.log'}
    stale_files = []
    for f in WORKSPACE.rglob('*'):
        if not f.is_file():
            continue
        # 跳过受保护目录
        if any(part in PROTECTED_DIRS for part in f.relative_to(WORKSPACE).parts):
            continue
        if f.suffix in stale_extensions:
            age = file_age_days(f)
            if age > STALE_DAYS_PY_JS_HTML:
                stale_files.append((f, age))
    total_size_stale = sum(f.stat().st_size for f, _ in stale_files)
    print(f"🗑️ 废弃文件 (>{STALE_DAYS_PY_JS_HTML}天): {len(stale_files)} 个, 共 {fmt_size(total_size_stale)}")
    for f, age in sorted(stale_files, key=lambda x: x[1], reverse=True)[:10]:
        rel = f.relative_to(WORKSPACE)
        print(f"   {age:3d}天  {str(rel)}")
    if len(stale_files) > 10:
        print(f"   ... 还有 {len(stale_files)-10} 个")
    if stale_files:
        issues.append(f"发现 {len(stale_files)} 个废弃文件")
    print()

    # 3. 重复文件检测
    hash_map = {}
    duplicates = []
    for f in WORKSPACE.rglob('*'):
        if not f.is_file() or f.stat().st_size == 0:
            continue
        if any(part in PROTECTED_DIRS for part in f.parts):
            continue
        h = file_hash(f)
        if h:
            if h in hash_map:
                duplicates.append((hash_map[h], f))
            else:
                hash_map[h] = f
    print(f"📋 重复文件: {len(duplicates)} 对")
    for orig, dup in sorted(duplicates, key=lambda x: str(x[0]))[:10]:
        print(f"   {orig.relative_to(WORKSPACE)}")
        print(f"   ↳ 重复: {dup.relative_to(WORKSPACE)}")
    if duplicates:
        issues.append(f"发现 {len(duplicates)} 对重复文件")
    print()

    # 4. 空目录检测
    empty_dirs = []
    for d in WORKSPACE.rglob('*'):
        if not d.is_dir():
            continue
        if any(part in PROTECTED_DIRS for part in d.parts):
            continue
        try:
            if not any(d.iterdir()):
                empty_dirs.append(d)
        except PermissionError:
            pass
    print(f"📂 空目录: {len(empty_dirs)} 个")
    for d in empty_dirs[:10]:
        print(f"   {d.relative_to(WORKSPACE)}")
    if empty_dirs:
        issues.append(f"发现 {len(empty_dirs)} 个空目录")
    print()

    # 5. 大文件检测
    large_files = []
    for f in WORKSPACE.rglob('*'):
        if not f.is_file():
            continue
        if any(part in PROTECTED_DIRS for part in f.parts):
            continue
        try:
            size = f.stat().st_size
            if size > LARGE_FILE_THRESHOLD:
                large_files.append((f, size))
        except OSError:
            pass
    large_files.sort(key=lambda x: x[1], reverse=True)
    print(f"📦 大文件 (>{fmt_size(LARGE_FILE_THRESHOLD)}): {len(large_files)} 个")
    total_large = sum(s for _, s in large_files)
    for f, size in large_files[:5]:
        print(f"   {fmt_size(size):>8s}  {f.relative_to(WORKSPACE)}")
    if len(large_files) > 5:
        print(f"   ... 还有 {len(large_files)-5} 个, 共 {fmt_size(total_large)}")
    if large_files:
        issues.append(f"发现 {len(large_files)} 个大文件, 共 {fmt_size(total_large)}")
    print()

    # 6. Bootstrap Context Token 估算
    bootstrap_files = [WORKSPACE / name for name in CORE_FILES if (WORKSPACE / name).is_file()]
    bootstrap_chars = 0
    for f in bootstrap_files:
        try:
            bootstrap_chars += len(f.read_text(encoding='utf-8'))
        except:
            pass
    bootstrap_tokens = estimate_tokens(str(bootstrap_chars))
    print(f"🧠 Bootstrap Context: ~{bootstrap_tokens:,} tokens ({bootstrap_chars:,} 字符)")
    if bootstrap_tokens > 8000:
        issues.append(f"Bootstrap context 过大: ~{bootstrap_tokens} tokens (建议 <8000)")
        print(f"   ⚠️ 偏大，建议精简 workspace 文件以节省 token")
    else:
        print(f"   ✅ 健康范围")
    print()

    # 7. Cron 僵尸检测
    cron_data = load_json(CRON_JOBS)
    if isinstance(cron_data, list):
        jobs = cron_data
    elif isinstance(cron_data, dict):
        jobs = cron_data.get("jobs", [])
    else:
        jobs = []
    cron_issues = 0
    if jobs:
        print(f"⏰ Cron 任务: {len(jobs)} 个")
        for job in jobs:
            name = job.get("name", "?")
            enabled = job.get("enabled", True)
            state = job.get("state", {})
            if not enabled:
                cron_issues += 1
                print(f"   ❌ 已禁用: {name}")
            elif any(kw in name.lower() for kw in ["test", "debug", "tmp", "temp"]):
                cron_issues += 1
                print(f"   ⚠️ 疑似临时: {name}")
            else:
                print(f"   ✅ {name}")
        if cron_issues:
            issues.append(f"发现 {cron_issues} 个可疑 cron 任务")
    else:
        print(f"⏰ Cron 任务: 无")
    print()

    # 8. 记忆树状态（如果安装了）
    mt_script = WORKSPACE / "skills" / "memory-tree" / "scripts" / "memory_tree.py"
    if mt_script.exists():
        print("🌳 记忆树: 已安装")
        print(f"   运行 `lobster_doctor.py check` 后可执行:")
        print(f"   python3 skills/memory-tree/scripts/memory_tree.py visualize")
    else:
        print("🌳 记忆树: 未安装")
    print()
    
    # 9. 0使用技能扫描
    zero_usage, low_match = scan_zero_usage_skills()
    print(f"🕳️ 0使用技能扫描:")
    if zero_usage:
        print(f"   ⚠️ 潜在未使用技能 ({len(zero_usage)} 个):")
        for s in zero_usage[:10]:
            desc_short = s['description'][:50] + "..." if len(s['description']) > 50 else s['description']
            print(f"      {s['name']}: {desc_short}")
        if len(zero_usage) > 10:
            print(f"      ... 还有 {len(zero_usage) - 10} 个")
        issues.append(f"发现 {len(zero_usage)} 个潜在未使用技能")
    else:
        print(f"   ✅ 未发现明显未使用技能")
    if low_match:
        print(f"   💡 场景匹配度低的技能 ({len(low_match)} 个):")
        for s in low_match[:5]:
            print(f"      {s['name']}")
    print()
    
    # 10. 重复技能检测
    duplicates = scan_duplicate_skills()
    print(f"🔄 重复技能检测:")
    if duplicates:
        print(f"   ⚠️ 发现 {len(duplicates)} 类功能重叠:")
        for dup in duplicates:
            print(f"      [{dup['category']}] {', '.join(dup['skills'])}")
            print(f"         → {dup['description']}")
        dup_count = sum(len(d['skills']) for d in duplicates)
        issues.append(f"发现 {dup_count} 个重复技能，建议保留最常用的一个")
    else:
        print(f"   ✅ 未发现功能重叠的技能")
    print()
    
    # 11. Token 消耗诊断
    token_issues = diagnose_token_usage()
    issues.extend(token_issues)

    # 总结
    if issues:
        print(f"{'='*50}")
        print(f"🔍 发现 {len(issues)} 个问题:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        print()
        print(f"💡 运行 `lobster_doctor.py cleanup` 自动修复（清理前会备份）")
    else:
        print(f"{'='*50}")
        print(f"✅ workspace 健康状况良好！")


# ==================== 清理 ====================

def cmd_cleanup(dry_run=False):
    if dry_run:
        print(f"🦞 龙虾医生 — 模拟清理 ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n")
    else:
        print(f"🦞 龙虾医生 — 自动清理 ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n")

    # 创建备份目录
    today = datetime.now().strftime('%Y-%m-%d')
    backup = BACKUP_DIR / today
    if not dry_run:
        backup.mkdir(parents=True, exist_ok=True)

    deleted_files = 0
    deleted_dirs = 0
    skipped = []
    freed_bytes = 0

    # 1. 清理根目录废弃脚本
    stale_extensions = {'.py', '.js', '.html', '.txt', '.log', '.json'}
    for f in list(WORKSPACE.iterdir()):
        if not f.is_file() or f.name in CORE_FILES:
            continue
        if f.name.startswith('.'):
            continue
        if f.suffix in stale_extensions and file_age_days(f) > STALE_DAYS_PY_JS_HTML:
            size = f.stat().st_size
            rel = f.relative_to(WORKSPACE)
            if dry_run:
                print(f"  🗑️ [模拟] {rel} ({fmt_size(size)})")
            else:
                try:
                    f.rename(backup / f.name)
                    print(f"  🗑️ {rel} → 备份 ({fmt_size(size)})")
                except OSError as e:
                    skipped.append((rel, str(e)))
                    continue
            deleted_files += 1
            freed_bytes += size

    # 2. 清理 .tmp/.bak 文件
    for f in WORKSPACE.rglob('*'):
        if not f.is_file():
            continue
        if any(part in PROTECTED_DIRS for part in f.parts):
            continue
        if f.suffix in {'.tmp', '.bak', '.old', '.swp'}:
            size = f.stat().st_size
            rel = f.relative_to(WORKSPACE)
            if dry_run:
                print(f"  🗑️ [模拟] {rel} ({fmt_size(size)})")
            else:
                try:
                    dest = backup / f.name
                    if dest.exists():
                        dest = backup / f"{f.name}_{id(f)}"
                    f.rename(dest)
                    print(f"  🗑️ {rel} → 备份 ({fmt_size(size)})")
                except OSError as e:
                    skipped.append((rel, str(e)))
                    continue
            deleted_files += 1
            freed_bytes += size

    # 3. 清理空目录
    for d in list(WORKSPACE.rglob('*')):
        if not d.is_dir() or d == WORKSPACE:
            continue
        if any(part in PROTECTED_DIRS for part in d.parts):
            continue
        try:
            if not any(d.iterdir()):
                rel = d.relative_to(WORKSPACE)
                if dry_run:
                    print(f"  📂 [模拟] 空目录: {rel}")
                else:
                    d.rmdir()
                    print(f"  📂 空目录已删除: {rel}")
                deleted_dirs += 1
        except (OSError, PermissionError):
            pass

    # 4. 清理过期 memory 日志
    memory_dir = WORKSPACE / "memory"
    if memory_dir.exists():
        cutoff = datetime.now() - timedelta(days=MEMORY_LOG_MAX_DAYS)
        for f in memory_dir.glob('*.md'):
            if f.name == 'README.md' or f.name == 'heartbeat-state.json':
                continue
            try:
                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                if mtime < cutoff:
                    size = f.stat().st_size
                    rel = f.relative_to(WORKSPACE)
                    if dry_run:
                        print(f"  📝 [模拟] 过期日志: {rel} ({file_age_days(f)}天)")
                    else:
                        f.rename(backup / f.name)
                        print(f"  📝 过期日志已归档: {rel} ({file_age_days(f)}天, {fmt_size(size)})")
                    deleted_files += 1
                    freed_bytes += size
            except OSError:
                pass

    # 5. 清理重复文件
    hash_map = {}
    for f in WORKSPACE.rglob('*'):
        if not f.is_file() or f.stat().st_size == 0:
            continue
        if any(part in PROTECTED_DIRS for part in f.parts):
            continue
        h = file_hash(f)
        if h:
            if h in hash_map:
                orig, dup = hash_map[h], f
                size = dup.stat().st_size
                rel = dup.relative_to(WORKSPACE)
                if dry_run:
                    print(f"  📋 [模拟] 重复文件: {rel} (与 {orig.relative_to(WORKSPACE)} 相同)")
                else:
                    try:
                        dup.rename(backup / f"{dup.name}_{id(dup)}")
                        print(f"  📋 重复文件已移除: {rel}")
                    except OSError as e:
                        skipped.append((rel, str(e)))
                deleted_files += 1
                freed_bytes += size
            else:
                hash_map[h] = f

    # 总结
    print(f"\n{'='*50}")
    mode = "模拟" if dry_run else "实际"
    print(f"🧹 {mode}清理完成:")
    print(f"   📄 删除文件: {deleted_files}")
    print(f"   📂 删除空目录: {deleted_dirs}")
    print(f"   💾 释放空间: {fmt_size(freed_bytes)}")
    if skipped:
        print(f"   ⚠️ 跳过 {len(skipped)} 个:")
        for rel, reason in skipped:
            print(f"      {rel}: {reason}")
    if not dry_run and (deleted_files > 0 or deleted_dirs > 0):
        print(f"   📦 备份位置: {backup}")


# ==================== Cron 巡检 ====================

def cmd_cron_audit():
    print(f"🦞 龙虾医生 — Cron 巡检 ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n")

    cron_data = load_json(CRON_JOBS)
    if isinstance(cron_data, list):
        jobs = cron_data
    elif isinstance(cron_data, dict):
        jobs = cron_data.get("jobs", [])
    else:
        jobs = []

    if not jobs:
        print("📭 没有 cron 任务")
        return

    print(f"⏰ 共 {len(jobs)} 个 cron 任务\n")

    healthy = 0
    warnings = []

    for i, job in enumerate(jobs, 1):
        name = job.get("name", f"#{i}")
        enabled = job.get("enabled", True)
        schedule = job.get("schedule", {})
        expr = schedule.get("expr", "?")
        session = job.get("sessionTarget", "?")
        created = job.get("createdAtMs", 0)
        state = job.get("state", {})
        next_run = state.get("nextRunAtMs")

        # 状态图标
        if not enabled:
            status = "❌ 禁用"
            warnings.append(f"{name}: 已禁用，建议删除")
        elif any(kw in name.lower() for kw in ["test", "debug", "tmp", "temp", "old"]):
            status = "⚠️ 疑似临时"
            warnings.append(f"{name}: 名称含 test/debug/tmp，可能是临时任务")
        else:
            status = "✅ 正常"
            healthy += 1

        # 创建时间
        if created:
            created_date = datetime.fromtimestamp(created / 1000).strftime('%Y-%m-%d')
            age_days = (datetime.now() - datetime.fromtimestamp(created / 1000)).days
        else:
            created_date = "未知"
            age_days = 0

        print(f"  {status} {name}")
        print(f"      调度: {expr} | 目标: {session} | 创建: {created_date} ({age_days}天前)")
        if next_run:
            next_date = datetime.fromtimestamp(next_run / 1000).strftime('%Y-%m-%d %H:%M')
            print(f"      下次运行: {next_date}")
        print()

    # 检查运行历史
    runs_dir = Path.home() / ".openclaw" / "cron" / "runs"
    if runs_dir.exists():
        run_files = list(runs_dir.glob("*.jsonl"))
        print(f"📊 运行历史: {len(run_files)} 条记录")

    print(f"\n{'='*50}")
    print(f"  ✅ 健康: {healthy}  |  ⚠️ 警告: {len(warnings)}")
    if warnings:
        print(f"\n  建议操作:")
        for w in warnings:
            print(f"  • {w}")
        print(f"\n  删除命令: openclaw cron rm <job-id>")


# ==================== 统计 ====================

def cmd_stats():
    print(f"🦞 龙虾医生 — Workspace 统计 ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n")

    total_files = 0
    total_size = 0
    ext_stats = {}
    dir_stats = {}

    for f in WORKSPACE.rglob('*'):
        if not f.is_file():
            continue
        total_files += 1
        try:
            size = f.stat().st_size
            total_size += size
        except OSError:
            size = 0

        ext = f.suffix.lower() or '.无后缀'
        ext_stats[ext] = ext_stats.get(ext, {"count": 0, "size": 0})
        ext_stats[ext]["count"] += 1
        ext_stats[ext]["size"] += size

        # 目录统计
        parent = f.parent.name
        if parent not in dir_stats:
            dir_stats[parent] = {"count": 0, "size": 0}
        dir_stats[parent]["count"] += 1
        dir_stats[parent]["size"] += size

    print(f"📂 总计: {total_files} 个文件, {fmt_size(total_size)}\n")

    # 按后缀分类
    print("📊 按类型:")
    sorted_exts = sorted(ext_stats.items(), key=lambda x: x[1]["size"], reverse=True)
    for ext, data in sorted_exts[:15]:
        bar = "█" * min(20, data["size"] // (total_size // 20 + 1))
        print(f"  {ext:12s} {data['count']:4d}个 {fmt_size(data['size']):>8s} {bar}")
    print()

    # 按目录分类
    print("📁 按目录:")
    sorted_dirs = sorted(dir_stats.items(), key=lambda x: x[1]["size"], reverse=True)
    for name, data in sorted_dirs[:10]:
        if name in PROTECTED_DIRS:
            continue
        print(f"  {name:25s} {data['count']:4d}个 {fmt_size(data['size']):>8s}")
    print()

    # 技能统计
    skills_dir = WORKSPACE / "skills"
    if skills_dir.exists():
        skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
        print(f"🧩 已安装技能: {len(skill_dirs)} 个")
        for s in sorted(skill_dirs, key=lambda x: x.name)[:10]:
            sk_files = list(s.rglob('*'))
            sk_size = sum(f.stat().st_size for f in sk_files if f.is_file())
            print(f"  {s.name:30s} {len(sk_files):3d}个文件 {fmt_size(sk_size):>8s}")
        if len(skill_dirs) > 10:
            print(f"  ... 还有 {len(skill_dirs)-10} 个")
        print()

    # Memory 目录统计
    memory_dir = WORKSPACE / "memory"
    if memory_dir.exists():
        mem_files = list(memory_dir.glob('*.md'))
        mem_size = sum(f.stat().st_size for f in mem_files if f.is_file())
        print(f"📝 记忆日志: {len(mem_files)} 个, {fmt_size(mem_size)}")


# ==================== Token 消耗诊断 ====================

def get_session_history_size():
    """获取会话历史总大小"""
    sessions = get_all_sessions()
    total_size = sum(s['size'] for s in sessions)
    return total_size, sessions


def diagnose_token_usage():
    """诊断 Token 消耗情况"""
    print(f"\n{'='*50}")
    print(f"📊 Token 消耗诊断")
    print(f"{'='*50}\n")
    
    issues = []
    
    # 1. 会话历史
    session_size, sessions = get_session_history_size()
    session_tokens = session_size // 4  # 粗略估算
    print(f"💬 会话历史: {fmt_size(session_size)} (~{fmt_tokens(session_tokens)} tokens)")
    
    if sessions:
        print(f"   活跃会话:")
        for s in sorted(sessions, key=lambda x: -x['tokens'])[:5]:
            tokens = s['tokens']
            warn = "⚠️" if tokens > SESSION_WARN_THRESHOLD else "  "
            print(f"   {warn} {s['id'][:20]}: {s['turns']}轮, ~{fmt_tokens(tokens)} tokens")
            if tokens > SESSION_WARN_THRESHOLD:
                issues.append(f"会话 {s['id'][:16]}... 历史过大 (~{fmt_tokens(tokens)} tokens)")
    
    if session_tokens > 500000:
        print(f"\n   ⚠️ 会话历史过大！每次请求都在重复发送这些历史。")
        print(f"   建议：")
        print(f"     /compress  — 压缩记忆，大事记住小事忘掉")
        print(f"     /new       — 开新会话，清空历史轻装上阵")
    elif session_tokens > 100000:
        print(f"\n   💡 会话历史较长，可考虑 /compress 或 /new")
    
    # 2. MEMORY.md
    memory_file = WORKSPACE / "MEMORY.md"
    if memory_file.exists():
        memory_size = memory_file.stat().st_size
        memory_tokens = memory_size // 4
        print(f"\n📝 MEMORY.md: {fmt_size(memory_size)} (~{fmt_tokens(memory_tokens)} tokens)")
        if memory_tokens > 5000:
            print(f"   💡 可考虑归档旧内容到 memory/ 目录")
    
    # 3. 技能描述
    skills_dir = WORKSPACE / "skills"
    total_desc_chars = 0
    skill_count = 0
    if skills_dir.exists():
        for skill_path in skills_dir.iterdir():
            if not skill_path.is_dir():
                continue
            skill_md = skill_path / "SKILL.md"
            if skill_md.exists():
                try:
                    content = skill_md.read_text()
                    # 提取 description
                    fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
                    if fm_match:
                        fm = fm_match.group(1)
                        desc_match = re.search(r'^description:\s*(.+?)(?=\n^[a-z]|\n---|\Z)', fm, re.MULTILINE | re.DOTALL)
                        if desc_match:
                            desc = desc_match.group(1)
                            desc = re.sub(r'^\s*>\s*', '', desc, flags=re.MULTILINE).strip()
                            total_desc_chars += len(desc)
                            skill_count += 1
                except:
                    pass
    
    # 系统技能
    sys_skills_dir = Path.home() / ".npm-global" / "lib" / "node_modules" / "openclaw" / "skills"
    if sys_skills_dir.exists():
        for skill_path in sys_skills_dir.iterdir():
            if not skill_path.is_dir():
                continue
            skill_md = skill_path / "SKILL.md"
            if skill_md.exists():
                try:
                    content = skill_md.read_text()
                    fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
                    if fm_match:
                        fm = fm_match.group(1)
                        desc_match = re.search(r'^description:\s*(.+?)(?=\n^[a-z]|\n---|\Z)', fm, re.MULTILINE | re.DOTALL)
                        if desc_match:
                            desc = desc_match.group(1)
                            desc = re.sub(r'^\s*>\s*', '', desc, flags=re.MULTILINE).strip()
                            total_desc_chars += len(desc)
                            skill_count += 1
                except:
                    pass
    
    desc_tokens = total_desc_chars // 4
    print(f"\n🧩 技能描述: {skill_count} 个技能, ~{fmt_tokens(desc_tokens)} tokens")
    if desc_tokens > 5000:
        print(f"   💡 可运行 skill-slim report 查看优化空间")
    
    # 总结
    total_estimated = session_tokens + memory_tokens + desc_tokens
    print(f"\n{'='*50}")
    print(f"📈 每轮请求估算: ~{fmt_tokens(total_estimated)} tokens")
    
    if session_tokens > 500000:
        print(f"\n⚠️ 主要消耗: 会话历史 ({fmt_tokens(session_tokens)} tokens)")
        print(f"   立即行动: /compress 或 /new")
    elif total_estimated > 100000:
        print(f"\n💡 Token 消耗较高，建议优化")
    
    return issues


# ==================== Memory 归档 ====================

MEMORY_ARCHIVE_THRESHOLD = 3  # 超过N天的文件归档
MEMORY_KEEP_PREFIXES = ["decision-", "重要-", "key-"]  # 保留的文件名前缀
MEMORY_KEEP_MARKERS = ["<!-- KEEP -->", "# 重要决策", "# Key Decision"]  # 内容标记

def cmd_memory_archive(dry_run=True):
    """归档过期的 memory 文件"""
    memory_dir = WORKSPACE / "memory"
    archive_dir = memory_dir / "archive"
    
    if not memory_dir.exists():
        print("❌ memory 目录不存在")
        return
    
    print(f"🦞 龙虾医生 — Memory 归档 ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n")
    
    if dry_run:
        print("📋 [预览模式] 以下文件将被归档:\n")
    else:
        archive_dir.mkdir(parents=True, exist_ok=True)
        print("📦 正在归档...\n")
    
    # 收集所有 memory 文件
    md_files = list(memory_dir.glob("*.md"))
    
    # 计算阈值日期
    cutoff = datetime.now() - timedelta(days=MEMORY_ARCHIVE_THRESHOLD)
    
    to_archive = []
    to_keep = []
    total_tokens = 0
    saved_tokens = 0
    
    for f in md_files:
        if f.name == "README.md":
            to_keep.append((f, "README"))
            continue
        
        # 读取内容检查是否有重要关键词
        try:
            content = f.read_text(encoding='utf-8')
        except:
            content = ""
        
        tokens = estimate_tokens(content)
        total_tokens += tokens
        
        # 检查是否应该保留
        mtime = datetime.fromtimestamp(f.stat().st_mtime)
        is_old = mtime < cutoff
        has_marker = any(marker in content for marker in MEMORY_KEEP_MARKERS)
        has_prefix = any(f.name.startswith(prefix) for prefix in MEMORY_KEEP_PREFIXES)
        
        # 检查是否是今日文件
        today_str = datetime.now().strftime('%Y-%m-%d')
        yesterday_str = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        is_recent = f.name.startswith(today_str) or f.name.startswith(yesterday_str)
        
        if is_recent:
            to_keep.append((f, "最近2天"))
        elif has_marker and is_old:
            to_keep.append((f, "标记保留"))
        elif has_prefix and is_old:
            to_keep.append((f, "重要前缀"))
        elif is_old:
            to_archive.append((f, mtime, tokens))
            saved_tokens += tokens
        else:
            to_keep.append((f, f"{(datetime.now() - mtime).days}天前"))
    
    # 显示归档列表
    if to_archive:
        print(f"{'文件名':<45} {'修改时间':<12} {'Tokens':>8}")
        print("-" * 70)
        for f, mtime, tokens in sorted(to_archive, key=lambda x: x[1]):
            age = (datetime.now() - mtime).days
            print(f"  {f.name:<43} {age:>3}天前     ~{tokens:>6,}")
        
        print(f"\n  归档文件数: {len(to_archive)}")
        print(f"  节省 tokens: ~{saved_tokens:,}")
    else:
        print("✅ 没有需要归档的文件")
    
    # 显示保留列表
    if to_keep:
        print(f"\n📋 保留文件 ({len(to_keep)} 个):")
        for f, reason in sorted(to_keep, key=lambda x: x[0].name):
            print(f"  ✅ {f.name:<40} ({reason})")
    
    # 执行归档
    if not dry_run and to_archive:
        print(f"\n{'='*50}")
        for f, mtime, tokens in to_archive:
            try:
                dest = archive_dir / f.name
                if dest.exists():
                    dest = archive_dir / f"{f.stem}_{mtime.strftime('%Y%m%d')}.md"
                f.rename(dest)
                print(f"  📦 {f.name} → archive/")
            except OSError as e:
                print(f"  ❌ {f.name}: {e}")
        
        print(f"\n✅ 归档完成!")
        print(f"   归档位置: {archive_dir}")
        print(f"   节省 tokens: ~{saved_tokens:,}")
        print(f"\n💡 重启后生效: systemctl --user restart openclaw-gateway.service")
    elif dry_run and to_archive:
        print(f"\n{'='*50}")
        print(f"💡 运行 `lobster_doctor.py memory-archive --apply` 执行归档")


def main():
    if len(sys.argv) < 2:
        print("🦞 Lobster Doctor v2.0 — 龙虾 workspace 健康管家\n")
        print("命令:")
        print("  session            会话健康检查（检测历史 token 大小）")
        print("  weekly             周报生成（自动检测已启用渠道推送）")
        print("  check              体检：扫描 workspace 健康状况")
        print("  cleanup            治疗：安全自动清理（清理前自动备份）")
        print("  cleanup --dry-run  模拟清理（只报告不删除）")
        print("  cron-audit         巡检：检测 cron 僵尸任务")
        print("  stats              统计：workspace 文件分布概览")
        print("  skill-slim report  技能瘦身：token 消耗报告（不修改）")
        print("  skill-slim dry-run 技能瘦身：预览精简效果（不修改）")
        print("  skill-slim apply   技能瘦身：应用精简（自动备份）")
        print("  memory-archive     Memory归档：预览过期文件（不移动）")
        print("  memory-archive --apply  Memory归档：执行归档")
        print()
        print("建议: 每周运行一次 check，每月运行一次 cleanup")
        return

    cmd = sys.argv[1]
    if cmd == "session":
        cmd_session()
    elif cmd == "weekly":
        cmd_weekly()
    elif cmd == "check":
        cmd_check()
    elif cmd == "cleanup":
        dry_run = "--dry-run" in sys.argv
        cmd_cleanup(dry_run=dry_run)
    elif cmd == "cron-audit":
        cmd_cron_audit()
    elif cmd == "stats":
        cmd_stats()
    elif cmd == "skill-slim":
        # 委托给 skill_slim.py
        from skill_slim import main as skill_slim_main
        sys.argv = [sys.argv[0], *sys.argv[2:]]  # 去掉 skill-slim
        skill_slim_main()
    elif cmd == "memory-archive":
        apply = "--apply" in sys.argv
        cmd_memory_archive(dry_run=not apply)
    else:
        print(f"❌ 未知命令: {cmd}")
        print("运行 `lobster_doctor.py` 查看可用命令")


if __name__ == "__main__":
    main()