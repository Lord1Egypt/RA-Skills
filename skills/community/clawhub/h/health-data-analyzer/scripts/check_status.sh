#!/bin/bash
# 健康数据服务器状态检查脚本

echo "=== 健康数据分析器状态检查 ==="
echo

# 检查 mcporter 是否可用
echo "1. 检查 mcporter 工具..."
if command -v mcporter &> /dev/null; then
    echo "✅ mcporter 已安装"
    mcporter --version
else
    echo "❌ mcporter 未安装或不在 PATH 中"
    exit 1
fi

echo

# 检查 MCP 服务器状态
echo "2. 检查 MCP 服务器状态..."
mcporter list | grep -E "(healthdata|sleep_health_data)"

echo

# 检查 healthdata 服务器连接
echo "3. 测试 healthdata 服务器连接..."
if mcporter call healthdata.list_available_tables &> /dev/null; then
    echo "✅ healthdata 服务器连接正常"
    
    # 显示可用表数量
    table_count=$(mcporter call healthdata.list_available_tables | jq '. | length' 2>/dev/null || echo "未知")
    echo "📊 可用数据表数量: $table_count"
else
    echo "❌ healthdata 服务器连接失败"
    echo "请检查服务器是否运行在 http://0.0.0.0:8003/mcp/sse"
fi

echo

# 检查 Python 环境
echo "4. 检查 Python 环境..."
if command -v python3 &> /dev/null; then
    echo "✅ Python3 已安装"
    python3 --version
else
    echo "❌ Python3 未安装"
fi

echo

# 测试基础查询功能
echo "5. 测试基础查询功能..."
echo "正在执行: mcporter call healthdata.list_available_tables"

if mcporter call healthdata.list_available_tables > /tmp/health_test.json 2>/dev/null; then
    echo "✅ 基础查询功能正常"
    
    # 显示前3个表名
    if command -v jq &> /dev/null; then
        echo "前3个数据表:"
        jq -r '.[0:3][].name' /tmp/health_test.json 2>/dev/null | sed 's/^/  - /'
    fi
    
    rm -f /tmp/health_test.json
else
    echo "❌ 基础查询功能异常"
fi

echo

# 检查技能脚本
echo "6. 检查技能脚本..."
script_path="$(dirname "$0")/health_analyzer.py"
if [ -f "$script_path" ]; then
    echo "✅ health_analyzer.py 脚本存在"
    if [ -x "$script_path" ]; then
        echo "✅ 脚本具有执行权限"
    else
        echo "⚠️  脚本缺少执行权限，正在修复..."
        chmod +x "$script_path"
    fi
else
    echo "❌ health_analyzer.py 脚本不存在"
fi

echo

echo "=== 状态检查完成 ==="
echo "如果所有检查都通过，健康数据分析器已准备就绪！"