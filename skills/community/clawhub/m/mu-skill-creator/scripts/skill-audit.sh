#!/bin/bash
# skill-audit.sh — mu-Skill 结构健康检查工具
# 所属: mu-skill-creator Skill（scripts/skill-audit.sh）
# 规则来源: mu-skill-creator 10层审计模型（56项，可脚本核验子集）
#
# 用法:
#   bash skill-audit.sh                    # 扫描全部 Skills
#   bash skill-audit.sh mu-excel-toolbox   # 只查指定 Skill（名称）
#   bash skill-audit.sh mu-a mu-b          # 查多个
#   bash skill-audit.sh --verbose          # 全部 + 详细说明
#
# 检查项:
#   IRON_LAW  - 是否在 frontmatter 之后有 IRON LAW 声明
#   IL_DIFF   - IRON LAW 内容是否差异化（不含通用套话、含至少1条Skill专属约束）
#   DESC      - description 格式（双引号单行 + 触发词 + 不适用）
#   SEC_RISK  - 是否引用了安全受限系统URL
#   LINES     - 行数（>250 标黄，信息项不阻断）
#   CODE     - scripts/+assets/ 代码质量扫描（L3/L7 可自动化项）

set -euo pipefail

# Auto-detect SKILL_BASE: env var > script location > fallback
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -z "${SKILL_BASE:-}" ]; then
  # Try 2 levels up (non-nested) then 3 levels up (nested subdir)
  for _d in "$(dirname "$(dirname "$SCRIPT_DIR")")" "$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"; do
    if find "$_d" -maxdepth 3 -name "SKILL.md" -print -quit 2>/dev/null | grep -q .; then
      SKILL_BASE="$_d"
      break
    fi
  done
fi
if [ -z "${SKILL_BASE:-}" ]; then
  echo "⚠️ 无法自动定位 Skills 目录，请设置 SKILL_BASE 环境变量" >&2
  echo "  例如: export SKILL_BASE=~/.skills" >&2
  exit 1
fi
VERBOSE=false
TARGETS=()

# 解析参数
for arg in "$@"; do
  if [ "$arg" = "--verbose" ]; then
    VERBOSE=true
  else
    TARGETS+=("$arg")
  fi
done

# 构建 SKILLS 数组：name|path
SKILLS=()

