# 🦞 li_maestro_evaluate — MAESTRO Threat Modeling Skill

---

## 🌐 English

**Description:** Interactive CSA MAESTRO threat modeling for agentic AI systems and OpenCode Skills. Produces multi-format risk assessments (.md/.docx/.xlsx) with AI risk classification mapping to China's 《人工智能安全治理框架》2.0.

**Two analysis modes:**
- **Full Assessment (默认):** 10-phase Q&A with all 7+1 MAESTRO layers, cross-layer analysis, full threat register, mitigations, code validation, residual risk.
- **MVTM Checklist (快速):** 10-item checklist per MAESTRO Minimum Viable Threat Model standard + China regulatory extension. Faster pass/fail evaluation with agent-driven threat analysis (Checks 6-7). Includes Scope Warning when system triggers Full/Standard criteria.

**Usage via ClawHub:**

```bash
# Install the skill
clawhub install li_maestro_evaluate

# Run threat modeling (varies by agent)
# In OpenCode: load the skill, choose analysis mode, and follow the workflow
# Full Assessment output: threat-models/<project>-<YYYYMMDD-HHMM>/01-business-context.md ... 10-output-summary.md
# MVTM Checklist output: threat-models/<project>-mvtm-<YYYYMMDD-HHMM>/01-mvtm-checklist.md
```

**Prerequisites:** OpenCode, Claude Code, or any compatible AI agent. For .docx/.xlsx output, install `python-docx openpyxl` or have WPS Office available.

---

## 🌏 中文

**说明：** 基于 CSA MAESTRO 框架的交互式威胁建模评估工具，面向智能体 AI 系统及 OpenCode Skill。支持两种分析模式：
- **全面风险评估（默认）：** 10 阶段 Q&A 流程，覆盖 7+1 MAESTRO 层、跨层分析、完整威胁登记表、缓解措施、代码验证、残余风险。
- **MVTM 快速检查表：** 10 项检查表流程，基于 MAESTRO 官方 MVTM 标准 + 中国法规扩展。快速通过/未通过评估，Check 6-7 由 AI 驱动自动生成威胁建议。当系统触发 Full/Standard 条件时输出范围限制警告。

输出多格式风险评估报告（.md/.docx/.xlsx），包含《人工智能安全治理框架》2.0 版三级九子类风险分类对照表。

**通过 ClawHub 使用：**

```bash
# 安装 skill
clawhub install li_maestro_evaluate

# 运行威胁建模（因 Agent 而异）
# 在 OpenCode 中：加载 skill，选择分析模式，按流程操作
# 全面评估输出：threat-models/<project>-<YYYYMMDD-HHMM>/01-business-context.md ... 10-output-summary.md
# MVTM 输出：threat-models/<project>-mvtm-<YYYYMMDD-HHMM>/01-mvtm-checklist.md
```

**前置条件：** OpenCode、Claude Code 或兼容的 AI Agent。如需生成 .docx/.xlsx 输出，安装 `python-docx openpyxl` 或确保 WPS Office 可用。

---

## 🇯🇵 日本語

**説明：** エージェンティック AI システムと OpenCode スキルのためのインタラクティブな CSA MAESTRO 脅威モデリングツール。中国《人工智能安全治理框架》2.0 版に準拠した AI リスク分類マッピング付きのマルチフォーマットリスク評価レポート（.md/.docx/.xlsx）を生成します。

**2つの分析モード:**
- **フルアセスメント（デフォルト）：** 10フェーズのQ&A、7+1 MAESTROレイヤー、クロスレイヤー分析、完全な脅威登録、緩和策、コード検証、残留リスク。
- **MVTMチェックリスト（クイック）：** MAESTRO公式MVTM標準＋中国規制拡張に基づく10項目チェックリスト。迅速な合格/不合格評価。Check 6-7はAI駆動。システムがFull/Standard条件をトリガーする場合、スコープ警告を出力。

**ClawHub での使用：**

