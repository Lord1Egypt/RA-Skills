#!/bin/bash
# ============================================================
# 九歌完美版音频处理流水线 - Jiuge Flow Perfect V1
# 基于2026-05-01 21:47《敬兄弟》no-wash完美经验封装
# 核心流程：01_Sep → 03_Dry → 04_Master（默认跳过洗声）
# ============================================================

set -e

# 配置环境
export PATH="/Users/imacaudio/miniconda3/envs/uvr_auto/bin:$PATH"
PYTHON="/Users/imacaudio/miniconda3/envs/uvr_auto/bin/python"
AUDIO_SEPARATOR="/Users/imacaudio/miniconda3/envs/uvr_auto/bin/audio-separator"
FFMPEG="/Users/imacaudio/miniconda3/envs/uvr_auto/bin/ffmpeg"

# 参数解析
INPUT_FILE="$1"
MODE="${2:-1}"
WASH_MODE="${3:-no-wash}"

# 路径配置
INPUT_DIR="$HOME/Desktop/Jiuge_Input"
OUTPUT_BASE="$HOME/Desktop/Jiuge_Audio_Projects"
TIMESTAMP=$(date +%m%d_%H%M)
PROJECT_NAME="${INPUT_FILE%.*}_${TIMESTAMP}"
PROJECT_DIR="${OUTPUT_BASE}/${PROJECT_NAME}"

# 模型路径
MDX_MODEL_DIR="/Applications/Ultimate Vocal Remover.app/Contents/Resources/models/MDX_Net_Models"
VR_MODEL_DIR="/Applications/Ultimate Vocal Remover.app/Contents/Resources/models/VR_Models"

# 分离模型
SEP_MODEL="Kim_Vocal_2.onnx"
DRY_MODEL="UVR-De-Echo-Aggressive.pth"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 日志函数
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 检查依赖
check_deps() {
    log_info "检查环境依赖..."
    
    if [ ! -f "$AUDIO_SEPARATOR" ]; then
        log_error "audio-separator 未找到: $AUDIO_SEPARATOR"
        exit 1
    fi
    
    if [ ! -f "$FFMPEG" ]; then
        log_error "ffmpeg 未找到: $FFMPEG"
        exit 1
    fi
    
    if [ ! -f "${INPUT_DIR}/${INPUT_FILE}" ]; then
        log_error "输入文件不存在: ${INPUT_DIR}/${INPUT_FILE}"
        exit 1
    fi
    
    log_success "环境检查通过"
}

# 创建项目目录
setup_project() {
    log_info "创建项目目录: ${PROJECT_NAME}"
    mkdir -p "${PROJECT_DIR}"/{01_Sep,02_Wash,03_Dry,04_Master}
    log_success "项目目录创建完成"
}

# 第一步：人声分离
step_01_separate() {
    log_info "步骤1/3: 人声分离 (Kim_Vocal_2.onnx)..."
    
    cd "${INPUT_DIR}"
    
    $AUDIO_SEPARATOR "$INPUT_FILE" \
        --model_filename "$SEP_MODEL" \
        --model_file_dir "$MDX_MODEL_DIR" \
        --output_dir "${PROJECT_DIR}/01_Sep" \
        --output_format wav
    
    # 检查输出
    if [ ! -f "${PROJECT_DIR}/01_Sep/${INPUT_FILE%.*}_(Vocals)_${SEP_MODEL%.onnx}.wav" ]; then
        log_error "分离失败，未找到人声文件"
        exit 1
    fi
    
    log_success "人声分离完成"
}

# 第二步：洗声（可选）
step_02_wash() {
    if [ "$WASH_MODE" = "no-wash" ]; then
        log_warn "跳过洗声步骤 (no-wash模式)"
        return 0
    fi
    
    log_info "步骤2/4: 洗声处理 (背景合唱分离)..."
    
    cd "${PROJECT_DIR}/01_Sep"
    
    # 获取人声文件名
    VOCALS_FILE=$(ls *_"(Vocals)_"*.wav | head -1)
    
    if [ -z "$VOCALS_FILE" ]; then
        log_error "未找到人声文件，无法洗声"
        exit 1
    fi
    
    # 使用 MDX-Net 模型进行背景合唱分离
    # 模型：UVR_MDXNET_KARA_2.onnx 专门用于分离主唱和背景合唱
    WASH_MODEL="UVR_MDXNET_KARA_2.onnx"
    WASH_MODEL_DIR="/Applications/Ultimate Vocal Remover.app/Contents/Resources/models/MDX_Net_Models"
    
    if [ ! -f "${WASH_MODEL_DIR}/${WASH_MODEL}" ]; then
        log_warn "洗声模型 ${WASH_MODEL} 未找到，使用默认人声作为洗声结果"
        # 复制原始人声到洗声目录
        cp "$VOCALS_FILE" "${PROJECT_DIR}/02_Wash/"
        log_success "洗声完成（使用原始人声）"
        return 0
    fi
    
    # 执行洗声分离
    $AUDIO_SEPARATOR "$VOCALS_FILE" \
        --model_filename "$WASH_MODEL" \
        --model_file_dir "$WASH_MODEL_DIR" \
        --output_dir "${PROJECT_DIR}/02_Wash" \
        --output_format wav
    
    # 检查输出 - 洗声后应该生成 (Lead Vocals) 和 (Backing Vocals)
    LEAD_VOCALS=$(ls "${PROJECT_DIR}/02_Wash/"*"(Lead Vocals)"*.wav 2>/dev/null | head -1)
    
    if [ -z "$LEAD_VOCALS" ]; then
        log_warn "未找到主唱人声文件，尝试查找其他格式..."
        # 尝试查找任何生成的wav文件
        ANY_WAV=$(ls "${PROJECT_DIR}/02_Wash/"*.wav 2>/dev/null | head -1)
        if [ -z "$ANY_WAV" ]; then
            log_warn "洗声未生成文件，复制原始人声到洗声目录"
            cp "$VOCALS_FILE" "${PROJECT_DIR}/02_Wash/"
        fi
    fi
    
    log_success "洗声完成"
}

