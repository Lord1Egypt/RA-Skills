#!/usr/bin/env python3
"""Protobuf Linter — lint .proto files for style, naming, breaking changes, best practices."""

import sys
import os
import re
import json
import glob
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class Issue:
    file: str
    line: int
    rule: str
    severity: Severity
    message: str
    category: str


@dataclass
class ProtoField:
    name: str
    type: str
    number: int
    label: str  # optional, repeated, required
    line: int


@dataclass
class ProtoEnumValue:
    name: str
    number: int
    line: int


@dataclass
class ProtoEnum:
    name: str
    values: list
    line: int


@dataclass
class ProtoRPC:
    name: str
    request: str
    response: str
    line: int


@dataclass
class ProtoMessage:
    name: str
    fields: list
    enums: list
    nested: list
    reserved_numbers: list
    reserved_names: list
    line: int


@dataclass
class ProtoService:
    name: str
    rpcs: list
    line: int


@dataclass
class ProtoFile:
    path: str
    syntax: Optional[str] = None
    package: Optional[str] = None
    imports: list = field(default_factory=list)
    messages: list = field(default_factory=list)
    enums: list = field(default_factory=list)
    services: list = field(default_factory=list)
    comments: list = field(default_factory=list)


def strip_comments(line):
    in_string = False
    for i, c in enumerate(line):
        if c == '"' and (i == 0 or line[i-1] != '\\'):
            in_string = not in_string
        if not in_string and i < len(line) - 1 and line[i:i+2] == '//':
            return line[:i].strip()
    return line.strip()


def parse_proto(filepath):
    pf = ProtoFile(path=filepath)
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
    except (IOError, OSError):
        return pf

    comment_lines = []
    block_comment = False

    for i, raw_line in enumerate(lines, 1):
        stripped = raw_line.strip()
        if block_comment:
            if '*/' in stripped:
                block_comment = False
                comment_lines.append(i)
            else:
                comment_lines.append(i)
            continue
        if stripped.startswith('/*'):
            block_comment = True
            comment_lines.append(i)
            if '*/' in stripped:
                block_comment = False
            continue
        if stripped.startswith('//'):
            comment_lines.append(i)

    pf.comments = comment_lines
    clean_lines = []
    for i, raw_line in enumerate(lines, 1):
        if i in comment_lines:
            clean_lines.append((i, ''))
        else:
            clean_lines.append((i, strip_comments(raw_line)))

    full_text = '\n'.join(line for _, line in clean_lines)

    syn = re.search(r'syntax\s*=\s*"(proto[23])"\s*;', full_text)
    if syn:
        pf.syntax = syn.group(1)

    pkg = re.search(r'package\s+([\w.]+)\s*;', full_text)
    if pkg:
        pf.package = pkg.group(1)

    for m in re.finditer(r'import\s+(?:public\s+|weak\s+)?"([^"]+)"\s*;', full_text):
        pf.imports.append(m.group(1))

    def find_line(text_pos):
        count = full_text[:text_pos].count('\n') + 1
        return count

    def parse_block(text, start_line_offset=0):
        msgs = []
        enms = []
        svcs = []

        for m in re.finditer(r'\bmessage\s+(\w+)\s*\{', text):
            msg_name = m.group(1)
            brace_start = m.end() - 1
            brace_count = 1
            pos = m.end()
            while pos < len(text) and brace_count > 0:
                if text[pos] == '{':
                    brace_count += 1
                elif text[pos] == '}':
                    brace_count -= 1
                pos += 1
            body = text[m.end():pos-1]
            line = find_line(m.start()) + start_line_offset

            fields = []
            reserved_nums = []
            reserved_names = []
            nested_msgs = []
            nested_enums = []

            for fm in re.finditer(
                r'(?:optional|repeated|required)?\s*(\w[\w.]*)\s+(\w+)\s*=\s*(\d+)',
                body
            ):
                label = ''
                prefix = body[:fm.start()].split('\n')[-1].strip()
                if prefix in ('optional', 'repeated', 'required'):
                    label = prefix
                fields.append(ProtoField(
                    name=fm.group(2), type=fm.group(1),
                    number=int(fm.group(3)), label=label,
                    line=line + body[:fm.start()].count('\n')
                ))

            for rm in re.finditer(r'reserved\s+(.+?)\s*;', body):
                val = rm.group(1)
                for part in val.split(','):
                    part = part.strip().strip('"')
                    if part.isdigit():
                        reserved_nums.append(int(part))
                    elif 'to' in part:
                        try:
                            a, b = part.split('to')
                            a, b = int(a.strip()), b.strip()
                            if b == 'max':
                                b = 536870911
                            reserved_nums.extend(range(a, int(b)+1))
                        except ValueError:
                            pass
                    elif re.match(r'^[a-zA-Z_]\w*$', part):
                        reserved_names.append(part)

            sub_msgs, sub_enums, _ = parse_block(body, line)
            msgs.append(ProtoMessage(
                name=msg_name, fields=fields, enums=sub_enums,
                nested=sub_msgs, reserved_numbers=reserved_nums,
                reserved_names=reserved_names, line=line
            ))

        for em in re.finditer(r'\benum\s+(\w+)\s*\{', text):
            enum_name = em.group(1)
            brace_count = 1
            pos = em.end()
            while pos < len(text) and brace_count > 0:
                if text[pos] == '{':
                    brace_count += 1
                elif text[pos] == '}':
                    brace_count -= 1
                pos += 1
            body = text[em.end():pos-1]
            line = find_line(em.start()) + start_line_offset

            values = []
            for vm in re.finditer(r'(\w+)\s*=\s*(-?\d+)', body):
                values.append(ProtoEnumValue(
                    name=vm.group(1), number=int(vm.group(2)),
                    line=line + body[:vm.start()].count('\n')
                ))
            enms.append(ProtoEnum(name=enum_name, values=values, line=line))

        for sm in re.finditer(r'\bservice\s+(\w+)\s*\{', text):
            svc_name = sm.group(1)
            brace_count = 1
            pos = sm.end()
            while pos < len(text) and brace_count > 0:
                if text[pos] == '{':
                    brace_count += 1
                elif text[pos] == '}':
                    brace_count -= 1
                pos += 1
            body = text[sm.end():pos-1]
            line = find_line(sm.start()) + start_line_offset

            rpcs = []
            for rm in re.finditer(
                r'rpc\s+(\w+)\s*\(\s*(?:stream\s+)?(\w[\w.]*)\s*\)\s*returns\s*\(\s*(?:stream\s+)?(\w[\w.]*)\s*\)',
                body
            ):
                rpcs.append(ProtoRPC(
                    name=rm.group(1), request=rm.group(2),
                    response=rm.group(3),
                    line=line + body[:rm.start()].count('\n')
                ))
            svcs.append(ProtoService(name=svc_name, rpcs=rpcs, line=line))

        return msgs, enms, svcs

    msgs, enms, svcs = parse_block(full_text)
    pf.messages = msgs
    pf.enums = enms
    pf.services = svcs
    return pf


