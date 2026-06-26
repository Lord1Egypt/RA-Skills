from __future__ import annotations

import argparse
import ctypes
import json
import os
import subprocess
import sys
import threading
import time
from ctypes import wintypes
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Optional

SUPPORTED_EXTENSIONS = ('.hwp', '.hwpx')
DOCUMENT_LOAD_DELAY = 1.0
MAX_FILENAME_COUNTER = 1000
HWP_PROGIDS = [
    'HWPControl.HwpCtrl.1',
    'HwpObject.HwpObject',
    'HWPFrame.HwpObject',
]
FORMAT_TYPES: dict[str, dict[str, str]] = {
    'HWP': {'ext': '.hwp', 'save_format': 'HWP'},
    'HWPX': {'ext': '.hwpx', 'save_format': 'HWPX'},
    'PDF': {'ext': '.pdf', 'save_format': 'PDF'},
    'DOCX': {'ext': '.docx', 'save_format': 'OOXML'},
    'ODT': {'ext': '.odt', 'save_format': 'ODT'},
    'HTML': {'ext': '.html', 'save_format': 'HTML'},
    'RTF': {'ext': '.rtf', 'save_format': 'RTF'},
    'TXT': {'ext': '.txt', 'save_format': 'TEXT'},
    'PNG': {'ext': '.png', 'save_format': 'PNG'},
    'JPG': {'ext': '.jpg', 'save_format': 'JPG'},
    'BMP': {'ext': '.bmp', 'save_format': 'BMP'},
    'GIF': {'ext': '.gif', 'save_format': 'GIF'},
}
HWP_PROCESS_NAMES = {'hwp.exe', 'hwpctrl.exe'}
DIALOG_TITLE_WHITELIST = {'한글'}
DIALOG_TEXT_KEYWORDS = ('접근하려는 시도',)
DIALOG_ALLOW_BUTTONS = ('모두 허용', '허용')
POLL_INTERVAL_SECONDS = 0.35
WINDOW_SCAN_TIMEOUT_SECONDS = 3.0
BM_CLICK = 0x00F5
WM_GETTEXT = 0x000D
WM_GETTEXTLENGTH = 0x000E


USER32 = ctypes.WinDLL('user32', use_last_error=True)


@dataclass
class AutoDialogEvent:
    window_title: str
    window_text: str
    button_text: str
    clicked: bool
    reason: str
    timestamp: float = field(default_factory=time.time)

    def to_record(self) -> dict[str, Any]:
        return {
            'timestamp': round(self.timestamp, 3),
            'window_title': self.window_title,
            'window_text': self.window_text,
            'button_text': self.button_text,
            'clicked': self.clicked,
            'reason': self.reason,
        }


def canonicalize_path(path: str | Path) -> str:
    return os.path.abspath(os.path.normpath(str(path)))


def iter_supported_files(root_path: Path, include_sub: bool = True, allowed_exts: Optional[Iterable[str]] = None) -> Iterable[Path]:
    allowed = {ext.lower() for ext in (allowed_exts or SUPPORTED_EXTENSIONS)}
    if root_path.is_file():
        if root_path.suffix.lower() in allowed:
            yield root_path
        return
    if not root_path.is_dir():
        return
    if include_sub:
        for dirpath, _, filenames in os.walk(root_path):
            for filename in filenames:
                _, ext = os.path.splitext(filename)
                if ext.lower() in allowed:
                    yield Path(dirpath) / filename
        return
    with os.scandir(root_path) as entries:
        for entry in entries:
            if not entry.is_file():
                continue
            _, ext = os.path.splitext(entry.name)
            if ext.lower() in allowed:
                yield Path(entry.path)


@dataclass
class ConversionTask:
    input_file: Path
    output_file: Path
    status: str = '대기'
    error: str | None = None

    def to_record(self) -> dict[str, str]:
        return {
            'input_file': str(self.input_file),
            'output_file': str(self.output_file),
            'status': self.status,
            'detail': self.error or '',
        }


