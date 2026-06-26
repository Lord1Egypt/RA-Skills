import sys
try:
    expr = sys.argv[1]
    result = eval(expr, {"builtins": {}}, {})
    print(f"{expr} = {result}")
except Exception as e:
    print(f"计算失败: {str(e)}")
