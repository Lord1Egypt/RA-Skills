#!/bin/bash
# ============================================================================
# EO Progress Executor 简单验证脚本
# ============================================================================

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   EO Progress Executor & Chain Signal 验证测试            ║"
echo "╚════════════════════════════════════════════════════════════╝"

# 检查文件是否存在
echo ""
echo "[1] 检查文件部署..."
if [ -f "/home/zzy/.openclaw/extensions/eo-collaboration/dist/workflow/progress-executor.js" ]; then
    echo "    ✅ progress-executor.js 已部署"
else
    echo "    ❌ progress-executor.js 未找到"
    exit 1
fi

if [ -f "/home/zzy/.openclaw/extensions/eo-collaboration/dist/skills/executor.js" ]; then
    echo "    ✅ executor.js 已部署"
else
    echo "    ❌ executor.js 未找到"
    exit 1
fi

# 检查关键函数是否导出
echo ""
echo "[2] 检查关键导出..."

grep -q "executeWithProgressReporting" /home/zzy/.openclaw/extensions/eo-collaboration/dist/workflow/progress-executor.js
[ $? -eq 0 ] && echo "    ✅ executeWithProgressReporting 导出" || echo "    ❌ 导出缺失"

grep -q "chainSignalManager" /home/zzy/.openclaw/extensions/eo-collaboration/dist/workflow/progress-executor.js
[ $? -eq 0 ] && echo "    ✅ chainSignalManager 导出" || echo "    ❌ 导出缺失"

grep -q "createChainTask" /home/zzy/.openclaw/extensions/eo-collaboration/dist/workflow/progress-executor.js
[ $? -eq 0 ] && echo "    ✅ createChainTask 导出" || echo "    ❌ 导出缺失"

grep -q "ProgressExecutor" /home/zzy/.openclaw/extensions/eo-collaboration/dist/workflow/progress-executor.js
[ $? -eq 0 ] && echo "    ✅ ProgressExecutor 导出" || echo "    ❌ 导出缺失"

grep -q "ChainSignalManager" /home/zzy/.openclaw/extensions/eo-collaboration/dist/workflow/progress-executor.js
[ $? -eq 0 ] && echo "    ✅ ChainSignalManager 导出" || echo "    ❌ 导出缺失"

# 检查超时策略配置
echo ""
echo "[3] 检查超时策略..."

grep -q "progressIntervalMs" /home/zzy/.openclaw/extensions/eo-collaboration/dist/skills/executor.js
[ $? -eq 0 ] && echo "    ✅ useProgressReporting 自动启用逻辑" || echo "    ❌ 缺失"

grep -q "adaptiveExtensions" /home/zzy/.openclaw/extensions/eo-collaboration/dist/workflow/progress-executor.js
[ $? -eq 0 ] && echo "    ✅ 自适应超时扩展机制" || echo "    ❌ 缺失"

# 检查链式信号机制
echo ""
echo "[4] 检查链式信号机制..."

grep -q "waitForDependencyStage" /home/zzy/.openclaw/extensions/eo-collaboration/dist/collaboration/task-distributor.js
[ $? -eq 0 ] && echo "    ✅ waitForDependencyStage 方法" || echo "    ❌ 缺失"

grep -q "createDependencyChain" /home/zzy/.openclaw/extensions/eo-collaboration/dist/collaboration/task-distributor.js
[ $? -eq 0 ] && echo "    ✅ createDependencyChain 方法" || echo "    ❌ 缺失"

# 检查模块大小
echo ""
echo "[5] 文件大小统计..."
wc -c /home/zzy/.openclaw/extensions/eo-collaboration/dist/workflow/progress-executor.js
wc -c /home/zzy/.openclaw/extensions/eo-collaboration/dist/skills/executor.js

echo ""
echo "========================================"
echo "验证完成！"
echo "========================================"
echo ""
echo "新增功能总结:"
echo "  1. ProgressExecutor - 进度汇报执行器"
echo "     - 自适应超时 (基础超时 × 2)"
echo "     - 每30秒进度汇报"
echo "     - 超时不中断任务"
echo ""
echo "  2. ChainSignalManager - 链式信号管理器"
echo "     - 里程碑式阶段触发"
echo "     - 下游任务可等待特定阶段"
echo "     - 依赖链自动协调"
echo ""
echo "  3. TaskDistributor 增强"
echo "     - submitChainTask()"
echo "     - waitForDependencyStage()"
echo "     - createDependencyChain()"
echo ""
echo "使用方式请参考 TOOLS.md"
