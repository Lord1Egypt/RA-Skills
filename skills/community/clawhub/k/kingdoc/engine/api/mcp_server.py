"""KingDoc MCP Server — 真实接入金山文档（WPS）开放平台

深度绑定在线文档能力：
- 云端 40+ 工具直连 open.kdocs.cn 开放 API（文件/表格/多维表/收集表/回收站/版本/权限/空间/通知/用户）
- 本地免密钥工具：DOCX/PPTX 生成、思维导图/流程图 SVG 渲染、本地 OCR、硬件画像
- 自动按本机硬件分配并发子进程数，避免拖累用户电脑
- 每日自动更新提醒（不自动安装）

运行：python -m engine.api.mcp_server --config ./config.json
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
import traceback
from pathlib import Path
from typing import Dict, List, Optional, Any

# 把 skill 根目录加入 path，便于 import engine.*
SKILL_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SKILL_ROOT))

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as e:  # 缺少 mcp 依赖时给出清晰指引
    sys.stderr.write(
        "KingDoc 需要 mcp 依赖：pip install mcp\n"
        "（若已通过 setup.sh/setup.ps1 安装仍报错，请确认 venv 已激活）\n"
        f"import error: {e}\n"
    )
    raise

from engine.hardware import get_recommended_settings
from engine.update_check import build_reminder, FEEDBACK_EMAIL
from engine.exceptions import KingDocError

APP_VERSION = "4.4.0"

# 配置路径：环境变量优先，其次 skill 根目录 config.json
CONFIG_PATH = os.environ.get("KINGDOC_CONFIG", str(SKILL_ROOT / "config.json"))

mcp = FastMCP("kingdoc")


def _backend():
    """惰性创建云端后端（需要 config / App Key）。"""
    from engine.api.tools import KingDocMcpServer
    return KingDocMcpServer(CONFIG_PATH)


def _local_root() -> Path:
    return SKILL_ROOT / "engine" / "local"


def _to_text(obj: Any) -> str:
    if isinstance(obj, str):
        return obj
    try:
        return json.dumps(obj, ensure_ascii=False, indent=2)
    except Exception:
        return str(obj)


def _wrap(fn_name: str):
    """统一包裹云端调用：捕获鉴权/网络异常，返回友好文本而非崩溃。"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                backend = _backend()
                method = getattr(backend, fn_name)
                result = method(*args, **kwargs)
                return _to_text(result)
            except KingDocError as e:
                return f"[{e.code}] {e.message}"
            except FileNotFoundError as e:
                return ("[KD001] 未找到 config.json，云端功能需要金山开放平台 App Key。\n"
                        "请先运行 setup.sh / setup.ps1 配置，或使用本地免密钥工具"
                        "（kdoc.local.* / kdoc.local.ocr.*）。")
            except Exception as e:
                return f"[KD010] 调用失败：{e}\n{traceback.format_exc()[-300:]}"
        return wrapper
    return decorator


# ===========================================================================
# 一、文件管理（深度绑定金山在线文档）
# ===========================================================================
@mcp.tool()
async def kdoc_file_create(name: str, doc_type: str, folder_id: Optional[str] = None,
                           content: Optional[str] = None) -> str:
    """创建在线文档。doc_type 取值：doc/sheet/ppt/smart_note/mindmap/flowchart/form/attachment。
    返回新文档的 file_id 与访问链接。"""
    return await _wrap("kdoc_file_create")(name, doc_type, folder_id, content)

@mcp.tool()
async def kdoc_file_content(file_id: str) -> str:
    """读取在线文档内容（按品类自动路由）。"""
    return await _wrap("kdoc_file_content")(file_id)

@mcp.tool()
async def kdoc_file_info(file_id: str) -> str:
    """获取文档元信息（类型/版本/权限），编辑前必须先调用以确认品类。"""
    return await _wrap("kdoc_file_info")(file_id)

@mcp.tool()
async def kdoc_file_rename(file_id: str, name: str) -> str:
    """重命名文档。"""
    return await _wrap("kdoc_file_rename")(file_id, name)

@mcp.tool()
async def kdoc_file_move(file_id: str, folder_id: str) -> str:
    """移动文档到目标文件夹。"""
    return await _wrap("kdoc_file_move")(file_id, folder_id)

@mcp.tool()
async def kdoc_file_delete(file_id: str) -> str:
    """⚠️ 危险操作：软删除文档到回收站（可回收）。彻底删除请用 kdoc_trash_destroy（需二次确认）。"""
    return await _wrap("kdoc_file_delete")(file_id)

@mcp.tool()
async def kdoc_file_search(keyword: str, limit: int = 10) -> str:
    """按关键词搜索在线文档。"""
    return await _wrap("kdoc_file_search")(keyword, limit)

@mcp.tool()
async def kdoc_file_upload(file_path: str, folder_id: Optional[str] = None) -> str:
    """上传本地文件到云端（新建文档/附件，二进制安全）。默认拦截禁止类型
    （.exe/.bat/.ps1/.zip 等，详见安全规范）；仅技能内部生成的
    docx/pptx/pdf/svg/png 等可上传。"""
    try:
        from engine.security import assert_upload_safe
        assert_upload_safe(file_path, internal=True)
        backend = _backend()
        return _to_text(backend.kdoc_file_upload(file_path, folder_id))
    except KingDocError as e:
        return f"[{e.code}] {e.message}"
    except FileNotFoundError:
        return "[KD001] 未找到 config.json，云端上传需先配置金山 App Key（本地生成无需 Key）。"
    except Exception as e:
        return f"[KD010] 上传失败：{e}"

@mcp.tool()
async def kdoc_file_download(file_id: str, target_path: str) -> str:
    """导出在线文档内容到本地文件。"""
    return await _wrap("kdoc_file_download")(file_id, target_path)


# ===========================================================================
# 二、文件夹 / 空间
# ===========================================================================
@mcp.tool()
async def kdoc_folder_create(name: str, parent_id: Optional[str] = None) -> str:
    """创建文件夹。"""
    return await _wrap("kdoc_folder_create")(name, parent_id)

@mcp.tool()
async def kdoc_folder_list(folder_id: Optional[str] = None) -> str:
    """列出子文件夹。"""
    return await _wrap("kdoc_folder_list")(folder_id)

@mcp.tool()
async def kdoc_space_quota() -> str:
    """查询空间用量与剩余配额。"""
    return await _wrap("kdoc_space_quota")()


# ===========================================================================
# 三、回收站 / 版本历史（金山独有，对标腾讯无此能力）
# ===========================================================================
@mcp.tool()
async def kdoc_trash_list(limit: int = 20, offset: int = 0) -> str:
    """列出回收站文件。"""
    return await _wrap("kdoc_trash_list")(limit, offset)

@mcp.tool()
async def kdoc_trash_recover(file_id: str) -> str:
    """从回收站恢复文件（误删可救回）。"""
    return await _wrap("kdoc_trash_recover")(file_id)

@mcp.tool()
async def kdoc_trash_destroy(file_id: str) -> str:
    """⚠️ 危险操作（不可逆）：彻底删除回收站文件。执行前必须向用户二次确认。"""
    return await _wrap("kdoc_trash_destroy")(file_id)

@mcp.tool()
async def kdoc_version_list(file_id: str) -> str:
    """列出文档历史版本。"""
    return await _wrap("kdoc_version_list")(file_id)

@mcp.tool()
async def kdoc_version_restore(file_id: str, version: int) -> str:
    """回滚文档到指定历史版本。"""
    return await _wrap("kdoc_version_restore")(file_id, version)


# ===========================================================================
# 四、电子表格（et API 精细编辑）
# ===========================================================================
@mcp.tool()
async def kdoc_et_create(name: str) -> str:
    """创建在线电子表格。"""
    return await _wrap("kdoc_et_create")(name)

@mcp.tool()
async def kdoc_et_range_write(sheet_id: str, range: str, values: List[List[Any]]) -> str:
    """批量写入单元格区域（连续 3+ 写入必须用批量接口）。"""
    return await _wrap("kdoc_et_range_write")(sheet_id, range, values)

@mcp.tool()
async def kdoc_et_formula_set(sheet_id: str, cell: str, formula: str) -> str:
    """设置单元格公式。"""
    return await _wrap("kdoc_et_formula_set")(sheet_id, cell, formula)


# ===========================================================================
# 五、多维表格（dbt API 精细编辑）
# ===========================================================================
@mcp.tool()
async def kdoc_dbt_create(name: str) -> str:
    """创建多维表格。"""
    return await _wrap("kdoc_dbt_create")(name)

@mcp.tool()
async def kdoc_dbt_field_add(table_id: str, name: str, field_type: str,
                             options: Optional[List[str]] = None) -> str:
    """添加字段（text/number/select/date 等）。"""
    return await _wrap("kdoc_dbt_field_add")(table_id, name, field_type, options)

@mcp.tool()
async def kdoc_dbt_record_add_batch(table_id: str, records: List[Dict]) -> str:
    """批量添加记录。"""
    return await _wrap("kdoc_dbt_record_add_batch")(table_id, records)

@mcp.tool()
async def kdoc_dbt_record_query(table_id: str, filter: Optional[str] = None,
                                limit: int = 100) -> str:
    """查询记录，filter 为 JSON 字符串。"""
    import json as _json
    fobj = _json.loads(filter) if filter else None
    return await _wrap("kdoc_dbt_record_query")(table_id, fobj, limit)

@mcp.tool()
async def kdoc_dbt_webhook_set(table_id: str, callback_url: str,
                               events: List[str]) -> str:
    """设置多维表格 Webhook 事件监听。"""
    return await _wrap("kdoc_dbt_webhook_set")(table_id, callback_url, events)


# ===========================================================================
# 六、收集表
# ===========================================================================
@mcp.tool()
async def kdoc_form_create(name: str, description: Optional[str] = None) -> str:
    """创建收集表/问卷。"""
    return await _wrap("kdoc_form_create")(name, description)

@mcp.tool()
async def kdoc_form_answers(form_id: str, limit: int = 50) -> str:
    """查询收集表答卷。"""
    return await _wrap("kdoc_form_answers")(form_id, limit)


# ===========================================================================
# 七、格式转换 / 纯文本提取 / 权限 / 通知 / 用户
# ===========================================================================
@mcp.tool()
async def kdoc_office_convert(file_id: str, target_format: str) -> str:
    """格式转换：doc→pdf/word/excel/ppt 等。"""
    return await _wrap("kdoc_office_convert")(file_id, target_format)

@mcp.tool()
async def kdoc_office_extract(file_id: str) -> str:
    """提取文档纯文本。"""
    return await _wrap("kdoc_office_extract")(file_id)

@mcp.tool()
async def kdoc_file_permission(file_id: str, members: List[Dict]) -> str:
    """变更文档权限/分享成员。"""
    return await _wrap("kdoc_file_permission")(file_id, members)

@mcp.tool()
async def kdoc_notification_send(channel: str, webhook_key: str, content: str) -> str:
    """发送通知（企微/钉钉/金山协作机器人）。content 为 JSON 字符串。"""
    import json as _json
    return await _wrap("kdoc_notification_send")(channel, webhook_key, _json.loads(content))

@mcp.tool()
async def kdoc_user_info() -> str:
    """获取当前用户信息。"""
    return await _wrap("kdoc_user_info")()


# ===========================================================================
# 八、本地免密钥工具（无需 App Key，离线可用）
# ===========================================================================
@mcp.tool()
async def kdoc_local_docx_generate(content: str, template: str = "blank",
                                   output_path: Optional[str] = None) -> str:
    """【免密钥】根据 Markdown/文本生成本地 DOCX（会议纪要/周报/合同等），可直接上传覆盖。
    template: blank/weekly_report/meeting_notes。"""
    try:
        from engine.local.generators import DocxGenerator
        out = output_path or str(SKILL_ROOT / "output" / "generated.docx")
        gen = DocxGenerator()
        # 简易 Markdown 段落解析
        for block in content.split("\n\n"):
            block = block.strip()
            if not block:
                continue
            if block.startswith("# "):
                gen.add_heading(block[2:].strip(), 1)
            elif block.startswith("## "):
                gen.add_heading(block[3:].strip(), 2)
            elif block.startswith("- ") or block.startswith("• "):
                gen.add_bullet_list([ln[2:].strip() for ln in block.splitlines()])
            else:
                gen.add_paragraph(block)
        gen.save(out)
        return f"[OK] 已生成本地 DOCX：{out}（可通过 kdoc_file_upload 覆盖上传）"
    except ImportError:
        return "[ERR] 需要 python-docx：pip install python-docx"
    except Exception as e:
        return f"[ERR] 生成失败：{e}"

