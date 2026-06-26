#!/bin/bash
################################################################################
# OpenClaw Team Builder v3.5 (Skill Edition)
# 适配 OpenClaw 2026.3.x | ClawhHub Skill 标准
#
# 双模式运行：
#   - TUI 模式（默认）：交互式菜单，人类直接使用
#   - CLI 模式：全参数化，AI Agent 调用
#
# 使用：
#   bash team-builder.sh                    # TUI 交互菜单
#   bash team-builder.sh --tree [--json]    # CLI 模式
################################################################################

set -e

# ── 基础设施 ──
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; MAGENTA='\033[0;35m'
BOLD='\033[1m'; DIM='\033[2m'; NC='\033[0m'

info()    { $JSON_OUTPUT && return; echo -e "${BLUE}  ℹ${NC} $1"; }
ok()      { $JSON_OUTPUT && return; echo -e "${GREEN}  ✓${NC} $1"; }
warn()    { $JSON_OUTPUT && return; echo -e "${YELLOW}  ⚠${NC} $1"; }
fail()    { $JSON_OUTPUT && return; echo -e "${RED}  ✗${NC} $1"; }
header()  { $JSON_OUTPUT && return; echo -e "\n${CYAN}${BOLD}$1${NC}"; }
note()    { $JSON_OUTPUT && return; echo -e "  ${DIM}$1${NC}"; }
divider() { $JSON_OUTPUT && return; echo -e "${DIM}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"; }
blank()   { $JSON_OUTPUT && return; echo ""; }

export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
OPENCLAW_DIR="$HOME/.openclaw"
CONFIG_FILE="$OPENCLAW_DIR/openclaw.json"
HIERARCHY_FILE="$OPENCLAW_DIR/team-hierarchy.json"
BACKUP_DIR="$OPENCLAW_DIR/backups"
FIXES_FILE="/tmp/openclaw-fixes-$$.txt"

# ── 全局标志 ──
JSON_OUTPUT=false
AUTO_YES=false
# batch 模式参数
B_ID="" B_NAME="" B_EMOJI="" B_ROLE="" B_PARENT=""
B_SOUL="auto" B_MODEL="" B_FEISHU_APPID="" B_FEISHU_SECRET=""
B_ROLLBACK_INDEX=""
B_GOAL=""

# ── 环境检查 ──
preflight() {
    local errors=0
    command -v openclaw &>/dev/null || { fail "找不到 openclaw 命令"; errors=1; }
    [ -f "$CONFIG_FILE" ] || { fail "找不到 $CONFIG_FILE"; errors=1; }
    command -v python3 &>/dev/null || { fail "找不到 python3"; errors=1; }
    if [ "$errors" -gt 0 ]; then
        exit 1
    fi
}

# ── 版本兼容性检查 ──
# 最低要求 OpenClaw 2026.3.0；解析 "2026.3.2" 格式
MIN_MAJOR=2026 MIN_MINOR=3 MIN_PATCH=0

