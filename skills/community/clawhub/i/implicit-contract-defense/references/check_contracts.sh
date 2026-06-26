#!/usr/bin/env bash
# ============================================================
# check_contracts.sh — 隐式契约防御通用检测脚本
#
# 用法: ./check_contracts.sh [src_dir]
# 默认 src_dir = ./src
#
# Agent 须知：根据项目实际情况修改下方 CONFIG 区域的路径
# ============================================================

set -euo pipefail

# ============================================================
# CONFIG — Agent 根据项目修改此区域
# ============================================================
SRC_DIR="${1:-./src}"

# API 契约文件名（不含路径，脚本自动在 SRC_DIR 中查找）
CONTRACTS_FILE="contracts.rs"

# 常量文件名
CONSTS_FILE="consts.rs"

# 前端生成类型文件名（用于提示，不做前端扫描）
FRONTEND_GENERATED_FILE="types.generated.ts"

# ============================================================
# 内部变量
# ============================================================
ERRORS=0
WARNINGS=0

red()    { printf "\033[31m%s\033[0m\n" "$1"; }
yellow() { printf "\033[33m%s\033[0m\n" "$1"; }
green()  { printf "\033[32m%s\033[0m\n" "$1"; }

error()   { red "  ❌ $1"; ERRORS=$((ERRORS + 1)); }
warn()    { yellow "  ⚠ $1"; WARNINGS=$((WARNINGS + 1)); }
ok()      { green "  ✅ $1"; }

# 自动检测 entity 目录
detect_entity_dir() {
    grep -rl "DeriveEntityModel" "$SRC_DIR" 2>/dev/null | xargs -I{} dirname {} | sort -u
}

# 自动检测契约文件路径
detect_contracts_file() {
    find "$SRC_DIR" -name "$CONTRACTS_FILE" 2>/dev/null | head -1
}

ENTITY_DIRS=$(detect_entity_dir)
CONTRACTS_PATH=$(detect_contracts_file)

echo "═══════════════════════════════════════"
echo "  🔒 隐式契约防御 — 全面检测"
echo "═══════════════════════════════════════"
echo ""
echo "  源码目录: $SRC_DIR"
echo "  契约文件: ${CONTRACTS_PATH:-未检测到}"
echo "  Entity 目录: ${ENTITY_DIRS:-未检测到}"
echo ""

# ============================================================
# 1. 数据库操作只走 SeaORM
# ============================================================
echo "🔍 [1] 数据库契约"

# 1a. 禁止其他数据库库
other_db_libs=$(grep -rn \
    -e "use rusqlite" \
    -e "use sqlx" \
    -e "use diesel" \
    -e "use tokio_postgres" \
    -e "use mysql" \
    "$SRC_DIR" 2>/dev/null || true)

if [ -n "$other_db_libs" ]; then
    error "发现非 SeaORM 数据库库引用:"
    while IFS= read -r line; do red "     $line"; done <<< "$other_db_libs"
else
    ok "未发现其他数据库库"
fi

# 1b. 禁止裸 SQL
raw_sql=$(grep -rn \
    -e "execute_unprepared" \
    -e "query_raw" \
    --include="*.rs" \
    "$SRC_DIR" 2>/dev/null \
    | grep -v "///\|//\|#\[" \
    || true)

if [ -n "$raw_sql" ]; then
    error "发现裸 SQL 操作:"
    while IFS= read -r line; do red "     $line"; done <<< "$raw_sql"
else
    ok "未发现裸 SQL 操作"
fi

# 1c. 禁止硬编码 SQL 语句
hardcoded_sql=$(grep -rn \
    -E "(\"|\')\ *(INSERT INTO|SELECT .+ FROM|UPDATE .+ SET|DELETE FROM)" \
    --include="*.rs" \
    "$SRC_DIR" 2>/dev/null \
    | grep -v "///\|//\|#\[\|doc\|test\|migration" \
    || true)

if [ -n "$hardcoded_sql" ]; then
    error "发现硬编码 SQL 语句:"
    while IFS= read -r line; do red "     $line"; done <<< "$hardcoded_sql"
else
    ok "未发现硬编码 SQL 语句"
fi

echo ""

# ============================================================
# 2. 类型安全
# ============================================================
echo "🔍 [2] 类型安全"

