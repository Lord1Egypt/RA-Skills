#!/usr/bin/env python3
r"""接口签名一致性校验：核对代码文件的函数签名与规约清单是否一致。
用法: python signature_check.py <code.py> <spec.json>
依赖：Python 3 标准库，无第三方依赖；可独立执行。
spec.json 格式: {"functions": [{"name": "bsearch", "params": ["arr", "target"], "returns": "int"}]}
仅比对名称/参数名/返回注解（注解以文本比对，宽松模式只核对存在性）。
"""
import ast, json, sys

def collect_funcs(path):
    tree = ast.parse(open(path, encoding="utf-8").read())
    funcs = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            params = [a.arg for a in node.args.args]
            ret = ast.unparse(node.returns) if node.returns else None
            funcs[node.name] = {"params": params, "returns": ret}
    return funcs

def main():
    if len(sys.argv) != 3:
        print("用法: python signature_check.py <code.py> <spec.json>"); sys.exit(2)
    impl = collect_funcs(sys.argv[1])
    spec = json.load(open(sys.argv[2], encoding="utf-8"))
    fails = []
    for item in spec["functions"]:
        name = item["name"]
        if name not in impl:
            fails.append(f"{name}: 未找到该函数"); continue
        f = impl[name]
        if item.get("params") and f["params"] != item["params"]:
            fails.append(f"{name}: 参数不一致 期望{item['params']} 实际{f['params']}")
        if item.get("returns") and f["returns"] is not None and f["returns"] != item["returns"]:
            fails.append(f"{name}: 返回注解不一致 期望{item['returns']} 实际{f['returns']}")
    if fails:
        print("FAIL"); [print(" -", x) for x in fails]; sys.exit(1)
    print(f"PASS 共 {len(spec['functions'])} 个函数签名一致")

if __name__ == "__main__":
    main()
