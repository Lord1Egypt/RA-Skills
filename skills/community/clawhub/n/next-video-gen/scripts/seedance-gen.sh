#!/bin/bash

# Next Video Gen 生成脚本
# 支持: 文生图、文生视频/音画、图生视频/音画、素材生视频
# 依赖: bash + node (无 jq, 无 curl)

set -uo pipefail

# 脚本目录（用于 node 工具脚本）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

readonly IMAGE_API_BASE="https://ark.cn-beijing.volces.com/api/v3/images"
readonly VIDEO_API_BASE="https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"
readonly IMAGE_MODEL="doubao-seedream-5-0-260128"
readonly VIDEO_MODEL="doubao-seedance-1-5-pro-251215"
readonly MAX_POLL_SECONDS=600
readonly POLL_INTERVAL=5
readonly PROGRESS_INTERVAL=30

MODE="txt2video"
MODEL=""
DURATION=5
QUALITY=""
ASPECT_RATIO=""
WATERMARK="true"
GENERATE_AUDIO="false"
VIDEO_URL=""
AUDIO_URL=""
REF_IMAGES=()
PROMPT=""
GLOBAL_TASK_ID=""
OUTPUT_MODE="video"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
error() { echo -e "${RED}ERROR: $1${NC}" >&2; exit 1; }
info() { echo -e "${BLUE}INFO: $1${NC}"; }
success() { echo -e "${GREEN}SUCCESS: $1${NC}"; }
warn() { echo -e "${YELLOW}WARNING: $1${NC}"; }

# ── 依赖检查 ──────────────────────────────────────────────────────────────────
check_dependencies() {
    if ! command -v node &> /dev/null; then
        error "node is required. Install: https://nodejs.org"
    fi
}

check_api_key() {
    if [[ -z "${DOUBAO_API_KEY:-}" ]]; then
        error "DOUBAO_API_KEY environment variable is required.
Get your API key from: https://console.volcengine.com/ark
Set it with: export DOUBAO_API_KEY=your_key_here"
    fi
}

# ── 参数解析 ──────────────────────────────────────────────────────────────────
parse_args() {
    if [[ $# -eq 0 ]]; then
        error "Usage: $0 \"prompt\" [options]

支持的模式:
  --mode txt2img       文生图
  --mode txt2video     文生视频 / 文生音画 (默认)
  --mode img2video     图生视频 / 图生音画
  --mode vid2video     素材生视频

Options:
  --mode <mode>        生成模式 (默认: txt2video)
  --prompt <text>      生成内容描述
  --image <url>        参考图片 URL (可多次)
  --video <url>        视频素材 URL (素材生视频)
  --audio <url>        参考音频 URL
  --duration <4-12>    视频时长 (默认: 5)
  --quality            图片: 2K/1K/HD / 视频: 480p/720p/1080p
  --aspect-ratio       图片: 1:1/16:9/9:16 / 视频: 16:9/9:16/1:1
  --watermark <true|false> (默认: true)
  --no-audio           关闭视频音频（音频默认关闭）
  --audio             启用视频音频（与 --audio <url> 参考音频不同）
  --model <id>         指定模型 (默认: doubao-seedance-1-5-pro-251215)
                        支持: doubao-seedance-1-5-pro-251215 / doubao-seedance-2-0-260128

Examples:
  \$0 \"一只橘猫在阳光下打盹\"
  \$0 \"未来城市夜景\" --mode txt2img --quality 2K
  \$0 \"猫在草地上奔跑，有鸟叫\" --mode txt2video --duration 5
  \$0 \"镜头推进\" --mode img2video --image \"https://example.com/cat.jpg\"
  \$0 \"加快节奏\" --mode vid2video --video \"https://example.com/input.mp4\""
  $0 "海边日落" --model doubao-seedance-2-0-260128 --duration 8
    fi

    while [[ $# -gt 0 ]]; do
        case $1 in
            --mode) MODE="$2"; shift 2 ;;
            --prompt) PROMPT="$2"; shift 2 ;;
            --image) REF_IMAGES+=("$2"); shift 2 ;;
            --video) VIDEO_URL="$2"; shift 2 ;;
            --audio) AUDIO_URL="$2"; shift 2 ;;
            --duration)
                DURATION="$2"
                if [[ ! "$DURATION" =~ ^[0-9]+$ ]] || ((DURATION < 4 || DURATION > 12)); then
                    error "Duration must be 4-12"
                fi
                shift 2 ;;
            --quality) QUALITY="$2"; shift 2 ;;
            --aspect-ratio) ASPECT_RATIO="$2"; shift 2 ;;
            --watermark) WATERMARK="$2"; shift 2 ;;
            --model) MODEL="$2"; shift 2 ;;
            --no-audio) GENERATE_AUDIO="false"; shift ;;
            --enable-audio) GENERATE_AUDIO="true"; shift ;;
            --audio) AUDIO_URL="$2"; shift 2 ;;
            -h|--help) error "Usage: $0 \"prompt\" [options]" ;;
            *) [[ -z "$PROMPT" ]] && PROMPT="$1" || error "Unknown: $1"; shift ;;
        esac
    done

    [[ -z "$PROMPT" ]] && error "Prompt required."

    [[ -n "$VIDEO_URL" && "$MODE" == "txt2video" ]] && MODE="vid2video"

    case $MODE in
        txt2img) OUTPUT_MODE="image" ;;
        txt2video|img2video|vid2video) OUTPUT_MODE="video" ;;
        *) error "Invalid mode: $MODE" ;;
    esac

    validate_args
}

