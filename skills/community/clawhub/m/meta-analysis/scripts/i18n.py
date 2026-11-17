#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
i18n.py -- bilingual (EN/ZH) localization for the ct- skill library (shared base layer)

Provides:
  - is_chinese_os(): detect if the OS locale is Chinese
  - t(key, **kwargs): translate a message key to the current locale
  - set_lang(locale): manually override the locale (for testing)

Rules (per ~/.workbuddy/MEMORY.md "双语语言策略"):
  - Default: English
  - Auto-switch to Chinese when OS locale contains zh/CN
  - Code output (R/Python) is NOT affected by language policy

Usage:
  from i18n import t
  print(t("error.rscript_not_found"))
  print(t("info.result_saved", path="/tmp/x.json"))
"""

import os
import sys


# ═══════════════════════════════════════════════════════════════════════════
# Locale detection / 系统语言检测
# ═══════════════════════════════════════════════════════════════════════════

_OVERRIDE_LANG = None


def set_lang(locale_code):
    """Manually override language (for testing). Pass None to reset to auto-detect."""
    global _OVERRIDE_LANG
    _OVERRIDE_LANG = locale_code


def is_chinese_os():
    """Detect if the OS is Chinese (zh-CN, zh-TW, zh-HK, etc.).

    Detection order:
      1. Environment variables: LANGUAGE / LC_ALL / LC_MESSAGES / LANG
      2. Windows API: GetLocaleInfoW + registry (LocaleName)
      3. Python locale module: getdefaultlocale()
    """
    global _OVERRIDE_LANG
    if _OVERRIDE_LANG is not None:
        return _OVERRIDE_LANG == "zh"

    # 1. Check environment variables
    for var in ("LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG"):
        val = os.environ.get(var, "")
        if val.lower().startswith("zh"):
            return True

    # 2. Windows-specific detection
    if sys.platform == "win32":
        try:
            import ctypes
            buf = ctypes.create_unicode_buffer(85)
            ctypes.windll.kernel32.GetLocaleInfoW(0x0400, 0x00000005, buf, 85)
            if buf.value.lower().startswith("zh"):
                return True
        except Exception:
            pass

        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, r"Control Panel\International"
            )
            locale_name = winreg.QueryValueEx(key, "LocaleName")[0]
            winreg.CloseKey(key)
            if locale_name.lower().startswith("zh"):
                return True
        except Exception:
            pass

    # 3. Python locale module fallback
    try:
        import locale
        loc = locale.getdefaultlocale()[0]
        if loc and loc.lower().startswith("zh"):
            return True
    except Exception:
        pass

    return False


def _current_lang():
    """Return 'zh' or 'en'."""
    return "zh" if is_chinese_os() else "en"


# ═══════════════════════════════════════════════════════════════════════════
# Message dictionary / 消息字典
# ═══════════════════════════════════════════════════════════════════════════

_MESSAGES = {
    # ── Generic messages shared by ALL ct- skills / 全库通用消息 ──
    "dry_run.not_executed": {
        "en": "[DRY RUN — code not executed. Remove --dry-run to execute.]",
        "zh": "[DRY RUN — 代码未执行。去掉 --dry-run 以执行。]",
    },
    "safe_preview.not_executed": {
        "en": "[SAFE PREVIEW] R code was NOT executed. Re-run with --yes to compute the result.",
        "zh": "[安全预览] R 代码未执行。追加 --yes 重新运行以计算结果。]",
    },
    "exec.running": {
        "en": "[EXECUTING R CODE...]",
        "zh": "[正在执行 R 代码...]",
    },
    "info.r_code_shown_default": {
        "en": "[INFO] R code is shown by default in preview mode. Re-run with --show-code while using --yes to also display it during execution.",
        "zh": "[提示] 预览模式默认展示 R 代码。执行时追加 --show-code 可同时查看代码。]",
    },
    "info.result_saved": {
        "en": "Result JSON saved to: {path}",
        "zh": "结果 JSON 已保存至：{path}",
    },
    "info.png_saved": {
        "en": "PNG saved to: {path}",
        "zh": "PNG 已保存至：{path}",
    },
    "error.rscript_not_found": {
        "en": "[ERROR] Rscript not found or invalid. Set RSCRIPT_PATH env or install R.",
        "zh": "[错误] 未找到 Rscript 或路径无效。请设置 RSCRIPT_PATH 环境变量或安装 R。",
    },
    "error.invalid_temp_path": {
        "en": "[ERROR] Invalid temp path; execution refused.",
        "zh": "[错误] 临时路径无效；执行已拒绝。]",
    },
    "error.r_timeout": {
        "en": "[ERROR] R execution timed out (300s limit)",
        "zh": "[错误] R 执行超时（300 秒限制）]",
    },
    "error.exec_failed": {
        "en": "[ERROR] Execution failed: {name}",
        "zh": "[错误] 执行失败：{name}",
    },
    "error.invalid_install_path": {
        "en": "[ERROR] Invalid install script path; execution refused.",
        "zh": "[错误] 安装脚本路径无效；执行已拒绝。]",
    },
    "error.rscript_not_found_install": {
        "en": "[ERROR] Rscript not found or invalid. Is R installed?",
        "zh": "[错误] 未找到 Rscript 或路径无效。是否已安装 R？]",
    },
    "error.generic": {
        "en": "ERROR: {msg}",
        "zh": "错误：{msg}",
    },
    "error.val_err": {
        "en": "ERROR: {msg}",
        "zh": "错误：{msg}",
    },
    "validation.failed": {
        "en": "Parameter validation failed:",
        "zh": "参数校验失败：",
    },
    "validation.range_error_gt": {
        "en": "--{label} must be > {bound} (got {val})",
        "zh": "--{label} 必须 > {bound}（当前值 {val}）",
    },
    "validation.range_error_lt": {
        "en": "--{label} must be < {bound} (got {val})",
        "zh": "--{label} 必须 < {bound}（当前值 {val}）",
    },
    "install.cmd_header": {
        "en": "[R package commands — for review only, NOT executed]",
        "zh": "[R 包安装命令 — 仅供审阅，未执行]",
    },
    "install.cran_warning": {
        "en": "This command will download and install {n} R packages from CRAN (the ONLY network operation in this skill).",
        "zh": "此命令会**从 CRAN 联网下载并安装** {n} 个 R 包（即本技能唯一会联网的操作）。",
    },
    "install.confirm_prompt": {
        "en": "If confirmed, re-run with --run-install to actually download:",
        "zh": "如确认无误，请重新运行并追加 --run-install 才会真正联网安装：",
    },
    "install.manual_alt": {
        "en": "Or paste the above command into an R console to install manually.",
        "zh": "或在 R 控制台中手动粘贴上述命令自行安装。",
    },
    "install.network_warning_en": {
        "en": "⚠️  NETWORK INSTALL: the following R code will download packages from CRAN",
        "zh": "⚠️  联网安装：以下 R 代码将从 CRAN 下载并安装 R 包（供应链风险由你知情触发）",
    },
    "install.code_header": {
        "en": "[R CODE — will be executed by Rscript]",
        "zh": "[R 代码 — 将由 Rscript 执行]",
    },
    "header.r_code": {
        "en": "[R CODE — generated for this analysis]",
        "zh": "[R 代码 — 本次分析生成]",
    },
    "header.install_cmd": {
        "en": "[R package commands — for review only, NOT executed]",
        "zh": "[R 包安装命令 — 仅供审阅，未执行]",
    },

    # ── Excel report (ct-registry export_xlsx.py) / Excel 报告专用键 ──
    # NOTE: these are FRAME labels only. Raw data values (e.g. CDE Chinese
    # status "进行中", Chinese conditions) are NEVER translated — data fidelity.
    # / 仅界面框架标签。原始数据值（如 CDE 中文状态、中文适应症）一律不翻译，保持数据保真。
    "xlsx.sheet.readme":   {"en": "README",                 "zh": "说明"},
    "xlsx.sheet.summary":  {"en": "Search Results Summary", "zh": "检索结果概要"},
    "xlsx.sheet.master":   {"en": "Trial Master Table",     "zh": "试验总表"},
    "xlsx.sheet.raw":      {"en": "Raw Details",            "zh": "原始明细"},

    "xlsx.banner.title":   {"en": "Clinical Trial Search Report",
                            "zh": "临床试验检索报告"},
    "xlsx.banner.summary": {"en": "Clinical Trial Search Results Summary",
                            "zh": "临床试验检索结果概要"},
    "xlsx.banner.master":  {"en": "Clinical Trial Master Table",
                            "zh": "临床试验明细总表"},
    "xlsx.banner.raw":     {"en": "Raw Details (normalized field snapshot)",
                            "zh": "原始明细（归一化字段快照）"},

    "xlsx.cover.topic":     {"en": "Search topic: ",
                             "zh": "检索主题："},
    "xlsx.cover.generated": {"en": "This workbook was auto-generated by ct-registry; a single file, readable offline.",
                             "zh": "本工作簿由 ct-registry 自动生成，单文件离线可读。"},

    "xlsx.kpi.total":    {"en": "Total Trials",        "zh": "总试验数"},
    "xlsx.kpi.total_sub":{"en": "selected projects",   "zh": "条入选项目"},
    "xlsx.kpi.who":      {"en": "WHO ICTRP",           "zh": "WHO ICTRP"},
    "xlsx.kpi.who_sub":  {"en": "global mirror registry", "zh": "全球镜像库"},
    "xlsx.kpi.cde":      {"en": "China CDE",           "zh": "中国 CDE"},
    "xlsx.kpi.cde_sub":  {"en": "official drug registry", "zh": "官方药品库"},
    "xlsx.kpi.span":     {"en": "Registration Year Span", "zh": "注册年份跨度"},
    "xlsx.kpi.span_sub": {"en": "first public listing year", "zh": "首次公示年份"},

    "xlsx.readme.scope_title": {"en": "Search Overview", "zh": "检索概览"},
    "xlsx.scope.topic":   {"en": "Search topic", "zh": "检索主题"},
    "xlsx.scope.range":   {"en": "Search scope", "zh": "检索范围"},
    "xlsx.scope.range_val": {"en": "WHO ICTRP (global mirror of 14+ primary registries) + China CDE",
                             "zh": "WHO ICTRP（全球镜像 14+ 一级注册库）+ 中国 CDE"},
    "xlsx.scope.source":  {"en": "Data source", "zh": "数据来源"},
    "xlsx.scope.source_val": {"en": "WHO ICTRP detail API (via unified endpoint); CDE drug trial registry platform",
                              "zh": "WHO ICTRP 详情接口（经统一端点）；CDE 药物临床试验登记平台"},
    "xlsx.scope.quota":   {"en": "Quota note", "zh": "配额说明"},
    "xlsx.scope.quota_val": {"en": "Free to use; to conserve shared resources, the daily cap is 10 demands (counted by demand_id). See README.",
                             "zh": "当前免费使用；为充分利用共享资源，每日上限 10 个需求（按 demand_id 计），详见 README"},

    "xlsx.readme.field_title": {"en": "Field Dictionary", "zh": "字段说明"},
    "xlsx.field.col":          {"en": "Field",   "zh": "字段"},
    "xlsx.field.meaning":      {"en": "Meaning", "zh": "含义"},
    "xlsx.field.registry_id":  {"en": "Registry ID", "zh": "登记号"},
    "xlsx.field.registry_id_desc": {"en": "Unique ID per registry (NCT / ChiCTR / DRKS / CTIS / jRCT / ACTRN, etc.)",
                                    "zh": "各注册库唯一编号（NCT / ChiCTR / DRKS / CTIS / jRCT / ACTRN 等）"},
    "xlsx.field.source":       {"en": "Source", "zh": "数据来源"},
    "xlsx.field.conditions":   {"en": "Conditions", "zh": "适应症"},
    "xlsx.field.conditions_desc": {"en": "Health condition(s)",
                                   "zh": "Health condition(s) / 健康状况"},
    "xlsx.field.study_type":   {"en": "Study Type", "zh": "研究类型"},
    "xlsx.field.study_type_desc": {"en": "Study type (Observational / Interventional, etc.)",
                                   "zh": "Study type（Observational / Interventional 等）"},
    "xlsx.field.phase":        {"en": "Phase", "zh": "分期"},
    "xlsx.field.phase_desc":   {"en": "Phase (some observational studies have no phase)",
                                "zh": "Phase（部分观察性研究无分期）"},
    "xlsx.field.enrollment":   {"en": "Enrollment", "zh": "样本量"},
    "xlsx.field.enrollment_desc": {"en": "Target sample size / actual total enrolled",
                                   "zh": "Target sample size / 实际入组总人数"},
    "xlsx.field.status":       {"en": "Status", "zh": "状态"},
    "xlsx.field.status_desc":  {"en": "Recruitment status (Recruiting / Completed, etc.; colour-coded in the master table)",
                                "zh": "Recruitment status（招募中 / 已完成 等，颜色编码见总表）"},
    "xlsx.field.sponsor":      {"en": "Sponsor", "zh": "申办方"},
    "xlsx.field.sponsor_desc": {"en": "Primary sponsor / applicant name",
                                "zh": "Primary sponsor / 申请人名称"},
    "xlsx.field.countries":    {"en": "Countries", "zh": "国家"},
    "xlsx.field.countries_desc": {"en": "Countries of recruitment (CDE is always China)",
                                  "zh": "Countries of recruitment（CDE 恒为 China）"},
    "xlsx.field.start_date":   {"en": "Registration Date", "zh": "注册日期"},
    "xlsx.field.start_date_desc": {"en": "Date of registration / first public listing",
                                   "zh": "Date of registration / 首次公示信息日期"},
    "xlsx.field.primary_outcome": {"en": "Primary Outcome", "zh": "主要终点"},
    "xlsx.field.primary_outcome_desc": {"en": "Primary Outcome(s)", "zh": "Primary Outcome(s)"},
    "xlsx.field.title":        {"en": "Title", "zh": "标题"},
    "xlsx.field.url":          {"en": "Homepage", "zh": "首页链接"},
    "xlsx.field.url_desc":     {"en": "Click to open each registry's official page (blue underline)",
                                "zh": "点击直达各注册库官方页面（蓝色下划线）"},
    "xlsx.field.interventions":   {"en": "Interventions", "zh": "干预措施"},
    "xlsx.field.secondary_outcome": {"en": "Secondary Outcome", "zh": "次要终点"},
    "xlsx.field.inclusion":     {"en": "Inclusion Criteria", "zh": "入选标准"},
    "xlsx.field.exclusion":     {"en": "Exclusion Criteria", "zh": "排除标准"},
    "xlsx.field.comparator":    {"en": "Comparator", "zh": "对照药"},
    "xlsx.field.age_min":       {"en": "Min Age", "zh": "最小年龄"},
    "xlsx.field.age_max":       {"en": "Max Age", "zh": "最大年龄"},
    "xlsx.field.gender":        {"en": "Gender", "zh": "性别"},

    "xlsx.col.count":        {"en": "Count",  "zh": "试验数"},
    "xlsx.col.share":        {"en": "Share",  "zh": "占比"},
    "xlsx.col.metric":       {"en": "Metric", "zh": "指标"},
    "xlsx.col.value":        {"en": "Value",  "zh": "数值"},
    "xlsx.col.enroll_band":  {"en": "Enrollment Band", "zh": "样本量区间"},
    "xlsx.col.category":     {"en": "Category", "zh": "分类"},
    "xlsx.total":            {"en": "Total", "zh": "合计"},
    "xlsx.unknown":          {"en": "(unknown)", "zh": "(未知)"},
    "xlsx.no_data":          {"en": "(no data)", "zh": "(无数据)"},

    "xlsx.block.phase":        {"en": "1. Phase Distribution", "zh": "一、分期分布"},
    "xlsx.block.status":       {"en": "2. Recruitment Status", "zh": "二、招募状态分布"},
    "xlsx.block.source":       {"en": "3. Data Source", "zh": "三、数据来源分布"},
    "xlsx.block.ind":          {"en": "4. Conditions (Top 12)", "zh": "四、适应症分布 (Top 12)"},
    "xlsx.block.countries":    {"en": "5. Recruitment Countries/Regions (Top 12)", "zh": "五、招募国家/地区分布 (Top 12)"},
    "xlsx.block.timeline":     {"en": "6. Registration Trend by Year", "zh": "六、逐年注册趋势"},
    "xlsx.block.sponsor":      {"en": "7. Sponsors (Top 15)", "zh": "七、申办方分布 (Top 15)"},
    "xlsx.block.enrollment":   {"en": "8. Enrollment Summary", "zh": "八、样本量汇总"},
    "xlsx.block.phase_status": {"en": "9. Phase × Status Cross-tab", "zh": "九、分期 × 状态 交叉分布"},

    "xlsx.label.phase":        {"en": "Phase", "zh": "分期"},
    "xlsx.label.status":       {"en": "Status", "zh": "状态"},
    "xlsx.label.source":       {"en": "Data Source", "zh": "数据来源"},
    "xlsx.label.ind":          {"en": "Conditions", "zh": "适应症"},
    "xlsx.label.countries":    {"en": "Countries/Regions", "zh": "国家/地区"},
    "xlsx.label.timeline":     {"en": "Registration Year", "zh": "注册年份"},
    "xlsx.label.sponsor":      {"en": "Sponsor", "zh": "申办方"},
    "xlsx.label.enrollment":   {"en": "Enrollment", "zh": "样本量"},
    "xlsx.label.phase_status": {"en": "Phase＼Status", "zh": "分期＼状态"},

    "xlsx.note.status_color": {"en": "Colour matches the master-table status coding",
                               "zh": "颜色与总表状态编码一致"},
    "xlsx.note.source":       {"en": "WHO ICTRP (global mirror) vs China CDE",
                               "zh": "WHO ICTRP（全球镜像）vs 中国 CDE"},
    "xlsx.note.top12":        {"en": "Top 12 only", "zh": "仅显示前 12 位"},
    "xlsx.note.top12_cde":    {"en": "Top 12 only; CDE is always China",
                               "zh": "仅显示前 12 位；CDE 恒为 China"},
    "xlsx.note.top15":        {"en": "Top 15 only", "zh": "仅显示前 15 位"},
    "xlsx.note.enroll":       {"en": "Target / actual enrollment statistics",
                               "zh": "目标/实际入组人数统计"},
    "xlsx.note.crosstab":     {"en": "Row totals in the last column; the colour scale shows counts",
                               "zh": "每行合计见末列；色阶表示数量"},

    "xlsx.stat.n":      {"en": "Trials with data", "zh": "有数据试验数"},
    "xlsx.stat.total":  {"en": "Total enrollment", "zh": "总样本量"},
    "xlsx.stat.median": {"en": "Median enrollment", "zh": "中位样本量"},
    "xlsx.stat.mean":   {"en": "Mean enrollment", "zh": "平均样本量"},
    "xlsx.stat.min":    {"en": "Min enrollment", "zh": "最小样本量"},
    "xlsx.stat.max":    {"en": "Max enrollment", "zh": "最大样本量"},

    "xlsx.chart.enroll_hist": {"en": "Enrollment Band Distribution",
                               "zh": "样本量区间分布"},

    "xlsx.doc.title": {"en": "Clinical Trial Search Results", "zh": "临床试验检索结果"},
    "xlsx.footer":    {"en": "Page &P of &N · Generated &D",
                       "zh": "第 &P 页 / 共 &N 页 · 生成于 &D"},

    "xlsx.summary.intro": {
        "en": ("The tables and charts below are auto-aggregated from the search results: "
               "each section shows a distribution table on the left and its chart on the right; "
               "the share column carries a data bar, so distributions and trends are grasped "
               "at a glance. Extended dimensions include data source, country/region, "
               "enrollment and phase×status."),
        "zh": ("下列数据表与图表由检索结果自动汇总生成：每个分区左侧为分布数据表、"
               "右侧为对应统计图；占比列带数据条，便于一眼掌握分布与趋势。"
               "含「数据来源 / 国家地区 / 样本量 / 分期×状态」等扩展维度。"),
    },
    "xlsx.caveat.text": {
        "en": ("Data caveats: ① If a CDE search returns empty in both Chinese and English, it means the drug "
               "has no China drug registration; ② some WHO records lack study type / phase — a source-coverage "
               "issue; ③ primary/secondary outcomes and inclusion/exclusion criteria are preserved verbatim, "
               "not translated; ④ the WHO advanced-search Phases field is narrow, so phase is verified against "
               "the normalized detail."),
        "zh": ("数据局限：① CDE 经中英双检索为空时表示该药暂无中国药物登记；"
               "② 部分 WHO 记录缺研究类型/分期的，属源数据覆盖问题；"
               "③ 主要/次要终点与入排标准原文保留，未做翻译；"
               "④ WHO 高级检索 Phases 归一化字段较窄，分期以详情归一化复核为准。"),
    },

    # ── status colour legend (README) / 状态色图例 ──
    "xlsx.legend.title":       {"en": "Status Colour Legend", "zh": "状态颜色图例"},
    "xlsx.legend.notyet":      {"en": "Not yet recruiting", "zh": "尚未招募"},
    "xlsx.legend.recruiting":  {"en": "Recruiting", "zh": "招募中"},
    "xlsx.legend.inprogress":  {"en": "Ongoing / In progress", "zh": "进行中"},
    "xlsx.legend.completed":   {"en": "Completed", "zh": "已完成"},
    "xlsx.legend.stopped":     {"en": "Withdrawn / Terminated / Suspended", "zh": "撤回 / 终止 / 暂停"},
    "xlsx.legend.unknown":     {"en": "Unknown / Pending", "zh": "未知 / 待定"},
    # ── FAERS / drug-safety Excel (ct-safety export_xlsx.py) / 药物安全 Excel 专用键 ──
    # SAME rule as ct-registry: raw DATA VALUES (reaction PTs, country codes, drug
    # names, indication text) are NEVER translated; only UI frame labels + code→label
    # mappings for FAERS enum fields (sex / serious / reporttype / drug role).
    # / 与 ct-registry 同规则：原始数据值（反应 PT、国家代码、药名、指征文本）一律不翻译；
    # 仅界面框架标签 + FAERS 枚举字段（性别/严重性/报告类型/药物角色）的 编码→标签 映射。
    "xlsx.safety.doc_title":      {"en": "FAERS Adverse Event Report", "zh": "FAERS 不良事件报告"},
    "xlsx.safety.banner":         {"en": "FAERS Adverse Event Search Report",
                                   "zh": "FAERS 不良事件检索报告"},
    "xlsx.safety.cover.generated": {
        "en": "Auto-generated by ct-safety from openFDA FAERS public data (drug/event.json). Single file, readable offline.",
        "zh": "由 ct-safety 基于 openFDA FAERS 公开数据（drug/event.json）自动生成，单文件离线可读。"},
    "xlsx.safety.watermark": {
        "en": "ct-safety", "zh": "ct-safety"},
    "xlsx.safety.scope.source":     {"en": "Data source", "zh": "数据来源"},
    "xlsx.safety.scope.source_val": {
        "en": "openFDA FAERS (FDA Adverse Event Reporting System) public API",
        "zh": "openFDA FAERS（FDA 不良事件报告系统）公开 API"},
    "xlsx.safety.scope.drug":      {"en": "Drug / medicinal product", "zh": "药物 / 药品"},
    "xlsx.safety.scope.field":     {"en": "Search field", "zh": "检索字段"},
    "xlsx.safety.scope.date":      {"en": "Date filter (receivedate)", "zh": "日期筛选（报告接收日）"},
    "xlsx.safety.scope.total":     {"en": "Total matching reports", "zh": "匹配报告总数"},
    "xlsx.safety.scope.downloaded": {"en": "Downloaded (first N)", "zh": "已下载（API 返回顺序前 N 条）"},
    "xlsx.safety.scope.downloaded_fast": {
        "en": "count mode — full matched population (no case download)",
        "zh": "count 模式 — 全量匹配报告（未下载逐条个案）"},
    "xlsx.safety.scope.mode":      {"en": "Mode", "zh": "分析模式"},
    "xlsx.safety.mode_fast":       {
        "en": "count-facet fast fetch (full matched population, seconds)",
        "zh": "count 分面快取（全量匹配报告，秒级生成）"},

    "xlsx.safety.scope.cap":       {"en": "Hard cap", "zh": "硬上限"},
    "xlsx.safety.caveat": {
        "en": ("Data caveats: ① Reports are the FIRST N in API return order — NOT a random sample; "
               "do not treat proportions as population estimates. ② FAERS is spontaneous reporting, "
               "subject to under-reporting and confounding. ③ Age uses mixed units (YR/MON/WK/DY/HR); "
               "normalized to years before binning. ④ Reaction / indication / drug-role text is split "
               "from semicolon-joined fields and counted verbatim."),
        "zh": ("数据局限：① 下载为 API 返回顺序前 N 条，非随机抽样，比例不可当作总体估计；"
               "② FAERS 为自发呈报，存在漏报与混杂偏倚；③ 年龄单位混杂（年/月/周/天/时），"
               "分箱前已统一折算为岁；④ 反应/指征/药物角色由分号拼接字段拆分后原文计数。")},

    "xlsx.safety.kpi.downloaded":     {"en": "Downloaded", "zh": "已下载"},
    "xlsx.safety.kpi.downloaded_sub": {"en": "reports (cap 10000)", "zh": "条（上限10000）"},
    "xlsx.safety.kpi.total":          {"en": "Total Matching", "zh": "匹配总数"},
    "xlsx.safety.kpi.total_sub":      {"en": "in FAERS", "zh": "条（全库）"},
    "xlsx.safety.kpi.serious":        {"en": "Serious", "zh": "严重报告"},
    "xlsx.safety.kpi.serious_sub":    {"en": "count", "zh": "条"},
    "xlsx.safety.kpi.serious_rate":   {"en": "Serious Rate", "zh": "严重率"},
    "xlsx.safety.kpi.serious_rate_sub": {"en": "serious / total", "zh": "严重/总计"},
    "xlsx.safety.kpi.male":           {"en": "Male", "zh": "男性"},
    "xlsx.safety.kpi.female":         {"en": "Female", "zh": "女性"},
    "xlsx.safety.kpi.median_age":     {"en": "Median Age", "zh": "中位年龄"},
    "xlsx.safety.kpi.median_age_sub": {"en": "years (normalized)", "zh": "岁（已折算）"},
    "xlsx.safety.kpi.year_span":      {"en": "Report Year Span", "zh": "报告年份跨度"},
    "xlsx.safety.kpi.year_span_sub":  {"en": "first – last", "zh": "首 – 末"},
    "xlsx.safety.kpi.population":     {"en": "Analyzed Population", "zh": "分析基数"},
    "xlsx.safety.kpi.population_sub": {"en": "all matching reports (count)", "zh": "全部匹配报告（count）"},

    "xlsx.safety.block.serious":    {"en": "1. Seriousness", "zh": "一、严重性分布"},
    "xlsx.safety.block.sex":        {"en": "2. Sex", "zh": "二、性别分布"},
    "xlsx.safety.block.report_type": {"en": "3. Report Type", "zh": "三、报告类型"},
    "xlsx.safety.block.country":    {"en": "4. Primary Source Country (Top 12)", "zh": "四、报告来源国家 (Top 12)"},
    "xlsx.safety.block.age":        {"en": "5. Age Distribution", "zh": "五、年龄分布"},
    "xlsx.safety.block.year":       {"en": "6. Annual Reporting Trend", "zh": "六、逐年报告趋势"},
    "xlsx.safety.block.reaction":   {"en": "7. Top Reaction Terms (Top 15)", "zh": "七、高频反应事件 (Top 15)"},
    "xlsx.safety.block.indication": {"en": "8. Top Indications (Top 12)", "zh": "八、高频用药指征 (Top 12)"},
    "xlsx.safety.block.drug_role":  {"en": "9. Drug Role", "zh": "九、药物角色分布"},

    "xlsx.safety.label.serious":    {"en": "Seriousness", "zh": "严重性"},
    "xlsx.safety.label.sex":        {"en": "Sex", "zh": "性别"},
    "xlsx.safety.label.report_type": {"en": "Report Type", "zh": "报告类型"},
    "xlsx.safety.label.country":    {"en": "Country", "zh": "国家"},
    "xlsx.safety.label.age":        {"en": "Age Band (years)", "zh": "年龄段（岁）"},
    "xlsx.safety.label.year":       {"en": "Report Year", "zh": "报告年份"},
    "xlsx.safety.label.reaction":   {"en": "Reaction (PT)", "zh": "反应事件 (PT)"},
    "xlsx.safety.label.indication": {"en": "Indication", "zh": "用药指征"},
    "xlsx.safety.label.drug_role":  {"en": "Drug Role", "zh": "药物角色"},

    # FAERS enum code → label mappings (codes are language-neutral, never translated)
    "xlsx.safety.serious_yes":   {"en": "Serious", "zh": "严重"},
    "xlsx.safety.serious_no":    {"en": "Non-serious", "zh": "非严重"},
    "xlsx.safety.sex_m":         {"en": "Male", "zh": "男性"},
    "xlsx.safety.sex_f":         {"en": "Female", "zh": "女性"},
    "xlsx.safety.sex_unknown":   {"en": "Unknown", "zh": "未知"},
    "xlsx.safety.rt_initial":    {"en": "Initial", "zh": "初始报告"},
    "xlsx.safety.rt_followup":   {"en": "Follow-up", "zh": "随访报告"},
    "xlsx.safety.rt_unknown":    {"en": "Unknown", "zh": "未知"},
    "xlsx.safety.role_suspect":    {"en": "Suspect drug", "zh": "怀疑药"},
    "xlsx.safety.role_concomitant": {"en": "Concomitant", "zh": "合并用药"},
    "xlsx.safety.role_interaction": {"en": "Interaction", "zh": "相互作用"},

    "xlsx.safety.note.top12":  {"en": "Top 12 only", "zh": "仅显示前 12 位"},
    "xlsx.safety.note.top15":  {"en": "Top 15 only", "zh": "仅显示前 15 位"},
    "xlsx.safety.note.age":    {"en": "Age normalized to years before binning", "zh": "分箱前年龄已折算为岁"},
    "xlsx.safety.note.year":   {"en": "By report receivedate year", "zh": "按报告接收年份"},
    "xlsx.safety.note.role":   {"en": "All drug roles across the report", "zh": "报告内全部药物角色计数"},
    "xlsx.safety.note.age_skip_fast": {
        "en": "Age distribution is NOT count-able via the API (404) → omitted; use non-fast mode to download cases.",
        "zh": "年龄分布无法经 API 分面统计（404）→ 此处略；如需年龄请用非 --fast 模式下载个案。"},
    "xlsx.safety.raw_fast_note": {
        "en": "Count fast mode did not download case-level records. Use non --fast mode to fetch raw cases.",
        "zh": "count 快取模式未下载逐条个案；如需原始个案请用非 --fast 模式下载。"},

    "xlsx.safety.col.count":    {"en": "Reports", "zh": "报告数"},
    "xlsx.safety.summary_intro": {
        "en": ("The tables and charts below are auto-aggregated from the downloaded FAERS cases: "
               "each section shows a distribution table on the left and its chart on the right; the "
               "share column carries a data bar. Nine dimensions cover seriousness, sex, report type, "
               "source country, age, annual trend, top reactions, top indications and drug role."),
        "zh": ("下列数据表与图表由下载的 FAERS 个案自动汇总生成：每个分区左侧为分布数据表、"
               "右侧为对应统计图；占比列带数据条。涵盖严重性、性别、报告类型、来源国家、年龄、"
               "逐年趋势、高频反应、高频指征与药物角色九个维度。")},
    "xlsx.safety.summary_intro_fast": {
        "en": ("The dimensions below are aggregated from openFDA count facets over the FULL matched "
               "population (generated in seconds, no selection bias). Age is NOT count-able via the "
               "API, so the age block is omitted — eight dimensions are shown."),
        "zh": ("以下维度基于 openFDA count 分面对「全部匹配报告」聚合生成（秒级、无选择偏倚）。"
               "年龄无法经 API 分面统计，故略去年龄块；共展示八个维度。")},
}


def t(key, **kwargs):
    """Translate a message key to the current locale.

    Args:
        key: message identifier in _MESSAGES
        **kwargs: format placeholders (e.g., path="/tmp/x.json")

    Returns:
        Localized string. Falls back to the key itself if not found.
    """
    lang = _current_lang()
    entry = _MESSAGES.get(key)
    if entry is None:
        return key
    text = entry.get(lang, entry.get("en", key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text
    return text


# Back-compatible alias
_ = t

_MESSAGES.update({
    "kw_gate.empty": {"en": "[ct_registry][KW-SYSTEM] No expandable keywords.", "zh": "[ct_registry][KW-SYSTEM] 无可扩展的关键字。"},
    "kw_gate.title": {"en": "Keyword system (auto-expand + EN/ZH translation) - confirm / supplement before searching", "zh": "关键字体系（自动扩展 + 中英互译）- 请确认 / 补充后再检索"},
    "kw_gate.original": {"en": "Original: {base}  |  Intent: {intent}", "zh": "原文：{base}  ｜  意图：{intent}"},
    "kw_gate.zh": {"en": "Chinese candidates", "zh": "中文候选"},
    "kw_gate.en": {"en": "English candidates", "zh": "英文候选"},
    "kw_gate.per_source": {"en": "Per-source assignment", "zh": "按源分配"},
    "kw_gate.ctgov": {"en": "CT.gov + WHO (English exact)", "zh": "CT.gov + WHO（英文·精确）"},
})

_MESSAGES.update({
    "kw_gate.cde": {"en": "CDE + ChiCTR (Chinese substring)", "zh": "CDE + ChiCTR（中文·子串）"},
    "kw_gate.risk": {"en": "Risk note:", "zh": "风险提示："},
    "kw_gate.speculative": {"en": "Speculative terms (review / removable):", "zh": "推测词（建议留意/可删）："},
    "kw_gate.confirm": {"en": "Please confirm:", "zh": "请确认："},
    "kw_gate.opt_adopt": {"en": "1. Adopt the above keyword system (recommended)", "zh": "1. 采用以上关键字体系（推荐）"},
    "kw_gate.opt_del": {"en": "2. Delete specific terms (reply: del term, e.g. del sitagliptin)", "zh": "2. 删除某些词（回复：删 词，如删 曲格列汀）"},
    "kw_gate.opt_add": {"en": "3. Add your own terms (reply: add term, e.g. add repaglinide)", "zh": "3. 补充我自己的词（回复：加 词，如加 瑞格列奈）"},
})

_MESSAGES.update({
    "kw_gate.opt_scope": {"en": "4. Narrow / widen scope (e.g. only saxagliptin)", "zh": "4. 改用更窄 / 更宽范围（如只搜 沙格列汀）"},
    "kw_gate.opt_cancel": {"en": "0. Cancel", "zh": "0. 取消"},
    "kw_gate.after": {"en": "(Search proceeds to scope/quota confirmation only after you confirm)", "zh": "（确认后才进入检索范围/配额确认 - 正式检索）"},
    "kw_gate.axis_condition": {"en": "Condition", "zh": "疾病/适应症"},
    "kw_gate.axis_intervention": {"en": "Intervention/Drug", "zh": "干预/药物"},
    "kw_gate.title_multi": {"en": "Keyword system #{i} ({axis}) - auto-expand + EN/ZH translation", "zh": "关键字体系 #{i}（{axis}）- 自动扩展 + 中英互译"},
    "kw_gate.multi_confirm": {"en": "Please confirm (the {n} keyword systems above are handled together):", "zh": "请确认（以上 {n} 组关键字体系一并处理）："},
    "kw_gate.stopped": {"en": "[ct_registry][KW-GATE] keyword system not confirmed - search stopped. confirm/supplement, then re-run.", "zh": "[ct_registry][KW-GATE] 关键字体系未确认 - 已停止检索。请确认/补充后，重新运行。"},
})

_MESSAGES.update({
    "kw_gate.none": {"en": "none", "zh": "无"},
    "kw_gate.multi_opt_adopt": {"en": "1. Adopt all the above keyword systems (recommended)", "zh": "1. 全部采用（推荐）"},
    "kw_gate.intent_disease": {"en": "Disease/Condition", "zh": "疾病/适应症"},
    "kw_gate.intent_intervention": {"en": "Intervention/Mechanism", "zh": "干预/机制"},
    "kw_gate.intent_drug": {"en": "Drug (specific)", "zh": "药物(具体)"},
    "kw_gate.intent_drug_class": {"en": "Drug class", "zh": "药物类别"},
    "kw_gate.intent_auto": {"en": "Auto-detect", "zh": "自动识别"},
})