def lint_structure(pf: ProtoFile) -> list:
    issues = []

    if not pf.syntax:
        issues.append(Issue(pf.path, 1, "missing-syntax", Severity.ERROR,
                            "Missing syntax declaration (syntax = \"proto3\";)", "structure"))

    if not pf.package:
        issues.append(Issue(pf.path, 1, "missing-package", Severity.WARNING,
                            "Missing package declaration", "structure"))

    def check_messages(msgs):
        for msg in msgs:
            if not msg.fields and not msg.nested and not msg.enums:
                issues.append(Issue(pf.path, msg.line, "empty-message", Severity.WARNING,
                                    f"Empty message '{msg.name}'", "structure"))

            numbers = {}
            for f in msg.fields:
                if f.number in numbers:
                    issues.append(Issue(pf.path, f.line, "duplicate-field-number", Severity.ERROR,
                                        f"Duplicate field number {f.number} in '{msg.name}' "
                                        f"(also used by '{numbers[f.number]}')", "structure"))
                numbers[f.number] = f.name

                if f.number in msg.reserved_numbers:
                    issues.append(Issue(pf.path, f.line, "reserved-conflict", Severity.ERROR,
                                        f"Field '{f.name}' uses reserved number {f.number}", "structure"))

                if f.name in msg.reserved_names:
                    issues.append(Issue(pf.path, f.line, "reserved-name-conflict", Severity.ERROR,
                                        f"Field '{f.name}' uses reserved name", "structure"))

            check_messages(msg.nested)

    check_messages(pf.messages)

    for enum in pf.enums:
        if not enum.values:
            issues.append(Issue(pf.path, enum.line, "empty-enum", Severity.WARNING,
                                f"Empty enum '{enum.name}'", "structure"))

    for svc in pf.services:
        if not svc.rpcs:
            issues.append(Issue(pf.path, svc.line, "empty-service", Severity.WARNING,
                                f"Empty service '{svc.name}'", "structure"))

    return issues


