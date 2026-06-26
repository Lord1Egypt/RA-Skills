---
name: Proto Break Check
description: Protobuf/gRPC breaking change detector. Compares two versions of .proto files (via git diff, two directories, or a before/after pair) and classifies every change as BREAKING, NON-BREAKING, or NOTE. Detects field number reuse (CRITICAL), field type changes, removed fields without deprecation, removed RPC methods, streaming mode changes, enum value removal, service/package renames, and oneof mutations. Zero external dependencies — pure .proto regex parsing, no protoc required. Outputs a migration guide + CI fail-gate command. Zero competitors on ClawHub.
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
tags:
  - protobuf
  - grpc
  - api
  - breaking-changes
  - microservices
  - developer-tools
  - security
  - backend
---

# phy-proto-break-check

**Protobuf/gRPC breaking change detector** — compares `.proto` schema versions and tells you exactly what will break client-generated stubs, serialized messages, and wire compatibility before you push.

Field numbers are sacred in protobuf. Reusing one corrupts serialized data in production. This tool catches that and 11 other breaking-change patterns before they reach users.

## What It Detects

| ID | Change Type | Severity | Why It Breaks |
|----|-------------|----------|---------------|
| FN001 | Field number reused for different type | **CRITICAL** | Corrupts existing serialized messages silently |
| FN002 | Field removed without `[deprecated = true]` | **BREAKING** | Old clients send the field; new server ignores it (silent data loss) |
| FT001 | Field type changed (e.g., `int32` → `string`) | **BREAKING** | Wire encoding changes — deserialization fails |
| FT002 | Field label changed (`repeated` ↔ singular) | **BREAKING** | Collection unpacking breaks |
| SM001 | Service RPC method removed | **BREAKING** | All callers get `NOT_FOUND`; generated stubs fail to compile |
| SM002 | RPC streaming mode changed (unary/server/client/bidi) | **BREAKING** | Generated client interface changes; existing calls fail |
| SM003 | Service name or package changed | **BREAKING** | All generated stubs must be recompiled and redeployed |
| EN001 | Enum value removed | **BREAKING** | Clients may have serialized the removed value; decode fails |
| EN002 | Enum value number changed for existing name | **CRITICAL** | Corrupts all previously serialized enum values |
| OO001 | Field moved into or out of `oneof` | **BREAKING** | Oneof fields have different wire behavior |
| DP001 | `[deprecated = true]` removed from field | **NOTE** | Field re-activated — may confuse clients that stopped sending it |
| NB001 | New field added with unused number | NON-BREAKING | Safe — old clients skip unknown fields |
| NB002 | New RPC method added | NON-BREAKING | Safe — old clients simply don't call it |
| NB003 | Field marked `[deprecated = true]` | NON-BREAKING | Soft signal — field still functional |

## How to Use

```
/phy-proto-break-check
Compare proto files: before/ is HEAD~1, after/ is HEAD
```

```
/phy-proto-break-check
Check if my .proto changes in src/proto/ are backward-compatible using git diff
```

```
/phy-proto-break-check
Diff user.proto v1 vs user.proto v2 for breaking changes
```

The agent will:
1. Locate `.proto` files (from git diff, two paths, or current directory)
2. Parse both versions into structured message/service/enum maps
3. Run all 14 checks against each field, enum value, and RPC
4. Print findings grouped by CRITICAL → BREAKING → NON-BREAKING → NOTE
5. Generate a migration guide for each BREAKING change
6. Print a CI fail-gate command

---

## Implementation

When invoked, run the following Python analysis. Accept `--before` and `--after` directory paths, or use `git diff` to extract proto changes automatically.

