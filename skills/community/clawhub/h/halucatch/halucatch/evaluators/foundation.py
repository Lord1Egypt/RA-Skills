"""地基评估：检查 .py 路径参数化、列名校验、validate 模式、依赖声明等。"""

import re


def check_foundation(info):
    """地基检查：有 .py？路径写死？有 validate？"""
    issues = []
    score = 0
    total = 6

    # 1) 有固化脚本
    if info['py']:
        issues.append(('✅ 有固化 .py 脚本', 'pass'))
        score += 1
    else:
        issues.append(('🔴 无固化 .py 脚本——AI 须自行编写全部代码', 'fail'))

    # 2) 路径参数化
    if info['py']:
        matches = re.findall(r"['\"](/[^'\"]+?)['\"]", info['py'])
        hardcoded = [m for m in matches if 'Users/' in m or 'home/' in m or 'C:' in m]
        if hardcoded:
            issues.append((f'🔴 发现 {len(hardcoded)} 处硬编码路径: {hardcoded[:3]}', 'fail'))
        else:
            issues.append(('✅ 路径已参数化或无本地绝对路径', 'pass'))
            score += 1
    else:
        issues.append(('🟡 无 .py 文件，无法检查路径', 'skip'))

    # 3) validate 模式
    if info['py'] and '--validate' in info['py']:
        issues.append(('✅ 有 --validate 验证模式', 'pass'))
        score += 1
    elif info['py']:
        issues.append(('🟠 有 .py 但缺少 --validate 验证模式 → 建议在 argparse 中添加 `--validate` 参数', 'warn'))
    else:
        issues.append(('🟡 无 .py 文件，无法检查验证模式', 'skip'))

    # 4) 列名预检/输入验证
    if info['py'] and ('check_columns' in info['py'] or 'required_' in info['py'] or '列名预检' in info['py'] or '列名' in info['py']):
        issues.append(('✅ 有输入验证/列名校验', 'pass'))
        score += 1
    elif info['py']:
        issues.append(('🟠 有 .py 但缺少输入验证 → 建议添加 check_columns() 或 required_ 字段预检', 'warn'))
    else:
        issues.append(('🟡 无 .py 文件，无法检查输入验证', 'skip'))

    # 5) 文件发现机制
    if info['py']:
        if 'glob' in info['py'] or 'os.listdir' in info['py']:
            issues.append(('✅ 使用通配符/自动发现文件', 'pass'))
            score += 1
        else:
            issues.append(('🟠 有 .py 但缺少文件自动发现机制（建议用 glob）', 'warn'))
    else:
        issues.append(('🟡 无 .py 文件，跳过文件发现检查', 'skip'))

    # 6) 依赖声明
    if info['skill_md'] and ('依赖' in info['skill_md'] or 'requirements' in info['skill_md'].lower()):
        issues.append(('✅ SKILL.md 声明了依赖', 'pass'))
        score += 1
    else:
        issues.append(('🟡 SKILL.md 未声明依赖', 'warn'))

    # 评级
    pct = score / max(total, 1)
    if pct >= 0.8:
        rating = '🟢 稳固'
    elif pct >= 0.4:
        rating = '🟡 有隐患'
    else:
        rating = '🔴 无地基'

    return {'rating': rating, 'issues': issues, 'score': f'{score}/{total}'}
