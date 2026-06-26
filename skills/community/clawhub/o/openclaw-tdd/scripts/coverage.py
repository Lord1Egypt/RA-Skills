#!/usr/bin/env python3
"""
TDD - Coverage Tracker

Tracks and reports test coverage.
"""

import subprocess
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any


class CoverageTracker:
    """Tracks test coverage"""

    def __init__(self, root_path: str):
        self.root = Path(root_path).resolve()

    def run_coverage(self, source_dir: Optional[str] = None) -> Dict[str, Any]:
        """Run coverage analysis"""
        source = source_dir or 'src'

        # Run pytest with coverage
        cmd = [
            'python', '-m', 'pytest',
            '--cov=' + source,
            '--cov-report=term-missing',
            '--cov-report=json:/tmp/coverage.json',
            '-q'
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.root)

        # Parse terminal output
        output = result.stdout + result.stderr

        # Extract coverage percentage
        coverage_match = re.search(r'TOTAL\s+\d+\s+\d+\s+(\d+)%', output)
        total_coverage = int(coverage_match.group(1)) if coverage_match else 0

        # Parse JSON report
        file_coverages = {}
        try:
            json_path = Path('/tmp/coverage.json')
            if json_path.exists():
                data = json.loads(json_path.read_text())
                for filename, info in data.get('files', {}).items():
                    file_coverages[filename] = {
                        'coverage': info.get('percent_covered', 0),
                        'missing_lines': info.get('missing_lines', [])
                    }
        except Exception as e:
            print(f"Warning: Could not parse coverage JSON: {e}")

        return {
            'total_coverage': total_coverage,
            'files': file_coverages,
            'output': output
        }

    def get_uncovered(self, threshold: int = 80) -> List[Dict[str, Any]]:
        """Get list of uncovered code"""
        coverage = self.run_coverage()
        uncovered = []

        for filename, info in coverage['files'].items():
            if info['coverage'] < threshold:
                uncovered.append({
                    'file': filename,
                    'coverage': info['coverage'],
                    'missing_lines': info.get('missing_lines', [])
                })

        # Sort by coverage (ascending)
        uncovered.sort(key=lambda x: x['coverage'])

        return uncovered

    def generate_html(self, output_dir: str = 'htmlcov') -> bool:
        """Generate HTML coverage report"""
        cmd = [
            'python', '-m', 'pytest',
            '--cov=src',
            '--cov-report=html:' + output_dir,
            '-q'
        ]

        result = subprocess.run(cmd, capture_output=True, cwd=self.root)

        if result.returncode in (0, 5):  # 5 = no tests collected
            output_path = self.root / output_dir / 'index.html'
            print(f"✅ HTML report generated: {output_path}")
            return True
        else:
            print(f"❌ Failed to generate HTML report")
            return False

    def print_report(self, coverage: Dict[str, Any]):
        """Print coverage report"""
        print(f"\n📊 Coverage Report")
        print(f"{'='*60}")
        print(f"Total Coverage: {coverage['total_coverage']}%")
        print()

        # Print file-level coverage
        print("By File:")
        print(f"{'File':<40} {'Coverage':<10} {'Status'}")
        print("-" * 60)

        for filename, info in sorted(coverage['files'].items()):
            cov = info['coverage']
            status = "✅" if cov >= 80 else ("⚠️" if cov >= 50 else "🔴")
            short_name = filename if len(filename) < 40 else "..." + filename[-37:]
            print(f"{short_name:<40} {cov:>6.1f}%    {status}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='TDD Coverage Tracker')
    parser.add_argument('--root', '-r', default='.', help='Project root')
    parser.add_argument('--source', '-s', default='src', help='Source directory')
    parser.add_argument('--uncovered', '-u', action='store_true', help='Show uncovered code')
    parser.add_argument('--html', action='store_true', help='Generate HTML report')
    parser.add_argument('--output', '-o', default='htmlcov', help='HTML output directory')
    parser.add_argument('--threshold', '-t', type=int, default=80, help='Coverage threshold')

    args = parser.parse_args()

    tracker = CoverageTracker(args.root)

    if args.html:
        tracker.generate_html(args.output)
    elif args.uncovered:
        uncovered = tracker.get_uncovered(args.threshold)

        print(f"\n🔍 Uncovered Code (below {args.threshold}%)")
        print(f"{'='*60}")

        if not uncovered:
            print("✅ All files meet coverage threshold!")
        else:
            for item in uncovered:
                print(f"\n{item['file']}: {item['coverage']:.1f}%")
                if item['missing_lines']:
                    # Group consecutive lines
                    lines = item['missing_lines']
                    ranges = []
                    start = lines[0]
                    end = lines[0]

                    for line in lines[1:]:
                        if line == end + 1:
                            end = line
                        else:
                            ranges.append((start, end))
                            start = end = line
                    ranges.append((start, end))

                    range_strs = [f"{s}" if s == e else f"{s}-{e}" for s, e in ranges]
                    print(f"   Missing lines: {', '.join(range_strs[:10])}")
                    if len(range_strs) > 10:
                        print(f"   ... and {len(range_strs) - 10} more")
    else:
        coverage = tracker.run_coverage(args.source)
        tracker.print_report(coverage)


if __name__ == '__main__':
    main()
