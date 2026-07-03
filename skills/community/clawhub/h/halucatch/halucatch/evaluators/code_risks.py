"""代码风险扫描：常见 AI 复现篡改点（裸 except、除零、硬编码等）。"""

import re
from ..config import MESSAGES


def check_code_risks(info):
    """代码风险扫描：常见 AI 复现篡改点。"""
    issues = []
    total_checks = 0
    found_risks = 0

    if not info['py']:
        return {'rating': '🟡 无嵌入式代码', 'issues': [('🟡 无 .py 文件，无法扫描代码风险', 'skip')], 'score': '-'}

    # 合并核心代码和测试代码一起扫描（测试质量的代码风险也很重要）
    all_py = info['py']
    if info.get('test_py'):
        all_py += '\n' + info['test_py']

    # 预处理：移除字符串字面量和注释，避免被误扫描为代码风险
    py_code = re.sub(r"r'[^']*'", ' ', all_py)
    py_code = re.sub(r'r"[^"]*"', ' ', py_code)
    py_code = re.sub(r"'''[\s\S]*?'''", ' ', py_code)
    py_code = re.sub(r'"""[\s\S]*?"""', ' ', py_code)
    py_code = re.sub(r"'[^'\\]*(?:\\.[^'\\]*)*'", ' ', py_code)
    py_code = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', ' ', py_code)
    py_code = re.sub(r'#.*', ' ', py_code)

    patterns = [
        ('异常处理', r'except\s*:\s*pass', '裸 except: pass — 可能吞掉内存错误等关键异常'),
        ('浮点比较', r'\w+\s*==\s*0\.0', '浮点数精确相等比较 — 可能漏判接近 0 的值'),
        ('除零风险', r'return\s+[^/\n]*/\s*\w+', 'return 中直接返回除法结果 — 分母为 0 时无保护'),
        ('硬编码阈值', r'skiprows\s*=\s*\d', '固定的 skiprows — 格式漂移时数据错位'),
        ('路径拼接', r'[\'\"][/\w]+\s*\+\s*[\'\"\/]|[\'\"\/]\s*\+\s*[\'\"][\w/]+', '字符串拼接路径 — 建议用 os.path.join'),
        ('静默覆盖', r'open\([^)]*,\s*[\'\"]w[\'\"]', '写模式打开文件 — 未警告覆盖已有内容'),
        ('超时缺失', r'requests\.(get|post|put|delete)\([^)]*\)', 'HTTP 请求未设置 timeout — 可能无限挂起'),
    ]

    for name, pattern, desc in patterns:
        total_checks += 1
        if re.search(pattern, py_code):
            issues.append((f'🟠 [{name}] {desc}', 'warn'))
            found_risks += 1

    if found_risks == 0:
        issues.append(('✅ 未检测到常见篡改点', 'pass'))

    # 评级基于嵌入代码行数（取最大单文件）
    lines = info.get('max_py_lines', len(info['py'].splitlines()) if info['py'] else 0)
    py_count = info.get('py_count', 1 if info['py'] else 0)
    if lines > 200:
        if py_count > 1:
            issues.append((f'🟡 嵌入代码 {py_count} 个 .py 文件，最大单文件 {lines} 行 — 文件较多，AI 复现时可能遗漏', 'warn'))
        else:
            issues.append((f'🟡 嵌入代码 {lines} 行 — 较长，AI 复现时可能遗漏或篡改', 'warn'))

    # 测试文件正向信号
    test_py_count = info.get('test_py_count', 0)
    if test_py_count > 0:
        issues.append((f'✅ 检测到 {test_py_count} 个测试文件（有测试代码，质量意识不错）', 'pass'))

    if found_risks == 0 and lines <= 200:
        rating = '🟢 低风险'
    elif found_risks <= 2:
        rating = '🟠 有风险'
    else:
        rating = '🔴 高风险'

    return {'rating': rating, 'issues': issues, 'score': f'{total_checks - found_risks}/{total_checks}'}
