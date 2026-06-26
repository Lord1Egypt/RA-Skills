#!/bin/bash
# macOS Desktop Control 鼠标键盘控制示例

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/desktop_ctrl.py"

echo "🦐 macOS Desktop Control - 鼠标键盘控制示例"
echo ""
echo "================================================"
echo ""

# 1. 获取鼠标位置
echo "1️⃣  获取鼠标位置"
python3 "$PYTHON_SCRIPT" mouse position
echo ""

# 2. 移动鼠标
echo "2️⃣  移动鼠标到 (500, 300)"
python3 "$PYTHON_SCRIPT" mouse move 500 300
sleep 1
echo ""

# 3. 点击鼠标
echo "3️⃣  点击鼠标"
python3 "$PYTHON_SCRIPT" mouse click 500 300
sleep 0.5
echo ""

# 4. 双击
echo "4️⃣  双击鼠标"
python3 "$PYTHON_SCRIPT" mouse click 500 300 --clicks 2
sleep 0.5
echo ""

# 5. 键盘输入
echo "5️⃣  键盘输入（需要焦点在文本框）"
echo "   ⚠️  此示例不会实际执行，避免误操作"
# python3 "$PYTHON_SCRIPT" keyboard type "Hello from macOS Desktop Control!"
echo ""

# 6. 按键
echo "6️⃣  按下空格键"
python3 "$PYTHON_SCRIPT" keyboard press space
sleep 0.5
echo ""

# 7. 快捷键
echo "7️⃣  快捷键 Cmd+Shift+4（区域截图）"
echo "   ⚠️  需要授予辅助功能权限"
# python3 "$PYTHON_SCRIPT" keyboard hotkey command shift 4
echo ""

# 8. 截屏
echo "8️⃣  Python 截屏"
python3 "$PYTHON_SCRIPT" screenshot
echo ""

# 9. 进程列表
echo "9️⃣  进程列表（CPU 占用前 10）"
python3 "$PYTHON_SCRIPT" process list
echo ""

echo "================================================"
echo "✅ 示例执行完成！"
echo ""
echo "📚 更多用法："
echo "  python3 scripts/desktop_ctrl.py --help"
echo "  cat examples/basic_usage.md"
echo ""
