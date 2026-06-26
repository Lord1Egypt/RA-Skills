#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════════
# generate-api-client.sh — 从 OpenAPI YAML 自动生成 TypeScript apiClient.ts
#
# 用法:
#   bash references/generate-api-client.sh standards/lexguard-openapi.yaml > frontend/src/api/generated/apiClient.ts
#   bash references/generate-api-client.sh standards/yujuzhilian-openapi.yaml
#
# 功能:
#   1. 从 YAML 的 paths 提取每个端点 → 生成 export const xxx = { ... } 函数
#   2. 从 components/schemas 生成 TypeScript interface 类型定义
#   3. 保留 request/configureApiClient/ApiError 基础设施
#   4. 函数签名从 YAML parameters 和 requestBody 派生
#   5. 纯 bash + awk/sed 实现，不依赖 yq/jq/Python
#
# 依赖: bash 4+, awk (POSIX), sed (POSIX), grep (POSIX)
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

YAML_FILE="${1:-}"

# ── 错误处理 ─────────────────────────────────────────────────────────────────
if [ -z "$YAML_FILE" ]; then
  echo "❌ 用法: $0 <openapi-yaml-file> [> output.ts]" >&2
  echo "" >&2
  echo "示例:" >&2
  echo "  $0 standards/lexguard-openapi.yaml > frontend/src/api/generated/apiClient.ts" >&2
  exit 1
fi

if [ ! -f "$YAML_FILE" ]; then
  echo "❌ 文件不存在: $YAML_FILE" >&2
  exit 1
fi

if [ ! -r "$YAML_FILE" ]; then
  echo "❌ 文件不可读: $YAML_FILE" >&2
  exit 1
fi

if ! grep -q '^openapi:' "$YAML_FILE" 2>/dev/null; then
  echo "❌ 不是有效的 OpenAPI 文件（缺少 'openapi:' 字段）" >&2
  exit 1
fi

if ! grep -q '^paths:' "$YAML_FILE" 2>/dev/null; then
  echo "❌ YAML 中缺少 'paths:' 定义（没有端点可生成）" >&2
  exit 1
fi