def lint_naming(pf: ProtoFile) -> list:
    issues = []

    if pf.package and not re.match(r'^[a-z][a-z0-9]*(\.[a-z][a-z0-9]*)*$', pf.package):
        issues.append(Issue(pf.path, 1, "package-naming", Severity.WARNING,
                            f"Package '{pf.package}' should be lower_snake_case with dots", "naming"))

    def check_messages(msgs):
        for msg in msgs:
            if not re.match(r'^[A-Z][a-zA-Z0-9]*$', msg.name):
                issues.append(Issue(pf.path, msg.line, "message-naming", Severity.WARNING,
                                    f"Message '{msg.name}' should be CamelCase", "naming"))

            for f in msg.fields:
                if not re.match(r'^[a-z][a-z0-9]*(_[a-z0-9]+)*$', f.name):
                    issues.append(Issue(pf.path, f.line, "field-naming", Severity.WARNING,
                                        f"Field '{f.name}' should be lower_snake_case", "naming"))

            check_messages(msg.nested)
            check_enums(msg.enums, msg.name)

    def check_enums(enums, parent=""):
        for enum in enums:
            if not re.match(r'^[A-Z][a-zA-Z0-9]*$', enum.name):
                issues.append(Issue(pf.path, enum.line, "enum-naming", Severity.WARNING,
                                    f"Enum '{enum.name}' should be CamelCase", "naming"))

            expected_prefix = re.sub(r'([A-Z])', r'_\1', enum.name).upper().lstrip('_') + '_'
            for val in enum.values:
                if not re.match(r'^[A-Z][A-Z0-9]*(_[A-Z0-9]+)*$', val.name):
                    issues.append(Issue(pf.path, val.line, "enum-value-naming", Severity.WARNING,
                                        f"Enum value '{val.name}' should be UPPER_SNAKE_CASE", "naming"))

                if not val.name.startswith(expected_prefix) and val.name != 'UNSPECIFIED':
                    issues.append(Issue(pf.path, val.line, "enum-value-prefix", Severity.INFO,
                                        f"Enum value '{val.name}' should be prefixed with "
                                        f"'{expected_prefix}'", "naming"))

    check_messages(pf.messages)
    check_enums(pf.enums)

    for svc in pf.services:
        if not re.match(r'^[A-Z][a-zA-Z0-9]*$', svc.name):
            issues.append(Issue(pf.path, svc.line, "service-naming", Severity.WARNING,
                                f"Service '{svc.name}' should be CamelCase", "naming"))

        for rpc in svc.rpcs:
            if not re.match(r'^[A-Z][a-zA-Z0-9]*$', rpc.name):
                issues.append(Issue(pf.path, rpc.line, "rpc-naming", Severity.WARNING,
                                    f"RPC '{rpc.name}' should be CamelCase", "naming"))

    return issues


def lint_best_practices(pf: ProtoFile) -> list:
    issues = []

    if pf.syntax == 'proto2':
        issues.append(Issue(pf.path, 1, "use-proto3", Severity.INFO,
                            "Consider using proto3 syntax for better compatibility", "best-practices"))

    if pf.syntax == 'proto2':
        for msg in pf.messages:
            for f in msg.fields:
                if f.label == 'required':
                    issues.append(Issue(pf.path, f.line, "avoid-required", Severity.WARNING,
                                        f"Avoid 'required' fields — they cause compatibility issues",
                                        "best-practices"))

    if pf.package:
        expected = pf.package.replace('.', '/') + '.proto'
        basename = os.path.basename(pf.path)
        pkg_last = pf.package.split('.')[-1]
        if basename != pkg_last + '.proto' and basename != expected:
            issues.append(Issue(pf.path, 1, "file-package-match", Severity.INFO,
                                f"File '{basename}' doesn't match package '{pf.package}'",
                                "best-practices"))

    total_entities = len(pf.messages) + len(pf.services)
    if total_entities > 0 and len(pf.comments) == 0:
        issues.append(Issue(pf.path, 1, "no-comments", Severity.INFO,
                            "No comments found — consider documenting messages and services",
                            "best-practices"))

    wrapper_types = {
        'google.protobuf.DoubleValue', 'google.protobuf.FloatValue',
        'google.protobuf.Int64Value', 'google.protobuf.UInt64Value',
        'google.protobuf.Int32Value', 'google.protobuf.UInt32Value',
        'google.protobuf.BoolValue', 'google.protobuf.StringValue',
        'google.protobuf.BytesValue'
    }
    has_wrappers_import = any('wrappers.proto' in imp for imp in pf.imports)

    if pf.syntax == 'proto3':
        for msg in pf.messages:
            for f in msg.fields:
                if f.type in ('int32', 'int64', 'uint32', 'uint64', 'bool', 'string', 'float', 'double'):
                    if f.label != 'repeated' and not has_wrappers_import:
                        pass  # only suggest if they're already importing wrappers

    return issues


