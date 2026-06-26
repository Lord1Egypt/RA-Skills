#!/bin/bash
# 多角色音频生成器 - 完整最终版（配置固化版）
# 基于真实需求开发，简化优先，实用导向，配置固化

set -e  # 出错时退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================================================
# 配置系统加载
# ============================================================================

# 加载配置系统
CONFIG_DIR="$(dirname "$0")/../config"
if [ -f "$CONFIG_DIR/config.sh" ]; then
    source "$CONFIG_DIR/config.sh"
    echo -e "${GREEN}✅ 配置系统加载成功${NC}"
else
    echo -e "${RED}❌ 配置文件不存在: $CONFIG_DIR/config.sh${NC}"
    echo -e "${YELLOW}⚠️  使用默认配置（建议安装完整配置系统）${NC}"
    
    # 默认配置（兼容模式）
    EDGE_TTS="edge-tts"
    FFMPEG="ffmpeg"
    DEFAULT_VOICE="zh-CN-XiaoxiaoNeural"
    DEFAULT_RATE="+10%"
    
    # 默认空间位置配置
    declare -A SPATIAL_POSITIONS=(
        ["center"]="0.5*c0+0.5*c1:0.5*c0+0.5*c1"
        ["left"]="0.7*c0+0.3*c1:0.3*c0+0.7*c1"
        ["right"]="0.3*c0+0.7*c1:0.7*c0+0.3*c1"
    )
    
    # 默认角色声音配置
    declare -A VOICE_CONFIG=(
        ["花花"]="zh-CN-XiaoxiaoNeural:+10%"
        ["小霞"]="zh-CN-XiaoyiNeural:+15%"
        ["观察者"]="zh-CN-YunxiaNeural:+0%"
    )
    
    # 默认角色空间位置配置
    declare -A POSITION_CONFIG=(
        ["花花"]="center"
        ["小霞"]="left"
        ["观察者"]="right"
    )
fi

# ============================================================================
# 配置变量映射（兼容现有代码）
# ============================================================================

# 如果配置系统加载成功，使用配置系统的变量
if [ -f "$CONFIG_DIR/config.sh" ]; then
    # 命令映射
    EDGE_TTS="$EDGE_TTS_CMD"
    FFMPEG="$FFMPEG_CMD"
    
    # 默认配置映射
    DEFAULT_VOICE="$DEFAULT_VOICE"
    DEFAULT_RATE="$DEFAULT_TTS_RATE"
    
    # 角色配置映射（从配置系统获取）
    # 注意：这里需要将配置系统的格式转换为脚本需要的格式
    # 配置系统格式：TTS_VOICES["花花"]="zh-CN-XiaoxiaoNeural"
    # 脚本需要格式：VOICE_CONFIG["花花"]="zh-CN-XiaoxiaoNeural:+10%"
    
    # 初始化角色配置
    declare -A VOICE_CONFIG
    declare -A POSITION_CONFIG
    
    # 从默认角色配置加载
    for role in "${!DEFAULT_ROLE_CONFIG[@]}"; do
        config="${DEFAULT_ROLE_CONFIG[$role]}"
        
        # 解析配置
        voice=$(echo "$config" | grep -o "voice:[^,]*" | cut -d: -f2)
        position=$(echo "$config" | grep -o "position:[^,]*" | cut -d: -f2)
        
        # 获取语音
        tts_voice="${TTS_VOICES[$voice]}"
        if [ -z "$tts_voice" ]; then
            tts_voice="$voice"
        fi
        
        # 设置配置
        VOICE_CONFIG["$role"]="$tts_voice:$DEFAULT_TTS_RATE"
        POSITION_CONFIG["$role"]="$position"
    done
fi

# 使用说明
usage() {
    echo -e "${GREEN}多角色音频生成器${NC}"
    echo "基于真实需求开发，简化优先，实用导向"
    echo ""
    echo "用法: $0 [选项] <脚本文件>"
    echo ""
    echo "选项:"
    echo "  -h, --help          显示帮助信息"
    echo "  -v, --verbose       详细输出模式"
    echo "  -o, --output <目录> 指定输出目录"
    echo "  --no-spatial        不添加空间音频效果"
    echo "  --keep-intermediate 保留中间文件"
    echo ""
    echo "示例:"
    echo "  $0 dialogue.txt"
    echo "  $0 -v -o ./output dialogue.txt"
    echo "  $0 --no-spatial dialogue.txt"
    exit 0
}