```bash
# スキルをインストール
clawhub install li_maestro_evaluate

# 脅威モデリングを実行（エージェントにより異なります）
# OpenCode の場合：スキルをロードし、分析モードを選択して操作
# フル出力：threat-models/<project>-<YYYYMMDD-HHMM>/01-business-context.md ... 10-output-summary.md
# MVTM出力：threat-models/<project>-mvtm-<YYYYMMDD-HHMM>/01-mvtm-checklist.md
```

**前提条件：** OpenCode、Claude Code、または互換性のある AI エージェント。.docx/.xlsx 出力には `python-docx openpyxl` のインストールまたは WPS Office が必要です。

---

## 🇰🇷 한국어

**설명:** 에이전틱 AI 시스템 및 OpenCode Skill을 위한 대화형 CSA MAESTRO 위협 모델링 도구입니다. 중국 《人工智能安全治理框架》2.0에 매핑된 AI 위험 분류표가 포함된 다중 형식 위험 평가 보고서(.md/.docx/.xlsx)를 생성합니다.

**2가지 분석 모드:**
- **전체 평가 (기본값):** 10단계 Q&A, 7+1 MAESTRO 레이어, 크로스 레이어 분석, 전체 위협 등록, 완화 조치, 코드 검증, 잔여 위험.
- **MVTM 체크리스트 (빠른):** MAESTRO 공식 MVTM 표준 + 중국 규제 확장 기반 10항목 체크리스트. 빠른 통과/실패 평가. Check 6-7은 AI 구동. 시스템이 Full/Standard 조건을 트리거하면 범위 경고 출력.

**ClawHub 사용법:**

```bash
# 스킬 설치
clawhub install li_maestro_evaluate

# 위협 모델링 실행 (에이전트에 따라 다름)
# OpenCode의 경우: 스킬 로드 후 분석 모드 선택하여 진행
# 전체 출력: threat-models/<project>-<YYYYMMDD-HHMM>/01-business-context.md ... 10-output-summary.md
# MVTM 출력: threat-models/<project>-mvtm-<YYYYMMDD-HHMM>/01-mvtm-checklist.md
```

**전제 조건:** OpenCode, Claude Code 또는 호환 가능한 AI 에이전트. .docx/.xlsx 출력에는 `python-docx openpyxl` 설치 또는 WPS Office가 필요합니다.

---

## 🇷🇺 Русский

**Описание:** Интерактивный инструмент моделирования угроз CSA MAESTRO для агентных AI-систем и навыков OpenCode. Создает многоформатные отчеты оценки рисков (.md/.docx/.xlsx) с картой классификации рисков ИИ по стандарту 《人工智能安全治理框架》2.0.

**Два режима анализа:**
- **Полная оценка (по умолчанию):** 10-фазный Q&A, 7+1 уровней MAESTRO, межуровневый анализ, полный реестр угроз, меры смягчения, проверка кода, остаточный риск.
- **MVTM чек-лист (быстрый):** 10 пунктов по стандарту MVTM MAESTRO + расширение для китайских нормативов. Быстрая оценка пройден/не пройден. Пункты 6-7 на основе AI. Предупреждение об ограничениях при триггере Full/Standard.

**Использование через ClawHub:**

```bash
# Установка навыка
clawhub install li_maestro_evaluate

# Запуск моделирования угроз (зависит от агента)
# В OpenCode: загрузите навык, выберите режим анализа
# Полный вывод: threat-models/<project>-<YYYYMMDD-HHMM>/01-business-context.md ... 10-output-summary.md
# MVTM вывод: threat-models/<project>-mvtm-<YYYYMMDD-HHMM>/01-mvtm-checklist.md
```

**Требования:** OpenCode, Claude Code или совместимый AI-агент. Для вывода .docx/.xlsx установите `python-docx openpyxl` или используйте WPS Office.

---

## 🇪🇸 Español

**Descripción:** Herramienta interactiva de modelado de amenazas CSA MAESTRO para sistemas de IA agentivos y Skills de OpenCode. Produce informes de evaluación de riesgos en múltiples formatos (.md/.docx/.xlsx) con mapeo de clasificación de riesgos de IA según el estándar chino 《人工智能安全治理框架》2.0.

