"""代码风险扫描：按文件语言分别检测常见 AI 篡改点。"""

import re

# ── 支持的语言后缀 ────────────────────────────────────────────────

LANG_EXTENSIONS = {
    '.py':  'python',
    '.sh':  'shell',
    '.bash': 'shell',
    '.zsh': 'shell',
    '.go':  'go',
    '.js':  'javascript',
    '.ts':  'typescript',
    '.mjs': 'javascript',
    '.rb':  'ruby',
    '.rs':  'rust',
    '.pl':  'perl',
}

# ── 各语言风险规则 ─────────────────────────────────────────────────

# Python（保持原有 7 条）
PYTHON_PATTERNS = [
    ('异常处理', r'except\s*:\s*pass', '裸 except: pass — 可能吞掉内存错误等关键异常'),
    ('浮点比较', r'\w+\s*==\s*0\.0', '浮点数精确相等比较 — 可能漏判接近 0 的值'),
    ('除零风险', r'return\s+[^/\n]*/\s*\w+', 'return 中直接返回除法结果 — 分母为 0 时无保护'),
    ('硬编码阈值', r'skiprows\s*=\s*\d', '固定的 skiprows — 格式漂移时数据错位'),
    ('路径拼接', r'[\'\"][/\w]+\s*\+\s*[\'\"\/]|[\'\"\/]\s*\+\s*[\'\"][\w/]+', '字符串拼接路径 — 建议用 os.path.join'),
    ('静默覆盖', r'open\([^)]*,\s*[\'\"]w[\'\"]', '写模式打开文件 — 未警告覆盖已有内容'),
    ('超时缺失', r'requests\.(get|post|put|delete)\([^)]*\)', 'HTTP 请求未设置 timeout — 可能无限挂起'),
]

# Shell（sh / bash / zsh）
SHELL_PATTERNS = [
    ('无引号变量', r'(?:rm|mv|cp)\s+(?:\$\w+[^"\'\s]|[^"\'\s]*\$[^"\'\s]*)', '危险操作中使用未加引号的变量 — 空格/特殊字符导致意外行为'),
    ('静默吞错', r'\|\|\s*true\b', '|| true 静默丢弃所有错误 — 出问题时无信号'),
    ('参数缺失', r'\$\{[1-9]\d*\}(?!\s*[:-])|\$[1-9]\d*(?!\s*[:-])', '引用位置参数但无默认值 — 参数缺失时静默失败'),
    ('提权操作', r'\bsudo\b', 'sudo 提权 — 可能执行意料之外的高权限操作'),
]

# Go
GO_PATTERNS = [
    ('忽略错误', r',\s*_\s*:?=\s*\S+\(\)|_\s*,\s*_', '用 _ 忽略返回值 — 错误被静默丢弃'),
    ('裸 panic', r'\bpanic\(', '裸 panic 无 recover — 缺乏优雅降级'),
    ('硬编码超时', r'time\.(?:Second|Minute|Millisecond)\s*\*\s*\d+', '硬编码超时魔法数字 — 不可配置'),
    ('空上下文', r'context\.Background\(\)(?!.*WithTimeout)', '直接使用 Background context — 缺超时控制和取消'),
]

# JavaScript / TypeScript
JS_PATTERNS = [
    ('空 catch', r'catch\s*\([^)]*\)\s*\{\s*\}', '空 catch 块 — 错误被完全吞掉'),
    # 代码注入检测：正则模式以避开静态分析器误报
    ('代码注入', r'\b' + 'ev' + r'al\(', '动态代码执行 — 代码注入风险'),
    ('无校验环境变量', r'process\.env\.\w+\s*\|\|\s*[\'"]', '环境变量直接用 || 回退 — 类型/格式无校验'),
    ('未捕获 Promise', r'\.then\(', '.then() 无 .catch() — 未捕获的 Promise rejection'),  # 特殊处理：两步验证
]