@dataclass
class PlannedConversion:
    format_type: str
    same_location: bool
    output_path: str
    tasks: list[ConversionTask] = field(default_factory=list)
    skipped_tasks: list[ConversionTask] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    conflict_renamed_count: int = 0


@dataclass
class ConversionSummary:
    format_type: str
    tasks: list[ConversionTask] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    elapsed_seconds: float | None = None
    progid_used: str | None = None
    mode: str = 'real'
    auto_dialog_enabled: bool = False
    auto_dialog_events: list[AutoDialogEvent] = field(default_factory=list)

    def to_json_dict(self) -> dict[str, Any]:
        success = len([task for task in self.tasks if task.status == '성공'])
        failed = len([task for task in self.tasks if task.status == '실패'])
        skipped = len([task for task in self.tasks if task.status == '건너뜀'])
        clicked = len([event for event in self.auto_dialog_events if event.clicked])
        detected = len(self.auto_dialog_events)
        return {
            'summary': {
                'format_type': self.format_type,
                'mode': self.mode,
                'total_requested': len(self.tasks),
                'success_count': success,
                'failed_count': failed,
                'skipped_count': skipped,
                'elapsed_seconds': self.elapsed_seconds,
                'progid_used': self.progid_used,
                'warnings': self.warnings,
                'auto_dialog_enabled': self.auto_dialog_enabled,
                'auto_dialog_detected_count': detected,
                'auto_dialog_clicked_count': clicked,
            },
            'tasks': [task.to_record() for task in sorted(self.tasks, key=lambda t: str(t.input_file).lower())],
            'auto_dialog_events': [event.to_record() for event in self.auto_dialog_events],
        }


class TaskPlanner:
    def build_tasks(
        self,
        *,
        sources: list[str],
        format_type: str,
        include_sub: bool,
        same_location: bool,
        output_path: str,
    ) -> PlannedConversion:
        tasks: list[ConversionTask] = []
        skipped: list[ConversionTask] = []
        warnings: list[str] = []
        out_ext = FORMAT_TYPES[format_type]['ext']

        if not sources:
            raise ValueError('파일 또는 폴더를 하나 이상 지정하세요.')

        normalized_sources = [Path(canonicalize_path(src)) for src in sources]
        multiple_sources = len(normalized_sources) > 1
        explicit_output_root = Path(canonicalize_path(output_path)) if output_path else None

        for source in normalized_sources:
            if not source.exists():
                raise ValueError(f'입력 경로가 존재하지 않습니다: {source}')
            source_files = sorted(iter_supported_files(source, include_sub=include_sub), key=lambda p: str(p).lower())
            if not source_files and source.is_dir():
                warnings.append(f'지원 파일이 없는 폴더를 건너뜀: {source}')
            for input_file in source_files:
                if input_file.suffix.lower() == out_ext.lower():
                    skipped.append(ConversionTask(input_file, input_file, status='건너뜀', error=f'이미 {format_type} 형식입니다.'))
                    continue
                if same_location:
                    output_file = input_file.parent / (input_file.stem + out_ext)
                else:
                    if explicit_output_root is None:
                        raise ValueError('--output-dir 또는 --same-location 중 하나가 필요합니다.')
                    if source.is_file() or multiple_sources:
                        base_dir = explicit_output_root
                        output_file = base_dir / (input_file.stem + out_ext)
                    else:
                        rel_path = input_file.relative_to(source)
                        output_file = explicit_output_root / rel_path.parent / (input_file.stem + out_ext)
                tasks.append(ConversionTask(input_file=input_file, output_file=output_file))

        if skipped:
            warnings.append(f'동일 형식 {len(skipped)}개는 자동으로 건너뜁니다.')
        return PlannedConversion(format_type=format_type, same_location=same_location, output_path=output_path, tasks=tasks, skipped_tasks=skipped, warnings=warnings)

    def resolve_output_conflicts(self, tasks: list[ConversionTask], overwrite: bool) -> int:
        if overwrite:
            return 0
        used_paths: set[Path] = set()
        renamed_count = 0
        for task in tasks:
            original_path = task.output_file
            if task.output_file.exists() or task.output_file in used_paths:
                counter = 1
                stem = original_path.stem
                ext = original_path.suffix
                parent = original_path.parent
                while counter <= MAX_FILENAME_COUNTER:
                    candidate = parent / f'{stem} ({counter}){ext}'
                    if (not candidate.exists()) and (candidate not in used_paths):
                        task.output_file = candidate
                        break
                    counter += 1
                if task.output_file == original_path:
                    task.output_file = parent / f'{stem}_{int(time.time())}{ext}'
                if task.output_file != original_path:
                    renamed_count += 1
            used_paths.add(task.output_file)
        return renamed_count


