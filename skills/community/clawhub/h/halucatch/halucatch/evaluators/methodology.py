"""方法论评估：检查步骤粒度、循环/分支、错误处理等。"""

import os
import re
from ..config import MESSAGES
from .guardrails import _branch_density


def check_methodology(info):
    """纯方法论型 Skill 评估。"""
    md = info['skill_md']
    issues = []

    if not md:
        return {'rating': '🟡 无 SKILL.md', 'issues': [('🟡 未找到 SKILL.md', 'skip')], 'score': '-'}

    total = 5
    score = 0

    # 1) 步骤清晰
    if re.search(r'(步骤|Step|##\s+\d|第[一二三四五六七八九十\d]+步)', md):
        issues.append(('✅ 有结构化步骤', 'pass'))
        score += 1
    else:
        issues.append(('🟠 缺少结构化步骤描述', 'warn'))

    # 2) 边界处理 — 跨语言结构信号（清单/图标/表格密度）
    status, text = _branch_density(md)
    issues.append((text, status))
    if status == 'pass':
        score += 1

    # 3) 输出格式定义 — 关键词 + 代码块检测
    has_output_kw = re.search(r'(输出|产出|结果|report|生成|respond\s+with|returns?\s+the)', md) is not None
    code_blocks = len(re.findall(r'```', md)) // 2
    if has_output_kw or code_blocks >= 2:
        issues.append(('✅ 定义了输出格式', 'pass'))
        score += 1
    else:
        issues.append(('🟡 未明确定义输出格式', 'warn'))

    # 4) 有示例
    if '例如' in md or '示例' in md or 'e.g.' in md.lower() or 'eg' in md.lower() or '```' in md:
        issues.append(('✅ 包含示例', 'pass'))
        score += 1
    else:
        issues.append(('🟡 缺少示例说明', 'warn'))

    # 5) 自洽 — 检查 SKILL.md 引用的文件是否在文件夹中存在
    mentioned_files = re.findall(r'[`"]([a-zA-Z0-9_./-]*[a-zA-Z0-9_]+\.(?:py|md|xlsx|xls|csv|json|yaml|yml|toml))[`"]', md)
    existing_names = {f['name'] for f in info.get('files', [])}
    existing_paths = {f.get('rel_path', f['name']) for f in info.get('files', [])}
    # 优先用完整相对路径匹配，退化为 basename
    missing = [m for m in mentioned_files if m not in existing_paths and os.path.basename(m) not in existing_names]
    if missing:
        issues.append((f'🟠 引用了不存在的文件: {missing[:3]}', 'warn'))
    elif mentioned_files:
        issues.append((f'✅ 引用文件均在文件夹中（{len(mentioned_files)} 个）', 'pass'))
        score += 1
    else:
        issues.append(('🟡 未在 SKILL.md 中检测到文件引用，跳过自洽检查', 'skip'))

    issues.append(('📝 以上为结构信号基线，语义判断（分支是否完备、逻辑是否正确）请由 AI 补充', 'info'))

    pct = score / max(total, 1)
    if pct >= 0.8:
        rating = '🟢 可靠'
    elif pct >= 0.4:
        rating = '🟡 有改进空间'
    else:
        rating = '🔴 不可靠'

    return {'rating': rating, 'issues': issues, 'score': f'{score}/{total}'}


# =============================================================================
# 4. 报告生成
# =============================================================================