def lint_breaking(old_pf: ProtoFile, new_pf: ProtoFile) -> list:
    issues = []

    old_msgs = {m.name: m for m in old_pf.messages}
    new_msgs = {m.name: m for m in new_pf.messages}

    for name, old_msg in old_msgs.items():
        if name not in new_msgs:
            issues.append(Issue(new_pf.path, 1, "removed-message", Severity.ERROR,
                                f"Message '{name}' was removed (breaking)", "compatibility"))
            continue

        new_msg = new_msgs[name]
        old_fields = {f.number: f for f in old_msg.fields}
        new_fields = {f.number: f for f in new_msg.fields}

        for num, old_f in old_fields.items():
            if num not in new_fields:
                if num not in new_msg.reserved_numbers:
                    issues.append(Issue(new_pf.path, old_f.line, "removed-field", Severity.ERROR,
                                        f"Field '{old_f.name}' (number {num}) removed from '{name}' "
                                        f"without reserving number (breaking)", "compatibility"))
                continue

            new_f = new_fields[num]
            if old_f.type != new_f.type:
                issues.append(Issue(new_pf.path, new_f.line, "changed-field-type", Severity.ERROR,
                                    f"Field '{old_f.name}' type changed from '{old_f.type}' to "
                                    f"'{new_f.type}' in '{name}' (breaking)", "compatibility"))

    old_enums = {e.name: e for e in old_pf.enums}
    new_enums = {e.name: e for e in new_pf.enums}

    for name, old_enum in old_enums.items():
        if name not in new_enums:
            issues.append(Issue(new_pf.path, 1, "removed-enum", Severity.ERROR,
                                f"Enum '{name}' was removed (breaking)", "compatibility"))
            continue

        new_enum = new_enums[name]
        old_vals = {v.number: v for v in old_enum.values}
        new_vals = {v.number: v for v in new_enum.values}

        for num, old_v in old_vals.items():
            if num not in new_vals:
                issues.append(Issue(new_pf.path, old_v.line, "removed-enum-value", Severity.ERROR,
                                    f"Enum value '{old_v.name}' removed from '{name}' (breaking)",
                                    "compatibility"))
            elif old_v.name != new_vals[num].name:
                issues.append(Issue(new_pf.path, new_vals[num].line, "renamed-enum-value",
                                    Severity.WARNING,
                                    f"Enum value renamed from '{old_v.name}' to "
                                    f"'{new_vals[num].name}' in '{name}' (may break clients)",
                                    "compatibility"))

    old_svcs = {s.name: s for s in old_pf.services}
    new_svcs = {s.name: s for s in new_pf.services}

    for name, old_svc in old_svcs.items():
        if name not in new_svcs:
            issues.append(Issue(new_pf.path, 1, "removed-service", Severity.ERROR,
                                f"Service '{name}' was removed (breaking)", "compatibility"))
            continue

        new_svc = new_svcs[name]
        old_rpcs = {r.name: r for r in old_svc.rpcs}
        new_rpcs = {r.name: r for r in new_svc.rpcs}

        for rpc_name, old_rpc in old_rpcs.items():
            if rpc_name not in new_rpcs:
                issues.append(Issue(new_pf.path, old_rpc.line, "removed-rpc", Severity.ERROR,
                                    f"RPC '{rpc_name}' removed from service '{name}' (breaking)",
                                    "compatibility"))
                continue

            new_rpc = new_rpcs[rpc_name]
            if old_rpc.request != new_rpc.request:
                issues.append(Issue(new_pf.path, new_rpc.line, "changed-rpc-request", Severity.ERROR,
                                    f"RPC '{rpc_name}' request type changed from "
                                    f"'{old_rpc.request}' to '{new_rpc.request}' (breaking)",
                                    "compatibility"))
            if old_rpc.response != new_rpc.response:
                issues.append(Issue(new_pf.path, new_rpc.line, "changed-rpc-response", Severity.ERROR,
                                    f"RPC '{rpc_name}' response type changed from "
                                    f"'{old_rpc.response}' to '{new_rpc.response}' (breaking)",
                                    "compatibility"))

    return issues