@mcp.tool()
async def kdoc_local_pptx_generate(title: str, slides: List[Dict], subtitle: str = "",
                                   output_path: Optional[str] = None) -> str:
    """【免密钥】生成本地 PPTX。slides: [{title, bullets:[...]}] 或 [{title, image}]。"""
    try:
        from engine.local.generators import PptxGenerator
        out = output_path or str(SKILL_ROOT / "output" / "generated.pptx")
        gen = PptxGenerator()
        gen.add_title_slide(title, subtitle)
        for s in slides:
            if s.get("image"):
                gen.add_image_slide(s.get("title", ""), s["image"])
            else:
                gen.add_content_slide(s.get("title", ""), s.get("bullets", []))
        gen.save(out)
        return f"[OK] 已生成本地 PPTX：{out}（可通过 kdoc_file_upload 覆盖上传）"
    except ImportError:
        return "[ERR] 需要 python-pptx：pip install python-pptx"
    except Exception as e:
        return f"[ERR] 生成失败：{e}"

@mcp.tool()
async def kdoc_local_mindmap_generate(code: str, output_path: Optional[str] = None) -> str:
    """【免密钥】根据 mermaid graph 代码生成本地思维导图 SVG。"""
    try:
        from engine.local.generators import MindmapGenerator
        out = output_path or str(SKILL_ROOT / "output" / "mindmap.svg")
        gen = MindmapGenerator()
        import re as _re
        for line in code.splitlines():
            line = line.strip()
            if not line or line.startswith("graph") or line.startswith("mindmap"):
                continue
            # 形如  A[标签] / A(标签) / A --> B[标签] / A --- B
            m = _re.search(
                r'([A-Za-z0-9_]+)\s*(?:-->|---|->|-)\s*([A-Za-z0-9_]+)\s*(?:\[([^\]]*)\]|\(([^)]*)\))?',
                line,
            )
            if m:
                src, tgt = m.group(1), m.group(2)
                tgt_label = m.group(3) or m.group(4) or tgt
                gen.add_node(src, src)
                gen.add_node(tgt, tgt_label, parent_id=src)
            else:
                m2 = _re.search(r'([A-Za-z0-9_]+)\s*(?:\[([^\]]*)\]|\(([^)]*)\))', line)
                if m2:
                    nid = m2.group(1)
                    lbl = m2.group(2) or m2.group(3) or nid
                    gen.add_node(nid, lbl)
        gen.render_svg(out)
        return f"[OK] 已生成本地思维导图 SVG：{out}（上传后即在线思维导图）"
    except Exception as e:
        return f"[ERR] 生成失败：{e}"

@mcp.tool()
async def kdoc_local_flowchart_generate(code: str, output_path: Optional[str] = None) -> str:
    """【免密钥】根据 mermaid flowchart 代码生成本地流程图 SVG。"""
    try:
        from engine.local.generators import FlowchartGenerator
        out = output_path or str(SKILL_ROOT / "output" / "flowchart.svg")
        gen = FlowchartGenerator()
        import re as _re
        for i, line in enumerate(code.splitlines()):
            line = line.strip()
            if not line or line.startswith("graph") or line.startswith("flowchart"):
                continue
            m = _re.search(
                r'([A-Za-z0-9_]+)\s*(?:\[([^\]]*)\]|\(([^)]*)\)|\{([^}]*)\})',
                line,
            )
            label = (m.group(2) or m.group(3) or m.group(4) or line) if m else line
            stype = "process"
            if line.startswith("start") or ("(" in line and "[" in line):
                stype = "start"
            elif line.startswith("end") or line.endswith("])"):
                stype = "end"
            elif "{" in line:
                stype = "decision"
            gen.add_step(f"step{i}", label or f"步骤{i}", stype)
        gen.render_svg(out)
        return f"[OK] 已生成本地流程图 SVG：{out}（上传后即在线流程图）"
    except Exception as e:
        return f"[ERR] 生成失败：{e}"

@mcp.tool()
async def kdoc_local_ocr_extract(image_path: str, lang: str = "chi_sim+eng") -> str:
    """【免密钥】本地 OCR 提取图片文字：v4.2 收敛为唯一入口，
    优先桥接 wps-office-suite OCR，未装则 Tesseract 最小兜底（数据不出域）。"""
    try:
        from engine.local.ocr import extract_text_bridged
        res = extract_text_bridged(image_path, lang=lang)
        if res["source"] == "none":
            return f"[OCR 未就绪] {res['hint']}"
        return _to_text(res)
    except Exception as e:
        return f"[ERR] OCR 失败：{e}"

@mcp.tool()
async def kdoc_local_hardware_profile() -> str:
    """【免密钥】采集本机硬件并自动给出推荐并发子进程数 / 批量大小（避免拖累电脑）。"""
    try:
        settings = get_recommended_settings()
        return _to_text(settings)
    except Exception as e:
        return f"[ERR] 采集失败：{e}"


# ===========================================================================
# 九、更新提醒 / 反馈
# ===========================================================================
@mcp.tool()
async def kdoc_skill_update_check() -> str:
    """每日首次调用时检查 KingDoc 更新；有新版返回升级提醒（不自动安装）。"""
    try:
        reminder = build_reminder(APP_VERSION)
        if reminder:
            return reminder
        return "[OK] 已是最新版本。"
    except Exception as e:
        return f"[INFO] 更新检查跳过：{e}"

@mcp.tool()
async def kdoc_skill_feedback(message: str) -> str:
    """提交功能建议/问题反馈（仅回显并提示邮箱，不自动发送）。"""
    return (f"感谢反馈！我们会认真评估。\n"
            f"您的建议已记录：{message}\n"
            f"也可直接邮件联系作者：{FEEDBACK_EMAIL}")


# ===========================================================================
# 十、WPS AI 能力（本地降级优先，自研逻辑实现）
# ===========================================================================
@mcp.tool()
async def kdoc_wps_ai_write(text: str, action: str = "polish") -> str:
    """【免密钥】AI 写作辅助：润色/扩写/缩写/续写/改写。

    action: polish(润色) / expand(扩写) / shorten(缩写) /
           continue_write(续写) / rewrite(改写)
    本地降级处理，效果有限但零配置可用。"""
    try:
        from engine.wps_ai.adapter import get_adapter
        result = get_adapter().write(text, action)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 写作辅助失败：{e}"

@mcp.tool()
async def kdoc_wps_ai_analyze(data: str, question: str) -> str:
    """【免密钥】AI 数据分析：自然语言提问，生成公式建议与基础统计。

    data: CSV 文本或表格数据（每行数值用逗号/空格分隔）
    question: 自然语言问题（如"分析趋势"、"计算平均"）
    本地基础统计分析，零配置可用。"""
    try:
        from engine.wps_ai.adapter import get_adapter
        result = get_adapter().analyze(data, question)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 数据分析失败：{e}"

@mcp.tool()
async def kdoc_wps_ai_ppt(outline: str, output_path: str = "") -> str:
    """【免密钥】AI PPT 生成：根据大纲自动生成本地 PPT。

    outline: Markdown 大纲（# 标题 → ## 子标题 → - 要点）
    output_path: 输出路径（默认 output/wps_ai_ppt.pptx）
    本地 python-pptx 生成，零配置可用。"""
    try:
        from engine.wps_ai.adapter import get_adapter
        out = output_path or str(SKILL_ROOT / "output" / "wps_ai_ppt.pptx")
        result = get_adapter().ppt(outline, output_path=out)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] PPT 生成失败：{e}"

@mcp.tool()
async def kdoc_wps_ai_read(content: str, action: str = "summarize",
                           question: str = "") -> str:
    """【免密钥】AI 阅读助手：总结/问答/思维导图。

    action: summarize(总结) / qa(问答，需传 question) / mindmap(思维导图)
    content: 文档全文
    本地 TextRank 摘要 + 关键词提取，零配置可用。"""
    try:
        from engine.wps_ai.adapter import get_adapter
        result = get_adapter().read(content, action, question=question)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 阅读助手失败：{e}"

@mcp.tool()
async def kdoc_wps_ai_detect_intent(user_input: str) -> str:
    """检测用户输入意图，返回匹配的 WPS AI 能力。"""
    try:
        from engine.wps_ai.adapter import get_adapter
        intent = get_adapter().detect_intent(user_input)
        caps = get_adapter().get_capabilities()
        return _to_text({"intent": intent, "capabilities": caps})
    except Exception as e:
        return f"[ERR] 意图检测失败：{e}"


# ===========================================================================
# 十一、协同编辑冲突解决（自研，零外部依赖）
# ===========================================================================
@mcp.tool()
async def kdoc_conflict_detect(base_text: str, version_a: str, version_b: str) -> str:
    """【免密钥】冲突检测：检测多人并发修改的冲突位置与双方内容。

    返回结构化冲突列表与统计。本地 difflib 算法，零配置可用。"""
    try:
        from engine.conflict_resolver import detect_conflicts
        result = detect_conflicts(base_text, version_a, version_b)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 冲突检测失败：{e}"

@mcp.tool()
async def kdoc_conflict_merge(base_text: str, version_a: str, version_b: str) -> str:
    """【免密钥】智能合并：无冲突段自动合并，冲突段标注 VERSION_A/VERSION_B。

    返回合并后文本与冲突统计。本地 difflib 算法，零配置可用。"""
    try:
        from engine.conflict_resolver import merge_versions
        result = merge_versions(base_text, version_a, version_b)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 合并失败：{e}"

@mcp.tool()
async def kdoc_conflict_diff(version_a: str, version_b: str,
                             label_a: str = "版本A", label_b: str = "版本B") -> str:
    """【免密钥】冲突可视化：生成 Git diff 风格的结构化差异数据。

    返回 diff 行列表、统计与可选 HTML。本地 difflib 算法，零配置可用。"""
    try:
        from engine.conflict_resolver import diff_versions
        result = diff_versions(version_a, version_b, label_a, label_b)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] diff 失败：{e}"

@mcp.tool()
async def kdoc_conflict_resolve(base_text: str, version_a: str, version_b: str,
                               strategy: str = "keep_a",
                               manual_text: str = "") -> str:
    """【免密钥】冲突解决：应用合并策略。

    strategy: keep_a(保留A) / keep_b(保留B) / manual(手动合并，需传 manual_text) / auto_merge(自动合并)
    本地 difflib 算法，零配置可用。"""
    try:
        from engine.conflict_resolver import resolve_conflicts
        result = resolve_conflicts(base_text, version_a, version_b, strategy, manual_text)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 冲突解决失败：{e}"


# ===========================================================================
# 十二、文档内容合规检查（v3.4.0 新增，自研正则+规则引擎）
# ===========================================================================
@mcp.tool()
async def kdoc_compliance_sensitive(text: str, custom_words: str = "") -> str:
    """【免密钥】敏感词扫描：内置敏感词库（适配中国监管），标注命中位置。

    custom_words: 逗号分隔的额外敏感词
    本地正则匹配，零配置可用。"""
    try:
        from engine.compliance_check import scan_sensitive
        words = [w.strip() for w in custom_words.split(",") if w.strip()] if custom_words else None
        result = scan_sensitive(text, custom_words=words)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 敏感词扫描失败：{e}"

@mcp.tool()
async def kdoc_compliance_leak(text: str) -> str:
    """【免密钥】数据泄露检测：扫描手机号/身份证号/银行卡号/邮箱等敏感信息。

    返回风险等级+脱敏显示。本地正则匹配，零配置可用。"""
    try:
        from engine.compliance_check import detect_leak
        result = detect_leak(text)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 泄露检测失败：{e}"

@mcp.tool()
async def kdoc_compliance_format(file_path: str) -> str:
    """【免密钥】格式规范检查：按企业文档规范逐项检查，生成不合规清单。

    支持 .docx / .pptx / .txt / .md 格式。本地 XML 解析，零配置可用。"""
    try:
        from engine.compliance_check import check_format
        result = check_format(file_path)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 格式检查失败：{e}"