check_version() {
    local ver
    ver=$(openclaw --version 2>/dev/null | head -1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
    if [ -z "$ver" ]; then
        warn "无法获取 OpenClaw 版本号，跳过兼容性检查"
        return 0
    fi

    local major minor patch
    major=$(echo "$ver" | cut -d. -f1)
    minor=$(echo "$ver" | cut -d. -f2)
    patch=$(echo "$ver" | cut -d. -f3)
    major=${major:-0}; minor=${minor:-0}; patch=${patch:-0}

    local compatible=true
    if [ "$major" -lt "$MIN_MAJOR" ] 2>/dev/null; then
        compatible=false
    elif [ "$major" -eq "$MIN_MAJOR" ] 2>/dev/null; then
        if [ "$minor" -lt "$MIN_MINOR" ] 2>/dev/null; then
            compatible=false
        elif [ "$minor" -eq "$MIN_MINOR" ] && [ "$patch" -lt "$MIN_PATCH" ] 2>/dev/null; then
            compatible=false
        fi
    fi

    if [ "$compatible" = "false" ]; then
        if $JSON_OUTPUT; then
            echo "{\"error\":\"version_incompatible\",\"current\":\"$ver\",\"minimum\":\"$MIN_MAJOR.$MIN_MINOR.$MIN_PATCH\"}"
        else
            echo ""
            fail "OpenClaw 版本不兼容！"
            echo -e "    当前版本: ${RED}$ver${NC}"
            echo -e "    最低要求: ${GREEN}$MIN_MAJOR.$MIN_MINOR.$MIN_PATCH${NC}"
            echo ""
            info "请运行以下命令升级："
            note "  npm install -g @anthropic-ai/openclaw@latest"
            note "  或参考 https://docs.openclaw.ai/install"
        fi
        exit 1
    fi

    $JSON_OUTPUT || note "OpenClaw $ver ✓"
}

# ══════════════════════════════════════════
# 层级管理（team-hierarchy.json）
# ══════════════════════════════════════════

init_hierarchy() {
    if [ -f "$HIERARCHY_FILE" ]; then
        return 0
    fi

    $JSON_OUTPUT || info "首次运行，正在初始化组织架构..."

    python3 << 'PYEOF'
import json, os, re

config_file = os.path.expanduser("~/.openclaw/openclaw.json")
hierarchy_file = os.path.expanduser("~/.openclaw/team-hierarchy.json")

with open(config_file) as f:
    config = json.load(f)

agents_list = config.get("agents", {}).get("list", [])

hierarchy = {"version": 2, "agents": {}}

for a in agents_list:
    aid = a["id"]
    identity = a.get("identity", {})
    name = identity.get("name", "")
    emoji = identity.get("emoji", "")

    if not name or not emoji:
        workspace = a.get("workspace", "")
        if not workspace and aid == "main":
            workspace = os.path.expanduser("~/clawd")
        if workspace:
            id_file = os.path.join(os.path.expanduser(workspace), "IDENTITY.md")
            if os.path.exists(id_file):
                with open(id_file) as idf:
                    content = idf.read()
                if not name:
                    m = re.search(r'\*\*Name:\*\*\s*(.+)', content)
                    if m:
                        val = m.group(1).strip()
                        if val and not val.startswith("_"):
                            name = val
                if not emoji:
                    m = re.search(r'\*\*Emoji:\*\*\s*(.+)', content)
                    if m:
                        val = m.group(1).strip()
                        if val and not val.startswith("_"):
                            emoji = val

    if not name:
        name = a.get("name", aid)
    if not emoji:
        emoji = "🤖"

    hierarchy["agents"][aid] = {
        "name": name,
        "emoji": emoji,
        "role": "director" if aid == "main" else "worker",
        "reports_to": None if aid == "main" else "main",
        "manages": [],
        "description": ""
    }

for aid, info in hierarchy["agents"].items():
    parent = info["reports_to"]
    if parent and parent in hierarchy["agents"]:
        if aid not in hierarchy["agents"][parent]["manages"]:
            hierarchy["agents"][parent]["manages"].append(aid)

with open(hierarchy_file, "w") as f:
    json.dump(hierarchy, f, indent=2, ensure_ascii=False)

import sys, os
if os.environ.get('JSON_OUTPUT') != 'true':
    print(f"  已检测到 {len(agents_list)} 个 Agent，层级初始化完成")
PYEOF
}

draw_tree() {
    local highlight="${1:-}"
    python3 - "$highlight" << 'PYEOF'
import json, os, sys

highlight = sys.argv[1] if len(sys.argv) > 1 else ""
hierarchy_file = os.path.expanduser("~/.openclaw/team-hierarchy.json")

if not os.path.exists(hierarchy_file):
    print("  (还没有组织架构)")
    sys.exit(0)

with open(hierarchy_file) as f:
    h = json.load(f)

agents = h.get("agents", {})
if not agents:
    print("  (还没有组织架构)")
    sys.exit(0)

roots = [aid for aid, info in agents.items() if info.get("reports_to") is None]

def role_label(role):
    labels = {"director": "管理者", "manager": "管理者", "worker": "执行者"}
    return labels.get(role, "")

def draw_node(aid, prefix="", is_last=True):
    info = agents.get(aid, {})
    connector = "└── " if is_last else "├── "
    emoji = info.get("emoji", "🤖")
    name = info.get("name", aid)
    role = info.get("role", "worker")
    desc = info.get("description", "")
    rlabel = ""
    manages = info.get("manages", [])
    if manages:
        rlabel = f" ─── {role_label(role)}"
    hl = ""
    hl_end = ""
    if aid == highlight:
        hl = "\033[1;32m"
        hl_end = " ← 新增\033[0m"
    desc_str = f"  \033[2m{desc[:30]}\033[0m" if desc else ""
    print(f"  {prefix}{connector}{hl}{emoji} {name} ({aid}){rlabel}{hl_end}{desc_str}")
    child_prefix = prefix + ("    " if is_last else "│   ")
    for i, child_id in enumerate(manages):
        if child_id in agents:
            draw_node(child_id, child_prefix, i == len(manages) - 1)

for i, root in enumerate(roots):
    info = agents[root]
    emoji = info.get("emoji", "🤖")
    name = info.get("name", root)
    manages = info.get("manages", [])
    rlabel = f" ─── {role_label(info.get('role', 'director'))}" if manages else ""
    print(f"  {emoji} {name} ({root}){rlabel}")
    for j, child_id in enumerate(manages):
        if child_id in agents:
            draw_node(child_id, "", j == len(manages) - 1)

PYEOF
}

draw_tree_json() {
    python3 << 'PYEOF'
import json, os

hierarchy_file = os.path.expanduser("~/.openclaw/team-hierarchy.json")
if not os.path.exists(hierarchy_file):
    print(json.dumps({"agents": {}}))
else:
    with open(hierarchy_file) as f:
        h = json.load(f)
    print(json.dumps(h.get("agents", {}), ensure_ascii=False))
PYEOF
}

list_parents() {
    python3 << 'PYEOF'
import json, os

hierarchy_file = os.path.expanduser("~/.openclaw/team-hierarchy.json")
with open(hierarchy_file) as f:
    h = json.load(f)

agents = h.get("agents", {})
for i, (aid, info) in enumerate(agents.items()):
    emoji = info.get("emoji", "🤖")
    name = info.get("name", aid)
    manages = info.get("manages", [])
    count = f" (当前管理 {len(manages)} 人)" if manages else ""
    print(f"  {i+1}) {emoji} {name} ({aid}){count}")
PYEOF
}

get_parent_id_by_index() {
    local idx="$1"
    python3 - "$idx" << 'PYEOF'
import json, os, sys

idx = int(sys.argv[1]) - 1
hierarchy_file = os.path.expanduser("~/.openclaw/team-hierarchy.json")
with open(hierarchy_file) as f:
    h = json.load(f)

agents = list(h.get("agents", {}).keys())
if 0 <= idx < len(agents):
    print(agents[idx])
PYEOF
}

update_hierarchy() {
    local new_id="$1" new_name="$2" new_emoji="$3" new_desc="$4" parent_id="$5" new_role="$6"
    python3 - "$new_id" "$new_name" "$new_emoji" "$new_desc" "$parent_id" "$new_role" << 'PYEOF'
import json, os, sys

new_id, new_name, new_emoji, new_desc, parent_id, new_role = sys.argv[1:7]
hierarchy_file = os.path.expanduser("~/.openclaw/team-hierarchy.json")

with open(hierarchy_file) as f:
    h = json.load(f)

h["agents"][new_id] = {
    "name": new_name,
    "emoji": new_emoji,
    "role": new_role,
    "reports_to": parent_id,
    "manages": [],
    "description": new_desc
}

if parent_id in h["agents"]:
    manages = h["agents"][parent_id].get("manages", [])
    if new_id not in manages:
        manages.append(new_id)
    h["agents"][parent_id]["manages"] = manages
    if h["agents"][parent_id]["role"] == "worker":
        h["agents"][parent_id]["role"] = "manager"

with open(hierarchy_file, "w") as f:
    json.dump(h, f, indent=2, ensure_ascii=False)
PYEOF
}

remove_from_hierarchy() {
    local aid="$1"
    python3 - "$aid" << 'PYEOF'
import json, os, sys

aid = sys.argv[1]
hierarchy_file = os.path.expanduser("~/.openclaw/team-hierarchy.json")

with open(hierarchy_file) as f:
    h = json.load(f)

if aid in h["agents"]:
    parent = h["agents"][aid].get("reports_to")
    if parent and parent in h["agents"]:
        manages = h["agents"][parent].get("manages", [])
        h["agents"][parent]["manages"] = [m for m in manages if m != aid]
        if not h["agents"][parent]["manages"] and h["agents"][parent]["role"] == "manager":
            h["agents"][parent]["role"] = "worker"
    del h["agents"][aid]

with open(hierarchy_file, "w") as f:
    json.dump(h, f, indent=2, ensure_ascii=False)
PYEOF
}

# ══════════════════════════════════════════
# 备份和回退
# ══════════════════════════════════════════

do_backup() {
    local label="$1"
    local ts
    ts=$(date +%Y%m%d-%H%M%S)
    local bdir="$BACKUP_DIR/$ts"
    mkdir -p "$bdir"

    cp "$CONFIG_FILE" "$bdir/openclaw.json"
    [ -f "$HIERARCHY_FILE" ] && cp "$HIERARCHY_FILE" "$bdir/team-hierarchy.json"

    # 备份所有 workspace 的 SOUL.md
    for ws in "$OPENCLAW_DIR"/workspace-*/; do
        if [ -f "$ws/SOUL.md" ]; then
            local wsname
            wsname=$(basename "$ws")
            mkdir -p "$bdir/$wsname"
            cp "$ws/SOUL.md" "$bdir/$wsname/SOUL.md"
        fi
    done
    # 也备份 main 的 SOUL.md
    local main_ws
    main_ws=$(python3 -c "
import json
c=json.load(open('$CONFIG_FILE'))
for a in c.get('agents',{}).get('list',[]):
    if a['id']=='main':
        print(a.get('workspace','$HOME/clawd'))
        break
" 2>/dev/null)
    if [ -n "$main_ws" ] && [ -f "$main_ws/SOUL.md" ]; then
        mkdir -p "$bdir/main-workspace"
        cp "$main_ws/SOUL.md" "$bdir/main-workspace/SOUL.md"
    fi

    echo "{\"label\":\"$label\",\"timestamp\":\"$ts\",\"created_agents\":[]}" > "$bdir/manifest.json"

    # 清理老备份，保留最近 5 个
    local count
    count=$(ls -1d "$BACKUP_DIR"/*/ 2>/dev/null | wc -l | tr -d ' ')
    if [ "$count" -gt 5 ]; then
        ls -1d "$BACKUP_DIR"/*/ 2>/dev/null | sort | head -n $((count - 5)) | while read -r old; do
            rm -rf "$old"
        done
    fi

    echo "$bdir"
}

record_created_agent() {
    local bdir="$1" aid="$2"
    python3 - "$bdir/manifest.json" "$aid" << 'PYEOF'
import json, sys
mf, aid = sys.argv[1], sys.argv[2]
with open(mf) as f:
    m = json.load(f)
m["created_agents"].append(aid)
with open(mf, "w") as f:
    json.dump(m, f, indent=2, ensure_ascii=False)
PYEOF
}

mode_rollback() {
    header "  回退操作"
    blank

    if [ ! -d "$BACKUP_DIR" ]; then
        fail "没有找到任何备份"
        return
    fi

    local backups
    backups=$(ls -d "$BACKUP_DIR"/*/ 2>/dev/null | sort -r | head -5)

    if [ -z "$backups" ]; then
        fail "没有找到任何备份"
        return
    fi

    local idx=0
    local backup_dirs=()
    while IFS= read -r bdir; do
        idx=$((idx + 1))
        backup_dirs+=("$bdir")
    done <<< "$backups"

    # batch 模式：使用 B_ROLLBACK_INDEX
    local choice
    if [ -n "$B_ROLLBACK_INDEX" ]; then
        choice="$B_ROLLBACK_INDEX"
    else
        echo "  最近的备份："
        blank
        for i in "${!backup_dirs[@]}"; do
            local bdir="${backup_dirs[$i]}"
            local mf="$bdir/manifest.json"
            if [ -f "$mf" ]; then
                local label ts agents_str
                label=$(python3 -c "import json; m=json.load(open('$mf')); print(m.get('label',''))")
                ts=$(python3 -c "import json; m=json.load(open('$mf')); print(m.get('timestamp',''))")
                agents_str=$(python3 -c "import json; m=json.load(open('$mf')); print(', '.join(m.get('created_agents',[])))")
                echo "  $((i+1))) [$ts] $label"
                [ -n "$agents_str" ] && note "    创建了: $agents_str"
            else
                echo "  $((i+1))) $(basename "$bdir")"
            fi
        done
        blank
        read -p "  选择要回退到哪个备份（输入数字，q取消）: " choice
        [ "$choice" = "q" ] || [ -z "$choice" ] && return
    fi

    local selected="${backup_dirs[$((choice - 1))]}"
    if [ -z "$selected" ] || [ ! -d "$selected" ]; then
        fail "无效选择"
        return
    fi

    local mf="$selected/manifest.json"
    if [ -f "$mf" ]; then
        local agents_to_delete
        agents_to_delete=$(python3 -c "import json; m=json.load(open('$mf')); [print(a) for a in m.get('created_agents',[])]")
        if [ -n "$agents_to_delete" ]; then
            if ! $AUTO_YES; then
                echo ""
                warn "将删除以下 Agent："
                echo "$agents_to_delete" | while read -r aid; do
                    echo "    - $aid"
                done
                blank
                read -p "  确认回退？(Y/n) " confirm
                if [[ ! "${confirm:-Y}" =~ ^[Yy]$ ]]; then
                    echo "  已取消"
                    return
                fi
            fi
            echo "$agents_to_delete" | while read -r aid; do
                openclaw agents delete "$aid" --force 2>/dev/null >/dev/null && ok "删除 $aid" || warn "$aid 删除失败（可能已不存在）"
            done
        fi
    fi

    cp "$selected/openclaw.json" "$CONFIG_FILE"
    ok "openclaw.json 已恢复"

    if [ -f "$selected/team-hierarchy.json" ]; then
        cp "$selected/team-hierarchy.json" "$HIERARCHY_FILE"
        ok "team-hierarchy.json 已恢复"
    fi

    # 恢复 SOUL.md
    for ws_bk in "$selected"/workspace-*/; do
        if [ -d "$ws_bk" ] && [ -f "$ws_bk/SOUL.md" ]; then
            local wsname
            wsname=$(basename "$ws_bk")
            local ws_dest="$OPENCLAW_DIR/$wsname"
            if [ -d "$ws_dest" ]; then
                cp "$ws_bk/SOUL.md" "$ws_dest/SOUL.md"
                ok "$wsname/SOUL.md 已恢复"
            fi
        fi
    done

    blank
    ok "回退完成"
    note "运行 openclaw gateway restart 使配置生效"

    if $JSON_OUTPUT; then
        python3 -c "import json; print(json.dumps({'status':'ok','restored_from':'$(basename "$selected")','message':'回退完成'}))"
    fi
}

# ══════════════════════════════════════════
# SOUL 角色模板库
# ══════════════════════════════════════════

get_role_template() {
    local role_key="$1"
    case "$role_key" in
        xingzheng)
            echo "企业行政部专属AI助手。专长：办公后勤/会议组织/差旅安排/员工福利/接待服务。性格细致、周到、热情、专业，像8年行政老主管。回复结构：处理结果 -> 注意事项(表格) -> 下一步行动 -> 可复制的邮件/表单模板。" ;;
        caiwu)
            echo "企业财务部专属AI助手。专长：报销审核/预算管理/发票处理/费用分析/财务报表解读。性格严谨、精确、有原则。回复结构：结论/金额 -> 政策依据 -> 操作步骤 -> 注意事项。红线：不做最终财务决策，大额支出/税务筹划提醒找专业会计师。" ;;
        hr)
            echo "企业人力资源部专属AI助手。专长：招聘支持/入离职办理/考勤管理/薪资答疑/培训组织。性格亲和、耐心、保密意识强。回复结构：处理方案 -> 所需材料清单 -> 时间节点 -> 相关政策。红线：薪资个案信息绝不跨人透露，劳动纠纷建议咨询法务。" ;;
        kefu)
            echo "企业客服部专属AI助手。专长：客户咨询/投诉处理/FAQ维护/工单跟踪/满意度回访。性格温暖、有同理心、解决问题导向。回复结构：问题确认 -> 解决方案 -> 预计时间 -> 跟进承诺。红线：无法确认的问题不瞎承诺，升级给人工并说明原因。" ;;
        yunying)
            echo "企业运营部专属AI助手。专长：数据分析/活动策划/用户增长/竞品监控/渠道运营。性格数据驱动、创意丰富、结果导向。回复结构：数据/结论 -> 洞察/原因 -> 行动建议 -> 预期效果。" ;;
        falv)
            echo "企业法务部专属AI助手。专长：合同审查/合规检查/法律咨询/风险提示。性格严谨、审慎、逻辑清晰。回复结构：风险等级 -> 问题条款 -> 修改建议 -> 法规依据。红线：明确说明是辅助参考，重大法律事项需律师最终确认。" ;;
        neirong)
            echo "企业内容部专属AI助手。专长：文案撰写/社媒运营/内容排期/SEO优化/品牌调性把控。性格有创意、懂传播、对文字敏感。回复结构：文案/方案 -> 投放建议 -> 配图/排版指引 -> 数据预期。" ;;
        shuju)
            echo "企业数据分析专属AI助手。专长：数据清洗/报表生成/趋势分析/异常检测/可视化建议。性格逻辑严密、追求精确。回复结构：核心发现 -> 数据支撑(表格) -> 趋势判断 -> 建议行动。" ;;
        jishu)
            echo "企业IT技术支持专属AI助手。专长：IT运维/故障排查/系统监控/技术文档/安全巡检。性格冷静、高效、对细节敏感。回复结构：故障定位 -> 解决步骤(编号) -> 根因分析 -> 预防建议。" ;;
        *)
            echo "" ;;
    esac
}

show_role_templates() {
    echo -e "  ${BOLD}角色模板库：${NC}"
    echo "  ┌──────────────────────────────────────────────────────┐"
    echo "  │  1) 小行-行政助手     办公后勤/会议/差旅/福利       │"
    echo "  │  2) 小财-财务助手     报销/预算/发票/财务报表       │"
    echo "  │  3) 小人-HR助手       招聘/入离职/考勤/薪资/培训    │"
    echo "  │  4) 小客-客服助手     客户咨询/投诉/FAQ/工单        │"
    echo "  │  5) 小运-运营助手     数据分析/活动策划/用户增长    │"
    echo "  │  6) 小法-法务助手     合同审查/合规/法律咨询        │"
    echo "  │  7) 小编-内容助手     文案/社媒/内容排期/SEO        │"
    echo "  │  8) 小数-数据分析师   数据清洗/报表/趋势分析        │"
    echo "  │  9) 小技-技术支持     IT运维/故障排查/系统监控      │"
    echo "  │  0) 不用模板，我自己填                              │"
    echo "  └──────────────────────────────────────────────────────┘"
}

