"""KingDoc 本地 OCR 模块（v3.7.0 升级：强制本地，数据不出域）

v3.7.0 变更：
- 移除云端 OCR 调用路径（规则 9：数据不出域）
- 强制本地 Tesseract（免密钥、零配置）
- 硬件自适应：OCR 并发不超过 workers
- 新增：手写/公式识别场景（education 入口）

v4.2 收敛（删除重复维护面）：
- 统一为唯一 OCR 入口；公式/教育场景改为 import 本模块（删除 engine/ocr/local_ocr.py 重复预处理）
- 新增 wps-office-suite OCR 桥接：白名单探测已装则桥接其 OCR（subprocess JSON 契约 {image_path, lang}）
- 未装 wps 保留 Tesseract 最小兜底；两路均本地引擎，数据不出域
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Optional

from engine.hardware import get_recommended_settings

# 内置默认语言：中英文。用户可在调用时覆盖。
DEFAULT_LANG = "chi_sim+eng"


# ---------------------------------------------------------------------------
# v4.2：OCR 收敛 — 唯一入口，优先桥接 wps-office-suite，未装则 Tesseract 兜底
# ---------------------------------------------------------------------------
def _wps_install_path() -> Optional[str]:
    """探测 wps-office-suite 安装路径（复用本地桥接白名单）。"""
    try:
        from engine.local_bridge import WpsDetector
        return WpsDetector.detect()
    except Exception:
        return None


def wps_ocr_available() -> bool:
    """检测 wps-office-suite 是否可提供 OCR（安装即认为可用）。"""
    return _wps_install_path() is not None


def _run_wps_ocr(image_path: str, lang: str) -> Dict:
    """桥接 wps-office-suite OCR：subprocess + JSON 契约 {image_path, lang}。

    与本地桥接引擎一致：超时自动关闭，不残留；未找到 OCR 脚本降级 Tesseract。
    数据不出域：本地引擎，绝不调用外部 API。
    """
    try:
        from engine.local_bridge import WpsDetector, SUBPROCESS_TIMEOUT
        install = _wps_install_path()
        if not install:
            return _fail("wps-office-suite 未安装，降级 Tesseract。")
        scripts_dir = WpsDetector.get_scripts_dir(install)
        ocr_script = os.path.join(scripts_dir, "wps_ocr.py")
        if not os.path.exists(ocr_script):
            return _fail("wps OCR 脚本缺失，降级 Tesseract。")
        contract = json.dumps({"image_path": image_path, "lang": lang}, ensure_ascii=False)
        proc = subprocess.run(
            ["python", ocr_script, "--bridge-stdin"], input=contract,
            capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT,
        )
        if proc.returncode != 0:
            return _fail(f"wps OCR 失败：{proc.stderr[:200]}，降级 Tesseract。")
        out = json.loads(proc.stdout) if proc.stdout else {}
        return {
            "source": "wps_ocr",
            "text": out.get("text", ""),
            "confidence": out.get("confidence"),
            "engine": "wps-office-suite OCR（桥接）",
            "hint": "",
        }
    except Exception as e:
        return _fail(f"wps OCR 桥接异常：{e}，降级 Tesseract。")


def extract_text_bridged(image_path: str, lang: str = DEFAULT_LANG) -> Dict:
    """OCR 统一入口（v4.2 收敛）：优先 wps-office-suite，未装 Tesseract 最小兜底。

    两路均为本地引擎，数据不出域。
    """
    if wps_ocr_available():
        res = _run_wps_ocr(image_path, lang)
        # 桥接成功且识别到文字 → 返回；否则（脚本缺失/空识别）降级 Tesseract
        if res.get("source") == "wps_ocr" and res.get("text", "").strip():
            return res
    return extract_text(image_path, lang)


def recognize(image_path: str, lang: str = DEFAULT_LANG) -> Dict:
    """兼容 engine.ocr.local_ocr 的 recognize 形态（success/text/confidence/engine/hint）。

    v4.2 收敛：公式/教育场景统一走 engine.local.ocr，删除重复预处理代码。
    """
    res = extract_text_bridged(image_path, lang)
    return {
        "success": res.get("source") != "none",
        "text": res.get("text", ""),
        "confidence": res.get("confidence"),
        "engine": res.get("engine", ""),
        "hint": res.get("hint", ""),
    }


def tesseract_available() -> bool:
    """检测本机是否已安装 Tesseract 命令行。"""
    return shutil.which("tesseract") is not None


def get_workers() -> int:
    """获取硬件推荐的并发数（不拖累电脑）。"""
    hw = get_recommended_settings()
    return hw.get("workers", 1)


def extract_text(
    image_path: str,
    lang: str = DEFAULT_LANG,
) -> Dict:
    """提取图片文字（强制本地 Tesseract，数据不出域）。

    Returns:
        {
          "source": "tesseract" | "none",
          "text": str,
          "confidence": float | None,
          "engine": str,
          "hint": str
        }
    """
    path = Path(image_path)
    if not path.exists():
        return _fail(f"文件不存在：{image_path}")

    # 方案 1：本地 Tesseract（唯一路径，强制本地）
    if tesseract_available():
        try:
            result = _run_tesseract(image_path, lang)
            if result.get("text", "").strip():
                return {
                    "source": "tesseract",
                    "text": result["text"],
                    "confidence": result.get("confidence"),
                    "engine": f"本地 Tesseract OCR（lang={lang}）",
                    "hint": "",
                }
            return _fail(
                "Tesseract 已运行但未识别到文字（图片可能为手写体或清晰度不足）。",
                engine=f"本地 Tesseract OCR（lang={lang}）",
            )
        except Exception as e:
            return _fail(f"Tesseract 调用失败：{e}")

    # 方案 2：全部不可用，给出友好指引
    return _fail(
        "当前环境未配置任何 OCR 引擎。推荐免费方案：本地安装 Tesseract（无需任何 key）。",
        engine="未配置",
    )


def _run_tesseract(image_path: str, lang: str) -> Dict:
    """调用本地 tesseract 命令行，返回文字与平均置信度。"""
    cmd = ["tesseract", image_path, "stdout", "-l", lang]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    text = proc.stdout or ""
    confidence = None
    # 尝试用 tsv 模式拿置信度
    try:
        tsv = subprocess.run(
            ["tesseract", image_path, "stdout", "-l", lang, "tsv"],
            capture_output=True, text=True, timeout=120,
        )
        confs = []
        for line in tsv.stdout.splitlines()[1:]:
            parts = line.split("\t")
            if len(parts) > 10:
                try:
                    c = float(parts[10])
                    if c >= 0:
                        confs.append(c)
                except ValueError:
                    pass
        if confs:
            confidence = round(sum(confs) / len(confs), 1)
    except Exception:
        confidence = None
    return {"text": text, "confidence": confidence}


def _fail(msg: str, engine: str = "未配置") -> Dict:
    hint = (
        "免费安装 Tesseract（无需任何 API Key）：\n"
        "  Windows : winget install UB-Mannheim.TesseractOCR\n"
        "  macOS   : brew install tesseract tesseract-lang\n"
        "  Linux   : sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim\n"
        "安装后重启终端即可。"
    )
    return {"source": "none", "text": "", "confidence": None, "engine": engine, "hint": f"{msg}\n{hint}"}


def image_to_table(image_path: str, lang: str = DEFAULT_LANG) -> Dict:
    """图片→表格：先做 OCR，再尝试把识别结果解析为二维表。

    轻量启发式：按空行/制表符/多空格切分行列，结果供后续写入电子表格。
    """
    ocr = extract_text(image_path, lang=lang)
    if ocr["source"] == "none":
        return ocr
    rows = []
    for raw_line in ocr["text"].splitlines():
        line = raw_line.strip()
        if not line:
            continue
        # 以制表符或 2+ 空格作为列分隔
        cells = [c.strip() for c in line.replace("\t", "  ").split("  ") if c.strip()]
        if cells:
            rows.append(cells)
    return {
        **ocr,
        "rows": rows,
        "note": "表格为 OCR 启发式解析结果，复杂表格请在金山电子表格中二次校正。",
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m engine.local.ocr <image_path> [lang]")
        sys.exit(1)
    out = extract_text(sys.argv[1], lang=sys.argv[2] if len(sys.argv) > 2 else DEFAULT_LANG)
    import json
    print(json.dumps(out, ensure_ascii=False, indent=2))