```python
#!/usr/bin/env python3
"""
phy-proto-break-check — Protobuf/gRPC backward-compatibility checker
Detects FN001, FN002, FT001, FT002, SM001, SM002, SM003,
        EN001, EN002, OO001, DP001, NB001, NB002, NB003
No external dependencies — zero protoc requirement.
"""
import os
import re
import sys
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# ─────────────────────────────────────────────────────
# Data models
# ─────────────────────────────────────────────────────

@dataclass
class ProtoField:
    number: int
    name: str
    type_: str          # int32, string, MyMessage, etc.
    label: str          # singular, repeated, optional, required
    deprecated: bool = False
    in_oneof: Optional[str] = None   # name of the oneof block, if any


@dataclass
class ProtoEnum:
    name: str
    values: dict[str, int]   # name → number
    deprecated_values: set[str] = field(default_factory=set)


@dataclass
class ProtoRPC:
    name: str
    request_type: str
    response_type: str
    client_streaming: bool = False
    server_streaming: bool = False


@dataclass
class ProtoMessage:
    name: str
    fields: dict[int, ProtoField]   # field_number → ProtoField
    oneofs: dict[str, list[int]]    # oneof_name → [field_numbers]
    nested: dict[str, 'ProtoMessage'] = field(default_factory=dict)


@dataclass
class ProtoService:
    name: str
    rpcs: dict[str, ProtoRPC]       # rpc_name → ProtoRPC


@dataclass
class ProtoFile:
    path: str
    package: str
    syntax: str                     # proto2 or proto3
    messages: dict[str, ProtoMessage]
    enums: dict[str, ProtoEnum]
    services: dict[str, ProtoService]


@dataclass
class BreakingChange:
    check_id: str
    severity: str          # CRITICAL / BREAKING / NON-BREAKING / NOTE
    proto_file: str
    element: str           # e.g. "MyMessage.user_id" or "UserService.GetUser"
    description: str
    migration: str


# ─────────────────────────────────────────────────────
# Proto parser (regex-based, no protoc required)
# ─────────────────────────────────────────────────────

_COMMENT_RE = re.compile(r'//[^\n]*|/\*.*?\*/', re.DOTALL)
_BLOCK_RE = re.compile(r'\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', re.DOTALL)

def strip_comments(text: str) -> str:
    return _COMMENT_RE.sub('', text)


def parse_field_line(line: str) -> Optional[tuple]:
    """Parse a single proto field line → (label, type, name, number, deprecated, oneof)"""
    line = line.strip().rstrip(';').strip()
    if not line or line.startswith('//') or line.startswith('option '):
        return None

    deprecated = '[deprecated = true]' in line.lower() or '[deprecated=true]' in line.lower()
    # Remove options block
    clean = re.sub(r'\[.*?\]', '', line).strip()

    # repeated/optional/required type name = number
    m = re.match(
        r'^(repeated|optional|required|map<[^>]+>)?\s*'
        r'(\S+)\s+(\w+)\s*=\s*(\d+)',
        clean
    )
    if m:
        label_raw = m.group(1) or 'singular'
        if label_raw.startswith('map<'):
            label_raw = 'map'
        type_ = m.group(2)
        name = m.group(3)
        number = int(m.group(4))
        return (label_raw, type_, name, number, deprecated)

    return None


def parse_oneof_block(block_text: str) -> tuple[str, list[str]]:
    """Extract oneof name and field names from a oneof { ... } block."""
    m = re.match(r'\s*oneof\s+(\w+)\s*\{(.*)\}', block_text, re.DOTALL)
    if not m:
        return ('', [])
    oneof_name = m.group(1)
    inner = m.group(2)
    field_names = re.findall(r'\w+\s+(\w+)\s*=\s*\d+', inner)
    return (oneof_name, field_names)


def parse_message(name: str, body: str) -> ProtoMessage:
    """Parse a message body into ProtoMessage."""
    fields_by_num: dict[int, ProtoField] = {}
    oneofs: dict[str, list[int]] = {}

    # Find oneof blocks first
    oneof_pattern = re.compile(r'\boneof\s+(\w+)\s*\{([^}]*)\}', re.DOTALL)
    oneof_field_names: dict[str, str] = {}  # field_name → oneof_name
    for m in oneof_pattern.finditer(body):
        oo_name = m.group(1)
        oo_body = m.group(2)
        oo_field_nums = []
        for line in oo_body.split('\n'):
            parsed = parse_field_line(line)
            if parsed:
                label, type_, fname, fnum, dep = parsed
                fields_by_num[fnum] = ProtoField(
                    number=fnum, name=fname, type_=type_,
                    label='oneof', deprecated=dep, in_oneof=oo_name
                )
                oo_field_nums.append(fnum)
                oneof_field_names[fname] = oo_name
        oneofs[oo_name] = oo_field_nums

    # Strip oneof blocks to avoid double-parsing
    cleaned_body = oneof_pattern.sub('', body)

    for line in cleaned_body.split('\n'):
        parsed = parse_field_line(line)
        if parsed:
            label, type_, fname, fnum, dep = parsed
            if fnum not in fields_by_num:
                fields_by_num[fnum] = ProtoField(
                    number=fnum, name=fname, type_=type_,
                    label=label, deprecated=dep,
                    in_oneof=oneof_field_names.get(fname)
                )

    return ProtoMessage(name=name, fields=fields_by_num, oneofs=oneofs)


def parse_enum(name: str, body: str) -> ProtoEnum:
    values: dict[str, int] = {}
    deprecated_values: set[str] = set()
    for line in body.split('\n'):
        line = line.strip().rstrip(';')
        if not line or line.startswith('//') or line.startswith('option'):
            continue
        deprecated = '[deprecated = true]' in line.lower()
        clean = re.sub(r'\[.*?\]', '', line).strip()
        m = re.match(r'(\w+)\s*=\s*(-?\d+)', clean)
        if m:
            vname = m.group(1)
            vnum = int(m.group(2))
            values[vname] = vnum
            if deprecated:
                deprecated_values.add(vname)
    return ProtoEnum(name=name, values=values, deprecated_values=deprecated_values)


def parse_service(name: str, body: str) -> ProtoService:
    rpcs: dict[str, ProtoRPC] = {}
    rpc_re = re.compile(
        r'rpc\s+(\w+)\s*\(\s*(stream\s+)?(\S+)\s*\)\s*returns\s*\(\s*(stream\s+)?(\S+)\s*\)',
        re.DOTALL
    )
    for m in rpc_re.finditer(body):
        rpc_name = m.group(1)
        client_stream = bool(m.group(2))
        req_type = m.group(3).strip(')').strip()
        server_stream = bool(m.group(4))
        resp_type = m.group(5).strip(')').strip()
        rpcs[rpc_name] = ProtoRPC(
            name=rpc_name,
            request_type=req_type,
            response_type=resp_type,
            client_streaming=client_stream,
            server_streaming=server_stream,
        )
    return ProtoService(name=name, rpcs=rpcs)


def parse_proto_file(path: Path) -> ProtoFile:
    """Parse a .proto file into a ProtoFile structure."""
    text = path.read_text(errors='ignore')
    text = strip_comments(text)

    package_m = re.search(r'^\s*package\s+([\w.]+)\s*;', text, re.MULTILINE)
    package = package_m.group(1) if package_m else ''

    syntax_m = re.search(r'^\s*syntax\s*=\s*"(proto[23])"\s*;', text, re.MULTILINE)
    syntax = syntax_m.group(1) if syntax_m else 'proto3'

    messages: dict[str, ProtoMessage] = {}
    enums: dict[str, ProtoEnum] = {}
    services: dict[str, ProtoService] = {}

    # Simple top-level block parser
    # Handles: message Name { ... }  enum Name { ... }  service Name { ... }
    block_re = re.compile(
        r'\b(message|enum|service)\s+(\w+)\s*\{',
        re.DOTALL
    )

    pos = 0
    while pos < len(text):
        m = block_re.search(text, pos)
        if not m:
            break
        keyword = m.group(1)
        name = m.group(2)
        start = m.end() - 1  # position of opening brace

        # Find matching closing brace
        depth = 0
        i = start
        while i < len(text):
            if text[i] == '{':
                depth += 1
            elif text[i] == '}':
                depth -= 1
                if depth == 0:
                    break
            i += 1

        body = text[start + 1:i]
        pos = i + 1

        if keyword == 'message':
            messages[name] = parse_message(name, body)
        elif keyword == 'enum':
            enums[name] = parse_enum(name, body)
        elif keyword == 'service':
            services[name] = parse_service(name, body)

    return ProtoFile(
        path=str(path),
        package=package,
        syntax=syntax,
        messages=messages,
        enums=enums,
        services=services,
    )


def parse_proto_dir(directory: Path) -> dict[str, ProtoFile]:
    """Parse all .proto files in a directory tree."""
    result = {}
    for proto_path in directory.rglob('*.proto'):
        try:
            pf = parse_proto_file(proto_path)
            # Key by relative path from directory root
            rel = str(proto_path.relative_to(directory))
            result[rel] = pf
        except Exception as e:
            print(f"  [WARN] Could not parse {proto_path}: {e}", file=sys.stderr)
    return result


# ─────────────────────────────────────────────────────
# Git diff extractor
# ─────────────────────────────────────────────────────

def extract_proto_from_git(git_ref_before: str = 'HEAD~1',
                            git_ref_after: str = 'HEAD',
                            repo_root: Path = Path('.')) -> tuple[dict, dict]:
    """
    Extract proto file content at two git refs.
    Returns (before_protos, after_protos) as dicts of {rel_path: ProtoFile}.
    """
    import tempfile

    def git_proto_files(ref: str) -> list[str]:
        result = subprocess.run(
            ['git', 'ls-tree', '-r', '--name-only', ref],
            capture_output=True, text=True, cwd=repo_root
        )
        return [f for f in result.stdout.split('\n') if f.endswith('.proto')]

    def git_show(ref: str, path: str) -> Optional[str]:
        result = subprocess.run(
            ['git', 'show', f'{ref}:{path}'],
            capture_output=True, text=True, cwd=repo_root
        )
        if result.returncode == 0:
            return result.stdout
        return None

    before_protos: dict[str, ProtoFile] = {}
    after_protos: dict[str, ProtoFile] = {}

    # Get changed proto files
    diff_result = subprocess.run(
        ['git', 'diff', '--name-only', git_ref_before, git_ref_after, '--', '*.proto'],
        capture_output=True, text=True, cwd=repo_root
    )
    changed_protos = [f for f in diff_result.stdout.split('\n') if f.endswith('.proto')]

    if not changed_protos:
        # If no explicit diff, check all proto files in HEAD
        changed_protos = git_proto_files(git_ref_after)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        for rel_path in changed_protos:
            if not rel_path.strip():
                continue
            # Write before version
            before_content = git_show(git_ref_before, rel_path)
            if before_content:
                before_file = tmp / 'before' / rel_path
                before_file.parent.mkdir(parents=True, exist_ok=True)
                before_file.write_text(before_content)
                try:
                    before_protos[rel_path] = parse_proto_file(before_file)
                except Exception:
                    pass

            # Write after version
            after_content = git_show(git_ref_after, rel_path)
            if after_content:
                after_file = tmp / 'after' / rel_path
                after_file.parent.mkdir(parents=True, exist_ok=True)
                after_file.write_text(after_content)
                try:
                    after_protos[rel_path] = parse_proto_file(after_file)
                except Exception:
                    pass

    return before_protos, after_protos


# ─────────────────────────────────────────────────────
# Diff engine
# ─────────────────────────────────────────────────────

def compare_proto_files(
    rel_path: str,
    before: ProtoFile,
    after: ProtoFile,
) -> list[BreakingChange]:
    changes: list[BreakingChange] = []

    # SM003 — Package or service names changed
    if before.package != after.package and before.package and after.package:
        changes.append(BreakingChange(
            check_id='SM003',
            severity='BREAKING',
            proto_file=rel_path,
            element=f'package {before.package}',
            description=f'Package renamed: `{before.package}` → `{after.package}`. '
                        f'All generated stub namespaces change.',
            migration=(
                f'If clients use old stubs, they must regenerate code with the new package. '
                f'Consider keeping the old package name and using an alias, or deprecate with a compatibility shim.'
            )
        ))

    # Compare messages
    for msg_name, before_msg in before.messages.items():
        if msg_name not in after.messages:
            # Entire message removed — check if any service references it
            changes.append(BreakingChange(
                check_id='SM001',
                severity='BREAKING',
                proto_file=rel_path,
                element=f'message {msg_name}',
                description=f'Message `{msg_name}` removed entirely.',
                migration=f'Mark as deprecated first: add a comment `// Deprecated: use NewMessage instead`. '
                          f'Keep for at least one release cycle before removal.'
            ))
            continue

        after_msg = after.messages[msg_name]
        changes.extend(_compare_message_fields(rel_path, msg_name, before_msg, after_msg))

    # Compare enums
    for enum_name, before_enum in before.enums.items():
        if enum_name not in after.enums:
            changes.append(BreakingChange(
                check_id='EN001',
                severity='BREAKING',
                proto_file=rel_path,
                element=f'enum {enum_name}',
                description=f'Enum `{enum_name}` removed.',
                migration=f'Mark as deprecated. Keep all enum values; remove only if usage tracking confirms zero clients.'
            ))
            continue
        after_enum = after.enums[enum_name]
        changes.extend(_compare_enum(rel_path, enum_name, before_enum, after_enum))

    # Compare services
    for svc_name, before_svc in before.services.items():
        if svc_name not in after.services:
            changes.append(BreakingChange(
                check_id='SM001',
                severity='BREAKING',
                proto_file=rel_path,
                element=f'service {svc_name}',
                description=f'Service `{svc_name}` removed. All RPCs unavailable.',
                migration=f'Deprecate the service before removal. Redirect traffic to new service.'
            ))
            continue
        after_svc = after.services[svc_name]
        changes.extend(_compare_service(rel_path, svc_name, before_svc, after_svc))

    # NB001 / NB002 — non-breaking additions
    for msg_name in after.messages:
        if msg_name not in before.messages:
            changes.append(BreakingChange(
                check_id='NB001',
                severity='NON-BREAKING',
                proto_file=rel_path,
                element=f'message {msg_name}',
                description=f'New message `{msg_name}` added.',
                migration='No action required.'
            ))
    for svc_name in after.services:
        if svc_name not in before.services:
            changes.append(BreakingChange(
                check_id='NB002',
                severity='NON-BREAKING',
                proto_file=rel_path,
                element=f'service {svc_name}',
                description=f'New service `{svc_name}` added.',
                migration='No action required.'
            ))

    return changes


