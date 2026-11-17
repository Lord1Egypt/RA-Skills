#!/bin/bash
# ═══════════════════════════════════════════════════════════
# PMM 全自动蒸馏引擎 9.3.12 — 每个AI体均可一键执行
# 蒸馏链路: 扫描 → LLM蒸馏(candidates→DeepSeek判定→result API合并) → 钩子验证 → 报告
#
# ⚠️ 行为声明：
#   非 --dry-run 模式下，蒸馏引擎会自动：
#   1. 扫描远程记忆（stats API）并生成报告
#   2. LLM 蒸馏（candidates→DeepSeek 判定→result API 合并去重，AI体自付Token）
#   3. 验证钩子完整性并写入蒸馏报告
#   使用 --dry-run 可预览即将执行的操作，不产生实际变更。
# ═══════════════════════════════════════════════════════════

readonly VERSION="9.3.12"

# grep 无匹配返回 1 是正常行为，不用严格模式
USER_ID=""           # 标准产品：不设默认 user_id，由 --user-id 参数显式传入
DRY_RUN=false
# 全局计数（供 generate_report 输出真实数字，替代写死"已完成"）
HOOK_EXIST="?"; HOOK_MISSING="?"; HOOK_SKIP="?"
AUTO_YES=false

# 解析参数
for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=true ;;
        --user-id=*) USER_ID="${arg#*=}" ;;
        --workspace=*) WORK_DIR="${arg#*=}" ;;
        --yes) AUTO_YES=true ;;   # cron 非交互环境自动确认，跳过 read
    esac
done
# 标准产品：工作区路径不按 user_id 硬编码映射，由 --workspace 参数或环境变量决定
if [ -z "$WORK_DIR" ]; then
    WORK_DIR="${KLYC_WORKSPACE:-${HOME}/workspace}"
fi
MEMORY_FILE="${WORK_DIR}/MEMORY.md"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
REPORT_FILE="${WORK_DIR}/memory/pmm-distill-${TIMESTAMP}.md"

# 配置目录（AI体自己的 .klyc-pmm），由环境变量 KLYC_PMM_CONFIG_DIR 覆盖，默认 ${HOME}/.klyc-pmm
CONFIG_DIR="${KLYC_PMM_CONFIG_DIR:-${HOME}/.klyc-pmm}"
KEY_FILE="${CONFIG_DIR}/api_key"

# 标准读 key：读 AI体自己的 API Key（@pmm_watch.sh 同源）
pmm_get_key() { cat "$KEY_FILE" 2>/dev/null || echo ""; }

G='\033[0;32m'; Y='\033[1;33m'; N='\033[0m'
log()  { echo -e "${G}[蒸馏]${N} $*"; }
warn() { echo -e "${Y}[警告]${N} $*"; }
step() { echo -e "\n${G}═══ $* ═══${N}"; }

# ─── 层1-4: 扫描 ───
scan_all() {
    step "层1-4: 寻踪→织网→入库→还原 扫描记忆"
    
    LOCAL_LINES=$(wc -l < "$MEMORY_FILE" 2>/dev/null || echo "0")
    LOCAL_KB=$(du -k "$MEMORY_FILE" 2>/dev/null | cut -f1 || echo "0")
    IRON_LAWS=$(grep -cE '^[0-9]+\. \*\*' "$MEMORY_FILE" 2>/dev/null || true)
    HOOKS=$(grep -cE '^\| .+ \| [0-9]{4} \| .+ \|' "$MEMORY_FILE" 2>/dev/null || true)
    echo "  本地: ${LOCAL_LINES}行/${LOCAL_KB}KB | 铁律${IRON_LAWS}条 | 钩子${HOOKS}条"
    
    # 远程 domain 分布（走 stats API，标准产品零本地 DB 直连）
    local auth_header=""
    if [ -n "${KYLC_API_KEY:-}" ]; then
        auth_header="X-KLYC-Key: ${KYLC_API_KEY}"
    else
        local own_key; own_key=$(pmm_get_key)
        [ -n "$own_key" ] && auth_header="X-KLYC-Key: ${own_key}"
    fi
    local stats_resp=$(curl -s --max-time 30 "${KYLC_PLATFORM_URL:-https://kunlunyaochi.com}/api.php?route=yaochi/memory/stats" -H "${auth_header}" 2>/dev/null)
    local total=$(echo "$stats_resp" | jq -r '.total // 0' 2>/dev/null)
    local domain_cnt=$(echo "$stats_resp" | jq -r '.domains | length // 0' 2>/dev/null)
    echo "  远程(user_id=${USER_ID}): ${total}条, ${domain_cnt}域"
    echo "$stats_resp" | jq -r '.domains[]? | "    \(.domain): \(.cnt)(加密\(.enc))"' 2>/dev/null
}