@mcp.tool()
async def kdoc_compliance_classify(text: str) -> str:
    """【免密钥】密级自动标注：根据内容建议密级（公开/内部/秘密/机密）。

    本地关键词+规则引擎，零配置可用。"""
    try:
        from engine.compliance_check import classify
        result = classify(text)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 密级标注失败：{e}"


# ===========================================================================
# 十三、实时协同编辑（v3.5.0 新增，序列 CRDT 自研实现）
# ===========================================================================
@mcp.tool()
async def kdoc_realtime_create(client_id: str, session_id: str = "") -> str:
    """【免密钥】创建实时协同文档。

    client_id: 当前客户端标识
    session_id: 会话 ID（留空则自动创建）
    本地 CRDT 引擎，零配置可用。"""
    try:
        from engine.realtime_collab import CRDTDocument
        doc = CRDTDocument(client_id)
        return _to_text({"client_id": client_id, "status": "created", "doc_id": id(doc)})
    except Exception as e:
        return f"[ERR] 创建协同文档失败：{e}"

@mcp.tool()
async def kdoc_realtime_insert(client_id: str, pos: int, text: str) -> str:
    """【免密钥】在协同文档中插入文本。

    client_id: 当前客户端标识
    pos: 插入位置
    text: 插入的文本
    本地 CRDT 引擎，零配置可用。"""
    try:
        from engine.realtime_collab import CRDTDocument
        doc = CRDTDocument(client_id)
        ops = doc.local_insert(pos, text)
        return _to_text({"client_id": client_id, "text": doc.get_text(), "ops_count": len(ops)})
    except Exception as e:
        return f"[ERR] 插入失败：{e}"

@mcp.tool()
async def kdoc_realtime_delete(client_id: str, pos: int, length: int = 1) -> str:
    """【免密钥】在协同文档中删除文本。

    client_id: 当前客户端标识
    pos: 删除起始位置
    length: 删除长度
    本地 CRDT 引擎，零配置可用。"""
    try:
        from engine.realtime_collab import CRDTDocument
        doc = CRDTDocument(client_id)
        ops = doc.local_delete(pos, length)
        return _to_text({"client_id": client_id, "text": doc.get_text(), "ops_count": len(ops)})
    except Exception as e:
        return f"[ERR] 删除失败：{e}"

@mcp.tool()
async def kdoc_realtime_get_text(client_id: str) -> str:
    """【免密钥】获取协同文档当前文本。

    client_id: 当前客户端标识
    本地 CRDT 引擎，零配置可用。"""
    try:
        from engine.realtime_collab import CRDTDocument
        doc = CRDTDocument(client_id)
        return _to_text({"client_id": client_id, "text": doc.get_text()})
    except Exception as e:
        return f"[ERR] 获取文本失败：{e}"

@mcp.tool()
async def kdoc_realtime_stats(client_id: str) -> str:
    """【免密钥】获取协同文档统计信息。

    client_id: 当前客户端标识
    本地 CRDT 引擎，零配置可用。"""
    try:
        from engine.realtime_collab import CRDTDocument
        doc = CRDTDocument(client_id)
        return _to_text(doc.get_stats())
    except Exception as e:
        return f"[ERR] 获取统计失败：{e}"


# ===========================================================================
# 十三、WPS AI 深度集成（v3.6.0 新增，段落级 AI 操作）
# ===========================================================================
@mcp.tool()
async def kdoc_wps_ai_rewrite(paragraph: str, style: str = "formal") -> str:
    """【免密钥】AI 段落改写：将指定段落按目标风格改写。

    style: formal(正式) / casual(口语) / concise(简洁) / elaborate(详细)
    本地降级占位，WPS AI API 开放后升级为原生。"""
    try:
        from engine.wps_ai.adapter import get_adapter
        result = get_adapter().rewrite_paragraph(paragraph, style)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 段落改写失败：{e}"

@mcp.tool()
async def kdoc_wps_ai_summarize(paragraph: str, max_length: int = 100) -> str:
    """【免密钥】AI 段落总结：提取段落核心要点。

    max_length: 最大摘要字数
    本地降级占位，WPS AI API 开放后升级为原生。"""
    try:
        from engine.wps_ai.adapter import get_adapter
        result = get_adapter().summarize_paragraph(paragraph, max_length)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 段落总结失败：{e}"

@mcp.tool()
async def kdoc_wps_ai_continue(paragraph: str, direction: str = "") -> str:
    """【免密钥】AI 段落续写：根据方向继续写作。

    direction: 续写方向（如"详细说明"、"举例"、"总结"）
    本地降级占位，WPS AI API 开放后升级为原生。"""
    try:
        from engine.wps_ai.adapter import get_adapter
        result = get_adapter().continue_paragraph(paragraph, direction)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 段落续写失败：{e}"


# ===========================================================================
# 十五、文档模板市场（v3.6.0 新增）
# ===========================================================================
@mcp.tool()
async def kdoc_template_list(category: str = "") -> str:
    """【免密钥】列出所有可用模板。

    category: 按类别筛选（可选）
    本地模板市场，零配置可用。"""
    try:
        from engine.template_marketplace import list_templates
        result = list_templates(category)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 获取模板列表失败：{e}"

@mcp.tool()
async def kdoc_template_search(keyword: str) -> str:
    """【免密钥】搜索模板。

    keyword: 搜索关键词
    本地模板市场，零配置可用。"""
    try:
        from engine.template_marketplace import search_templates
        result = search_templates(keyword)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 搜索模板失败：{e}"

@mcp.tool()
async def kdoc_template_use(name: str, variables: str = "{}") -> str:
    """【免密钥】使用模板（变量替换）。

    name: 模板名称
    variables: JSON 格式变量，如 '{"title": "周报", "author": "张三"}'
    本地模板市场，零配置可用。"""
    try:
        import json
        from engine.template_marketplace import use_template
        vars_dict = json.loads(variables) if variables else {}
        result = use_template(name, vars_dict)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 使用模板失败：{e}"

@mcp.tool()
async def kdoc_template_refresh() -> str:
    """【免密钥】刷新模板仓库（git pull）。

    本地模板市场，零配置可用。"""
    try:
        from engine.template_marketplace import refresh_templates
        result = refresh_templates(force=True)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 刷新模板失败：{e}"


# ===========================================================================
# 十六、文档对比（v3.5.0 新增，复用 difflib 引擎）
# ===========================================================================
@mcp.tool()
async def kdoc_compare_diff(text_a: str, text_b: str,
                            label_a: str = "版本A", label_b: str = "版本B") -> str:
    """【免密钥】文档对比：两版文档差异高亮。

    返回差异行列表+统计+相似度。本地 difflib 算法，零配置可用。"""
    try:
        from engine.doc_comparator import compare_documents
        result = compare_documents(text_a, text_b, label_a, label_b)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 文档对比失败：{e}"

@mcp.tool()
async def kdoc_compare_summary(text_a: str, text_b: str) -> str:
    """【免密钥】变更摘要：两版文档增删改统计+关键变化。

    本地 difflib 算法，零配置可用。"""
    try:
        from engine.doc_comparator import change_summary
        result = change_summary(text_a, text_b)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 变更摘要失败：{e}"

@mcp.tool()
async def kdoc_compare_export(text_a: str, text_b: str,
                              format: str = "markdown") -> str:
    """【免密钥】导出对比报告。

    format: markdown(默认) | html
    本地 difflib 算法，零配置可用。"""
    try:
        from engine.doc_comparator import export_report
        result = export_report(text_a, text_b, format)
        return result
    except Exception as e:
        return f"[ERR] 导出报告失败：{e}"


# ===========================================================================
# 十七、多维表格视图增强（v3.7.0 新增，对标 Airtable）
# ===========================================================================
@mcp.tool()
async def kdoc_view_render(view_type: str, data: str, config: str = "") -> str:
    """【免密钥】多维表格视图渲染：看板/日历/甘特图。

    view_type: kanban / calendar / gantt
    data: JSON 字符串，格式 {"records": [...], "fields": [...]}
    config: JSON 字符串（可选），如 {"mode": "month"}

    本地渲染引擎，零配置可用。"""
    try:
        import json
        from engine.views import render_view
        data_obj = json.loads(data)
        config_obj = json.loads(config) if config else None
        result = render_view(view_type, data_obj, config_obj)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 视图渲染失败：{e}"

@mcp.tool()
async def kdoc_view_list() -> str:
    """【免密钥】列出所有可用的多维表格视图类型。

    本地规则引擎，零配置可用。"""
    return _to_text({
        "views": [
            {"type": "kanban", "name": "看板", "description": "按状态字段分组卡片"},
            {"type": "calendar", "name": "日历", "description": "按日期字段月/周布局"},
            {"type": "gantt", "name": "甘特图", "description": "时间轴+任务依赖箭头"},
        ]
    })


# ===========================================================================
# 十八、手写/公式识别 OCR（v3.7.0 新增，教育场景）
# ===========================================================================
@mcp.tool()
async def kdoc_ocr_formula(image_path: str, output_format: str = "latex") -> str:
    """【免密钥】数学公式识别：图片 → LaTeX/MathML。

    image_path: 公式图片路径
    output_format: latex（默认）| mathml | text

    本地 Tesseract + 符号映射，零配置可用。"""
    try:
        from engine.ocr.formula_recognizer import FormulaRecognizer
        recognizer = FormulaRecognizer()
        result = recognizer.recognize(image_path, output_format)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 公式识别失败：{e}"

@mcp.tool()
async def kdoc_ocr_education(image_path: str, scene: str = "auto") -> str:
    """【免密钥】教育场景 OCR：手写公式/试卷/题目识别。

    image_path: 图片路径
    scene: auto（自动检测）| handwriting | formula | mixed

    自动判断手写体/印刷公式/混合内容，零配置可用。"""
    try:
        from engine.ocr.education import EducationOCR
        ocr = EducationOCR()
        result = ocr.recognize(image_path, scene)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 教育 OCR 失败：{e}"


# ===========================================================================
# 十九、历史管理（v3.7.0 新增，合并回收站+版本历史）
# ===========================================================================
@mcp.tool()
async def kdoc_history_list(source: str = "trash", limit: int = 20, offset: int = 0,
                            file_id: str = "") -> str:
    """列出历史记录：回收站文件 或 文档历史版本。

    source: trash（回收站）| version（版本历史，需传 file_id）
    limit: 数量限制
    offset: 分页偏移（仅 trash）
    file_id: 文档 ID（仅 version 需要）"""
    try:
        from engine.history import HistoryManager
        mgr = HistoryManager(backend=None)
        if source == "version" and file_id:
            result = mgr.list_versions(file_id, limit)
        else:
            result = mgr.list_history(source, limit, offset)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 获取历史列表失败：{e}"

@mcp.tool()
async def kdoc_history_restore(file_id: str, source: str = "trash",
                               version: int = 0) -> str:
    """恢复文件：从回收站还原 或 回滚到指定版本。

    file_id: 文件 ID
    source: trash | version
    version: 版本号（仅 version 需要，≥1）"""
    try:
        from engine.history import HistoryManager
        mgr = HistoryManager(backend=None)
        result = mgr.restore(file_id, source, version)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 恢复失败：{e}"

@mcp.tool()
async def kdoc_history_destroy(file_id: str) -> str:
    """⚠️ 危险操作（不可逆）：彻底删除回收站文件。执行前必须向用户二次确认。"""
    try:
        from engine.history import HistoryManager
        mgr = HistoryManager(backend=None)
        result = mgr.destroy(file_id)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 删除失败：{e}"


# ===========================================================================
# 二十、智能画布元素级编辑（v3.8.0 新增，对标腾讯文档）
# ===========================================================================
@mcp.tool()
async def kdoc_element_read(file_id: str, element_id: str = "") -> str:
    """【免密钥】读取智能画布元素。

    file_id: 文档 ID
    element_id: 元素 ID（空则返回全量结构化数据）
    本地降级模式，零配置可用。"""
    try:
        from engine.element_engine import CanvasElementEditor
        editor = CanvasElementEditor(backend=None)
        result = editor.read_element(file_id, element_id)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 元素读取失败：{e}"