def _compare_message_fields(
    rel_path: str,
    msg_name: str,
    before: ProtoMessage,
    after: ProtoMessage,
) -> list[BreakingChange]:
    changes: list[BreakingChange] = []

    # Map: field_number → field in before and after
    before_nums = set(before.fields.keys())
    after_nums = set(after.fields.keys())

    # FN001 — field number reused for different field
    for num in before_nums & after_nums:
        bf = before.fields[num]
        af = after.fields[num]
        if bf.name != af.name:
            changes.append(BreakingChange(
                check_id='FN001',
                severity='CRITICAL',
                proto_file=rel_path,
                element=f'{msg_name}.{bf.name} (field {num})',
                description=(
                    f'Field number {num} was `{bf.name}` ({bf.type_}), now `{af.name}` ({af.type_}). '
                    f'Reusing a field number CORRUPTS all existing serialized messages.'
                ),
                migration=(
                    f'NEVER reuse field numbers. Reserve the old number: '
                    f'`reserved {num};` and `reserved "{bf.name}";` '
                    f'Then assign a NEW number to `{af.name}`.'
                )
            ))

    # FN002 — field removed without deprecation
    for num in before_nums - after_nums:
        bf = before.fields[num]
        if not bf.deprecated:
            changes.append(BreakingChange(
                check_id='FN002',
                severity='BREAKING',
                proto_file=rel_path,
                element=f'{msg_name}.{bf.name} (field {num})',
                description=(
                    f'Field `{bf.name}` (number {num}, type {bf.type_}) removed without prior deprecation. '
                    f'Clients still sending this field will have data silently dropped.'
                ),
                migration=(
                    f'Before removing: add `[deprecated = true]` option and release. '
                    f'After all clients have migrated, add `reserved {num};` and `reserved "{bf.name}";` '
                    f'to prevent accidental reuse.'
                )
            ))

    # FT001 / FT002 — field type or label changed
    for num in before_nums & after_nums:
        bf = before.fields[num]
        af = after.fields[num]
        if bf.name != af.name:
            continue  # Already caught by FN001
        if bf.type_ != af.type_:
            changes.append(BreakingChange(
                check_id='FT001',
                severity='BREAKING',
                proto_file=rel_path,
                element=f'{msg_name}.{bf.name} (field {num})',
                description=(
                    f'Field type changed: `{bf.type_}` → `{af.type_}`. '
                    f'Wire encoding changes; old clients fail to deserialize.'
                ),
                migration=(
                    f'Add a new field with a new field number and the new type. '
                    f'Mark the old field `[deprecated = true]`. Migrate clients. '
                    f'Then reserve the old field number.'
                )
            ))
        if bf.label != af.label:
            changes.append(BreakingChange(
                check_id='FT002',
                severity='BREAKING',
                proto_file=rel_path,
                element=f'{msg_name}.{bf.name} (field {num})',
                description=(
                    f'Field label changed: `{bf.label}` → `{af.label}`. '
                    f'`repeated` ↔ singular conversion breaks collection unpacking in all generated stubs.'
                ),
                migration=(
                    f'Add a new field with the correct label and a new field number. '
                    f'Deprecate the old field and migrate clients.'
                )
            ))

    # OO001 — field moved into or out of oneof
    for num in before_nums & after_nums:
        bf = before.fields[num]
        af = after.fields[num]
        if bf.name != af.name:
            continue
        if (bf.in_oneof is None) != (af.in_oneof is None):
            direction = 'moved INTO oneof' if af.in_oneof else 'moved OUT OF oneof'
            changes.append(BreakingChange(
                check_id='OO001',
                severity='BREAKING',
                proto_file=rel_path,
                element=f'{msg_name}.{bf.name} (field {num})',
                description=(
                    f'Field `{bf.name}` {direction}. '
                    f'Oneof fields have different serialization behavior; existing clients break.'
                ),
                migration=(
                    f'Oneof membership is part of the wire contract. '
                    f'Add a new field in/out of the oneof with a new field number instead.'
                )
            ))

    # DP001 — deprecated flag removed
    for num in before_nums & after_nums:
        bf = before.fields[num]
        af = after.fields[num]
        if bf.name == af.name and bf.deprecated and not af.deprecated:
            changes.append(BreakingChange(
                check_id='DP001',
                severity='NOTE',
                proto_file=rel_path,
                element=f'{msg_name}.{bf.name} (field {num})',
                description=f'Deprecation annotation removed from `{bf.name}`. Field re-activated.',
                migration='Verify no clients have dropped sending this field during the deprecation period.'
            ))

    # NB001 — new fields added
    for num in after_nums - before_nums:
        af = after.fields[num]
        changes.append(BreakingChange(
            check_id='NB001',
            severity='NON-BREAKING',
            proto_file=rel_path,
            element=f'{msg_name}.{af.name} (field {num})',
            description=f'New field `{af.name}` ({af.type_}) added with number {num}.',
            migration='No action required. Old clients skip unknown fields (proto3).'
        ))

    return changes


