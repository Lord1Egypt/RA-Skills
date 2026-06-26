#!/bin/bash
# OpenClaw Optimize - 命令行工具
# 性能优化脚本

set -e

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 显示帮助
show_help() {
    echo -e "${BLUE}OpenClaw Optimize${NC} - 性能优化工具"
    echo ""
    echo "用法:"
    echo "  openclaw-optimize [命令] [选项]"
    echo ""
    echo "命令:"
    echo "  --full              执行完整优化"
    echo "  --memory            仅优化内存"
    echo "  --skills            优化技能加载"
    echo "  --clean-history     清理历史记录"
    echo "  --diagnose          诊断系统问题"
    echo "  --monitor           监控性能"
    echo "  --report            生成报告"
    echo "  --help              显示帮助"
    echo ""
    echo "示例:"
    echo "  openclaw-optimize --full"
    echo "  openclaw-optimize --memory"
    echo "  openclaw-optimize --diagnose"
}

# 检查依赖
check_deps() {
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}✗ 需要 Python3${NC}"
        exit 1
    fi
    
    if ! python3 -c "import psutil" 2>/dev/null; then
        echo -e "${YELLOW}⚠ 安装依赖: pip install psutil${NC}"
        pip install psutil -q
    fi
}

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 运行 Python 优化
run_optimize() {
    python3 "$SCRIPT_DIR/openclaw_optimize.py"
}

