#!/bin/bash

# 热点数据获取脚本 v2.0
# 用法: ./fetch-hotspots.sh [platform]
# 支持真实API和模拟数据两种模式

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="/root/clawd/memory/hotspots/data"
CONFIG_FILE="$SCRIPT_DIR/../config.json"
mkdir -p "$DATA_DIR"

PLATFORM="${1:-all}"
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H%M%S)

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }

# 检查是否使用真实API
USE_REAL_API=${USE_REAL_API:-false}
PROXY=${PROXY:-""}

# 通用请求函数
fetch_url() {
    local url="$1"
    local output="$2"
    
    if [[ -n "$PROXY" ]]; then
        curl -s --max-time 10 -x "$PROXY" "$url" -o "$output" 2>/dev/null
    else
        curl -s --max-time 10 "$url" -o "$output" 2>/dev/null
    fi
}

# 获取微博热搜
fetch_weibo() {
    log_info "获取微博热搜..."
    local output="$DATA_DIR/weibo_${DATE}_${TIME}.json"
    
    if [[ "$USE_REAL_API" == "true" ]]; then
        # 尝试真实API（需要代理或特殊处理）
        local url="https://weibo.com/ajax/side/hotSearch"
        if fetch_url "$url" "$output.tmp"; then
            # 解析真实数据
            if jq -e '.ok' "$output.tmp" > /dev/null 2>&1; then
                jq '[.data.realtime[] | {rank: .rank, title: .word, heat: .realpos, tag: .icon_desc}] | {platform: "weibo", date: "'$DATE'", time: "'$TIME'", data: .}' "$output.tmp" > "$output"
                rm -f "$output.tmp"
                log_info "微博热搜(真实数据)已保存"
                return
            fi
        fi
        log_warn "真实API获取失败，使用模拟数据"
    fi
    
    # 模拟数据（演示用）
    cat > "$output" << 'HTMLEOF'
{
  "platform": "weibo",
  "date": "DATE_PLACEHOLDER",
  "time": "TIME_PLACEHOLDER",
  "source": "demo",
  "data": [
    {"rank": 1, "title": "两会热点议题", "heat": 1234567, "tag": "hot"},
    {"rank": 2, "title": "AI技术新突破引发热议", "heat": 987654, "tag": "new"},
    {"rank": 3, "title": "春季养生健康指南", "heat": 876543, "tag": "health"},
    {"rank": 4, "title": "电影票房排行榜", "heat": 765432, "tag": "entertainment"},
    {"rank": 5, "title": "科技公司发布会", "heat": 654321, "tag": "tech"},
    {"rank": 6, "title": "股市行情分析", "heat": 543210, "tag": "finance"},
    {"rank": 7, "title": "体育赛事预告", "heat": 432109, "tag": "sports"},
    {"rank": 8, "title": "美食推荐打卡", "heat": 321098, "tag": "life"},
    {"rank": 9, "title": "教育政策解读", "heat": 210987, "tag": "education"},
    {"rank": 10, "title": "旅游攻略分享", "heat": 109876, "tag": "travel"}
  ]
}
HTMLEOF
    sed -i "s/DATE_PLACEHOLDER/$DATE/g; s/TIME_PLACEHOLDER/$TIME/g" "$output"
    log_info "微博热搜(演示数据)已保存: $output"
}

