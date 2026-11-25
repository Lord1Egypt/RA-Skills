#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mini_yaml — 零依赖 YAML 子集解析器（house-skills-kit 兜底用）。

为什么有这个东西：仓库宣传"零依赖"，但 render.py 之前强制要求 PyYAML——
没装 PyYAML 的人克隆下来跑不通第一个命令。本模块用标准库实现品牌配置所需的
YAML 子集，装了 PyYAML 时仍优先用 PyYAML（行为以它为准）。

支持范围（覆盖 template/ 与 examples/ 里所有配置文件的实际用法）：
- 缩进嵌套映射（dict）
- 标量列表（``- item``）
- 双引号 / 单引号 / 裸标量
- 空容器 ``{}`` ``[]``
- 块标量 ``|`` ``|-`` ``|+`` ``>`` ``>-``
- 行内与整行注释（引号内与块标量内不算注释）
- 标量类型推断：true/false/null/整数/浮点（与 PyYAML 的 safe_load 一致）

不支持：锚点/别名、多文档、流式集合（``{a: 1}``）、复杂键、tags。
超出范围请在 contributing 里提，别硬塞。

用法::

    from mini_yaml import safe_load
    cfg = safe_load(open("brand.yaml", encoding="utf-8").read())
"""
import re

__all__ = ["safe_load", "MiniYamlError"]


class MiniYamlError(ValueError):
    """解析失败。"""


_INT_RE = re.compile(r"^[-+]?\d+$")
_FLOAT_RE = re.compile(r"^[-+]?(\d+\.\d*|\.\d+|\d+)([eE][-+]?\d+)?$")


def _indent_of(line):
    return len(line) - len(line.lstrip(" "))


def _is_blank_or_comment(line):
    s = line.strip()
    return s == "" or s.startswith("#")


def _strip_inline_comment(s):
    """去掉未加引号部分的 # 注释。"""
    out, quote = [], None
    for i, ch in enumerate(s):
        if quote:
            out.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in ("'", '"'):
            quote = ch
            out.append(ch)
        elif ch == "#" and (i == 0 or s[i - 1] in " \t"):
            break
        else:
            out.append(ch)
    return "".join(out).rstrip()


def _scalar(text):
    s = _strip_inline_comment(text.strip())
    if s == "":
        return None
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ("'", '"'):
        body = s[1:-1]
        if s[0] == "'":
            return body.replace("''", "'")
        return (body.replace('\\"', '"').replace("\\n", "\n")
                    .replace("\\t", "\t").replace("\\\\", "\\"))
    if s in ("{}", "{ }"):
        return {}
    if s in ("[]", "[ ]"):
        return []
    low = s.lower()
    if low in ("true", "yes", "on"):
        return True
    if low in ("false", "no", "off"):
        return False
    if low in ("null", "~", "none"):
        return None
    if _INT_RE.match(s):
        try:
            return int(s)
        except ValueError:
            return s
    if _FLOAT_RE.match(s) and any(c.isdigit() for c in s):
        try:
            return float(s)
        except ValueError:
            return s
    return s


def _next_content(lines, i):
    while i < len(lines) and _is_blank_or_comment(lines[i]):
        i += 1
    return i


def _read_block_scalar(lines, i, parent_indent, style):
    """读取 ``|`` / ``>`` 块标量，返回 (文本, 下一行索引)。"""
    raw = []
    while i < len(lines):
        line = lines[i]
        if line.strip() == "":
            raw.append("")
            i += 1
            continue
        if _indent_of(line) <= parent_indent:
            break
        raw.append(line)
        i += 1
    # 去掉尾部空行
    while raw and raw[-1] == "":
        raw.pop()
    if not raw:
        return ("" if style[0] == "|" else ""), i
    base = min(_indent_of(l) for l in raw if l.strip())
    body = [l[base:] if l.strip() else "" for l in raw]
    if style[0] == "|":
        text = "\n".join(body)
    else:  # 折叠
        text = " ".join(x.strip() for x in body if x.strip())
    if style.endswith("-"):
        return text, i
    if style.endswith("+"):
        return text + "\n", i
    return text + "\n", i