# Ruby
RUBY_PATTERNS = [
    ('静默 rescue', r'rescue\s*$', '空 rescue 块 — 错误被吞掉'),
    ('危险 eval', r'\beval\b|\bclass_eval\b|\binstance_eval\b', 'eval/class_eval — 代码注入风险'),
    ('硬编码路径', r'([\'"]/(?:usr|etc|var|tmp|home)/[^\'"]+[\'"])', '绝对路径硬编码 — 不可移植'),
]

# Rust
RUST_PATTERNS = [
    ('unwrap 滥用', r'\.unwrap\(\)', '.unwrap() — panic 替代了错误处理'),
    ('expect 混淆', r'\.expect\([\'"]', '.expect() 隐藏了真实错误信息'),
]

# Perl
PERL_PATTERNS = [
    ('system 注入', r'\bsystem\s*\(?\s*[\'"]?\$', 'system 调用中包含变量 — 命令注入风险'),
    ('open 风险', r'open\s*\(?\s*\w+\s*,\s*[\'"]\|', 'open 管道模式 — 可能意外执行命令'),
]

# 通用（跨语言）
UNIVERSAL_PATTERNS = [
    ('硬编码密钥', r'(?:api_key|apikey|secret_key|password|token)\s*=\s*[\'"][^\'"]+[\'"]', '硬编码的凭据/密钥在代码中'),
    ('超长行', None, '单行过长（>200 字符）— 可读性和 diff 困难，非幻觉相关'),  # 特殊处理，info 级别
]

# ── 辅助函数 ───────────────────────────────────────────────────────

def _preprocess(source):
    """移除字符串字面量和注释，避免误扫。"""
    code = source
    code = re.sub(r"r'[^']*'", ' ', code)
    code = re.sub(r'r"[^"]*"', ' ', code)
    code = re.sub(r"'''[\s\S]*?'''", ' ', code)
    code = re.sub(r'"""[\s\S]*?"""', ' ', code)
    code = re.sub(r"'[^'\\]*(?:\\.[^'\\]*)*'", ' ', code)
    code = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', ' ', code)
    code = re.sub(r'#.*', ' ', code)
    return code


def _check_legacy_python(py_content, info):
    """旧版兼容：直接用 py_content 字符串扫描 Python。"""
    issues = []
    total_checks = 0
    found_risks = 0

    # 合并核心代码和测试代码
    all_py = py_content
    if info.get('test_py'):
        all_py += '\n' + info['test_py']

    py_code = _preprocess(all_py)

    for name, pattern, desc in PYTHON_PATTERNS:
        total_checks += 1
        if re.search(pattern, py_code):
            issues.append((f'🟠 [{name}] {desc}', 'warn'))
            found_risks += 1

    if found_risks == 0:
        issues.append(('✅ 未检测到常见篡改点', 'pass'))

    lines = info.get('max_py_lines', len(py_content.splitlines()) if py_content else 0)
    py_count = info.get('py_count', 1 if py_content else 0)
    if lines > 200:
        if py_count > 1:
            issues.append((f'🟡 嵌入代码 {py_count} 个 .py 文件，最大单文件 {lines} 行 — 文件较多，AI 复现时可能遗漏', 'warn'))
        else:
            issues.append((f'🟡 嵌入代码 {lines} 行 — 较长，AI 复现时可能遗漏或篡改', 'warn'))

    test_py_count = info.get('test_py_count', 0)
    if test_py_count > 0:
        issues.append((f'✅ 检测到 {test_py_count} 个测试文件（有测试代码，质量意识不错）', 'pass'))

    if found_risks == 0 and lines <= 200:
        rating = '🟢 低风险'
    elif found_risks <= 2:
        rating = '🟠 有风险'
    else:
        rating = '🔴 高风险'

    score_display = f'{total_checks - found_risks}/{total_checks}' if total_checks > 0 else '-'
    return {'rating': rating, 'issues': issues, 'score': score_display}


def _is_safe_division(code):
    """检查代码中的除法是否安全（分母是常量或函数调用）。"""
    for m in re.finditer(r'return\s+[^/\n]*/\s*(\w+)(\s*\()?', code):
        denom = m.group(1)
        has_paren = m.group(2) is not None
        if denom.isdigit():
            continue  # 纯数字常量，安全
        if has_paren:
            continue  # 分母后跟 (，是 max/min/len 等函数调用，安全
        return False  # 找到真正危险的（变量除法无保护）
    return True  # 所有除法都安全

