"""
Step 2：工业语义解析层（控制计划模型化）

读取 input_dir 中的 .csv 文件（由 Step 1 产出），解析为 GenProductPart JSON AST，
输出 .json 文件到 output_dir。
已处理 CSV 移入 input_dir/processed_csv，失败文件隔离到 input_dir/failed_csv。
退出码 0 全部成功，1 存在失败（供工作流 retry 机制使用）。
"""

import argparse
import json
import logging
import re
import shutil
import sys
import time
from datetime import datetime
from decimal import Decimal, InvalidOperation
from logging.handlers import RotatingFileHandler
from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
RUN_ID_FILE = ROOT_DIR / "current_run_id.txt"

# -------------------------------------------------------
# 枚举映射
# -------------------------------------------------------

EN_SOURCES = {
    "过程检验": 1,
    "入厂检验": 2,
    "出厂检验": 3,
}

EN_FREQUENCY: dict = {
    "每批": 1,
    "每年": 2,
}

EN_MEASURE: dict = {
    "计量型": 1,
    "计数型": 2,
}

EN_FEATURE: dict = {
    "SC": 2,
    "/":  1,
    "":   1,
}

EN_PLAN: dict = {
    "aql":   2,
    "fixed": 1,
}

DEFAULT_PARTVERSION = ""

# -------------------------------------------------------
# 运行时全局路径（由 ensure_runtime_dirs 初始化）
# -------------------------------------------------------
INPUT_CSV_DIR: Path  = ROOT_DIR / "output" / "csv"
OUTPUT_JSON_DIR: Path = ROOT_DIR / "output" / "json"
PROCESSED_CSV_DIR: Path = ROOT_DIR / "processed_csv"
FAILED_CSV_DIR: Path    = ROOT_DIR / "failed_csv"
LOG_DIR: Path           = ROOT_DIR / "logs"


# ═══════════════════════════════════════════════════════
# 参数 / 目录 / 日志
# ═══════════════════════════════════════════════════════

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Step 2 - CSV 语义解析层：将 CSV 解析为 JSON AST"
    )
    parser.add_argument("--input-dir",  default="./output/csv",  help="CSV 输入目录（默认: ./output/csv）")
    parser.add_argument("--output-dir", default="./output/json", help="JSON 输出目录（默认: ./output/json）")
    return parser.parse_args()


def resolve_dir(raw: str, label: str) -> Path:
    target = Path(raw).expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)
    if not target.is_dir():
        raise SystemExit(f"{label}不是有效目录: {target}")
    return target


def ensure_runtime_dirs(run_dir: Path) -> None:
    global INPUT_CSV_DIR, OUTPUT_JSON_DIR, PROCESSED_CSV_DIR, FAILED_CSV_DIR, LOG_DIR
    INPUT_CSV_DIR     = run_dir / "output" / "csv"
    OUTPUT_JSON_DIR   = run_dir / "output" / "json"
    PROCESSED_CSV_DIR = run_dir / "processed_csv"
    FAILED_CSV_DIR    = run_dir / "failed_csv"
    LOG_DIR           = run_dir / "logs"

    INPUT_CSV_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_CSV_DIR.mkdir(parents=True, exist_ok=True)
    FAILED_CSV_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def load_run_id() -> str:
    if not RUN_ID_FILE.exists():
        raise SystemExit("未找到 current_run_id.txt，请先执行 Step 1")
    run_id = RUN_ID_FILE.read_text(encoding="utf-8").strip()
    if not run_id:
        raise SystemExit("current_run_id.txt 为空，请先执行 Step 1")
    return run_id