apply_role_template() {
    local choice="$1"
    case "$choice" in
        1) echo "xingzheng|小行-行政助手|📋|$(get_role_template xingzheng)" ;;
        2) echo "caiwu|小财-财务助手|💰|$(get_role_template caiwu)" ;;
        3) echo "hr|小人-HR助手|👥|$(get_role_template hr)" ;;
        4) echo "kefu|小客-客服助手|💬|$(get_role_template kefu)" ;;
        5) echo "yunying|小运-运营助手|📈|$(get_role_template yunying)" ;;
        6) echo "falv|小法-法务助手|⚖️|$(get_role_template falv)" ;;
        7) echo "neirong|小编-内容助手|✍️|$(get_role_template neirong)" ;;
        8) echo "shuju|小数-数据分析师|📊|$(get_role_template shuju)" ;;
        9) echo "jishu|小技-技术支持|🔧|$(get_role_template jishu)" ;;
        *) echo "" ;;
    esac
}

list_templates_json() {
    python3 << 'PYEOF'
import json
templates = [
    {"key": "xingzheng", "id": "xingzheng", "name": "小行-行政助手", "emoji": "📋", "focus": "办公后勤/会议/差旅/福利"},
    {"key": "caiwu", "id": "caiwu", "name": "小财-财务助手", "emoji": "💰", "focus": "报销/预算/发票/财务报表"},
    {"key": "hr", "id": "hr", "name": "小人-HR助手", "emoji": "👥", "focus": "招聘/入离职/考勤/薪资/培训"},
    {"key": "kefu", "id": "kefu", "name": "小客-客服助手", "emoji": "💬", "focus": "客户咨询/投诉/FAQ/工单"},
    {"key": "yunying", "id": "yunying", "name": "小运-运营助手", "emoji": "📈", "focus": "数据分析/活动策划/用户增长"},
    {"key": "falv", "id": "falv", "name": "小法-法务助手", "emoji": "⚖️", "focus": "合同审查/合规/法律咨询"},
    {"key": "neirong", "id": "neirong", "name": "小编-内容助手", "emoji": "✍️", "focus": "文案/社媒/内容排期/SEO"},
    {"key": "shuju", "id": "shuju", "name": "小数-数据分析师", "emoji": "📊", "focus": "数据清洗/报表/趋势分析"},
    {"key": "jishu", "id": "jishu", "name": "小技-技术支持", "emoji": "🔧", "focus": "IT运维/故障排查/系统监控"},
]
print(json.dumps(templates, ensure_ascii=False))
PYEOF
}

# ══════════════════════════════════════════
# 目标驱动团队推荐 (--suggest)
# ══════════════════════════════════════════

# 预定义团队场景
mode_suggest() {
    local goal="${B_GOAL:-}"

    if [ -z "$goal" ]; then
        if $JSON_OUTPUT; then
            echo '{"error":"missing_goal","message":"--goal 参数必填"}'
            exit 1
        fi
        fail "--suggest 需要 --goal 参数"
        note "用法: $0 --suggest --goal \"你的业务目标\""
        exit 1
    fi

    # 关键词匹配引擎
    local _json_flag="false"
    $JSON_OUTPUT && _json_flag="true"
    python3 - "$goal" "$_json_flag" << 'PYEOF'
import json, sys, re

goal = sys.argv[1].lower()
json_mode = sys.argv[2] == "true"

# 场景定义：关键词 → 推荐模板组合
SCENARIOS = {
    "ecommerce": {
        "keywords": ["电商", "商城", "网店", "淘宝", "天猫", "shopify", "ecommerce", "shop", "卖货", "零售"],
        "name": "电商团队",
        "agents": [
            {"id": "kefu", "template": "kefu", "reason": "处理客户咨询和售后"},
            {"id": "yunying", "template": "yunying", "reason": "运营数据分析和活动策划"},
            {"id": "neirong", "template": "neirong", "reason": "产品文案和营销内容"},
            {"id": "shuju", "template": "shuju", "reason": "销售数据报表和趋势分析"},
        ]
    },
    "content": {
        "keywords": ["内容", "自媒体", "公众号", "博客", "短视频", "content", "media", "写作", "创作"],
        "name": "内容创作团队",
        "agents": [
            {"id": "neirong", "template": "neirong", "reason": "内容创作和排期管理"},
            {"id": "shuju", "template": "shuju", "reason": "内容数据分析和效果追踪"},
            {"id": "yunying", "template": "yunying", "reason": "渠道运营和用户增长"},
        ]
    },
    "devteam": {
        "keywords": ["开发", "研发", "编程", "软件", "代码", "dev", "code", "技术团队", "工程"],
        "name": "研发团队",
        "agents": [
            {"id": "jishu", "template": "jishu", "reason": "技术架构和运维支持"},
            {"id": "shuju", "template": "shuju", "reason": "数据分析和监控"},
            {"id": "neirong", "template": "neirong", "reason": "技术文档和API文档"},
        ]
    },
    "startup": {
        "keywords": ["创业", "startup", "公司", "企业", "团队管理", "管理"],
        "name": "创业公司团队",
        "agents": [
            {"id": "xingzheng", "template": "xingzheng", "reason": "行政后勤和日程管理"},
            {"id": "caiwu", "template": "caiwu", "reason": "财务管理和报销审批"},
            {"id": "hr", "template": "hr", "reason": "招聘和人事管理"},
            {"id": "falv", "template": "falv", "reason": "合同审查和法律咨询"},
        ]
    },
    "consulting": {
        "keywords": ["咨询", "顾问", "服务", "客户", "consulting", "律所", "会计"],
        "name": "专业服务团队",
        "agents": [
            {"id": "kefu", "template": "kefu", "reason": "客户接待和需求对接"},
            {"id": "falv", "template": "falv", "reason": "专业合规和法律支持"},
            {"id": "xingzheng", "template": "xingzheng", "reason": "日程和文件管理"},
            {"id": "shuju", "template": "shuju", "reason": "案例数据分析"},
        ]
    },
    "solo": {
        "keywords": ["超级个体", "一人公司", "自由职业", "独立", "solo", "freelance", "个人"],
        "name": "超级个体团队",
        "agents": [
            {"id": "solo-dev", "template": None, "reason": "全栈开发", "name": "全栈工程师", "emoji": "💻"},
            {"id": "solo-design", "template": None, "reason": "UI/UX设计", "name": "设计师", "emoji": "🎨"},
            {"id": "solo-content", "template": None, "reason": "内容创作", "name": "内容专家", "emoji": "✍️"},
            {"id": "solo-data", "template": None, "reason": "数据分析", "name": "数据分析", "emoji": "📊"},
        ]
    },
}

# 匹配场景
matched = []
for key, scenario in SCENARIOS.items():
    score = sum(1 for kw in scenario["keywords"] if kw in goal)
    if score > 0:
        matched.append((score, key, scenario))

matched.sort(key=lambda x: -x[0])

if not matched:
    # 无匹配 → 返回通用建议
    result = {
        "goal": goal,
        "matched_scenario": None,
        "message": "未匹配到预设场景，建议从模板库中选择",
        "available_templates": ["xingzheng", "caiwu", "hr", "kefu", "yunying", "falv", "neirong", "shuju", "jishu"],
        "tip": "使用 --templates --json 查看所有模板详情"
    }
else:
    best = matched[0]
    scenario = best[2]
    agents = scenario["agents"]

    # 生成部署命令
    cmds = []
    for a in agents:
        if a.get("template"):
            cmds.append(f"$TB --add --id {a['id']} --soul template:{a['template']} --parent main --yes")
        else:
            name = a.get("name", a["id"])
            emoji = a.get("emoji", "🤖")
            cmds.append(f"$TB --add --id {a['id']} --name \"{name}\" --emoji \"{emoji}\" --role \"{a['reason']}\" --parent main --yes")

    result = {
        "goal": goal,
        "matched_scenario": best[1],
        "scenario_name": scenario["name"],
        "recommended_agents": agents,
        "deploy_commands": cmds,
        "total_agents": len(agents),
    }

    # 如果有其他匹配，也列出
    if len(matched) > 1:
        result["alternative_scenarios"] = [
            {"key": m[1], "name": m[2]["name"], "agents": len(m[2]["agents"])}
            for m in matched[1:3]
        ]

if json_mode:
    print(json.dumps(result, ensure_ascii=False, indent=2))
else:
    if result.get("matched_scenario"):
        print(f"\n  推荐团队：{result['scenario_name']}")
        print(f"  目标：{goal}")
        print(f"  匹配场景：{result['matched_scenario']}")
        print()
        for a in result["recommended_agents"]:
            tpl = a.get("template") or "自定义"
            emoji = a.get("emoji", "🤖")
            print(f"    {emoji} {a['id']} — {a['reason']} (模板: {tpl})")
        print()
        print("  部署命令：")
        for cmd in result["deploy_commands"]:
            print(f"    {cmd}")
        print()
    else:
        print(f"\n  未匹配到预设场景: {goal}")
        print("  建议使用 --templates 查看可用角色模板")
        print()
PYEOF
}

# ══════════════════════════════════════════
# 生成 SOUL.md
# ══════════════════════════════════════════

