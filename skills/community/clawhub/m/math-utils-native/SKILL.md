# math-utils (Native CLI Edition)

## Description
这是一个基于本地操作系统 CLI 工具实现的计算技能。它不依赖大语言模型的预测能力，而是通过调用系统原生的计算器（如 Linux 下的 `bc` 或 `python3`）来确保计算的 100% 准确性。

## Implementation Logic
1. **OS Detection**: 自动识别 Linux, macOS 或 Windows 操作系统。
2. **Native Tool Selection**: 
   - Linux/macOS: 优先使用 `bc` (Arbitrary precision calculator)，备选 `python3`。
   - Windows: 使用 `PowerShell`。
3. **Execution**: 生成对应的 CLI 命令并执行。
4. **Validation**: 返回经过系统内核计算的精确结果。

## Usage
直接提供数学表达式，技能将通过服务器本地环境完成计算。

## Functions
- `calculate(expression)`: 输入数学字符串（如 "123.45 * (67 + 8.9)"），返回精确数值。
