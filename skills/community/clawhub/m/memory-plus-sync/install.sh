#!/bin/bash
# 共享文件夹记忆同步系统 - 安装脚本

set -e

echo "🚀 开始安装共享文件夹记忆同步系统"
echo "======================================"

# 检查 Python 版本
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python 版本: $PYTHON_VERSION"

# 检查必要目录
echo "📁 检查目录结构..."
mkdir -p ~/.shared-memory/hermes/{to_openclaw,from_openclaw,processed,logs}
mkdir -p ~/.shared-memory/openclaw/{to_hermes,from_hermes,processed,logs}
mkdir -p ~/.shared-memory/backups

echo "✓ 共享文件夹目录创建完成"

# 检查 Hermes 记忆目录
if [ ! -d ~/.hermes/memories ]; then
    echo "⚠️ Hermes 记忆目录不存在: ~/.hermes/memories"
    echo "   请确保 Hermes Agent 已正确安装"
else
    echo "✓ Hermes 记忆目录存在"
fi

# 检查 OpenClaw 数据库
if [ ! -f ~/.openclaw/memory/main.sqlite ]; then
    echo "⚠️ OpenClaw 数据库不存在: ~/.openclaw/memory/main.sqlite"
    echo "   请确保 OpenClaw 已正确安装并初始化"
else
    echo "✓ OpenClaw 数据库存在"
fi

# 安装 Python 依赖
echo "📦 检查 Python 依赖..."
REQUIRED_PACKAGES=("sqlite3")

for package in "${REQUIRED_PACKAGES[@]}"; do
    if python3 -c "import $package" 2>/dev/null; then
        echo "✓ $package 已安装"
    else
        echo "⚠️ $package 未安装，尝试安装..."
        pip3 install $package || echo "❌ 安装 $package 失败，请手动安装"
    fi
done

# 设置执行权限
echo "🔧 设置执行权限..."
chmod +x ~/.hermes/skills/openclaw-imports/memory-plus-sync/shared_memory_cli.py

# 创建符号链接（可选）
echo "🔗 创建命令行快捷方式..."
if [ ! -f /usr/local/bin/shared-memory-sync ]; then
    sudo ln -sf ~/.hermes/skills/openclaw-imports/memory-plus-sync/shared_memory_cli.py /usr/local/bin/shared-memory-sync 2>/dev/null || \
    echo "⚠️ 无法创建系统级符号链接，使用本地别名"
    
    # 创建本地别名
    echo "alias shared-memory-sync='python3 ~/.hermes/skills/openclaw-imports/memory-plus-sync/shared_memory_cli.py'" >> ~/.bashrc 2>/dev/null || true
    echo "alias shared-memory-sync='python3 ~/.hermes/skills/openclaw-imports/memory-plus-sync/shared_memory_cli.py'" >> ~/.zshrc 2>/dev/null || true
fi

# 创建定时任务配置
echo "⏰ 创建定时任务配置..."
CRON_CONFIG="# 共享记忆同步系统定时任务
# 每小时同步一次
0 * * * * cd ~/.hermes/skills/openclaw-imports/memory-plus-sync && python3 shared_memory_cli.py sync-bidirectional
# 每天凌晨2点清理记忆
0 2 * * * cd ~/.hermes/skills/openclaw-imports/memory-plus-sync && python3 shared_memory_cli.py cleanup
# 每周日凌晨3点完整工作流
0 3 * * 0 cd ~/.hermes/skills/openclaw-imports/memory-plus-sync && python3 shared_memory_cli.py full-workflow"

echo "$CRON_CONFIG" > ~/.shared-memory/cron_config.txt
echo "✓ 定时任务配置已保存到 ~/.shared-memory/cron_config.txt"

# 测试系统
echo "🧪 测试系统功能..."
cd ~/.hermes/skills/openclaw-imports/memory-plus-sync

echo "1. 测试 Hermes 记忆导出..."
python3 -c "
from hermes_exporter import HermesMemoryExporter
exporter = HermesMemoryExporter()
memories = exporter.read_memory_md()
print(f'✓ 读取到 {len(memories[\"system_memories\"])} 条系统记忆')
"

echo "2. 测试共享文件夹状态..."
python3 -c "
from shared_memory_controller import SharedMemoryController
controller = SharedMemoryController()
status = controller.get_status()
print(f'✓ 系统状态检查完成')
print(f'  待处理文件: {status[\"shared_folder\"][\"hermes_to_openclaw\"]}')
"

echo "3. 测试命令行接口..."
python3 shared_memory_cli.py status --min-importance 7 | grep -q "timestamp" && echo "✓ 命令行接口工作正常"

echo ""
echo "======================================"
echo "🎉 安装完成！"
echo ""
echo "使用方法："
echo "1. 手动同步: shared-memory-sync sync-bidirectional"
echo "2. 清理记忆: shared-memory-sync cleanup"
echo "3. 完整工作流: shared-memory-sync full-workflow"
echo "4. 查看状态: shared-memory-sync status"
echo ""
echo "定时任务配置已保存到 ~/.shared-memory/cron_config.txt"
echo "请根据需要添加到 crontab: crontab -e"
echo ""
echo "共享文件夹位置: ~/.shared-memory/"
echo "日志文件位置: ~/.shared-memory/{hermes,openclaw}/logs/"
echo "备份文件位置: ~/.shared-memory/backups/"
echo "======================================"