# 2a. #[ts(export)] 只允许在契约文件中
if [ -n "$CONTRACTS_PATH" ]; then
    ts_export_elsewhere=$(grep -rn '#\[ts(export)\]' --include="*.rs" "$SRC_DIR" 2>/dev/null \
        | grep -v "$CONTRACTS_FILE" \
        || true)

    if [ -n "$ts_export_elsewhere" ]; then
        error "#[ts(export)] 出现在 $CONTRACTS_FILE 之外:"
        while IFS= read -r line; do red "     $line"; done <<< "$ts_export_elsewhere"
    else
        ok "#[ts(export)] 仅出现在 $CONTRACTS_FILE"
    fi
else
    warn "未找到 $CONTRACTS_FILE，跳过 ts(export) 检查"
fi

# 2b. Entity 中禁止 serde_json::Value
if [ -n "$ENTITY_DIRS" ]; then
    json_value=$(grep -rn "serde_json::Value" $ENTITY_DIRS 2>/dev/null \
        | grep -v "///\|//" || true)
    if [ -n "$json_value" ]; then
        warn "Entity 中使用了 serde_json::Value（建议用强类型 struct）:"
        while IFS= read -r line; do yellow "     $line"; done <<< "$json_value"
    else
        ok "Entity 中未使用弱类型 JSON"
    fi
fi

# 2c. Entity 中禁止 NaiveDateTime
if [ -n "$ENTITY_DIRS" ]; then
    naive_dt=$(grep -rn "NaiveDateTime" $ENTITY_DIRS 2>/dev/null \
        | grep -v "///\|//" || true)
    if [ -n "$naive_dt" ]; then
        error "Entity 中使用了 NaiveDateTime（应用 DateTimeUtc）:"
        while IFS= read -r line; do red "     $line"; done <<< "$naive_dt"
    else
        ok "Entity 中未使用 NaiveDateTime"
    fi
fi

# 2d. col_expr 中禁止字符串字面量
col_expr_str=$(grep -rn \
    -e 'col_expr.*Expr::value.*"' \
    --include="*.rs" "$SRC_DIR" 2>/dev/null \
    | grep -v "///\|//" || true)

if [ -n "$col_expr_str" ]; then
    error "col_expr 中使用了字符串字面量（应用 ActiveModel 替代）:"
    while IFS= read -r line; do red "     $line"; done <<< "$col_expr_str"
else
    ok "col_expr 未使用字符串字面量"
fi

echo ""

# ============================================================
# 3. 魔法值检测
# ============================================================
echo "🔍 [3] 魔法值"

# 检测业务代码中的裸数字常量（排除 0/1、测试、entity、consts 本身）
magic_numbers=$(
    find "$SRC_DIR" -name '*.rs' \
        ! -name "$CONSTS_FILE" \
        ! -name "*.entity.rs" \
        ! -path '*/entity/*' \
        ! -path '*/test*' \
        ! -path '*/migration*' \
        -exec awk '
            /^#\[cfg\(test\)\]/ { exit }
            /\/\/|\/\*|#\[/ { next }
            # 匹配裸数字 >= 2 出现在比较或赋值中（排除常见的 port/array index/bit shift 等）
            /[><=!]+[[:space:]]*[0-9]{2,}/ { print FILENAME ":" NR ": " $0 }
            /[[:space:]][0-9]{4,}[[:space:]]/ { print FILENAME ":" NR ": " $0 }
        ' {} \; 2>/dev/null \
    | sort -u \
    || true
)

if [ -n "$magic_numbers" ]; then
    warn "疑似魔法数字（确认是否应提取到 $CONSTS_FILE）:"
    while IFS= read -r line; do yellow "     $line"; done <<< "$magic_numbers"
else
    ok "未发现明显魔法数字"
fi

# 检测裸字符串做状态/类型判断
magic_strings=$(grep -rn \
    -E '==\s*"[a-z_]+"' \
    --include="*.rs" "$SRC_DIR" 2>/dev/null \
    | grep -v "///\|//\|#\[\|test\|$CONSTS_FILE" \
    | grep -v -E '==[[:space:]]*"(true|false|ok|error|GET|POST|PUT|DELETE)"' \
    || true)

if [ -n "$magic_strings" ]; then
    warn "疑似用裸字符串做判断（应用 enum 或常量替代）:"
    while IFS= read -r line; do yellow "     $line"; done <<< "$magic_strings"
else
    ok "未发现裸字符串判断"
fi

echo ""

# ============================================================
# 4. 业务规范
# ============================================================
echo "🔍 [4] 业务规范"