@mcp.tool()
async def kdoc_element_insert(file_id: str, element_type: str, content: str,
                              position: int = -1, attributes: str = "") -> str:
    """【免密钥】在指定位置插入新元素。

    file_id: 文档 ID
    element_type: text / heading / image / table / divider / code / quote
    content: 元素内容
    position: 插入位置（-1 末尾）
    attributes: JSON 字符串（可选，如 {"level": 2}）
    本地降级模式，零配置可用。"""
    try:
        import json
        from engine.element_engine import CanvasElementEditor
        editor = CanvasElementEditor(backend=None)
        attrs = json.loads(attributes) if attributes else None
        result = editor.insert_element(file_id, element_type, content, position, attrs)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 元素插入失败：{e}"

@mcp.tool()
async def kdoc_element_update(file_id: str, element_id: str, content: str,
                              attributes: str = "") -> str:
    """【免密钥】更新指定元素。

    file_id: 文档 ID
    element_id: 元素 ID
    content: 新内容
    attributes: JSON 字符串（可选）
    本地降级模式，零配置可用。"""
    try:
        import json
        from engine.element_engine import CanvasElementEditor
        editor = CanvasElementEditor(backend=None)
        attrs = json.loads(attributes) if attributes else None
        result = editor.update_element(file_id, element_id, content, attrs)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 元素更新失败：{e}"

@mcp.tool()
async def kdoc_element_delete(file_id: str, element_id: str) -> str:
    """【免密钥】删除指定元素。

    file_id: 文档 ID
    element_id: 元素 ID
    本地降级模式，零配置可用。"""
    try:
        from engine.element_engine import CanvasElementEditor
        editor = CanvasElementEditor(backend=None)
        result = editor.delete_element(file_id, element_id)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 元素删除失败：{e}"

@mcp.tool()
async def kdoc_element_append_md(file_id: str, markdown_content: str,
                                 position: int = -1) -> str:
    """【免密钥】向文档末尾追加 Markdown 内容（增量，不改已有内容）。

    file_id: 文档 ID
    markdown_content: Markdown 内容
    position: 插入位置（-1 末尾）
    本地降级模式，零配置可用。"""
    try:
        from engine.element_engine import CanvasElementEditor
        editor = CanvasElementEditor(backend=None)
        result = editor.append_markdown(file_id, markdown_content, position)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] Markdown 追加失败：{e}"


# ===========================================================================
# 二十一、空间节点管理增强（v3.8.0 新增，对标腾讯文档）
# ===========================================================================
@mcp.tool()
async def kdoc_space_tree(folder_id: str = "", depth: int = 3) -> str:
    """【免密钥】列出空间目录树（递归）。

    folder_id: 文件夹 ID（空字符串表示根目录）
    depth: 递归深度（默认 3 层）
    本地降级模式，零配置可用。"""
    try:
        from engine.space_tree import SpaceTreeManager
        mgr = SpaceTreeManager(backend=None)
        result = mgr.list_tree(folder_id, depth=depth)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 目录树查询失败：{e}"

@mcp.tool()
async def kdoc_space_tree_visualize(folder_id: str = "", format: str = "json") -> str:
    """【免密钥】目录可视化（JSON/Markdown 树形）。

    folder_id: 文件夹 ID（空字符串表示根目录）
    format: json | markdown
    本地降级模式，零配置可用。"""
    try:
        from engine.space_tree import SpaceTreeManager
        mgr = SpaceTreeManager(backend=None)
        result = mgr.visualize_tree(folder_id, format=format)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 目录可视化失败：{e}"

@mcp.tool()
async def kdoc_space_node_create(parent_id: str, name: str, target_id: str,
                                 node_type: str = "shortcut") -> str:
    """【免密钥】创建链接节点（快捷方式/引用）。

    parent_id: 父文件夹 ID
    name: 节点名称
    target_id: 目标文件/文件夹 ID
    node_type: shortcut | reference
    本地降级模式，零配置可用。"""
    try:
        from engine.space_tree import SpaceTreeManager
        mgr = SpaceTreeManager(backend=None)
        result = mgr.create_link_node(parent_id, name, target_id, node_type)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 节点创建失败：{e}"

@mcp.tool()
async def kdoc_space_delete_recursive(folder_id: str, dry_run: bool = True) -> str:
    """⚠️ 危险操作：递归删除文件夹及其所有子内容。

    folder_id: 要删除的文件夹 ID
    dry_run: True 时仅预览不执行（默认安全模式）
    本地降级模式，零配置可用。"""
    try:
        from engine.space_tree import SpaceTreeManager
        mgr = SpaceTreeManager(backend=None)
        result = mgr.delete_recursive(folder_id, dry_run)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 递归删除失败：{e}"


# ===========================================================================
# 二十二、文档内容全文搜索（v3.8.0 新增，超越腾讯）
# ===========================================================================
@mcp.tool()
async def kdoc_content_search(query: str, file_id: str = "", limit: int = 20) -> str:
    """【免密钥】全文搜索文档内容（超越腾讯：搜内容+结果定位高亮）。

    query: 搜索关键词
    file_id: 限定搜索范围（空字符串搜索全部文档）
    limit: 返回结果数量限制
    本地降级模式，零配置可用。"""
    try:
        from engine.content_search import ContentSearchEngine
        engine = ContentSearchEngine(backend=None)
        result = engine.search(query, file_id, limit)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 全文搜索失败：{e}"

@mcp.tool()
async def kdoc_content_search_in_document(file_id: str, query: str) -> str:
    """【免密钥】在指定文档内搜索，返回匹配行及上下文。

    file_id: 文档 ID
    query: 搜索关键词
    本地降级模式，零配置可用。"""
    try:
        from engine.content_search import ContentSearchEngine
        engine = ContentSearchEngine(backend=None)
        result = engine.search_in_document(file_id, query)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 文档内搜索失败：{e}"


# ===========================================================================
# 二十三、统一删除（v3.8.0 新增，合并 delete + trash destroy）
# ===========================================================================
@mcp.tool()
async def kdoc_file_delete_unified(file_id: str, force: bool = False,
                                  from_trash: bool = False) -> str:
    """文件删除统一入口（合并软删除/彻底删除/直接删除）。

    file_id: 文件 ID
    force: True 时直接彻底删除（跳过回收站，⚠️ 需二次确认）
    from_trash: True 时从回收站彻底删除；False 时软删除到回收站

    用法：
        delete(file_id)                    → 软删除到回收站
        delete(file_id, from_trash=True)   → 从回收站彻底删除
        delete(file_id, force=True)       → 直接彻底删除（⚠️）
    需配置金山 App Key 后可用。"""
    try:
        from engine.history import HistoryManager
        mgr = HistoryManager(backend=None)
        result = mgr.delete(file_id, force=force, from_trash=from_trash)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 删除失败：{e}"


# ===========================================================================
# 二十四、本地 OCR 升级（v3.7.0 升级提示）
# ===========================================================================
@mcp.tool()
async def kdoc_local_ocr_extract(image_path: str, lang: str = "chi_sim+eng") -> str:
    """【免密钥】本地 OCR 提取图片文字：v4.2 收敛为唯一入口，
    优先桥接 wps-office-suite OCR，未装则 Tesseract 最小兜底（数据不出域）。"""
    try:
        from engine.local.ocr import extract_text_bridged
        res = extract_text_bridged(image_path, lang=lang)
        if res["source"] == "none":
            return f"[OCR 未就绪] {res['hint']}"
        return _to_text(res)
    except Exception as e:
        return f"[ERR] OCR 失败：{e}"


# ===========================================================================
# 十五、品类管理（v3.5.0 新增，9 品类 + 子类型识别）
# ===========================================================================
@mcp.tool()
async def kdoc_category_resolve(user_input: str) -> str:
    """【免密钥】品类识别：根据用户输入自动识别文档品类（9 品类）。

    返回品类 ID、名称、子类型、编辑方式。本地规则引擎，零配置可用。"""
    try:
        from engine.categories import resolve_category
        result = resolve_category(user_input)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 品类识别失败：{e}"

@mcp.tool()
async def kdoc_category_list() -> str:
    """【免密钥】列出所有可用品类（9 品类）。

    本地规则引擎，零配置可用。"""
    try:
        from engine.categories import list_categories
        result = list_categories()
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 获取品类列表失败：{e}"


# ===========================================================================
# 二十五、块级编辑引擎（v3.9.0 新增，段落级在线编辑）
# ===========================================================================
@mcp.tool()
async def kdoc_block_list(file_id: str) -> str:
    """【免密钥】拉取文档块列表（段落级编辑基础）。

    file_id: 文档 ID
    本地降级模式，零配置可用。"""
    try:
        from engine.blocks import BlockEditor
        editor = BlockEditor(backend=None)
        result = editor.blocks_list(file_id)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 拉取块列表失败：{e}"

@mcp.tool()
async def kdoc_block_replace(file_id: str, block_id: str, content: str,
                             block_type: str = "paragraph") -> str:
    """【免密钥】按 block_id 替换块内容。

    file_id: 文档 ID
    block_id: 块 ID
    content: 新内容
    block_type: paragraph / heading / list / table / code / quote / divider
    本地降级模式，零配置可用。"""
    try:
        from engine.blocks import BlockEditor
        editor = BlockEditor(backend=None)
        result = editor.block_replace(file_id, block_id, content, block_type)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 替换块失败：{e}"

@mcp.tool()
async def kdoc_block_insert(file_id: str, block_id: str, content: str,
                            position: str = "after", block_type: str = "paragraph") -> str:
    """【免密钥】按 block_id 插入新块。

    file_id: 文档 ID
    block_id: 参考块 ID
    content: 新块内容
    position: after（之后）/ before（之前）
    block_type: paragraph / heading / list / table / code / quote / divider
    本地降级模式，零配置可用。"""
    try:
        from engine.blocks import BlockEditor
        editor = BlockEditor(backend=None)
        result = editor.block_insert(file_id, block_id, content, position, block_type)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 插入块失败：{e}"

@mcp.tool()
async def kdoc_block_delete(file_id: str, block_id: str) -> str:
    """【免密钥】按 block_id 删除块。

    file_id: 文档 ID
    block_id: 块 ID
    本地降级模式，零配置可用。"""
    try:
        from engine.blocks import BlockEditor
        editor = BlockEditor(backend=None)
        result = editor.block_delete(file_id, block_id)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 删除块失败：{e}"

@mcp.tool()
async def kdoc_block_move(file_id: str, block_id: str,
                          target_block_id: str, position: str = "after") -> str:
    """【免密钥】按 block_id 移动块。

    file_id: 文档 ID
    block_id: 要移动的块 ID
    target_block_id: 目标块 ID
    position: after / before
    本地降级模式，零配置可用。"""
    try:
        from engine.blocks import BlockEditor
        editor = BlockEditor(backend=None)
        result = editor.block_move(file_id, block_id, target_block_id, position)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 移动块失败：{e}"


# ===========================================================================
# 二十六、演示页替换引擎（v3.9.0 新增，双路径自动选择）
# ===========================================================================
@mcp.tool()
async def kdoc_page_swap(file_id: str, source_path: str, page_number: int,
                         title: str = "", bullets: str = "",
                         layout: str = "title_and_content") -> str:
    """【免密钥】替换演示文稿中的指定页（自动选择页级更新或整文件替换）。

    file_id: 在线文档 ID
    source_path: 原始 PPTX 本地路径
    page_number: 页码（从1开始）
    title: 新页面标题
    bullets: 新页面要点（每行一个）
    layout: 页面布局（title_and_content / title_only / blank）
    本地降级模式，零配置可用。"""
    try:
        from engine.page_swap import PptxPageSwapEngine
        page_content = {
            "title": title,
            "bullets": [b.strip() for b in bullets.splitlines() if b.strip()],
            "layout": layout,
        }
        engine = PptxPageSwapEngine(backend=None)
        result = engine.swap_page(file_id, source_path, page_content, page_number)
        return _to_text(result.to_dict())
    except Exception as e:
        return f"[ERR] 页替换失败：{e}"


# ===========================================================================
# 二十七、配额管理器（v3.9.0 新增，API 配额与限流）
# ===========================================================================
@mcp.tool()
async def kdoc_quota_check() -> str:
    """【免密钥】检查当前配额状态（按天计数，500 次/天限制）。

    返回剩余配额、使用率、状态；用量越过 80% / 95% 时返回 alerts（已触发 webhook 告警）。
    本地模式，零配置可用。"""
    try:
        from engine.quota_manager import check_quota
        result = check_quota()
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 配额检查失败：{e}"