# 内存优化
cmd_memory() {
    echo -e "${BLUE}🧠 内存优化${NC}"
    echo "------------------------"
    
    # 显示当前状态
    echo "当前内存状态:"
    python3 -c "
from openclaw_optimize import MemoryOptimizer
m = MemoryOptimizer()
status = m.get_status()
print(f\"  系统内存: {status['system_percent']}% 已用\")
print(f\"  进程内存: {status['process_rss']}\")
"
    
    # 强制垃圾回收
    echo ""
    echo "执行垃圾回收..."
    python3 -c "
from openclaw_optimize import MemoryOptimizer
m = MemoryOptimizer()
result = m.force_gc()
if result['success']:
    print(f\"  ✓ 释放内存: {result['freed_human']}\")
else:
    print(f\"  ℹ 无需释放\")
"
    
    echo ""
    echo -e "${GREEN}✓ 内存优化完成${NC}"
}

# 技能优化
cmd_skills() {
    echo -e "${BLUE}🚀 技能优化${NC}"
    echo "------------------------"
    
    python3 -c "
from openclaw_optimize import SkillOptimizer
opt = SkillOptimizer()

# 分析技能
print('技能加载时间分析:')
skills = opt.analyze_load_time()
for skill in skills[:5]:
    print(f\"  {skill['name']}: {skill['size_human']} (约{skill['estimated_load_time']})\")

# 优化建议
print('')
print('优化建议:')
suggestions = opt.get_optimization_suggestions()
if suggestions:
    for s in suggestions:
        print(f\"  ⚠ {s}\")
else:
    print('  ✓ 技能状态良好')
"
    
    echo ""
    echo -e "${GREEN}✓ 技能分析完成${NC}"
}

# 清理历史
cmd_clean_history() {
    echo -e "${BLUE}🧹 清理历史记录${NC}"
    echo "------------------------"
    
    # 显示当前大小
    echo "当前历史记录:"
    python3 -c "
from openclaw_optimize import HistoryOptimizer
opt = HistoryOptimizer()
size = opt.get_size()
print(f\"  文件数: {size['memory_files']}\")
print(f\"  内存文件: {size['memory_size']}\")
print(f\"  向量数据库: {size['vector_db_size']}\")
print(f\"  总计: {size['total_size']}\")
"
    
    # 清理
    echo ""
    echo "清理3天前的记录..."
    python3 -c "
from openclaw_optimize import HistoryOptimizer
opt = HistoryOptimizer()
result = opt.clean_old(days=3)
print(f\"  ✓ 清理文件: {result['cleaned_files']} 个\")
print(f\"  ✓ 释放空间: {result['freed']}\")
"
    
    echo ""
    echo -e "${GREEN}✓ 历史记录清理完成${NC}"
}

# 诊断
cmd_diagnose() {
    echo -e "${BLUE}🔍 系统诊断${NC}"
    echo "------------------------"
    
    python3 -c "
from openclaw_optimize import OpenClawOptimizer
opt = OpenClawOptimizer()
diagnosis = opt.diagnose()

print(f\"发现问题: {diagnosis['issue_count']} 个\")
print('')

if diagnosis['issues']:
    for issue in diagnosis['issues']:
        icon = '🔴' if issue['severity'] == 'high' else ('🟡' if issue['severity'] == 'medium' else '🔵')
        print(f\"{icon} [{issue['severity'].upper()}] {issue['message']}\")
else:
    print('✓ 系统状态良好，未发现明显问题')

print('')
print(f\"建议: {diagnosis['recommendation']}\")
"
}

# 监控
cmd_monitor() {
    echo -e "${BLUE}📊 性能监控${NC}"
    echo "------------------------"
    echo "监控60秒，按 Ctrl+C 停止..."
    echo ""
    
    python3 -c "
from openclaw_optimize import PerformanceMonitor
monitor = PerformanceMonitor()
try:
    monitor.start_monitoring(duration=60)
    report = monitor.generate_report()
    
    print('')
    print('监控报告:')
    print(f\"  持续时间: {report['duration']} 秒\")
    print(f\"  CPU 平均: {report['cpu_avg']:.1f}%\")
    print(f\"  CPU 峰值: {report['cpu_max']:.1f}%\")
    print(f\"  内存平均: {report['memory_avg']:.1f}%\")
    print(f\"  内存峰值: {report['memory_max']:.1f}%\")
    print(f\"  状态: {report['status']}\")
except KeyboardInterrupt:
    print('')
    print('监控已停止')
"
}

# 完整优化
cmd_full() {
    echo -e "${BLUE}⚡ 执行完整优化${NC}"
    echo "================================"
    echo ""
    
    cmd_diagnose
    echo ""
    
    cmd_memory
    echo ""
    
    cmd_clean_history
    echo ""
    
    cmd_skills
    echo ""
    
    echo "================================"
    echo -e "${GREEN}🎉 完整优化完成！${NC}"
    echo ""
    echo "建议: 重启 OpenClaw Gateway 以应用所有优化"
    echo "  openclaw gateway restart"
}

# 生成报告
cmd_report() {
    echo -e "${BLUE}📈 生成优化报告${NC}"
    echo "------------------------"
    
    REPORT_FILE="/tmp/openclaw-optimize-report-$(date +%Y%m%d-%H%M%S).txt"
    
    {
        echo "OpenClaw 优化报告"
        echo "生成时间: $(date)"
        echo "================================"
        echo ""
        
        echo "【系统诊断】"
        python3 -c "
from openclaw_optimize import OpenClawOptimizer
opt = OpenClawOptimizer()
diagnosis = opt.diagnose()
print(f\"问题数量: {diagnosis['issue_count']}\")
for issue in diagnosis['issues']:
    print(f\"- [{issue['severity']}] {issue['message']}\")
"
        echo ""
        
        echo "【内存状态】"
        python3 -c "
from openclaw_optimize import MemoryOptimizer
m = MemoryOptimizer()
status = m.get_status()
print(f\"系统内存使用率: {status['system_percent']}%\")
print(f\"进程内存占用: {status['process_rss']}\")
"
        echo ""
        
        echo "【技能分析】"
        python3 -c "
from openclaw_optimize import SkillOptimizer
opt = SkillOptimizer()
skills = opt.analyze_load_time()
print(f\"技能总数: {len(skills)}\")
print('加载时间最长的5个技能:')
for skill in skills[:5]:
    print(f\"  - {skill['name']}: {skill['size_human']}\")
"
        echo ""
        
        echo "【历史记录】"
        python3 -c "
from openclaw_optimize import HistoryOptimizer
opt = HistoryOptimizer()
size = opt.get_size()
print(f\"总大小: {size['total_size']}\")
print(f\"内存文件: {size['memory_files']} 个\")
"
        
    } > "$REPORT_FILE"
    
    echo -e "${GREEN}✓ 报告已生成: $REPORT_FILE${NC}"
    echo ""
    cat "$REPORT_FILE"
}

# 主命令分发
case "${1:-}" in
    --full)
        check_deps
        cmd_full
        ;;
    --memory)
        check_deps
        cmd_memory
        ;;
    --skills)
        check_deps
        cmd_skills
        ;;
    --clean-history)
        check_deps
        cmd_clean_history
        ;;
    --diagnose)
        check_deps
        cmd_diagnose
        ;;
    --monitor)
        check_deps
        cmd_monitor
        ;;
    --report)
        check_deps
        cmd_report
        ;;
    --help|-h|help)
        show_help
        ;;
    *)
        show_help
        ;;
esac
