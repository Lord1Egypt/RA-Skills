#!/bin/bash
# Process Flow Navigator CLI
# 业务流程导航命令行工具

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_FILE="$SCRIPT_DIR/../data/flow-rules.json"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

show_help() {
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${BLUE}   Process Flow Navigator - 流程导航助手${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
    echo "用法：$0 <命令> [参数]"
    echo ""
    echo "命令:"
    echo "  next <节点>        查询下一步去向"
    echo "  path <起点> <终点>  规划从起点到终点的路径"
    echo "  code <节点>        查询节点的技能编码"
    echo "  list               列出所有节点"
    echo "  tree <分支>        显示分支结构"
    echo "  help               显示帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 next B"
    echo "  $0 path B 结束"
    echo "  $0 code C"
    echo "  $0 tree C"
}

get_node_code() {
    local node=$1
    if [ -f "$DATA_FILE" ]; then
        python3 -c "
import json
with open('$DATA_FILE') as f:
    data = json.load(f)
node = '$node'
if node in data['nodes']:
    n = data['nodes'][node]
    print(f\"校验：{n.get('check', 'N/A')}\")
    print(f\"执行：{n.get('exec', 'N/A')}\")
    print(f\"下一步：{n.get('next', 'N/A')}\")
else:
    print(f'节点 {node} 未找到')
"
    else
        echo -e "${RED}数据文件未找到${NC}"
    fi
}

get_next_step() {
    local node=$1
    echo -e "${GREEN}当前节点：${node}${NC}"
    echo ""
    
    case $node in
        "A")
            echo "下一步：A-1"
            echo "技能编码：PROC-A-EXEC-001"
            ;;
        "A-1")
            echo "下一步：最终判断"
            echo "  - [是] → 结束"
            echo "  - [否] → 流程 B"
            ;;
        "B")
            echo "下一步：判断 2"
            echo "  - [是] → 流程 C"
            echo "  - [否] → 流程 B-1"
            ;;
        "B-1")
            echo "下一步：B-2"
            ;;
        "B-2")
            echo "下一步：最终判断"
            echo "  - [是] → 结束"
            echo "  - [否] → 流程 C"
            ;;
        "C")
            echo "下一步：判断 3"
            echo "  - [是] → 流程 C-1"
            echo "  - [否] → 流程 C-3"
            ;;
        "C-1")
            echo "下一步：最终判断"
            echo "  - [是] → 结束"
            echo "  - [否] → 判断 4"
            ;;
        "C-2"|"C-3")
            echo "下一步：C-4"
            ;;
        "C-4")
            echo "下一步：最终判断"
            echo "  - [是] → 结束"
            echo "  - [否] → 判断 5"
            ;;
        "C-5")
            echo "下一步：最终判断"
            echo "  - [是] → 结束"
            echo "  - [否] → 流程 D"
            ;;
        "D")
            echo "下一步：判断 6"
            echo "  - [是] → 流程 E"
            echo "  - [否] → 流程 D-1"
            ;;
        "D-1")
            echo "下一步：最终判断"
            echo "  - [是] → 结束"
            echo "  - [否] → 流程 E"
            ;;
        "E")
            echo "下一步：判断 7"
            echo "  - [报错] → 流程 F"
            echo "  - [乱码] → 售后"
            ;;
        "F")
            echo "下一步：流程 G"
            ;;
        "G")
            echo "下一步：判断 8"
            echo "  - [是] → 最终判断"
            echo "  - [否] → 售后"
            ;;
        "H"|"I"|"J")
            echo "下一步：$(echo $node | tr 'HIJ' 'IJK')"
            ;;
        "K")
            echo "下一步：收尾"
            ;;
        *)
            echo -e "${RED}未知节点：$node${NC}"
            echo "使用 'list' 命令查看所有节点"
            ;;
    esac
}

list_nodes() {
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${BLUE}   所有流程节点${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
    echo "主流程：A → B → C → D → E → F → G → H → I → J → K"
    echo ""
    echo "子流程:"
    echo "  A-1"
    echo "  B-1, B-2"
    echo "  C-1, C-2, C-3, C-4, C-5"
    echo "  D-1"
    echo ""
    echo "判断节点:"
    echo "  判断 2, 判断 3, 判断 4, 判断 5"
    echo "  判断 6, 判断 7, 判断 8, 判断 9"
    echo "  最终判断"
    echo ""
    echo "终点:"
    echo "  结束，售后"
}

show_tree() {
    local branch=$1
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${BLUE}   ${branch} 分支流程结构${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
    
    case $branch in
        "A"|"a")
            echo "流程 A → A-1 → 最终判断"
            echo "                  ├─ [是] → 结束"
            echo "                  └─ [否] → 流程 B"
            ;;
        "B"|"b")
            echo "流程 B → 判断 2"
            echo "            ├─ [是] → 流程 C"
            echo "            └─ [否] → B-1 → B-2 → 最终判断"
            echo "                                 ├─ [是] → 结束"
            echo "                                 └─ [否] → 流程 C"
            ;;
        "C"|"c")
            echo "流程 C → 判断 3"
            echo "            ├─ [是] → C-1 → 最终判断"
            echo "            │            ├─ [是] → 结束"
            echo "            │            └─ [否] → 判断 4 → C-2 → C-3 → C-4 → 最终判断"
            echo "            │                                                    ├─ [是] → 结束"
            echo "            │                                                    └─ [否] → 判断 5"
            echo "            │"
            echo "            └─ [否] → C-3 → C-4 → 最终判断"
            echo "                             ├─ [是] → 结束"
            echo "                             └─ [否] → 判断 5"
            echo ""
            echo "判断 5"
            echo "  ├─ [是] → 流程 D"
            echo "  └─ [否] → C-5 → 最终判断"
            echo "               ├─ [是] → 结束"
            echo "               └─ [否] → 流程 D"
            ;;
        "D"|"d")
            echo "流程 D → 判断 6"
            echo "            ├─ [是] → 流程 E"
            echo "            └─ [否] → D-1 → 最终判断"
            echo "                         ├─ [是] → 结束"
            echo "                         └─ [否] → 流程 E"
            ;;
        "E"|"e")
            echo "流程 E → 判断 7"
            echo "            ├─ [报错] → 流程 F → 流程 G → 判断 8"
            echo "            │                        ├─ [是] → 最终判断"
            echo "            │                        │         ├─ [是] → 结束"
            echo "            │                        │         └─ [否] → 流程 H"
            echo "            │                        │"
            echo "            │                        └─ [否] → 售后"
            echo "            │"
            echo "            └─ [乱码] → 售后"
            ;;
        *)
            echo -e "${RED}未知分支：$branch${NC}"
            echo "可用分支：A, B, C, D, E"
            ;;
    esac
}

# 主程序
case $1 in
    "next")
        get_next_step "$2"
        ;;
    "path")
        echo -e "${YELLOW}路径规划：$2 → $3${NC}"
        echo ""
        echo "提示：请使用 interactive 模式或咨询 AI 助手获取详细路径规划"
        ;;
    "code")
        get_node_code "$2"
        ;;
    "list")
        list_nodes
        ;;
    "tree")
        show_tree "$2"
        ;;
    "help"|"-h"|"--help"|"")
        show_help
        ;;
    *)
        echo -e "${RED}未知命令：$1${NC}"
        echo "使用 '$0 help' 查看帮助"
        exit 1
        ;;
esac