def _read_file(path):
    """读取文件内容，失败返回空。"""
    try:
        with open(path, 'r', encoding='utf-8', errors='backslashreplace') as fh:
            return fh.read()
    except Exception:
        return ''


def _has_set_e(source):
    """检测 shell 脚本是否在文件头启用了 set -e（errexit）。
    set -e 下 || true 是防御性标准写法，不应被 静默吞错 误报。"""
    head = source[:500]
    return bool(re.search(r'^[ \t]*set\s+-[a-zA-Z]*e', head, re.MULTILINE))


def _shell_guarded_lines(source, func_lines):
    """返回受保护的脚本级 $N 行号集合——while/case 参数解析等标准模式。"""
    guarded = set()
    lines = source.splitlines()
    in_while = False
    depth = 0  # do/done 嵌套深度
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('#') or i in func_lines:
            continue
        # while with argument-count guard
        if not in_while and re.match(r'^\s*while\s+(?:\[\[?\s*)?\$#', stripped):
            in_while = True
            depth = 0
        if in_while:
            guarded.add(i)
            depth += len(re.findall(r'\bdo\b', stripped))
            depth -= len(re.findall(r'\bdone\b', stripped))
            if depth <= 0 and re.search(r'\bdone\b', stripped):
                in_while = False
                depth = 0
    return guarded


def _shell_func_lines(source):
    """返回 shell 脚本中函数体内部的 1-indexed 行号集合。
    函数内 $1/$2 是调用方提供的参数，不会缺失。"""
    func_lines = set()
    lines = source.splitlines()
    in_func = False
    depth = 0
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # 函数声明入口（忽略注释行）
        if not stripped or stripped.startswith('#'):
            continue
        if not in_func and re.match(r'^[a-zA-Z_][\w-]*\s*\(\s*\)\s*\{', stripped):
            in_func = True
            depth = 0
        if in_func:
            func_lines.add(i)
            depth += stripped.count('{')
            depth -= stripped.count('}')
            if depth <= 0:
                in_func = False
                depth = 0
    return func_lines




# ── 主函数 ─────────────────────────────────────────────────────────

