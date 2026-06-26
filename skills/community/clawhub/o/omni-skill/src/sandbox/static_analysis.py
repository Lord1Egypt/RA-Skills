import ast
import re
from typing import List, Tuple
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.settings as settings

class SecurityAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.findings = []
        self.score = settings.SCORE_INITIAL
        # 常见危险模块，主要涉及系统调用、文件操作和网络请求
        self.dangerous_imports = {
            'os', 'sys', 'subprocess', 'shlex', 'pty', 
            'socket', 'urllib', 'requests', 'http', 'ftplib'
        }
        # 常见危险函数
        self.dangerous_functions = {
            'eval', 'exec', 'compile', 'open', 'system', 'popen'
        }

    def visit_Import(self, node):
        for alias in node.names:
            base_module = alias.name.split('.')[0]
            if base_module in self.dangerous_imports:
                self.findings.append(f"危险导入: {alias.name} (行 {node.lineno})")
                self.score -= settings.SCORE_PENALTY_OS_MODULE
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            base_module = node.module.split('.')[0]
            if base_module in self.dangerous_imports:
                self.findings.append(f"危险导入: {node.module} (行 {node.lineno})")
                self.score -= settings.SCORE_PENALTY_OS_MODULE
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in self.dangerous_functions:
                self.findings.append(f"危险函数调用: {node.func.id} (行 {node.lineno})")
                self.score -= settings.SCORE_PENALTY_EVAL
        elif isinstance(node.func, ast.Attribute):
            if node.func.attr in self.dangerous_functions:
                self.findings.append(f"危险方法调用: {node.func.attr} (行 {node.lineno})")
                self.score -= settings.SCORE_PENALTY_OPEN
        self.generic_visit(node)

def analyze_code(code: str) -> Tuple[int, List[str]]:
    """
    静态分析代码，结合正则表达式与抽象语法树(AST)检测危险的文件或网络API。
    返回: (安全分数, 发现的问题列表)
    """
    score = settings.SCORE_INITIAL
    findings = []
    
    # 正则表达式备用检查（用于快速检测硬编码的网络URL和文件路径特征）
    url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
    file_path_pattern = re.compile(r'(?:/[^/\0]+)+/?|[a-zA-Z]:\\[^\\]+')
    
    for i, line in enumerate(code.splitlines(), 1):
        if url_pattern.search(line):
            findings.append(f"疑似硬编码URL: (行 {i})")
            score -= settings.SCORE_PENALTY_URL
            
    try:
        tree = ast.parse(code)
        analyzer = SecurityAnalyzer()
        analyzer.visit(tree)
        
        # 汇总AST的扣分
        score -= (settings.SCORE_INITIAL - analyzer.score)
        findings.extend(analyzer.findings)
    except SyntaxError as e:
        findings.append(f"语法错误，无法解析为AST: {e}")
        score = 0
        
    # 分数下限为0
    final_score = max(0, score)
    return final_score, findings
