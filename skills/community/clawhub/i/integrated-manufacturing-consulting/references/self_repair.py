#!/usr/bin/env python3
"""
S13 技能自修复引擎 — 每次PPT生成后自动分析问题、更新SKILL.md
版本: v6 consulting-report-generator
"""

import os
import re
import json
from datetime import datetime

SKILL_BASE = os.path.expanduser("~/.workbuddy/skills/consulting-report-generator")
SKILL_MD = os.path.join(SKILL_BASE, "SKILL.md")
EVOLUTION_DIR = os.path.join(SKILL_BASE, "self_evolution")
ERROR_LOG = os.path.join(EVOLUTION_DIR, "error_log.json")
IMPROVEMENTS_LOG = os.path.join(EVOLUTION_DIR, "improvements.json")
SUMMARY_FILE = os.path.join(EVOLUTION_DIR, "evolution_summary.md")


def load_json(path):
    """加载JSON文件"""
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path, data):
    """保存JSON文件"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_skill_md():
    """加载SKILL.md全文"""
    if not os.path.exists(SKILL_MD):
        return ""
    with open(SKILL_MD, 'r', encoding='utf-8') as f:
        return f.read()


def save_skill_md(content):
    """保存SKILL.md"""
    with open(SKILL_MD, 'w', encoding='utf-8') as f:
        f.write(content)


# =====================================================
# 问题收集
# =====================================================

def collect_issues_from_log():
    """从error_log.json收集未修复的问题"""
    errors = load_json(ERROR_LOG)
    pending = [e for e in errors if not e.get("fixed", False)]
    return pending


def collect_issues_from_run(run_errors, user_feedback=""):
    """从运行过程中收集问题"""
    issues = {
        "errors": [],
        "warnings": [],
        "user_feedback": [],
        "improvements": [],
    }
    
    # 运行时异常
    for err in run_errors:
        issues["errors"].append(err)
    
    # 用户反馈关键词提取
    if user_feedback:
        feedback_keywords = {
            "打不开": "文件损坏需修复",
            "修复": "文件兼容性问题",
            "方块": "中文显示异常",
            "乱码": "文字编码问题",
            "重叠": "文字重叠",
            "空白": "内容未显示",
            "风格": "模板风格问题",
            "颜色": "配色问题",
            "太短": "内容不够详细",
            "太简单": "内容深度不足",
            "数据不对": "数据准确性",
        }
        for kw, desc in feedback_keywords.items():
            if kw in user_feedback:
                issues["user_feedback"].append({"keyword": kw, "description": desc})
    
    return issues


# =====================================================
# 问题分级
# =====================================================

def classify_issue(issue):
    """对问题分级: P0致命/P1严重/P2一般/P3优化"""
    p0_keywords = ["打不开", "崩溃", "损坏", "无法打开", "空指针", "crash"]
    p1_keywords = ["方块", "乱码", "重叠", "空白", "缺失", "显示异常"]
    p2_keywords = ["搜索不到", "数据不准确", "风格不对", "内容不全"]
    p3_keywords = ["可以更好", "优化", "建议", "美观"]
    
    desc = str(issue.get("description", "")).lower()
    
    for kw in p0_keywords:
        if kw in desc:
            return "P0"
    for kw in p1_keywords:
        if kw in desc:
            return "P1"
    for kw in p2_keywords:
        if kw in desc:
            return "P2"
    for kw in p3_keywords:
        if kw in desc:
            return "P3"
    return "P2"


# =====================================================
# SKILL.md 更新操作
# =====================================================

def is_error_already_documented(error_text):
    """检查错误是否已在SKILL.md的常见错误中出现"""
    content = load_skill_md()
    if not content:
        return False
    # 检查错误描述是否已在「常见错误与修复」章节中
    error_section = content.split("## 十二、常见错误与修复")[-1] if "## 十二、常见错误与修复" in content else ""
    if not error_section:
        return False
    # 用关键片段匹配
    keywords = error_text[:20]  # 取前20字
    return keywords in error_section


def append_error_to_skill_md(error_text, cause_text, fix_text, error_number=None):
    """向SKILL.md追加新的错误条目"""
    content = load_skill_md()
    if not content:
        return
    
    # 自动计算错误编号
    if error_number is None:
        error_pattern = re.findall(r'### 错误(\d+)', content)
        if error_pattern:
            error_number = max(int(n) for n in error_pattern) + 1
        else:
            error_number = 10  # 当前已有9个
    
    # 标签
    tag = "【v6 新增】" if error_number >= 8 else ""
    new_entry = f"""