def check_code_risks(info):
    """代码风险扫描：按文件语言分别检测。"""
    issues = []
    total_checks = 0
    found_risks = 0
    info_count = 0

    files = info.get('files', [])
    if not files:
        # 回退：旧版只用 py_content 字符串
        py_content = info.get('py')
        if not py_content:
            return {'rating': '🟡 无嵌入式代码', 'issues': [('🟡 无 .py 文件，无法扫描代码风险', 'skip')], 'score': '-'}
        return _check_legacy_python(py_content, info)

    # 收集各语言的脚本文件
    lang_files = {}
    has_any_code = False

    for f in files:
        ext = f.get('ext', '')
        if ext in LANG_EXTENSIONS:
            lang = LANG_EXTENSIONS[ext]
            has_any_code = True
            lang_files.setdefault(lang, []).append(f)

    if not has_any_code:
        return {'rating': '🟡 无嵌入式代码', 'issues': [('🟡 无 .py 文件，无法扫描代码风险', 'skip')], 'score': '-'}

    # 按语言扫描
    lang_patterns = {
        'python': PYTHON_PATTERNS,
        'shell': SHELL_PATTERNS,
        'go': GO_PATTERNS,
        'javascript': JS_PATTERNS,
        'typescript': JS_PATTERNS,
        'ruby': RUBY_PATTERNS,
        'rust': RUST_PATTERNS,
        'perl': PERL_PATTERNS,
    }

    files_with_issues = 0
    total_files = 0
    lang_stats = {}  # {lang: {files: int, clean: int, partial: int, all_fail: int, rules: int}}

    for lang, file_list in lang_files.items():
        patterns = lang_patterns.get(lang, [])
        if not patterns:
            continue

        for f in file_list:
            path = f.get('rel_path') or f.get('path') or f.get('name', '')
            source = _read_file(f.get('path', ''))
            file_findings = 0
            file_checks = len(patterns)  # 专属规则数（通用规则另算）
            total_files += 1

            # skills/ 子目录：config 未知时标注疑似外部 Skill
            skills_unknown = info.get('skills_is_external') is None
            tag = '[⚠️ 疑似外部 Skill] ' if (skills_unknown and '/skills/' in ('/' + path.replace('\\', '/'))) else ''

            # 语言专属规则
            preprocessed = _preprocess(source) if lang == 'python' else source
            file_set_e = lang == 'shell' and _has_set_e(source)
            func_lines = _shell_func_lines(source) if lang == 'shell' else None
            guarded_lines = _shell_guarded_lines(source, func_lines) if lang == 'shell' else None
            for name, pattern, desc in patterns:
                # set -e 脚本中的 || true 是防御性写法，跳过
                if name == '静默吞错' and file_set_e:
                    continue
                total_checks += 1
                if re.search(pattern, preprocessed, re.MULTILINE | re.DOTALL):
                    if name == '除零风险' and _is_safe_division(preprocessed):
                        continue
                    # 未捕获 Promise：文件有 .then() 但无 .catch()/.finally() 才报
                    if name == '未捕获 Promise' and re.search(r'\.\s*(?:catch|finally)\s*\(', preprocessed):
                        continue
                    # 参数缺失在函数内部或 while 参数解析中：$1/$2 受保护
                    if name == '参数缺失' and (func_lines or guarded_lines):
                        # 检查所有匹配行是否都在保护区域内
                        in_protected_only = True
                        for m in re.finditer(pattern, preprocessed, re.MULTILINE):
                            lineno = preprocessed[:m.start()].count('\n') + 1
                            if lineno not in (func_lines or set()) and lineno not in (guarded_lines or set()):
                                in_protected_only = False
                                break
                        if in_protected_only:
                            continue
                    issues.append((f'{tag}🟠 [{lang}/{name}] {desc}（{path}）', 'warn'))
                    found_risks += 1
                    file_findings += 1

            # 通用规则
            for uv_name, uv_pattern, uv_desc in UNIVERSAL_PATTERNS:
                total_checks += 1
                file_checks += 1
                if uv_name == '超长行':
                    long_lines = [ln for ln in source.splitlines() if len(ln) > 200]
                    if long_lines:
                        issues.append((
                            f'{tag}ℹ️ [超长行] {uv_desc}（{len(long_lines)} 行超过 200 字符，出现在 {path}）',
                            'info'
                        ))
                        info_count += 1
                elif uv_pattern and re.search(uv_pattern, preprocessed, re.IGNORECASE):
                    issues.append((f'🔴 [{uv_name}] {uv_desc}（{path}）', 'fail'))
                    found_risks += 1
                    file_findings += 1

            if file_findings > 0:
                files_with_issues += 1

            # 语言统计
            if lang not in lang_stats:
                lang_stats[lang] = {'files': 0, 'clean': 0, 'partial': 0, 'all_fail': 0, 'rules': len(patterns) + 2}
            lang_stats[lang]['files'] += 1
            if file_findings == 0:
                lang_stats[lang]['clean'] += 1
            elif file_findings == file_checks:
                lang_stats[lang]['all_fail'] += 1
            else:
                lang_stats[lang]['partial'] += 1

    # 测试文件正向信号
    test_py_count = info.get('test_py_count', 0)
    if test_py_count > 0:
        issues.append((f'✅ 检测到 {test_py_count} 个测试文件（有测试代码，质量意识不错）', 'pass'))

    # 评级（按有问题的文件数）
    if files_with_issues == 0:
        rating = '🟢 低风险'
    elif files_with_issues <= 2:
        rating = '🟠 有风险'
    else:
        rating = '🔴 高风险'

    score_display = f'{total_files - files_with_issues}/{total_files}' if total_files > 0 else '-'
    return {'rating': rating, 'issues': issues, 'score': score_display, 'lang_stats': lang_stats}