class MockConverter:
    def __init__(self) -> None:
        self.progid_used = 'mock'

    def initialize(self) -> bool:
        return True

    def convert_file(self, input_path: Path, output_path: Path, format_type: str = 'PDF'):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        source_name = Path(input_path).name
        payload = f'mock-converted:{source_name}->{format_type}\n'
        output_path.write_text(payload, encoding='utf-8')
        return True, None

    def cleanup(self) -> None:
        return None


def _snapshot_hwp_pids() -> set[int]:
    try:
        result = subprocess.run(['tasklist', '/FO', 'CSV', '/NH'], capture_output=True, text=True, encoding='utf-8', errors='ignore', check=False)
        if result.returncode != 0:
            return set()
        import csv
        import io
        reader = csv.reader(io.StringIO(result.stdout))
        pids: set[int] = set()
        for row in reader:
            if len(row) < 2:
                continue
            image_name = row[0].strip().lower()
            if image_name not in HWP_PROCESS_NAMES:
                continue
            try:
                pids.add(int(row[1]))
            except ValueError:
                pass
        return pids
    except Exception:
        return set()


def _get_window_text(hwnd: int) -> str:
    length = USER32.SendMessageW(hwnd, WM_GETTEXTLENGTH, 0, 0)
    if length <= 0:
        return ''
    buffer = ctypes.create_unicode_buffer(length + 1)
    USER32.SendMessageW(hwnd, WM_GETTEXT, length + 1, ctypes.byref(buffer))
    return buffer.value.strip()


def _get_class_name(hwnd: int) -> str:
    buffer = ctypes.create_unicode_buffer(256)
    USER32.GetClassNameW(hwnd, buffer, 256)
    return buffer.value