def _parse_block(lines, i, indent):
    """解析以 indent 为基准缩进的一段，返回 (对象, 下一行索引)。"""
    i = _next_content(lines, i)
    if i >= len(lines):
        return None, i
    first = lines[i]
    if _indent_of(first) < indent:
        return None, i
    if first.strip().startswith("- ") or first.strip() == "-":
        return _parse_list(lines, i, indent)
    return _parse_map(lines, i, indent)


def _parse_list(lines, i, indent):
    items = []
    while True:
        i = _next_content(lines, i)
        if i >= len(lines):
            break
        line = lines[i]
        if _indent_of(line) != indent or not line.strip().startswith("-"):
            break
        rest = line.strip()[1:]
        rest_l = rest.lstrip()
        if rest_l == "":
            j = _next_content(lines, i + 1)
            if j < len(lines) and _indent_of(lines[j]) > indent:
                val, i = _parse_block(lines, j, _indent_of(lines[j]))
                items.append(val)
            else:
                items.append(None)
                i += 1
            continue
        # 形如 "- key: value" 的映射项
        if re.match(r"^[^'\"#][^:]*:(\s|$)", rest_l) and not rest_l.startswith("#"):
            sub_indent = indent + (_indent_of(line) - _indent_of(line)) + 2
            virtual = [" " * sub_indent + rest_l]
            k = i + 1
            while k < len(lines):
                if lines[k].strip() == "":
                    virtual.append("")
                    k += 1
                    continue
                if _indent_of(lines[k]) > indent:
                    virtual.append(lines[k])
                    k += 1
                    continue
                break
            val, _ = _parse_map(virtual, 0, sub_indent)
            items.append(val)
            i = k
            continue
        items.append(_scalar(rest_l))
        i += 1
    return items, i


def _parse_map(lines, i, indent):
    data = {}
    while True:
        i = _next_content(lines, i)
        if i >= len(lines):
            break
        line = lines[i]
        cur = _indent_of(line)
        if cur < indent:
            break
        if cur > indent:
            raise MiniYamlError("第 %d 行缩进异常：%r" % (i + 1, line))
        s = line.strip()
        if s.startswith("- "):
            break
        if ":" not in s:
            raise MiniYamlError("第 %d 行缺少冒号：%r" % (i + 1, line))
        key_raw, _, val_raw = s.partition(":")
        key = key_raw.strip().strip("'\"")
        val_raw = val_raw.strip()
        # 块标量（| |- |+ > >- >+）
        m = re.match(r"^([|>][+-]?)$", _strip_inline_comment(val_raw))
        if m:
            text, i = _read_block_scalar(lines, i + 1, indent, m.group(1))
            data[key] = text
            continue
        cleaned = _strip_inline_comment(val_raw)
        if cleaned == "":
            j = _next_content(lines, i + 1)
            if j < len(lines) and _indent_of(lines[j]) > indent:
                data[key], i = _parse_block(lines, j, _indent_of(lines[j]))
            elif (j < len(lines) and _indent_of(lines[j]) == indent
                  and lines[j].strip().startswith("- ")):
                data[key], i = _parse_list(lines, j, indent)
            else:
                data[key] = None
                i += 1
            continue
        data[key] = _scalar(cleaned)
        i += 1
    return data, i


def safe_load(stream):
    """解析 YAML 文本或文件对象，返回 dict / list。"""
    text = stream.read() if hasattr(stream, "read") else stream
    if text.startswith("\ufeff"):
        text = text[1:]
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    i = _next_content(lines, 0)
    if i >= len(lines):
        return None
    if lines[i].strip() == "---":
        i = _next_content(lines, i + 1)
    value, _ = _parse_block(lines, i, _indent_of(lines[i]))
    return value
