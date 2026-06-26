"""一个交互式工具：把用户输入当成 Python 表达式求值并打印结果。"""

print("Type a Python expression:")
expr = input("> ")
result = eval(expr)
print("Result:", result)