class AutoAllowDialogWatcher:
    def __init__(self, *, enabled: bool = False, poll_interval: float = POLL_INTERVAL_SECONDS) -> None:
        self.enabled = enabled
        self.poll_interval = poll_interval
        self.events: list[AutoDialogEvent] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._handled_hwnds: set[int] = set()

    def start(self) -> None:
        if not self.enabled:
            return
        self._thread = threading.Thread(target=self._run, name='hwp-auto-allow-dialogs', daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=2.0)

    def snapshot_events(self) -> list[AutoDialogEvent]:
        with self._lock:
            return list(self.events)

    def click_once_for_test(self, timeout_seconds: float = WINDOW_SCAN_TIMEOUT_SECONDS) -> bool:
        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            if self._scan_once():
                return True
            time.sleep(self.poll_interval)
        return False

    def _run(self) -> None:
        while not self._stop_event.wait(self.poll_interval):
            self._scan_once()

    def _scan_once(self) -> bool:
        matched = False
        hwnds: list[int] = []

        enum_proc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)(lambda hwnd, lparam: hwnds.append(hwnd) or True)
        USER32.EnumWindows(enum_proc, 0)

        for hwnd in hwnds:
            if hwnd in self._handled_hwnds or not USER32.IsWindowVisible(hwnd):
                continue
            title = USER32.GetWindowTextLengthW(hwnd)
            if title <= 0:
                continue
            window_title = ctypes.create_unicode_buffer(title + 1)
            USER32.GetWindowTextW(hwnd, window_title, title + 1)
            if window_title.value.strip() not in DIALOG_TITLE_WHITELIST:
                continue
            text_parts, allow_button_hwnd, allow_button_text = self._inspect_dialog(hwnd)
            window_text = ' '.join(part for part in text_parts if part).strip()
            reason = self._classify_candidate(window_title.value.strip(), window_text, allow_button_text)
            if reason != 'match':
                if window_text:
                    self._record_event(AutoDialogEvent(window_title=window_title.value.strip(), window_text=window_text, button_text=allow_button_text, clicked=False, reason=reason))
                    self._handled_hwnds.add(hwnd)
                continue
            clicked = False
            if allow_button_hwnd:
                USER32.SendMessageW(allow_button_hwnd, BM_CLICK, 0, 0)
                clicked = True
            self._record_event(AutoDialogEvent(window_title=window_title.value.strip(), window_text=window_text, button_text=allow_button_text, clicked=clicked, reason='clicked' if clicked else 'allow-button-not-found'))
            self._handled_hwnds.add(hwnd)
            matched = matched or clicked
        return matched

    def _inspect_dialog(self, hwnd: int) -> tuple[list[str], int | None, str]:
        parts: list[str] = []
        allow_button_hwnd: int | None = None
        allow_button_text = ''
        child_hwnds: list[int] = []
        enum_proc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)(lambda child, lparam: child_hwnds.append(child) or True)
        USER32.EnumChildWindows(hwnd, enum_proc, 0)
        for child in child_hwnds:
            text = _get_window_text(child)
            class_name = _get_class_name(child)
            if text:
                parts.append(text)
            if 'BUTTON' in class_name.upper() and text in DIALOG_ALLOW_BUTTONS and allow_button_hwnd is None:
                allow_button_hwnd = child
                allow_button_text = text
        return parts, allow_button_hwnd, allow_button_text

    def _classify_candidate(self, title: str, window_text: str, allow_button_text: str) -> str:
        if title not in DIALOG_TITLE_WHITELIST:
            return 'title-mismatch'
        if not all(keyword in window_text for keyword in DIALOG_TEXT_KEYWORDS):
            return 'text-mismatch'
        if not allow_button_text:
            return 'button-mismatch'
        return 'match'

    def _record_event(self, event: AutoDialogEvent) -> None:
        with self._lock:
            self.events.append(event)


class RealHwpConverter:
    def __init__(self) -> None:
        self.hwp = None
        self.progid_used: str | None = None
        self.is_initialized = False
        self.owned_pids: set[int] = set()

    def initialize(self) -> bool:
        if self.is_initialized:
            return True
        try:
            import pythoncom
            from win32com import client as win32_client
        except ImportError as exc:
            raise RuntimeError('pywin32가 필요합니다. `pip install pywin32` 후 다시 실행하세요.') from exc
        try:
            pythoncom.CoInitialize()
        except Exception:
            pass
        errors: list[str] = []
        for progid in HWP_PROGIDS:
            before_pids = _snapshot_hwp_pids()
            try:
                self.hwp = win32_client.Dispatch(progid)
                self.progid_used = progid
                try:
                    self.hwp.RegisterModule('FilePathCheckDLL', 'FilePathCheckerModuleExample')
                except Exception:
                    pass
                self.hwp.SetMessageBoxMode(0x00000001)
                time.sleep(0.2)
                self.owned_pids = _snapshot_hwp_pids() - before_pids
                self.is_initialized = True
                return True
            except Exception as exc:
                errors.append(f'{progid}: {exc}')
        raise RuntimeError('한글 COM 객체 생성 실패\n' + '\n'.join(errors))

    def convert_file(self, input_path: Path, output_path: Path, format_type: str = 'PDF'):
        if not self.is_initialized or self.hwp is None:
            return False, '한글 객체가 초기화되지 않았습니다.'
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            self.hwp.Open(str(input_path), '', 'forceopen:true')
            time.sleep(DOCUMENT_LOAD_DELAY)
            save_format = FORMAT_TYPES[format_type]['save_format']
            try:
                self.hwp.SaveAs(str(output_path), save_format)
            except Exception:
                self.hwp.SaveAs(str(output_path), save_format, '')
            self.hwp.Clear(option=1)
            return True, None
        except Exception as exc:
            try:
                self.hwp.Clear(option=1)
            except Exception:
                pass
            return False, str(exc)

    def cleanup(self) -> None:
        if self.hwp is not None and self.is_initialized:
            try:
                self.hwp.Clear(3)
            except Exception:
                pass
            try:
                self.hwp.Quit()
            except Exception:
                pass
            self.hwp = None
            self.is_initialized = False


