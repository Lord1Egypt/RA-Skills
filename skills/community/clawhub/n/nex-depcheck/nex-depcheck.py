#!/usr/bin/env python3
"""
Nex DepCheck - Skill dependency checker.
Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.scanner import scan_skill, scan_all_skills, scan_imports
from lib.config import SEPARATOR, SUBSEPARATOR

FOOTER = "[DepCheck by Nex AI | nex-ai.be]"


def cmd_check(args):
    result = scan_skill(args.path)
    if not result:
        print(f"No Python files found in: {args.path}")
        print(FOOTER)
        return

    print(f"\n{SEPARATOR}")
    print(f"DEPENDENCY CHECK: {result['name']}")
    print(f"{SEPARATOR}\n")

    print(f"Python files: {len(result['py_files'])}")
    print(f"Total unique imports: {result['total_imports']}")
    print(f"SKILL.md: {'yes' if result['has_skill_md'] else 'MISSING'}")
    print(f"setup.sh: {'yes' if result['has_setup'] else 'MISSING'}")

    if result['external']:
        print(f"\n  EXTERNAL DEPENDENCIES ({len(result['external'])}):")
        for imp in sorted(result['external'], key=lambda x: x['module']):
            print(f"    - {imp['module']}")
        print(f"\n  STATUS: NOT CLEAN (external deps found)")
    else:
        print(f"\n  STATUS: CLEAN (stdlib + internal only)")

    if args.verbose:
        print(f"\n  Stdlib ({len(result['stdlib'])}):")
        for imp in sorted(result['stdlib'], key=lambda x: x['module']):
            print(f"    {imp['module']}")

        print(f"\n  Internal ({len(result['internal'])}):")
        for imp in sorted(result['internal'], key=lambda x: x['module']):
            print(f"    {imp['module']}")

        print(f"\n  Files:")
        for f, imports in result['file_imports'].items():
            ext = [i for i in imports if i['category'] == 'external']
            marker = " [!]" if ext else ""
            print(f"    {f}{marker}")

    print(f"\n{FOOTER}")


def cmd_scan(args):
    results = scan_all_skills(args.path)
    if not results:
        print(f"No skill directories found in: {args.path}")
        print(FOOTER)
        return

    clean = [r for r in results if r['clean']]
    dirty = [r for r in results if not r['clean']]

    print(f"\n{SEPARATOR}")
    print(f"SCAN: {len(results)} skills in {args.path}")
    print(f"{SEPARATOR}\n")

    print(f"{'Skill':<30} {'Files':<7} {'Imports':<9} {'External':<10} {'Status':<8}")
    print("-" * 64)

    for r in sorted(results, key=lambda x: (-len(x['external']), x['name'])):
        ext_count = len(r['external'])
        status = "CLEAN" if r['clean'] else f"{ext_count} ext"
        print(f"{r['name'][:29]:<30} {len(r['py_files']):<7} {r['total_imports']:<9} {ext_count:<10} {status:<8}")

    print(f"\nClean: {len(clean)} | Issues: {len(dirty)} | Total: {len(results)}")

    if dirty:
        print(f"\nSkills with external dependencies:")
        for r in dirty:
            ext_names = ', '.join(i['module'] for i in r['external'])
            print(f"  {r['name']}: {ext_names}")

    print(f"\n{FOOTER}")


def cmd_file(args):
    imports = scan_imports(args.path)
    if not imports:
        print(f"No imports found in: {args.path}")
        print(FOOTER)
        return

    print(f"\nImports in {args.path}:\n")
    for imp in sorted(imports, key=lambda x: (x['category'], x['module'])):
        tag = f"[{imp['category']}]"
        print(f"  {tag:<12} {imp['module']}")

    external = [i for i in imports if i['category'] == 'external']
    if external:
        print(f"\n  External deps: {', '.join(i['module'] for i in external)}")
    else:
        print(f"\n  All imports are stdlib or internal.")

    print(FOOTER)


def cmd_stdlib(args):
    from lib.config import STDLIB_MODULES
    query = args.module.lower()
    if query in STDLIB_MODULES:
        print(f"  '{query}' is a Python stdlib module.")
    else:
        close = [m for m in sorted(STDLIB_MODULES) if query in m]
        if close:
            print(f"  '{query}' is NOT in stdlib. Similar: {', '.join(close[:10])}")
        else:
            print(f"  '{query}' is NOT in stdlib.")
    print(FOOTER)


# --- Main ---

def main():
    parser = argparse.ArgumentParser(
        description="Nex DepCheck - Skill dependency checker.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # CHECK
    p = subparsers.add_parser('check', help='Check a single skill for external deps')
    p.add_argument('path', help='Path to skill directory')
    p.add_argument('--verbose', '-v', action='store_true', help='Show all imports')
    p.set_defaults(func=cmd_check)

    # SCAN
    p = subparsers.add_parser('scan', help='Scan all skills in a directory')
    p.add_argument('path', help='Path to parent directory containing skills')
    p.set_defaults(func=cmd_scan)

    # FILE
    p = subparsers.add_parser('file', help='Check a single Python file')
    p.add_argument('path', help='Path to Python file')
    p.set_defaults(func=cmd_file)

    # STDLIB
    p = subparsers.add_parser('stdlib', help='Check if a module is in Python stdlib')
    p.add_argument('module', help='Module name to check')
    p.set_defaults(func=cmd_stdlib)

    args = parser.parse_args()

    if not hasattr(args, 'func'):
        parser.print_help()
        return

    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
