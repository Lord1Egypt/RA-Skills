"""
mcp_tool_maker.py — MCP工具自动生成器
从Python函数自动生成MCP工具注册代码
"""
import ast, os, sys

def scan_functions(filepath):
    """扫描Python文件，提取所有顶层函数信息"""
    with open(filepath, encoding="utf-8") as f:
        source = f.read()
    
    tree = compile(source, filepath, 'exec', ast.PyCF_ONLY_AST)
    functions = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
            doc = ast.get_docstring(node) or ""
            desc = doc.split('\n\n')[0].strip() if doc else f"{node.name} function"
            
            params = []
            for arg in node.args.args:
                if arg.arg == 'self':
                    continue
                params.append(arg.arg)
            
            functions.append({
                'name': node.name,
                'params': params,
                'doc': desc,
                'line': node.lineno,
            })
    
    return functions


def generate_mcp_code(functions, module_name="auto_tools"):
    """根据函数列表生成MCP工具注册代码"""
    parts = [f"# Auto-generated MCP tools from {module_name}"]
    parts.append("import sys")
    parts.append("sys.path.insert(0, r'D:\\\\coze-local\\\\db')")
    parts.append("")
    
    for fn in functions:
        name = fn['name']
        params = fn['params']
        desc_line = fn['doc'][:100].replace('"', "'")
        
        sig_parts = [f'{p}: str = ""' for p in params]
        sig = ", ".join(sig_parts)
        call_args = ", ".join(f'{p}={p}' for p in params)
        
        parts.append("@mcp.tool()")
        parts.append(f"def {name}({sig}):")
        parts.append(f'    """{desc_line}"""')
        parts.append(f"    try:")
        parts.append(f"        from {module_name} import {name}")
        parts.append(f"        return {name}({call_args})")
        parts.append(f"    except Exception as e:")
        parts.append(f'        return f"Error: {{e}}"')
        parts.append("")
    
    return "\n".join(parts)


def generate_mcp_file(input_py, output_py=None):
    """从输入文件生成MCP工具文件"""
    if not os.path.exists(input_py):
        print(f"文件不存在: {input_py}")
        return
    
    module_name = os.path.splitext(os.path.basename(input_py))[0]
    functions = scan_functions(input_py)
    
    if not functions:
        print(f"未找到可注册的函数: {input_py}")
        return
    
    code = generate_mcp_code(functions, module_name)
    
    if output_py:
        with open(output_py, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"已生成: {output_py} ({len(functions)} 个工具)")
    else:
        print(code)
    
    return code


def list_targets():
    """列出可以扫描的Python文件"""
    targets = [
        r"D:\coze-local\db\capability_executor.py",
        r"D:\coze-local\db\learn.py",
        r"D:\coze-local\db\super_search.py",
        r"D:\coze-local\db\hand.py",
        r"D:\coze-local\skills\bilibili-learn\bilibili_learn.py",
    ]
    print("可扫描的目标文件:")
    for t in targets:
        if os.path.exists(t):
            size = os.path.getsize(t)
            print(f"  [OK]   {t} ({size//1024}KB)")
        else:
            print(f"  [MISS] {t}")
    return targets


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        cmd = sys.argv[1]
        if cmd == "scan":
            path = sys.argv[2] if len(sys.argv) > 2 else r"D:\coze-local\db\capability_executor.py"
            functions = scan_functions(path)
            print(f"在 {path} 中找到 {len(functions)} 个函数:")
            for fn in functions:
                print(f"  {fn['name']}({', '.join(fn['params'])})  — 第{fn['line']}行")
        elif cmd == "generate":
            src = sys.argv[2] if len(sys.argv) > 2 else r"D:\coze-local\db\capability_executor.py"
            dst = sys.argv[3] if len(sys.argv) > 3 else None
            generate_mcp_file(src, dst)
        elif cmd == "list":
            list_targets()
        else:
            print(f"未知命令: {cmd}")
    else:
        list_targets()
        print("\n用法: py mcp_tool_maker.py scan <文件路径>")
        print("      py mcp_tool_maker.py generate <源文件> [输出文件]")
        print("      py mcp_tool_maker.py list")