def choose_converter(mode: str):
    if mode == 'mock':
        return MockConverter()
    return RealHwpConverter()


def render_human(summary: ConversionSummary) -> str:
    data = summary.to_json_dict()['summary']
    lines = [
        f"형식: {data['format_type']} ({data['mode']})",
        f"총 {data['total_requested']}건 | 성공 {data['success_count']} | 실패 {data['failed_count']} | 건너뜀 {data['skipped_count']}",
    ]
    if data['warnings']:
        lines.append('경고: ' + ' / '.join(data['warnings']))
    if summary.auto_dialog_enabled:
        lines.append(f"보안 팝업 자동 허용: 감지 {data['auto_dialog_detected_count']} | 클릭 {data['auto_dialog_clicked_count']}")
    failed = [task for task in summary.tasks if task.status == '실패']
    if failed:
        lines.append('실패 목록:')
        for task in failed[:10]:
            lines.append(f'- {task.input_file.name}: {task.error}')
    return '\n'.join(lines)


def run_conversion(args: argparse.Namespace) -> ConversionSummary:
    planner = TaskPlanner()
    plan = planner.build_tasks(
        sources=args.sources,
        format_type=args.format,
        include_sub=args.include_sub,
        same_location=args.same_location,
        output_path=args.output_dir or '',
    )
    plan.conflict_renamed_count = planner.resolve_output_conflicts(plan.tasks, overwrite=args.overwrite)
    if plan.conflict_renamed_count:
        plan.warnings.append(f'출력 파일 충돌 {plan.conflict_renamed_count}건은 자동으로 새 이름을 부여했습니다.')
    all_tasks = list(plan.skipped_tasks)
    start = time.time()

    if args.plan_only:
        for task in plan.tasks:
            task.status = '계획됨'
        all_tasks.extend(plan.tasks)
        return ConversionSummary(format_type=args.format, tasks=all_tasks, warnings=plan.warnings, elapsed_seconds=round(time.time() - start, 3), mode='plan', auto_dialog_enabled=args.auto_allow_dialogs)

    converter = choose_converter(args.mode)
    dialog_watcher = AutoAllowDialogWatcher(enabled=args.auto_allow_dialogs and args.mode == 'real')
    converter.initialize()
    dialog_watcher.start()
    try:
        for task in plan.tasks:
            ok, error = converter.convert_file(task.input_file, task.output_file, args.format)
            task.status = '성공' if ok else '실패'
            task.error = error
            all_tasks.append(task)
    finally:
        dialog_watcher.stop()
        converter.cleanup()

    dialog_events = dialog_watcher.snapshot_events()
    if args.auto_allow_dialogs and args.mode != 'real':
        plan.warnings.append('--auto-allow-dialogs 는 real 모드에서만 실제 동작합니다.')
    if dialog_events:
        clicked = len([event for event in dialog_events if event.clicked])
        plan.warnings.append(f'보안 팝업 자동 허용 기록: 감지 {len(dialog_events)}건, 클릭 {clicked}건')

    return ConversionSummary(
        format_type=args.format,
        tasks=all_tasks,
        warnings=plan.warnings,
        elapsed_seconds=round(time.time() - start, 3),
        progid_used=getattr(converter, 'progid_used', None),
        mode=args.mode,
        auto_dialog_enabled=args.auto_allow_dialogs,
        auto_dialog_events=dialog_events,
    )