validate_args() {
    if [[ "$OUTPUT_MODE" == "image" ]]; then
        QUALITY="${QUALITY:-2K}"
        ASPECT_RATIO="${ASPECT_RATIO:-1:1}"
        [[ ! "$QUALITY" =~ ^(2K|1K|HD)$ ]] && error "Image quality: 2K/1K/HD"
        [[ ! "$ASPECT_RATIO" =~ ^(1:1|16:9|9:16)$ ]] && error "Image ratio: 1:1/16:9/9:16"
    else
        QUALITY="${QUALITY:-720p}"
        ASPECT_RATIO="${ASPECT_RATIO:-16:9}"
        [[ ! "$QUALITY" =~ ^(480p|720p|1080p)$ ]] && error "Video quality: 480p/720p/1080p"
        [[ ! "$ASPECT_RATIO" =~ ^(16:9|9:16|1:1)$ ]] && error "Video ratio: 16:9/9:16/1:1"
    fi
}

# ── Node.js JSON 工具 (替代 jq) ───────────────────────────────────────────────

# 用临时文件传递 JSON，避免命令行参数转义问题
_TMPDIR="${TMPDIR:-${TEMP:-/tmp}}"
_JSON_FILE="${_TMPDIR}/next_video_gen_$$.json"

_cleanup_json() { rm -f "$_JSON_FILE"; }
trap _cleanup_json EXIT