### 错误{error_number}：{error_text} {tag}
**原因**：{cause_text}
**修复**：{fix_text}
"""
    
    # 追加到「常见错误与修复」章节末尾
    marker = "---\n\n## 十三、技能自进化系统"
    if marker in content:
        content = content.replace(marker, f"{new_entry}\n{marker}")
    else:
        # fallback: 文件末尾追加
        content += f"\n{new_entry}\n"
    
    save_skill_md(content)
    print(f"🛠️ 自修复完成：已在SKILL.md追加「错误{error_number}：{error_text}」")


def update_function_spec(func_name, new_spec):
    """更新助手函数的实现规范"""
    content = load_skill_md()
    if not content:
        return
    
    # 在「助手函数规范」表中更新
    table_pattern = re.compile(r'\| `' + re.escape(func_name) + r'`[^|]*\|')
    if table_pattern.search(content):
        # 找到函数名称在当前行的行
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if f"`{func_name}`" in line and line.strip().startswith("|"):
                # 更新用途描述
                parts = line.split('|')
                if len(parts) >= 3:
                    parts[2] = f" {new_spec} "
                    lines[i] = '|'.join(parts)
                    break
        save_skill_md('\n'.join(lines))
        print(f"🛠️ 自修复完成：已更新函数 `{func_name}()` 规范")


def append_checklist_item(item_text):
    """追加交付检查项"""
    content = load_skill_md()
    if not content:
        return
    
    marker = "- [ ] ✅ **【S13新增】** 技能自修复已执行"
    new_item = f"- [ ] ✅ **【S13新增】** {item_text}"
    
    if new_item in content:
        return  # 已存在
    
    if marker in content:
        content = content.replace(marker, f"{new_item}\n{marker}")
        save_skill_md(content)
        print(f"🛠️ 自修复完成：已追加检查项「{item_text}」")


# =====================================================
# 版本号管理
# =====================================================

def update_version_number():
    """更新小版本号"""
    content = load_skill_md()
    if not content:
        return
    
    # 匹配 v6.x 格式
    match = re.search(r'v(\d+)\.(\d+)', content)
    if match:
        major = match.group(1)
        minor = int(match.group(2)) + 1
        new_version = f"v{major}.{minor}"
        content = content.replace(f"v{major}.{match.group(2)}", new_version, 1)
        save_skill_md(content)
        print(f"🛠️ 版本号升级: {new_version}")
        return new_version
    return None


# =====================================================
# 进化日志输出
# =====================================================

def write_evolution_summary(issues, repair_count):
    """写入进化摘要"""
    os.makedirs(EVOLUTION_DIR, exist_ok=True)
    
    summary = f"""## S13 自修复报告 ({datetime.now().strftime('%Y-%m-%d %H:%M')})

### 问题概览
- 总问题数: {len(issues['errors'])}
- 已修复数: {repair_count}
- 用户反馈: {len(issues['user_feedback'])} 条

### 修复详情
"""
    
    for err in issues.get("errors", []):
        level = classify_issue(err)
        summary += f"- [{level}] {err.get('description','')}\n"
        if err.get("fix"):
            summary += f"  → 修复: {err['fix']}\n"
    
    with open(SUMMARY_FILE, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"📝 进化摘要已更新: {SUMMARY_FILE}")


# =====================================================
# 主入口
# =====================================================

def self_repair(run_errors=None, user_feedback=""):
    """
    S13 技能自修复主函数
    
    参数:
        run_errors: 本次运行的错误列表 [{"description":"...", "root_cause":"...", "fix":"...", "level":"P0"}, ...]
        user_feedback: 用户反馈文本
    
    返回:
        repair_count: 本次修复的问题数量
    """
    print("=" * 50)
    print("🔄 S13 技能自修复引擎启动")
    print("=" * 50)
    
    if run_errors is None:
        run_errors = []
    
    # 1. 收集问题
    issues = collect_issues_from_run(run_errors, user_feedback)
    log_issues = collect_issues_from_log()
    issues["errors"].extend(log_issues)
    
    print(f"📋 收集到 {len(issues['errors'])} 个错误, {len(issues['user_feedback'])} 条反馈")
    
    # 2. 分级并修复
    repair_count = 0
    for issue in issues["errors"]:
        level = classify_issue(issue)
        issue["level"] = level
        
        if level in ("P0", "P1") and not is_error_already_documented(issue.get("description", "")):
            append_error_to_skill_md(
                error_text=issue.get("description", ""),
                cause_text=issue.get("root_cause", "待分析"),
                fix_text=issue.get("fix", "待确定")
            )
            
            # 如果有配套的函数更新
            if issue.get("function_to_update"):
                update_function_spec(issue["function_to_update"], issue.get("new_spec", ""))
            
            # 如果有配套的检查项
            if issue.get("new_checklist_item"):
                append_checklist_item(issue["new_checklist_item"])
            
            # 标记为已修复
            issue["fixed"] = True
            repair_count += 1
    
    # 3. 更新错误日志
    save_json(ERROR_LOG, issues["errors"])
    
    # 4. 写入进化摘要
    write_evolution_summary(issues, repair_count)
    
    # 5. 如果有P0修复，升级小版本
    if any(i.get("level") == "P0" for i in issues["errors"]):
        update_version_number()
    
    # 6. 输出报告
    print(f"\n{'=' * 50}")
    print(f"✅ S13 自修复完成 | 修复: {repair_count} 项 | 累计: 查看 evolution_summary.md")
    print(f"{'=' * 50}")
    
    return repair_count


# =====================================================
# 使用示例
# =====================================================
if __name__ == "__main__":
    # 模拟：本次运行遇到的错误
    example_errors = [
        {
            "description": "PPT生成后PowerPoint打开提示'需要修复'",
            "root_cause": "full_cleanup()使用replace字符串替换而非正则移除p:style完整节点",
            "fix": "改用re.sub彻底移除<p:style>...</p:style>完整节点，清理空<a:ln/>，移除a:themeShadow",
            "function_to_update": "full_cleanup",
            "new_spec": "深度XML净化（正则移除p:style+空ln+themeShadow，补齐typeface）",
            "new_checklist_item": "执行 full_cleanup()（正则完整移除p:style+空ln+themeShadow）",
        }
    ]
    
    # 用户反馈
    user_feedback = "文件打不开，PowerPoint提示需要修复"
    
    # 执行自修复
    self_repair(example_errors, user_feedback)