# ── 提取项目名（用于注释） ───────────────────────────────────────────────────
PROJECT_TITLE=$(grep -m1 '^\s*title:' "$YAML_FILE" 2>/dev/null | \
  sed 's/.*title:[[:space:]]*"\([^"]*\)".*/\1/;s/.*title:[[:space:]]*'\''\([^'\'']*\)'\''.*/\1/;s/.*title:[[:space:]]*\(.*\)/\1/' | \
  sed 's/[[:space:]]*$//')

if [ -z "$PROJECT_TITLE" ]; then
  PROJECT_TITLE="$(basename "$YAML_FILE" .yaml)"
fi

# ═══════════════════════════════════════════════════════════════════════════════
# 输出 TypeScript apiClient.ts
# ═══════════════════════════════════════════════════════════════════════════════

cat << END_HEADER
/**
 * ⚠️ 本文件由 OpenAPI 契约自动生成，前端 agent 禁止手改。
 * 新增端点流程：改 standards/{project}-openapi.yaml → 重新运行 generate-api-client.sh → 两端同步。
 *
 * 项目: ${PROJECT_TITLE}
 * 生成时间: $(date '+%Y-%m-%d %H:%M:%S')
 * 源文件:  ${YAML_FILE}
 * 生成命令:
 *   bash references/generate-api-client.sh ${YAML_FILE}
 */
/* eslint-disable */

// ── 运行时配置 ────────────────────────────────────
let _baseUrl = '';
let _getToken: () => string | null = () => null;

export function configureApiClient(opts: { baseUrl: string; getToken: () => string | null }) {
  _baseUrl = opts.baseUrl;
  _getToken = opts.getToken;
}

// ── 请求基础设施 ──────────────────────────────────
async function request<T>(method: string, path: string, body?: unknown, params?: Record<string, string>): Promise<T> {
  const url = new URL(\`\${_baseUrl}\${path}\`);
  if (params) Object.entries(params).forEach(([k, v]) => { if (v !== undefined) url.searchParams.set(k, v); });

  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  const token = _getToken();
  if (token) headers['Authorization'] = \`Bearer \${token}\`;

  const res = await fetch(url.toString(), { method, headers, body: body ? JSON.stringify(body) : undefined });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ message: res.statusText }));
    throw new ApiError(res.status, err.message ?? res.statusText);
  }
  return res.json();
}

export class ApiError extends Error {
  constructor(public status: number, message: string) { super(message); this.name = 'ApiError'; }
}

// ── 类型别名 ──────────────────────────────────────
type Single<T> = { code: number; message: string; data: T };
type Paginated<T> = { code: number; message: string; data: { records: T[]; total: number; page: number; size: number } };
END_HEADER

# ═══════════════════════════════════════════════════════════════════════════════
# 阶段 1: 生成 TypeScript 类型定义（从 components/schemas）
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "// ══════════════════════════════════════════════════════"
echo "// 类型定义（从 components/schemas 自动生成）"
echo "// ══════════════════════════════════════════════════════"

# 先提取 schemas 段落到临时文件，便于 awk 解析
SCHEMA_SECTION=$(mktemp)
trap "rm -f '$SCHEMA_SECTION'" EXIT

awk '
/^  schemas:/        { flag=1; next }
/^  [a-z]/ && flag   { flag=0 }  # 下一个兄弟键结束 schemas 段
/^[a-zA-Z]/ && flag  { flag=0 }  # 顶层键也结束
flag                 { print }
' "$YAML_FILE" > "$SCHEMA_SECTION"

# 解析 schemas 并输出 TypeScript interfaces
awk '
function trim(s) {
  gsub(/^[[:space:]]+|[[:space:]]+$/, "", s)
  return s
}
function get_indent(s) {
  match(s, /^[[:space:]]*/)
  return RLENGTH
}
function map_type(t) {
  if (t == "string")  return "string"
  if (t == "integer") return "number"
  if (t == "number")  return "number"
  if (t == "boolean") return "boolean"
  if (t == "object")  return "Record<string, unknown>"
  if (t == "array")   return "unknown[]"
  return "unknown"
}

# 跟踪 schema 顶层定义的缩进
/^    [A-Z]/ {
  # 退出前保存挂起的属性（处理无空行分隔的连续 schema）
  if (in_props && cur_prop != "" && prop_type_buf != "") {
    if (schema_prop_count > 0) schema_props = schema_props "\n"
    schema_props = schema_props "  " cur_prop ": " prop_type_buf ";"
    schema_prop_count++
    schema_has_props = 1
  }
  # 新 schema 开始 → 先输出上一个
  if (schema_name != "" && schema_has_props) {
    print_schema()
  }
  schema_name = trim($0)
  sub(/:$/, "", schema_name)
  schema_type = ""
  schema_item_type = ""
  in_props = 0
  in_items = 0
  cur_prop = ""
  prop_type_buf = ""
  schema_props = ""
  schema_prop_count = 0
  schema_has_props = 0
  next
}

# schema 级别的 type（无 properties 的简单类型）
schema_name != "" && !in_props && /^      type:/ {
  schema_type = $0
  sub(/^[[:space:]]*type:[[:space:]]*"?/, "", schema_type)
  sub(/"?[[:space:]]*$/, "", schema_type)
}

# schema 级别的 items（数组类型）
schema_name != "" && !in_props && /^      items:/ {
  in_items = 1
}
schema_name != "" && in_items && /^        type:/ {
  t = $0; sub(/^[[:space:]]*type:[[:space:]]*"?/, "", t); sub(/"?[[:space:]]*$/, "", t)
  schema_item_type = t
}

# 进入 properties 块
schema_name != "" && /^      properties:/ {
  in_props = 1
  props_base_indent = get_indent($0)
  cur_prop = ""
  prop_type_buf = ""
  next
}

# properties 块内：属性名（比 properties 多缩进 2 格）
schema_name != "" && in_props {
  ind = get_indent($0)
  # 属性名行（不在更深嵌套里）
  if (ind == props_base_indent + 2 && $0 !~ /^[[:space:]]+(type|format|description|example|items|properties|required|\$ref|allOf|oneOf|anyOf|nullable|default|enum|readOnly|writeOnly|deprecated):/) {
    # 保存上一个属性
    if (cur_prop != "" && prop_type_buf != "") {
      if (schema_prop_count > 0) schema_props = schema_props "\n"
      schema_props = schema_props "  " cur_prop ": " prop_type_buf ";"
      schema_prop_count++
    }
    cur_prop = trim($0)
    sub(/:$/, "", cur_prop)
    prop_type_buf = ""
    # type 可能在同行
    if ($0 ~ /type:[[:space:]]*"?[a-z]+"?/) {
      t = $0; sub(/.*type:[[:space:]]*"?/, "", t); sub(/"?[,;].*/, "", t); sub(/"?[[:space:]]*$/, "", t)
      prop_type_buf = map_type(t)
    }
    # items 可能在同行（数组简写）
    if ($0 ~ /type:[[:space:]]*"?array"?/ && $0 ~ /items:/) {
      it = $0; sub(/.*items:[[:space:]]*\{[[:space:]]*type:[[:space:]]*"?/, "", it); sub(/"?[[:space:]]*\}.*/, "", it)
      prop_type_buf = map_type(it) "[]"
    }
    # $ref 可能在同行
    if ($0 ~ /\$ref:/) {
      r = $0; sub(/.*\$ref:[[:space:]]*"[^"]*\//, "", r); sub(/".*/, "", r)
      prop_type_buf = r
    }
  }
  # type: 在下一行（更深缩进）
  else if (cur_prop != "" && prop_type_buf == "" && $0 ~ /type:[[:space:]]*"?[a-z]+"?/) {
    t = $0; sub(/^[[:space:]]*type:[[:space:]]*"?/, "", t); sub(/"?[[:space:]]*$/, "", t)
    prop_type_buf = map_type(t)
  }
  # $ref: 在下一行
  else if (cur_prop != "" && prop_type_buf == "" && $0 ~ /\$ref:/) {
    r = $0; sub(/.*\$ref:[[:space:]]*"[^"]*\//, "", r); sub(/".*/, "", r)
    prop_type_buf = r
  }
  # items 在下一行（数组）
  else if (cur_prop != "" && prop_type_buf == "" && $0 ~ /^[[:space:]]*items:/) {
    # 先标记，等 type 行
    prop_type_buf = "__ARRAY__"
  }
  else if (cur_prop != "" && prop_type_buf == "__ARRAY__" && $0 ~ /type:/) {
    t = $0; sub(/^[[:space:]]*type:[[:space:]]*"?/, "", t); sub(/"?[[:space:]]*$/, "", t)
    prop_type_buf = map_type(t) "[]"
  }
  # 遇到与 properties 同级或更浅的缩进 → 退出 properties 块
  else if (ind <= props_base_indent) {
    # 保存最后一个属性
    if (cur_prop != "" && prop_type_buf != "") {
      if (schema_prop_count > 0) schema_props = schema_props "\n"
      schema_props = schema_props "  " cur_prop ": " prop_type_buf ";"
      schema_prop_count++
    }
    if (schema_prop_count > 0) schema_has_props = 1
    in_props = 0
    cur_prop = ""
    prop_type_buf = ""
  }
}

function print_schema() {
  # 不再跳过内置 schema，全部生成接口；由调用方按需使用
  if (0) { }
  printf "export interface %s {\n", schema_name
  if (schema_has_props) {
    printf "%s\n", schema_props
  } else if (schema_type == "object") {
    printf "  [key: string]: unknown;\n"
  } else if (schema_type == "array") {
    printf "  // Array of %s\n", (schema_item_type != "" ? map_type(schema_item_type) : "unknown")
    printf "  [index: number]: %s;\n", (schema_item_type != "" ? map_type(schema_item_type) : "unknown")
  } else if (schema_type != "") {
    printf "  // Type alias for %s\n", schema_type
  } else {
    printf "  [key: string]: unknown;\n"
  }
  printf "}\n\n"
}

END {
  # 输出最后一个 schema
  if (schema_name != "" && schema_has_props) {
    print_schema()
  }
}
' "$SCHEMA_SECTION"

# ═══════════════════════════════════════════════════════════════════════════════
# 阶段 2: 生成 API 函数（从 paths）
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "// ══════════════════════════════════════════════════════"
echo "// API 函数（从 paths 自动生成）"
echo "// ══════════════════════════════════════════════════════"

# 提取 paths 段落到临时文件
PATHS_SECTION=$(mktemp)
trap "rm -f '$SCHEMA_SECTION' '$PATHS_SECTION'" EXIT

awk '
/^paths:/           { flag=1; next }
/^[a-zA-Z]/ && flag { flag=0 }
flag                { print }
' "$YAML_FILE" > "$PATHS_SECTION"

# 解析 paths 并生成端点数据（用特殊分隔符输出，shell 再组装）
# 格式: GROUP|OPID|METHOD|PATH|SUMMARY|PARAMS|BODY_TYPE|RESP_TYPE
awk '
function trim(s) {
  gsub(/^[[:space:]]+|[[:space:]]+$/, "", s)
  return s
}
function get_indent(s) {
  match(s, /^[[:space:]]*/)
  return RLENGTH
}
function map_type(t) {
  if (t == "string")  return "string"
  if (t == "integer") return "number"
  if (t == "number")  return "number"
  if (t == "boolean") return "boolean"
  if (t == "object")  return "Record<string, unknown>"
  return "unknown"
}

# ── 路径行 ──
/^  \// {
  # 检测新路径 → 输出上一个端点
  if (method != "" && op_id != "") output_endpoint()

  path = $0; sub(/:$/, "", path); sub(/^[[:space:]]+/, "", path)
  method = ""; op_id = ""; summary = ""; tag_group = ""
  params_str = ""; body_type = ""; resp_type = "any"
  in_tags = 0; in_params = 0; in_reqbody = 0; in_resp = 0
  in_200 = 0; in_200_schema = 0; in_200_content = 0; in_allof = 0
  allof_extra = ""
  reqbody_ref = ""
  param_name_buf = ""; param_in_buf = ""
  reqbody_props_buf = ""; reqbody_in_props = 0; reqbody_props_indent = 0
  cur_req_prop = ""; cur_req_prop_type = ""
}

# ── HTTP 方法行 ──
/^    (get|post|put|delete|patch|options):/ {
  if (method != "" && op_id != "") output_endpoint()

  match($0, /^[[:space:]]*([a-z]+):/, a)
  method = toupper(a[1])
  op_id = ""; summary = ""; tag_group = ""
  params_str = ""; body_type = ""; resp_type = "any"
  in_tags = 0; in_params = 0; in_reqbody = 0; in_resp = 0
  in_200 = 0; in_200_schema = 0; in_200_content = 0; in_allof = 0
  allof_extra = ""
  reqbody_ref = ""
  param_name_buf = ""; param_in_buf = ""
  reqbody_props_buf = ""; reqbody_in_props = 0; reqbody_props_indent = 0
  cur_req_prop = ""; cur_req_prop_type = ""
}

# ── operationId ──
method != "" && /^      operationId:/ {
  op_id = $0; sub(/^[[:space:]]*operationId:[[:space:]]*"?/, "", op_id); sub(/"?[[:space:]]*$/, "", op_id)
}

# ── summary ──
method != "" && /^      summary:/ {
  summary = $0
  sub(/^[[:space:]]*summary:[[:space:]]*>?[[:space:]]*/, "", summary)
  gsub(/^"/, "", summary); gsub(/"$/, "", summary)
  gsub(/^\x27/, "", summary); gsub(/\x27$/, "", summary)
}

# ── tags 行 → 开始收集 tag ──
method != "" && /^      tags:/  { in_tags = 1
  # 处理内联格式: tags: [xxx, yyy]
  if ($0 ~ /\[/) {
    tag_raw = $0
    sub(/^[[:space:]]*tags:[[:space:]]*\[/, "", tag_raw)
    sub(/\].*/, "", tag_raw)
    gsub(/"/, "", tag_raw); gsub(/^\x27/, "", tag_raw); gsub(/\x27$/, "", tag_raw)
    split(tag_raw, tags_arr, ",")
    for (i in tags_arr) {
      t = tags_arr[i]; gsub(/^[[:space:]]+|[[:space:]]+$/, "", t)
      if (tag_group == "") {
        extract_group(t)
      }
    }
    in_tags = 0
  }
}

# 辅助函数：从 tag 名提取分组
function extract_group(tag,  group) {
  if (tag ~ / - /) {
    split(tag, parts, " - ")
    group = parts[2]
    gsub(/[[:space:]-]+/, "", group)
    if (group != "") {
      tag_group = tolower(substr(group, 1, 1)) substr(group, 2)
    }
  }
  if (tag_group == "") {
    gsub(/[^a-zA-Z0-9]/, "", tag)
    if (tag != "") tag_group = tolower(substr(tag, 1, 1)) substr(tag, 2)
  }
}

# ── tag 列表项 ──
method != "" && in_tags && /^        - / {
  tag_raw = $0
  sub(/^[[:space:]]*-[[:space:]]*/, "", tag_raw)
  gsub(/"/, "", tag_raw); gsub(/^\x27/, "", tag_raw); gsub(/\x27$/, "", tag_raw)
  gsub(/[[:space:]]+$/, "", tag_raw)
  if (tag_group == "") extract_group(tag_raw)
}

# ── 退出 tags 块 ──
method != "" && in_tags && $0 !~ /^        - / && $0 !~ /^      tags:/ { in_tags = 0 }

# ── parameters 块 ──
method != "" && /^      parameters:/ {
  in_params = 1
  param_name_buf = ""; param_in_buf = ""
}

method != "" && in_params && /^        - name:/ {
  param_name_buf = $0; sub(/^[[:space:]]*-[[:space:]]*name:[[:space:]]*"?/, "", param_name_buf); sub(/"?[[:space:]]*$/, "", param_name_buf)
  param_in_buf = ""
}
method != "" && in_params && param_name_buf != "" && /^          in:/ {
  param_in_buf = $0; sub(/^[[:space:]]*in:[[:space:]]*"?/, "", param_in_buf); sub(/"?[[:space:]]*$/, "", param_in_buf)
  if (param_in_buf == "query") {
    if (params_str != "") params_str = params_str ", "
    params_str = params_str param_name_buf "?: string"
  }
  if (param_in_buf == "path") {
    # path params are part of the URL template, not function params
  }
  param_name_buf = ""; param_in_buf = ""
}
method != "" && in_params && /^      [a-z]/ && $0 !~ /^      (parameters|requestBody|responses|security):/ {
  if ($0 !~ /^        /) {
    in_params = 0
    param_name_buf = ""; param_in_buf = ""
  }
}

# ── requestBody 块 ──
method != "" && /^      requestBody:/ { in_reqbody = 1 }

# requestBody 中的 $ref
method != "" && in_reqbody && /\$ref:/ {
  r = $0; sub(/.*\$ref:[[:space:]]*"[^"]*\//, "", r); sub(/".*/, "", r)
  reqbody_ref = r
  body_type = r
}

# requestBody 中有 content → schema（内联对象）
method != "" && in_reqbody && /schema:/ { in_reqbody_schema = 1 }

# schema 中的 $ref
method != "" && in_reqbody_schema && /\$ref:/ {
  r = $0; sub(/.*\$ref:[[:space:]]*"[^"]*\//, "", r); sub(/".*/, "", r)
  body_type = r
}

# schema 中的 type: object → 准备收集 properties
method != "" && in_reqbody_schema && /type:[[:space:]]*object/ {
  # type is object, will collect properties
}

# schema 中的 type: 非 object
method != "" && in_reqbody_schema && !reqbody_in_props && /type:/ && $0 !~ /object/ {
  t = $0; sub(/^[[:space:]]*type:[[:space:]]*"?/, "", t); sub(/"?[[:space:]]*$/, "", t)
  body_type = map_type(t)
}

# schema 中的 properties: → 开始收集属性
method != "" && in_reqbody_schema && /properties:/ {
  reqbody_in_props = 1
  reqbody_props_indent = get_indent($0)
  cur_req_prop = ""; cur_req_prop_type = ""
  reqbody_props_buf = ""
  next
}

# properties 中的属性名
method != "" && reqbody_in_props {
  ind = get_indent($0)
  if (ind == reqbody_props_indent + 2 && $0 !~ /^[[:space:]]+(type|format|description|\$ref|items):/) {
    # 保存上一个
    if (cur_req_prop != "" && cur_req_prop_type != "") {
      if (reqbody_props_buf != "") reqbody_props_buf = reqbody_props_buf "; "
      reqbody_props_buf = reqbody_props_buf cur_req_prop ": " cur_req_prop_type
    }
    cur_req_prop = trim($0); sub(/:$/, "", cur_req_prop)
    cur_req_prop_type = ""
    if ($0 ~ /type:[[:space:]]*"?[a-z]+"?/) {
      t = $0; sub(/.*type:[[:space:]]*"?/, "", t); sub(/"?.*/, "", t)
      cur_req_prop_type = map_type(t)
    }
    if ($0 ~ /\$ref:/) {
      r = $0; sub(/.*\$ref:[[:space:]]*"[^"]*\//, "", r); sub(/".*/, "", r)
      cur_req_prop_type = r
    }
  }
  # type 在下一行
  else if (cur_req_prop != "" && cur_req_prop_type == "" && $0 ~ /type:[[:space:]]*"?[a-z]+"?/) {
    t = $0; sub(/^[[:space:]]*type:[[:space:]]*"?/, "", t); sub(/"?[[:space:]]*$/, "", t)
    cur_req_prop_type = map_type(t)
  }
  # $ref 在下一行
  else if (cur_req_prop != "" && cur_req_prop_type == "" && $0 ~ /\$ref:/) {
    r = $0; sub(/.*\$ref:[[:space:]]*"[^"]*\//, "", r); sub(/".*/, "", r)
    cur_req_prop_type = r
  }
  # 退出 properties
  else if (ind <= reqbody_props_indent) {
    if (cur_req_prop != "" && cur_req_prop_type != "") {
      if (reqbody_props_buf != "") reqbody_props_buf = reqbody_props_buf "; "
      reqbody_props_buf = reqbody_props_buf cur_req_prop ": " cur_req_prop_type
    }
    if (reqbody_props_buf != "") {
      body_type = "{ " reqbody_props_buf " }"
    }
    reqbody_in_props = 0
    cur_req_prop = ""; cur_req_prop_type = ""
  }
}

# ── responses 块 ──
method != "" && /^      responses:/ { in_resp = 1; in_200 = 0; in_200_schema = 0; in_200_content = 0; in_allof = 0; resp_type = "any" }

method != "" && in_resp && /^        "200":/ { in_200 = 1 }

method != "" && in_resp && in_200 && /^          content:/ { in_200_content = 1 }

method != "" && in_200_content && /schema:/ { in_200_schema = 1 }

# 200 schema 中的 $ref（直接引用 ApiResponse 等）—— 不在 allOf 内才生效
method != "" && in_200_schema && !in_allof && /\$ref:/ {
  r = $0; sub(/.*\$ref:[[:space:]]*"[^"]*\//, "", r); sub(/".*/, "", r)
  resp_type = r
}

# 200 schema 中的 allOf（ApiResponse + 额外 data）
method != "" && in_200_schema && /allOf:/ { in_allof = 1 }

# allOf 中的 $ref（通常是 ApiResponse）
method != "" && in_allof && /\$ref:.*ApiResponse/ && resp_type == "any" {
  allof_extra = "ApiResponse"
}
# allOf 中有额外的 type: object（补充 data 字段）
method != "" && in_allof && /type:[[:space:]]*object/ && allof_extra != "" && allof_extra !~ /& \{ data:/ {
  allof_extra = allof_extra " & { data: Record<string, unknown> }"
}
# allof 退出：遇到非深入缩进的下一属性
method != "" && in_allof && /^      [a-z]/ && $0 !~ /^        / {
  resp_type = (allof_extra != "" ? allof_extra : "any")
  in_allof = 0
  allof_extra = ""
}

# ── 退出各子块 ──
method != "" && in_params && /^      [a-z]/ && $0 !~ /^      parameters:/ && $0 !~ /^        / { in_params = 0 }
method != "" && in_reqbody && /^      [a-z]/ && $0 !~ /^      requestBody:/ && $0 !~ /^        / { in_reqbody = 0; in_reqbody_schema = 0; reqbody_ref = "" }
method != "" && in_resp && /^      [a-z]/ && $0 !~ /^      responses:/ && $0 !~ /^        / { in_resp = 0; in_200 = 0; in_200_schema = 0; in_200_content = 0; in_allof = 0 }

# ── 遇到新路径 → 输出端点 ──
/^  \// && method != "" {
  if (op_id != "") output_endpoint()
}

# 输出当前端点
function output_endpoint() {
  # 清理挂起的 allOf 额外信息
  if (in_allof && allof_extra != "") {
    resp_type = allof_extra
    in_allof = 0
    allof_extra = ""
  }
  # 分组名默认用 tag_group，没有则用 "api"
  grp = (tag_group != "" ? tag_group : "api")
  # 构造请求体签名
  if (body_type == "" && (method == "POST" || method == "PUT" || method == "PATCH")) {
    body_type = "Record<string, unknown>"
  }
  # 用 | 分隔各字段
  printf "ENDPOINT|%s|%s|%s|%s|%s|%s|%s|%s\n",
    grp, op_id, method, path, summary, params_str, body_type, resp_type
}

END {
  # 输出最后一个端点
  if (method != "" && op_id != "") output_endpoint()
}
' "$PATHS_SECTION" | sort -t'|' -k1,1 -k3,3 -k2,2 | \
awk -F'|' '
function to_camel(s) {
  # 将 operationId 转为 camelCase（已经是，但确保首字母小写）
  if (s == "") return s
  return tolower(substr(s, 1, 1)) substr(s, 2)
}
BEGIN {
  prev_group = ""
  first_group = 1
}
{
  group = $2
  op_id = to_camel($3)
  # 如果 operationId 以分组名开头，去掉前缀（如 authHealth → health）
  if (group != "" && tolower(op_id) ~ ("^" tolower(group)) && length(op_id) > length(group)) {
    stripped = substr(op_id, length(group) + 1)
    op_id = tolower(substr(stripped, 1, 1)) substr(stripped, 2)
  }
  method = $4
  path = $5
  summary = $6
  params_str = $7
  body_type = $8
  resp_type = $9

  # 新 group
  if (group != prev_group) {
    if (prev_group != "") printf "};\n\n"
    printf "export const %s = {\n", group
    prev_group = group
  }

  # JSDoc 注释
  if (summary != "") printf "  /** %s */\n", summary

  # 构造函数签名
  sig_parts = ""
  if (body_type != "" && body_type != "null") {
    sig_parts = sig_parts "body: " body_type
  }
  if (params_str != "") {
    if (sig_parts != "") sig_parts = sig_parts ", "
    sig_parts = sig_parts "params?: { " params_str " }"
  }

  # request 调用
  req_args = ""
  req_args = req_args "\x27" method "\x27, \x27" path "\x27"
  if (body_type != "" && body_type != "null") {
    req_args = req_args ", body"
  } else {
    req_args = req_args ", undefined"
  }
  if (params_str != "") {
    req_args = req_args ", params"
  } else {
    req_args = req_args ", undefined"
  }

  if (sig_parts != "") {
    printf "  %s: (%s) =>\n    request<%s>(%s),\n", op_id, sig_parts, resp_type, req_args
  } else {
    printf "  %s: () =>\n    request<%s>(%s),\n", op_id, resp_type, req_args
  }
  printf "\n"
}
END {
  if (prev_group != "") printf "};\n"
}
'

# ── 清理 ─────────────────────────────────────────────────────────────────────
rm -f "$SCHEMA_SECTION" "$PATHS_SECTION"
trap - EXIT

exit 0