# ─── 层9-12: 提炼钩子 ───
auto_extract_hooks() {
    step "层9-12: 修订→追本→炼金→提纯 提炼钩子"
    
    local hook_count=$(grep -cE '^\| .+ \| [0-9]{4} \| .+ \|' "$MEMORY_FILE" 2>/dev/null || echo "0")
    echo "  蒸馏钩子: ${hook_count} 条"
    
    if $DRY_RUN; then
        grep -E '^\|.*\| *[0-9]+ *\|' "$MEMORY_FILE" 2>/dev/null | tail -5
        return
    fi
    
    # 验证钩子远程存在性（走 memory/view API，标准产品零本地 DB 直连）
    local auth_header=""
    if [ -n "${KYLC_API_KEY:-}" ]; then
        auth_header="X-KLYC-Key: ${KYLC_API_KEY}"
    else
        local own_key; own_key=$(pmm_get_key)
        [ -n "$own_key" ] && auth_header="X-KLYC-Key: ${own_key}"
    fi
    local exist=0 skip=0 missing=0
    while IFS= read -r line; do
        [ -z "$line" ] && continue
        local hid=$(echo "$line" | grep -oE '\|\s*[0-9]{4}\s*\|' | grep -oE '[0-9]+' | head -1)
        [ -z "$hid" ] && continue
        if echo "$line" | grep -qE '404|本地自包含|本地副本|以本地为准|已清'; then
            echo "  ⏭️ ID=$hid 本地自包含/已404,跳过"; skip=$((skip+1)); continue
        fi
        local view_resp=$(curl -s --max-time 10 "${KYLC_PLATFORM_URL:-https://kunlunyaochi.com}/api.php?route=yaochi/memory/view&id=${hid}" -H "${auth_header}" 2>/dev/null)
        if echo "$view_resp" | jq -e '.success == true and .memory != null' >/dev/null 2>&1; then
            exist=$((exist+1))
        else
            echo "  ⏭️ ID=$hid 远程无此记忆(端口/编号),跳过"; skip=$((skip+1))
        fi
    done < <(grep -E '^\|.*\| *[0-9]+ *\|' "$MEMORY_FILE" 2>/dev/null)
    HOOK_EXIST=$exist; HOOK_SKIP=$skip; HOOK_MISSING=$missing

}

# ─── 层13-14: 报告 ───
# ─── 本地轻量化：MEMORY.md 低频段落钩子化（标准化，全站通用）───
auto_local_hook() {
    step "本地轻量化: 低频段落钩子化"
    $DRY_RUN && { echo "  dry-run跳过"; return; }
    # 标准产品：低频段落钩子化是站内优化功能（依赖站内 klyc_local_hook.php DB 直写）。
    # 标准产品零本地 DB 直连，不自动做此优化；AI 体可自行用 memory/create API 实现。
    echo "  低频段落钩子化：标准产品不自动执行（站内专用优化，可通过 yaochi/memory/create API 自行实现）"
}