@mcp.tool()
async def kdoc_quota_dashboard() -> str:
    """【免密钥】获取配额看板（配额+令牌桶+硬件+小时分布+建议）。

    本地模式，零配置可用。"""
    try:
        from engine.quota_manager import get_dashboard
        result = get_dashboard()
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 获取看板失败：{e}"

@mcp.tool()
async def kdoc_quota_batch_params(total_items: int) -> str:
    """【免密钥】计算安全的批量任务参数（硬件自适应削峰）。

    total_items: 总任务数
    返回 workers、batch_chunk、预估时间、建议。
    本地模式，零配置可用。"""
    try:
        from engine.quota_manager import get_safe_batch_params
        result = get_safe_batch_params(total_items)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 计算批量参数失败：{e}"


# ===========================================================================
# 二十八、格式转换引擎（v3.9.0 升级，补齐 jpg/png/txt）
# ===========================================================================
@mcp.tool()
async def kdoc_office_convert_enhanced(file_id: str, source_path: str,
                                      target_format: str) -> str:
    """【免密钥】格式转换（云端优先 → 本地兜底）。

    file_id: 在线文档 ID
    source_path: 源文件本地路径
    target_format: pdf / jpg / png / txt / docx / xlsx / pptx / html / md

    v3.9.0 新增：补齐 jpg/png/txt 三类目标格式，全量覆盖参数校验与失败降级链。
    本地降级模式，零配置可用。"""
    try:
        from engine.format_converter import convert_file
        result = convert_file(backend=None, file_id=file_id,
                              source_path=source_path, target_format=target_format)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 格式转换失败：{e}"


# ===========================================================================
# 二十九、本地桥接引擎（v4.0 新增，wps-office-suite 双向互通）
# ===========================================================================
@mcp.tool()
async def kdoc_bridge_status() -> str:
    """【免密钥】获取桥接状态（wps-office-suite 安装状态、映射数量）。

    本地模式，零配置可用。"""
    try:
        from engine.local_bridge import get_local_bridge
        bridge = get_local_bridge(backend=None)
        result = bridge.get_status()
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 获取桥接状态失败：{e}"

@mcp.tool()
async def kdoc_bridge_download(file_id: str, file_name: str = "",
                              file_type: str = "doc") -> str:
    """【免密钥】下行：拉取云端文档到本地临时目录。

    file_id: 文档 ID
    file_name: 文件名
    file_type: doc / sheet / ppt
    本地降级模式，零配置可用。"""
    try:
        from engine.local_bridge import get_local_bridge
        bridge = get_local_bridge(backend=None)
        result = bridge.downstream_download(file_id, file_name, file_type)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 下载失败：{e}"

@mcp.tool()
async def kdoc_bridge_process(file_id: str, action: str,
                             params: str = "") -> str:
    """【免密钥】下行：调用 wps 脚本处理本地文档。

    file_id: 文档 ID
    action: analyze / convert / format / extract
    params: JSON 字符串（可选）
    本地降级模式，零配置可用。"""
    try:
        import json
        from engine.local_bridge import get_local_bridge
        bridge = get_local_bridge(backend=None)
        params_obj = json.loads(params) if params else None
        result = bridge.downstream_process(file_id, action, params_obj)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 处理失败：{e}"

@mcp.tool()
async def kdoc_bridge_upload(file_id: str, local_path: str = "") -> str:
    """【免密钥】上行：将本地文件上传覆盖云端。

    file_id: 文档 ID
    local_path: 本地文件路径（空则使用映射中的路径）
    本地降级模式，零配置可用。"""
    try:
        from engine.local_bridge import get_local_bridge
        bridge = get_local_bridge(backend=None)
        result = bridge.downstream_upload(file_id, local_path)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 上传失败：{e}"

@mcp.tool()
async def kdoc_bridge_sync(file_id: str = "") -> str:
    """【免密钥】上行：同步本地文件到云端（检查 mtime 变化）。

    file_id: 文档 ID（空则同步所有变化的文档）
    本地降级模式，零配置可用。"""
    try:
        from engine.local_bridge import get_local_bridge
        bridge = get_local_bridge(backend=None)
        if file_id:
            result = bridge.upstream_sync(file_id)
        else:
            result = bridge.upstream_sync_all()
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 同步失败：{e}"


# ===========================================================================
# 三十、记忆桥接引擎（v4.0 新增，zwjh 记忆库打通）
# ===========================================================================
@mcp.tool()
async def kdoc_memory_status() -> str:
    """【免密钥】获取记忆桥接状态（zwjh 安装状态、待迁移事件数）。

    本地模式，零配置可用。"""
    try:
        from engine.memory_bridge import get_memory_bridge
        bridge = get_memory_bridge(backend=None)
        result = bridge.get_status()
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 获取记忆桥接状态失败：{e}"

@mcp.tool()
async def kdoc_memory_deposit(event_type: str, doc_id: str,
                              file_name: str = "", action_details: str = "") -> str:
    """【免密钥】发送文档关键事件到 zwjh 长期记忆。

    event_type: create / edit / share / delete
    doc_id: 文档 ID
    file_name: 文件名
    action_details: JSON 字符串（可选）
    本地模式，零配置可用。"""
    try:
        import json
        from engine.memory_bridge import get_memory_bridge
        bridge = get_memory_bridge(backend=None)
        details = json.loads(action_details) if action_details else None
        result = bridge.deposit_event(event_type, doc_id, file_name, details)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 事件写入失败：{e}"

@mcp.tool()
async def kdoc_memory_migrate() -> str:
    """【免密钥】一次性导入所有待迁移事件到 zwjh。

    本地模式，零配置可用。"""
    try:
        from engine.memory_bridge import get_memory_bridge
        bridge = get_memory_bridge(backend=None)
        result = bridge.migrate_pending_events()
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 迁移失败：{e}"


# ===========================================================================
# 三十一、表单答卷收集统计（v4.0 新增，云端数据本地智能加工）
# ===========================================================================
@mcp.tool()
async def kdoc_form_analyze(form_id: str, limit: int = 100) -> str:
    """【免密钥】分析表单答卷（按题统计、交叉分析、未填名单）。

    form_id: 表单 ID
    limit: 答卷数量限制
    本地降级模式，零配置可用。"""
    try:
        from engine.form_analytics import FormAnalyticsEngine
        engine = FormAnalyticsEngine(backend=None)
        result = engine.analyze(form_id, limit)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 分析失败：{e}"

@mcp.tool()
async def kdoc_form_export(form_id: str, format: str = "csv",
                          output_path: str = "") -> str:
    """【免密钥】导出答卷（CSV / Excel）。

    form_id: 表单 ID
    format: csv / xlsx
    output_path: 输出路径（空则使用临时目录）
    本地降级模式，零配置可用。"""
    try:
        from engine.form_analytics import FormAnalyticsEngine
        engine = FormAnalyticsEngine(backend=None)
        if format == "csv":
            result = engine.export_to_csv(form_id, output_path)
        elif format == "xlsx":
            result = engine.export_to_excel(form_id, output_path)
        else:
            result = {"success": False, "error": f"不支持的格式: {format}"}
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 导出失败：{e}"

@mcp.tool()
async def kdoc_form_chart_data(form_id: str) -> str:
    """【免密钥】生成图表数据（供前端渲染）。

    form_id: 表单 ID
    本地降级模式，零配置可用。"""
    try:
        from engine.form_analytics import FormAnalyticsEngine
        engine = FormAnalyticsEngine(backend=None)
        result = engine.generate_chart_data(form_id)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 生成图表数据失败：{e}"

@mcp.tool()
async def kdoc_form_write_to_doc(form_id: str, target_doc_id: str) -> str:
    """【免密钥】将统计结果写回智能文档表格。

    form_id: 表单 ID
    target_doc_id: 目标智能文档 ID
    本地降级模式，零配置可用。"""
    try:
        from engine.form_analytics import FormAnalyticsEngine
        engine = FormAnalyticsEngine(backend=None)
        result = engine.write_to_smart_doc(form_id, target_doc_id)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 写回失败：{e}"


# ===========================================================================
# 三十二、AirScript 在线自动化（v4.1.0 新增，自然语言→脚本→确认→执行）
# ===========================================================================
@mcp.tool()
async def kdoc_airscript_list_capabilities() -> str:
    """【免密钥】列出所有可用的 AirScript 脚本能力域。

    能力域：定时通知 / 数据汇总 / 表格批量操作 / 字段计算
    本地模式，零配置可用。"""
    try:
        from engine.airscript import list_capabilities
        result = list_capabilities()
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 列出能力域失败：{e}"

@mcp.tool()
async def kdoc_airscript_generate(domain: str, params: str = "") -> str:
    """【免密钥】生成 AirScript 脚本（本地规则引擎模板，无需外部 LLM）。

    domain: scheduled_notify / data_summary / batch_operation / field_calc
    params: JSON 字符串，如 '{"channel":"wecom","webhook_key":"xxx","content":"通知内容"}'

    危险操作（DELETE/OVERWRITE/DROP 等）在预检阶段拦截，需二次确认。
    本地模式，零配置可用。"""
    try:
        import json
        from engine.airscript import generate_script
        params_obj = json.loads(params) if params else {}
        result = generate_script(domain, params_obj)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 生成脚本失败：{e}"

@mcp.tool()
async def kdoc_airscript_precheck(script_content: str) -> str:
    """【免密钥】脚本预检：扫描危险操作（DELETE/OVERWRITE/DROP 等）。

    script_content: 脚本内容
    返回危险操作列表与风险等级。
    本地模式，零配置可用。"""
    try:
        from engine.airscript import precheck_script
        result = precheck_script(script_content)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 预检失败：{e}"

@mcp.tool()
async def kdoc_airscript_submit(script_id: str, script_content: str,
                                domain: str, safety_result: str = "") -> str:
    """【免密钥】提交脚本等待用户确认。

    script_id: 脚本 ID
    script_content: 脚本内容
    domain: 能力域
    safety_result: JSON 字符串（预检结果）
    本地模式，零配置可用。"""
    try:
        import json
        from engine.airscript import submit_for_confirmation
        safety_obj = json.loads(safety_result) if safety_result else {"safe": True, "findings": []}
        result = submit_for_confirmation(script_id, script_content, domain, safety_obj)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 提交失败：{e}"

@mcp.tool()
async def kdoc_airscript_execute(script_id: str, confirmed: bool = False) -> str:
    """【免密钥】用户确认后执行脚本。

    script_id: 脚本 ID
    confirmed: 用户确认（True 执行，False 取消）
    本地模式，零配置可用。"""
    try:
        from engine.airscript import confirm_and_execute
        result = confirm_and_execute(script_id, confirmed)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 执行失败：{e}"

@mcp.tool()
async def kdoc_airscript_history(limit: int = 20) -> str:
    """【免密钥】获取 AirScript 执行历史。

    limit: 数量限制
    本地模式，零配置可用。"""
    try:
        from engine.airscript import get_execution_history
        result = get_execution_history(limit)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 获取历史失败：{e}"

@mcp.tool()
async def kdoc_airscript_pending() -> str:
    """【免密钥】获取待确认脚本列表。

    本地模式，零配置可用。"""
    try:
        from engine.airscript import get_pending_scripts
        result = get_pending_scripts()
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 获取待确认列表失败：{e}"


# ===========================================================================
# 三十三、多维表格字段自动化（v4.1.0 新增，公式/关联/汇总字段批量填充）
# ===========================================================================
@mcp.tool()
async def kdoc_dbf_list_field_types() -> str:
    """【免密钥】列出所有支持的字段类型。

    支持 text/number/select/date/person/link/formula/relation/rollup 等。
    本地模式，零配置可用。"""
    try:
        from engine.dbf_auto import list_field_types
        result = list_field_types()
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 列出字段类型失败：{e}"

@mcp.tool()
async def kdoc_dbf_list_formula_templates() -> str:
    """【免密钥】列出公式字段模板。

    包含 SUM/AVG/COUNT/IF/CONCAT/DATEDIF/TODAY/ROUND 等常用公式。
    本地模式，零配置可用。"""
    try:
        from engine.dbf_auto import list_formula_templates
        result = list_formula_templates()
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 列出公式模板失败：{e}"