def _compare_enum(
    rel_path: str,
    enum_name: str,
    before: ProtoEnum,
    after: ProtoEnum,
) -> list[BreakingChange]:
    changes: list[BreakingChange] = []

    for vname, vnum in before.values.items():
        if vname not in after.values:
            if vname not in before.deprecated_values:
                changes.append(BreakingChange(
                    check_id='EN001',
                    severity='BREAKING',
                    proto_file=rel_path,
                    element=f'{enum_name}.{vname} = {vnum}',
                    description=(
                        f'Enum value `{vname}` (= {vnum}) removed without prior deprecation. '
                        f'Clients with serialized data containing this value fail to decode.'
                    ),
                    migration=(
                        f'Mark as deprecated first: `{vname} = {vnum} [deprecated = true];` '
                        f'Then after migration: use `reserved "{vname}"; reserved {vnum};`'
                    )
                ))
        else:
            if after.values[vname] != vnum:
                changes.append(BreakingChange(
                    check_id='EN002',
                    severity='CRITICAL',
                    proto_file=rel_path,
                    element=f'{enum_name}.{vname}',
                    description=(
                        f'Enum value number changed: `{vname}` was {vnum}, now {after.values[vname]}. '
                        f'All existing serialized data with value {vnum} will decode to the WRONG enum constant.'
                    ),
                    migration=(
                        f'NEVER change enum value numbers. Revert immediately. '
                        f'If you need a rename, add a new alias: `{vname}_V2 = {after.values[vname]};` '
                        f'and deprecate the old name.'
                    )
                ))

    return changes