**Dos modos de análisis:**
- **Evaluación completa (predeterminado):** Q&A de 10 fases, 7+1 capas MAESTRO, análisis entre capas, registro de amenazas completo, mitigaciones, validación de código, riesgo residual.
- **Lista MVTM (rápida):** Lista de 10 ítems según estándar MVTM MAESTRO + extensión regulatoria china. Evaluación rápida de aprobado/fallido. Ítems 6-7 impulsados por IA. Advertencia de alcance cuando el sistema activa criterios Full/Standard.

**Uso mediante ClawHub:**

```bash
# Instalar el skill
clawhub install li_maestro_evaluate

# Ejecutar modelado de amenazas (varía según el agente)
# En OpenCode: cargue el skill, seleccione modo de análisis
# Salida completa: threat-models/<project>-<YYYYMMDD-HHMM>/01-business-context.md ... 10-output-summary.md
# Salida MVTM: threat-models/<project>-mvtm-<YYYYMMDD-HHMM>/01-mvtm-checklist.md
```

**Requisitos:** OpenCode, Claude Code o cualquier agente de IA compatible. Para salida .docx/.xlsx, instale `python-docx openpyxl` o tenga WPS Office disponible.

---

## 🇫🇷 Français

**Description :** Outil interactif de modélisation des menaces CSA MAESTRO pour les systèmes d'IA agentifs et les compétences OpenCode. Produit des rapports d'évaluation des risques multi-formats (.md/.docx/.xlsx) avec une cartographie de classification des risques IA selon le cadre chinois 《人工智能安全治理框架》2.0.

**Deux modes d'analyse :**
- **Évaluation complète (par défaut) :** Q&A en 10 phases, 7+1 couches MAESTRO, analyse inter-couches, registre des menaces complet, mesures d'atténuation, validation de code, risque résiduel.
- **Checklist MVTM (rapide) :** 10 éléments selon la norme MVTM MAESTRO + extension réglementaire chinoise. Évaluation rapide réussi/échoué. Éléments 6-7 pilotés par IA. Avertissement de périmètre si le système déclenche les critères Full/Standard.

**Utilisation via ClawHub :**

```bash
# Installer la compétence
clawhub install li_maestro_evaluate

# Exécuter la modélisation des menaces (varie selon l'agent)
# Dans OpenCode : chargez la compétence, sélectionnez le mode d'analyse
# Sortie complète : threat-models/<project>-<YYYYMMDD-HHMM>/01-business-context.md ... 10-output-summary.md
# Sortie MVTM : threat-models/<project>-mvtm-<YYYYMMDD-HHMM>/01-mvtm-checklist.md
```

**Prérequis :** OpenCode, Claude Code ou tout agent IA compatible. Pour la sortie .docx/.xlsx, installez `python-docx openpyxl` ou disposez de WPS Office.

---

## 🇸🇦 العربية

**الوصف:** أداة تفاعلية لنمذجة التهديدات باستخدام إطار CSA MAESTRO للأنظمة الذكية العاملة بالوكلاء ومهارات OpenCode. تُنتج تقارير تقييم المخاطر بتنسيقات متعددة (.md/.docx/.xlsx) مع تصنيف مخاطر الذكاء الاصطناعي وفقًا لإطار 《人工智能安全治理框架》2.0 الصيني.

**وضعا التحليل:**
- **التقييم الكامل (افتراضي):** أسئلة وأجوبة من 10 مراحل، 7+1 طبقات MAESTRO، تحليل عبر الطبقات، سجل تهديدات كامل، تخفيف، التحقق من الكود، المخاطر المتبقية.
- **قائمة MVTM (سريع):** 10 عناصر وفقًا لمعيار MVTM الرسمي من MAESTRO + تمديد اللوائح الصينية. تقييم سريع ناجح/راسب. العناصر 6-7 مدفوعة بالذكاء الاصطناعي. تحذير النطاق عند تفعيل معايير Full/Standard.

**الاستخدام عبر ClawHub:**

