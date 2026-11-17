# -*- coding: utf-8 -*-
"""最小 YAML 解析器：仅支持本项目 config.yaml 的固定 schema 子集。

支持：嵌套映射（空格缩进）、映射列表（- key: value）、纯标量列表、
引号字符串、int/bool/None、注释、空行、行内流式列表 [a, b]。
不支持：锚点、多文档、块标量等——超出 schema 的输入直接报错。
"""
import re


class YamlMiniError(Exception):
    pass


def _strip_comment(line):
    """去掉注释（# 前须有空白或位于行首，引号内的 # 不算注释）。"""
    in_s = None
    for i, ch in enumerate(line):
        if in_s:
            if ch == in_s:
                in_s = None
        elif ch in ('"', "'"):
            in_s = ch
        elif ch == '#' and (i == 0 or line[i - 1] in ' \t'):
            return line[:i]
    return line


def _split_flow(inner):
    """按逗号切分流式列表内容（引号内的逗号不切）。"""
    parts, buf, in_s = [], [], None
    for ch in inner:
        if in_s:
            buf.append(ch)
            if ch == in_s:
                in_s = None
        elif ch in ('"', "'"):
            in_s = ch
            buf.append(ch)
        elif ch == ',':
            parts.append(''.join(buf))
            buf = []
        else:
            buf.append(ch)
    if buf:
        parts.append(''.join(buf))
    return parts


def _scalar(s):
    """标量解析：引号串 / bool / int / float / null / 流式列表。"""
    s = s.strip()
    if s == '':
        return None
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ('"', "'"):
        return s[1:-1]
    low = s.lower()
    if low in ('true', 'yes'):
        return True
    if low in ('false', 'no'):
        return False
    if low in ('null', '~'):
        return None
    if s == '[]':
        return []
    if s == '{}':
        return {}
    if s.startswith('[') and s.endswith(']'):
        return [_scalar(p) for p in _split_flow(s[1:-1])]
    if re.fullmatch(r'-?\d+', s):
        return int(s)
    if re.fullmatch(r'-?\d+\.\d+', s):
        return float(s)
    return s


def _split_kv(content):
    """切分 'key: value'。返回 (key, value)；无合法分隔符返回 (None, None)。"""
    in_s = None
    for i, ch in enumerate(content):
        if in_s:
            if ch == in_s:
                in_s = None
        elif ch in ('"', "'"):
            in_s = ch
        elif ch == ':':
            if i == len(content) - 1 or content[i + 1] in ' \t':
                key = content[:i].strip()
                if key and '"' not in key and "'" not in key:
                    return key, content[i + 1:].strip()
    return None, None


def load(text):
    """解析 YAML 文本为 dict；语法不支持时抛 YamlMiniError。"""
    lines = []
    for no, raw in enumerate(text.splitlines(), 1):
        line = _strip_comment(raw).rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(' '))
        if '\t' in line[:indent]:
            raise YamlMiniError(f'第 {no} 行：不支持 Tab 缩进')
        lines.append((indent, line.strip(), no))
    if not lines:
        return {}
    val, idx = _parse_block(lines, 0, lines[0][0])
    if idx != len(lines):
        raise YamlMiniError(f'第 {lines[idx][2]} 行附近：无法解析的内容')
    return val


def _parse_block(lines, i, indent):
    if lines[i][1] == '-' or lines[i][1].startswith('- '):
        return _parse_list(lines, i, indent)
    return _parse_map(lines, i, indent)


def _parse_map(lines, i, indent):
    result = {}
    while i < len(lines):
        ind, content, no = lines[i]
        if ind < indent:
            break
        if ind > indent:
            raise YamlMiniError(f'第 {no} 行：意外的缩进')
        if content == '-' or content.startswith('- '):
            break
        key, val = _split_kv(content)
        if key is None:
            raise YamlMiniError(f'第 {no} 行：应为 "key: value"，实为 {content!r}')
        if val:
            result[key] = _scalar(val)
            i += 1
        else:
            # 子块：更深缩进，或与 key 同缩进的序列
            if i + 1 < len(lines):
                nind, ncontent, _ = lines[i + 1]
                if nind > indent:
                    child, i = _parse_block(lines, i + 1, nind)
                    result[key] = child
                    continue
                if nind == indent and (ncontent == '-' or ncontent.startswith('- ')):
                    seq, i = _parse_list(lines, i + 1, indent)
                    result[key] = seq
                    continue
            result[key] = None
            i += 1
    return result, i


def _parse_list(lines, i, indent):
    result = []
    while i < len(lines):
        ind, content, _ = lines[i]
        if ind != indent or not (content == '-' or content.startswith('- ')):
            break
        after = content[1:]
        stripped = after.lstrip(' ')
        key_col = indent + 1 + (len(after) - len(stripped))
        if not stripped:
            # 块状列表项：内容在后续更深缩进行
            if i + 1 < len(lines) and lines[i + 1][0] > indent:
                v, i = _parse_block(lines, i + 1, lines[i + 1][0])
                result.append(v)
            else:
                result.append(None)
                i += 1
            continue
        key, val = _split_kv(stripped)
        if key is None:
            result.append(_scalar(stripped))
            i += 1
            continue
        # 映射列表项：首个键值对在 "-" 行内，其余键在 key_col 缩进行
        item = {}
        if val:
            item[key] = _scalar(val)
        else:
            if i + 1 < len(lines) and lines[i + 1][0] > key_col:
                v, i = _parse_block(lines, i + 1, lines[i + 1][0])
                item[key] = v
                result.append(item)
                continue
            item[key] = None
        i += 1
        while i < len(lines):
            ind2, content2, no2 = lines[i]
            if ind2 != key_col or content2 == '-' or content2.startswith('- '):
                break
            k2, v2 = _split_kv(content2)
            if k2 is None:
                raise YamlMiniError(f'第 {no2} 行：列表项内应为 "key: value"，实为 {content2!r}')
            if v2:
                item[k2] = _scalar(v2)
                i += 1
            else:
                if i + 1 < len(lines) and lines[i + 1][0] > key_col:
                    v, i = _parse_block(lines, i + 1, lines[i + 1][0])
                    item[k2] = v
                else:
                    item[k2] = None
                    i += 1
        result.append(item)
    return result, i