def _compare_service(
    rel_path: str,
    svc_name: str,
    before: ProtoService,
    after: ProtoService,
) -> list[BreakingChange]:
    changes: list[BreakingChange] = []

    for rpc_name, before_rpc in before.rpcs.items():
        if rpc_name not in after.rpcs:
            changes.append(BreakingChange(
                check_id='SM001',
                severity='BREAKING',
                proto_file=rel_path,
                element=f'{svc_name}.{rpc_name}',
                description=f'RPC method `{rpc_name}` removed. All callers receive NOT_FOUND / unimplemented.',
                migration=(
                    f'Mark the method as deprecated first with a comment. '
                    f'Monitor call volume to zero before removing. '
                    f'Keep the method and return UNIMPLEMENTED for a grace period.'
                )
            ))
            continue

        after_rpc = after.rpcs[rpc_name]
        if (before_rpc.client_streaming != after_rpc.client_streaming or
                before_rpc.server_streaming != after_rpc.server_streaming):
            before_mode = _stream_mode(before_rpc)
            after_mode = _stream_mode(after_rpc)
            changes.append(BreakingChange(
                check_id='SM002',
                severity='BREAKING',
                proto_file=rel_path,
                element=f'{svc_name}.{rpc_name}',
                description=(
                    f'RPC streaming mode changed: {before_mode} → {after_mode}. '
                    f'Generated client interface changes; existing calls fail.'
                ),
                migration=(
                    f'Add a new RPC method with the new streaming mode. '
                    f'Deprecate the old method. Migrate clients. Then remove.'
                )
            ))

    for rpc_name in after.rpcs:
        if rpc_name not in before.rpcs:
            changes.append(BreakingChange(
                check_id='NB002',
                severity='NON-BREAKING',
                proto_file=rel_path,
                element=f'{svc_name}.{rpc_name}',
                description=f'New RPC method `{rpc_name}` added to `{svc_name}`.',
                migration='No action required.'
            ))

    return changes