```bash
# تثبيت المهارة
clawhub install li_maestro_evaluate

# تشغيل نمذجة التهديدات (يختلف حسب الوكيل)
# في OpenCode: قم بتحميل المهارة، اختر وضع التحليل
# المخرجات الكاملة: threat-models/<project>-<YYYYMMDD-HHMM>/01-business-context.md ... 10-output-summary.md
# مخرجات MVTM: threat-models/<project>-mvtm-<YYYYMMDD-HHMM>/01-mvtm-checklist.md
```

**المتطلبات الأساسية:** OpenCode أو Claude Code أو أي وكيل ذكاء اصطناعي متوافق. لإخراج .docx/.xlsx، قم بتثبيت `python-docx openpyxl` أو استخدم WPS Office.

---

## 📦 Skill Metadata

| Field | Value |
|-------|-------|
| Name | `li_maestro_evaluate` |
| Version | 1.0.3 |
| Author | 北京老李（BeijingLL） |
| Framework | MAESTRO (CSA + OWASP GenAI) |
| Layers | 7+1 (L1-L7 + S0) |
| Phases | 10 (Full Assessment) / 10 Checks (MVTM) |
| Analysis Modes | Full Assessment, MVTM Checklist |
| Template Languages | English, Chinese |
| License | CC BY-NC-SA 4.0 |
| Tags | `threat-modeling`, `maestro`, `ai-security`, `risk-assessment`, `opencode` |

## 🆕 What's New in v1.0.3

**Multi-Language Template System:**
- **English Templates** - Standard MAESTRO templates (~200 fields)
- **Chinese Templates** - With Chinese regulatory extensions (等保、数据出境、生成式AI备案)
- **MVTM Simplified Templates** - Quick assessment templates (~60 fields with auto-inheritance)

**Chinese Regulatory Extensions (6 new fields):**
- 等保级别 (Classification Level)
- 数据出境要求 (Data Export Requirements)
- 重要数据/核心数据 (Important/Core Data)
- 生成式AI服务备案 (Generative AI Filing)
- AI安全风险分类 (AI Risk Classification)
- 合规负责人 (Compliance Officer)

**Auto Field Inheritance (MVTM mode):**
- Automatic field population from previous phases
- Reduces duplication by 60%
- Faster threat modeling workflow

See [CHANGELOG.md](./CHANGELOG.md) for detailed release notes.

## 📁 Output Structure

```
# Full Assessment mode:
threat-models/<project>-<YYYYMMDD-HHMM>/   ← per-run timestamped directory
├── state.json                              # Progress tracking
├── 01-business-context.md                  # Phase 1
├── 02-architecture.md                      # Phase 2
├── 03-threat-actors.md                     # Phase 3
├── 04-trust-boundaries.md                  # Phase 4
├── 05-asset-flows.md                       # Phase 5
├── 06-threat-register.md                   # Phase 6
├── 07-mitigations.md                       # Phase 7
├── 08-code-validation.md                   # Phase 8
├── 09-residual-risk.md                     # Phase 9
├── 10-output-summary.md                    # Phase 10 — full report
├── threat-model.json                       # Machine-readable JSON
├── 11-ai-risk-classification.md            # 《人工智能安全治理框架》2.0 mapping
├── 11-ai-risk-classification.docx          # Word version
├── 11-ai-risk-classification.xlsx          # Excel version
└── 12-skill-risk-assessment.md             # Skill-specific 6-step report

# MVTM mode:
threat-models/<project>-mvtm-<YYYYMMDD-HHMM>/   ← MVTM run directory
├── state.json                                    # Progress tracking
├── 01-mvtm-checklist.md                          # MVTM checklist report
├── threat-model.json                             # Machine-readable JSON
├── 11-ai-risk-classification.md                  # 《人工智能安全治理框架》2.0 mapping
├── 11-ai-risk-classification.docx                # Word version
├── 11-ai-risk-classification.xlsx                # Excel version
└── 12-skill-risk-assessment.md                   # Skill-specific 6-step report
```

## 🔗 Links

- **MAESTRO Playbook:** https://github.com/agentic-threat-modeling/MAESTRO
- **ClawHub Registry:** https://clawhub.ai
- **License:** CC BY-NC-SA 4.0 (non-commercial use only). See SKILL.md for full terms.
