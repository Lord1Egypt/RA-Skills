#!/bin/sh
# J6B泊车日志批量下载脚本
# 用法: ./download_log.sh [选项] [模块名...]
# 示例:
#   ./download_log.sh                    # 下载所有模块日志
#   ./download_log.sh planning           # 下载planning模块日志
#   ./download_log.sh planning od rd     # 下载多个模块日志
#   ./download_log.sh -a                 # 打包下载所有日志
#   ./download_log.sh -o /tmp/logs       # 指定本地保存目录
#   ./download_log.sh -c 192.168.2.10    # 指定板端IP（百兆网口）

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 默认配置
REMOTE_IP="192.168.1.10"
REMOTE_USER="root"
REMOTE_LOG_DIR="/app/apa/log"
REMOTE_COREDUMP_DIR="/log/coredump"
LOCAL_DIR="./j6b_logs"
ARCHIVE_MODE=false

# 支持的模块列表
ALL_MODULES="dr loc sensorcenter image_preprocess od rd psd gridmap planning ui_control perception_fusion"

# 帮助信息
show_help() {
    echo -e "${CYAN}══════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}        J6B泊车日志批量下载脚本 v1.0${NC}"
    echo -e "${CYAN}══════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "用法: $0 [选项] [模块名...]"
    echo ""
    echo "选项:"
    echo "  -a          打包模式（先在板端打包再下载）"
    echo "  -c <IP>     指定板端IP（默认: 192.168.1.10）"
    echo "  -o <目录>   指定本地保存目录（默认: ./j6b_logs）"
    echo "  -h          显示帮助信息"
    echo ""
    echo "支持的模块:"
    echo "  dr loc sensorcenter image_preprocess od rd"
    echo "  psd gridmap planning ui_control perception_fusion"
    echo ""
    echo "示例:"
    echo "  $0                              # 下载所有模块日志"
    echo "  $0 planning                     # 下载planning模块日志"
    echo "  $0 -a                           # 打包下载所有日志"
    echo "  $0 -c 192.168.2.10 planning     # 通过百兆网口下载"
    echo ""
}

# 解析参数
MODULES=""
while [ $# -gt 0 ]; do
    case "$1" in
        -a) ARCHIVE_MODE=true; shift ;;
        -c) REMOTE_IP="$2"; shift 2 ;;
        -o) LOCAL_DIR="$2"; shift 2 ;;
        -h) show_help; exit 0 ;;
        -*) echo -e "${RED}未知选项: $1${NC}"; show_help; exit 1 ;;
        *) MODULES="$MODULES $1"; shift ;;
    esac
done

# 如果没有指定模块，则下载所有模块
if [ -z "$MODULES" ]; then
    MODULES="$ALL_MODULES"
fi

# 创建本地目录
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
SAVE_DIR="${LOCAL_DIR}/${TIMESTAMP}"
mkdir -p "$SAVE_DIR"

# 打印配置
echo -e "${CYAN}══════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}        J6B泊车日志批量下载${NC}"
echo -e "${CYAN}══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}【配置信息】${NC}"
echo "  板端地址: ${REMOTE_USER}@${REMOTE_IP}"
echo "  日志路径: ${REMOTE_LOG_DIR}"
echo "  保存目录: ${SAVE_DIR}"
echo "  下载模块: ${MODULES}"
echo "  打包模式: ${ARCHIVE_MODE}"
echo ""

# 测试连接
echo -e "${YELLOW}【测试连接】${NC}"
if ! ssh -o ConnectTimeout=5 ${REMOTE_USER}@${REMOTE_IP} "echo ok" > /dev/null 2>&1; then
    echo -e "${RED}  ✗ 无法连接到 ${REMOTE_USER}@${REMOTE_IP}${NC}"
    echo -e "${YELLOW}  请检查:${NC}"
    echo "    1. 网络是否连通 (ping ${REMOTE_IP})"
    echo "    2. SSH服务是否运行"
    exit 1
fi
echo -e "${GREEN}  ✓ 连接成功${NC}"
echo ""

# 打包模式下载
if [ "$ARCHIVE_MODE" = true ]; then
    echo -e "${YELLOW}【打包模式下载】${NC}"
    
    ARCHIVE_NAME="j6b_logs_${TIMESTAMP}.tar.gz"
    REMOTE_ARCHIVE="/tmp/${ARCHIVE_NAME}"
    
    echo -e "${BLUE}  1/4 在板端打包日志...${NC}"
    ssh ${REMOTE_USER}@${REMOTE_IP} "tar czf ${REMOTE_ARCHIVE} -C ${REMOTE_LOG_DIR} ."
    
    echo -e "${BLUE}  2/4 下载压缩包...${NC}"
    scp ${REMOTE_USER}@${REMOTE_IP}:${REMOTE_ARCHIVE} "${SAVE_DIR}/"
    
    echo -e "${BLUE}  3/4 解压日志文件...${NC}"
    cd "${SAVE_DIR}" && tar xzf "${ARCHIVE_NAME}" && rm -f "${ARCHIVE_NAME}"
    
    echo -e "${BLUE}  4/4 清理板端临时文件...${NC}"
    ssh ${REMOTE_USER}@${REMOTE_IP} "rm -f ${REMOTE_ARCHIVE}"
    
    echo -e "${GREEN}  ✓ 打包下载完成${NC}"
else
    # 逐模块下载
    SUCCESS=0
    FAIL=0
    TOTAL=$(echo $MODULES | wc -w)
    CURRENT=0
    
    for module in $MODULES; do
        CURRENT=$((CURRENT + 1))
        echo -e "${YELLOW}【${CURRENT}/${TOTAL}】下载 ${module} 模块日志...${NC}"
        
        if ssh ${REMOTE_USER}@${REMOTE_IP} "test -d ${REMOTE_LOG_DIR}/${module}" > /dev/null 2>&1; then
            mkdir -p "${SAVE_DIR}/${module}"
            scp -r ${REMOTE_USER}@${REMOTE_IP}:${REMOTE_LOG_DIR}/${module}/* "${SAVE_DIR}/${module}/" 2>/dev/null
            
            if [ $? -eq 0 ]; then
                FILE_COUNT=$(ls "${SAVE_DIR}/${module}/" 2>/dev/null | wc -l)
                TOTAL_SIZE=$(du -sh "${SAVE_DIR}/${module}/" 2>/dev/null | cut -f1)
                echo -e "${GREEN}  ✓ ${module}: ${FILE_COUNT} 个文件, ${TOTAL_SIZE}${NC}"
                SUCCESS=$((SUCCESS + 1))
            else
                echo -e "${RED}  ✗ ${module}: 下载失败${NC}"
                FAIL=$((FAIL + 1))
            fi
        else
            echo -e "${YELLOW}  ⚠ ${module}: 远程目录不存在${NC}"
            FAIL=$((FAIL + 1))
        fi
    done
    
    echo ""
    echo -e "${YELLOW}【下载摘要】${NC}"
    echo "  成功: ${SUCCESS}/${TOTAL}"
    echo "  失败: ${FAIL}/${TOTAL}"
fi

# 下载摘要
echo ""
echo -e "${CYAN}══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}下载完成！${NC}"
echo -e "${CYAN}══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}【保存位置】${NC} ${SAVE_DIR}"
echo -e "${BLUE}【总大小】${NC}   $(du -sh "${SAVE_DIR}" | cut -f1)"
echo -e "${BLUE}【文件数】${NC}   $(find "${SAVE_DIR}" -type f | wc -l)"