@mcp.tool()
async def kdoc_dbf_create_field(table_id: str, field_name: str, field_type: str,
                               options: str = "", formula: str = "",
                               relation_table_id: str = "",
                               rollup_field: str = "",
                               rollup_operation: str = "") -> str:
    """【免密钥】创建字段（公式/关联/汇总/基础字段）。

    table_id: 多维表格 ID
    field_name: 字段名
    field_type: text/number/select/date/person/link/formula/relation/rollup
    options: 选项列表（JSON 数组，仅 select 需要）
    formula: 公式表达式（仅 formula 需要）
    relation_table_id: 关联表格 ID（仅 relation 需要）
    rollup_field: 汇总字段名（仅 rollup 需要）
    rollup_operation: sum/avg/count/max/min（仅 rollup 需要）
    本地模式，零配置可用。"""
    try:
        import json
        from engine.dbf_auto import create_field
        opts = json.loads(options) if options else None
        result = create_field(table_id, field_name, field_type, opts,
                              formula, relation_table_id, rollup_field, rollup_operation)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 创建字段失败：{e}"

@mcp.tool()
async def kdoc_dbf_batch_fill(table_id: str, field_name: str,
                             records: str, batch_size: int = 100) -> str:
    """【免密钥】批量填充字段值（硬件自适应削峰）。

    table_id: 多维表格 ID
    field_name: 字段名
    records: JSON 字符串（记录列表）
    batch_size: 批次大小（默认 100）
    本地模式，零配置可用。"""
    try:
        import json
        from engine.dbf_auto import batch_fill_field
        records_obj = json.loads(records)
        result = batch_fill_field(table_id, field_name, records_obj, batch_size)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 批量填充失败：{e}"

@mcp.tool()
async def kdoc_dbf_history(table_id: str = "", limit: int = 20) -> str:
    """【免密钥】获取多维表格字段自动化操作历史。

    table_id: 表格 ID（空则返回全部）
    limit: 数量限制
    本地模式，零配置可用。"""
    try:
        from engine.dbf_auto import get_dbf_history
        result = get_dbf_history(table_id, limit)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 获取历史失败：{e}"


# ===========================================================================
# 三十四、视图渲染引擎（v4.1.0 新增，看板/甘特图渲染导出）
# ===========================================================================
@mcp.tool()
async def kdoc_view_render_kanban(table_id: str = "", status_field: str = "status",
                                 title_field: str = "title",
                                 output_path: str = "") -> str:
    """【免密钥】渲染看板视图（matplotlib 柱图）。

    table_id: 多维表格 ID（空则从 data 参数获取）
    status_field: 状态字段名
    title_field: 标题字段名
    output_path: 输出图片路径（空则自动生成）
    本地模式，零配置可用。"""
    try:
        from engine.view_render import render_kanban
        # 如果没有 records，返回示例
        records = []
        if table_id:
            try:
                backend = _backend()
                result = backend.kdoc_dbt_record_query(table_id, None, 1000)
                records = json.loads(result) if isinstance(result, str) else []
            except Exception:
                records = []
        result = render_kanban(records, status_field, title_field, output_path)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 渲染看板失败：{e}"

@mcp.tool()
async def kdoc_view_render_gantt(table_id: str = "", start_field: str = "start_date",
                                end_field: str = "end_date",
                                title_field: str = "title",
                                output_path: str = "") -> str:
    """【免密钥】渲染甘特视图（mermaid 时间线）。

    table_id: 多维表格 ID
    start_field: 开始日期字段名
    end_field: 结束日期字段名
    title_field: 标题字段名
    output_path: 输出图片路径
    本地模式，零配置可用。"""
    try:
        from engine.view_render import render_gantt
        records = []
        if table_id:
            try:
                backend = _backend()
                result = backend.kdoc_dbt_record_query(table_id, None, 1000)
                records = json.loads(result) if isinstance(result, str) else []
            except Exception:
                records = []
        result = render_gantt(records, start_field, end_field, title_field, output_path)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 渲染甘特图失败：{e}"

@mcp.tool()
async def kdoc_view_render_advanced(view_type: str, data: str,
                                   config: str = "") -> str:
    """【免密钥】高级视图渲染（支持直接传入数据）。

    view_type: kanban / gantt
    data: JSON 字符串，格式 {"records": [...], "fields": [...]}
    config: JSON 字符串（可选），如 {"status_field": "状态", "output_path": "/tmp/kanban.png"}
    本地模式，零配置可用。"""
    try:
        import json
        from engine.view_render import render_view
        data_obj = json.loads(data)
        config_obj = json.loads(config) if config else None
        result = render_view(view_type, data_obj, config_obj)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 渲染失败：{e}"


# ===========================================================================
# 三十五、CRDT 表格扩展（v4.1.0 新增，单元格级无冲突协作）
# ===========================================================================
@mcp.tool()
async def kdoc_crdt_table_create(session_id: str, category: str,
                                client_id: str) -> str:
    """【免密钥】创建 CRDT 表格协同会话。

    session_id: 会话 ID
    category: sheet / smartsheet / smart_note
    client_id: 客户端标识
    本地模式，零配置可用。"""
    try:
        from engine.crdt_table import create_session
        result = create_session(session_id, category, client_id)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 创建会话失败：{e}"

@mcp.tool()
async def kdoc_crdt_table_set_cell(session_id: str, cell_id: str, value: str,
                                  client_id: str, row: int = 0, col: int = 0) -> str:
    """【免密钥】设置单元格值（单元格级操作日志+向量时钟）。

    session_id: 会话 ID
    cell_id: 单元格 ID
    value: 单元格值
    client_id: 客户端标识
    row: 行号
    col: 列号
    本地模式，零配置可用。"""
    try:
        from engine.crdt_table import set_cell
        result = set_cell(session_id, cell_id, value, client_id, row, col)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 设置单元格失败：{e}"

@mcp.tool()
async def kdoc_crdt_table_get_cell(session_id: str, cell_id: str) -> str:
    """【免密钥】获取单元格状态（含冲突信息）。

    session_id: 会话 ID
    cell_id: 单元格 ID
    本地模式，零配置可用。"""
    try:
        from engine.crdt_table import get_cell
        result = get_cell(session_id, cell_id)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 获取单元格失败：{e}"

@mcp.tool()
async def kdoc_crdt_table_resolve(session_id: str, cell_id: str,
                                 chosen_value: str, chosen_client: str = "") -> str:
    """【免密钥】解决单元格冲突。

    session_id: 会话 ID
    cell_id: 单元格 ID
    chosen_value: 选择的值
    chosen_client: 选择的客户端标识
    本地模式，零配置可用。"""
    try:
        from engine.crdt_table import resolve_conflict
        result = resolve_conflict(session_id, cell_id, chosen_value, chosen_client)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 解决冲突失败：{e}"

@mcp.tool()
async def kdoc_crdt_table_get_conflicts(session_id: str) -> str:
    """【免密钥】获取所有冲突单元格。

    session_id: 会话 ID
    本地模式，零配置可用。"""
    try:
        from engine.crdt_table import get_conflicts
        result = get_conflicts(session_id)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 获取冲突失败：{e}"

@mcp.tool()
async def kdoc_crdt_table_state(session_id: str) -> str:
    """【免密钥】获取完整表格状态。

    session_id: 会话 ID
    本地模式，零配置可用。"""
    try:
        from engine.crdt_table import get_table_state
        result = get_table_state(session_id)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 获取表格状态失败：{e}"


# ===========================================================================
# 三十六、Excel/CSV 双向导入导出（v4.1.0 新增，四类字段序列化）
# ===========================================================================
@mcp.tool()
async def kdoc_bidata_get_field_rules() -> str:
    """【免密钥】获取字段类型序列化规则文档。

    包含 date/link/select/person 四类字段的序列化规则。
    本地模式，零配置可用。"""
    try:
        from engine.bidata_io import get_field_rules
        result = get_field_rules()
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 获取规则失败：{e}"

@mcp.tool()
async def kdoc_bidata_import_csv(file_path: str, table_id: str = "",
                                field_types: str = "", batch_size: int = 100) -> str:
    """【免密钥】导入 CSV 文件（硬件自适应削峰）。

    file_path: CSV 文件路径
    table_id: 多维表格 ID（空则仅解析不写入）
    field_types: JSON 字符串，如 '{"日期": "date", "链接": "link"}'
    batch_size: 批次大小
    本地模式，零配置可用。"""
    try:
        import json
        from engine.bidata_io import import_csv
        ft = json.loads(field_types) if field_types else None
        result = import_csv(file_path, table_id, ft, batch_size)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 导入 CSV 失败：{e}"

@mcp.tool()
async def kdoc_bidata_import_excel(file_path: str, table_id: str = "",
                                  field_types: str = "", sheet_name: str = "",
                                  batch_size: int = 100) -> str:
    """【免密钥】导入 Excel 文件（openpyxl 读写）。

    file_path: Excel 文件路径
    table_id: 多维表格 ID
    field_types: JSON 字符串
    sheet_name: 工作表名（空则使用活动表）
    batch_size: 批次大小
    本地模式，零配置可用。"""
    try:
        import json
        from engine.bidata_io import import_excel
        ft = json.loads(field_types) if field_types else None
        result = import_excel(file_path, table_id, ft, sheet_name, batch_size)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 导入 Excel 失败：{e}"

@mcp.tool()
async def kdoc_bidata_export_csv(records: str, output_path: str = "",
                                field_types: str = "") -> str:
    """【免密钥】导出 CSV（支持视图级筛选快照）。

    records: JSON 字符串（记录列表）
    output_path: 输出路径（空则自动生成）
    field_types: JSON 字符串
    本地模式，零配置可用。"""
    try:
        import json
        from engine.bidata_io import export_csv
        records_obj = json.loads(records)
        ft = json.loads(field_types) if field_types else None
        result = export_csv(records_obj, output_path, ft)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 导出 CSV 失败：{e}"

@mcp.tool()
async def kdoc_bidata_export_excel(records: str, output_path: str = "",
                                  field_types: str = "") -> str:
    """【免密钥】导出 Excel（支持视图级筛选快照）。

    records: JSON 字符串（记录列表）
    output_path: 输出路径（空则自动生成）
    field_types: JSON 字符串
    本地模式，零配置可用。"""
    try:
        import json
        from engine.bidata_io import export_excel
        records_obj = json.loads(records)
        ft = json.loads(field_types) if field_types else None
        result = export_excel(records_obj, output_path, ft)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 导出 Excel 失败：{e}"


# ===========================================================================
# 三十七、Webhook 与通知中心（v4.1.0 新增，三通道分发）
# ===========================================================================
@mcp.tool()
async def kdoc_webhook_list_events() -> str:
    """【免密钥】列出所有 Webhook 事件类型。

    事件类型：record_created / record_updated / record_deleted / field_updated / table_created
    本地模式，零配置可用。"""
    try:
        from engine.webhook_center import list_event_types
        result = list_event_types()
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 列出事件类型失败：{e}"

@mcp.tool()
async def kdoc_webhook_list_channels() -> str:
    """【免密钥】列出所有通知通道。

    通道：金山协作消息 / 企业微信 / 钉钉
    本地模式，零配置可用。"""
    try:
        from engine.webhook_center import list_channels
        result = list_channels()
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 列出通道失败：{e}"

@mcp.tool()
async def kdoc_webhook_subscribe(table_id: str, event_type: str,
                                callback_url: str, channel: str,
                                webhook_key: str = "") -> str:
    """【免密钥】订阅事件（签名校验+SQLite 去重）。

    table_id: 多维表格 ID
    event_type: record_created / record_updated / record_deleted
    callback_url: 回调 URL
    channel: kdocs / wecom / dingtalk
    webhook_key: Webhook 密钥
    本地模式，零配置可用。"""
    try:
        from engine.webhook_center import subscribe
        result = subscribe(table_id, event_type, callback_url, channel, webhook_key)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 订阅失败：{e}"

@mcp.tool()
async def kdoc_webhook_unsubscribe(table_id: str, event_type: str) -> str:
    """【免密钥】取消订阅事件。

    table_id: 多维表格 ID
    event_type: 事件类型
    本地模式，零配置可用。"""
    try:
        from engine.webhook_center import unsubscribe
        result = unsubscribe(table_id, event_type)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 取消订阅失败：{e}"

@mcp.tool()
async def kdoc_webhook_list_subscriptions(table_id: str = "") -> str:
    """【免密钥】列出所有订阅。

    table_id: 多维表格 ID（空则返回全部）
    本地模式，零配置可用。"""
    try:
        from engine.webhook_center import list_subscriptions
        result = list_subscriptions(table_id)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 列出订阅失败：{e}"