# 获取百度热搜
fetch_baidu() {
    log_info "获取百度热搜..."
    local output="$DATA_DIR/baidu_${DATE}_${TIME}.json"
    
    if [[ "$USE_REAL_API" == "true" ]]; then
        local url="https://top.baidu.com/api/board?platform=wise&tab=realtime"
        if fetch_url "$url" "$output.tmp"; then
            if jq -e '.data' "$output.tmp" > /dev/null 2>&1; then
                jq '{platform: "baidu", date: "'$DATE'", time: "'$TIME'", source: "real", data: [.data.cards[0].content[] | {rank: .index, title: .word, search_count: .hotScore, category: .category}]} | .data |= .[:10]' "$output.tmp" > "$output"
                rm -f "$output.tmp"
                log_info "百度热搜(真实数据)已保存"
                return
            fi
        fi
        log_warn "真实API获取失败，使用模拟数据"
    fi
    
    cat > "$output" << 'HTMLEOF'
{
  "platform": "baidu",
  "date": "DATE_PLACEHOLDER",
  "time": "TIME_PLACEHOLDER",
  "source": "demo",
  "data": [
    {"rank": 1, "title": "最新科技动态", "search_count": 890123, "category": "科技"},
    {"rank": 2, "title": "国际新闻头条", "search_count": 789012, "category": "国际"},
    {"rank": 3, "title": "财经要闻速递", "search_count": 678901, "category": "财经"},
    {"rank": 4, "title": "娱乐八卦热点", "search_count": 567890, "category": "娱乐"},
    {"rank": 5, "title": "体育赛事直播", "search_count": 456789, "category": "体育"},
    {"rank": 6, "title": "社会民生关注", "search_count": 345678, "category": "社会"},
    {"rank": 7, "title": "汽车资讯汇总", "search_count": 234567, "category": "汽车"},
    {"rank": 8, "title": "房产市场动态", "search_count": 123456, "category": "房产"},
    {"rank": 9, "title": "健康养生知识", "search_count": 98765, "category": "健康"},
    {"rank": 10, "title": "教育考试资讯", "search_count": 87654, "category": "教育"}
  ]
}
HTMLEOF
    sed -i "s/DATE_PLACEHOLDER/$DATE/g; s/TIME_PLACEHOLDER/$TIME/g" "$output"
    log_info "百度热搜(演示数据)已保存: $output"
}

# 获取知乎热榜
fetch_zhihu() {
    log_info "获取知乎热榜..."
    local output="$DATA_DIR/zhihu_${DATE}_${TIME}.json"
    
    if [[ "$USE_REAL_API" == "true" ]]; then
        local url="https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"
        if fetch_url "$url" "$output.tmp"; then
            if jq -e '.data' "$output.tmp" > /dev/null 2>&1; then
                jq '{platform: "zhihu", date: "'$DATE'", time: "'$TIME'", source: "real", data: [.data[] | {rank: .detail_index, title: .target.title, hot_value: .detail_text | gsub("[^0-9]"; "") | tonumber, answers: .target.answer_count}]} | .data |= .[:10]' "$output.tmp" > "$output"
                rm -f "$output.tmp"
                log_info "知乎热榜(真实数据)已保存"
                return
            fi
        fi
        log_warn "真实API获取失败，使用模拟数据"
    fi
    
    cat > "$output" << 'HTMLEOF'
{
  "platform": "zhihu",
  "date": "DATE_PLACEHOLDER",
  "time": "TIME_PLACEHOLDER",
  "source": "demo",
  "data": [
    {"rank": 1, "title": "如何评价最新的AI技术发展？", "hot_value": 1234567, "answers": 234},
    {"rank": 2, "title": "有什么值得推荐的书籍？", "hot_value": 987654, "answers": 567},
    {"rank": 3, "title": "工作中遇到瓶颈怎么办？", "hot_value": 876543, "answers": 123},
    {"rank": 4, "title": "如何提高学习效率？", "hot_value": 765432, "answers": 456},
    {"rank": 5, "title": "有哪些相见恨晚的生活技巧？", "hot_value": 654321, "answers": 789},
    {"rank": 6, "title": "理财入门有哪些建议？", "hot_value": 543210, "answers": 321},
    {"rank": 7, "title": "如何保持健康的生活方式？", "hot_value": 432109, "answers": 654},
    {"rank": 8, "title": "有哪些适合年轻人的职业方向？", "hot_value": 321098, "answers": 987},
    {"rank": 9, "title": "如何评价最近的热门电影？", "hot_value": 210987, "answers": 111},
    {"rank": 10, "title": "科技改变生活的例子有哪些？", "hot_value": 109876, "answers": 222}
  ]
}
HTMLEOF
    sed -i "s/DATE_PLACEHOLDER/$DATE/g; s/TIME_PLACEHOLDER/$TIME/g" "$output"
    log_info "知乎热榜(演示数据)已保存: $output"
}

