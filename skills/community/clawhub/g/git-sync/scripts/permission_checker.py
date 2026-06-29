#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
permission_checker.py v1.0.0
权限检查器：扫描 skill 脚本，提取文件操作，计算权限权重，生成风险报告。

检查维度：
1. 敏感信息访问（memory/、credentials、token、password）
2. 关键位置写入（skills/、.workbuddy/、系统目录）
3. 网络访问（requests、urllib、httpx、curl）
4. 文件删除（os.remove、os.rmdir、shutil.rmtree、del、rm）
5. Subprocess 调用（os.system、subprocess、popen）

权重模型：
- 敏感信息访问：40%
- 关键位置写入：30%
- 网络访问：20%
- 文件删除：10%
- Subprocess 调用：+20% 额外加权

输出：JSON 格式风险报告 + 权限权重评分
"""

import os
from pathlib import Path
import re

import json
import sys
import ast
import tokenize
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any

# ── 路径集中管理 ─────────────────────────────────────────
from _paths import (
    _data_dir_abs, DEFAULT_DATA_DIR_RAW, SKILL_DIR,
)




# ── 常量定义 ────────────────────────────────────────────────────────────────────

SENSITIVE_PATTERNS = [
    # 记忆文件路径
    r"memory/", r"\.workbuddy/memory", r"MEMORY\.md", r"\d{4}-\d{2}-\d{2}\.md",
    # 凭证相关：前导允许 _ 禁止字母数字，尾部允许 _- 禁止字母数字
    r"(?<![a-zA-Z0-9])credential(?![a-zA-Z0-9])",
    r"(?<![a-zA-Z0-9])passwd(?![a-zA-Z0-9])",
    r"(?<![a-zA-Z0-9])password(?![a-zA-Z0-9])",
    r"(?<![a-zA-Z0-9])secret(?![a-zA-Z0-9])",
    r"(?<![a-zA-Z0-9])api[_-]?key(?![a-zA-Z0-9])",
    r"(?<![a-zA-Z0-9])token(?![a-zA-Z0-9])",
    r"(?<![a-zA-Z0-9])access[_-]?token(?![a-zA-Z0-9])",
    r"(?<![a-zA-Z0-9])private[_-]?key(?![a-zA-Z0-9])",
    # 环境变量敏感词（精确匹配）
    r"OPENAI_API_KEY", r"ANTHROPIC_API_KEY", r"GITHUB_TOKEN", r"AWS_",
]

CRITICAL_PATH_PATTERNS = [
    # 系统关键目录（真正危险的写入位置）
    r"/$", r"^[A-Za-z]:[\\/]$",  # 根目录
    r"C:\\Windows", r"C:\\Program Files", r"C:\\Users",
    r"/usr/", r"/etc/", r"/var/", r"/boot/", r"/root/",
    r"\.ssh/", r"\.gnupg/", r"\.config/", r"\.aws/",
    # 排除（合法路径，不应标记）：
    # .standardization/ → skill 标准数据目录，合法
    # skills/ → skill 安装目录，写入 SKILL.md/scripts/ 是正常操作
]

NETWORK_PATTERNS = [
    r"import requests", r"from requests", r"urllib", r"httpx",
    r"curl", r"wget", r"fetch\(", r"XMLHttpRequest",
    r"axios", r"http\.get", r"http\.post", r"websocket",
]

DELETE_PATTERNS = [
    r"os\.remove", r"os\.rmdir", r"shutil\.rmtree",
    r"\bos\.unlink\b", r"\brm\b", r"\brmdir\b",
    r"fs\.unlink", r"fs\.rmdir", r"fs\.rm",
]

SUBPROCESS_PATTERNS = [
    r"os\.system", r"subprocess", r"popen", r"popen2",
    r"exec\(", r"eval\(", r"Runtime\.getRuntime", r"ProcessBuilder",
]

# ── 权限权重配置 ────────────────────────────────────────────────────────────────

WEIGHT_CONFIG = {
    "sensitive_access": 0.40,    # 敏感信息访问 40%
    "critical_write": 0.30,       # 关键位置写入 30%
    "network_access": 0.20,       # 网络访问 20%
    "file_delete": 0.10,          # 文件删除 10%
    "subprocess_call": 0.20,      # Subprocess 调用 +20% 额外加权
}

# ── 风险等级阈值 ─────────────────────────────────────────────────────────────────

RISK_THRESHOLD = {
    "low": 0.0,
    "medium": 0.30,    # ≥ 30% 中风险
    "high": 0.60,      # ≥ 60% 高风险
    "critical": 0.80,  # ≥ 80% 严重风险
}

class PermissionChecker:
    """
    权限检查器主类。

    扫描 skill 目录下的脚本文件，检测敏感操作，计算权限权重。
    """

    def __init__(self, skill_dir: str, verbose: bool = False):
        """
        初始化权限检查器。

        Args:
            skill_dir: skill 根目录路径
            verbose: 是否输出详细日志
        """
        self.skill_dir = Path(skill_dir).resolve()
        self.verbose = verbose
        self.issues: List[Dict] = []
        self.stats = {
            "files_scanned": 0,
            "lines_scanned": 0,
            "sensitive_access": 0,
            "critical_write": 0,
            "network_access": 0,
            "file_delete": 0,
            "subprocess_call": 0,
        }
        self._current_string_ranges = []  # (start_char, end_char) for .py string literals

    # ── 公共接口 ────────────────────────────────────────────────────────────────

    def scan(self) -> Dict:
        """
        扫描 skill 目录，执行完整权限检查。

        Returns:
            dict: 检查结果字典，含权限权重、风险等级、问题列表
        """
        if self.verbose:
            print(f"[*] 扫描 skill 目录: {self.skill_dir}")

        # 1. 扫描脚本文件
        self._scan_scripts()

        # 2. 检查 SKILL.md frontmatter
        self._check_frontmatter()

        # 3. 计算权限权重
        weight = self._calculate_weight()

        # 4. 确定风险等级
        risk_level = self._determine_risk_level(weight)

        # 4.5 生成授权方式建议，并合并进 issues
        suggestions = self.suggest_authorization_methods()
        for i, sug in enumerate(suggestions):
            if i < len(self.issues):
                self.issues[i]["authorization_method"] = sug["authorization_method"]
                self.issues[i]["reason"] = sug["reason"]

        # 5. 生成报告
        report = self._generate_report(weight, risk_level)

        if self.verbose:
            print(f"[*] 扫描完成: {self.stats['files_scanned']} 文件, "
                  f"{self.stats['lines_scanned']} 行")
            print(f"[*] 风险等级: {risk_level.upper()}, 权重: {weight:.2%}")

        return report

    # ── 内部方法：文件扫描 ─────────────────────────────────────────────────────

    def _scan_scripts(self) -> None:
        """扫描 scripts/ 目录下的所有脚本文件。"""
        scripts_dir = self.skill_dir / "scripts"
        if not scripts_dir.is_dir():
            if self.verbose:
                print(f"[!] scripts/ 目录不存在: {scripts_dir}")
            return

        for ext in ["*.py", "*.js", "*.sh", "*.ps1", "*.bat"]:
            for file_path in scripts_dir.glob(ext):
                if file_path.is_file():
                    self._scan_file(file_path)

    def _get_ast_string_ranges(self, content: str) -> List[Tuple[int, int]]:
        """
        用 AST 解析 Python 源码，返回所有字符串字面量的字符偏移范围。
        用于跳过字符串内容中的关键词误匹配。
        """
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return []

        ranges = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                # 有精确结束位置（Python 3.8+）
                if hasattr(node, 'end_lineno') and hasattr(node, 'end_col_offset'):
                    start = self._linecol_to_offset(content, node.lineno, node.col_offset)
                    end = self._linecol_to_offset(content, node.end_lineno, node.end_col_offset)
                    if start is not None and end is not None:
                        ranges.append((start, end))
        return ranges

    def _linecol_to_offset(self, content: str, line: int, col: int) -> Optional[int]:
        """(line, col) → 字符偏移。"""
        lines = content.splitlines(True)
        if line < 1 or line > len(lines):
            return None
        offset = sum(len(lines[i]) for i in range(line - 1))
        return offset + col

    def _in_string(self, pos: int) -> bool:
        """检查字符位置是否在字符串字面量内。"""
        for (s, e) in self._current_string_ranges:
            if s <= pos < e:
                return True
        return False

    def _scan_file(self, file_path: Path) -> None:
        """
        扫描单个文件，检测权限相关操作。

        Args:
            file_path: 文件路径
        """
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            if self.verbose:
                print(f"[!] 无法读取文件 {file_path}: {e}")
            return

        self.stats["files_scanned"] += 1
        self.stats["lines_scanned"] += len(content.splitlines())

        # 对 .py 文件，用 AST 计算字符串字面量范围，用于跳过误匹配
        self._current_string_ranges = []
        if file_path.suffix == '.py':
            self._current_string_ranges = self._get_ast_string_ranges(content)

        # 检测各类操作
        self._check_sensitive_access(file_path, content)
        self._check_critical_write(file_path, content)
        self._check_network_access(file_path, content)
        self._check_file_delete(file_path, content)
        self._check_subprocess_call(file_path, content)

    # ── 内部方法：操作检测 ─────────────────────────────────────────────────────

    def _check_sensitive_access(self, file_path: Path, content: str) -> None:
        """
        检测敏感信息访问。

        根本修复：放弃对原始文本做正则扫描（误报率极高），
        改用 AST 语义分析：
        1. 遍历所有 ast.Constant(str) 节点
        2. 若字符串值含敏感关键词，检查其 AST 上下文
        3. 若上下文表明它是正则表达式模式定义 → 跳过
        4. 否则标记为真正的敏感信息访问
        """
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return

        # ── 构建 parent_map（节点 → 父节点）──────────────────────────────
        parent_map = {}
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                parent_map[child] = node

        # ── 收集所有含敏感关键词的字符串常量 ─────────────────────────────
        suspect_nodes = []  # (node, matched_pattern)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
                continue
            s = node.value
            for pat in SENSITIVE_PATTERNS:
                if re.search(pat, s, re.IGNORECASE):
                    suspect_nodes.append((node, pat))
                    break  # 一个字符串只要命中一个模式就够

        # ── 过滤：排除正则模式定义 ───────────────────────────────────────
        for node, matched_pattern in suspect_nodes:
            if self._is_sensitive_false_positive(node, parent_map):
                continue  # 是正则模式定义，不是真正访问敏感信息

            line_num = getattr(node, "lineno", 1)
            col = getattr(node, "col_offset", 0)
            # 尝试提取匹配的片段用于报告
            matched_text = node.value[:40].replace("\n", " ")
            self.stats["sensitive_access"] += 1
            self.issues.append({
                "type": "sensitive_access",
                "file": str(file_path.relative_to(self.skill_dir)),
                "line": line_num,
                "pattern": matched_pattern,
                "match": matched_text,
                "description": "检测到敏感信息访问（字符串常量含敏感关键词）",
                "severity": "HIGH",
            })

        # ── 额外检查：os.environ / os.getenv 调用 ─────────────────────
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            # 匹配 os.environ[...] 或 os.getenv(...)
            is_env_access = False
            if isinstance(func, ast.Subscript):
                # os.environ[...]
                if isinstance(func.value, ast.Attribute) and func.value.attr == "environ":
                    is_env_access = True
            elif isinstance(func, ast.Attribute) and func.attr in ("getenv", "environ"):
                is_env_access = True

            if not is_env_access:
                continue

            # 检查参数/下标是否含敏感关键词
            for arg in (list(node.args) + list(node.keywords)):
                val = None
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    val = arg.value
                elif isinstance(arg, ast.keyword) and isinstance(arg.value, ast.Constant) and isinstance(arg.value.value, str):
                    val = arg.value.value
                elif isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    val = arg.value

                if val:
                    for pat in SENSITIVE_PATTERNS:
                        if re.search(pat, val, re.IGNORECASE):
                            line_num = getattr(arg, "lineno", getattr(node, "lineno", 1))
                            self.stats["sensitive_access"] += 1
                            self.issues.append({
                                "type": "sensitive_access",
                                "file": str(file_path.relative_to(self.skill_dir)),
                                "line": line_num,
                                "pattern": pat,
                                "match": val[:40],
                                "description": "检测到敏感信息访问（os.environ/os.getenv 读取敏感环境变量）",
                                "severity": "HIGH",
                            })
                            break

    # ── 内部方法：正则模式判断 ─────────────────────────────────────────────

    # ── 内部方法：敏感词误报判断 ─────────────────────────────────────

    def _is_sensitive_false_positive(self, node: ast.AST, parent_map: dict) -> bool:
        """
        判断一个含敏感词的 ast.Constant(str) 节点是否是误报。
        
        通用规则（满足任一即认为是误报）：
        1. 是正则表达式模式定义（变量名含 pattern/regex/pat，或传给 re 模块函数）
        2. 是 dict 的 value 且 key 是元数据字段（label/description/replace/redact 等）
        3. 是 docstring（函数/类/模块的第一个语句，或模块级裸字符串）
        4. 是占位符字符串（如 "[credential-redacted]"、"[hidden]"）
        5. 所属变量名含 label/desc/replace/redact/placeholder/fake/mock
        """
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            return False
        
        s = node.value
        parent = parent_map.get(node)
        _META_KEYS = ("label", "description", "desc", "replace", "redact",
                     "help", "msg", "message", "text", "title", "name",
                     "note", "comment", "hint", "summary")
        _PLACEHOLDER_PREFIXES = ("[", "【", "(", "（")
        _PLACEHOLDER_SUFFIXES = ("]", "】", ")", "）", "-redacted]", "-hidden]", "-masked]")
        
        # 4. 占位符字符串
        if (s and any(s.startswith(p) for p in _PLACEHOLDER_PREFIXES)
                and any(s.endswith(p) for p in _PLACEHOLDER_SUFFIXES)):
            return True
        
        # 3. docstring / 模块级裸字符串判断（更通用）
        # Python AST 中 docstring 结构：Expr(value=Constant(value=str))
        # node 是 Constant，其父节点是 Expr，Expr 的父节点才是 Module/FunctionDef/ClassDef
        if parent is not None and isinstance(parent, ast.Expr):
            # node 在 Expr.value 中，再往上取一层得到真正的父节点
            grandparent = parent_map.get(parent)
            if grandparent is not None:
                # 模块级：Expr 在 Module.body 中 → 是模块 docstring 或裸字符串
                if isinstance(grandparent, ast.Module):
                    if parent in list(grandparent.body):
                        return True
                # 函数/类 docstring：Expr 是函数/类的第一个语句
                if isinstance(grandparent, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if grandparent.body and grandparent.body[0] is parent:
                        if isinstance(parent.value, ast.Constant) and isinstance(parent.value.value, str):
                            return True
        
        # 2. dict value，且 key 是元数据字段
        if isinstance(parent, ast.Dict):
            for i, key in enumerate(parent.keys):
                if (key is not None and i < len(parent.values)
                        and parent.values[i] is node):
                    if isinstance(key, ast.Constant) and isinstance(key.value, str):
                        if key.value.strip('"\'\'').lower() in _META_KEYS:
                            return True
        
        # 5. 所属变量名含 label/desc/replace 等
        if isinstance(parent, ast.Assign):
            for target in parent.targets:
                name = self._node_name(target)
                if name and any(k in name.lower() for k in
                                 ("label", "desc", "replace", "redact",
                                  "placeholder", "fake", "mock", "example", "demo")):
                    return True
        
        # 1. 正则模式判断（原有逻辑）
        return self._is_regex_pattern(node, parent_map)
    
    # ── 内部方法：正则模式判断 ─────────────────────────────────────────────

    def _is_regex_pattern(self, node: ast.AST, parent_map: dict) -> bool:
        """
        判断一个 ast.Constant(str) 节点是否是正则表达式模式定义。

        判断依据（满足任一即认为是模式定义）：
        1. 父节点是赋值语句，且左值变量名含 pattern/regex/pat/rule
        2. 父节点是函数调用参数，且函数名是 re.compile/re.search/re.match/re.finditer 等
        3. 父节点是 dict 的值节点，且对应的 key 字符串含 regex/pattern/pat/rule
        4. 父节点是列表/元组元素，且该列表赋值给含 pattern/regex 的变量
        """
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            return False

        parent = parent_map.get(node)

        # 1. 赋值语句：var = "...", 变量名含 pattern/regex/pat/rule
        if isinstance(parent, ast.Assign):
            for target in parent.targets:
                name = self._node_name(target)
                if name and any(k in name.lower() for k in ("pattern", "regex", "pat", "rule", "sensitive", "credential")):
                    return True

        # 2. 函数调用参数：re.compile("..."), re.search("...", ...)
        if isinstance(parent, ast.Call):
            func = parent.func
            func_name = self._node_name(func)
            if func_name and any(k in func_name.lower() for k in
                                   ("re.compile", "re.search", "re.match", "re.finditer",
                                    "re.findall", "compile", "search", "match")):
                return True
            # 方法调用：pattern.search(...), pat.match(...) 等
            if isinstance(func, ast.Attribute):
                method_name = func.attr
                if method_name and any(k in method_name.lower() for k in
                                                 ("search", "match", "finditer", "findall",
                                                  "compile", "sub", "split")):
                    # 进一步检查调用者变量名是否含 pattern/regex
                    if isinstance(func.value, ast.Name):
                        if any(k in func.value.id.lower() for k in ("pattern", "pat", "regex", "rule")):
                            return True

        # 3. dict 值节点：{"regex": "..."}，key 含 regex/pattern
        if isinstance(parent, ast.Dict):
            for i, key in enumerate(parent.keys):
                if key is not None and isinstance(key, ast.Constant) and isinstance(key.value, str):
                    if any(k in key.value.lower() for k in ("regex", "pattern", "pat", "rule", "sensitive")):
                        # 检查这个 value 节点是否是当前 node
                        if i < len(parent.values) and parent.values[i] is node:
                            return True

        # 4. 列表/元组元素，且所属容器赋值给含 pattern/regex 的变量
        if isinstance(parent, (ast.List, ast.Tuple)):
            container_parent = parent_map.get(parent)
            if isinstance(container_parent, ast.Assign):
                for target in container_parent.targets:
                    name = self._node_name(target)
                    if name and any(k in name.lower() for k in
                                     ("pattern", "patterns", "regex", "regexs", "pat", "pats")):
                        return True

        return False

    def _node_name(self, node: ast.AST) -> str:
        """提取 AST 节点的变量名/属性名。"""
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return node.attr
        return ""

    # ── 内部方法：操作检测 ─────────────────────────────────────────────

    def _check_critical_write(self, file_path: Path, content: str) -> None:
        """
        检测关键位置写入。

        正确逻辑：
        - 扫描文件写入函数调用（open/write/writelines/makedirs等）
        - 检查其路径参数是否指向系统关键目录
        - 不扫描路径定义语句（如 DATA_DIR = ...），那不是写入操作
        """
        # 真正的文件写入/创建函数
        write_patterns = [
            r"\bopen\s*\(",
            r"\.write\s*\(",
            r"\.writelines\s*\(",
            r"os\.makedirs\s*\(",
            r"os\.mkdir\s*\(",
            r"Path\(.*\)\.write",
            r"json\.dump\s*\(",
            r"yaml\.dump\s*\(",
            r"csv\.writer",
            r"open\(.*,\s*['\"]w",
        ]
        for pattern in write_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                if self._in_string(match.start()):
                    continue
                line_num = content[:match.start()].count("\n") + 1
                line_content = content.splitlines()[line_num - 1] if line_num <= len(content.splitlines()) else ""
                if line_content.strip().startswith("#"):
                    continue

                # 检查路径参数是否指向关键目录
                # 简单启发：同一行或下一行含系统目录路径
                context = line_content
                if line_num < len(content.splitlines()):
                    context += " " + content.splitlines()[line_num]

                # 只标记指向系统关键目录的写入
                sys_dirs = ["/usr/", "/etc/", "/var/", "/boot/", "/root/",
                             "C:\\Windows", "C:\\Program Files", "C:\\Users"]
                hit = any(d in context for d in sys_dirs)
                if not hit:
                    continue  # 不是系统目录，跳过

                self.stats["critical_write"] += 1
                self.issues.append({
                    "type": "critical_write",
                    "file": str(file_path.relative_to(self.skill_dir)),
                    "line": line_num,
                    "pattern": pattern,
                    "match": match.group(0),
                    "description": "检测到关键位置写入（系统目录）",
                    "severity": "HIGH",
                })

    def _check_network_access(self, file_path: Path, content: str) -> None:
        """
        检测网络访问。

        Args:
            file_path: 文件路径
            content: 文件内容
        """
        for pattern in NETWORK_PATTERNS:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                if self._in_string(match.start()):
                    continue
                line_num = content[:match.start()].count("\n") + 1
                self.stats["network_access"] += 1
                self.issues.append({
                    "type": "network_access",
                    "file": str(file_path.relative_to(self.skill_dir)),
                    "line": line_num,
                    "pattern": pattern,
                    "match": match.group(0),
                    "description": "检测到网络访问（requests/urllib/httpx等）",
                    "severity": "MEDIUM",
                })

    def _check_file_delete(self, file_path: Path, content: str) -> None:
        """
        检测文件删除操作。

        Args:
            file_path: 文件路径
            content: 文件内容
        """
        for pattern in DELETE_PATTERNS:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                if self._in_string(match.start()):
                    continue
                line_num = content[:match.start()].count("\n") + 1
                self.stats["file_delete"] += 1
                self.issues.append({
                    "type": "file_delete",
                    "file": str(file_path.relative_to(self.skill_dir)),
                    "line": line_num,
                    "pattern": pattern,
                    "match": match.group(0),
                    "description": "检测到文件删除操作（os.remove/shutil.rmtree等）",
                    "severity": "HIGH",
                })

    def _check_subprocess_call(self, file_path: Path, content: str) -> None:
        """
        检测 subprocess 调用。

        Args:
            file_path: 文件路径
            content: 文件内容
        """
        for pattern in SUBPROCESS_PATTERNS:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                if self._in_string(match.start()):
                    continue
                line_num = content[:match.start()].count("\n") + 1
                # 排除注释
                line_content = content.splitlines()[line_num - 1] if line_num <= len(content.splitlines()) else ""
                if line_content.strip().startswith("#"):
                    continue

                self.stats["subprocess_call"] += 1
                self.issues.append({
                    "type": "subprocess_call",
                    "file": str(file_path.relative_to(self.skill_dir)),
                    "line": line_num,
                    "pattern": pattern,
                    "match": match.group(0),
                    "description": "检测到 subprocess 调用（os.system/subprocess等）",
                    "severity": "HIGH",
                })

    # ── 内部方法：frontmatter 检查 ──────────────────────────────────────────────

    def _check_frontmatter(self) -> None:
        """检查 SKILL.md 的 frontmatter 是否声明了权限相关字段。"""
        skill_md = self.skill_dir / "SKILL.md"
        if not skill_md.is_file():
            return

        try:
            with open(skill_md, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            return

        # 提取 frontmatter
        fm_match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL | re.MULTILINE)
        if not fm_match:
            return

        fm_content = fm_match.group(1)

        # 检查 sensitive_access 声明
        if "sensitive_access" not in fm_content and self.stats["sensitive_access"] > 0:
            self.issues.append({
                "type": "missing_declaration",
                "file": "SKILL.md",
                "line": 1,
                "pattern": "sensitive_access",
                "match": "",
                "description": "脚本含敏感信息访问，但 frontmatter 未声明 sensitive_access: true",
                "severity": "ERROR",
            })

        # 检查 critical_write 声明
        if "critical_write" not in fm_content and self.stats["critical_write"] > 0:
            self.issues.append({
                "type": "missing_declaration",
                "file": "SKILL.md",
                "line": 1,
                "pattern": "critical_write",
                "match": "",
                "description": "脚本含关键位置写入，但 frontmatter 未声明 critical_write: true",
                "severity": "ERROR",
            })

    # ── 内部方法：权重计算 ──────────────────────────────────────────────────────

    def _calculate_weight(self) -> float:
        """
        计算权限权重。

        Returns:
            float: 权重值（0.0 ~ 1.0+）
        """
        weight = 0.0

        if self.stats["sensitive_access"] > 0:
            weight += WEIGHT_CONFIG["sensitive_access"]

        if self.stats["critical_write"] > 0:
            weight += WEIGHT_CONFIG["critical_write"]

        if self.stats["network_access"] > 0:
            weight += WEIGHT_CONFIG["network_access"]

        if self.stats["file_delete"] > 0:
            weight += WEIGHT_CONFIG["file_delete"]

        if self.stats["subprocess_call"] > 0:
            weight += WEIGHT_CONFIG["subprocess_call"]

        # 归一化到 0.0 ~ 1.0
        return min(weight, 1.0)

    def _determine_risk_level(self, weight: float) -> str:
        """
        根据权重确定风险等级。

        Args:
            weight: 权限权重

        Returns:
            str: 风险等级（low/medium/high/critical）
        """
        if weight >= RISK_THRESHOLD["critical"]:
            return "critical"
        elif weight >= RISK_THRESHOLD["high"]:
            return "high"
        elif weight >= RISK_THRESHOLD["medium"]:
            return "medium"
        else:
            return "low"

    # ── 内部方法：报告生成 ──────────────────────────────────────────────────────

    def _generate_report(self, weight: float, risk_level: str) -> Dict:
        """
        生成权限检查报告。

        Args:
            weight: 权限权重
            risk_level: 风险等级

        Returns:
            dict: 完整报告字典
        """
        return {
            "skill_dir": str(self.skill_dir),
            "risk_level": risk_level,
            "permission_weight": round(weight, 4),
            "stats": self.stats,
            "issues": self.issues,
            "summary": {
                "total_issues": len(self.issues),
                "high_severity": sum(1 for i in self.issues if i["severity"] == "HIGH"),
                "error_severity": sum(1 for i in self.issues if i["severity"] == "ERROR"),
                "recommendation": self._get_recommendation(risk_level),
            }
        }

    def _get_recommendation(self, risk_level: str) -> str:
        """
        根据风险等级给出建议。

        Args:
            risk_level: 风险等级

        Returns:
            str: 建议文本
        """
        recommendations = {
            "low": "风险较低，建议保持当前设计。",
            "medium": "中风险：建议在 SKILL.md 中增加权限说明，并在高权限操作前增加用户确认。",
            "high": "高风险：必须在 frontmatter 声明 sensitive_access/critical_write，"
                    "并在执行前通过 authorization_manager.py 请求用户授权。",
            "critical": "严重风险：建议重新评估 skill 设计，避免不必要的敏感信息访问和关键位置写入。"
                          "必须实施完整的授权检查机制。",
        }
        return recommendations.get(risk_level, "未知风险等级。")

    def _detect_skill_nature(self) -> str:
        """
        检测技能工作性质：automated（自动化）或 interactive（交互式）。

        判断依据（按优先级）：
        1. SKILL.md frontmatter 含 `automated: true` / `cron: true` → automated
        2. SKILL.md frontmatter 含 `interactive: true` → interactive
        3. description 含关键词（自动/定时/cron/schedule）→ automated
        4. tags 含 automation/cron/schedule → automated
        5. 默认 → interactive（保守）

        Returns:
            str: "automated" 或 "interactive"
        """
        skill_md = self.skill_dir / "SKILL.md"
        if not skill_md.is_file():
            return "interactive"

        try:
            content = skill_md.read_text(encoding="utf-8")
        except Exception:
            return "interactive"

        fm_match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL | re.MULTILINE)
        fm_content = fm_match.group(1) if fm_match else ""
        desc_match = re.search(r"description:\s*>(.*?)(?=\n\w|$)", content, re.DOTALL)
        description = desc_match.group(1) if desc_match else ""

        # 1. frontmatter 显式声明
        if re.search(r"^\s*automated\s*:\s*true", fm_content, re.MULTILINE | re.IGNORECASE):
            return "automated"
        if re.search(r"^\s*cron\s*:\s*true", fm_content, re.MULTILINE | re.IGNORECASE):
            return "automated"
        if re.search(r"^\s*interactive\s*:\s*true", fm_content, re.MULTILINE | re.IGNORECASE):
            return "interactive"

        # 2. description 关键词
        auto_keywords = ["自动", "定时", "cron", "schedule", "周期性", "每天", "每周", "hourly", "daily", "weekly"]
        if any(kw in description.lower() for kw in auto_keywords):
            return "automated"

        # 3. tags 关键词
        tags_match = re.search(r"tags:\s*\[(.*?)\]", fm_content, re.DOTALL)
        if tags_match:
            tags_str = tags_match.group(1).lower()
            if any(kw in tags_str for kw in ["automation", "cron", "schedule", "sync", "backup"]):
                return "automated"

        return "interactive"

    def suggest_authorization_methods(self) -> List[Dict]:
        """
        为每个检测到的风险操作建议授权方式。

        授权方式决策逻辑：
        1. 先判断技能工作性质（_detect_skill_nature）：
           - automated：自动化技能（如 git-sync、定时任务）
           - interactive：交互式技能（需要用户对话触发）

        2. 根据性质和风险类型决定授权方式：
           [automated 技能]
           - critical_write（skills/系统目录写入）→ unified（一次性授权，后续不再询问）
           - file_delete（文件删除）→ unified
           - subprocess_call（子进程调用）→ unified
           - sensitive_access（敏感信息访问）→ unified
           - 中风险 → silent（静默执行，仅记录）
           - 极关键操作（如删除非工作区目录）→ immediate（每次确认）

           [interactive 技能]
           - 高风险 → immediate（每次执行前确认）
           - 中风险 → unified（一次性授权）
           - 低风险 → silent

        Returns:
            list: 含授权建议的操作列表，每项含 {
                "file", "line", "type", "severity",
                "description", "authorization_method", "reason"
            }
        """
        nature = self._detect_skill_nature()
        suggestions = []

        for issue in self.issues:
            severity = issue.get("severity", "")
            issue_type = issue.get("type", "")
            method = "silent"
            reason = ""

            if nature == "automated":
                # 自动化技能：优先 unified，减少用户打扰
                if severity in ("HIGH", "ERROR"):
                    # 判断是否「极关键操作」→ 才用 immediate
                    is_critical = (
                        issue_type == "critical_write"
                        and "outside" in issue.get("description", "").lower()
                    ) or (
                        issue_type == "file_delete"
                        and "system" in issue.get("description", "").lower()
                    )
                    if is_critical:
                        method = "immediate"
                        reason = "极关键操作，即使是自动化技能也需每次确认"
                    else:
                        method = "unified"
                        reason = "自动化技能：一次性授权，后续自动执行不再询问"
                elif severity == "MEDIUM":
                    method = "silent"
                    reason = "自动化技能：中风险静默执行，仅记录"
                else:
                    method = "silent"
                    reason = "低风险操作，静默执行，仅记录"
            else:
                # 交互式技能：保守策略
                if severity in ("HIGH", "ERROR"):
                    method = "immediate"
                    reason = "高风险操作，每次执行前需用户确认"
                elif severity == "MEDIUM":
                    method = "unified"
                    reason = "中风险操作，可批量统一授权"
                else:
                    method = "silent"
                    reason = "低风险操作，静默执行，仅记录"

            suggestions.append({
                "file": issue.get("file", ""),
                "line": issue.get("line", 0),
                "type": issue_type,
                "severity": severity,
                "description": issue.get("description", ""),
                "authorization_method": method,
                "reason": reason,
            })

        return suggestions

# ── CLI 入口 ─────────────────────────────────────────────────────────────────────

def main():
    """命令行入口。"""
    import argparse

    parser = argparse.ArgumentParser(
        description="权限检查器：扫描 skill 脚本，计算权限权重，生成风险报告"
    )
    parser.add_argument("skill_dir", help="skill 根目录路径")
    parser.add_argument("--verbose", "-v", action="store_true", help="输出详细日志")
    parser.add_argument("--output", "-o", help="输出 JSON 报告文件路径")
    parser.add_argument("--exit-code", action="store_true",
                        help="根据风险等级设置退出码（low=0, medium=1, high=2, critical=3）")

    args = parser.parse_args()

    # 执行扫描
    checker = PermissionChecker(args.skill_dir, verbose=args.verbose)
    report = checker.scan()

    # 输出报告
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"[*] 报告已保存: {args.output}")
    else:
        print(json.dumps(report, indent=2, ensure_ascii=False))

    # 退出码
    if args.exit_code:
        exit_code_map = {"low": 0, "medium": 1, "high": 2, "critical": 3}
        sys.exit(exit_code_map.get(report["risk_level"], 0))

if __name__ == "__main__":
    main()
