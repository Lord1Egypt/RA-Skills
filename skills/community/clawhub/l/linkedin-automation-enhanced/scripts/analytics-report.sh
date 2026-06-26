#!/bin/bash
# =============================================================================
# LinkedIn Analytics Report Script
# =============================================================================
# PURPOSE:
#   Generate markdown analytics report from extracted JSON data with
#   benchmark comparisons, trend analysis, and actionable recommendations.
#
# REQUIREMENTS:
#   - analytics-extract.sh executed first (generates JSON input)
#   - jq installed for JSON processing
#   - bc installed for calculations
#
# USAGE:
#   ./analytics-report.sh [YYYY-MM-DD]
#   ./analytics-report.sh              # Use today's date
#   ./analytics-report.sh 2026-05-07   # Use specific date
#
# INPUT:
#   - JSON: system/linkedin-analytics/YYYY-MM-DD.json
#   - Log:  system/logs/linkedin-analytics.log
#
# OUTPUT:
#   - Markdown: system/linkedin-reports/YYYY-MM-DD.md
#   - Log:      system/logs/linkedin-analytics.log
#
# AUTHOR: Renato MB (via OpenClaw Agent)
# VERSION: 2.0.0
# LAST UPDATED: 2026-05-07
# =============================================================================

set -euo pipefail

# Configuration
DATE="${1:-$(date +%Y-%m-%d)}"
INPUT_FILE="system/linkedin-analytics/$DATE.json"
OUTPUT_FILE="system/linkedin-reports/$DATE.md"
WORKSPACE_DIR="$HOME/vaults/openclaw/workspace"
LOG_FILE="${OPENCLAW_LOG_FILE:-$WORKSPACE_DIR/logs/scripts.log}"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Benchmarks
BENCHMARK_ER=5.0
BENCHMARK_CR=1.0

# Retry configuration for file operations
MAX_RETRIES=3
RETRY_DELAYS=(1 2 4)

# =============================================================================
# Logging Functions
# =============================================================================

log() {
    local level="$1"
    local message="$2"
    echo "[$TIMESTAMP] [$level] $message" >> "$LOG_FILE"
    echo "[$level] $message"
}

log_info() { log "INFO" "$1"; }
log_warn() { log "WARN" "$1"; }
log_error() { log "ERROR" "$1"; }

# =============================================================================
# Retry Logic for File Operations
# =============================================================================

retry_file_operation() {
    local attempt=1
    local operation="$1"
    local description="$2"
    
    while [[ $attempt -le $MAX_RETRIES ]]; do
        log_info "File operation attempt $attempt/$MAX_RETRIES: $description"
        
        if eval "$operation"; then
            log_info "File operation successful on attempt $attempt"
            return 0
        fi
        
        if [[ $attempt -lt $MAX_RETRIES ]]; then
            local delay=${RETRY_DELAYS[$((attempt-1))]}
            log_warn "File operation failed. Retrying in ${delay}s..."
            sleep $delay
        fi
        
        ((attempt++))
    done
    
    log_error "File operation failed after $MAX_RETRIES attempts: $description"
    return 1
}

# =============================================================================
# JSON Validation Function
# =============================================================================

validate_json() {
    local json_file="$1"
    
    # Check 1: File exists
    if [[ ! -f "$json_file" ]]; then
        log_error "❌ JSON file does not exist: $json_file"
        return 1
    fi
    
    # Check 2: File is not empty
    if [[ ! -s "$json_file" ]]; then
        log_error "❌ JSON file is empty: $json_file"
        return 1
    fi
    
    # Check 3: Valid JSON syntax
    if ! jq '.' "$json_file" > /dev/null 2>&1; then
        log_error "❌ Invalid JSON syntax in: $json_file"
        return 1
    fi
    
    # Check 4: Required fields exist
    local required_fields=("status" "summary.total_impressions" "summary.total_engagements")
    for field in "${required_fields[@]}"; do
        if ! jq -e ".$field" "$json_file" > /dev/null 2>&1; then
            log_warn "⚠️ Missing field: $field (using default)"
        fi
    done
    
    log_info "✅ JSON validation passed"
    return 0
}

# =============================================================================
# Manual Report Fallback
# =============================================================================