def collect_files(path, recursive=False):
    if os.path.isfile(path):
        return [path]
    if os.path.isdir(path):
        if recursive:
            return sorted(glob.glob(os.path.join(path, '**', '*.proto'), recursive=True))
        return sorted(glob.glob(os.path.join(path, '*.proto')))
    return []


def format_text(issues):
    if not issues:
        return "\033[32m\u2714 No issues found\033[0m"

    sev_icons = {Severity.ERROR: "\033[31m\u2716\033[0m", Severity.WARNING: "\033[33m\u26a0\033[0m",
                 Severity.INFO: "\033[36m\u2139\033[0m"}
    lines = []
    current_file = None
    for issue in sorted(issues, key=lambda i: (i.file, i.line)):
        if issue.file != current_file:
            current_file = issue.file
            lines.append(f"\n\033[1m{current_file}\033[0m")
        icon = sev_icons.get(issue.severity, "")
        lines.append(f"  {icon} {issue.line}:{issue.rule} — {issue.message}")

    errors = sum(1 for i in issues if i.severity == Severity.ERROR)
    warnings = sum(1 for i in issues if i.severity == Severity.WARNING)
    infos = sum(1 for i in issues if i.severity == Severity.INFO)
    lines.append(f"\n{errors} error(s), {warnings} warning(s), {infos} info(s)")
    return '\n'.join(lines)


def format_json(issues):
    return json.dumps([{
        'file': i.file, 'line': i.line, 'rule': i.rule,
        'severity': i.severity.value, 'message': i.message,
        'category': i.category
    } for i in issues], indent=2)


def format_summary(issues):
    errors = sum(1 for i in issues if i.severity == Severity.ERROR)
    warnings = sum(1 for i in issues if i.severity == Severity.WARNING)
    infos = sum(1 for i in issues if i.severity == Severity.INFO)
    files = len(set(i.file for i in issues))
    return (f"Files: {files} | Errors: {errors} | Warnings: {warnings} | "
            f"Info: {infos} | Total: {len(issues)}")


def main():
    if len(sys.argv) < 3:
        print("Usage: protobuf_linter.py <command> <path> [options]")
        print("Commands: lint, naming, breaking, validate")
        print("Options: --recursive, --format json|text|summary")
        sys.exit(2)

    command = sys.argv[1]
    path = sys.argv[2]
    fmt = 'text'
    recursive = '--recursive' in sys.argv

    for i, arg in enumerate(sys.argv):
        if arg == '--format' and i + 1 < len(sys.argv):
            fmt = sys.argv[i + 1]

    if command == 'breaking':
        if len(sys.argv) < 4:
            print("Usage: protobuf_linter.py breaking <old.proto> <new.proto>")
            sys.exit(2)
        old_path = sys.argv[2]
        new_path = sys.argv[3]
        old_pf = parse_proto(old_path)
        new_pf = parse_proto(new_path)
        issues = lint_breaking(old_pf, new_pf)
    else:
        files = collect_files(path, recursive)
        if not files:
            print(f"No .proto files found at '{path}'")
            sys.exit(2)

        issues = []
        for filepath in files:
            pf = parse_proto(filepath)
            if command == 'lint':
                issues.extend(lint_structure(pf))
                issues.extend(lint_naming(pf))
                issues.extend(lint_best_practices(pf))
            elif command == 'naming':
                issues.extend(lint_naming(pf))
            elif command == 'validate':
                issues.extend(lint_structure(pf))
            else:
                print(f"Unknown command: {command}")
                sys.exit(2)

    if fmt == 'json':
        print(format_json(issues))
    elif fmt == 'summary':
        print(format_summary(issues))
    else:
        print(format_text(issues))

    has_errors = any(i.severity == Severity.ERROR for i in issues)
    sys.exit(1 if has_errors else 0)


if __name__ == '__main__':
    main()