if [ ${#TARGETS[@]} -eq 0 ]; then
  # 未指定 → 自动扫描全部含 SKILL.md 的子目录
  # 先不带 -L 查找（快），找不到再带 -L（跟随 symlink，覆盖 ~/.skills/mu-* symlink 安装路径）
  _scan_result=$(find "$SKILL_BASE" -maxdepth 3 -name "SKILL.md" ! -path "*/_archive/*" ! -path "*/_*/*" 2>/dev/null | sort)
  if [ -z "$_scan_result" ]; then
    _scan_result=$(find -L "$SKILL_BASE" -maxdepth 3 -name "SKILL.md" ! -path "*/_archive/*" ! -path "*/_*/*" 2>/dev/null | sort)
  fi
  while IFS= read -r skill_md; do
    [ -z "$skill_md" ] && continue
    skill_dir=$(dirname "$skill_md")
    name=$(basename "$skill_dir")
    # 跳过 _开头的目录（如 _archive）
    case "$name" in _*) continue ;; esac
    SKILLS+=("${name}|${skill_md}")
  done <<< "$_scan_result"
else
  # 指定名称 → 找对应 SKILL.md（支持嵌套子目录 + symlink 安装路径）
  for target in "${TARGETS[@]}"; do
    skill_md=$(find "$SKILL_BASE" -maxdepth 3 -path "*/${target}/SKILL.md" 2>/dev/null | head -1 || true)
    # Fallback: 跟随 symlink 重试（覆盖 ~/.skills/mu-* symlink 安装路径）
    if [ -z "$skill_md" ]; then
      skill_md=$(find -L "$SKILL_BASE" -maxdepth 3 -path "*/${target}/SKILL.md" 2>/dev/null | head -1 || true)
    fi
    if [ -n "$skill_md" ]; then
      SKILLS+=("${target}|${skill_md}")
    else
      echo "❌ 找不到 Skill: $target（搜索: $SKILL_BASE/**/${target}/SKILL.md）"
    fi
  done
fi

# 找不到任何 Skill 时早退
if [ ${#SKILLS[@]} -eq 0 ]; then
  echo "❌ 未找到任何可检查的 Skill"
  exit 1
fi

# 核验计数：这些结果只提供全面审计所需的脚本证据，不构成独立审计结论。
total=0
pass=0
warn=0
fail=0

printf "%-20s %5s %8s %8s %8s %8s %8s %8s %6s\n" "SKILL" "LINES" "IRON" "IL専" "DESC" "SEC" "CODE" "GOTCHA" "ICE"
printf "%-20s %5s %8s %8s %8s %8s %8s %8s %6s\n" "--------------------" "-----" "--------" "--------" "--------" "--------" "--------" "--------" "------"

for entry in "${SKILLS[@]}"; do
  IFS='|' read -r name f <<< "$entry"
  total=$((total + 1))

  if [ ! -f "$f" ]; then
    printf "%-20s %5s %8s %8s %8s %8s\n" "$name" "N/A" "❌文件缺" "-" "-" "-"
    fail=$((fail + 1))
    continue
  fi

  lines=$(wc -l < "$f")
  skill_ok=true

  # L1-8: Gotchas 膨胀机检（AP-34）— 条目>10 或 占全文行数>40% 则告警
  # 定位 Gotchas/踩坑 标题到下一个同级 ## 之间：统计 ### 条目数与段落行数
  gotcha="✅"
  gt_stats=$(awk -v total="$lines" '
    /^## .*([Gg]otcha|踩坑|排坑|坑记录)/ {flag=1; seclines=0; items=0; next}
    /^## / {flag=0}
    flag {
      seclines++
      if ($0 ~ /^### /) items++
    }
    END {
      pct = (total>0) ? (seclines*100/total) : 0
      printf "%d %d %d", items, seclines, pct
    }
  ' "$f" 2>/dev/null || echo "0 0 0")
  gt_items=$(echo "$gt_stats" | awk '{print $1}')
  gt_pct=$(echo "$gt_stats" | awk '{print $3}')
  if [ "${gt_items:-0}" -gt 10 ] || [ "${gt_pct:-0}" -gt 40 ]; then
    gotcha="⚠️${gt_items}条/${gt_pct}%"
  elif [ "${gt_items:-0}" -eq 0 ]; then
    gotcha="-"
  fi

  # L1-9: markdown 表格被空行截断机检（AP-39）— 表格块间仅隔一个空行且新块首行后无表头分隔行
  tbl_hits=""
  tbl_hits=$(python3 -c "
import sys,re
def trow(l):
    s=l.strip()
    return s.startswith('|') and s.endswith('|') and s.count('|')>=2
def sep(l):
    return bool(re.match(r'^\|[\s:\-|]+\|', l.strip()))
hits=[]
for path in sys.argv[1:]:
    lines=open(path,encoding='utf-8').read().split('\n')
    blocks=[];i=0;n=len(lines)
    while i<n:
        if trow(lines[i]):
            j=i
            while j+1<n and trow(lines[j+1]):
                j+=1
            blocks.append((i,j));i=j+1
        else:
            i+=1
    for k in range(1,len(blocks)):
        s=blocks[k][0];pe=blocks[k-1][1]
        if s-pe==2 and not (s+1<n and sep(lines[s+1])):
            hits.append(str(s+1))
print(','.join(hits))
" "$f" 2>/dev/null) || tbl_hits=""
  if [ -n "$tbl_hits" ]; then
    gotcha="❌TBL截断L${tbl_hits}"
    skill_ok=false
  fi

  # IRON LAW check — 存在性（无 IRON LAW 为警告而非强制失败）
  if grep -qi "IRON LAW" "$f"; then iron="✅"; else iron="⚠️建议"; fi

  # IRON LAW 差异化检查 — 有 IRON LAW 时必须是业务专属约束，不得只写通用套话
  il_diff="⚠️"
  if grep -qi "IRON LAW" "$f"; then
    # 优先提取 ## IRON LAW 段；若铁律以内联加粗行呈现，则回退读取该行。
    il_section=$(awk '/^## IRON LAW/{flag=1;next}/^## /{flag=0}flag' "$f")
    if [ -z "$il_section" ]; then
      il_section=$(grep -im1 "IRON LAW" "$f" || true)
    fi
    has_biz=$(echo "$il_section" | python3 -c "import sys,re; t=sys.stdin.read(); print(1 if re.search(r'禁止|必须|不得|告知|文档|报告|消息|触发', t) else 0)" 2>/dev/null || true)
    only_generic=$(echo "$il_section" | python3 -c "import sys,re; t=sys.stdin.read(); print(1 if re.search(r'shebang|set -euo|API Key', t) else 0)" 2>/dev/null || true)
    if [ "$has_biz" -gt 0 ]; then
      il_diff="✅"
    elif [ "$only_generic" -gt 0 ]; then
      il_diff="❌套话"; skill_ok=false
    else
      il_diff="⚠️待查"
    fi
  else
    il_diff="-"
  fi

  # Description check: double-quoted single line + 触发词 + 不适用
  desc_line=$(grep -m1 "^description:" "$f")
  if [ -z "$desc_line" ]; then
    desc="❌缺失"; skill_ok=false
  elif echo "$desc_line" | grep -qE '^description:[[:space:]]*".*"'; then
    has_trigger=$(echo "$desc_line" | grep -c "触发词\|触发条件\|trigger" || true)
    has_exclude=$(echo "$desc_line" | grep -c "不适用\|不用于" || true)
    if [ "$has_trigger" -gt 0 ] && [ "$has_exclude" -gt 0 ]; then
      desc="✅"
    elif [ "$has_trigger" -gt 0 ]; then
      desc="⚠️无排除"; skill_ok=false
    elif [ "$has_exclude" -gt 0 ]; then
      desc="⚠️无触发"; skill_ok=false
    else
      desc="⚠️缺两项"; skill_ok=false
    fi
  else
    desc="❌格式"; skill_ok=false
  fi

  # Security: restricted system URLs (domains configurable via RESTRICTED_DOMAINS, keep generic defaults)
  restricted_pattern="${RESTRICTED_DOMAINS:-hr\.internal\.example|okr\.internal\.example|talent\.internal\.example}"
  sec_hits=$(grep -cE "$restricted_pattern" "$f" 2>/dev/null || true)
  if [ "$sec_hits" -gt 0 ]; then sec="⚠️${sec_hits}处"; else sec="✅"; fi

  # ── Code Quality checks (scripts/ + assets/可执行文件) — L3/L7 automated subset ──
  skill_dir=$(dirname "$f")
  scripts_dir="${skill_dir}/scripts"
  assets_dir="${skill_dir}/assets"
  code="✅"
  code_issues=""

  # Build scan targets: scripts/ + assets/*.js + assets/*.py
  # 排除当前审计器自身：它包含用于匹配 eval/except/debug 的规则字面量，不能作为被审计代码误报。
  scan_files=""
  if [ -d "$scripts_dir" ]; then
    scan_files=$(find "$scripts_dir" -type f \( -name '*.py' -o -name '*.sh' \) ! -path "$SCRIPT_DIR/skill-audit.sh" 2>/dev/null || true)
  fi
  if [ -d "$assets_dir" ]; then
    assets_code=$(find "$assets_dir" -type f \( -name '*.py' -o -name '*.js' \) 2>/dev/null || true)
    scan_files="${scan_files}\n${assets_code}"
  fi

  if [ -n "$(echo -e "$scan_files" | tr -d '[:space:]')" ]; then
    # L3-2: eval/exec (critical — AP-23) — scan scripts/ + assets/
    eval_hits=$(echo -e "$scan_files" | xargs grep -rn 'ev[a]l(\|ex[e]c(' 2>/dev/null | grep -v 'safe_eval\|evaluate\|exec_' | wc -l || true)
    if [ "${eval_hits:-0}" -gt 0 ]; then code="❌"; code_issues="${code_issues}eval "; fi

    # L3-3: bare except (warning — AP-24)
    except_hits=$(echo -e "$scan_files" | xargs grep -rn 'except:\|except Exception' 2>/dev/null | wc -l || true)
    if [ "${except_hits:-0}" -gt 0 ]; then [ "$code" = "✅" ] && code="⚠️"; code_issues="${code_issues}except "; fi

    # L3-4: debug residual (warning — AP-25)
    debug_hits=$(echo -e "$scan_files" | xargs grep -rn 'if False\|import pdb\|breakpoint()' 2>/dev/null | wc -l || true)
    if [ "${debug_hits:-0}" -gt 0 ]; then [ "$code" = "✅" ] && code="⚠️"; code_issues="${code_issues}debug "; fi

    # L3-6: shebang in .sh files (warning — AP-17)
    for sh_file in "$scripts_dir"/*.sh; do
      [ -f "$sh_file" ] || continue
      if ! head -1 "$sh_file" | grep -q '^#!'; then
        [ "$code" = "✅" ] && code="⚠️"; code_issues="${code_issues}shebang "; break
      fi
    done

    # L7-5: .gitignore missing (warning — AP-32)
    if [ ! -f "${skill_dir}/.gitignore" ]; then
      [ "$code" = "✅" ] && code="⚠️"; code_issues="${code_issues}gitignore "
    fi

    # L7-6: platform artifacts (warning)
    artifact_found=$(find "$skill_dir" \( -name '.DS_Store' -o -name 'Thumbs.db' -o -name '__pycache__' \) 2>/dev/null | head -1 || true)
    if [ -n "$artifact_found" ]; then
      [ "$code" = "✅" ] && code="⚠️"; code_issues="${code_issues}artifacts "
    fi

    [ -z "$code_issues" ] && code_issues="-"
  else
    code_issues="N/A"
  fi

  # ── ICE-5 Closure Gate check (L10-2) ──
  # Only triggers when SKILL.md frontmatter explicitly declares ICE: required or incident-closure: required
  # Does NOT auto-flag based on fuzzy Chinese incident words or body-text mentions in backticks
  ice="-"
  # Extract frontmatter only (lines between first two --- delimiters)
  _frontmatter=$(awk '/^---$/{n++; next} n==1{print}' "$f" 2>/dev/null || true)
  ice_declared=$(echo "$_frontmatter" | grep -ciE 'ICE:\s*required|incident-closure:\s*required' 2>/dev/null || true)
  if [ "${ice_declared:-0}" -gt 0 ]; then
    # Look for closure_check/gate/quality check scripts
    closure_script=""
    for _pattern in 'closure_check*' '*gate*' '*quality*' '*audit*'; do
      _found=$(find "$skill_dir/scripts" -type f -name "$_pattern" 2>/dev/null | head -1 || true)
      if [ -n "$_found" ]; then
        closure_script="$_found"
        break
      fi
    done
    if [ -z "$closure_script" ]; then
      ice="❌无门"
      skill_ok=false
    else
      # ⚖️ Static check only — this audit tool never executes third-party scripts.
      # To verify a closure script actually exits 0, run it manually:
      #   bash <skill>/scripts/closure_check.sh
      case "$closure_script" in
        *.sh)
          if head -1 "$closure_script" 2>/dev/null | grep -q '^#!.*sh'; then
            ice="✅有门(静态)"
          else
            ice="⚠️有门但无shebang"
          fi
          ;;
        *)
          ice="✅有门(静态)"
          ;;
      esac
    fi
  fi

  printf "%-20s %5d %8s %8s %8s %8s %8s %8s %6s\n" "$name" "$lines" "$iron" "$il_diff" "$desc" "$sec" "$code" "$gotcha" "$ice"

  # Show code issues in verbose mode
  if [ "$VERBOSE" = true ] && [ -n "$code_issues" ] && [ "$code_issues" != "-" ] && [ "$code_issues" != "N/A" ]; then
    echo "    └─ CODE issues: $code_issues"
  fi

  if [ "$skill_ok" = true ] && [ "$sec_hits" -eq 0 ] && [ "$code" != "❌" ] && [ "$ice" != "❌无门" ] && [ "$ice" != "❌退出非0" ]; then
    pass=$((pass + 1))
  elif [ "$skill_ok" = false ] || [ "$code" = "❌" ] || [ "$ice" = "❌无门" ] || [ "$ice" = "❌退出非0" ]; then
    fail=$((fail + 1))
  else
    warn=$((warn + 1))
  fi
done

echo ""
echo "━━━ 脚本核验摘要（全面审计证据，不单独构成审计结论）━━━"
echo "对象: $total | ✅ 无阻断项: $pass | ⚠️ 需复核: $warn | ❌ 核验失败: $fail"

if [ "$VERBOSE" = true ]; then
  echo ""
  echo "规则说明:"
  echo "  IRON:    SKILL.md 中包含 'IRON LAW' 关键词"
  echo "  IL専:    IRON LAW 内容差异化检查（✅业务专属 / ❌套话 / ⚠️待查）"
  echo "  DESC:    description 双引号单行 + 含'触发词' + 含'不适用'"
  echo "  SEC:     不引用安全受限系统URL (hr/ehr/ov/goal等内部域名)"
  echo "  LINES:   >250行为信息提示(IRON LAW豁免场景不阻断)"
  echo "  CODE:    scripts/+assets/代码扫描(L3-2 eval/L3-3 except/L3-4 debug/L3-6 shebang/L7-5 gitignore/L7-6 artifacts)"
  echo "  GOTCHA:  Gotchas/踩坑段膨胀检测(L1-8/AP-34): 条目>10 或 占全文>40% 告警——提示按分层处置下沉到 troubleshooting.md"
  echo "  TBL:     markdown表格被空行截断检测(L1-9/AP-39): 表格块间仅隔空行且新块无表头分隔行=❌, 修复=删空行或给新块加表头"
  echo "  ICE:     SKILL.md标ICE:required时须有closure_check/gate/quality脚本(静态检查存在性+shebang, 执行验证请手动运行该脚本); 未标记则不检查"
fi

# ── 全面审计的 56 项 10 层逐项清单（每次都打印）──
echo ""
echo "━━━ 全面审计：10层56项逐项清单（逐项确认后再发布）━━━"
echo ""
echo "【L1 文档结构】(9项, 6可自动化)"
echo "  [ ] L1-1  IRON LAW: frontmatter后第一位, 业务专属; 无高频风险可不写"
echo "  [ ] L1-2  description: 单行无emoji+触发词+不适用 | 无禁止词 | 触发范围与定位匹配"
echo "  [ ] L1-3  intro: 三段式有emoji≠description, tags≥6; SKILL.md无intro字段"
echo "  [ ] L1-4  name: 小写+数字+连字符, 与目录名完全一致"
echo "  [ ] L1-5  行数≤300; 超限不直接判红,先评估能否拆分而不降效果,做不到则保留超行数视为通过(IRON LAW 5/AP-1)"
echo "  [ ] L1-6  references/索引: 所有文件存在+SKILL.md有索引"
echo "  [ ] L1-7  版本历史不入SKILL.md: 只留1行版本号+CHANGELOG链接 (AP-33)"
echo "  [ ] L1-8  Gotchas未膨胀: 踩坑段条目≤10且占全文≤40%; 超标按分层处置(删除/上浮/下沉)到troubleshooting.md (AP-34)"
echo "  [ ] L1-9  表格连续性: markdown表格无空行截断; 跨表格必须空行+完整新表头 (AP-39)"
echo ""
echo "【L2 架构一致性】(5项, 2可自动化)"
echo "  [ ] L2-1  逻辑冲突: 新旧规则不矛盾? 编号/数量声明与实际一致? 因果闭环"
echo "  [ ] L2-2  阶段编号+入口/出口 | 无AP-1~39 | 指令可yes/no验证"
echo "  [ ] L2-3  跨章节一致: 原则↔AP↔事故三处对应? 联动表/正文无矛盾?"
echo "  [ ] L2-4  交互一致: 多模式/分支流程描述不矛盾"
echo "  [ ] L2-5  版本号: 改动幅度与版本号匹配"
echo ""
echo "【L3 代码质量】(8项, 6可自动化, scripts/+assets/可执行文件)"
echo "  [ ] L3-1  API契约: 函数签名与调用方参数匹配"
echo "  [ ] L3-2  无ev""al()/ex""ec()执行用户输入 (AP-23)"
echo "  [ ] L3-3  异常宽度: 无bare except/except Exception (AP-24)"
echo "  [ ] L3-4  无调试残留: if False/pdb/breakpoint() (AP-25)"
echo "  [ ] L3-5  无废弃API调用 (AP-26)"
echo "  [ ] L3-6  Shell脚本有shebang+set-euo (AP-17)"
echo "  [ ] L3-7  硬编码: 脚本固定值已参数化"
echo "  [ ] L3-8  功能退化: 改动未破坏已有功能"
echo ""
echo "【L4 跨文件一致性】(5项, 1可自动化)"
echo "  [ ] L4-1  模板双源: 同一内容不在SKILL.md和references/各存一份"
echo "  [ ] L4-2  信息冗余: 清单条目未被正文流程自动覆盖"
echo "  [ ] L4-3  共享模式一致: 多脚本共享的utils/类/函数用法一致"
echo "  [ ] L4-4  数值一致性: 跨文件尺寸/字号/坐标/色值统一(viewBox/font-size/hex/间距)"
echo "  [ ] L4-5  附件职责唯一: 同一主题不在templates/和references/同时存在功能等价文件 (AP-36)"
echo ""
echo "【L5 文档↔代码对齐】(3项, 2可自动化, scripts/+test-output参考实现)"
echo "  [ ] L5-1  参数表一致: SKILL.md/references中CLI参数与脚本实际一致"
echo "  [ ] L5-2  功能路由完整: 列出的功能/命令在脚本中均有实现"
echo "  [ ] L5-3  参考实现正确性: 示例代码/模板/SVG语法正确且与文档对齐"
echo ""
echo "【L6 依赖完整性】(3项, 2可自动化, scripts/ only)"
echo "  [ ] L6-1  import↔requirements: 脚本import的第三方库均在requirements.txt声明"
echo "  [ ] L6-2  技术栈表: frontmatter/SKILL.md声明的技术栈与实际使用一致"
echo "  [ ] L6-3  可选依赖有fallback: try/except ImportError降级处理"
echo ""
echo "【L7 文件卫生】(6项, 5可自动化)"
echo "  [ ] L7-1  僵尸文件: references/所有文件均被SKILL.md引用"
echo "  [ ] L7-2  断链引用: SKILL.md引用的references/文件均真实存在"
echo "  [ ] L7-3  路径孤儿: .skillignore/README/脚本旧路径已同步更新"
echo "  [ ] L7-4  用户态数据: 未混入已安装列表/快照/偏好等个性化文件"
echo "  [ ] L7-5  .gitignore: 有scripts/时必须存在 (AP-32)"
echo "  [ ] L7-6  无平台产物: .DS_Store/Thumbs.db/__pycache__已排除"
echo ""
echo "【L8 安全合规】(4项, 3可自动化)"
echo "  [ ] L8-1  安全扫描: 无平台密钥/AK/SK/cookie | 无组织/人才/高敏数据 | 无受限系统 | 无真实内部账号"
echo "  [ ] L8-2  内部API: SSO方案确定+无硬编码凭据"
echo "  [ ] L8-3  frontmatter/metadata无真实内部账号 (AP-21)"
echo "  [ ] L8-4  _meta.json含凭据已.skillignore排除 (AP-22)"
echo ""
echo "【L9 健壮性&降级】(7项, 1可自动化)"
echo "  [ ] L9-1  降级链: 每个外部依赖(API/CLI/认证)均有失败场景处理"
echo "  [ ] L9-2  改动类有Confirmation Gate"
echo "  [ ] L9-3  流水线有子Agent最小规范(≤30行)"
echo "  [ ] L9-4  数据量限制: 批量操作有limit/截断/分页 (AP-13)"
echo "  [ ] L9-5  大文件截断: 读取/输出有字数/行数上限 (AP-15)"
echo "  [ ] L9-6  路径安全: 用os.path.splitext而非字符串替换 (AP-30)"
echo "  [ ] L9-7  资源遍历上限: 遍历循环有行数/条数上限 (AP-31)"
echo ""
echo "【L10 内容质量】(6项, 2可自动化)"
echo "  [ ] L10-1 可验证性: 指令可yes/no判断"
echo "  [ ] L10-2 AP清零: 无AP-1~39反模式; 标ICE:required时须有closure_check.*或等价质量门且运行退出0"
echo "  [ ] L10-3 文案质量: 无错别字/歧义/矛盾"
echo "  [ ] L10-4 已知局限: 每条含三要素(能力边界→触发条件→降级路径); P/D/E分类标注; 同类合并; ≤3条; 重要性降序(三维:不可逆性/发生概率/影响范围); 非硬伤不收入; 无降级路径=AP-37"
echo "  [ ] L10-5 停滞检测: 含循环/迭代/Cron的Skill有stale_count机制"
echo "  [ ] L10-6 边缘输入覆盖: 极短/极长/空输入/非预期语言等边界条件有处理指引或在已知局限中声明"
echo ""
echo "以上仅为脚本核验证据；必须与其余审计判断合并，逐项完成56项全面审计后，才能进入发布流程。"

# 审计发现阻断项必须以非零退出码传递给调用方；否则 ICE 无门会显示失败却仍被流水线放行。
if [ "$fail" -gt 0 ]; then
  exit 1
fi