@mcp.tool()
async def kdoc_webhook_process_event(payload: str, signature: str = "") -> str:
    """【免密钥】处理传入的 Webhook 事件。

    payload: JSON 字符串（事件数据）
    signature: 签名（校验用）
    本地模式，零配置可用。"""
    try:
        import json
        from engine.webhook_center import process_event
        payload_obj = json.loads(payload)
        result = process_event(payload_obj, signature)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 处理事件失败：{e}"

@mcp.tool()
async def kdoc_webhook_history(table_id: str = "", limit: int = 20) -> str:
    """【免密钥】获取事件历史。

    table_id: 多维表格 ID
    limit: 数量限制
    本地模式，零配置可用。"""
    try:
        from engine.webhook_center import get_event_history
        result = get_event_history(table_id, limit)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 获取历史失败：{e}"

@mcp.tool()
async def kdoc_webhook_statistics() -> str:
    """【免密钥】获取 Webhook 统计信息。

    本地模式，零配置可用。"""
    try:
        from engine.webhook_center import get_webhook_statistics
        result = get_webhook_statistics()
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 获取统计失败：{e}"


# ===========================================================================
# 三十八、知识中枢 / 政企合规 / 主题生成 / 跨品类对比 / OCR 桥接（v4.2.0 新增）
# ===========================================================================
@mcp.tool()
async def kdoc_khub_index(docs: str, space_id: str = "") -> str:
    """【免密钥】构建团队知识库索引（本地倒排索引）。

    docs: JSON 字符串，格式 [{"doc_id": "...", "title": "...", "content": "...", "space_id": "...", "owner": "..."}]
    space_id: 空间 ID（可选）
    硬件自适应分块建索引，零配置可用。"""
    try:
        import json
        from engine.knowledge_hub import index_documents
        docs_obj = json.loads(docs)
        result = index_documents(docs_obj, space_id)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 索引构建失败：{e}"

@mcp.tool()
async def kdoc_khub_search(query: str, space_id: str = "", limit: int = 20,
                         viewer_id: str = "") -> str:
    """【免密钥】权限感知全文检索（先鉴权后检索，无 read 权限文档不进结果）。

    query: 搜索关键词
    space_id: 空间 ID（可选）
    limit: 返回数量
    viewer_id: 查看者标识（可选，用于权限过滤）
    本地倒排索引 + 可选 jieba 中文分词，零配置可用。"""
    try:
        from engine.knowledge_hub import search_knowledge
        result = search_knowledge(query, space_id, limit, viewer_id)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 检索失败：{e}"

@mcp.tool()
async def kdoc_khub_permission(space_id: str, matrix: str) -> str:
    """【免密钥】注入空间权限矩阵（doc_id → 级别，1=read/2=edit/3=admin）。

    space_id: 空间 ID
    matrix: JSON 字符串，如 '{"doc_1": 1, "doc_2": 3}'
    检索前据此过滤，无权限文档不进入结果（遵守平台权限边界）。"""
    try:
        import json
        from engine.knowledge_hub import set_permission
        matrix_obj = json.loads(matrix)
        result = set_permission(space_id, matrix_obj)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 权限矩阵设置失败：{e}"

@mcp.tool()
async def kdoc_khub_status() -> str:
    """【免密钥】获取知识中枢状态（文档数/词项数/权限加载/jieba 状态）。"""
    try:
        from engine.knowledge_hub import get_hub_status
        return _to_text(get_hub_status())
    except Exception as e:
        return f"[ERR] 状态获取失败：{e}"

@mcp.tool()
async def kdoc_compliance_label(doc_id: str, level: str, reason: str = "") -> str:
    """【免密钥】政企合规中心：标注文档密级（公开/内部/秘密/机密）并落库。

    doc_id: 文档 ID
    level: 公开 / 内部 / 秘密 / 机密
    reason: 标注理由（可选）
    本地降级模式，零配置可用。"""
    try:
        from engine.compliance_center import label_classification
        result = label_classification(doc_id, level, reason)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 密级标注失败：{e}"

@mcp.tool()
async def kdoc_compliance_get(doc_id: str) -> str:
    """【免密钥】获取文档已标注密级。"""
    try:
        from engine.compliance_center import get_classification
        return _to_text(get_classification(doc_id))
    except Exception as e:
        return f"[ERR] 查询失败：{e}"

@mcp.tool()
async def kdoc_compliance_scan(text: str, doc_id: str = "") -> str:
    """【免密钥】政企合规全量扫描：敏感词 + 数据泄露（Luhn/校验码）+ 密级建议，聚合报告。

    text: 待扫描全文
    doc_id: 文档 ID（可选，传入则自动落库密级建议）
    复用 v3.4 合规检查，零配置可用。"""
    try:
        from engine.compliance_center import full_scan
        result = full_scan(text, doc_id)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 扫描失败：{e}"

@mcp.tool()
async def kdoc_compliance_declare(doc_id: str = "", engine: str = "tesseract") -> str:
    """【免密钥】生成数据不出域声明（本地 OCR 强制、云端仅元数据）。

    doc_id: 文档 ID（可选）
    engine: tesseract / wps_ocr（均为本地引擎，绝不调用外部 API）
    零配置可用。"""
    try:
        from engine.compliance_center import declare_data_local
        result = declare_data_local(doc_id, engine)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 声明生成失败：{e}"

@mcp.tool()
async def kdoc_compliance_status() -> str:
    """【免密钥】获取政企合规中心状态。"""
    try:
        from engine.compliance_center import get_center_status
        return _to_text(get_center_status())
    except Exception as e:
        return f"[ERR] 状态获取失败：{e}"


# ===========================================================================
# 三十九、合规套件门面 / 行业分包 / 周扫定时化 / 配额告警（v4.3.5  sanitized 分包 + 外部词包支持）
# ===========================================================================
@mcp.tool()
async def kdoc_compliance_quick_scan(
    text: str,
    packs: str = "",
    external_packs_dir: str = "",
) -> str:
    """【免密钥】合规快速扫（单入口两档·快档）：敏感词命中即报 + 数据泄露，秒级返回。

    text: 待扫描全文
    packs: 选中的行业包（逗号分隔，如 "edu,finance"）；base 通用包始终加载
    external_packs_dir: 外部词包目录（可选），企业可加载本地详细词库
    返回风险三档（高/中/低）汇总 + 命中明细（含段落行号与责任人字段）。零配置可用。"""
    try:
        import json
        from engine.compliance_suite import quick_scan
        pack_ids = [p.strip() for p in packs.split(",") if p.strip()] if packs else None
        ext = external_packs_dir or None
        return _to_text(quick_scan(text, packs=pack_ids, external_packs_dir=ext))
    except Exception as e:
        return f"[ERR] 快速扫描失败：{e}"


@mcp.tool()
async def kdoc_compliance_full(
    text: str,
    doc_id: str = "",
    include_history: str = "",
    packs: str = "",
    external_packs_dir: str = "",
) -> str:
    """【免密钥】合规全域扫（单入口两档·全档）：全文敏感词 + 数据泄露 + 格式 + 密级建议 + 历史版本时间线。

    text: 待扫描全文
    doc_id: 文档 ID（可选，传入则自动落库密级建议）
    include_history: 历史版本 JSON（可选），如 '[{"version":1,"author":"...","time":"...","content":"..."}]'
    packs: 行业包（逗号分隔，可选）
    external_packs_dir: 外部词包目录（可选），企业可加载本地详细词库
    复用 v4.3 合并后唯一引擎，零配置可用。"""
    try:
        import json
        from engine.compliance_suite import full_scan
        pack_ids = [p.strip() for p in packs.split(",") if p.strip()] if packs else None
        hist = json.loads(include_history) if include_history else None
        ext = external_packs_dir or None
        return _to_text(full_scan(text, doc_id=doc_id, include_history=hist, packs=pack_ids,
                                  external_packs_dir=ext))
    except Exception as e:
        return f"[ERR] 全域扫描失败：{e}"


@mcp.tool()
async def kdoc_compliance_packs(external_packs_dir: str = "") -> str:
    """【免密钥】列出可用行业敏感词分包（教培/医疗/金融/政务 + base 通用），含词数、责任人字段与来源。"""
    try:
        from engine.compliance_suite import list_packs
        ext = external_packs_dir or None
        return _to_text({"packs": list_packs(external_packs_dir=ext)})
    except Exception as e:
        return f"[ERR] 分包列表获取失败：{e}"


@mcp.tool()
async def kdoc_compliance_scheduler_register(
    space_id: str,
    packs: str = "",
    weekday: str = "MON",
    scan_time: str = "03:00",
    external_packs_dir: str = "",
) -> str:
    """【免密钥】注册合规周扫任务：Windows 产出 schtasks 命令；非 Windows 产出 cron 行。

    space_id: 空间 ID
    packs: 行业包（逗号分隔，可选）
    weekday: MON/TUE/...；scan_time: HH:MM
    external_packs_dir: 外部词包目录（可选）
    命令需由用户在宿主环境（管理员）执行生效。零配置可用。"""
    try:
        import json
        from engine.compliance_scheduler import register_weekly_scan
        pack_ids = [p.strip() for p in packs.split(",") if p.strip()] if packs else None
        ext = external_packs_dir or None
        return _to_text(register_weekly_scan(space_id, packs=pack_ids, weekday=weekday,
                                             scan_time=scan_time, external_packs_dir=ext))
    except Exception as e:
        return f"[ERR] 周扫注册失败：{e}"


@mcp.tool()
async def kdoc_compliance_scheduler_run(
    space_id: str,
    docs: str = "",
    packs: str = "",
    external_packs_dir: str = "",
) -> str:
    """【免密钥】执行一次全域扫描（仅推送新增，去重防扰民）。

    space_id: 空间 ID
    docs: JSON 文档列表（云端模式由 backend 拉取后传入），如 '[{"doc_id":"d1","content":"..."}]'
    packs: 行业包（逗号分隔，可选）
    external_packs_dir: 外部词包目录（可选）
    新检出项经 webhook 三通道推送（签名核验 + 跨周去重）。零配置可用。"""
    try:
        import json
        from engine.compliance_scheduler import run_scan
        pack_ids = [p.strip() for p in packs.split(",") if p.strip()] if packs else None
        doc_list = json.loads(docs) if docs else []
        ext = external_packs_dir or None
        return _to_text(run_scan(space_id, docs=doc_list, packs=pack_ids, external_packs_dir=ext))
    except Exception as e:
        return f"[ERR] 周扫执行失败：{e}"


@mcp.tool()
async def kdoc_compliance_scheduler_status(external_packs_dir: str = "") -> str:
    """【免密钥】获取合规周扫调度状态（已注册任务 + 跨周去重计数 + 外部词包目录）。"""
    try:
        from engine.compliance_scheduler import get_scheduler_status
        ext = external_packs_dir or None
        return _to_text(get_scheduler_status(external_packs_dir=ext))
    except Exception as e:
        return f"[ERR] 调度状态获取失败：{e}"

@mcp.tool()
async def kdoc_topic_generate(topic: str, outline: str, target_format: str = "doc") -> str:
    """【免密钥】主题一键生成（WPS AI 适配层 generate）：大纲 → 智能文档/PPT/表格初稿。

    topic: 主题/标题
    outline: JSON 字符串（要点列表），如 '["背景", "目标", "方案"]'
    target_format: doc / ppt / table
    本地降级：模板驱动 + 分段生成；WPS AI 真源可用时无缝切换。零配置可用。"""
    try:
        import json
        from engine.topic_generator import generate_topic
        outline_obj = json.loads(outline) if outline else []
        result = generate_topic(topic, outline_obj, target_format)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 生成失败：{e}"

@mcp.tool()
async def kdoc_topic_status() -> str:
    """【免密钥】获取主题生成适配层状态（当前生效 AI 源：local / wps_ai）。"""
    try:
        from engine.topic_generator import get_generator_status
        return _to_text(get_generator_status())
    except Exception as e:
        return f"[ERR] 状态获取失败：{e}"

@mcp.tool()
async def kdoc_compare_timeline(file_id: str = "", snapshots: str = "") -> str:
    """【免密钥】跨品类版本时间线：逐版本 difflib 生成 who/when/what。

    file_id: 文档 ID（云端模式轮询版本历史）
    snapshots: JSON 字符串（本地模式），格式 [{"version":1,"author":"...","time":"...","content":"..."}]
    文本类走行级 diff，表格类走行级 diff。零配置可用。"""
    try:
        import json
        from engine.cross_compare import build_timeline
        snaps = json.loads(snapshots) if snapshots else None
        result = build_timeline(file_id, snaps)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 时间线生成失败：{e}"

