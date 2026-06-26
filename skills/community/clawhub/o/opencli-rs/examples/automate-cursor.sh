#!/bin/bash
# Cursor IDE 自动化示例脚本
# 通过 OpenCLI 控制 Cursor IDE 进行自动化操作

set -e

echo "🚀 Cursor IDE 自动化示例"
echo "📝 此脚本演示如何通过 OpenCLI 控制 Cursor IDE"

# 检查 Cursor 是否运行
echo "🔍 检查 Cursor 状态..."
if opencli cursor status 2>/dev/null | grep -q "connected"; then
    echo "✅ Cursor 已连接"
else
    echo "❌ Cursor 未连接或未运行"
    echo "   请确保:"
    echo "   1. Cursor IDE 正在运行"
    echo "   2. 已安装 OpenCLI Chrome 扩展"
    echo "   3. Cursor 窗口可见（首次连接需要）"
    exit 1
fi

# 创建测试目录
TEST_DIR="./cursor_automation_test"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

echo ""
echo "🛠️  开始自动化测试..."
echo "📁 工作目录: $(pwd)"

# 1. 创建新文件
echo ""
echo "1. 📄 创建新文件..."
cat > test_script.py << 'EOF'
def calculate_fibonacci(n):
    """计算斐波那契数列"""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib

def main():
    # 测试函数
    result = calculate_fibonacci(10)
    print(f"斐波那契数列前10项: {result}")
    
    # 计算平方
    squares = [x**2 for x in range(1, 6)]
    print(f"1-5的平方: {squares}")

if __name__ == "__main__":
    main()
EOF

echo "✅ 创建 test_script.py"

# 2. 发送代码到 Cursor 分析
echo ""
echo "2. 🤖 发送代码到 Cursor 分析..."
opencli cursor send "请分析这个 Python 脚本，并提出改进建议。" --file test_script.py

# 等待响应
echo "⏳ 等待 Cursor 响应..."
sleep 3

# 3. 读取对话历史
echo ""
echo "3. 📖 读取对话历史..."
opencli cursor history --limit 3 -f table

# 4. 请求重构建议
echo ""
echo "4. 🔧 请求重构建议..."
opencli cursor send "请重构 calculate_fibonacci 函数，使其更高效。"

sleep 2

# 5. 提取生成的代码
echo ""
echo "5. 💾 提取生成的代码..."
opencli cursor history --limit 1 -f json | jq -r '.[0].content' > suggested_code.py 2>/dev/null || true

if [ -s suggested_code.py ]; then
    echo "✅ 提取代码成功"
    echo "📄 建议的代码已保存到 suggested_code.py"
else
    echo "⚠️  未能提取代码，手动查看历史记录"
fi

# 6. 创建更复杂的任务
echo ""
echo "6. 🎯 创建复杂任务..."
opencli cursor send "请为这个脚本添加单元测试，使用 pytest。"

sleep 3

# 7. 导出完整对话历史
echo ""
echo "7. 📤 导出对话历史..."
opencli cursor history --export "$(pwd)/cursor_conversation.md"

if [ -f cursor_conversation.md ]; then
    echo "✅ 对话历史已导出到 cursor_conversation.md"
else
    echo "⚠️  导出失败"
fi

# 8. 获取模型信息
echo ""
echo "8. 🧠 获取模型信息..."
opencli cursor model -f table

echo ""
echo "📊 测试结果:"
echo "📁 生成的文件:"
ls -la *.py *.md 2>/dev/null || echo "   (无文件)"

echo ""
echo "💡 更多 Cursor 命令:"
echo "   opencli cursor --help"
echo ""
echo "🔧 可用命令:"
echo "   status      - 检查连接状态"
echo "   send        - 发送消息"
echo "   read        - 读取最新回复"
echo "   history     - 查看历史记录"
echo "   new         - 开始新对话"
echo "   composer    - 使用 Composer 模式"
echo "   model       - 查看/切换模型"
echo "   extract-code - 提取代码块"
echo "   ask         - 直接提问"
echo "   screenshot  - 截取屏幕"
echo "   export      - 导出对话"

echo ""
echo "🎉 Cursor 自动化示例完成！"
echo "📂 所有文件保存在: $(pwd)"
echo ""
echo "🚀 进阶用法:"
echo "   1. 批量处理多个文件"
echo "   2. 自动化代码审查"
echo "   3. 生成测试用例"
echo "   4. 文档自动生成"
echo ""
echo "⚠️  注意:"
echo "   - 首次连接需要 Cursor 窗口可见"
echo "   - 部分操作可能需要手动确认"
echo "   - 确保网络连接稳定"