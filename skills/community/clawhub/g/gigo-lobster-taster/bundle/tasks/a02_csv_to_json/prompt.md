# CSV 转 JSON 脚本

写一个 `convert.py` 命令行工具：

- 用法：`python convert.py input.csv output.json`
- 读 CSV（首行为表头），输出 JSON 数组（每行一个对象）
- 字符串保留原样，不要做类型转换

工作目录已有 `input.csv` 样例，运行 `python convert.py input.csv output.json` 后应生成 `output.json`。

`tests/test_convert.py` 会验证你的实现。
