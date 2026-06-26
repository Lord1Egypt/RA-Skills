"""
AST 级别安全分析模块
使用 Python AST 进行深度代码分析
"""
import ast
import os
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict


class ASTAnalyzer:
    """AST 安全分析器"""
    
    def __init__(self):
        self.findings: List[Dict] = []
        self.data_flows: List[Dict] = []
        self.sinks: Set[str] = {
            # 数据外泄 sink
            'send', 'post', 'request', 'http', 'fetch', 'axios',
            # 代码执行 sink
            'eval', 'exec', 'compile', '__import__',
            # 文件操作 sink
            'open', 'write', 'read', 'os.system',
        }
        self.sources: Set[str] = {
            # 敏感数据 source
            'password', 'secret', 'token', 'key', 'credential',
            'api_key', 'auth', 'private',
        }
    
    def analyze_file(self, filepath: str) -> Dict:
        """分析单个 Python 文件"""
        self.findings = []
        self.data_flows = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                source = f.read()
            
            tree = ast.parse(source, filename=filepath)
            self._analyze_tree(tree, filepath)
            
        except SyntaxError as e:
            self.findings.append({
                'file': filepath,
                'type': 'syntax_error',
                'message': str(e),
                'severity': 'low'
            })
        except Exception as e:
            self.findings.append({
                'file': filepath,
                'type': 'analysis_error',
                'message': str(e),
                'severity': 'low'
            })
        
        return {
            'findings': self.findings,
            'data_flows': self.data_flows
        }
    
    def _analyze_tree(self, tree: ast.AST, filepath: str):
        """分析 AST 树"""
        # 1. 查找危险函数调用
        self._find_dangerous_calls(tree, filepath)
        
        # 2. 查找硬编码敏感数据
        self._find_hardcoded_secrets(tree, filepath)
        
        # 3. 追踪数据流
        self._trace_data_flow(tree, filepath)
        
        # 4. 查找不安全的反模式
        self._find_antipatterns(tree, filepath)
    
    def _find_dangerous_calls(self, tree: ast.AST, filepath: str):
        """查找危险函数调用"""
        dangerous_patterns = {
            'eval': '代码执行风险',
            'exec': '代码执行风险',
            '__import__': '动态导入风险',
            'compile': '动态编译风险',
            'pickle.load': '不安全的反序列化',
            'yaml.load': '不安全的 YAML 解析',
            'os.system': '系统命令执行',
            'subprocess': '子进程风险',
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = self._get_func_name(node.func)
                
                if func_name in dangerous_patterns:
                    lineno = node.lineno or 0
                    self.findings.append({
                        'file': filepath,
                        'line': lineno,
                        'type': 'dangerous_call',
                        'function': func_name,
                        'message': dangerous_patterns.get(func_name, '危险函数调用'),
                        'severity': 'critical'
                    })
                
                # 检查 subprocess 调用
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr in ['system', 'popen', 'call', 'run', 'Popen']:
                        if isinstance(node.func.value, ast.Name) and node.func.value.id == 'os':
                            lineno = node.lineno or 0
                            self.findings.append({
                                'file': filepath,
                                'line': lineno,
                                'type': 'dangerous_call',
                                'function': f'os.{node.func.attr}',
                                'message': '系统命令执行风险',
                                'severity': 'critical'
                            })
    
    def _find_hardcoded_secrets(self, tree: ast.AST, filepath: str):
        """查找硬编码的敏感数据"""
        for node in ast.walk(tree):
            # 检查字符串赋值
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_name = target.id.lower()
                        
                        # 检查变量名是否包含敏感关键词
                        if any(s in var_name for s in self.sources):
                            if isinstance(node.value, ast.Constant):
                                value = str(node.value.value)
                                if len(value) > 5 and not any(w in value.lower() for w in ['example', 'test', 'changeme', 'xxx']):
                                    lineno = node.lineno or 0
                                    self.findings.append({
                                        'file': filepath,
                                        'line': lineno,
                                        'type': 'hardcoded_secret',
                                        'variable': target.id,
                                        'message': f'硬编码敏感数据: {target.id}',
                                        'severity': 'high'
                                    })
    
    def _trace_data_flow(self, tree: ast.AST, filepath: str):
        """追踪数据流：source -> sink"""
        
        class DataFlowVisitor(ast.NodeVisitor):
            def __init__(inner_self):
                inner_self.variables: Dict[str, List[str]] = defaultdict(list)
                inner_self.findings: List[Dict] = []
            
            def visit_Assign(inner_self, node):
                # 追踪变量赋值
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        if isinstance(node.value, ast.Constant):
                            inner_self.variables[target.id].append(str(node.value.value))
                        elif isinstance(node.value, ast.Attribute):
                            inner_self.variables[target.id].append(ast.unparse(node.value))
                
                ast.NodeVisitor.generic_visit(inner_self, node)
            
            def visit_Call(inner_self, node):
                func_name = ast.unparse(node.func) if hasattr(ast, 'unparse') else ''
                
                # 检查是否是危险 sink
                for sink in ['eval', 'exec', 'os.system', 'subprocess']:
                    if sink in func_name:
                        # 检查参数是否来自敏感变量
                        for arg in node.args:
                            arg_str = ast.unparse(arg) if hasattr(ast, 'unparse') else ''
                            for var, values in inner_self.variables.items():
                                if any(var in v or v in arg_str for v in values):
                                    inner_self.findings.append({
                                        'file': filepath,
                                        'line': node.lineno or 0,
                                        'type': 'data_flow',
                                        'from': var,
                                        'to': func_name,
                                        'message': f'数据流: {var} -> {func_name}',
                                        'severity': 'critical'
                                    })
                
                ast.NodeVisitor.generic_visit(inner_self, node)
        
        visitor = DataFlowVisitor()
        visitor.visit(tree)
        self.data_flows = visitor.findings
        self.findings.extend(visitor.findings)
    
    def _find_antipatterns(self, tree: ast.AST, filepath: str):
        """查找不安全反模式"""
        
        # 1. 比较 != None 应该用 is not
        for node in ast.walk(tree):
            if isinstance(node, ast.Compare):
                for op in node.ops:
                    if isinstance(op, ast.Eq) or isinstance(op, ast.NotEq):
                        # 检查是否是 None 比较
                        comparators = [c for c in node.comparators if isinstance(c, ast.Constant) and c.value is None]
                        if comparators:
                            for comp in comparators:
                                self.findings.append({
                                    'file': filepath,
                                    'line': node.lineno or 0,
                                    'type': 'antipattern',
                                    'message': '使用 ==/!= None 应该用 is/is not',
                                    'severity': 'low'
                                })
        
        # 2. 无限循环检测
        for node in ast.walk(tree):
            if isinstance(node, ast.While):
                if isinstance(node.test, ast.Constant) and node.test.value is True:
                    self.findings.append({
                        'file': filepath,
                        'line': node.lineno or 0,
                        'type': 'antipattern',
                        'message': '潜在无限循环',
                        'severity': 'medium'
                    })
    
    def _get_func_name(self, node) -> str:
        """获取函数名"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name):
                return f"{node.value.id}.{node.attr}"
            return node.attr
        return ""
    
    def analyze_directory(self, directory: str) -> Dict:
        """分析目录下所有 Python 文件"""
        all_findings = []
        path = Path(directory)
        
        for pyfile in path.rglob('*.py'):
            if '__pycache__' in str(pyfile):
                continue
            result = self.analyze_file(str(pyfile))
            all_findings.extend(result['findings'])
        
        return {'findings': all_findings}
    
    def generate_report(self) -> str:
        """生成报告"""
        lines = []
        lines.append("=" * 50)
        lines.append("AST 安全分析报告")
        lines.append("=" * 50)
        
        if not self.findings:
            lines.append("\n✓ 未发现问题")
            return "\n".join(lines)
        
        critical = [f for f in self.findings if f.get('severity') == 'critical']
        high = [f for f in self.findings if f.get('severity') == 'high']
        medium = [f for f in self.findings if f.get('severity') == 'medium']
        
        lines.append(f"\n共发现 {len(self.findings)} 个问题:")
        lines.append(f"  - Critical: {len(critical)}")
        lines.append(f"  - High: {len(high)}")
        lines.append(f"  - Medium: {len(medium)}")
        
        for f in self.findings[:15]:
            lines.append(f"\n[{f.get('severity', '?').upper()}] {f.get('file', 'unknown')}")
            if 'line' in f:
                lines.append(f"  Line {f['line']}: {f.get('message', '')}")
            else:
                lines.append(f"  {f.get('message', '')}")
        
        return "\n".join(lines)


# 示例用法
if __name__ == "__main__":
    analyzer = ASTAnalyzer()
    
    test_code = """
import os
import pickle
import yaml

# 硬编码密码
API_KEY = "sk-1234567890abcdef"
password = "admin123"

# 危险函数
def dangerous():
    eval("print('hello')")
    os.system("ls")

# 数据流问题
def unsafe_use():
    secret = "my_password"
    os.system(secret)  # 数据流: secret -> os.system

# 反模式
def bad_compare():
    if password != None:
        print("not none")

# 无限循环
def infinite():
    while True:
        print("forever")
"""
    
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        f.flush()
        result = analyzer.analyze_file(f.name)
    
    print(analyzer.generate_report())