@mcp.tool()
async def kdoc_compare_cells(rows_a: str, rows_b: str, headers: str = "") -> str:
    """【免密钥】单元格级 diff（表格/多维表格品类跨版本差异）。

    rows_a: 旧版二维表 JSON
    rows_b: 新版二维表 JSON
    headers: 列名 JSON（可选）
    标注新增/修改/删除单元格，零配置可用。"""
    try:
        import json
        from engine.cross_compare import diff_cells
        a = json.loads(rows_a)
        b = json.loads(rows_b)
        h = json.loads(headers) if headers else None
        result = diff_cells(a, b, h)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 单元格 diff 失败：{e}"

@mcp.tool()
async def kdoc_ocr_bridge_status() -> str:
    """【免密钥】OCR 收敛状态：wps-office-suite OCR 是否可用、Tesseract 兜底就绪。

    v4.2 起 OCR 统一为单一入口（优先桥接 wps，未装则 Tesseract 最小兜底）。"""
    try:
        from engine.local.ocr import wps_ocr_available, tesseract_available
        return _to_text({
            "wps_ocr_available": wps_ocr_available(),
            "tesseract_available": tesseract_available(),
            "mode": "wps_bridge" if wps_ocr_available() else "tesseract_fallback",
        })
    except Exception as e:
        return f"[ERR] 状态获取失败：{e}"


# ===========================================================================
# v4.4.0 表单实时化 + 多维表格自动化工具
# ===========================================================================
@mcp.tool()
async def kdoc_form_realtime_poll(form_id: str, answers: str = "", key_fields: str = "",
                                  answer_url_template: str = "", webhook: str = "false") -> str:
    """【免密钥】答卷实时推送：轮询+增量游标检测新答卷，经 webhook 三通道推送摘要与链接。

    form_id: 表单 ID
    answers: 答卷 JSON 数组字符串（本地模式直接注入；留空则走云端 backend）
    key_fields: 摘要保留的题目 ID，逗号分隔
    answer_url_template: 答卷链接模板，支持 {form_id}/{answer_id} 占位
    webhook: true 时启用 webhook 推送（默认只落库）"""
    try:
        from engine.form_realtime import FormRealtimeEngine
        answer_list = json.loads(answers) if answers else None
        fields = [f.strip() for f in key_fields.split(",") if f.strip()] or None
        wh = None
        if webhook.lower() == "true":
            try:
                from engine.webhook_center import get_webhook_center
                wh = get_webhook_center()
            except Exception:
                wh = None
        eng = FormRealtimeEngine(webhook_center=wh)
        return _to_text(eng.poll_once(form_id, answer_list, fields, answer_url_template))
    except Exception as e:
        return f"[ERR] 答卷实时推送失败：{e}"


@mcp.tool()
async def kdoc_form_realtime_cursor(form_id: str) -> str:
    """【免密钥】查询答卷实时推送的增量游标状态。"""
    try:
        from engine.form_realtime import get_form_realtime
        return _to_text(get_form_realtime().get_cursor(form_id))
    except Exception as e:
        return f"[ERR] 游标查询失败：{e}"


@mcp.tool()
async def kdoc_form_realtime_history(form_id: str = "", limit: int = 20) -> str:
    """【免密钥】查询答卷推送历史。"""
    try:
        from engine.form_realtime import get_form_realtime
        return _to_text(get_form_realtime().get_push_history(form_id, limit))
    except Exception as e:
        return f"[ERR] 推送历史查询失败：{e}"


@mcp.tool()
async def kdoc_form_cross_add(form_id: str, form_name: str, answers: str, mapping: str) -> str:
    """【免密钥】跨表聚合：添加一张收集表及其「问题→标准字段」映射。

    answers: 答卷 JSON 数组字符串
    mapping: 映射 JSON 对象字符串，如 {"q1":"姓名","q2":"phone"}
    注：当前 session 内累积多张表后调用 kdoc_form_cross_run 聚合。"""
    return _to_text({"success": True, "hint": "请用 Python API FormCrossAnalyticsEngine.add_form 累积多表，"
                     "或一次性调用 kdoc_form_cross_aggregate 传入全部表单", "form_id": form_id})


@mcp.tool()
async def kdoc_form_cross_aggregate(forms: str, dedup_fields: str = "") -> str:
    """【免密钥】一次性跨表聚合：多张表按映射合并去重统计。

    forms: JSON 数组字符串，每项 {"form_id","form_name","answers":[...],"mapping":{...}}
    dedup_fields: 去重身份字段优先级，逗号分隔（默认 phone,mobile,email,id_card,name,wechat）"""
    try:
        from engine.form_cross_analytics import aggregate_forms
        form_list = json.loads(forms)
        fields = [f.strip() for f in dedup_fields.split(",") if f.strip()] or None
        result = aggregate_forms(form_list, fields)
        result.pop("rows", None)
        return _to_text(result)
    except Exception as e:
        return f"[ERR] 跨表聚合失败：{e}"


@mcp.tool()
async def kdoc_form_cross_dashboard(forms: str, output_path: str = "", title: str = "跨表聚合看板") -> str:
    """【免密钥】生成跨表聚合 HTML 看板（自包含离线可打开）。

    forms: JSON 数组字符串，同 kdoc_form_cross_aggregate 的 forms 参数。"""
    try:
        from engine.form_cross_analytics import render_cross_dashboard
        return _to_text(render_cross_dashboard(json.loads(forms), output_path, title))
    except Exception as e:
        return f"[ERR] 看板生成失败：{e}"


@mcp.tool()
async def kdoc_form_bidata_deposit(form_id: str, table_id: str, answers: str, field_map: str) -> str:
    """【免密钥】答卷一键沉淀多维表格行（复用四类字段序列化），person/link 双向可编辑。

    answers: 答卷 JSON 数组字符串
    field_map: JSON 对象，{"目标字段":{"question":"题ID","type":"date/link/select/person"}}"""
    try:
        from engine.form_to_bidata import deposit_answers
        return _to_text(deposit_answers(form_id, table_id, json.loads(answers), json.loads(field_map)))
    except Exception as e:
        return f"[ERR] 答卷沉淀失败：{e}"


@mcp.tool()
async def kdoc_form_bidata_update_draft(form_id: str, table_id: str, answer_id: str,
                                        updated_fields: str, field_map: str) -> str:
    """【免密钥】从多维表格行反向生成答卷更新草稿（person/link 双向可编辑）。"""
    try:
        from engine.form_to_bidata import get_form_to_bidata
        eng = get_form_to_bidata()
        return _to_text(eng.prepare_update_draft(form_id, table_id, answer_id,
                                                  json.loads(updated_fields), json.loads(field_map)))
    except Exception as e:
        return f"[ERR] 更新草稿生成失败：{e}"


@mcp.tool()
async def kdoc_form_bidata_field_rules() -> str:
    """【免密钥】查看四类字段序列化规则（date/link/select/person）与双向字段清单。"""
    try:
        from engine.form_to_bidata import field_rules
        return _to_text(field_rules())
    except Exception as e:
        return f"[ERR] 字段规则查询失败：{e}"


@mcp.tool()
async def kdoc_table_snapshot_take(table_id: str, rows: str, headers: str = "",
                                   snapshot_date: str = "", base_date: str = "",
                                   push: bool = False) -> str:
    """【免密钥】多维表格每日快照（行数+字段哈希存 SQLite），可与基线 diff。

    rows: 二维表 JSON 数组字符串
    headers: 列名 JSON 数组字符串（可选）
    base_date: 对比基线日期 YYYY-MM-DD（留空只快照）"""
    try:
        from engine.table_snapshot import get_table_snapshot
        hdrs = json.loads(headers) if headers else None
        return _to_text(get_table_snapshot().take_snapshot(
            table_id, json.loads(rows), hdrs, snapshot_date, push, base_date))
    except Exception as e:
        return f"[ERR] 快照失败：{e}"


@mcp.tool()
async def kdoc_table_snapshot_diff(table_id: str, date_a: str, date_b: str,
                                   headers: str = "") -> str:
    """【免密钥】对比两次快照，输出增/删/改行清单（谁改了我的表）。"""
    try:
        from engine.table_snapshot import diff
        hdrs = json.loads(headers) if headers else None
        return _to_text(diff(table_id, date_a, date_b, hdrs))
    except Exception as e:
        return f"[ERR] 快照 diff 失败：{e}"


@mcp.tool()
async def kdoc_table_snapshot_history(table_id: str = "", limit: int = 30) -> str:
    """【免密钥】列出表格快照历史。"""
    try:
        from engine.table_snapshot import get_table_snapshot
        return _to_text(get_table_snapshot().list_snapshots(table_id, limit))
    except Exception as e:
        return f"[ERR] 快照历史查询失败：{e}"


@mcp.tool()
async def kdoc_airscript_preset_list() -> str:
    """【免密钥】列出 AirScript 预设库全部 22 个预设（含元数据与测试样例标识）。"""
    try:
        from engine.airscript_presets import list_presets
        return _to_text(list_presets())
    except Exception as e:
        return f"[ERR] 预设列表查询失败：{e}"


@mcp.tool()
async def kdoc_airscript_preset_match(text: str) -> str:
    """【免密钥】自然语言匹配最佳 AirScript 预设（本地规则，无需 LLM）。"""
    try:
        from engine.airscript_presets import preset_from_text
        return _to_text(preset_from_text(text))
    except Exception as e:
        return f"[ERR] 预设匹配失败：{e}"


@mcp.tool()
async def kdoc_airscript_preset_generate(preset_id: str, params: str = "") -> str:
    """【免密钥】按预设生成脚本 + 测试样例 + 预期输出（走预检）。

    params: JSON 对象字符串（可选，缺省用预设的测试样例）"""
    try:
        from engine.airscript_presets import generate_from_preset
        return _to_text(generate_from_preset(preset_id, json.loads(params) if params else None))
    except Exception as e:
        return f"[ERR] 预设生成失败：{e}"


@mcp.tool()
async def kdoc_airscript_preset_validate() -> str:
    """【免密钥】校验全部预设：测试样例可生成脚本 + 预期输出非空。"""
    try:
        from engine.airscript_presets import get_preset_library
        return _to_text(get_preset_library().validate_all())
    except Exception as e:
        return f"[ERR] 预设校验失败：{e}"


@mcp.tool()
async def kdoc_crdt_viz_export(session_id: str) -> str:
    """【免密钥】导出 CRDT 会话的单元格级操作日志（含向量时钟与冲突标记）。"""
    try:
        from engine.crdt_table import get_crdt_table_engine
        from engine.crdt_visualizer import get_visualizer
        return _to_text(get_visualizer(get_crdt_table_engine()).export_operations(session_id))
    except Exception as e:
        return f"[ERR] 操作日志导出失败：{e}"


@mcp.tool()
async def kdoc_crdt_viz_visualize(session_id: str, output_path: str = "") -> str:
    """【免密钥】生成 CRDT 冲突时间线 HTML（ECharts 单文件 + SVG 离线降级）。"""
    try:
        from engine.crdt_table import get_crdt_table_engine
        from engine.crdt_visualizer import get_visualizer
        return _to_text(get_visualizer(get_crdt_table_engine()).visualize_session(session_id, output_path))
    except Exception as e:
        return f"[ERR] 冲突可视化失败：{e}"


@mcp.tool()
async def kdoc_crdt_viz_replay(operations: str, output_path: str = "") -> str:
    """【免密钥】从操作日志直接渲染时间线，还原一次真实并发编辑。

    operations: 操作日志 JSON 数组字符串"""
    try:
        from engine.crdt_visualizer import render_conflict_timeline
        return _to_text(render_conflict_timeline(json.loads(operations), output_path))
    except Exception as e:
        return f"[ERR] 时间线回放失败：{e}"


def main():
    # 兼容 setup 传入的 --config 参数（FastMCP 自身不消费，需提前剥离）
    argv = [a for a in sys.argv[1:] if not a.startswith("--config")]
    sys.argv[1:] = argv
    mcp.run()


if __name__ == "__main__":
    main()