generate_soul() {
    local aid="$1" aname="$2" arole="$3" parent_id="$4" workspace="$5"

    local parent_name=""
    if [ -n "$parent_id" ] && [ -f "$HIERARCHY_FILE" ]; then
        parent_name=$(python3 -c "
import json
h=json.load(open('$HIERARCHY_FILE'))
a=h.get('agents',{}).get('$parent_id',{})
print(a.get('name','$parent_id'))
" 2>/dev/null)
    fi

    local subordinates=""
    if [ -f "$HIERARCHY_FILE" ]; then
        subordinates=$(python3 -c "
import json
h=json.load(open('$HIERARCHY_FILE'))
a=h.get('agents',{}).get('$aid',{})
manages=a.get('manages',[])
for m in manages:
    mi=h['agents'].get(m,{})
    print(f\"- {mi.get('emoji','🤖')} {mi.get('name',m)} ({m})\")
" 2>/dev/null)
    fi

    cat > "$workspace/SOUL.md" << SOULEOF
# $aname

## 你是谁

你是 **$aname**，一位专业的数字员工。

## 职责

$arole

## 组织关系
$(if [ -n "$parent_name" ]; then
    echo "
- 你的上级是 **$parent_name**
- 完成任务后向上级汇报结果
- 遇到超出能力范围的问题，及时反馈给上级
- 可以通过 agentToAgent 向其他同事请求协助"
else
    echo "
- 你是团队的最高管理者
- 负责接收任务，判断交给谁处理
- 简单问题自己回答，专业问题分配给下属
- 汇总下属的工作结果，整合后回复用户"
fi)
$(if [ -n "$subordinates" ]; then
    echo "
## 你的团队

$subordinates

管理原则：
- 收到任务后判断交给哪个下属最合适
- 追踪任务进度，汇总结果
- 下属遇到困难时提供支持"
fi)

## 性格

- 专业专注，精通自己的领域
- 结果导向，关注业务产出
- 简洁高效，用数据说话

## 沟通风格

- 永远用中文回复
- 回复结构清晰：结论先行，再给细节
- 遇到不确定的事情主动说明，不编造
SOULEOF
}

update_parent_soul() {
    local parent_id="$1"
    if [ "$parent_id" = "main" ]; then
        local workspace
        workspace=$(python3 -c "
import json
c=json.load(open('$CONFIG_FILE'))
for a in c.get('agents',{}).get('list',[]):
    if a['id']=='main':
        print(a.get('workspace','$HOME/clawd'))
        break
" 2>/dev/null)
        if [ -n "$workspace" ] && [ -d "$workspace" ]; then
            local parent_name parent_role
            parent_name=$(python3 -c "import json; h=json.load(open('$HIERARCHY_FILE')); print(h['agents'].get('main',{}).get('name','main'))" 2>/dev/null)
            parent_role=$(python3 -c "import json; h=json.load(open('$HIERARCHY_FILE')); print(h['agents'].get('main',{}).get('description','统筹全局，协调团队'))" 2>/dev/null)
            generate_soul "main" "$parent_name" "${parent_role:-统筹全局，协调团队}" "" "$workspace"
        fi
    else
        local workspace="$OPENCLAW_DIR/workspace-$parent_id"
        if [ -d "$workspace" ]; then
            local parent_name parent_role parent_parent
            parent_name=$(python3 -c "import json; h=json.load(open('$HIERARCHY_FILE')); print(h['agents'].get('$parent_id',{}).get('name','$parent_id'))" 2>/dev/null)
            parent_role=$(python3 -c "import json; h=json.load(open('$HIERARCHY_FILE')); print(h['agents'].get('$parent_id',{}).get('description',''))" 2>/dev/null)
            parent_parent=$(python3 -c "import json; h=json.load(open('$HIERARCHY_FILE')); print(h['agents'].get('$parent_id',{}).get('reports_to','') or '')" 2>/dev/null)
            generate_soul "$parent_id" "$parent_name" "$parent_role" "$parent_parent" "$workspace"
        fi
    fi
}

# ══════════════════════════════════════════
# Channel 自适应 Binding
# ══════════════════════════════════════════

auto_bind_channels() {
    local aid="$1"
    local channels
    channels=$(openclaw config get channels --json 2>/dev/null | python3 -c "
import json, sys
try:
    channels = json.load(sys.stdin)
    for name, cfg in channels.items():
        if isinstance(cfg, dict) and cfg.get('enabled', False):
            print(name)
except:
    pass" 2>/dev/null)

    if [ -z "$channels" ]; then
        return 0
    fi

    local bound_ok=""
    local bound_fail=""

    for ch in $channels; do
        local result
        case "$ch" in
            feishu)
                result=$(openclaw agents bind --agent "$aid" --bind "feishu:$aid" --json 2>&1) || true
                ;;
            *)
                result=$(openclaw agents bind --agent "$aid" --bind "$ch" --json 2>&1) || true
                ;;
        esac
        if echo "$result" | grep -qi "conflict\|error\|fail"; then
            bound_fail="$bound_fail $ch"
        else
            bound_ok="$bound_ok $ch"
        fi
    done

    # Output binding summary (visible in script output, AI can forward to user)
    if [ -n "$bound_ok" ]; then
        echo "  BIND_OK:$bound_ok"
    fi
    if [ -n "$bound_fail" ]; then
        echo "  BIND_NEED_BOT:$bound_fail"
        echo "  NOTE: 以上渠道需要为 $aid 创建独立 bot。"
        echo "  Telegram: 找 @BotFather 发 /newbot 获取 token"
        echo "  Discord: Developer Portal 创建 Application 获取 token"
        echo "  飞书: 开放平台创建应用获取 App ID + Secret"
        echo "  然后执行: \$TB --channels --agent $aid --channel <渠道> --token <token> --yes"
    fi
}

# ══════════════════════════════════════════
# Channel 管理
# ══════════════════════════════════════════

mode_channels() {
    local agent_filter="${B_AGENT:-}"
    local feishu_appid="${B_FEISHU_APPID:-}"
    local feishu_secret="${B_FEISHU_SECRET:-}"
    local channel_name="${B_CHANNEL:-}"
    local channel_token="${B_TOKEN:-}"

    # Action: add a channel bot for an agent
    if [ -n "$channel_name" ] && [ -n "$agent_filter" ]; then
        case "$channel_name" in
            feishu)
                if [ -z "$feishu_appid" ] || [ -z "$feishu_secret" ]; then
                    fail "飞书需要 --feishu-app-id 和 --feishu-secret"; return 1
                fi
                if ! $AUTO_YES; then
                    read -p "  为 $agent_filter 配置飞书账号？(y/n) " yn
                    [ "$yn" != "y" ] && [ "$yn" != "Y" ] && return
                fi
                do_backup
                openclaw config set --json "channels.feishu.accounts.$agent_filter" \
                    "{\"appId\":\"$feishu_appid\",\"appSecret\":\"$feishu_secret\"}" 2>/dev/null
                openclaw agents bind --agent "$agent_filter" --bind "feishu:$agent_filter" --json 2>/dev/null >/dev/null || true
                if $JSON_OUTPUT; then
                    echo "{\"action\":\"channel_configured\",\"channel\":\"feishu\",\"agent\":\"$agent_filter\",\"status\":\"ok\"}"
                else
                    ok "已为 $agent_filter 配置飞书独立账号并绑定"
                fi
                ;;
            telegram|discord)
                if [ -z "$channel_token" ]; then
                    fail "$channel_name 需要 --token <bot-token>"; return 1
                fi
                if ! $AUTO_YES; then
                    read -p "  为 $agent_filter 添加 $channel_name bot？(y/n) " yn
                    [ "$yn" != "y" ] && [ "$yn" != "Y" ] && return
                fi
                do_backup
                openclaw channels add --channel "$channel_name" --token "$channel_token" --account "$agent_filter" 2>/dev/null
                openclaw agents bind --agent "$agent_filter" --bind "$channel_name:$agent_filter" --json 2>/dev/null >/dev/null || true
                if $JSON_OUTPUT; then
                    echo "{\"action\":\"channel_configured\",\"channel\":\"$channel_name\",\"agent\":\"$agent_filter\",\"status\":\"ok\"}"
                else
                    ok "已为 $agent_filter 添加 $channel_name bot 并绑定"
                fi
                ;;
            *)
                if [ -z "$channel_token" ]; then
                    fail "$channel_name 需要 --token <token>"; return 1
                fi
                if ! $AUTO_YES; then
                    read -p "  为 $agent_filter 配置 $channel_name？(y/n) " yn
                    [ "$yn" != "y" ] && [ "$yn" != "Y" ] && return
                fi
                do_backup
                openclaw channels add --channel "$channel_name" --token "$channel_token" --account "$agent_filter" 2>/dev/null
                openclaw agents bind --agent "$agent_filter" --bind "$channel_name:$agent_filter" --json 2>/dev/null >/dev/null || true
                if $JSON_OUTPUT; then
                    echo "{\"action\":\"channel_configured\",\"channel\":\"$channel_name\",\"agent\":\"$agent_filter\",\"status\":\"ok\"}"
                else
                    ok "已为 $agent_filter 配置 $channel_name 并绑定"
                fi
                ;;
        esac
        return
    fi

    # Legacy: feishu-only shorthand (backward compat)
    if [ -n "$feishu_appid" ] && [ -n "$feishu_secret" ] && [ -n "$agent_filter" ]; then
        B_CHANNEL="feishu"
        channel_name="feishu"
        mode_channels
        return
    fi

    if $JSON_OUTPUT; then
        python3 - "$agent_filter" << 'PYEOF'
import json, os, sys

agent_filter = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else ""

config_file = os.path.expanduser("~/.openclaw/openclaw.json")
with open(config_file) as f:
    c = json.load(f)

channels_cfg = c.get("channels", {})
channels = {}
for name, cfg in channels_cfg.items():
    if isinstance(cfg, dict):
        enabled = cfg.get("enabled", False)
        ch_type = "per-agent" if name == "feishu" else "shared"
        accounts = cfg.get("accounts", {}) if name == "feishu" else {}
        channels[name] = {"enabled": enabled, "type": ch_type, "accounts": list(accounts.keys())}

bindings_raw = c.get("bindings", [])
agents_list = c.get("agents", {}).get("list", [])
enabled_channels = [ch for ch, info in channels.items() if info["enabled"]]

agents = []
for a in agents_list:
    aid = a["id"]
    if agent_filter and aid != agent_filter:
        continue
    ident = a.get("identity", {})
    name = ident.get("name", a.get("name", aid))
    agent_binds = []
    for b in bindings_raw:
        if b.get("agentId") == aid:
            agent_binds.append({
                "channel": b.get("match", {}).get("channel", "?"),
                "accountId": b.get("match", {}).get("accountId", "")
            })
    bound_chs = [b["channel"] for b in agent_binds]
    missing = [ch for ch in enabled_channels if ch not in bound_chs]
    agents.append({
        "id": aid, "name": name,
        "bindings": agent_binds,
        "missing_channels": missing
    })

result = {"channels": channels, "agents": agents}
print(json.dumps(result, ensure_ascii=False))
PYEOF
        return
    fi

    header "  渠道管理"
    blank

    echo -e "  ${BOLD}已配置渠道：${NC}"
    python3 -c "
import json, os
c = json.load(open(os.path.expanduser('~/.openclaw/openclaw.json')))
channels = c.get('channels', {})
for name, cfg in channels.items():
    if isinstance(cfg, dict):
        enabled = '✅' if cfg.get('enabled', False) else '❌'
        ch_type = '独立账号' if name == 'feishu' else '共享'
        accounts = ''
        if name == 'feishu':
            accts = cfg.get('accounts', {})
            if accts:
                accounts = f' (账号: {\", \".join(accts.keys())})'
        print(f'  {enabled} {name:12s} [{ch_type}]{accounts}')
" 2>/dev/null
    blank

    echo -e "  ${BOLD}Agent 绑定情况：${NC}"
    python3 -c "
import json, os
c = json.load(open(os.path.expanduser('~/.openclaw/openclaw.json')))
agents = c.get('agents', {}).get('list', [])
bindings = c.get('bindings', [])
channels = c.get('channels', {})
enabled_chs = [ch for ch, cfg in channels.items() if isinstance(cfg, dict) and cfg.get('enabled', False)]

agent_filter = '$agent_filter'
for a in agents:
    aid = a['id']
    if agent_filter and aid != agent_filter:
        continue
    ident = a.get('identity', {})
    name = ident.get('name', a.get('name', aid))
    agent_binds = [b for b in bindings if b.get('agentId') == aid]
    bound_chs = [b.get('match', {}).get('channel', '?') for b in agent_binds]
    missing = [ch for ch in enabled_chs if ch not in bound_chs]
    status = '✅' if not missing else '⚠️'
    print(f'  {status} {name} ({aid})')
    for b in agent_binds:
        ch = b.get('match', {}).get('channel', '?')
        acc = b.get('match', {}).get('accountId', '')
        acc_str = f':{acc}' if acc else ''
        print(f'      ├─ {ch}{acc_str}')
    for m in missing:
        print(f'      ├─ {m} (未绑定)')
    print()
" 2>/dev/null

    divider
    echo -e "  ${BOLD}渠道说明：${NC}"
    echo "  - 每个 Agent 可以有自己独立的 bot（Telegram/Discord/飞书等）"
    echo "  - 共享 bot 只能绑定一个 Agent；需要多 Agent 就需要多个 bot"
    echo ""
    echo -e "  ${BOLD}为 Agent 添加渠道 bot：${NC}"
    echo "    Telegram:  bash $0 --channels --agent <id> --channel telegram --token <bot-token> --yes"
    echo "    Discord:   bash $0 --channels --agent <id> --channel discord --token <bot-token> --yes"
    echo "    飞书:      bash $0 --channels --agent <id> --channel feishu --feishu-app-id <id> --feishu-secret <s> --yes"
    blank
}

# ══════════════════════════════════════════
# 创建 Agent（核心）
# ══════════════════════════════════════════