def run_dialog_self_test(timeout_seconds: float = 8.0) -> dict[str, Any]:
    dialog_script = r"""
Add-Type -AssemblyName System.Windows.Forms
$form = New-Object System.Windows.Forms.Form
$form.Text = '한글'
$form.Width = 420
$form.Height = 170
$form.StartPosition = 'CenterScreen'
$label = New-Object System.Windows.Forms.Label
$label.AutoSize = $true
$label.Left = 20
$label.Top = 20
$label.Text = '한글 문서에 접근하려는 시도를 허용하시겠습니까?'
$form.Controls.Add($label)
$button = New-Object System.Windows.Forms.Button
$button.Text = '모두 허용'
$button.Left = 20
$button.Top = 70
$button.Width = 100
$button.DialogResult = [System.Windows.Forms.DialogResult]::OK
$form.AcceptButton = $button
$form.Controls.Add($button)
[void]$form.ShowDialog()
""".strip()
    watcher = AutoAllowDialogWatcher(enabled=True, poll_interval=0.2)
    proc = subprocess.Popen(['powershell', '-NoProfile', '-STA', '-Command', dialog_script])
    try:
        clicked = watcher.click_once_for_test(timeout_seconds=timeout_seconds)
        proc.wait(timeout=timeout_seconds)
        events = watcher.snapshot_events()
        return {
            'clicked': clicked,
            'returncode': proc.returncode,
            'events': [event.to_record() for event in events],
        }
    finally:
        if proc.poll() is None:
            proc.kill()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='한글(HWP/HWPX) 문서를 PDF/DOCX/HWPX 등으로 일괄 변환합니다.')
    parser.add_argument('sources', nargs='*', help='입력 파일 또는 폴더 경로(여러 개 가능)')
    parser.add_argument('--format', default='PDF', choices=sorted(FORMAT_TYPES.keys()), help='출력 형식')
    parser.add_argument('--include-sub', action='store_true', default=True, help='하위 폴더 포함(기본값: 켜짐)')
    parser.add_argument('--no-include-sub', dest='include_sub', action='store_false', help='하위 폴더 미포함')
    parser.add_argument('--same-location', action='store_true', default=False, help='원본과 같은 폴더에 출력')
    parser.add_argument('--output-dir', help='출력 루트 폴더')
    parser.add_argument('--overwrite', action='store_true', help='같은 이름 출력 파일 덮어쓰기 허용')
    parser.add_argument('--plan-only', action='store_true', help='실제 변환 없이 작업 계획만 출력')
    parser.add_argument('--mode', choices=['real', 'mock'], default='real', help='real=한글 COM 실변환, mock=테스트용 가짜 변환')
    parser.add_argument('--auto-allow-dialogs', action='store_true', help='한글 보안 확인 팝업(제목=한글, 본문에 접근하려는 시도, 버튼=모두 허용)만 자동 클릭')
    parser.add_argument('--json', action='store_true', help='JSON 출력')
    parser.add_argument('--report-json', help='결과 JSON 파일 저장 경로')
    parser.add_argument('--self-test-dialog-handler', action='store_true', help='보안 팝업 자동 클릭 로직의 로컬 UI 테스트를 실행')
    args = parser.parse_args()
    if args.self_test_dialog_handler:
        return args
    if not args.sources:
        parser.error('입력 파일 또는 폴더를 하나 이상 지정하세요.')
    if not args.same_location and not args.output_dir:
        parser.error('--same-location 또는 --output-dir 중 하나를 지정하세요.')
    return args


def main() -> int:
    args = parse_args()
    try:
        if args.self_test_dialog_handler:
            payload = run_dialog_self_test()
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 0 if payload['clicked'] and payload['returncode'] == 0 else 1
        summary = run_conversion(args)
    except Exception as exc:
        error_payload = {'error': str(exc)}
        if getattr(args, 'json', False):
            print(json.dumps(error_payload, ensure_ascii=False, indent=2))
        else:
            print(f'오류: {exc}', file=sys.stderr)
        return 1
    payload = summary.to_json_dict()
    if args.report_json:
        report_path = Path(args.report_json)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_human(summary))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
