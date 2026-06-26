from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from _shared import DATA_TABLES, FIXED_SPREADSHEET_TITLE, SHEET_STATE_FILE, csv_path, read_csv_matrix, read_csv_rows, utc_now, write_csv_rows

MAX_WRITE_VALUES_CHARS = 7000


def parse_lark_json_output(output: str) -> dict[str, Any]:
    text = (output or "").strip()
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise
        return json.loads(text[start : end + 1])


def spreadsheet_column_name(index: int) -> str:
    label = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        label = chr(65 + remainder) + label
    return label


def build_value_range_batches(sheet_id: str, rows: list[list[Any]]) -> list[list[dict[str, Any]]]:
    batches: list[list[dict[str, Any]]] = []
    current_batch: list[dict[str, Any]] = []
    current_rows: list[list[Any]] = []
    start_row = 1
    max_columns = 1

    def flush() -> None:
        nonlocal current_rows, start_row, max_columns, current_batch
        if not current_rows:
            return
        end_row = start_row + len(current_rows) - 1
        end_column = spreadsheet_column_name(max_columns)
        current_batch.append({"range": f"{sheet_id}!A{start_row}:{end_column}{end_row}", "values": current_rows})
        if len(current_batch) >= 10:
            batches.append(current_batch)
            current_batch = []
        current_rows = []
        max_columns = 1

    for row_index, row in enumerate(rows, start=1):
        candidate = [*current_rows, row]
        candidate_columns = max(max_columns, len(row), 1)
        if current_rows and (len(json.dumps(candidate, ensure_ascii=False)) > MAX_WRITE_VALUES_CHARS or len(candidate) > 5000):
            flush()
            start_row = row_index
            candidate = [row]
            candidate_columns = max(len(row), 1)
        current_rows = candidate
        max_columns = max(max_columns, candidate_columns)
    flush()
    if current_batch:
        batches.append(current_batch)
    return batches