create_agent_core() {
    local aid="$1" aname="$2" aemoji="$3" arole="$4" parent_id="$5"
    local amodel="$6" f_appid="$7" f_secret="$8" soul_mode="$9"
    local workspace="$OPENCLAW_DIR/workspace-$aid"

    if openclaw agents list 2>/dev/null | grep -q "^- $aid"; then
        echo -e "  ${YELLOW}⏭${NC} $aemoji $aname — 已存在，跳过"
        return 0
    fi

    openclaw agents add "$aid" \
        --workspace "$workspace" \
        --non-interactive \
        $amodel \
        --json 2>/dev/null >/dev/null

    BIND_RESULT=$(auto_bind_channels "$aid" 2>/dev/null)

    openclaw agents set-identity \
        --agent "$aid" \
        --name "$aname" \
        --emoji "$aemoji" \
        --json 2>/dev/null >/dev/null || true

    if [ "$soul_mode" = "auto" ] || [ -z "$soul_mode" ]; then
        generate_soul "$aid" "$aname" "$arole" "$parent_id" "$workspace"
    elif [ "$soul_mode" = "skip" ]; then
        :
    fi

    if [ -n "$f_appid" ] && [ -n "$f_secret" ]; then
        openclaw config set --json \
            "channels.feishu.accounts.$aid" \
            "{\"appId\":\"$f_appid\",\"appSecret\":\"$f_secret\"}" \
            2>/dev/null
    fi

    # agentToAgent
    python3 -c "
import json
with open('$CONFIG_FILE') as f:
    c = json.load(f)
a2a = c.get('tools', {}).get('agentToAgent', {})
allow = a2a.get('allow', [])
for a in c.get('agents', {}).get('list', []):
    if a['id'] not in allow and a['id'] != 'main':
        allow.append(a['id'])
if '$aid' not in allow:
    allow.append('$aid')
a2a['enabled'] = True
a2a['allow'] = allow
c.setdefault('tools', {})['agentToAgent'] = a2a
with open('$CONFIG_FILE', 'w') as f:
    json.dump(c, f, indent=2, ensure_ascii=False)
" 2>/dev/null

    local role_type="worker"
    update_hierarchy "$aid" "$aname" "$aemoji" "$arole" "$parent_id" "$role_type"
    update_parent_soul "$parent_id"

    ok "$aemoji $aname ($aid) → 汇报给 $parent_id"
}

# ══════════════════════════════════════════
# 共用交互
# ══════════════════════════════════════════

choose_model() {
    blank
    echo -e "  ${BOLD}选择 AI 大脑${NC}"
    echo "  ┌─────────────────────────────────────────────────┐"
    echo "  │  1) 继承全局默认（推荐）                        │"
    echo "  │  2) 自己选一个模型                              │"
    echo "  └─────────────────────────────────────────────────┘"
    read -p "  请选择（回车=1）: " _mc
    _mc=${_mc:-1}
    MODEL_ARG=""
    MODEL_DISPLAY="继承全局默认"
    if [ "$_mc" = "2" ]; then
        note "常见：anthropic/claude-sonnet-4-6（均衡）、claude-opus-4-6（最强）、claude-haiku-4-5（最快）"
        read -p "  模型全名: " _model
        [ -n "$_model" ] && MODEL_ARG="--model $_model" && MODEL_DISPLAY="$_model"
    fi
}

choose_soul_mode() {
    blank
    echo -e "  ${BOLD}SOUL.md（角色定义）怎么写？${NC}"
    echo "  ┌──────────────────────────────────────────────────────┐"
    echo "  │  1) 自动生成 — 根据职责描述 + 组织关系自动写  推荐 │"
    echo "  │  2) 从模板库选 — 10个常见角色，专业 SOUL 一键生成  │"
    echo "  │  3) 我自己写 — 创建后你手动编辑 SOUL.md             │"
    echo "  │  4) 先跳过   — 用 OpenClaw 默认模板                 │"
    echo "  └──────────────────────────────────────────────────────┘"
    note "提示：也可以之后让上级 Agent 帮你写下属的 SOUL.md"
    read -p "  请选择（回车=1）: " _sm
    case "${_sm:-1}" in
        1) SOUL_MODE="auto" ;;
        2) SOUL_MODE="template" ;;
        3) SOUL_MODE="custom" ;;
        4) SOUL_MODE="skip" ;;
        *) SOUL_MODE="auto" ;;
    esac
}