# 提取 JSON 字段 (支持 data[0].url 语法)
# 用法: json_get "path" < "$resp_file"
json_get() {
    local path="$1"
    node -e "
var fs=require('fs');
var input=fs.readFileSync(process.argv[1],'utf8');
var path=process.argv[2];
try {
  var obj=JSON.parse(input);
  var parts=path.split('.').filter(Boolean);
  for(var i=0;i<parts.length;i++) {
    if(obj==null){console.log('');process.exit(0);}
    var p=parts[i];
    var m=p.match(/^([^\[]+)\[(\d+)\]$/);
    if(m){obj=obj[m[1]][parseInt(m[2])];}
    else{obj=obj[p];}
  }
  console.log(obj==null?'':(typeof obj==='string'?obj:JSON.stringify(obj)));
} catch(e){ console.log(''); }
" "$_JSON_FILE" "$path" || true
}

# 构建文生图 payload
build_image_payload() {
    local prompt_file="${_TMPDIR}/prompt_$$.txt"
    echo -n "$PROMPT" > "$prompt_file"

    IMAGE_MODEL="$IMAGE_MODEL" QUALITY="$QUALITY" ASPECT_RATIO="$ASPECT_RATIO" WATERMARK="$WATERMARK" PROMPT_FILE="$prompt_file" node -e "
var fs=require('fs');
var prompt=fs.readFileSync(process.env.PROMPT_FILE,'utf8');
console.log(JSON.stringify({
  model: process.env.IMAGE_MODEL,
  prompt: prompt,
  sequential_image_generation: 'disabled',
  response_format: 'url',
  size: process.env.QUALITY,
  aspect_ratio: process.env.ASPECT_RATIO,
  watermark: process.env.WATERMARK==='true',
  stream: false
}));
" || true

    rm -f "$prompt_file"
}

# 构建视频 payload
build_video_payload() {
    # ref images 转 JSON
    REF_JSON="[]"
    for img in "${REF_IMAGES[@]}"; do
        REF_JSON=$(REF_IMG="$img" node -e "
var arr=JSON.parse(process.env.REF||'[]');
arr.push({type:'image_url',image_url:{url:process.env.REF_IMG},role:'reference_image'});
console.log(JSON.stringify(arr));
" || true)
    done

    VIDEO_REF_JSON="null"
    [[ -n "$VIDEO_URL" ]] && VIDEO_REF_JSON=$(node -e "console.log(JSON.stringify({type:'video_url',video_url:{url:'$VIDEO_URL'},role:'reference_video'}))" || true)

    AUDIO_REF_JSON="null"
    [[ -n "$AUDIO_URL" ]] && AUDIO_REF_JSON=$(node -e "console.log(JSON.stringify({type:'audio_url',audio_url:{url:'$AUDIO_URL'},role:'reference_audio'}))" || true)

    node -e "
var refImages=JSON.parse(process.env.REF_JSON||'[]');
var content=[{type:'text',text:process.env.PROMPT}];
refImages.forEach(function(i){content.push(i);});
var v=$VIDEO_REF_JSON; if(v)content.push(v);
var a=$AUDIO_REF_JSON; if(a)content.push(a);
console.log(JSON.stringify({
  model:process.env.MODEL || process.env.VIDEO_MODEL,
  content:content,
  generate_audio:process.env.GENERATE_AUDIO==='true',
  ratio:process.env.ASPECT_RATIO,
  duration:parseInt(process.env.DURATION),
  watermark:process.env.WATERMARK==='true'
}));
" || true
}

# ── HTTP (Node.js 实现，跨平台) ─────────────────────────────────────────────
do_request() {
    local method="$1" url="$2" payload="$3"
    local resp; resp=$(node "${SCRIPT_DIR}/http-request.js" "$method" "$url" ${payload:+-d "$payload"} 2>&1) || true
    echo "$resp"
}

# ── 文生图 (同步) ──────────────────────────────────────────────────────────────
submit_image() {
    export IMAGE_MODEL QUALITY ASPECT_RATIO WATERMARK
    local payload; payload=$(build_image_payload)

    local resp http_code
    resp=$(do_request "POST" "${IMAGE_API_BASE}/generations" "$payload")
    http_code=$(echo "$resp" | tail -n1)
    resp=$(echo "$resp" | sed '$d')

    [[ "$http_code" != "200" ]] && handle_error "$http_code" "$resp"

    echo "$resp" > "$_JSON_FILE"
    local image_url; image_url=$(json_get "data[0].url")
    if [[ -z "$image_url" || "$image_url" == "null" ]]; then
        error "Failed to get image URL: $resp"
    fi

    echo "TASK_SUBMITTED: task_id=sync mode=文生图"
    echo "IMAGE_URL=$image_url"
    echo "RESOLUTION=${QUALITY}"
    echo "ASPECT_RATIO=${ASPECT_RATIO}"
    echo "ELAPSED=0s"
    download_file "$image_url" "img"
}

# ── 视频 (异步) ───────────────────────────────────────────────────────────────
submit_video() {
    # ref images 转 JSON
    REF_JSON="[]"
    for img in "${REF_IMAGES[@]}"; do
        REF_JSON=$(REF_IMG="$img" node -e "
var arr=JSON.parse(process.env.REF||'[]');
arr.push({type:'image_url',image_url:{url:process.env.REF_IMG},role:'reference_image'});
console.log(JSON.stringify(arr));
" || true)
    done

    export PROMPT VIDEO_MODEL QUALITY ASPECT_RATIO DURATION GENERATE_AUDIO WATERMARK MODEL
    export REF_JSON VIDEO_URL AUDIO_URL

    local payload; payload=$(build_video_payload)

    local resp http_code
    resp=$(do_request "POST" "${VIDEO_API_BASE}" "$payload")
    http_code=$(echo "$resp" | tail -n1)
    resp=$(echo "$resp" | sed '$d')

    [[ "$http_code" != "200" ]] && handle_error "$http_code" "$resp"

    echo "$resp" > "$_JSON_FILE"
    local task_id; task_id=$(json_get "id")
    if [[ -z "$task_id" || "$task_id" == "null" ]]; then
        error "Failed to get task_id: $resp"
    fi

    GLOBAL_TASK_ID="$task_id"
    local mode_info
    case $MODE in
        txt2video) [[ "$GENERATE_AUDIO" == "true" ]] && mode_info="文生音画" || mode_info="文生视频" ;;
        img2video) [[ "$GENERATE_AUDIO" == "true" ]] && mode_info="图生音画" || mode_info="图生视频" ;;
        vid2video) mode_info="素材生视频" ;;
    esac
    echo "TASK_SUBMITTED: task_id=${task_id} mode=${mode_info}"
}

