#!/usr/bin/env python3
"""
TDD - Test Runner

Runs tests and reports results.
"""

import subprocess
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
import time


class TestRunner:
    """Runs tests and collects results"""

    def __init__(self, root_path: str):
        self.root = Path(root_path).resolve()
        self.test_dir = self.root / 'tests'
        self.framework = self._detect_framework()

    def _detect_framework(self) -> str:
        """Detect the testing framework"""
        # Check for pytest
        if (self.root / 'pytest.ini').exists() or (self.root / 'pyproject.toml').exists():
            return 'pytest'

        # Check for tests directory structure
        if self.test_dir.exists():
            for file in self.test_dir.glob('test_*.py'):
                content = file.read_text(encoding='utf-8', errors='ignore')
                if 'import pytest' in content or 'from pytest' in content:
                    return 'pytest'
                if 'import unittest' in content:
                    return 'unittest'

        # Default to pytest
        return 'pytest'

    def run(self, target: Optional[str] = None, verbose: bool = False) -> Dict[str, Any]:
        """Run tests and return results"""
        if self.framework == 'pytest':
            return self._run_pytest(target, verbose)
        elif self.framework == 'unittest':
            return self._run_unittest(target, verbose)
        else:
            return {'success': False, 'error': f'Unknown framework: {self.framework}'}

    def _run_pytest(self, target: Optional[str], verbose: bool) -> Dict[str, Any]:
        """Run pytest"""
        cmd = ['python', '-m', 'pytest']

        if target:
            cmd.append(target)
        elif self.test_dir.exists():
            cmd.append(str(self.test_dir))

        cmd.append('-v' if verbose else '-q')
        cmd.append('--tb=short')

        # Try to get JSON output
        cmd.append('--json-report')
        cmd.append('--json-report-file=/tmp/pytest_report.json')

        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.root)
        elapsed = time.time() - start_time

        # Parse results
        passed = result.returncode == 0

        # Parse output
        output = result.stdout + result.stderr

        # Extract test counts from output
        passed_count = output.count(' PASSED')
        failed_count = output.count(' FAILED')
        error_count = output.count(' ERROR')
        skipped_count = output.count(' SKIPPED')

        # Try to read JSON report
        try:
            json_report = Path('/tmp/pytest_report.json')
            if json_report.exists():
                report_data = json.loads(json_report.read_text())
                passed_count = report_data.get('summary', {}).get('passed', passed_count)
                failed_count = report_data.get('summary', {}).get('failed', failed_count)
        except:
            pass

        total = passed_count + failed_count + error_count + skipped_count

        return {
            'success': passed and failed_count == 0,
            'framework': 'pytest',
            'passed': passed_count,
            'failed': failed_count,
            'errors': error_count,
            'skipped': skipped_count,
            'total': total,
            'time': elapsed,
            'output': output
        }

    def _run_unittest(self, target: Optional[str], verbose: bool) -> Dict[str, Any]:
        """Run unittest"""
        cmd = ['python', '-m', 'unittest']

        if target:
            cmd.append(target)
        else:
            cmd.append('discover')
            cmd.append('-s')
            cmd.append(str(self.test_dir) if self.test_dir.exists() else '.')

        if verbose:
            cmd.append('-v')

        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.root)
        elapsed = time.time() - start_time

        output = result.stdout + result.stderr

        # Parse unittest output
        passed = result.returncode == 0

        # Count tests (approximate from output)
        ok_count = output.count('... ok')
        fail_count = output.count('... FAIL')
        error_count = output.count('... ERROR')

        total = ok_count + fail_count + error_count

        return {
            'success': passed,
            'framework': 'unittest',
            'passed': ok_count,
            'failed': fail_count,
            'errors': error_count,
            'skipped': 0,
            'total': total,
            'time': elapsed,
            'output': output
        }

    def watch(self, target: Optional[str] = None) -> None:
        """Watch for changes and re-run tests"""
        print("👀 Watch mode enabled. Press Ctrl+C to stop.")
        print(f"   Monitoring: {target or self.test_dir or self.root}")
        print()

        import time
        from pathlib import Path

        last_mtime = {}

        def get_mtimes(path: Path) -> Dict[Path, float]:
            mtimes = {}
            if path.is_file():
                mtimes[path] = path.stat().st_mtime
            elif path.is_dir():
                for f in path.rglob('*.py'):
                    mtimes[f] = f.stat().st_mtime
            return mtimes

        watch_path = Path(target) if target else (self.test_dir if self.test_dir.exists() else self.root)

        # Initial run
        result = self.run(target)
        self._print_result(result)
        last_mtime = get_mtimes(watch_path)

        try:
            while True:
                time.sleep(1)

                current_mtime = get_mtimes(watch_path)

                # Check for changes
                changed = False
                for f, mtime in current_mtime.items():
                    if f not in last_mtime or last_mtime[f] != mtime:
                        changed = True
                        break

                if changed:
                    print("\n🔄 Changes detected, re-running tests...")
                    print("=" * 60)
                    result = self.run(target)
                    self._print_result(result)
                    last_mtime = current_mtime

        except KeyboardInterrupt:
            print("\n\n👋 Watch mode stopped.")

    def _print_result(self, result: Dict[str, Any]):
        """Print test results"""
        if result['success']:
            print(f"\n💚 PASSED ({result['time']:.2f}s)")
        else:
            print(f"\n🔴 FAILED ({result['time']:.2f}s)")

        print(f"   Total: {result['total']}")
        print(f"   Passed: {result['passed']}")
        print(f"   Failed: {result['failed']}")
        print(f"   Errors: {result['errors']}")

        if result.get('output') and result['failed'] > 0:
            print("\n--- Output ---")
            # Print last part of output
            output = result['output']
            lines = output.split('\n')
            print('\n'.join(lines[-30:]))  # Last 30 lines


def main():
    import argparse

    parser = argparse.ArgumentParser(description='TDD Test Runner')
    parser.add_argument('target', nargs='?', help='Test file or directory')
    parser.add_argument('--root', '-r', default='.', help='Project root')
    parser.add_argument('--watch', '-w', action='store_true', help='Watch mode')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    runner = TestRunner(args.root)
    print(f"🧪 Test Framework: {runner.framework}")

    if args.watch:
        runner.watch(args.target)
    else:
        result = runner.run(args.target, args.verbose)
        runner._print_result(result)

        # Exit with appropriate code
        sys.exit(0 if result['success'] else 1)


if __name__ == '__main__':
    main()