# ══════════════════════════════════════════
# 模式：新增单个 Agent（TUI）
# ══════════════════════════════════════════
mode_add() {
    blank
    echo -e "  ${BOLD}${CYAN}── 新增一位员工 ──${NC}"
    blank

    local main_manages
    main_manages=$(python3 -c "
import json
h=json.load(open('$HIERARCHY_FILE'))
print(len(h.get('agents',{}).get('main',{}).get('manages',[])))
" 2>/dev/null)

    if [ "$main_manages" = "0" ]; then
        warn "这是你第一次添加 Agent。"
        echo "  main（你的主 Agent）将自动升级为 CEO 模式 ——"
        echo "  负责接收任务、分配给下属、汇总结果。"
        echo "  main 的 SOUL.md 会相应更新。"
        blank
        read -p "  继续？(Y/n) " _c
        [[ ! "${_c:-Y}" =~ ^[Yy]$ ]] && return
    fi

    header "  当前组织架构"
    blank
    draw_tree
    blank
    divider

    # SOUL 模式先选（影响后续步骤）
    header "  第 1 步：角色定义"
    choose_soul_mode

    local AGENT_ID="" DISPLAY_NAME="" AGENT_EMOJI="" ROLE_DESC=""

    # 如果选了模板，直接填充基本信息
    if [ "$SOUL_MODE" = "template" ]; then
        blank
        show_role_templates
        read -p "  选择角色模板 [0-9]: " _tmpl_choice
        if [ "$_tmpl_choice" != "0" ] && [ -n "$_tmpl_choice" ]; then
            local tmpl_data
            tmpl_data=$(apply_role_template "$_tmpl_choice")
            if [ -n "$tmpl_data" ]; then
                IFS='|' read -r AGENT_ID DISPLAY_NAME AGENT_EMOJI ROLE_DESC <<< "$tmpl_data"
                ok "已加载模板：$AGENT_EMOJI $DISPLAY_NAME"
                blank
                note "可以修改以下信息，回车保持默认"
                SOUL_MODE="auto"  # 模板填充了角色描述，用 auto 生成 SOUL
            fi
        fi
    fi

    header "  第 2 步：工号"
    note "英文 + 短横线，如 finance-lead、translator"
    if [ -n "$AGENT_ID" ]; then
        read -p "  Agent ID [$AGENT_ID]: " _custom_id
        [ -n "$_custom_id" ] && AGENT_ID="$_custom_id"
    else
        read -p "  Agent ID: " AGENT_ID
    fi
    [ -z "$AGENT_ID" ] && { fail "ID 不能为空"; return; }
    if openclaw agents list 2>/dev/null | grep -q "^- $AGENT_ID"; then
        fail "'$AGENT_ID' 已存在"; return
    fi

    header "  第 3 步：名字和头像"
    if [ -n "$DISPLAY_NAME" ]; then
        read -p "  显示名称 [$DISPLAY_NAME]: " _custom_name
        [ -n "$_custom_name" ] && DISPLAY_NAME="$_custom_name"
    else
        read -p "  显示名称: " DISPLAY_NAME
        DISPLAY_NAME=${DISPLAY_NAME:-$AGENT_ID}
    fi
    if [ -n "$AGENT_EMOJI" ]; then
        read -p "  Emoji [$AGENT_EMOJI]: " _custom_emoji
        [ -n "$_custom_emoji" ] && AGENT_EMOJI="$_custom_emoji"
    else
        read -p "  Emoji [🤖]: " AGENT_EMOJI
        AGENT_EMOJI=${AGENT_EMOJI:-"🤖"}
    fi

    header "  第 4 步：职责描述"
    if [ -n "$ROLE_DESC" ]; then
        note "模板已填充，回车保持或输入新内容覆盖"
        read -p "  职责: " _custom_role
        [ -n "$_custom_role" ] && ROLE_DESC="$_custom_role"
    else
        note "一两句话，如「负责财务报表和预算管理」"
        read -p "  职责: " ROLE_DESC
        ROLE_DESC=${ROLE_DESC:-"通用AI助手"}
    fi

    header "  第 5 步：挂在谁下面？"
    blank
    list_parents
    blank
    read -p "  选择上级（输入数字）: " PARENT_IDX
    PARENT_ID=$(get_parent_id_by_index "${PARENT_IDX:-1}")
    [ -z "$PARENT_ID" ] && { fail "无效选择"; return; }

    header "  第 6 步：AI 大脑"
    choose_model

    header "  第 7 步：飞书（可跳过）"
    echo "  ┌──────────────────────────────┐"
    echo "  │  1) 先跳过（推荐）           │"
    echo "  │  2) 现在配置                 │"
    echo "  └──────────────────────────────┘"
    read -p "  选择（回车=1）: " _fc
    local f_appid="" f_secret=""
    if [ "${_fc:-1}" = "2" ]; then
        read -p "  App ID (cli_xxx): " f_appid
        read -s -p "  App Secret: " f_secret
        echo ""
    fi

    # 预览
    header "  添加后的架构预览"
    blank
    python3 - "$AGENT_ID" "$DISPLAY_NAME" "$AGENT_EMOJI" "$ROLE_DESC" "$PARENT_ID" << 'PYEOF'
import json, os, sys, copy

new_id, new_name, new_emoji, new_desc, parent_id = sys.argv[1:6]
hierarchy_file = os.path.expanduser("~/.openclaw/team-hierarchy.json")

with open(hierarchy_file) as f:
    h = json.load(f)

preview = copy.deepcopy(h)
preview["agents"][new_id] = {
    "name": new_name, "emoji": new_emoji, "role": "worker",
    "reports_to": parent_id, "manages": [], "description": new_desc
}
if parent_id in preview["agents"]:
    preview["agents"][parent_id]["manages"].append(new_id)

agents = preview["agents"]
roots = [aid for aid, info in agents.items() if info.get("reports_to") is None]

def draw_node(aid, prefix="", is_last=True):
    info = agents.get(aid, {})
    connector = "└── " if is_last else "├── "
    emoji = info.get("emoji", "🤖")
    name = info.get("name", aid)
    manages = info.get("manages", [])
    rlabel = " ─── 管理者" if manages else ""
    hl = "\033[1;32m" if aid == new_id else ""
    hl_end = " ← 新增\033[0m" if aid == new_id else ""
    desc = info.get("description", "")
    desc_str = f"  \033[2m{desc[:30]}\033[0m" if desc and aid == new_id else ""
    print(f"  {prefix}{connector}{hl}{emoji} {name} ({aid}){rlabel}{hl_end}{desc_str}")
    child_prefix = prefix + ("    " if is_last else "│   ")
    for i, child_id in enumerate(manages):
        if child_id in agents:
            draw_node(child_id, child_prefix, i == len(manages) - 1)

for root in roots:
    info = agents[root]
    manages = info.get("manages", [])
    rlabel = " ─── 管理者" if manages else ""
    print(f"  {info.get('emoji','🤖')} {info.get('name',root)} ({root}){rlabel}")
    for j, child_id in enumerate(manages):
        if child_id in agents:
            draw_node(child_id, "", j == len(manages) - 1)
PYEOF

    blank
    read -p "  确认创建？(Y/n) " CONFIRM
    [[ ! "${CONFIRM:-Y}" =~ ^[Yy]$ ]] && { echo "  已取消"; return; }

    local bdir
    bdir=$(do_backup "新增 $DISPLAY_NAME ($AGENT_ID)")

    blank
    info "正在创建..."
    create_agent_core "$AGENT_ID" "$DISPLAY_NAME" "$AGENT_EMOJI" "$ROLE_DESC" \
        "$PARENT_ID" "$MODEL_ARG" "$f_appid" "$f_secret" "$SOUL_MODE"

    record_created_agent "$bdir" "$AGENT_ID"

    blank
    divider
    echo -e "  ${GREEN}${BOLD}入职完成！${NC}"
    blank
    if [ -z "$f_appid" ]; then
        note "飞书补配：openclaw config set --json channels.feishu.accounts.$AGENT_ID '{\"appId\":\"cli_xxx\",\"appSecret\":\"xxx\"}'"
    fi
    if [ "$SOUL_MODE" = "custom" ]; then
        note "记得手动编辑 SOUL.md：~/.openclaw/workspace-$AGENT_ID/SOUL.md"
    fi
    note "生效：openclaw gateway restart"
    blank
}

# ══════════════════════════════════════════
# 模式：新增 Agent（CLI batch 模式）
# ══════════════════════════════════════════
mode_add_batch() {
    [ -z "$B_ID" ] && { echo '{"error":"missing --id"}'; exit 1; }
    [ -z "$B_PARENT" ] && B_PARENT="main"
    [ -z "$B_NAME" ] && B_NAME="$B_ID"
    [ -z "$B_EMOJI" ] && B_EMOJI="🤖"
    [ -z "$B_ROLE" ] && B_ROLE="通用AI助手"

    # 处理 soul 模式：template:key 格式
    local soul_mode="$B_SOUL"
    if [[ "$B_SOUL" == template:* ]]; then
        local tkey="${B_SOUL#template:}"
        local tdesc
        tdesc=$(get_role_template "$tkey")
        if [ -n "$tdesc" ]; then
            B_ROLE="$tdesc"
            soul_mode="auto"
        fi
    fi

    # 检查是否已存在
    if openclaw agents list 2>/dev/null | grep -q "^- $B_ID"; then
        if $JSON_OUTPUT; then
            echo "{\"status\":\"skipped\",\"id\":\"$B_ID\",\"reason\":\"already exists\"}"
        else
            warn "$B_ID 已存在，跳过"
        fi
        return 0
    fi

    local model_arg=""
    [ -n "$B_MODEL" ] && model_arg="--model $B_MODEL"

    local bdir
    bdir=$(do_backup "新增 $B_NAME ($B_ID)")

    create_agent_core "$B_ID" "$B_NAME" "$B_EMOJI" "$B_ROLE" \
        "$B_PARENT" "$model_arg" "$B_FEISHU_APPID" "$B_FEISHU_SECRET" "$soul_mode"

    record_created_agent "$bdir" "$B_ID"

    # Extract bind results from create_agent_core
    local bind_ok bind_need
    bind_ok=$(echo "$BIND_RESULT" | grep "BIND_OK:" | sed 's/.*BIND_OK://' | xargs)
    bind_need=$(echo "$BIND_RESULT" | grep "BIND_NEED_BOT:" | sed 's/.*BIND_NEED_BOT://' | xargs)

    if $JSON_OUTPUT; then
        python3 - "$B_ID" "$B_NAME" "$B_EMOJI" "$B_PARENT" "$soul_mode" "$OPENCLAW_DIR/workspace-$B_ID" "$bind_ok" "$bind_need" << 'PYEOF'
import json, sys
result = {
    'status': 'created',
    'id': sys.argv[1],
    'name': sys.argv[2],
    'emoji': sys.argv[3],
    'parent': sys.argv[4],
    'soul_mode': sys.argv[5],
    'workspace': sys.argv[6],
    'channels_bound': sys.argv[7].split() if sys.argv[7] else [],
    'channels_need_bot': sys.argv[8].split() if sys.argv[8] else [],
    'message': '创建成功，运行 openclaw gateway restart 生效',
    'next_steps': []
}
for ch in result['channels_need_bot']:
    if ch == 'telegram':
        result['next_steps'].append(f'Telegram: 找 @BotFather 创建 bot，获取 token 后执行 --channels --agent {sys.argv[1]} --channel telegram --token <token> --yes')
    elif ch == 'discord':
        result['next_steps'].append(f'Discord: Developer Portal 创建 bot，获取 token 后执行 --channels --agent {sys.argv[1]} --channel discord --token <token> --yes')
    elif ch == 'feishu':
        result['next_steps'].append(f'飞书: 开放平台创建应用，获取凭证后执行 --channels --agent {sys.argv[1]} --channel feishu --feishu-app-id <id> --feishu-secret <s> --yes')
print(json.dumps(result, ensure_ascii=False))
PYEOF
    else
        blank
        ok "入职完成：$B_EMOJI $B_NAME ($B_ID) → $B_PARENT"
        if [ -n "$bind_ok" ]; then
            echo -e "  ${GREEN}渠道已绑定：${NC}$bind_ok"
        fi
        if [ -n "$bind_need" ]; then
            echo -e "  ${YELLOW}需要独立 bot：${NC}$bind_need"
            echo "  Telegram: 找 @BotFather 发 /newbot 获取 token"
            echo "  Discord: Developer Portal 创建 Application 获取 token"
            echo "  飞书: 开放平台创建应用获取 App ID + Secret"
            echo "  配置: bash $0 --channels --agent $B_ID --channel <渠道> --token <token> --yes"
        fi
        note "生效：openclaw gateway restart"
    fi
}

# ══════════════════════════════════════════
# 模式：超级个体模板
# ══════════════════════════════════════════
mode_solo_template() {
    if $AUTO_YES; then
        # batch 模式：直接部署，无交互
        local model_arg=""
        [ -n "$B_MODEL" ] && model_arg="--model $B_MODEL"
        local soul_mode="${B_SOUL:-auto}"

        local bdir
        bdir=$(do_backup "超级个体模板部署")

        local SOLO_AGENTS=(
            "solo-dev|全栈工程师|💻|负责所有开发工作：前端、后端、数据库、部署。快速交付可用的代码。|main"
            "solo-design|设计师|🎨|负责 UI/UX 设计、视觉设计、交互优化。让产品好看又好用。|main"
            "solo-content|内容专家|✍️|负责内容创作：文案、博客、社媒、产品文档。专业但不枯燥。|main"
            "solo-data|数据分析|📊|负责数据分析、报告生成、指标监控。用数据驱动决策。|main"
        )

        local results=()
        for entry in "${SOLO_AGENTS[@]}"; do
            IFS='|' read -r aid aname aemoji adesc aparent <<< "$entry"
            create_agent_core "$aid" "$aname" "$aemoji" "$adesc" "$aparent" \
                "$model_arg" "" "" "$soul_mode"
            record_created_agent "$bdir" "$aid"
            results+=("$aid")
        done

        if $JSON_OUTPUT; then
            python3 -c "
import json
print(json.dumps({
    'status': 'ok',
    'created': $(printf '%s\n' "${results[@]}" | python3 -c "import sys,json; print(json.dumps([l.strip() for l in sys.stdin]))"),
    'message': '超级个体部署完成，运行 openclaw gateway restart 生效'
}, ensure_ascii=False))
"
        else
            ok "超级个体部署完成！创建了 ${#results[@]} 个 Agent"
            note "生效：openclaw gateway restart"
        fi
        return
    fi

    # TUI 模式
    blank
    echo -e "${BOLD}${MAGENTA}"
    echo "  ┌────────────────────────────────────────────────────┐"
    echo "  │                                                    │"
    echo "  │  超级个体模式 — 一人公司的 AI 团队                │"
    echo "  │                                                    │"
    echo "  │  你的 main Agent 自动升级为 CEO，                  │"
    echo "  │  下面挂 4 个专家各管一摊。                         │"
    echo "  │                                                    │"
    echo "  └────────────────────────────────────────────────────┘"
    echo -e "${NC}"

    echo -e "  ${BOLD}参考资料：${NC}"
    note "Orchestrator + Specialists 模式（社区最火，65%+ 生产用户）"
    note "官方文档：https://docs.openclaw.ai/concepts/multi-agent"
    blank
    divider
    blank

    local existing_count
    existing_count=$(python3 -c "
import json
h=json.load(open('$HIERARCHY_FILE'))
manages = h.get('agents',{}).get('main',{}).get('manages',[])
print(len(manages))
" 2>/dev/null)

    if [ "$existing_count" -gt 0 ] 2>/dev/null; then
        warn "main 下面已经有 $existing_count 个 Agent："
        blank
        draw_tree
        blank
        echo -e "  ${BOLD}超级个体模板将在已有架构上追加 4 个专家${NC}"
        echo "  已存在同 ID 的 Agent 会自动跳过"
        blank
        divider
        blank
    fi

    echo -e "  ${BOLD}部署预览（追加后）：${NC}"
    blank
    python3 << 'PYEOF'
import json, os

hierarchy_file = os.path.expanduser("~/.openclaw/team-hierarchy.json")
with open(hierarchy_file) as f:
    h = json.load(f)

agents = h.get("agents", {})
main_info = agents.get("main", {})
main_emoji = main_info.get("emoji", "🤖")
main_name = main_info.get("name", "main")
existing_manages = list(main_info.get("manages", []))

solo = [
    ("solo-dev", "全栈工程师", "💻"),
    ("solo-design", "设计师", "🎨"),
    ("solo-content", "内容专家", "✍️"),
    ("solo-data", "数据分析", "📊"),
]

all_children = list(existing_manages)
for sid, sname, semoji in solo:
    if sid not in all_children:
        all_children.append(sid)

print(f"  {main_emoji} {main_name} (main) ─── CEO / 管理者")
for i, cid in enumerate(all_children):
    is_last = (i == len(all_children) - 1)
    connector = "└── " if is_last else "├── "
    if cid in agents:
        ci = agents[cid]
        print(f"  {connector}{ci.get('emoji','🤖')} {ci.get('name',cid)} ({cid})")
    else:
        for sid, sname, semoji in solo:
            if sid == cid:
                print(f"  {connector}\033[1;32m{semoji} {sname} ({sid}) ← 新增\033[0m")
                break
PYEOF
    blank
    note "已存在同 ID 的 Agent 会自动跳过"
    blank

    choose_model
    choose_soul_mode

    echo "  ┌──────────────────────────────────────┐"
    echo "  │  飞书: 1) 跳过（推荐） 2) 逐个配    │"
    echo "  └──────────────────────────────────────┘"
    read -p "  选择（回车=1）: " FEISHU_MODE
    FEISHU_MODE=${FEISHU_MODE:-1}

    blank
    read -p "  确认部署超级个体团队？(Y/n) " CONFIRM
    [[ ! "${CONFIRM:-Y}" =~ ^[Yy]$ ]] && { echo "  已取消"; return; }

    local bdir
    bdir=$(do_backup "超级个体模板部署")

    blank
    echo -e "  ${BOLD}${GREEN}开始部署...${NC}"
    blank

    local SOLO_AGENTS=(
        "solo-dev|全栈工程师|💻|负责所有开发工作：前端、后端、数据库、部署。快速交付可用的代码。|main"
        "solo-design|设计师|🎨|负责 UI/UX 设计、视觉设计、交互优化。让产品好看又好用。|main"
        "solo-content|内容专家|✍️|负责内容创作：文案、博客、社媒、产品文档。专业但不枯燥。|main"
        "solo-data|数据分析|📊|负责数据分析、报告生成、指标监控。用数据驱动决策。|main"
    )

    local total=${#SOLO_AGENTS[@]}
    local created=0

    for i in "${!SOLO_AGENTS[@]}"; do
        IFS='|' read -r aid aname aemoji adesc aparent <<< "${SOLO_AGENTS[$i]}"
        local num=$((i + 1))
        echo -ne "  ${DIM}[$num/$total]${NC} "

        local f_appid="" f_secret=""
        if [ "$FEISHU_MODE" = "2" ]; then
            echo ""; read -p "    飞书 App ID for $aname: " f_appid
            read -s -p "    App Secret: " f_secret; echo ""
        fi

        create_agent_core "$aid" "$aname" "$aemoji" "$adesc" "$aparent" \
            "$MODEL_ARG" "$f_appid" "$f_secret" "$SOUL_MODE"

        record_created_agent "$bdir" "$aid"
        created=$((created + 1))
    done

    blank
    ok "部署完成！新建 $created 人"
    blank
    if [ "$FEISHU_MODE" != "2" ]; then
        note "飞书补配：openclaw config set --json channels.feishu.accounts.<id> '{\"appId\":\"xxx\",\"appSecret\":\"xxx\"}'"
    fi
    if [ "$SOUL_MODE" = "custom" ]; then
        note "记得编辑每个 Agent 的 SOUL.md"
    fi
    note "生效：openclaw gateway restart"
    note "回退：重新运行脚本选择「回退操作」"
    blank
    show_ops_tips
}

# ══════════════════════════════════════════
# 模式：军团体检
# ══════════════════════════════════════════
mode_checkup() {
    header "  军团体检"
    blank

    local issues=0
    rm -f "$FIXES_FILE"
    touch "$FIXES_FILE"

    # JSON 收集器
    local json_checks="[]"

    add_check() {
        local name="$1" status="$2" detail="$3"
        if $JSON_OUTPUT; then
            json_checks=$(python3 -c "
import json, sys
checks = json.loads(sys.argv[1])
checks.append({'name': sys.argv[2], 'status': sys.argv[3], 'detail': sys.argv[4] if sys.argv[4] else None})
print(json.dumps(checks, ensure_ascii=False))
" "$json_checks" "$name" "$status" "$detail")
        fi
    }

    # 检查 1: Gateway
    if openclaw gateway status &>/dev/null; then
        ok "Gateway 运行中"
        add_check "gateway" "ok" ""
    else
        warn "Gateway 未运行"
        echo "gateway" >> "$FIXES_FILE"
        issues=$((issues + 1))
        add_check "gateway" "warn" "Gateway 未运行"
    fi

    # 检查 2: agentToAgent 通信
    local a2a_enabled
    a2a_enabled=$(python3 -c "
import json
c=json.load(open('$CONFIG_FILE'))
a2a=c.get('tools',{}).get('agentToAgent',{})
print('yes' if a2a.get('enabled') else 'no')
" 2>/dev/null)

    if [ "$a2a_enabled" = "yes" ]; then
        ok "Agent 间通信已开启"
        add_check "a2a_enabled" "ok" ""
    else
        warn "Agent 间通信（agentToAgent）未开启"
        echo "a2a" >> "$FIXES_FILE"
        issues=$((issues + 1))
        add_check "a2a_enabled" "warn" "agentToAgent 未开启"
    fi

    # 检查 3: agentToAgent allow 列表完整性
    local missing_a2a
    missing_a2a=$(python3 -c "
import json
c=json.load(open('$CONFIG_FILE'))
allow=c.get('tools',{}).get('agentToAgent',{}).get('allow',[])
agents=[a['id'] for a in c.get('agents',{}).get('list',[]) if a['id']!='main']
missing=[a for a in agents if a not in allow]
if missing:
    print(' '.join(missing))
" 2>/dev/null)

    if [ -n "$missing_a2a" ]; then
        warn "以下 Agent 不在通信白名单中：$missing_a2a"
        echo "a2a_allow" >> "$FIXES_FILE"
        issues=$((issues + 1))
        add_check "a2a_allow" "warn" "缺失: $missing_a2a"
    else
        ok "通信白名单完整"
        add_check "a2a_allow" "ok" ""
    fi

    # 检查 4: 每个 Agent 的 SOUL.md
    local agent_ids
    agent_ids=$(python3 -c "
import json
c=json.load(open('$CONFIG_FILE'))
for a in c.get('agents',{}).get('list',[]):
    if a['id']!='main':
        print(a['id'])
" 2>/dev/null)

    if [ -n "$agent_ids" ]; then
        while read -r aid; do
            local soul="$OPENCLAW_DIR/workspace-$aid/SOUL.md"
            if [ ! -f "$soul" ]; then
                warn "$aid 缺少 SOUL.md"
                echo "soul:$aid" >> "$FIXES_FILE"
                issues=$((issues + 1))
                add_check "soul:$aid" "warn" "缺少 SOUL.md"
            elif [ "$(wc -l < "$soul" | tr -d ' ')" -lt 5 ]; then
                warn "$aid 的 SOUL.md 内容过少（不到 5 行）"
                echo "soul:$aid" >> "$FIXES_FILE"
                issues=$((issues + 1))
                add_check "soul:$aid" "warn" "SOUL.md 内容过少"
            else
                ok "$aid — SOUL.md 正常 ($(wc -l < "$soul" | tr -d ' ')行)"
                add_check "soul:$aid" "ok" "$(wc -l < "$soul" | tr -d ' ')行"
            fi
        done <<< "$agent_ids"
    fi

    # 检查 5: bindings 完整性
    local missing_bindings
    missing_bindings=$(python3 -c "
import json
c=json.load(open('$CONFIG_FILE'))
bindings=c.get('bindings',[])
bound_ids={b.get('agentId') for b in bindings}
agents=[a['id'] for a in c.get('agents',{}).get('list',[]) if a['id']!='main']
missing=[a for a in agents if a not in bound_ids]
if missing:
    print(' '.join(missing))
" 2>/dev/null)

    if [ -n "$missing_bindings" ]; then
        warn "以下 Agent 缺少 binding：$missing_bindings"
        echo "bind:$missing_bindings" >> "$FIXES_FILE"
        issues=$((issues + 1))
        add_check "bindings" "warn" "缺失: $missing_bindings"
    else
        ok "所有 Agent 的 binding 配置完整"
        add_check "bindings" "ok" ""
    fi

    # 检查 6: 层级文件
    if [ -f "$HIERARCHY_FILE" ]; then
        ok "组织架构文件存在"
        add_check "hierarchy" "ok" ""
    else
        warn "缺少组织架构文件（team-hierarchy.json）"
        echo "hierarchy" >> "$FIXES_FILE"
        issues=$((issues + 1))
        add_check "hierarchy" "warn" "缺少 team-hierarchy.json"
    fi

    # 汇总
    if $JSON_OUTPUT; then
        python3 -c "
import json, sys
checks = json.loads(sys.argv[1])
print(json.dumps({'checks': checks, 'issues': int(sys.argv[2])}, ensure_ascii=False))
" "$json_checks" "$issues"
        rm -f "$FIXES_FILE"
        return
    fi

    blank
    divider
    if [ "$issues" -eq 0 ]; then
        ok "军团状态完美，无需修复"
        rm -f "$FIXES_FILE"
    else
        warn "发现 $issues 个问题"
        blank
        echo -e "  运行${BOLD}「一键修复」${NC}可自动解决以上问题"
    fi
    blank
}

# ══════════════════════════════════════════
# 模式：一键修复
# ══════════════════════════════════════════
mode_fix() {
    header "  一键修复"
    blank

    if [ ! -f "$FIXES_FILE" ] || [ ! -s "$FIXES_FILE" ]; then
        if $JSON_OUTPUT; then
            # JSON 模式下静默运行体检（只需要 FIXES_FILE）
            local saved_json=$JSON_OUTPUT
            JSON_OUTPUT=false
            mode_checkup > /dev/null 2>&1
            JSON_OUTPUT=$saved_json
        else
            info "先运行体检..."
            mode_checkup
        fi
    fi

    if [ ! -f "$FIXES_FILE" ] || [ ! -s "$FIXES_FILE" ]; then
        ok "无需修复"
        if $JSON_OUTPUT; then
            echo '{"status":"ok","fixes":0,"message":"无需修复"}'
        fi
        return
    fi

    local bdir
    bdir=$(do_backup "一键修复")
    ok "已备份到 $bdir"
    blank

    local fixed=0
    while IFS= read -r fix; do
        case "$fix" in
            gateway)
                info "重启 Gateway..."
                openclaw gateway restart 2>/dev/null && ok "Gateway 已重启" || warn "Gateway 重启失败"
                fixed=$((fixed + 1))
                ;;
            a2a)
                info "开启 agentToAgent 通信..."
                python3 -c "
import json
with open('$CONFIG_FILE') as f:
    c = json.load(f)
c.setdefault('tools',{})['agentToAgent'] = {'enabled': True, 'allow': c.get('tools',{}).get('agentToAgent',{}).get('allow',[])}
with open('$CONFIG_FILE', 'w') as f:
    json.dump(c, f, indent=2, ensure_ascii=False)
" 2>/dev/null
                ok "agentToAgent 已开启"
                fixed=$((fixed + 1))
                ;;
            a2a_allow)
                info "补全通信白名单..."
                python3 -c "
import json
with open('$CONFIG_FILE') as f:
    c = json.load(f)
a2a = c.get('tools',{}).get('agentToAgent',{})
allow = a2a.get('allow',[])
for a in c.get('agents',{}).get('list',[]):
    if a['id'] not in allow and a['id'] != 'main':
        allow.append(a['id'])
a2a['enabled'] = True
a2a['allow'] = allow
c.setdefault('tools',{})['agentToAgent'] = a2a
with open('$CONFIG_FILE', 'w') as f:
    json.dump(c, f, indent=2, ensure_ascii=False)
" 2>/dev/null
                ok "通信白名单已补全"
                fixed=$((fixed + 1))
                ;;
            soul:*)
                local aid="${fix#soul:}"
                info "为 $aid 生成 SOUL.md..."
                local ws="$OPENCLAW_DIR/workspace-$aid"
                if [ -d "$ws" ]; then
                    local aname
                    aname=$(python3 -c "import json; h=json.load(open('$HIERARCHY_FILE')); print(h.get('agents',{}).get('$aid',{}).get('name','$aid'))" 2>/dev/null)
                    generate_soul "$aid" "${aname:-$aid}" "通用AI助手" "main" "$ws"
                    ok "$aid SOUL.md 已生成"
                    fixed=$((fixed + 1))
                else
                    warn "$aid workspace 不存在，跳过"
                fi
                ;;
            bind:*)
                local aids="${fix#bind:}"
                for aid in $aids; do
                    info "为 $aid 添加 binding（自动检测所有 channel）..."
                    auto_bind_channels "$aid"
                    ok "$aid binding 已添加"
                    fixed=$((fixed + 1))
                done
                ;;
            hierarchy)
                info "初始化组织架构..."
                rm -f "$HIERARCHY_FILE"
                init_hierarchy
                ok "组织架构已初始化"
                fixed=$((fixed + 1))
                ;;
        esac
    done < "$FIXES_FILE"

    rm -f "$FIXES_FILE"
    blank
    ok "所有问题已修复！"
    note "运行 openclaw gateway restart 使配置生效"

    if $JSON_OUTPUT; then
        echo "{\"status\":\"ok\",\"fixes\":$fixed,\"message\":\"修复完成\"}"
    fi
    blank
}

# ══════════════════════════════════════════
# 模式：军团状态
# ══════════════════════════════════════════
mode_status() {
    if $JSON_OUTPUT; then
        python3 << 'PYEOF'
import json, os

config_file = os.path.expanduser("~/.openclaw/openclaw.json")
hierarchy_file = os.path.expanduser("~/.openclaw/team-hierarchy.json")

with open(config_file) as f:
    c = json.load(f)

# agents
agents = []
for a in c.get("agents", {}).get("list", []):
    aid = a["id"]
    ident = a.get("identity", {})
    name = ident.get("name", a.get("name", aid))
    if aid == "main":
        ws = a.get("workspace", os.path.expanduser("~/clawd"))
    else:
        ws = a.get("workspace", os.path.expanduser(f"~/.openclaw/workspace-{aid}"))
    soul_path = os.path.join(ws, "SOUL.md") if ws else ""
    soul_lines = 0
    if soul_path and os.path.exists(soul_path):
        soul_lines = len(open(soul_path).readlines())
    agents.append({"id": aid, "name": name, "soul_lines": soul_lines})

# a2a
a2a = c.get("tools", {}).get("agentToAgent", {})

# bindings
bindings = []
for b in c.get("bindings", []):
    bindings.append({
        "agentId": b.get("agentId", "?"),
        "channel": b.get("match", {}).get("channel", "?"),
        "accountId": b.get("match", {}).get("accountId", "?")
    })

# hierarchy
hierarchy = {}
if os.path.exists(hierarchy_file):
    with open(hierarchy_file) as f:
        hierarchy = json.load(f).get("agents", {})

# backups
backup_dir = os.path.expanduser("~/.openclaw/backups")
backup_count = 0
if os.path.isdir(backup_dir):
    backup_count = len([d for d in os.listdir(backup_dir) if os.path.isdir(os.path.join(backup_dir, d))])

result = {
    "agents": agents,
    "agent_count": len(agents),
    "a2a": {"enabled": a2a.get("enabled", False), "allow": a2a.get("allow", [])},
    "bindings": bindings,
    "hierarchy": hierarchy,
    "backup_count": backup_count
}
print(json.dumps(result, ensure_ascii=False))
PYEOF
        return
    fi

    header "  军团状态"
    blank

    # 架构图
    echo -e "  ${BOLD}组织架构：${NC}"
    blank
    draw_tree
    blank
    divider

    # Agent 列表
    echo -e "  ${BOLD}Agent 列表：${NC}"
    python3 -c "
import json
c=json.load(open('$CONFIG_FILE'))
agents=c.get('agents',{}).get('list',[])
for a in agents:
    aid=a['id']
    ident=a.get('identity',{})
    name=ident.get('name',a.get('name',aid))
    print(f'  - {aid:20s} {name}')
print(f'  共 {len(agents)} 个 Agent')
" 2>/dev/null
    blank

    # 通信状态
    echo -e "  ${BOLD}Agent 间通信：${NC}"
    python3 -c "
import json
c=json.load(open('$CONFIG_FILE'))
a2a=c.get('tools',{}).get('agentToAgent',{})
enabled='开启' if a2a.get('enabled') else '关闭'
allow=a2a.get('allow',[])
print(f'  状态: {enabled}')
print(f'  白名单: {', '.join(allow) if allow else '(空)'}')
" 2>/dev/null
    blank

    # Bindings
    echo -e "  ${BOLD}Bindings 路由：${NC}"
    python3 -c "
import json
c=json.load(open('$CONFIG_FILE'))
for b in c.get('bindings',[]):
    aid=b.get('agentId','?')
    ch=b.get('match',{}).get('channel','?')
    acc=b.get('match',{}).get('accountId','?')
    print(f'  {aid:20s} <- {ch}:{acc}')
" 2>/dev/null
    blank

    # SOUL.md 状态
    echo -e "  ${BOLD}SOUL.md 状态：${NC}"
    python3 -c "
import json, os
config_file = os.path.expanduser('~/.openclaw/openclaw.json')
c=json.load(open(config_file))
for a in c.get('agents',{}).get('list',[]):
    aid=a['id']
    if aid=='main':
        ws=a.get('workspace',os.path.expanduser('~/clawd'))
    else:
        ws=a.get('workspace',os.path.expanduser(f'~/.openclaw/workspace-{aid}'))
    soul=os.path.join(ws,'SOUL.md') if ws else ''
    if soul and os.path.exists(soul):
        lines=len(open(soul).readlines())
        print(f'  {aid:20s} {lines:3d} 行')
    else:
        print(f'  {aid:20s} 缺失')
" 2>/dev/null
    blank

    # 备份
    echo -e "  ${BOLD}备份：${NC}"
    if [ -d "$BACKUP_DIR" ]; then
        local bk_count
        bk_count=$(ls -1d "$BACKUP_DIR"/*/ 2>/dev/null | wc -l | tr -d ' ')
        echo "  共 $bk_count 个备份（保留最近 5 个）"
    else
        echo "  暂无备份"
    fi
    blank
}

# ══════════════════════════════════════════
# 运维提示
# ══════════════════════════════════════════
show_ops_tips() {
    divider
    echo -e "  ${BOLD}运维提示：${NC}"
    note "查看 skills：openclaw skills list"
    note "安装 skills：npx clawhub"
    note "记忆搜索：  openclaw memory search <关键词>"
    note "健康检查：  openclaw health"
    note "查看日志：  openclaw logs"
    note "修复问题：  openclaw doctor --fix"
    blank
}

# ══════════════════════════════════════════
# 主菜单（TUI）
# ══════════════════════════════════════════
main_menu() {
    preflight
    check_version
    init_hierarchy

    local VERSION
    VERSION=$(openclaw --version 2>/dev/null | head -1)

    blank
    echo -e "${BOLD}"
    echo "  ┌──────────────────────────────────────────┐"
    echo "  │                                          │"
    echo "  │  🦞  OpenClaw Team Builder  v3.1         │"
    echo "  │                                          │"
    echo "  │  自由组织你的 AI 团队                    │"
    echo "  │                                          │"
    echo "  └──────────────────────────────────────────┘"
    echo -e "${NC}"
    note "OpenClaw $VERSION | $(hostname)"
    blank

    echo -e "  ${BOLD}当前架构：${NC}"
    blank
    draw_tree
    blank
    divider
    blank

    echo "  ┌──────────────────────────────────────────────────┐"
    echo "  │                                                  │"
    echo "  │  1)  新增员工 — 挂到组织树的任意位置            │"
    echo "  │                                                  │"
    echo "  │  2)  快速模板：超级个体（4人 + CEO）            │"
    echo "  │                                                  │"
    echo "  │  3)  查看架构图                                  │"
    echo "  │                                                  │"
    echo "  │  4)  军团体检 — 自动扫描缺失配置                │"
    echo "  │                                                  │"
    echo "  │  5)  一键修复 — 根据体检结果自动修复            │"
    echo "  │                                                  │"
    echo "  │  6)  军团状态 — Agent/通信/备份总览             │"
    echo "  │                                                  │"
    echo "  │  7)  回退上次操作                                │"
    echo "  │                                                  │"
    echo "  │  q)  退出                                        │"
    echo "  │                                                  │"
    echo "  └──────────────────────────────────────────────────┘"
    blank
    note "所有操作前会自动备份，随时可以回退。"
    blank
    read -p "  请选择: " CHOICE

    case "$CHOICE" in
        1) mode_add ;;
        2) mode_solo_template ;;
        3) blank; draw_tree; blank ;;
        4) mode_checkup ;;
        5) mode_fix ;;
        6) mode_status ;;
        7) mode_rollback ;;
        q|Q) echo "  再见！"; exit 0 ;;
        *) fail "无效选择"; exit 1 ;;
    esac
}

# ══════════════════════════════════════════
# CLI 参数解析
# ══════════════════════════════════════════
if [ $# -gt 0 ]; then
    MODE=""
    while [ $# -gt 0 ]; do
        case "$1" in
            --add)      MODE="add"; shift ;;
            --solo)     MODE="solo"; shift ;;
            --tree)     MODE="tree"; shift ;;
            --checkup)  MODE="checkup"; shift ;;
            --fix)      MODE="fix"; shift ;;
            --status)   MODE="status"; shift ;;
            --rollback) MODE="rollback"; shift ;;
            --templates) MODE="templates"; shift ;;
            --json)     JSON_OUTPUT=true; export JSON_OUTPUT; shift ;;
            --yes|-y)   AUTO_YES=true; shift ;;
            --id)       B_ID="$2"; shift 2 ;;
            --name)     B_NAME="$2"; shift 2 ;;
            --emoji)    B_EMOJI="$2"; shift 2 ;;
            --role)     B_ROLE="$2"; shift 2 ;;
            --parent)   B_PARENT="$2"; shift 2 ;;
            --soul)     B_SOUL="$2"; shift 2 ;;
            --model)    B_MODEL="$2"; shift 2 ;;
            --feishu-app-id)  B_FEISHU_APPID="$2"; shift 2 ;;
            --feishu-secret)  B_FEISHU_SECRET="$2"; shift 2 ;;
            --suggest)  MODE="suggest"; shift ;;
            --goal)     B_GOAL="$2"; shift 2 ;;
            --channels) MODE="channels"; shift ;;
            --agent)    B_AGENT="$2"; shift 2 ;;
            --channel)  B_CHANNEL="$2"; shift 2 ;;
            --token)    B_TOKEN="$2"; shift 2 ;;
            --index)    B_ROLLBACK_INDEX="$2"; shift 2 ;;
            --help|-h)  MODE="help"; shift ;;
            *) fail "未知参数: $1"; echo "  用 --help 查看帮助"; exit 1 ;;
        esac
    done

    case "$MODE" in
        add)
            preflight; check_version; init_hierarchy
            if [ -n "$B_ID" ] || $AUTO_YES; then
                mode_add_batch
            else
                mode_add
            fi
            ;;
        solo)
            preflight; check_version; init_hierarchy; mode_solo_template ;;
        tree)
            preflight; check_version; init_hierarchy
            if $JSON_OUTPUT; then
                draw_tree_json
            else
                blank; draw_tree; blank
            fi
            ;;
        checkup)
            preflight; check_version; init_hierarchy; mode_checkup ;;
        fix)
            preflight; check_version; init_hierarchy; mode_fix ;;
        status)
            preflight; check_version; init_hierarchy; mode_status ;;
        rollback)
            preflight; check_version; init_hierarchy; mode_rollback ;;
        suggest)
            preflight; check_version; init_hierarchy; mode_suggest ;;
        channels)
            preflight; check_version; mode_channels ;;
        templates)
            if $JSON_OUTPUT; then
                list_templates_json
            else
                show_role_templates
            fi
            ;;
        help)
            echo "OpenClaw Team Builder v3.5"
            echo ""
            echo "TUI 模式（人类使用）："
            echo "  bash $0              # 交互菜单"
            echo ""
            echo "CLI 模式（Agent 调用）："
            echo "  bash $0 --tree [--json]           # 查看架构树"
            echo "  bash $0 --checkup [--json]        # 军团体检"
            echo "  bash $0 --fix [--yes]             # 一键修复"
            echo "  bash $0 --status [--json]         # 军团状态"
            echo "  bash $0 --templates [--json]      # 角色模板列表"
            echo "  bash $0 --suggest --goal <desc> [--json]  # 目标驱动团队推荐"
            echo "  bash $0 --channels [--agent <id>] [--json]  # 渠道管理"
            echo "  bash $0 --channels --agent <id> --channel telegram --token <token> --yes  # 添加 Telegram bot"
            echo "  bash $0 --channels --agent <id> --channel discord --token <token> --yes  # 添加 Discord bot"
            echo "  bash $0 --channels --agent <id> --channel feishu --feishu-app-id <id> --feishu-secret <s> --yes  # 添加飞书"
            echo "  bash $0 --rollback [--index N] [--yes]  # 回退"
            echo ""
            echo "  bash $0 --add --id <id> --name <name> --emoji <emoji> \\"
            echo "    --role <desc> --parent <parent-id> [--soul auto|template:<key>|skip] \\"
            echo "    [--model <model>] [--feishu-app-id <id> --feishu-secret <s>] [--yes]"
            echo ""
            echo "  bash $0 --solo [--soul auto|skip] [--model <m>] [--yes]"
            echo ""
            echo "标志："
            echo "  --json    输出 JSON（查询类命令）"
            echo "  --yes     跳过确认提示（操作类命令）"
            ;;
        *)
            fail "未指定操作模式"; echo "  用 --help 查看帮助"; exit 1 ;;
    esac
else
    main_menu
fi