def setup_logging(log_dir: Path) -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    fh = RotatingFileHandler(
        log_dir / "csv_to_json.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    fh.setFormatter(fmt)
    logger.addHandler(sh)
    logger.addHandler(fh)


# ═══════════════════════════════════════════════════════
# CSV 读取
# ═══════════════════════════════════════════════════════

def read_csv_as_df(p: Path) -> pd.DataFrame:
    """读取 Step 1 产出的 CSV，使用 header=None 保留原始行位置（与 Excel 解析对齐）"""
    df = pd.read_csv(
        p,
        header=None,
        dtype=str,
        keep_default_na=False,
        encoding="utf-8-sig",
    )
    return df


# ═══════════════════════════════════════════════════════
# 公差 / AQL 解析
# ═══════════════════════════════════════════════════════

def _to_float(s: str):
    try:
        return float(Decimal(str(s).strip()))
    except (InvalidOperation, ValueError, AttributeError):
        return None


def _first_number(s: str):
    m = re.search(r"-?\d+\.?\d*", str(s))
    return float(m.group()) if m else None


def parse_tolerance(spec_raw, offset_raw):
    """
    解析规范列（col5）+ 偏差列（col6），返回 (maxlimit, avglimit, minlimit, describe)
    """
    spec   = str(spec_raw).strip()   if (spec_raw   is not None and str(spec_raw)   != "nan") else ""
    offset = str(offset_raw).strip() if (offset_raw is not None and str(offset_raw) != "nan") else ""

    maxlimit = avglimit = minlimit = None

    if offset:
        nom_str = re.sub(r"[φΦ\s]", "", spec)
        nom_str = re.sub(r"[A-Za-z]+$", "", nom_str)
        nominal = _to_float(nom_str) or _first_number(spec)

        parts = re.split(r"\n|(?:\s{2,})", offset)
        parts = [p.strip() for p in parts if p.strip()]

        if len(parts) >= 2:
            upper_str, lower_str = parts[0], parts[-1]
        elif len(parts) == 1:
            upper_str = lower_str = parts[0]
        else:
            upper_str = lower_str = ""

        upper = _to_float(upper_str)
        lower = _to_float(lower_str)

        if nominal is not None and upper is not None and lower is not None:
            maxlimit = round(nominal + upper, 6)
            minlimit = round(nominal + lower, 6)
            avglimit = round((maxlimit + minlimit) / 2, 6)

        u_fmt = upper_str if upper_str else ""
        l_fmt = lower_str if lower_str else ""
        describe = f"{spec}[{u_fmt},{l_fmt}]" if (u_fmt or l_fmt) else spec
        return maxlimit, avglimit, minlimit, describe

    describe = spec
    if not spec:
        return None, None, None, describe

    m = re.match(r"^[φΦ]?\s*(-?\d+\.?\d*)\s*±\s*(\d+\.?\d*)$", spec)
    if m:
        base, tol = float(m.group(1)), float(m.group(2))
        return round(base + tol, 6), base, round(base - tol, 6), describe

    m = re.match(r"^[φΦ]?\s*(-?\d+\.?\d*)\s*max$", spec, re.IGNORECASE)
    if m:
        return float(m.group(1)), None, None, describe

    m = re.match(r"^[φΦ]?\s*(-?\d+\.?\d*)\s*min$", spec, re.IGNORECASE)
    if m:
        return None, None, float(m.group(1)), describe

    m = re.match(r"^[φΦ]?\s*(-?\d+\.?\d*)$", spec.strip())
    if m:
        return float(m.group(1)), None, None, describe

    return None, None, None, describe


def parse_aql(sample_raw):
    s = str(sample_raw).strip() if (sample_raw is not None and str(sample_raw) != "nan") else ""
    if not s or s == "/":
        return None, None, EN_PLAN["fixed"]
    m = re.search(r"AQL\s*=\s*(\d+\.?\d*)", s, re.IGNORECASE)
    if m:
        return m.group(1), None, EN_PLAN["aql"]
    m = re.match(r"(\d+)\s*件", s)
    if m:
        return None, int(m.group(1)), EN_PLAN["fixed"]
    return None, None, EN_PLAN["fixed"]


# ═══════════════════════════════════════════════════════
# 头部 / 数据行解析
# ═══════════════════════════════════════════════════════

def parse_header(df: pd.DataFrame) -> dict:
    def cell(r, c):
        try:
            v = str(df.iloc[r, c]).strip()
            return v if v not in ("", "nan") else ""
        except IndexError:
            return ""

    # Step 1 用 header=0 读 Excel 再写 CSV，row 0 在 CSV 中是原 Excel 的第 0 行（列名行），
    # 因此 header=None 读取时行偏移与原 pipeline 一致。
    partnumber    = cell(3, 1)
    partname      = cell(3, 3)
    partsuppliers = cell(5, 0)

    m_ver = re.search(r"([A-Za-z]+)$", partnumber)
    partversion = m_ver.group(1) if m_ver else DEFAULT_PARTVERSION

    return {
        "partnumber":    partnumber,
        "partname":      partname,
        "partversion":   partversion,
        "partsuppliers": partsuppliers,
        "en_source":     EN_SOURCES["入厂检验"],
    }


def _col(row, c: int, default: str = "") -> str:
    if c >= len(row):
        return default
    v = str(row.iloc[c]).strip()
    return default if v in ("", "nan") else v


def _split_nl(s: str) -> list:
    items = [x.strip() for x in str(s).split("\n") if x.strip()]
    return items if items else [str(s).strip()]


def _split_codeno(s: str) -> list:
    if "\n" in s:
        return _split_nl(s)
    if re.match(r"^\d+(?:\s+\d+)+$", s.strip()):
        return [x.strip() for x in s.strip().split() if x.strip()]
    return [s.strip()]


def _split_spec_x(spec: str) -> list:
    m = re.match(r"^(-?\d+\.?\d*)\s*[xX×]\s*(.+)$", spec.strip())
    if m:
        return [m.group(1), m.group(2).strip()]
    return [spec.strip()]


def _pad_list(lst: list, n: int) -> list:
    if not lst:
        return [""] * n
    result = list(lst)
    while len(result) < n:
        result.append(result[-1])
    return result[:n]


def parse_data_rows(df: pd.DataFrame, header_info: dict) -> list:
    """从 DataFrame（跳过前 9 行）解析检验数据行，构建 GenProductPart 列表"""
    data_df = df.iloc[9:].copy()
    data_df.columns = range(len(data_df.columns))

    data_df[0] = data_df[0].replace("", pd.NA).ffill()
    data_df[1] = data_df[1].replace("", pd.NA).ffill()

    parts = []

    for data_row_no, (_, row) in enumerate(data_df.iterrows(), start=1):
        base = dict(header_info)
        base["sort_id"] = data_row_no

        sort_str = _col(row, 0)
        try:
            base["processsort"] = int(float(sort_str)) if sort_str else 1
        except ValueError:
            base["processsort"] = 1
        base["processname"] = _col(row, 1)
        base["name"]        = _col(row, 3)

        feat_raw = _col(row, 4)
        base["en_feature"] = EN_FEATURE.get(feat_raw, EN_FEATURE.get("/", 1))

        measure_raw = _col(row, 7)
        base["en_measure"] = EN_MEASURE.get(measure_raw, EN_MEASURE.get("计数型", 2))

        aqlcode, fea_frequency, en_plan = parse_aql(row.iloc[11] if 11 < len(row) else "")
        base["aqlcode"]       = aqlcode
        base["fea_frequency"] = fea_frequency
        base["en_plan"]       = en_plan

        freq_raw = _col(row, 12)
        base["en_frequency"] = EN_FREQUENCY.get(freq_raw, EN_FREQUENCY.get("每批", 1))

        codeno_raw = _col(row, 2)
        spec_raw   = str(row.iloc[5]).strip() if 5 < len(row) else ""
        offset_raw = row.iloc[6]              if 6 < len(row) else ""
        tech_raw   = _col(row, 8)
        inst_raw   = _col(row, 9)

        if "\n" in codeno_raw or re.match(r"^\d+(?:\s+\d+)+$", codeno_raw.strip()):
            codenos = _split_codeno(codeno_raw)
            n       = len(codenos)
            specs   = _pad_list(_split_spec_x(spec_raw), n)
            techs   = _pad_list(_split_nl(tech_raw) if tech_raw else [""], n)
            insts   = _pad_list(_split_nl(inst_raw) if inst_raw else [""], n)
            offsets = [""] * n
        else:
            codenos = [codeno_raw]
            specs   = [spec_raw]
            offsets = [offset_raw]
            techs   = [tech_raw]
            insts   = [inst_raw]

        for i, codeno in enumerate(codenos):
            part = dict(base)
            part["codeno"] = codeno

            maxlimit, avglimit, minlimit, describe = parse_tolerance(specs[i], offsets[i])
            part["describe"]  = describe if describe else None
            part["maxlimit"]  = maxlimit
            part["avglimit"]  = avglimit
            part["minlimit"]  = minlimit

            part["technology"]     = techs[i] or None
            part["instrumentname"] = insts[i] or None

            part = {k: v for k, v in part.items() if v is not None}
            parts.append(part)

    return parts


# ═══════════════════════════════════════════════════════
# 文件管理
# ═══════════════════════════════════════════════════════

def safe_move(src: Path, dest_dir: Path) -> Path:
    dest = dest_dir / src.name
    if dest.exists():
        dest = dest_dir / f"{src.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{src.suffix}"
    shutil.move(str(src), dest)
    return dest


def quarantine_file(src: Path, reason: str) -> None:
    try:
        moved = safe_move(src, FAILED_CSV_DIR)
        report = FAILED_CSV_DIR / f"{src.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.error.txt"
        report.write_text(
            f"time: {datetime.now().isoformat()}\nfile: {src.name}\nreason: {reason}\n",
            encoding="utf-8",
        )
        logging.error(f"CSV 已隔离: {moved.name} | 原因: {reason}")
    except Exception as e:
        logging.exception(f"隔离失败: {src.name} | {e}")


# ═══════════════════════════════════════════════════════
# 单文件处理
# ═══════════════════════════════════════════════════════

def process_csv_file(p: Path) -> bool:
    """解析单个 CSV 文件，返回 True 表示成功"""
    logging.info(f"解析文件: {p.name}")

    try:
        df = read_csv_as_df(p)
    except Exception as e:
        quarantine_file(p, f"读取CSV失败: {e}")
        return False

    try:
        header_info = parse_header(df)
        if not header_info.get("partnumber"):
            raise ValueError("未找到有效零件号（partnumber），请检查 CSV 格式")
        parts = parse_data_rows(df, header_info)
        logging.info(
            f"{p.name} | 零件号: {header_info['partnumber']} "
            f"| 名称: {header_info['partname']} | 共 {len(parts)} 条检验项"
        )
    except Exception as e:
        quarantine_file(p, f"解析失败: {e}")
        return False

    # 写出 JSON AST
    json_path = OUTPUT_JSON_DIR / f"{p.stem}.json"
    if json_path.exists():
        json_path = OUTPUT_JSON_DIR / f"{p.stem}_{int(time.time())}.json"
    try:
        json_path.write_text(
            json.dumps(parts, ensure_ascii=False, indent=2, default=str),
            encoding="utf-8",
        )
    except Exception as e:
        quarantine_file(p, f"写出JSON失败: {e}")
        return False

    try:
        safe_move(p, PROCESSED_CSV_DIR)
    except Exception as e:
        logging.exception(f"归档CSV失败: {p.name} | {e}")
        return False

    logging.info(f"输出 JSON: {json_path.name}")
    return True


# ═══════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════

def main() -> int:
    run_id = load_run_id()
    run_dir = ROOT_DIR / f"run_{run_id}"
    ensure_runtime_dirs(run_dir)
    setup_logging(LOG_DIR)

    logging.info("=== Step 2: CSV 语义解析层 启动 ===")
    logging.info(f"运行目录:     {run_dir}")
    logging.info(f"CSV 输入目录:  {INPUT_CSV_DIR}")
    logging.info(f"JSON 输出目录: {OUTPUT_JSON_DIR}")

    csv_files = [p for p in INPUT_CSV_DIR.iterdir() if p.is_file() and p.suffix.lower() == ".csv"]

    if not csv_files:
        logging.info("未发现待处理的 CSV 文件，Step 2 正常结束")
        return 0

    logging.info(f"共发现 {len(csv_files)} 个 CSV 文件，开始批量解析")

    success_count = fail_count = 0
    for p in csv_files:
        if process_csv_file(p):
            success_count += 1
        else:
            fail_count += 1

    logging.info(f"=== Step 2 完成 | 成功: {success_count}，失败: {fail_count} ===")
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    parse_args()
    sys.exit(main())