# 检查依赖
check_dependencies() {
    echo -e "${BLUE}🔍 检查依赖...${NC}"
    
    # 检查edge-tts
    if ! command -v $EDGE_TTS &> /dev/null; then
        echo -e "${RED}❌ 未找到edge-tts，请安装: pip install edge-tts${NC}"
        exit 1
    fi
    echo -e "  ✅ edge-tts: 已安装"
    
    # 检查ffmpeg
    if ! command -v $FFMPEG &> /dev/null; then
        echo -e "${RED}❌ 未找到ffmpeg，请安装${NC}"
        echo -e "  macOS: brew install ffmpeg"
        echo -e "  Ubuntu: sudo apt install ffmpeg"
        exit 1
    fi
    echo -e "  ✅ ffmpeg: 已安装"
    
    echo -e "${GREEN}✅ 所有依赖检查通过${NC}"
}

# 解析脚本文件
parse_script() {
    local script_file="$1"
    local output_dir="$2"
    
    echo -e "${BLUE}📝 解析脚本文件: $script_file${NC}"
    
    if [ ! -f "$script_file" ]; then
        echo -e "${RED}❌ 脚本文件不存在: $script_file${NC}"
        exit 1
    fi
    
    # 提取所有角色
    local roles=($(grep -o '【[^】]*】' "$script_file" | sort -u | tr -d '【】'))
    
    if [ ${#roles[@]} -eq 0 ]; then
        echo -e "${RED}❌ 未找到角色标记，请使用【角色名】格式${NC}"
        exit 1
    fi
    
    echo -e "  找到 ${#roles[@]} 个角色: ${roles[*]}"
    
    # 为每个角色提取内容
    for role in "${roles[@]}"; do
        echo -e "  📄 提取角色: $role"
        
        # 使用awk提取角色内容
        awk -v role="$role" '
        BEGIN { in_role=0 }
        $0 ~ "【" role "】" { in_role=1; next }
        /^【/ { in_role=0; next }
        /^===/ { in_role=0; next }
        in_role && NF > 0 { 
            # 过滤标记符号
            gsub(/^[=【】\t ]+/, "", $0)
            gsub(/[=【】\t ]+$/, "", $0)
            if ($0 != "" && $0 !~ /^#/) print $0
        }
        ' "$script_file" > "$output_dir/${role}_内容.txt"
        
        local line_count=$(wc -l < "$output_dir/${role}_内容.txt")
        echo -e "    ✅ 提取 $line_count 行内容"
    done
    
    echo -e "${GREEN}✅ 脚本解析完成${NC}"
    echo "${roles[@]}"
}

# 生成角色音频
generate_audio() {
    local role="$1"
    local content_file="$2"
    local output_file="$3"
    local verbose="$4"
    
    echo -e "${BLUE}🔊 生成角色音频: $role${NC}"
    
    # 获取角色配置
    local voice_config="${VOICE_CONFIG[$role]:-$DEFAULT_VOICE:$DEFAULT_RATE}"
    local voice=$(echo "$voice_config" | cut -d':' -f1)
    local rate=$(echo "$voice_config" | cut -d':' -f2)
    
    echo -e "  声音: $voice, 语速: $rate"
    
    # 检查内容文件
    if [ ! -s "$content_file" ]; then
        echo -e "${YELLOW}⚠️  角色 $role 内容为空，跳过音频生成${NC}"
        return 1
    fi
    
    # 生成音频
    if [ "$verbose" = "1" ]; then
        $EDGE_TTS --voice "$voice" --rate "$rate" --text "$(cat "$content_file")" --write-media "$output_file"
    else
        $EDGE_TTS --voice "$voice" --rate "$rate" --text "$(cat "$content_file")" --write-media "$output_file" 2>/dev/null
    fi
    
    if [ $? -eq 0 ] && [ -f "$output_file" ]; then
        local file_size=$(du -h "$output_file" | cut -f1)
        echo -e "  ✅ 生成成功: $output_file ($file_size)"
        return 0
    else
        echo -e "${RED}❌ 音频生成失败: $role${NC}"
        return 1
    fi
}

# 添加空间音频效果
add_spatial_audio() {
    local input_file="$1"
    local output_file="$2"
    local position="$3"
    local verbose="$4"
    
    echo -e "${BLUE}🎧 添加空间音频效果: $position${NC}"
    
    # 获取空间位置参数
    local pan_params="${SPATIAL_POSITIONS[$position]}"
    if [ -z "$pan_params" ]; then
        echo -e "${YELLOW}⚠️  未知的空间位置: $position，使用默认(center)${NC}"
        pan_params="${SPATIAL_POSITIONS[center]}"
    fi
    
    local left_channel=$(echo "$pan_params" | cut -d':' -f1)
    local right_channel=$(echo "$pan_params" | cut -d':' -f2)
    
    # 使用ffmpeg添加空间效果
    if [ "$verbose" = "1" ]; then
        $FFMPEG -i "$input_file" -af "pan=stereo|c0=$left_channel|c1=$right_channel" -y "$output_file"
    else
        $FFMPEG -i "$input_file" -af "pan=stereo|c0=$left_channel|c1=$right_channel" -y "$output_file" 2>/dev/null
    fi
    
    if [ $? -eq 0 ] && [ -f "$output_file" ]; then
        local file_size=$(du -h "$output_file" | cut -f1)
        echo -e "  ✅ 空间音频生成成功: $output_file ($file_size)"
        return 0
    else
        echo -e "${YELLOW}⚠️  空间音频生成失败，使用原文件${NC}"
        cp "$input_file" "$output_file"
        return 1
    fi
}

# 合成最终音频
synthesize_audio() {
    local roles=($1)
    local output_dir="$2"
    local use_spatial="$3"
    local final_output="$4"
    local verbose="$5"
    
    echo -e "${BLUE}🔗 合成最终音频${NC}"
    
    # 创建合成列表
    local concat_list="$output_dir/concat_list.txt"
    > "$concat_list"
    
    for role in "${roles[@]}"; do
        if [ "$use_spatial" = "1" ]; then
            echo "file '空间版/${role}_空间版.mp3'" >> "$concat_list"
        else
            echo "file '${role}_原始.mp3'" >> "$concat_list"
        fi
    done
    
    # 使用ffmpeg合成
    if [ "$verbose" = "1" ]; then
        $FFMPEG -f concat -safe 0 -i "$concat_list" -c copy "$final_output"
    else
        $FFMPEG -f concat -safe 0 -i "$concat_list" -c copy "$final_output" 2>/dev/null
    fi
    
    if [ $? -eq 0 ] && [ -f "$final_output" ]; then
        # 音频优化（标准化音量，淡入淡出）
        local optimized_output="${final_output%.mp3}_优化版.mp3"
        
        local duration=$($FFMPEG -i "$final_output" 2>&1 | grep Duration | awk '{print $2}' | tr -d ',')
        local seconds=$(echo "$duration" | awk -F: '{print ($1*3600)+($2*60)+$3}')
        local fade_out=$(echo "$seconds - 1" | bc)
        
        if [ "$verbose" = "1" ]; then
            $FFMPEG -i "$final_output" \
                -af "loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=in:st=0:d=1,afade=t=out:st=$fade_out:d=1" \
                -y "$optimized_output"
        else
            $FFMPEG -i "$final_output" \
                -af "loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=in:st=0:d=1,afade=t=out:st=$fade_out:d=1" \
                -y "$optimized_output" 2>/dev/null
        fi
        
        if [ -f "$optimized_output" ]; then
            mv "$optimized_output" "$final_output"
        fi
        
        local file_size=$(du -h "$final_output" | cut -f1)
        local duration_formatted=$(printf "%.1f秒" "$seconds")
        echo -e "${GREEN}✅ 最终音频生成成功: $final_output ($file_size, $duration_formatted)${NC}"
        return 0
    else
        echo -e "${RED}❌ 音频合成失败${NC}"
        return 1
    fi
}

# 清理中间文件
cleanup_intermediate() {
    local output_dir="$1"
    local keep_intermediate="$2"
    
    if [ "$keep_intermediate" != "1" ]; then
        echo -e "${BLUE}🧹 清理中间文件...${NC}"
        rm -f "$output_dir"/*_内容.txt
        rm -f "$output_dir"/*_原始.mp3
        rm -f "$output_dir"/空间版/*.mp3
        rm -f "$output_dir"/concat_list.txt
        rmdir "$output_dir/空间版" 2>/dev/null || true
        echo -e "${GREEN}✅ 清理完成${NC}"
    else
        echo -e "${YELLOW}📁 保留中间文件${NC}"
    fi
}

# 生成报告
generate_report() {
    local script_file="$1"
    local output_dir="$2"
    local roles=($3)
    local final_output="$4"
    local use_spatial="$5"
    
    local report_file="$output_dir/生成报告.md"
    
    cat > "$report_file" << EOF
# 多角色音频生成报告

## 生成信息
- **生成时间**: $(date '+%Y-%m-%d %H:%M:%S')
- **脚本文件**: $(basename "$script_file")
- **输出目录**: $(basename "$output_dir")
- **空间音频**: $( [ "$use_spatial" = "1" ] && echo "是" || echo "否" )

## 角色信息
**共生成 ${#roles[@]} 个角色:**

$(for role in "${roles[@]}"; do
    content_file="$output_dir/${role}_内容.txt"
    audio_file="$output_dir/${role}_原始.mp3"
    spatial_file="$output_dir/空间版/${role}_空间版.mp3"
    
    echo "### $role"
    echo "- **内容行数**: $(wc -l < "$content_file" 2>/dev/null || echo 0)"
    echo "- **原始音频**: $( [ -f "$audio_file" ] && du -h "$audio_file" | cut -f1 || echo "未生成" )"
    if [ "$use_spatial" = "1" ]; then
        echo "- **空间音频**: $( [ -f "$spatial_file" ] && du -h "$spatial_file" | cut -f1 || echo "未生成" )"
    fi
    echo ""
done)

## 最终输出
- **文件**: $(basename "$final_output")
- **大小**: $(du -h "$final_output" | cut -f1)
- **时长**: $(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$final_output" 2>/dev/null | awk '{printf "%.1f秒", $1}' || echo "未知")

## 配置信息
### 角色声音配置:
$(for role in "${roles[@]}"; do
    voice_config="${VOICE_CONFIG[$role]}"
    if [ -n "$voice_config" ]; then
        echo "- **$role**: $voice_config"
    fi
done)

### 空间位置配置:
$(for role in "${roles[@]}"; do
    position="${POSITION_CONFIG[$role]}"
    if [ -n "$position" ]; then
        echo "- **$role**: $position"
    fi
done)

## 使用建议
1. **耳机体验**: 建议使用耳机获得最佳空间音频效果
2. **环境安静**: 在安静环境中体验以获得最佳沉浸感
3. **心理准备**: 放松身心，跟随音频引导
4. **反馈优化**: 如有反馈可调整脚本和配置重新生成

## 技术信息
- **Edge TTS版本**: 已安装
- **ffmpeg版本**: 已安装
- **生成脚本版本**: v1.0.0

---
**生成工具**: 多角色音频生成器  
**项目地址**: https://github.com/yourusername/multirole-tts-skill  
**致谢**: 基于真实用户需求开发，感谢所有反馈者
EOF

    echo -e "${GREEN}📄 生成报告: $report_file${NC}"
}

# 主函数
main() {
    # 解析参数
    local verbose=0
    local output_dir=""
    local use_spatial=1
    local keep_intermediate=0
    local script_file=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                usage
                ;;
            -v|--verbose)
                verbose=1
                shift
                ;;
            -o|--output)
                output_dir="$2"
                shift 2
                ;;
            --no-spatial)
                use_spatial=0
                shift
                ;;
            --keep-intermediate)
                keep_intermediate=1
                shift
                ;;
            -*)
                echo -e "${RED}❌ 未知选项: $1${NC}"
                usage
                ;;
            *)
                script_file="$1"
                shift
                ;;
        esac
    done
    
    # 检查必要参数
    if [ -z "$script_file" ]; then
        echo -e "${RED}❌ 请指定脚本文件${NC}"
        usage
    fi
    
    # 设置输出目录
    if [ -z "$output_dir" ]; then
        output_dir="$(pwd)/output_$(date +%Y%m%d_%H%M%S)"
    fi
    
    # 创建输出目录
    mkdir -p "$output_dir"
    mkdir -p "$output_dir/空间版"
    
    # 显示开始信息
    echo -e "${GREEN}🚀 开始多角色音频生成${NC}"
    echo -e "脚本文件: $script_file"
    echo -e "输出目录: $output_dir"
    echo -e "空间音频: $( [ "$