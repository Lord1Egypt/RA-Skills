#!/usr/bin/env python3
"""
OpenClaw 代码扫描器
扫描源代码文件，提取关键信息
"""
import os
import re
from pathlib import Path
from typing import Dict, List, Set
import ast

class CodeScanner:
    """代码扫描器"""
    
    def __init__(self, openclaw_path='/root/.nvm/versions/node/v22.22.0/lib/node_modules/openclaw'):
        self.openclaw_path = Path(openclaw_path)
        
    def scan_all_files(self) -> Dict[str, List[Path]]:
        """扫描所有代码文件"""
        files = {
            'javascript': [],
            'typescript': [],
            'python': [],
            'json': []
        }
        
        for root, dirs, filenames in os.walk(self.openclaw_path):
            root_path = Path(root)
            
            for filename in filenames:
                file_path = root_path / filename
                suffix = file_path.suffix
                
                if suffix == '.js':
                    files['javascript'].append(file_path)
                elif suffix == '.ts':
                    files['typescript'].append(file_path)
                elif suffix == '.py':
                    files['python'].append(file_path)
                elif suffix == '.json':
                    files['json'].append(file_path)
        
        return files
    
    def extract_functions(self, file_path: Path) -> List[Dict]:
        """提取函数定义"""
        functions = []
        
        try:
            content = file_path.read_text()
            
            # JavaScript/TypeScript函数
            if file_path.suffix in ['.js', '.ts']:
                patterns = [
                    r'async\s+function\s+(\w+)\s*\([^)]*\)',
                    r'function\s+(\w+)\s*\([^)]*\)',
                    r'const\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>',
                    r'(\w+)\s*:\s*(?:async\s+)?function'
                ]
                
                for pattern in patterns:
                    matches = re.finditer(pattern, content)
                    for match in matches:
                        func_name = match.group(1)
                        line_num = content[:match.start()].count('\n') + 1
                        
                        functions.append({
                            'name': func_name,
                            'file': str(file_path.relative_to(self.openclaw_path)),
                            'line': line_num,
                            'type': 'async' if 'async' in match.group(0) else 'sync'
                        })
            
            # Python函数
            elif file_path.suffix == '.py':
                try:
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            functions.append({
                                'name': node.name,
                                'file': str(file_path.relative_to(self.openclaw_path)),
                                'line': node.lineno,
                                'type': 'async' if isinstance(node, ast.AsyncFunctionDef) else 'sync'
                            })
                except:
                    pass
                    
        except Exception as e:
            pass
        
        return functions
    
    def find_hook_patterns(self) -> Dict[str, List[Dict]]:
        """查找钩子模式"""
        patterns = {
            'event_emitters': [],
            'callback_calls': [],
            'middleware_use': []
        }
        
        files = self.scan_all_files()
        all_js_files = files['javascript'] + files['typescript']
        
        for file_path in all_js_files:
            try:
                content = file_path.read_text()
                
                # 查找事件发射器
                event_pattern = r'\.emit\s*\([\'"](\w+)[\'"]'
                matches = re.finditer(event_pattern, content)
                for match in matches:
                    patterns['event_emitters'].append({
                        'event': match.group(1),
                        'file': str(file_path.relative_to(self.openclaw_path)),
                        'line': content[:match.start()].count('\n') + 1
                    })
                
                # 查找回调调用
                callback_pattern = r'(\w+)\s*\('
                # 简化的模式匹配
                matches = re.finditer(callback_pattern, content)
                for match in matches:
                    func_name = match.group(1)
                    if 'hook' in func_name.lower() or 'callback' in func_name.lower():
                        patterns['callback_calls'].append({
                            'function': func_name,
                            'file': str(file_path.relative_to(self.openclaw_path)),
                            'line': content[:match.start()].count('\n') + 1
                        })
                        
            except Exception as e:
                continue
        
        return patterns

if __name__ == '__main__':
    scanner = CodeScanner()
    
    print("=== 代码扫描 ===\n")
    
    files = scanner.scan_all_files()
    for file_type, file_list in files.items():
        print(f"{file_type}: {len(file_list)} files")
    
    # 扫描函数
    all_functions = []
    for js_file in files['javascript'][:5]:  # 限制数量
        funcs = scanner.extract_functions(js_file)
        all_functions.extend(funcs)
    
    print(f"\n发现函数: {len(all_functions)}")
    
    # 查找钩子模式
    patterns = scanner.find_hook_patterns()
    print(f"\n事件发射器: {len(patterns['event_emitters'])}")
    print(f"回调调用: {len(patterns['callback_calls'])}")
