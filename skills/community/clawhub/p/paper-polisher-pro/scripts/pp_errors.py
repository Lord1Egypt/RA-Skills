#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pp_errors.py — 统一错误呈现（v6.0.0 新增）

背景（评监委 errorHandling 扣分点）：异常处理逻辑分散在各脚本，部分错误
提示偏技术化（如 zip-bomb 护栏原文直出），用户遇到非预期错误时自助定位
成本高。本模块把「技术原因 → 人话解释 → 下一步动作」收敛为一处：

    from pp_errors import render, wrap_main
    ...
    if __name__ == "__main__":
        wrap_main(main)          # 或在既有 except 分支里 print(render(e))

只改呈现，不改退出码契约（0/1/2/3 稳定承诺不变，见 SKILL.md）。
零依赖、零网络；所有已知护栏异常类在此翻译，未知异常给通用自助路径。
"""
import sys
import subprocess
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

try:
    from docx_text import DocxError
except Exception:  # docx_text 缺失时不阻塞本模块的其他职责
    DocxError = ()

_DOCTOR = "python3 scripts/pp_doctor.py 环境自检"
_GUIDE = "python3 scripts/pp_setup.py --guide 查看监督模型获取指南"
_ISSUE = "问题持续请到 GitHub 仓库（docsor1212/paper-polisher-pro）提 issue 并附本输出"


def render(exc):
    """把异常翻译为 (人话标题, 下一步动作)。未知异常给通用自助路径。"""
    s = str(exc)
    cls = type(exc).__name__

    if DocxError and isinstance(exc, DocxError) or cls == "DocxError":
        if "总量超上限" in s:
            return ("文件过大或已损坏：解压后内容超出 30MB 安全上限（防解压炸弹护栏）",
                    "正常大文档请拆分后分次检测；网页版/加密导出的文档请先用 Word/WPS "
                    "另存为标准 .docx 或导出纯文本再试")
        if "成员数超上限" in s:
            return ("文件结构异常（内部成员数超出安全上限），疑似损坏或非正常导出",
                    "用 Word/WPS 重新另存为标准 .docx，或导出纯文本后再试")
        if "PDF" in s or "图片" in s or "魔数" in s or "转存" in s:
            return (s[:120] or "输入是二进制格式（PDF/图片等），无法按文本解析",
                    "本工具只吃文本：请先把 PDF 转存为纯文本或 .docx（排版翻译场景可用 doc-holmes）")
        return (s[:140] or "Word 文档解析失败（格式不符合 .docx 规范）",
                "确认文件能被 Word/WPS 正常打开；网页/加密文档请另存为标准 .docx 或导出纯文本")
    if cls in ("BadZipFile",) or "not a zip" in s.lower() or "不是有效的 docx" in s:
        return ("不是有效的 Word 文档（.docx 实质是 ZIP 包，解包失败）",
                "确认扩展名与实际格式一致；损坏文件请用 Word/WPS 另存一次，或导出纯文本")
    if cls == "FileNotFoundError" or "不存在" in s or "not found" in s.lower():
        return ("文件不存在或路径不可达", "检查路径拼写（含空格请加引号）；本工具支持 .txt/.md/.docx")
    if cls == "IsADirectoryError" or "是一个目录" in s or "is a directory" in s.lower():
        return ("输入是一个目录而不是文件", "单文件检测请直接传文件；整目录批量用 --batch 目录")
    if cls == "PermissionError":
        return ("没有读取权限", "检查文件权限；Windows 下确认文件未被占用（关闭 Word 再试）")
    if "不足 100" in s or "100 字" in s or "insufficient" in s.lower() or "<100" in s:
        return ("文本太短，不出判定（铁律：短文本误报不可控）", "提交 100 字以上（建议 300 字以上）再检测")
    if "模型" in s and ("未安装" in s or "缺失" in s or "not installed" in s.lower()):
        return ("可选监督模型未安装（当前为降级档，功能完整但医学文本只采信 @high）",
                f"{_GUIDE}；不装模型也可正常使用")
    if "onnxruntime" in s.lower():
        return ("可选依赖 onnxruntime 未安装（监督层不可用，已自动降级）",
                f"pip install onnxruntime regex 可启用监督层；{_GUIDE}")
    if "AST" in s and ("命中" in s or "编译" in s or "网络" in s):
        return ("结构化自证发现疑似网络调用或编译错误（AST 级扫描）",
                "按输出里的 文件:行 逐条核对——报告页脚的 URL 字符串是数据不是调用；"
                "自行无法处置时到 docsor1212 仓库提 issue 附本输出")
    if "漂移" in s or "drift" in s.lower():
        return ("基线漂移：本次结果与已发布基线不一致",
                "先 python3 scripts/pp_doctor.py 查环境与档位；指纹保鲜漂移跑 "
                "python3 scripts/pp.py freshness --status；不要自行回改基线文件")
    if "REJECTED" in s or "签发注册表" in s or "不在作者签发" in s:
        return ("监督模型指纹校验未通过：不是作者签发版本",
                "重新获取当前签发版（python3 scripts/pp_setup.py --guide）；"
                "签名注册表保护的是打分可信度，请勿绕过")
    if "worker 崩溃" in s:
        return ("批处理中有一个文件让引擎进程异常崩溃——已被子进程隔离，其余文件不受影响",
                "单独跑该文件定位：python3 scripts/ai_detector.py <该文件> --format json；"
                "持续复现请到 docsor1212 仓库提 issue 附输出")
    if isinstance(exc, subprocess.TimeoutExpired) or "超时" in s or "timed out" in s.lower():
        return ("处理超时（单文件/单步超出保护时限）",
                "超长文稿请拆分后分次处理；仍复现请到 docsor1212 仓库提 issue 附 pp_doctor 输出")
    if cls == "UnicodeDecodeError" or "编码" in s or "codec" in s.lower():
        return ("文件编码不是可识别的文本（或损坏）",
                "把文件另存为 UTF-8 纯文本（记事本/VS Code 另存为都行）或转存 .docx 再试")
    if "解析失败" in s and ("层" in s or "gate" in s.lower()):
        return ("某个门禁层临时解析失败（已自动回退中性分，不影响其他层与总判定）",
                "重试一次；仍复现则 python3 scripts/pp_doctor.py 查环境")
    if isinstance(exc, ValueError):
        return (f"输入不合法：{s[:140]}", "检查输入内容与参数；契约：非法输入抛 ValueError（对应退出码 2）")
    if isinstance(exc, RuntimeError):
        hint = s if "恢复建议" in s or "doctor" in s else f"{_DOCTOR}；{s[:120]}"
        return ("运行失败（引擎或子检查异常）", hint)
    return (f"发生未预期错误：{cls}: {s[:120]}", f"{_DOCTOR}；{_ISSUE}")


def print_friendly(exc, err=True):
    """把 render 结果按两行写stderr（或 stdout），并附 FAQ 检索指针。"""
    title, nxt = render(exc)
    out = sys.stderr if err else sys.stdout
    print(f"ERROR: {title}", file=out)
    print(f"  下一步: {nxt}", file=out)
    print("  更多: python3 scripts/pp.py faq <关键词>（或查 references/faq.md）", file=out)


def wrap_main(fn, exit_codes=(0, 1, 2, 3)):
    """入口包装：main() 的未知异常不再裸 traceback，转三段式呈现（退出码 1）。

    main() 自己按契约 return 的退出码原样透传；SystemExit/KeyboardInterrupt 不拦截。
    """
    try:
        return fn()
    except SystemExit:
        raise
    except KeyboardInterrupt:
        print("已中断", file=sys.stderr)
        return 130
    except Exception as e:  # noqa: BLE001 —— 统一呈现层，契约退出码 1
        print_friendly(e)
        return 1