generate_manual_report() {
    local date="$1"
    local output="$2"
    
    log_warn "Generating manual report template (extraction failed)"
    
    cat > "$output" << EOF
# LinkedIn Analytics Report — $date

**Gerado em:** $(date +%Y-%m-%d\ %H:%M)
**Período:** Últimos 7 dias
**Status da Extração:** ❌ FAILED - Dados não disponíveis

---

## ⚠️ Dados Não Disponíveis

A extração automática falhou. Preencha manualmente:

### 📊 Resumo da Semana (Manual)

| Métrica | Valor | Benchmark | Status |
|---------|-------|-----------|--------|
| **Impressões Totais** | _preencher_ | - | - |
| **Engajamentos Totais** | _preencher_ | - | - |
| **Engagement Rate** | _preencher_ | ${BENCHMARK_ER}% | - |
| **Comment Rate** | _preencher_ | ${BENCHMARK_CR}% | - |

---

## 📝 Posts da Semana (Manual)

| Data | Post (preview) | Impressões | Reações | Comentários | ER |
|------|----------------|------------|---------|-------------|-----|
| _preencher_ | _preencher_ | - | - | - | - |

---

## 📥 Inbound Leads (Manual)

| Data | Nome | Cargo | Empresa | Origem | Tipo | ICP Fit |
|------|------|-------|---------|--------|------|---------|
| - | - | - | - | - | - | - |

**Meta:** 1-3 inbound ICP/mês

---

## ✅ Ações Recomendadas

- [ ] Revisar falha na extração (ver log: system/logs/linkedin-analytics.log)
- [ ] Preencher métricas manualmente
- [ ] Preencher inbound leads
- [ ] Agendar próxima extração

---

**Nota:** Extração automática falhou. Verifique:
1. Browser está rodando? \`openclaw browser status\`
2. LinkedIn login ativo?
3. Permissões de arquivo?
EOF

    log_info "Manual report template generated: $output"
}

# =============================================================================
# Main Script
# =============================================================================

log_info "═══════════════════════════════════════════"
log_info "📊 LINKEDIN ANALYTICS REPORT STARTED"
log_info "═══════════════════════════════════════════"
log_info "Data: $DATE"
log_info "Input: $INPUT_FILE"
log_info "Output: $OUTPUT_FILE"

# Validate JSON input
if ! validate_json "$INPUT_FILE"; then
    log_warn "JSON validation failed. Generating manual report fallback..."
    generate_manual_report "$DATE" "$OUTPUT_FILE"
    echo ""
    echo "⚠️ Report template gerado (dados não disponíveis)"
    echo "📄 Ver: $OUTPUT_FILE"
    exit 0
fi

# Read data from JSON with retry logic
read_json_field() {
    local field="$1"
    local default="$2"
    local result
    
    result=$(jq -r ".$field // \"$default\"" "$INPUT_FILE" 2>/dev/null || echo "$default")
    echo "$result"
}

TOTAL_IMPRESSIONS=$(read_json_field "summary.total_impressions" "0")
TOTAL_ENGAGEMENTS=$(read_json_field "summary.total_engagements" "0")
AVG_ER=$(read_json_field "summary.engagement_rate" "0")
AVG_CR=$(read_json_field "summary.comment_rate" "0")
EXTRACTION_STATUS=$(read_json_field "status" "unknown")
POSTS_COUNT=$(read_json_field "posts_count" "0")

# Classify performance
classify_performance() {
    local value="$1"
    local benchmark="$2"
    local warning_threshold="$3"
    
    if (( $(echo "$value >= $benchmark" | bc -l 2>/dev/null || echo 0) )); then
        echo "✅ Sucesso"
    elif (( $(echo "$value >= $warning_threshold" | bc -l 2>/dev/null || echo 0) )); then
        echo "⚠️ Atenção"
    else
        echo "❌ Fracasso"
    fi
}

ER_STATUS=$(classify_performance "$AVG_ER" "$BENCHMARK_ER" "3.0")
CR_STATUS=$(classify_performance "$AVG_CR" "$BENCHMARK_CR" "0.5")

# Determine overall status
if [[ "$ER_STATUS" == "✅ Sucesso" && "$CR_STATUS" == "✅ Sucesso" ]]; then
    OVERALL_STATUS="✅ Estratégia funcionando"
    OVERALL_MESSAGE="Ambas métricas acima do benchmark. Manter estratégia de conteúdo."
    ACTIONS="- [ ] Manter estratégia de conteúdo
- [ ] Escalar formatos que funcionam"
elif [[ "$ER_STATUS" == "⚠️ Atenção" || "$CR_STATUS" == "⚠️ Atenção" ]]; then
    OVERALL_STATUS="⚠️ Ajustes necessários"
    OVERALL_MESSAGE="Uma ou mais métricas na zona de atenção. Testar novos formatos/hooks."
    ACTIONS="- [ ] Testar novos hooks (primeiras linhas)
- [ ] Adicionar mais perguntas/CTAs nos posts
- [ ] Revisar formato (bullet points, line breaks)"
else
    OVERALL_STATUS="❌ Mudança estratégica necessária"
    OVERALL_MESSAGE="Métricas abaixo do benchmark por 3+ semanas. Revisar conteúdo e público."
    ACTIONS="- [ ] Revisar público-alvo do conteúdo
- [ ] Testar formatos radicalmente diferentes
- [ ] Pedir feedback direto (DM, pesquisa)"
fi

# Generate report markdown with retry logic for file write
log_info "Generating markdown report..."

REPORT_CONTENT=$(cat << EOF
# LinkedIn Analytics Report — $DATE

**Gerado em:** $(date +%Y-%m-%d\ %H:%M)
**Período:** Últimos 7 dias
**Status da Extração:** $EXTRACTION_STATUS
**Posts Analisados:** $POSTS_COUNT

---

## 📊 Resumo da Semana

| Métrica | Valor | Benchmark | Status |
|---------|-------|-----------|--------|
| **Impressões Totais** | $TOTAL_IMPRESSIONS | - | - |
| **Engajamentos Totais** | $TOTAL_ENGAGEMENTS | - | - |
| **Engagement Rate** | ${AVG_ER}% | ${BENCHMARK_ER}% | $ER_STATUS |
| **Comment Rate** | ${AVG_CR}% | ${BENCHMARK_CR}% | $CR_STATUS |

---

## 🎯 Classificação Geral

**Status:** $OVERALL_STATUS

$OVERALL_MESSAGE

---

## 📝 Posts da Semana

<!-- TODO: Preencher com dados dos posts individuais -->

| Data | Post (preview) | Impressões | Reações | Comentários | ER |
|------|----------------|------------|---------|-------------|-----|
| - | - | - | - | - | - |

---

## 📥 Inbound Leads

<!-- Preencher manualmente -->

| Data | Nome | Cargo | Empresa | Origem | Tipo | ICP Fit |
|------|------|-------|---------|--------|------|---------|
| - | - | - | - | - | - | - |

**Meta:** 1-3 inbound ICP/mês

---

## 🔄 Trends (4 semanas)

<!-- Preencher manualmente nas primeiras semanas -->

| Semana | Engagement Rate | Trend |
|--------|-----------------|-------|
| $DATE | ${AVG_ER}% | - |

---

## ✅ Ações Recomendadas

$ACTIONS

---

## 📌 Próximos Passos

1. Revisar este report com Renato
2. Preencher inbound leads manualmente
3. Decidir ajustes de estratégia (se necessário)
4. Agendar próxima extração (sexta que vem, 17:30)

---

**Arquivo de dados brutos:** \`system/linkedin-analytics/$DATE.json\`
**Log da extração:** \`system/logs/linkedin-analytics.log\`
EOF
)

# Write report with retry logic
retry_file_operation "echo \"$REPORT_CONTENT\" > \"$OUTPUT_FILE\"" "Write report to $OUTPUT_FILE"

# Verify file was written
if [[ ! -f "$OUTPUT_FILE" ]]; then
    log_error "❌ Failed to create report file"
    exit 1
fi

log_info "═══════════════════════════════════════════"
log_info "✅ REPORT GENERATED SUCCESSFULLY"
log_info "═══════════════════════════════════════════"
log_info "📄 Report: $OUTPUT_FILE"
echo ""
echo "📄 Preview (first 30 lines):"
echo "───────────"
head -30 "$OUTPUT_FILE"
echo ""
echo "───────────"
echo ""
echo "Report completo salvo em: $OUTPUT_FILE"

exit 0