poll_video() {
    local task_id=$1
    local start_time=$(date +%s)
    local last_report=-1

    while true; do
        local elapsed=$(( $(date +%s) - start_time ))

        if (( elapsed > MAX_POLL_SECONDS )); then
            echo "POLL_TIMEOUT: task_id=${task_id}"
            warn "Timed out. Check: https://console.volcengine.com/ark"
            exit 1
        fi

        local bucket=$(( elapsed / PROGRESS_INTERVAL ))
        if (( bucket > last_report && elapsed >= PROGRESS_INTERVAL )); then
            last_report=$bucket
            echo "STATUS_UPDATE: 视频生成中... (已等待 ${elapsed} 秒)"
        fi

        sleep "$POLL_INTERVAL"

        local resp http_code
        resp=$(do_request "GET" "${VIDEO_API_BASE}/${task_id}" "")
        http_code=$(echo "$resp" | tail -n1)
        resp=$(echo "$resp" | sed '$d')

        [[ "$http_code" != "200" ]] && handle_error "$http_code" "$resp"

        echo "$resp" > "$_JSON_FILE"
        local status; status=$(json_get "status")

        case $status in
            succeeded)
                handle_video_success "$resp" "$elapsed"
                return 0
                ;;
            failed)
                local err; err=$(json_get "error")
                [[ -z "$err" ]] && err=$(json_get "message")
                [[ -z "$err" ]] && err="Unknown"
                error "Generation failed: $err"
                ;;
            running|pending) ;;
            "") echo "STATUS_UPDATE: 等待中... (${elapsed}秒)" ;;
            *) echo "STATUS_UPDATE: ${status}... (${elapsed}秒)" ;;
        esac
    done
}

handle_video_success() {
    local resp=$1 elapsed=$2

    echo "$resp" > "$_JSON_FILE"

    echo "ELAPSED=${elapsed}s"
    local vu du ra re ha
    vu=$(json_get "content.video_url")
    du=$(json_get "duration")
    ra=$(json_get "ratio")
    re=$(json_get "resolution")
    ha=$(json_get "generate_audio")

    if [[ -z "$vu" || "$vu" == "null" ]]; then
        error "No video URL: $resp"
    fi

    [[ -n "$du" && "$du" != "null" ]] && echo "DURATION=${du}s"
    [[ -n "$ra" && "$ra" != "null" ]] && echo "ASPECT_RATIO=${ra}"
    [[ -n "$re" && "$re" != "null" ]] && echo "RESOLUTION=${re}"
    echo "HAS_AUDIO=${ha}"
    echo "VIDEO_URL=$vu"
    download_file "$vu" "video"
}

# ── 通用 ──────────────────────────────────────────────────────────────────────
handle_error() {
    case $1 in
        401) error "Invalid API key. https://console.volcengine.com/ark" ;;
        403) error "Access forbidden. Check API key permissions." ;;
        429) error "Rate limit exceeded. Wait and retry." ;;
        500|502|503) error "Service error. Try again later." ;;
        *) error "API error ($1): $2" ;;
    esac
}

OUTPUT_DIR="${NEXT_VIDEO_GEN_OUTPUT_DIR:-$HOME/Videos/next-video-gen}"
mkdir -p "$OUTPUT_DIR"

download_file() {
    local url=$1 type=$2 ts=$(date +%Y%m%d_%H%M%S)
    local ext; [[ "$type" == "img" ]] && ext="png" || ext="mp4"
    local fp="${OUTPUT_DIR}/${type}_${ts}.${ext}"

    info "正在下载${type}..."
    if node "${SCRIPT_DIR}/download-file.js" "$url" "$fp" 2>/dev/null; then
        success "${type}已保存: $fp"
        echo "LOCAL_FILE=$fp"
        [[ "$(uname)" == "Darwin" ]] && open "$OUTPUT_DIR"
    else
        warn "${type}下载失败，请使用在线链接"
    fi
}

# ── 主入口 ────────────────────────────────────────────────────────────────────
main() {
    check_dependencies
    check_api_key
    parse_args "$@"

    if [[ "$OUTPUT_MODE" == "image" ]]; then
        submit_image
    else
        submit_video
        poll_video "$GLOBAL_TASK_ID"
    fi
}

main "$@"
