#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
adapters/coze_error_analyze.py — coze 返回 error 时的「针对性诊断」

目标（用户 2026-09-13 诉求 2）：
  coze 返回 HTTP 200 + {status:"error", notes:"..."}（非成功！对齐
  LRN-20260817-002：网关 200 ≠ 任务成功）。本模块把 notes / warnings / task
  映射成**结构化的、可操作的问题定位与修正指导**，而不是把原始报错甩给用户。

判定口径：
  - 只看响应体 status 字段（不是 HTTP 码）；status!="error" 时返回 None。
  - 先按已知错误签名（正则，大小写不敏感）匹配；都不中 → 通用兜底
    （回显原始 notes + 建议走 build_request 重装）。

公开 API：
  analyze_coze_error(resp) -> ErrorAnalysis | None
      ErrorAnalysis.code        主匹配签名 code
      ErrorAnalysis.summary     一句话问题定性
      ErrorAnalysis.causes      [str] 可能原因
      ErrorAnalysis.fixes       [{"action","detail"}] 针对性修正动作
      ErrorAnalysis.raw_notes   coze 原始 notes（保留溯源）
  render_error_analysis(ea) -> str   渲染成多行文本（给 agent / CLI 转述）
"""
from __future__ import annotations

import re

# 每个签名：(regex 模式, code, summary, [causes], [fixes])
# 顺序即匹配优先级（更具体的放前面）。
_SIGNATURES = [
    (
        r"data\.rows is empty|data\.rows 为空",
        "COZE_E01_ROWS_EMPTY",
        "coze 收到信封后 data.rows 为空（source=inline 必须有 data.rows 数组）。",
        [
            "最常见：把效应量写成了并行顶层数组 data.yi/sei/slab，而不是 data.rows 行对象数组。",
            "或 data 给了 {'rows': []} / 缺 rows / source 不是 inline。",
        ],
        [
            {"action": "重组为 data.rows",
             "detail": "每行写成一个对象：{te, sete, study}（已算效应量）或 "
                       "{event_exp,n_exp,event_ctrl,n_ctrl,study}（2×2）。不要并列顶层数组。"},
            {"action": "走 build_request 重装",
             "detail": "把数据写成 csv/json 行数组，用 scripts/run_meta.py --query ... --data ... 自动装配合规信封。"},
            {"action": "用本地校验器预检",
             "detail": "出站前 adapters/coze_contract_validate.validate_request 会自动修复此类信封并拦截其余不合规项。"},
        ],
    ),
    (
        r"missing effect-size se|缺少效应量标准误|provide sete column or ci_low/ci_high",
        "COZE_E02_NO_SE",
        "has_te 分支缺效应量标准误（sete 或 ci_low/ci_high）。",
        [
            "给了 te 但没给 sete；也没给 ci_low/ci_high 供反推 SE。",
        ],
        [
            {"action": "补 sete 列",
             "detail": "每个研究加一列标准误 seTE（与 te 同尺度，log 尺度给 log SE）。"},
            {"action": "或给 CI 列",
             "detail": "给 ci_low / ci_high（与 te 同尺度），coze 会按 SE=(ci_high-ci_low)/(2·1.96) 反推。"},
        ],
    ),
    (
        r"missing column|缺少列|role=",
        "COZE_E03_MISSING_COLUMN",
        "某逻辑角色（列）在数据中找不到。",
        [
            "colmap 指定了不存在的列名，或数据缺该列。",
            "常见：亚组列 / 协变量列名拼错，或 2×2 四列不全。",
        ],
        [
            {"action": "核对列名",
             "detail": "对照报错里的 role 与可用列名（报错会列出 available columns），修正 colmap 或数据。"},
            {"action": "走 build_request 自动匹配",
             "detail": "列名别名表能识别中英文同义列名；仅剩解析不出的才需 --colmap 兜底。"},
        ],
    ),
    (
        r"功能需要 R 包|需要 R 包|package .* not installed|library\(|could not find function|there is no package",
        "COZE_E04_MISSING_PACKAGE",
        "coze 服务端缺所需 R 包（环境限制）。",
        [
            "该 task 依赖 coze 容器未预装的包（如 gemtc/JAGS 已被移除）。",
            "bayesian_nma 已知环境限制（容器无 root 无法装 JAGS）。",
        ],
        [
            {"action": "换等价 task",
             "detail": "bayesian_nma → 改用 nma（netmeta 频率学）；其余缺失包联系技能维护者在 coze 端补装。"},
            {"action": "核对 coze 依赖清单",
             "detail": "见 coze_contract.md §6（核心 14 包 + 可选 2 包）。"},
        ],
    ),
    (
        r"no comparable studies|未找到可构成对比|each study needs|≥2 arms|>=2 arm",
        "COZE_E05_NMA_ARMS",
        "NMA：没有可构成对比的研究（每个 study 需 ≥2 个 arm）。",
        [
            "arm-based 输入里每个 study 只有 1 个 arm，无法成对比较。",
            "或 treat1/treat2 标识列没解析出来，所有行被当成单臂。",
        ],
        [
            {"action": "检查 arm 标识",
             "detail": "NMA 对比格式需 treat1/treat2（或 treatment）且每个 study 至少 2 行不同 arm。"},
            {"action": "换数据形态",
             "detail": "若本就是 pairwise 数据（每研究一个对比），用 pairwise_meta 而非 nma。"},
        ],
    ),
    (
        r"object ['\"]?TE['\"]? not found|object ['\"]?seTE['\"]? not found|'TE' not found",
        "COZE_E06_NMA_TE",
        "NMA：对比分支没拿到 TE/seTE（列名未归一）。",
        [
            "对比连续格式给了 te/sete 但列名拼写/大小写未被识别。",
            "或 arm 连续格式 treatment/te/sete 缺失。",
        ],
        [
            {"action": "对齐 NMA 列名",
             "detail": "对比连续：treat1/treat2 + te/sete；arm 连续：treatment + te/sete（别名见 build_request.NMA_FORMATS）。"},
        ],
    ),
    (
        r"unknown_task|unknown task|未知任务|task .* not (found|registered)",
        "COZE_E07_UNKNOWN_TASK",
        "task 不在 coze 任务枚举中。",
        [
            "拼写错误，或用了未实现的 task 名。",
        ],
        [
            {"action": "改用合法 task",
             "detail": "见 coze_contract.md §3（pairwise_meta / nma / subgroup_analysis / metareg …）。"},
        ],
    ),
    (
        r"non-numeric argument to binary operator",
        "COZE_E16_NON_NUMERIC_OP",
        "NMA / 数值列混入非数值，二元运算（如 +/-/*）失败。",
        [
            "效应量 / 样本量 / arm 标识列里有文本、空串或 NA。",
            "NMA 对比格式里 treat1/treat2 或 te/sete 含脏数据。",
        ],
        [
            {"action": "清洗数值列",
             "detail": "确保 te/sete/事件数/样本量全为数值且无空值；NMA 检查 treat1/treat2 与 te/sete 列。"},
            {"action": "删 NA 行",
             "detail": "含非数值的研究整行删除或补全后重试。"},
        ],
    ),
    (
        r"argument is of length zero|non-numeric|na/nan|cannot (coerce|open)",
        "COZE_E08_DATA_VALUE",
        "数据值异常（非数值 / 缺失 / NA 导致 R 计算中断）。",
        [
            "某数值列混入了空字符串 / 文本 / NA。",
            "2×2 四格表出现非整数或缺失。",
        ],
        [
            {"action": "清洗数据",
             "detail": "确保事件数 / 样本量 / 效应量 / SE 全为数值且无空值；缺失研究整行删除或补全。"},
        ],
    ),
    (
        r"Argument 'sm' must be",
        "COZE_E09_SM_INVALID",
        "params.sm 与数据类型不匹配（summary measure 选错）。",
        [
            "二分类数据用了连续型 sm（MD/SMD/ROM），或反之。",
            "单组率数据用了 OR/RR 等，或用了连续型 sm。",
        ],
        [
            {"action": "按数据类型选 sm",
             "detail": "二分类(事件/样本量)→ OR/RR/RD；连续型(mean/sd/n)→ MD/SMD/ROM；"
                       "单组率→ PLOGIT/PRAW/MRAW；单组均值→ MD。详见 coze_contract.md §2。"},
            {"action": "让 build_request 推断",
             "detail": "不显式传 sm 时 build_request 会按数据形态推断；显式传错会覆盖推断导致此错。"},
        ],
    ),
    (
        r"Argument '(\w+)' is NULL",
        "COZE_E10_NULL_ARG",
        "R 端某必需参数/列为 NULL（取不到值）。",
        [
            "数据缺该列，或该列全为 NA/空。",
            "single_group_meta 常见：缺 mean / n 列（或其别名未被识别）。",
        ],
        [
            {"action": "补齐报错指名的列",
             "detail": "检查 coze 报错里 Argument '<列>' 的名称，确认数据里有该列且非全空。"},
            {"action": "single_group_meta 必填",
             "detail": "单组均值 Meta 需 mean + n（+sd）；单组率需 event + n。缺则补列或改 task。"},
        ],
    ),
    (
        r"missing value where (TRUE|true)/FALSE",
        "COZE_E11_NA_VALUE",
        "数据含缺失值(NA)，导致 R 逻辑判断（if/while）崩溃。",
        [
            "某列混入了 NA / 空字符串 / 非数值。",
            "2×2 四格表有缺失格子；或效应量列有空。",
        ],
        [
            {"action": "删除/补全含 NA 的研究行",
             "detail": "用 na.omit() 或人工删除空行；确保二分类事件数/样本量无空值。"},
            {"action": "出站前本地预检",
             "detail": "coze_contract_validate 现会对 data.rows 做 NA/空值扫描并预警（W07）。"},
        ],
    ),
    (
        r"Cannot recognize data format",
        "COZE_E12_DATA_FORMAT",
        "数据类型无法识别（未提供合法格式）。",
        [
            "期望 binary/continuous/pre-computed/single-group 列但都没给齐。",
            "列名未被别名表识别，colmap 没指对。",
        ],
        [
            {"action": "明确数据形态",
             "detail": "二分类→ event_exp/n_exp/event_ctrl/n_ctrl；连续→ mean/sd/n；"
                       "已算效应量→ te/sete（或 yi/vi）。"},
            {"action": "走 build_request 自动识别",
             "detail": "列名别名表能识别中英文同义列名；仅剩解析不出的才需 --colmap。"},
        ],
    ),
    (
        r"separate sub-networks|netconnection",
        "COZE_E13_NMA_DISCONNECTED",
        "NMA 网络不连通（存在 ≥2 个互不相连的子网络）。",
        [
            "干预措施之间缺乏共同对比的研究，网络被割裂。",
            "部分干预只在少数研究出现，无法并入主网络。",
        ],
        [
            {"action": "用 netconnection 识别子网络",
             "detail": "R 里 netmeta::netconnection() 可列出各子网络；只保留想分析的那块。"},
            {"action": "补入连接研究",
             "detail": "加入能连接各子网络的头对头研究，使网络连通后再做 NMA。"},
        ],
    ),
    (
        r"pre-computed effect-size columns|requires pre-computed",
        "COZE_E14_PRECOMPUTED_ES",
        "该 task 需要预计算效应量列（yi/vi 或 te/sete），但数据未提供。",
        [
            "用了 leave_one_out / cumulative 等需已算效应量的 task，却只给了原始数据。",
            "数据只给了 2×2 或 mean/sd，未先算效应量。",
        ],
        [
            {"action": "先算效应量再喂入",
             "detail": "用 pairwise_meta 先算出 yi/vi（或 te/sete），再把结果喂给 leave_one_out。"},
            {"action": "直接给 te/sete 列",
             "detail": "若已有效应量，直接提供 te/sete（或 yi/vi）列，跳过效应量计算步骤。"},
        ],
    ),
    (
        r"numbers of columns of arguments do not match|columns of arguments do not match",
        "COZE_E15_COLUMN_COUNT",
        "参与运算的列数量不对齐（行列长度不一致）。",
        [
            "不同数值列的行数不一致（某列比其它短）。",
            "某列缺失导致与其它列长度不匹配。",
        ],
        [
            {"action": "对齐各数值列",
             "detail": "确保所有数值列行数一致、无缺失行；删除不完整的研究行。"},
            {"action": "走 build_request 自动对齐",
             "detail": "build_request 会按行对齐各列，避免手搓时长度错位。"},
        ],
    ),
]


class ErrorAnalysis:
    __slots__ = ("code", "summary", "causes", "fixes", "raw_notes", "task", "matched")

    def __init__(self, code, summary, causes, fixes, raw_notes="", task=None, matched=True):
        self.code = code
        self.summary = summary
        self.causes = causes
        self.fixes = fixes
        self.raw_notes = raw_notes
        self.task = task
        self.matched = matched

    def as_dict(self):
        return {
            "code": self.code,
            "summary": self.summary,
            "causes": self.causes,
            "fixes": self.fixes,
            "raw_notes": self.raw_notes,
            "task": self.task,
            "matched": self.matched,
        }


def analyze_coze_error(resp) -> ErrorAnalysis | None:
    """分析 coze 错误响应（status=='error'）。非 error 返回 None。"""
    if not isinstance(resp, dict):
        return None
    status = resp.get("status")
    if status != "error":
        return None

    notes = resp.get("notes") or ""
    warnings = resp.get("warnings") or []
    task = resp.get("task")
    if isinstance(warnings, list):
        wtext = " ".join(str(w) for w in warnings)
    else:
        wtext = str(warnings)
    haystack = ("%s %s" % (notes, wtext)).lower()

    for pat, code, summary, causes, fixes in _SIGNATURES:
        if re.search(pat, haystack, flags=re.IGNORECASE):
            return ErrorAnalysis(code, summary, causes, fixes,
                                 raw_notes=str(notes), task=task, matched=True)

    # 通用兜底：未识别到具体签名
    return ErrorAnalysis(
        "COZE_E99_GENERIC",
        "coze 返回 status=error（HTTP 200 但任务未成功，符合「网关 200 ≠ 任务成功」）。",
        ["原始报错信息见下方 raw_notes；可能是数据形态 / 参数 / 环境限制。"],
        [
            {"action": "重走 build_request 装配",
             "detail": "用 scripts/run_meta.py --query ... --data <文件> 重新生成合规信封，避免手搓字段名。"},
            {"action": "贴出 raw_notes 给维护者",
             "detail": "若无法自行判断，把下方 coze 原始 notes 发给技能维护者定位。"},
        ],
        raw_notes=str(notes), task=task, matched=False,
    )


def render_error_analysis(ea: ErrorAnalysis) -> str:
    """渲染成多行文本（给 agent / CLI 转述给用户）。"""
    lines = []
    lines.append("【coze 错误诊断 · %s】" % ea.code)
    lines.append(ea.summary)
    if ea.causes:
        lines.append("可能原因：")
        for c in ea.causes:
            lines.append("  • " + c)
    lines.append("修正动作：")
    for f in ea.fixes:
        lines.append("  → %s：%s" % (f.get("action", ""), f.get("detail", "")))
    if ea.raw_notes:
        lines.append("coze 原始报错：%s" % ea.raw_notes[:300])
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    import json
    if len(sys.argv) > 1:
        try:
            resp = json.load(open(sys.argv[1], encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            print("无法读取 JSON: %s" % e)
            sys.exit(1)
    else:
        resp = json.load(sys.stdin)
    ea = analyze_coze_error(resp)
    if ea is None:
        print("非 error 响应，无需诊断。")
        sys.exit(0)
    print(render_error_analysis(ea))
    sys.exit(0)