# 获取抖音热搜
fetch_douyin() {
    log_info "获取抖音热搜..."
    local output="$DATA_DIR/douyin_${DATE}_${TIME}.json"
    
    if [[ "$USE_REAL_API" == "true" ]]; then
        # 使用第三方聚合API
        local url="https://api.oioweb.cn/api/toutiao/douyinHot"
        if fetch_url "$url" "$output.tmp"; then
            if jq -e '.result' "$output.tmp" > /dev/null 2>&1; then
                jq '{platform: "douyin", date: "'$DATE'", time: "'$TIME'", source: "real", data: [.result[] | {rank: .index, title: .name, play_count: .hot, author: "热门创作者"}]} | .data |= .[:10]' "$output.tmp" > "$output"
                rm -f "$output.tmp"
                log_info "抖音热搜(真实数据)已保存"
                return
            fi
        fi
        log_warn "真实API获取失败，使用模拟数据"
    fi
    
    cat > "$output" << 'HTMLEOF'
{
  "platform": "douyin",
  "date": "DATE_PLACEHOLDER",
  "time": "TIME_PLACEHOLDER",
  "source": "demo",
  "data": [
    {"rank": 1, "title": "热门舞蹈挑战", "play_count": 12345678, "author": "热门创作者"},
    {"rank": 2, "title": "搞笑段子合集", "play_count": 9876543, "author": "搞笑达人"},
    {"rank": 3, "title": "美食制作教程", "play_count": 8765432, "author": "美食博主"},
    {"rank": 4, "title": "旅行Vlog分享", "play_count": 7654321, "author": "旅行达人"},
    {"rank": 5, "title": "健身教学视频", "play_count": 6543210, "author": "健身教练"},
    {"rank": 6, "title": "萌宠日常记录", "play_count": 5432109, "author": "萌宠博主"},
    {"rank": 7, "title": "音乐翻唱作品", "play_count": 4321098, "author": "音乐人"},
    {"rank": 8, "title": "科技产品测评", "play_count": 3210987, "author": "科技博主"},
    {"rank": 9, "title": "时尚穿搭分享", "play_count": 2109876, "author": "时尚达人"},
    {"rank": 10, "title": "知识科普内容", "play_count": 1098765, "author": "知识博主"}
  ]
}
HTMLEOF
    sed -i "s/DATE_PLACEHOLDER/$DATE/g; s/TIME_PLACEHOLDER/$TIME/g" "$output"
    log_info "抖音热搜(演示数据)已保存: $output"
}

# 主函数
main() {
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    echo -e "${BLUE}   🔥 热点聚合监控 v2.0${NC}"
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    log_info "开始获取热点数据..."
    log_info "平台: $PLATFORM | 模式: $([ "$USE_REAL_API" == "true" ] && echo "真实API" || echo "演示数据")"
    echo ""
    
    case "$PLATFORM" in
        weibo)   fetch_weibo ;;
        baidu)   fetch_baidu ;;
        zhihu)   fetch_zhihu ;;
        douyin)  fetch_douyin ;;
        all)
            fetch_weibo
            fetch_baidu
            fetch_zhihu
            fetch_douyin
            ;;
        *)
            log_error "未知平台: $PLATFORM"
            echo "支持的平台: weibo, baidu, zhihu, douyin, all"
            exit 1
            ;;
    esac
    
    echo ""
    log_info "✅ 热点数据获取完成！"
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
}

main