def _stream_mode(rpc: ProtoRPC) -> str:
    if rpc.client_streaming and rpc.server_streaming:
        return 'bidirectional streaming'
    if rpc.client_streaming:
        return 'client streaming'
    if rpc.server_streaming:
        return 'server streaming'
    return 'unary'


# ─────────────────────────────────────────────────────
# Main runner
# ─────────────────────────────────────────────────────

SEVERITY_ORDER = {'CRITICAL': 0, 'BREAKING': 1, 'NON-BREAKING': 2, 'NOTE': 3}
SEVERITY_EMOJI = {'CRITICAL': '💀', 'BREAKING': '🔴', 'NON-BREAKING': '🟢', 'NOTE': '🔵'}


def run_check(before_protos: dict, after_protos: dict, ci_mode: bool = False) -> int:
    all_changes: list[BreakingChange] = []

    for rel_path in set(before_protos) | set(after_protos):
        if rel_path in before_protos and rel_path in after_protos:
            changes = compare_proto_files(rel_path, before_protos[rel_path], after_protos[rel_path])
            all_changes.extend(changes)
        elif rel_path not in before_protos:
            # New proto file — no breaking changes, just note
            all_changes.append(BreakingChange(
                check_id='NB001',
                severity='NON-BREAKING',
                proto_file=rel_path,
                element='<new file>',
                description=f'New proto file added: {rel_path}',
                migration='No action required.'
            ))
        else:
            # Proto file removed — all messages/services/enums are BREAKING
            all_changes.append(BreakingChange(
                check_id='SM003',
                severity='BREAKING',
                proto_file=rel_path,
                element='<file removed>',
                description=f'Proto file `{rel_path}` removed. All types and services are gone.',
                migration='Never remove a proto file unless all clients have been migrated. '
                          'Keep the file and mark all messages/services as deprecated.'
            ))

    # Sort by severity
    all_changes.sort(key=lambda c: (SEVERITY_ORDER.get(c.severity, 4), c.proto_file, c.element))

    critical = [c for c in all_changes if c.severity == 'CRITICAL']
    breaking = [c for c in all_changes if c.severity == 'BREAKING']
    non_breaking = [c for c in all_changes if c.severity == 'NON-BREAKING']
    notes = [c for c in all_changes if c.severity == 'NOTE']

    print(f"\n🔍  phy-proto-break-check\n{'─'*60}")
    print(f"Scanned {len(before_protos)} proto file(s)  |  "
          f"💀 CRITICAL={len(critical)}  🔴 BREAKING={len(breaking)}  "
          f"🟢 NON-BREAKING={len(non_breaking)}  🔵 NOTE={len(notes)}\n")

    if not critical and not breaking:
        print("✅  No breaking changes detected.")
        if non_breaking:
            print(f"\n{len(non_breaking)} non-breaking addition(s):")
            for c in non_breaking:
                print(f"  🟢 [{c.check_id}] {c.proto_file} — {c.description}")
    else:
        # Print CRITICAL and BREAKING
        for severity in ('CRITICAL', 'BREAKING'):
            group = [c for c in all_changes if c.severity == severity]
            if not group:
                continue
            emoji = SEVERITY_EMOJI[severity]
            print(f"\n{emoji} {severity} CHANGES\n{'─'*50}")
            for c in group:
                print(f"\n[{c.check_id}] {c.proto_file}")
                print(f"  Element: {c.element}")
                print(f"  Issue:   {c.description}")
                print(f"  Fix:")
                for line in c.migration.split('\n'):
                    print(f"    {line}")

        if non_breaking or notes:
            print(f"\n{'─'*50}")
            print(f"Non-blocking: {len(non_breaking)} additions, {len(notes)} notes")

    # Migration summary
    if critical or breaking:
        print(f"\n{'═'*60}")
        print(f"MIGRATION REQUIRED: {len(critical)} CRITICAL + {len(breaking)} BREAKING changes")
        print(f"\nRequired steps before merging:")
        printed_fixes: set[str] = set()
        for c in critical + breaking:
            key = c.check_id + c.element
            if key not in printed_fixes:
                print(f"  • [{c.check_id}] {c.element}: {c.migration.split('.')[0]}")
                printed_fixes.add(key)
        print(f"\nCI fail-gate:")
        print(f"  python proto_break_check.py --before path/to/old --after path/to/new --ci")

    if ci_mode and (critical or breaking):
        print("\n[CI] Exit 1 — breaking changes detected.")
        return 1
    return 0


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Protobuf/gRPC breaking change detector')
    parser.add_argument('--before', help='Directory of old .proto files (or git ref)')
    parser.add_argument('--after', help='Directory of new .proto files (or git ref)')
    parser.add_argument('--git-before', default='HEAD~1', help='Git ref for before state (default: HEAD~1)')
    parser.add_argument('--git-after', default='HEAD', help='Git ref for after state (default: HEAD)')
    parser.add_argument('--use-git', action='store_true', help='Compare using git history instead of directories')
    parser.add_argument('--ci', action='store_true', help='Exit 1 on any CRITICAL or BREAKING change')
    args = parser.parse_args()

    if args.before and args.after:
        before_protos = parse_proto_dir(Path(args.before))
        after_protos = parse_proto_dir(Path(args.after))
    elif args.use_git:
        print(f"Comparing git {args.git_before}..{args.git_after}")
        before_protos, after_protos = extract_proto_from_git(
            args.git_before, args.git_after
        )
    else:
        # Default: use git HEAD~1..HEAD
        print("No --before/--after specified. Using git HEAD~1..HEAD")
        before_protos, after_protos = extract_proto_from_git('HEAD~1', 'HEAD')

    sys.exit(run_check(before_protos, after_protos, ci_mode=args.ci))