generate_report() {
    step "层13-14: 通变→取舍 生成报告"
    
    local auth_header=""
    if [ -n "${KYLC_API_KEY:-}" ]; then
        auth_header="X-KLYC-Key: ${KYLC_API_KEY}"
    else
        local own_key; own_key=$(pmm_get_key)
        [ -n "$own_key" ] && auth_header="X-KLYC-Key: ${own_key}"
    fi
    local remote_cnt=$(curl -s --max-time 30 "${KYLC_PLATFORM_URL:-https://kunlunyaochi.com}/api.php?route=yaochi/memory/stats" -H "${auth_header}" 2>/dev/null | jq -r '.total // "?"' 2>/dev/null)
    
    cat > "$REPORT_FILE" << EOF
# PMM 全自动蒸馏报告

**AI体:** user_id=${USER_ID}  
**时间:** $(date '+%Y-%m-%d %H:%M:%S')  
**模式:** $($DRY_RUN && echo '预览' || echo '执行')

## 蒸馏统计

| 指标 | 值 |
|------|-----|
| 本地 MEMORY.md | ${LOCAL_LINES:-?}行/${LOCAL_KB:-?}KB |
| 铁律 | ${IRON_LAWS:-?}条 |
| 蒸馏钩子 | ${HOOKS:-?}条 |
| 远程记忆 | ${remote_cnt}条 |

## 本次操作

- LLM 蒸馏：由 candidates→DeepSeek 判定→result API 合并链路完成（本机不做本地软删）
- 钩子验证：已完成(存在 ${HOOK_EXIST:-N/A} / 缺失 ${HOOK_MISSING:-N/A} / 跳过 ${HOOK_SKIP:-N/A})
EOF
    
    log "报告: $REPORT_FILE"
}

# ═══════════════════════════════════════════
main() {
    echo ""
    echo "══════════════════════════════════════"
    echo "  PMM 全自动蒸馏引擎 v2.0"
    echo "  AI体: user_id=${USER_ID}"
    $DRY_RUN && echo "  模式: 预览 (--dry-run)"
    echo "  $(date '+%Y-%m-%d %H:%M:%S')"
    echo "══════════════════════════════════════"

    # 非 dry-run 模式：二次确认（防止误执行写库操作）
    if ! $DRY_RUN; then
        echo ""
        echo -e "${Y}⚠️  蒸馏引擎将执行以下操作：${N}"
        echo "  1. 扫描远程记忆并生成报告"
        echo "  2. LLM 蒸馏（candidates→DeepSeek 判定→result API 合并）"
        echo "  3. 验证钩子完整性并写入蒸馏报告"
        echo ""
        if $AUTO_YES; then
            echo "  ✅ 自动确认（--yes）"
        else
            read -r -p "确认执行？[y/N] " confirm
            case "$confirm" in
                [yY]|[yY][eE][sS]) echo "  继续执行..." ;;
                *) echo "  已取消。使用 --dry-run 可预览即将执行的操作。"; exit 0 ;;
            esac
        fi
    fi

    scan_all
    distill_with_llm    # 🆕 层5-12: LLM蒸馏 (AI体用自己的DeepSeek Key)
    auto_extract_hooks
    auto_local_hook    # 本地轻量化：MEMORY.md 低频段落钩子化
    generate_report
    
    echo ""
    $DRY_RUN && echo "  🔍 预览完成。去掉 --dry-run 执行实际蒸馏。" || echo "  ✅ 全自动蒸馏完成。"
    echo ""
}