# 4a. 状态变更检查 can_transition_to
status_updates=$(
    find "$SRC_DIR" -name '*.rs' \
        -exec awk '
            /^#\[cfg\(test\)\]/ { exit }
            /\.status[[:space:]]*=[[:space:]]*Set\(/ { print FILENAME ":" NR ": " $0 }
        ' {} \; 2>/dev/null \
    | grep -v "///\|//" \
    || true
)

if [ -n "$status_updates" ]; then
    has_unchecked=false
    while IFS= read -r line; do
        file=$(echo "$line" | cut -d: -f1)
        lineno=$(echo "$line" | cut -d: -f2)
        start=$((lineno - 15))
        [ "$start" -lt 1 ] && start=1
        nearby=$(sed -n "${start},${lineno}p" "$file" 2>/dev/null \
            | grep -c "can_transition_to" || true)
        nearby=$((nearby + 0))
        if [ "$nearby" -eq 0 ]; then
            warn "状态变更未见 can_transition_to 检查: $line"
            has_unchecked=true
        fi
    done <<< "$status_updates"
    [ "$has_unchecked" = false ] && ok "状态变更均有流转检查"
else
    ok "未发现状态变更操作"
fi

# 4b. 软删除查询过滤
if [ -n "$ENTITY_DIRS" ]; then
    soft_delete_entities=$(grep -rl "is_deleted" $ENTITY_DIRS 2>/dev/null | sort -u || true)
    for entity_file in $soft_delete_entities; do
        [ -f "$entity_file" ] || continue
        entity_name=$(basename "$entity_file" .rs)
        [ "$entity_name" = "mod" ] && continue

        entity_finds=$(grep -rn "${entity_name}::Entity::find" "$SRC_DIR" 2>/dev/null || true)
        if [ -n "$entity_finds" ]; then
            while IFS= read -r line; do
                file=$(echo "$line" | cut -d: -f1)
                lineno=$(echo "$line" | cut -d: -f2)
                has_filter=$(sed -n "${lineno},$((lineno + 10))p" "$file" 2>/dev/null \
                    | grep -c "is_deleted\|IsDeleted" || echo "0")
                if [ "$has_filter" -eq 0 ]; then
                    warn "查询软删除表 ${entity_name} 未见 is_deleted 过滤: $line"
                fi
            done <<< "$entity_finds"
        fi
    done
fi

echo ""

# ============================================================
# 5. Entity 文件完整性
# ============================================================
echo "🔍 [5] Entity 文件完整性"

if [ -z "$ENTITY_DIRS" ]; then
    yellow "  ⚠ 未检测到 Entity 文件，跳过"
else
    for dir in $ENTITY_DIRS; do
        for file in "$dir"/*.rs; do
            [ -f "$file" ] || continue
            fname=$(basename "$file")
            [ "$fname" = "mod.rs" ] && continue
            [ "$fname" = "prelude.rs" ] && continue

            # 文件级 doc comment
            if ! head -3 "$file" | grep -q "^//!"; then
                error "$fname 缺少文件级 doc comment（//! 开头）"
            fi

            # 状态枚举的 can_transition_to
            has_enum=$(grep -c "DeriveActiveEnum" "$file" 2>/dev/null || true)
            has_enum=$((has_enum + 0))
            if [ "$has_enum" -gt 0 ]; then
                has_transition=$(grep -c "can_transition_to" "$file" 2>/dev/null || true)
                has_transition=$((has_transition + 0))
                if [ "$has_transition" -eq 0 ]; then
                    has_status=$(grep -E "enum.*(Status|State)" "$file" || true)
                    if [ -n "$has_status" ]; then
                        warn "$fname 有状态枚举但未定义 can_transition_to()"
                    fi
                fi
            fi

            # 字段注释覆盖度
            pub_fields=$(grep -c "pub " "$file" 2>/dev/null || true)
            pub_fields=$((pub_fields + 0))
            doc_comments=$(grep -c "/// " "$file" 2>/dev/null || true)
            doc_comments=$((doc_comments + 0))
            if [ "$pub_fields" -gt 4 ] && [ "$doc_comments" -lt 3 ]; then
                warn "$fname 字段注释偏少（$doc_comments 个注释 / $pub_fields 个字段）"
            fi
        done
    done
fi

echo ""

# ============================================================
# 汇总
# ============================================================
echo "═══════════════════════════════════════"
if [ "$ERRORS" -gt 0 ]; then
    red "  ❌ 发现 $ERRORS 个错误，$WARNINGS 个警告"
    exit 1
elif [ "$WARNINGS" -gt 0 ]; then
    yellow "  ⚠ 无错误，$WARNINGS 个警告（建议修复）"
    exit 0
else
    green "  ✅ 所有检查通过"
    exit 0
fi