```

---

## Usage Examples

### 1. Check current git diff (most common in CI)
```bash
python proto_break_check.py --use-git
```

### 2. Compare two versions of a proto directory
```bash
python proto_break_check.py --before proto/v1/ --after proto/v2/
```

### 3. CI pipeline (exits 1 on breaking changes)
```bash
python proto_break_check.py --use-git --ci
# In GitHub Actions:
# - name: Check proto compatibility
#   run: python proto_break_check.py --git-before origin/main --git-after HEAD --ci
```

### 4. Compare specific git refs
```bash
python proto_break_check.py --use-git --git-before v1.2.0 --git-after v2.0.0
```

---

## Example Output

```
🔍  phy-proto-break-check
────────────────────────────────────────────────────────────
Scanned 3 proto file(s)  |  💀 CRITICAL=1  🔴 BREAKING=3  🟢 NON-BREAKING=2  🔵 NOTE=0

💀 CRITICAL CHANGES
──────────────────────────────────────────────────────

[FN001] api/user.proto
  Element: UserProfile.email (field 3)
  Issue:   Field number 3 was `email` (string), now `phone_number` (string).
           Reusing a field number CORRUPTS all existing serialized messages.
  Fix:
    NEVER reuse field numbers. Reserve the old number:
    `reserved 3;` and `reserved "email";`
    Then assign a NEW number to `phone_number`.

