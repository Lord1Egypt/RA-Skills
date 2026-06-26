#!/usr/bin/env python3
"""
TDD - Main Entry Point

Commands:
  generate    - Generate test cases
  run         - Run tests
  coverage    - Track coverage
  status      - Show TDD status
"""

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent


def run_generate(args):
    """Run test generation"""
    sys.path.insert(0, str(SCRIPT_DIR))
    from generator import TestGenerator

    generator = TestGenerator(args.root)
    file_path = Path(args.file)

    if not file_path.is_absolute():
        file_path = Path(args.root) / file_path

    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        sys.exit(1)

    if args.function:
        result = generator.generate_for_function(args.function, file_path)
    else:
        result = generator.generate_for_file(file_path)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result, encoding='utf-8')
        print(f"✅ Tests written to: {args.output}")
    else:
        print(result)


def run_run(args):
    """Run tests"""
    sys.path.insert(0, str(SCRIPT_DIR))
    from runner import TestRunner

    runner = TestRunner(args.root)
    print(f"🧪 Test Framework: {runner.framework}")

    if args.watch:
        runner.watch(args.target)
    else:
        result = runner.run(args.target, args.verbose)
        runner._print_result(result)

        if args.fail_under and result['total_coverage'] < args.fail_under:
            print(f"❌ Coverage {result['total_coverage']}% below threshold {args.fail_under}%")
            sys.exit(1)

        sys.exit(0 if result['success'] else 1)


def run_coverage(args):
    """Run coverage analysis"""
    sys.path.insert(0, str(SCRIPT_DIR))
    from coverage import CoverageTracker

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
                    lines = item['missing_lines']
                    print(f"   Missing: {lines[:5]}...")
    else:
        coverage = tracker.run_coverage(args.source)
        tracker.print_report(coverage)

        if args.fail_under and coverage['total_coverage'] < args.fail_under:
            print(f"\n❌ Coverage {coverage['total_coverage']}% below threshold {args.fail_under}%")
            sys.exit(1)


def run_status(args):
    """Show TDD status"""
    sys.path.insert(0, str(SCRIPT_DIR))
    from runner import TestRunner
    from coverage import CoverageTracker

    print("\n📊 TDD Status")
    print(f"{'='*60}")

    # Check test framework
    runner = TestRunner(args.root)
    print(f"Framework: {runner.framework}")

    # Check tests
    test_dir = Path(args.root) / 'tests'
    if test_dir.exists():
        test_files = list(test_dir.glob('test_*.py'))
        print(f"Test files: {len(test_files)}")
    else:
        print("Test files: 0 (no tests directory)")

    # Run tests
    print("\nRunning tests...")
    result = runner.run()
    print(f"Result: {'💚 PASSED' if result['success'] else '🔴 FAILED'}")
    print(f"Tests: {result['passed']}/{result['total']} passed")

    # Coverage
    print("\nChecking coverage...")
    tracker = CoverageTracker(args.root)
    coverage = tracker.run_coverage()
    print(f"Coverage: {coverage['total_coverage']}%")

    print(f"\n{'='*60}")
    if result['success'] and coverage['total_coverage'] >= 80:
        print("✅ All systems green!")
    elif result['success']:
        print("⚠️ Tests pass but coverage needs improvement")
    else:
        print("🔴 Tests failing - fix them first")


def main():
    parser = argparse.ArgumentParser(
        description='TDD - Test-Driven Development Assistant',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate tests for a file
  python3 main.py generate --file src/calculator.py

  # Generate tests for a specific function
  python3 main.py generate --file src/calc.py --function add

  # Run tests
  python3 main.py run

  # Run tests in watch mode
  python3 main.py run --watch

  # Check coverage
  python3 main.py coverage

  # Show TDD status
  python3 main.py status
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # generate command
    generate_parser = subparsers.add_parser('generate', help='Generate test cases')
    generate_parser.add_argument('--file', '-f', required=True, help='Source file')
    generate_parser.add_argument('--function', help='Specific function to test')
    generate_parser.add_argument('--output', '-o', help='Output file')
    generate_parser.add_argument('--root', '-r', default='.', help='Project root')
    generate_parser.set_defaults(func=run_generate)

    # run command
    run_parser = subparsers.add_parser('run', help='Run tests')
    run_parser.add_argument('target', nargs='?', help='Test file or directory')
    run_parser.add_argument('--root', '-r', default='.', help='Project root')
    run_parser.add_argument('--watch', '-w', action='store_true', help='Watch mode')
    run_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    run_parser.add_argument('--fail-under', type=int, help='Fail if coverage below threshold')
    run_parser.set_defaults(func=run_run)

    # coverage command
    coverage_parser = subparsers.add_parser('coverage', help='Track coverage')
    coverage_parser.add_argument('--root', '-r', default='.', help='Project root')
    coverage_parser.add_argument('--source', '-s', default='src', help='Source directory')
    coverage_parser.add_argument('--uncovered', '-u', action='store_true', help='Show uncovered code')
    coverage_parser.add_argument('--html', action='store_true', help='Generate HTML report')
    coverage_parser.add_argument('--output', '-o', default='htmlcov', help='HTML output directory')
    coverage_parser.add_argument('--threshold', '-t', type=int, default=80, help='Coverage threshold')
    coverage_parser.add_argument('--fail-under', type=int, help='Fail if coverage below threshold')
    coverage_parser.set_defaults(func=run_coverage)

    # status command
    status_parser = subparsers.add_parser('status', help='Show TDD status')
    status_parser.add_argument('--root', '-r', default='.', help='Project root')
    status_parser.set_defaults(func=run_status)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == '__main__':
    main()