class LarkSheetClient:
    def __init__(self, identity: str):
        self.identity = identity
        self.cli_command = self._resolve_lark_cli()

    def _resolve_lark_cli(self) -> str:
        for candidate in ["lark-cli", "lark-cli.cmd", "lark-cli.exe"]:
            resolved = shutil.which(candidate)
            if resolved:
                return resolved
        raise RuntimeError("Unable to locate lark-cli in PATH.")

    def _run(self, args: list[str], input_text: str | None = None) -> dict[str, Any]:
        result = subprocess.run(
            [self.cli_command, *args],
            input=input_text,
            capture_output=True,
            text=True,
            check=False,
            shell=os.name == "nt",
        )
        if result.returncode != 0:
            raise RuntimeError(result.stdout.strip() or result.stderr.strip() or "lark-cli failed")
        return parse_lark_json_output(result.stdout)

    def _api(self, method: str, path: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
        args = ["api", method.upper(), path, "--as", self.identity]
        input_text = None
        if data is not None:
            args.extend(["--data", "-"])
            input_text = json.dumps(data, ensure_ascii=False)
        payload = self._run(args, input_text=input_text)
        if payload.get("code") not in [None, 0]:
            raise RuntimeError(json.dumps(payload, ensure_ascii=False))
        return payload

    def create_spreadsheet(self, title: str, folder_token: str = "") -> dict[str, Any]:
        args = ["sheets", "+create", "--as", self.identity, "--title", title, "--headers", '["init"]', "--data", '[["init"]]']
        if folder_token:
            args.extend(["--folder-token", folder_token])
        return self._run(args).get("data", {})

    def query_sheets(self, spreadsheet_token: str) -> list[dict[str, Any]]:
        payload = self._api("GET", f"/open-apis/sheets/v3/spreadsheets/{spreadsheet_token}/sheets/query")
        return payload.get("data", {}).get("sheets", [])

    def batch_update_sheets(self, spreadsheet_token: str, requests: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not requests:
            return []
        payload = self._api("POST", f"/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/sheets_batch_update", data={"requests": requests})
        return payload.get("data", {}).get("replies", [])

    def write_value_ranges(self, spreadsheet_token: str, value_ranges: list[dict[str, Any]]) -> None:
        if value_ranges:
            self._api("POST", f"/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values_batch_update", data={"valueRanges": value_ranges})

    def replace_managed_sheets(self, spreadsheet_token: str) -> dict[str, str]:
        existing_by_title = {}
        for sheet in self.query_sheets(spreadsheet_token):
            title = sheet.get("title") or sheet.get("name")
            sheet_id = sheet.get("sheet_id") or sheet.get("sheetId") or sheet.get("id")
            if title and sheet_id:
                existing_by_title[title] = sheet_id

        new_ids: dict[str, str] = {}
        for index, table in enumerate(DATA_TABLES.values()):
            title = table["sheet_title"]
            old_id = existing_by_title.get(title)
            if old_id:
                self.batch_update_sheets(spreadsheet_token, [{"deleteSheet": {"sheetId": old_id}}])
            replies = self.batch_update_sheets(spreadsheet_token, [{"addSheet": {"properties": {"title": title, "index": index}}}])
            new_id = self._extract_added_sheet_id(replies)
            if not new_id:
                raise RuntimeError(f"未能获取新建工作表 ID：{title}")
            new_ids[title] = new_id
            print(f"  ✓ 已替换工作表 {title}: {old_id or '-'} -> {new_id}")
        return new_ids

    def mirror_csv_tables(self, spreadsheet_token: str, data_dir: Path, sheet_ids: dict[str, str]) -> dict[str, dict[str, int]]:
        stats: dict[str, dict[str, int]] = {}
        for key, table in DATA_TABLES.items():
            title = table["sheet_title"]
            path = csv_path(data_dir, key)
            if not path.exists():
                raise RuntimeError(f"缺少本地 CSV 文件：{path}")
            rows = read_csv_matrix(path)
            if rows and rows[0] != table["fields"]:
                raise RuntimeError(f"{path} 表头与 DATA_TABLES 配置不一致。")
            print(f"  → 写入 {title}: {len(rows)} 行")
            for batch in build_value_range_batches(sheet_ids[title], rows):
                self.write_value_ranges(spreadsheet_token, batch)
            stats[title] = {"rows": len(rows), "columns": len(rows[0]) if rows else len(table["fields"])}
            print(f"  ✓ {title} 已写入")
        return stats

    @staticmethod
    def _extract_added_sheet_id(replies: list[dict[str, Any]]) -> str:
        for reply in replies:
            add_sheet = reply.get("addSheet") or reply.get("add_sheet") or {}
            properties = add_sheet.get("properties") or {}
            sheet_id = properties.get("sheetId") or properties.get("sheet_id")
            if sheet_id:
                return sheet_id
        return ""


def load_sheet_state(sheet_state_file: Path = SHEET_STATE_FILE) -> dict[str, Any]:
    if not sheet_state_file.exists():
        return {}
    try:
        return json.loads(sheet_state_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_sheet_state(state: dict[str, Any], sheet_state_file: Path = SHEET_STATE_FILE) -> None:
    sheet_state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def update_last_sync_run(data_dir: Path, updates: dict[str, Any]) -> None:
    rows = read_csv_rows(csv_path(data_dir, "sync_runs"))
    if not rows:
        return
    rows[-1].update(updates)
    write_csv_rows(csv_path(data_dir, "sync_runs"), rows, DATA_TABLES["sync_runs"]["fields"])


def run_sync(data_dir: Path, identity: str, *, folder_token: str = "", sheet_state_file: Path = SHEET_STATE_FILE, title: str = FIXED_SPREADSHEET_TITLE) -> dict[str, Any]:
    client = LarkSheetClient(identity)
    state = load_sheet_state(sheet_state_file)
    spreadsheet_token = state.get("spreadsheet_token", "")
    url = state.get("url", "")

    if not spreadsheet_token:
        print("未检测到已有电子表格，创建新电子表格...")
        created = client.create_spreadsheet(title, folder_token=folder_token)
        spreadsheet_token = created.get("spreadsheet_token") or created.get("token") or created.get("spreadsheetToken")
        url = created.get("url") or created.get("spreadsheet_url") or ""
        if not spreadsheet_token:
            raise RuntimeError(f"创建电子表格成功但未返回 token: {json.dumps(created, ensure_ascii=False)}")
    else:
        print("检测到已有电子表格，替换受管工作表...")

    managed_sheets = client.replace_managed_sheets(spreadsheet_token)
    sheet_stats = client.mirror_csv_tables(spreadsheet_token, data_dir, managed_sheets)
    new_state = {
        "spreadsheet_title": title,
        "spreadsheet_token": spreadsheet_token,
        "url": url,
        "created_at": state.get("created_at") or utc_now(),
        "last_updated_at": utc_now(),
        "identity": identity,
        "managed_sheets": managed_sheets,
        "sheet_stats": sheet_stats,
    }
    save_sheet_state(new_state, sheet_state_file)
    update_last_sync_run(data_dir, {"spreadsheet_token": spreadsheet_token, "spreadsheet_url": url, "identity": identity})
    return new_state