# 第三步：去混响脱水
step_03_dry() {
    log_info "步骤3/3: 去混响脱水 (UVR-De-Echo-Aggressive)..."
    
    # 确定输入源：如果02_Wash有文件，使用洗声后的文件；否则使用01_Sep的原始人声
    if [ "$WASH_MODE" = "wash" ]; then
        cd "${PROJECT_DIR}/02_Wash"
        # 优先查找主唱人声 (Vocals)，排除 (Instrumental)
        INPUT_VOCALS=$(ls *_"(Vocals)_"*.wav 2>/dev/null | grep -v "Instrumental" | head -1)
        if [ -z "$INPUT_VOCALS" ]; then
            # 如果没有找到，查找任何非Instrumental的wav文件
            INPUT_VOCALS=$(ls *.wav 2>/dev/null | grep -v "Instrumental" | head -1)
        fi
        
        if [ -z "$INPUT_VOCALS" ]; then
            log_warn "02_Wash目录为空，回退到01_Sep原始人声"
            cd "${PROJECT_DIR}/01_Sep"
            INPUT_VOCALS=$(ls *_"(Vocals)_"*.wav | head -1)
        fi
    else
        cd "${PROJECT_DIR}/01_Sep"
        INPUT_VOCALS=$(ls *_"(Vocals)_"*.wav | head -1)
    fi
    
    if [ -z "$INPUT_VOCALS" ]; then
        log_error "未找到人声文件"
        exit 1
    fi
    
    log_info "使用输入文件: $INPUT_VOCALS"
    
    $AUDIO_SEPARATOR "$INPUT_VOCALS" \
        --model_filename "$DRY_MODEL" \
        --model_file_dir "$VR_MODEL_DIR" \
        --output_dir "${PROJECT_DIR}/03_Dry" \
        --output_format wav
    
    # 检查输出
    if [ ! -f "${PROJECT_DIR}/03_Dry/${INPUT_VOCALS%.*}_(No Echo)_${DRY_MODEL%.pth}.wav" ]; then
        log_error "脱水失败，未找到去混响文件"
        exit 1
    fi
    
    log_success "去混响脱水完成"
}

# 第四步：母带处理
step_04_master() {
    log_info "步骤4/4: 母带处理 (48kHz/320kbps)..."
    
    cd "${PROJECT_DIR}/03_Dry"
    
    # 获取脱水后人声文件
    DRY_FILE=$(ls *_"(No Echo)_"*.wav | head -1)
    
    if [ -z "$DRY_FILE" ]; then
        log_error "未找到脱水后人声文件"
        exit 1
    fi
    
    # 生成母带版本 (320kbps)
    $FFMPEG -y -i "$DRY_FILE" \
        -ar 48000 -ac 2 -b:a 320k \
        "${PROJECT_DIR}/04_Master/${PROJECT_NAME}_Master.mp3"
    
    # 生成预览版本 (128kbps)
    $FFMPEG -y -i "${PROJECT_DIR}/04_Master/${PROJECT_NAME}_Master.mp3" \
        -ar 48000 -ac 2 -b:a 128k \
        "${PROJECT_DIR}/04_Master/${PROJECT_NAME}_Preview.mp3"
    
    log_success "母带处理完成"
}

# 清理和归档
cleanup() {
    log_info "清理临时文件..."
    
    # 保留关键目录，清理临时文件
    find "${PROJECT_DIR}" -name "*.tmp" -delete 2>/dev/null || true
    
    log_success "清理完成"
}

# 生成报告
report() {
    echo ""
    echo "============================================================"
    echo -e "${GREEN}🎵 九歌完美版音频处理完成${NC}"
    echo "============================================================"
    echo "项目: ${PROJECT_NAME}"
    echo "模式: ${MODE}"
    echo "洗声: ${WASH_MODE}"
    echo ""
    echo "输出文件:"
    echo "  母带: ${PROJECT_DIR}/04_Master/${PROJECT_NAME}_Master.mp3"
    echo "  预览: ${PROJECT_DIR}/04_Master/${PROJECT_NAME}_Preview.mp3"
    echo ""
    echo "项目目录: ${PROJECT_DIR}"
    echo "============================================================"
}

# 主流程
main() {
    echo "============================================================"
    echo -e "${BLUE}🎵 九歌完美版音频处理流水线 V1.0${NC}"
    echo "============================================================"
    echo "输入: ${INPUT_FILE}"
    echo "模式: ${MODE}"
    echo "洗声: ${WASH_MODE}"
    echo "============================================================"
    
    check_deps
    setup_project
    step_01_separate
    step_02_wash
    step_03_dry
    step_04_master
    cleanup
    report
    
    echo -e "${GREEN}✅ 全流程已闭环，Boss请安睡 🌙${NC}"
}

# 执行
main "$@"