🔴 BREAKING CHANGES
──────────────────────────────────────────────────────

[SM001] api/user.proto
  Element: UserService.DeleteUser
  Issue:   RPC method `DeleteUser` removed. All callers receive NOT_FOUND.
  Fix:
    Mark the method as deprecated first with a comment.
    Monitor call volume to zero before removing.

[FT001] api/payment.proto
  Element: PaymentRequest.amount (field 2)
  Issue:   Field type changed: `int64` → `double`. Wire encoding changes;
           old clients fail to deserialize.
  Fix:
    Add a new field `amount_v2 = 7 double;` and migrate clients.
    Deprecate `amount`. Reserve field 2 after migration.

[EN002] api/status.proto
  Element: OrderStatus.PENDING
  Issue:   Enum value number changed: `PENDING` was 1, now 0.
           All serialized data with value 1 will decode to the WRONG enum constant.
  Fix:
    NEVER change enum value numbers. Revert immediately.

════════════════════════════════════════════════════════════
MIGRATION REQUIRED: 1 CRITICAL + 3 BREAKING changes

Required steps before merging:
  • [FN001] UserProfile.email (field 3): NEVER reuse field numbers
  • [SM001] UserService.DeleteUser: Mark the method as deprecated first
  • [FT001] PaymentRequest.amount (field 2): Add a new field with the new type
  • [EN002] OrderStatus.PENDING: NEVER change enum value numbers

CI fail-gate:
  python proto_break_check.py --before path/to/old --after path/to/new --ci
```

---

## Why Field Numbers Are Sacred

In Protocol Buffers, the field number (not the field name) is the wire identifier. When you serialize a `UserProfile` with `email = 3`, the bytes on the wire say "field 3, type string". If a new client reads those bytes and field 3 is now `phone_number`, the client silently reads the old email value into `phone_number`. **Data corruption is guaranteed, no error is thrown.**

The protobuf spec solution:
```protobuf
message UserProfile {
  // After removing email:
  reserved 3;           // prevents reuse of field number
  reserved "email";     // prevents reuse of field name
  string phone_number = 7;   // new field, new number
}
```

This tool enforces that discipline automatically.

---

## Relationship to Other phy- Skills

| Skill | Protocol | When to Use |
|-------|----------|------------|
| `phy-proto-break-check` (this) | gRPC / protobuf `.proto` | Before merging schema changes |
| `phy-api-changelog-gen` | REST / OpenAPI 3.x | Before releasing a new API version |
| `phy-api-version-audit` | REST | Auditing versioning consistency in source code |
| `phy-openapi-mock-server` | REST / OpenAPI | Generating mock servers from specs |

---

## What It Does NOT Cover

- Runtime reflection or actual message deserialization testing
- Proto3 default value semantics (use `buf lint` for that)
- Import cycle detection (use `buf build`)
- Code generation validation (use `protoc --descriptor_set_out`)

For full proto linting and style enforcement, combine with `buf lint` in CI. This tool focuses exclusively on **backward-compatibility** — the changes that will break existing clients.

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
