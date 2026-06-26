"""
Step 1：Excel 工业预处理层（核心稳定区）

批量将 input 目录中的 .xls/.xlsx 转换为 CSV，
输出到 root.yaml 同级目录下的 run_时间戳/output/csv。
并将原始文件按结果归档到 run_时间戳 目录。
"""

import argparse
import importlib
import logging
import shutil
import sys
import time
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
RUN_ID_FILE = ROOT_DIR / "current_run_id.txt"

INPUT_DIR: Path = ROOT_DIR / "input"
OUTPUT_CSV_DIR: Path = ROOT_DIR / "output" / "csv"
PROCESSED_DIR: Path = ROOT_DIR / "processed_excels"
FAILED_DIR: Path = ROOT_DIR / "failed_excels"
LOG_DIR: Path = ROOT_DIR / "logs"

SHEET_TO_PROCESS = 1
EXCEL_SUFFIXES = (".xls", ".xlsx")


def parse_sheet_arg(raw_sheet: str):
    value = raw_sheet.strip()
    if value.isdigit():
        return int(value)
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Step 1 - Excel 工业预处理层：批量将 Excel 转为 CSV"
    )
    parser.add_argument(
        "--input-dir",
        default=str(ROOT_DIR / "input"),
        help="Excel 输入目录（默认: root.yaml 同级目录下 input）",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--sheet",
        default="1",
        help="要处理的 sheet 索引(从0开始)或名称（默认: 1）",
    )
    return parser.parse_args()


def resolve_dir(raw: str, label: str) -> Path:
    target = Path(raw).expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)
    if not target.is_dir():
        raise SystemExit(f"{label}不是有效目录: {target}")
    return target


def create_run_id() -> str:
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    RUN_ID_FILE.write_text(run_id, encoding="utf-8")
    return run_id


def ensure_runtime_dirs(input_dir: Path, run_dir: Path) -> None:
    global INPUT_DIR, OUTPUT_CSV_DIR, PROCESSED_DIR, FAILED_DIR, LOG_DIR

    INPUT_DIR = input_dir
    OUTPUT_CSV_DIR = run_dir / "output" / "csv"
    PROCESSED_DIR = run_dir / "processed_excels"
    FAILED_DIR = run_dir / "failed_excels"
    LOG_DIR = run_dir / "logs"

    OUTPUT_CSV_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    FAILED_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def setup_logging(log_dir: Path) -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        log_dir / "preprocess_excel.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)


def get_excel_engine(suffix: str) -> str:
    if suffix == ".xlsx":
        try:
            importlib.import_module("openpyxl")
        except ModuleNotFoundError as exc:
            raise RuntimeError("缺少依赖 openpyxl，无法处理 .xlsx") from exc
        return "openpyxl"

    if suffix == ".xls":
        try:
            importlib.import_module("xlrd")
        except ModuleNotFoundError as exc:
            raise RuntimeError("缺少依赖 xlrd，无法处理 .xls") from exc
        return "xlrd"

    raise ValueError(f"不支持的文件类型: {suffix}")


def file_ready(p: Path, checks: int = 3, interval: float = 1.0) -> bool:
    try:
        last_size = None
        last_mtime = None
        for _ in range(checks):
            stat = p.stat()
            current_size = stat.st_size
            current_mtime = stat.st_mtime

            if last_size is None:
                last_size = current_size
                last_mtime = current_mtime
                time.sleep(interval)
                continue

            if current_size == last_size and current_mtime == last_mtime:
                with p.open("rb"):
                    return True

            last_size = current_size
            last_mtime = current_mtime
            time.sleep(interval)

        return False
    except Exception:
        return False


def convert_excel_to_csv(p: Path) -> Path:
    suffix = p.suffix.lower()
    engine = get_excel_engine(suffix)
    df = pd.read_excel(p, engine=engine, sheet_name=SHEET_TO_PROCESS)
    df = df.replace(r"^\s*$", pd.NA, regex=True)
    df = df.dropna(axis=0, how="all").dropna(axis=1, how="all")

    csv_path = OUTPUT_CSV_DIR / f"{p.stem}.csv"
    if csv_path.exists():
        csv_path = OUTPUT_CSV_DIR / f"{p.stem}_{int(time.time())}.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    return csv_path


def safe_move(src: Path, dest_dir: Path) -> Path:
    dest = dest_dir / src.name
    if dest.exists():
        dest = dest_dir / f"{src.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{src.suffix}"
    shutil.move(str(src), dest)
    return dest


def write_failure_report(file_name: str, reason: str) -> None:
    report_name = f"{Path(file_name).stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.error.txt"
    report_path = FAILED_DIR / report_name
    report_path.write_text(
        f"time: {datetime.now().isoformat()}\nfile: {file_name}\nreason: {reason}\n",
        encoding="utf-8",
    )


def quarantine_file(src: Path, reason: str) -> None:
    try:
        moved_to = safe_move(src, FAILED_DIR)
        write_failure_report(src.name, reason)
        logging.error(f"文件已隔离到失败目录: {moved_to.name} | 原因: {reason}")
    except Exception as move_error:
        logging.exception(f"失败文件隔离异常: {src.name} | {move_error}")


def process_excel_file(p: Path) -> bool:
    logging.info(f"处理文件: {p.name}")
    if not file_ready(p):
        logging.warning(f"文件未写入完成，跳过: {p.name}")
        return False

    try:
        csv_path = convert_excel_to_csv(p)
    except Exception as convert_error:
        quarantine_file(p, str(convert_error))
        return False

    try:
        safe_move(p, PROCESSED_DIR)
    except Exception as move_error:
        logging.exception(f"移动已处理文件失败: {p.name} | {move_error}")
        return False

    logging.info(f"转换完成: {p.name} -> {csv_path.name}")
    return True


def main(input_dir: Path, sheet_to_process=1) -> int:
    global SHEET_TO_PROCESS
    SHEET_TO_PROCESS = sheet_to_process

    run_id = create_run_id()
    run_dir = ROOT_DIR / f"run_{run_id}"
    ensure_runtime_dirs(input_dir, run_dir)
    setup_logging(LOG_DIR)

    logging.info("=== Step 1: Excel 工业预处理层 启动 ===")
    logging.info(f"输入目录:    {INPUT_DIR}")
    logging.info(f"运行目录:    {run_dir}")
    logging.info(f"CSV输出目录: {OUTPUT_CSV_DIR}")
    logging.info(f"处理Sheet:   {SHEET_TO_PROCESS}")
    logging.info(f"已处理归档:  {PROCESSED_DIR}")
    logging.info(f"失败隔离:    {FAILED_DIR}")

    excel_files = [
        p for p in INPUT_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in EXCEL_SUFFIXES
    ]

    if not excel_files:
        logging.info("未发现待处理的 Excel 文件，Step 1 正常结束")
        return 0

    logging.info(f"共发现 {len(excel_files)} 个 Excel 文件，开始批量处理")

    success_count = 0
    fail_count = 0

    for p in excel_files:
        ok = process_excel_file(p)
        if ok:
            success_count += 1
        else:
            fail_count += 1

    logging.info(f"=== Step 1 完成 | 成功: {success_count}，失败: {fail_count} ===")
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    args = parse_args()
    _input_dir = resolve_dir(args.input_dir, "输入目录")

    exit_code = main(
        input_dir=_input_dir,
        sheet_to_process=parse_sheet_arg(args.sheet),
    )
    sys.exit(exit_code)
