#!/bin/bash

# media-analyzer - 音视频内容分析工具

set -e

# 检查依赖
check_dependencies() {
    if ! command -v ffprobe &> /dev/null || ! command -v ffmpeg &> /dev/null; then
        echo "错误: 需要安装 ffmpeg 和 ffprobe"
        exit 1
    fi
}

# 格式化时长 (秒 -> HH:MM:SS)
format_duration() {
    local seconds=$1
    printf "%02d:%02d:%02d" $((seconds/3600)) $((seconds%3600/60)) $((seconds%60))
}

# 分析媒体文件
analyze_media() {
    local file="$1"
    
    if [[ ! -f "$file" ]]; then
        echo "错误: 文件不存在: $file"
        exit 1
    fi
    
    # 获取媒体信息 (JSON格式)
    local info
    info=$(ffprobe -v quiet -print_format json -show_format -show_streams "$file" 2>/dev/null)
    
    if [[ -z "$info" ]]; then
        echo "错误: 无法读取媒体文件: $file"
        exit 1
    fi
    
    # 提取关键信息
    local duration width height frame_rate video_codec audio_codec bitrate
    duration=$(echo "$info" | grep -o '"duration": "[^"]*"' | head -1 | cut -d'"' -f4)
    width=$(echo "$info" | grep -o '"width": [0-9]*' | head -1 | cut -d' ' -f2)
    height=$(echo "$info" | grep -o '"height": [0-9]*' | head -1 | cut -d' ' -f2)
    frame_rate=$(echo "$info" | grep -o '"r_frame_rate": "[^"]*"' | head -1 | cut -d'"' -f4)
    video_codec=$(echo "$info" | grep -o '"codec_name": "[^"]*"' | head -1 | cut -d'"' -f4)
    audio_codec=$(echo "$info" | grep -o '"codec_name": "[^"]*"' | tail -1 | cut -d'"' -f4)
    bitrate=$(echo "$info" | grep -o '"bit_rate": "[^"]*"' | head -1 | cut -d'"' -f4)
    
    # 判断媒体类型
    local media_type="unknown"
    local has_video=$(echo "$info" | grep -c '"codec_type": "video"')
    local has_audio=$(echo "$info" | grep -c '"codec_type": "audio"')
    
    if [[ $has_video -gt 0 && $has_audio -gt 0 ]]; then
        media_type="video"
    elif [[ $has_video -gt 0 ]]; then
        media_type="video"
    elif [[ $has_audio -gt 0 ]]; then
        media_type="audio"
    fi
    
    # 格式化输出
    local duration_formatted=""
    if [[ -n "$duration" ]]; then
        duration_formatted=$(format_duration "${duration%.*}")
    fi
    
    # 构建JSON输出
    cat << EOF
{
  "file": "$file",
  "type": "$media_type",
  "duration": "$duration_formatted",
  "duration_seconds": "${duration%.*}",
  "resolution": "${width}x${height}",
  "width": $width,
  "height": $height,
  "frame_rate": "$frame_rate",
  "video_codec": "$video_codec",
  "audio_codec": "$audio_codec",
  "bitrate": "$bitrate"
}
EOF
}

# 提取视频帧
extract_frame() {
    local file="$1"
    local timestamp="${2:-0}"
    local output="${3:-frame.jpg}"
    
    if [[ ! -f "$file" ]]; then
        echo "错误: 文件不存在: $file"
        exit 1
    fi
    
    ffmpeg -y -ss "$timestamp" -i "$file" -vframes 1 -q:v 2 "$output" 2>/dev/null
    
    if [[ -f "$output" ]]; then
        echo "已保存帧到: $output"
    else
        echo "错误: 提取帧失败"
        exit 1
    fi
}

# 提取视频封面
extract_cover() {
    local file="$1"
    local output="${2:-cover.jpg}"
    
    if [[ ! -f "$file" ]]; then
        echo "错误: 文件不存在: $file"
        exit 1
    fi
    
    # 尝试从视频中提取嵌入的封面
    ffmpeg -y -i "$file" -vcodec copy -an "$output" 2>/dev/null
    
    # 如果没有嵌入封面，提取第一帧
    if [[ ! -s "$output" ]]; then
        ffmpeg -y -ss 00:00:01 -i "$file" -vframes 1 -q:v 2 "$output" 2>/dev/null
    fi
    
    if [[ -f "$output" && -s "$output" ]]; then
        echo "已保存封面到: $output"
    else
        echo "错误: 提取封面失败"
        exit 1
    fi
}

# 生成音频波形
generate_waveform() {
    local file="$1"
    local output="${2:-waveform.png}"
    
    if [[ ! -f "$file" ]]; then
        echo "错误: 文件不存在: $file"
        exit 1
    fi
    
    ffmpeg -y -i "$file" -filter_complex "showwavespic=s=800x200:colors=#4A90D9" -frames:v 1 "$output" 2>/dev/null
    
    if [[ -f "$output" ]]; then
        echo "已保存波形图到: $output"
    else
        echo "错误: 生成波形失败"
        exit 1
    fi
}

# 批量分析目录
batch_analyze() {
    local dir="$1"
    
    if [[ ! -d "$dir" ]]; then
        echo "错误: 目录不存在: $dir"
        exit 1
    fi
    
    echo "分析目录: $dir"
    echo "---"
    
    for file in "$dir"/*; do
        if [[ -f "$file" ]]; then
            echo ">> $file"
            analyze_media "$file" 2>/dev/null || echo "  无法分析"
            echo ""
        fi
    done
}

# 显示帮助
show_help() {
    cat << EOF
media-analyzer - 音视频内容分析工具

用法:
  media-analyzer analyze <文件>     分析媒体文件并输出JSON
  media-analyzer frame <文件> [时间] [输出文件]  提取视频帧
  media-analyzer cover <文件> [输出文件]        提取视频封面
  media-analyzer waveform <文件> [输出文件]     生成音频波形图
  media-analyzer batch <目录>       批量分析目录中的媒体文件
  media-analyzer help               显示帮助

示例:
  media-analyzer analyze /path/to/video.mp4
  media-analyzer frame /path/to/video.mp4 10
  media-analyzer cover /path/to/video.mp4
  media-analyzer waveform /path/to/audio.mp3
EOF
}

# 主程序
main() {
    check_dependencies
    
    local command="${1:-help}"
    
    case "$command" in
        analyze)
            analyze_media "$2"
            ;;
        frame)
            extract_frame "$2" "$3" "$4"
            ;;
        cover)
            extract_cover "$2" "$3"
            ;;
        waveform)
            generate_waveform "$2" "$3"
            ;;
        batch)
            batch_analyze "$2"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo "未知命令: $command"
            echo "使用 'media-analyzer help' 查看帮助"
            exit 1
            ;;
    esac
}

main "$@"