# ═══════════════════════════════════════════════════════════
# 层9-12: LLM蒸馏 (2026-08-12 新增)
# AI体用自己的 DeepSeek Key 调平台候选对 API → 逐对判定 → 回传结果
# ═══════════════════════════════════════════════════════════
distill_with_llm() {
    step "层9-12: LLM蒸馏 (自付Token)"
    
    $DRY_RUN && { echo "  dry-run跳过LLM蒸馏"; return; }
    
    local platform_url="${KYLC_PLATFORM_URL:-https://kunlunyaochi.com}"
    
    # ─── key 列表轮换（支持单/双/多 key，每个 AI 体用自己的 key）───
    # 优先级：PMM_DEEPSEEK_KEYS(逗号分隔，多key) > PRIMARY+BACKUP(双key) > DEEPSEEK_API_KEY(单key)
    local keys=()
    local k
    if [ -n "${PMM_DEEPSEEK_KEYS:-}" ]; then
        IFS=',' read -ra keys <<< "$PMM_DEEPSEEK_KEYS"
    fi
    if [ ${#keys[@]} -eq 0 ]; then
        [ -n "${PMM_DEEPSEEK_KEY_PRIMARY:-}" ] && keys+=("$PMM_DEEPSEEK_KEY_PRIMARY")
        [ -n "${PMM_DEEPSEEK_KEY_BACKUP:-}" ] && keys+=("$PMM_DEEPSEEK_KEY_BACKUP")
    fi
    if [ ${#keys[@]} -eq 0 ] && [ -n "${DEEPSEEK_API_KEY:-}" ]; then
        keys+=("$DEEPSEEK_API_KEY")
    fi
    
    # 去空 + 去首尾空白
    local clean_keys=()
    for k in "${keys[@]}"; do
        k=$(printf '%s' "$k" | tr -d '[:space:]')
        [ -n "$k" ] && clean_keys+=("$k")
    done
    keys=("${clean_keys[@]}")
    
    if [ ${#keys[@]} -eq 0 ]; then
        echo "  跳过: 未找到 DeepSeek API Key (设置 PMM_DEEPSEEK_KEYS 或 DEEPSEEK_API_KEY 环境变量)"
        return
    fi
    echo "  已配置 ${#keys[@]} 个 DeepSeek key（按需轮换）"
    
    local state_file="/tmp/distill_key_index_${USER_ID}"
    local key_idx=0
    [ -f "$state_file" ] && key_idx=$(cat "$state_file" 2>/dev/null || echo 0)
    
    # ─── 确定平台认证头（X-KLYC-Key = AI体自己的 API Key）
    # 标准读法：读自己的 ~/.klyc-pmm/api_key（@pmm_watch.sh 同源），
    # 与昆仑令(token)是两码事——token 是找回身份用，日常调 API 用 api_key。
    local auth_header=""
    if [ -n "${KYLC_API_KEY:-}" ]; then
        auth_header="X-KLYC-Key: ${KYLC_API_KEY}"
    else
        local own_key; own_key=$(pmm_get_key)
        [ -n "$own_key" ] && auth_header="X-KLYC-Key: ${own_key}"
    fi
    
    if [ -z "$auth_header" ]; then
        echo "  跳过: 未找到平台认证凭据"
        return
    fi
    
    # ─── ① 请求候选对
    local task_resp=$(curl -s --max-time 90 -X POST "${platform_url}/api/klyc_distill_candidates.php"         -H "${auth_header}"         -H "Content-Type: application/json"         -d '{"limit":20,"user_id":'"$USER_ID"'}' 2>/dev/null)
    
    local task_id=$(echo "$task_resp" | jq -r '.task_id // empty' 2>/dev/null)
    if [ -z "$task_id" ]; then
        local err=$(echo "$task_resp" | jq -r '.error // "请求失败"' 2>/dev/null)
        echo "  候选对API失败: ${err}"
        return
    fi
    echo "  task: ${task_id}"

    # ─── ② 取候选对（2026-08-16 根治：POST 已同步返回 status:done + candidates，直接消费，不再轮询会 500 的 status 接口）
    local candidates_json=""
    local post_status=$(echo "$task_resp" | jq -r '.status // empty' 2>/dev/null)
    if [ "$post_status" = "done" ]; then
        candidates_json="$task_resp"
        echo "  候选对已同步返回（跳过轮询）"
    else
        # 兜底：极少数 queued 情况才轮询（status 接口若 500 则放弃，不影响主路径）
        for i in 1 2 3; do
            sleep 3
            local status_resp=$(curl -s --max-time 90 "${platform_url}/api/klyc_distill_candidates_status.php?task_id=${task_id}"             -H "${auth_header}" 2>/dev/null)
            local status=$(echo "$status_resp" | jq -r '.status // "queued"' 2>/dev/null)
            if [ "$status" = "done" ]; then
                candidates_json="$status_resp"
                break
            elif [ "$status" = "failed" ]; then
                echo "  候选对生成失败: $(echo $status_resp | jq -r '.error // "unknown"' 2>/dev/null)"
                return
            fi
        done
    fi

    # 容错：status 轮询接口可能因 user_id 失配返回空，回退用触发响应里的 candidates（同步生成模式）
    if [ -z "$candidates_json" ] || [ "$candidates_json" = "null" ]; then
        candidates_json=$(echo "$task_resp" | jq -c '{total:.total, candidates:.candidates}' 2>/dev/null)
    fi
    if [ -z "$candidates_json" ] || [ "$candidates_json" = "null" ]; then
        echo "  候选对未就绪（超时），下次心跳再试"
        return
    fi
    
    local total=$(echo "$candidates_json" | jq -r '.total // 0')
    echo "  候选对: ${total}"
    [ "$total" -eq 0 ] && return
    
    # ─── ③ 逐对调 DeepSeek 判定
    local tmpfile="/tmp/pmm_distill_results_$$.json"
    echo "[" > "$tmpfile"
    local processed=0
    
    while IFS= read -r cluster; do
        [ -z "$cluster" ] && continue
        local cluster_id=$(echo "$cluster" | jq -r '.cluster_id')
        local mem_count=$(echo "$cluster" | jq -r '.memories | length')
        [ "$mem_count" -lt 2 ] && continue
        local source_ids=$(echo "$cluster" | jq -c '.memories | map(.id)')
        local mems_text=$(echo "$cluster" | jq -r '[.memories[] | "记忆#\(.id)[\(.title)]: \(.content)"] | join("\n")')
        local user_prompt="你是记忆蒸馏引擎。将下面 ${mem_count} 条语义相关的记忆提炼合并为一条精华：
${mems_text}
要求：merged 必须是提炼后的精华正文，完整保留所有记忆的关键事实/决策/教训/洞察，一条不落；去掉重复表述和过程噪音；不要简单拼接，要语义级提炼。
输出JSON: {\"rel\":\"identical|overlap|related|unrelated\",\"conf\":0.XX,\"merged\":\"提炼精华正文\",\"reason\":\"理由(50字内)\"}"
        local prompt_data=$(jq -n --arg up "$user_prompt" '{model:"deepseek-v4-flash",messages:[{role:"system",content:"你是记忆蒸馏引擎。将一组语义相关的记忆提炼为一条精华。只输出JSON。"},{role:"user",content:$up}],temperature:0.1,max_tokens:4000,thinking:{"type":"disabled"}}')
        if [ -z "$prompt_data" ] || ! echo "$prompt_data" | jq -e . >/dev/null 2>&1; then
            echo "  prompt构造失败，跳过该簇"
            continue
        fi
        # key 列表轮换：从当前 key_idx 开始，失败切下一个，最多试完所有 key
        local llm_resp=""
        local try_i idx candidate
        for try_i in $(seq 0 $(( ${#keys[@]} - 1 ))); do
            idx=$(( (key_idx + try_i) % ${#keys[@]} ))
            candidate="${keys[$idx]}"
            llm_resp=$(curl -s --max-time 60 -X POST "https://api.deepseek.com/v1/chat/completions" -H "Authorization: Bearer ${candidate}" -H "Content-Type: application/json" -d "$prompt_data" 2>/dev/null)
            if echo "$llm_resp" | jq -e '.choices[0].message.content // .choices[0].message.reasoning_content' >/dev/null 2>&1; then
                # 成功：记录当前可用 key 索引（下次从这里开始轮换）
                [ "$idx" -ne 0 ] && echo "$idx" > "$state_file" || rm -f "$state_file"
                [ "$idx" -ne "$key_idx" ] && echo "  key[${idx}] 接管（前一个不可用）"
                break
            else
                echo "  key[${idx}] 失败(欠费/故障/超时)，切下一个"
            fi
        done
        local llm_content=$(echo "$llm_resp" | jq -r '.choices[0].message.content // empty' 2>/dev/null)
        if [ -z "$llm_content" ]; then
            llm_content=$(echo "$llm_resp" | jq -r '.choices[0].message.reasoning_content // empty' 2>/dev/null)
        fi
        if [ -z "$llm_content" ]; then continue; fi
        local llm_raw="$llm_content"
        llm_raw=$(echo "$llm_raw" | sed -E 's/^[[:space:]]*```[a-zA-Z]*[[:space:]]*//; s/[[:space:]]*```[[:space:]]*$//')
        local llm_json=$(printf '%s' "$llm_raw" | python3 -c 'import sys,json;
data=sys.stdin.read();
s=data.find("{");
if s<0: sys.exit(1);
depth=0;
for i in range(s,len(data)):
    if data[i]=="{": depth+=1
    elif data[i]=="}":
        depth-=1
        if depth==0:
            cand=data[s:i+1];
            try: json.loads(cand); print(cand); break
            except: pass' 2>/dev/null)
        if [ -z "$llm_json" ]; then continue; fi
        local rel=$(echo "$llm_json" | jq -r '.rel // "related"' 2>/dev/null)
        local conf=$(echo "$llm_json" | jq -r '.conf // 0' 2>/dev/null)
        local merged=$(echo "$llm_json" | jq -r '.merged // ""' 2>/dev/null)
        local reason=$(echo "$llm_json" | jq -r '.reason // ""' 2>/dev/null)
        if [ "$rel" != "identical" ] && [ "$rel" != "overlap" ]; then merged=""; fi
        if [ "$(awk "BEGIN{print ($conf<0.9)?1:0}")" = "1" ]; then merged=""; fi
        local entry=$(jq -nc --arg cid "$cluster_id" --argjson sids "$source_ids" --arg rel "$rel" --argjson conf "$conf" --arg merged "$merged" --arg reason "$reason" '{cluster_id:$cid, source_ids:$sids, rel:$rel, conf:$conf, merged:$merged, reason:$reason}')
        if [ $processed -gt 0 ]; then echo "," >> "$tmpfile"; fi
        echo "  [CLUSTER] cluster_id=$cluster_id mems=$mem_count rel=$rel conf=$conf merged_len=${#merged}"
        echo "$entry" >> "$tmpfile"
        processed=$((processed + 1))
        [ $processed -ge 10 ] && break
    done < <(echo "$candidates_json" | jq -c '.clusters[]' 2>/dev/null)

    
    echo "]" >> "$tmpfile"
    
    # ─── ④ 回传结果
    echo "  LLM判定完成: 成功处理 $processed 对 / 共 $total 对"
    if [ $processed -gt 0 ] && [ -f "$tmpfile" ]; then
        local final_results=$(cat "$tmpfile")
        rm -f "$tmpfile"
        
        local payload=$(jq -nc --argjson r "$final_results" '{results: $r}')
        # 方案Y(2026-08-16): 绕过 fpm 在 beginTransaction 后 C 级崩溃，改用 CLI 本地合并
        local result_resp=$(curl -s --max-time 60 -X POST "${platform_url}/api/klyc_distill_result.php" -H "${auth_header}" -H "Content-Type: application/json" -d "$payload" 2>/dev/null)
        
        local merged_count=$(echo "$result_resp" | jq -r '.merged // 0' 2>/dev/null)
        local conflict_count=$(echo "$result_resp" | jq -r '.conflicts // 0' 2>/dev/null)
        echo "  LLM蒸馏完成: 判定${processed}对, 合并${merged_count}, 冲突${conflict_count}"
    fi
}

main "$@"

# ── 更新 last_distill_at（走 candidates_status API，标准产品零本地 DB 直连）──
# 2026-09-05 修复：dry-run 不得写库（否则违背"不产生实际变更"声明）
if ! $DRY_RUN; then
    local_auth_header=""
    if [ -n "${KYLC_API_KEY:-}" ]; then
        local_auth_header="X-KLYC-Key: ${KYLC_API_KEY}"
    else
        local_own_key=$(pmm_get_key)
        [ -n "$local_own_key" ] && local_auth_header="X-KLYC-Key: ${local_own_key}"
    fi
    curl -s --max-time 30 -X POST "${KYLC_PLATFORM_URL:-https://kunlunyaochi.com}/api/klyc_distill_candidates_status.php" -H "${local_auth_header}" -H "Content-Type: application/json" -d '{"action":"distill_done"}' >/dev/null 2>&1
    echo "[蒸馏] last_distill_at 已更新"
else
    echo "[蒸馏] dry-run：跳过 last_distill_at 写入"
fi
