"""极简 YAML 解析器（零第三方依赖）。

仅覆盖本技能所需的 YAML 子集：
  - 嵌套 map、list（含 "- key: value" 形式的 list-of-dict）
  - 标量：int / float / bool / null / 字符串（支持单、双引号）
  - 行内注释（引号内的 # 不视为注释）
  - 行内序列 [a, b, c] 与空集合 [] {}
  - 文档分隔符 ---

不支持：锚点/别名、多行块标量 | 与 >。config.yaml / skill.yaml / 分析日志均不使用这些特性。
"""


def _strip_comment(line):
    in_s = in_d = False
    for i, ch in enumerate(line):
        if ch == "'" and not in_d:
            in_s = not in_s
        elif ch == '"' and not in_s:
            in_d = not in_d
        elif ch == "#" and not in_s and not in_d:
            return line[:i]
    return line


def _indent(line):
    return len(line) - len(line.lstrip(" "))


def _split_commas(s):
    parts = []
    cur = []
    in_s = in_d = False
    for ch in s:
        if ch == "'" and not in_d:
            in_s = not in_s
            cur.append(ch)
        elif ch == '"' and not in_s:
            in_d = not in_d
            cur.append(ch)
        elif ch == "," and not in_s and not in_d:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    tail = "".join(cur).strip()
    if tail:
        parts.append(tail)
    return [p.strip() for p in parts]


def _parse_inline_seq(s):
    inner = s[1:-1].strip()
    if not inner:
        return []
    return [_parse_scalar(x) for x in _split_commas(inner)]


def _parse_scalar(s):
    s = s.strip()
    if s == "":
        return ""
    if s == "[]":
        return []
    if s == "{}":
        return {}
    if s.startswith("[") and s.endswith("]"):
        return _parse_inline_seq(s)
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        return s[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    if len(s) >= 2 and s[0] == "'" and s[-1] == "'":
        return s[1:-1].replace("''", "'")
    if s in ("null", "~", "Null", "NULL"):
        return None
    if s in ("true", "True", "TRUE"):
        return True
    if s in ("false", "False", "FALSE"):
        return False
    try:
        if s.lower().startswith("0x"):
            return int(s, 16)
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
    return s


def _parse_map(lines, indent, pos):
    d = {}
    n = len(lines)
    while pos < n:
        line = lines[pos]
        if _indent(line) < indent:
            break
        if _indent(line) > indent:
            pos += 1
            continue
        content = line[indent:]
        if content.startswith("- "):
            break
        if ":" not in content:
            break
        key, _, rest = content.partition(":")
        key = key.strip()
        rest = rest.strip()
        pos += 1
        if rest:
            d[key] = _parse_scalar(rest)
        else:
            val, pos = _parse_nested(lines, indent, pos)
            d[key] = val
    return d, pos


def _is_quoted_string(s):
    """判断 s 是否为一条完整带引号的字符串（如 "https://...")."""
    s = s.strip()
    return len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'"))


def _parse_list(lines, indent, pos):
    items = []
    n = len(lines)
    while pos < n:
        line = lines[pos]
        if _indent(line) < indent:
            break
        if _indent(line) > indent:
            pos += 1
            continue
        content = line[indent:]
        if not content.startswith("- "):
            break
        item = content[2:].strip()
        pos += 1

        if not item:
            val, pos = _parse_nested(lines, indent, pos)
            items.append(val)
        elif ":" in item and not item.startswith(("http://", "https://")) and not _is_quoted_string(item):
            key, _, rest = item.partition(":")
            key = key.strip()
            rest = rest.strip()
            sub = {}
            if rest:
                sub[key] = _parse_scalar(rest)
                item_indent = indent + 2
                while pos < n:
                    ln = lines[pos]
                    if _indent(ln) < indent:
                        break
                    if _indent(ln) == indent and ln[indent:].startswith("- "):
                        break
                    if _indent(ln) == item_indent and ":" in ln[item_indent:]:
                        k2, _, v2 = ln[item_indent:].partition(":")
                        k2 = k2.strip()
                        v2 = v2.strip()
                        pos += 1
                        if v2:
                            sub[k2] = _parse_scalar(v2)
                        else:
                            val, pos = _parse_nested(lines, item_indent, pos)
                            sub[k2] = val
                    else:
                        break
            else:
                val, pos = _parse_nested(lines, indent, pos)
                sub[key] = val
            items.append(sub)
        else:
            items.append(_parse_scalar(item))
    return items, pos


def _parse_nested(lines, parent_indent, pos):
    n = len(lines)
    if pos >= n:
        return None, pos
    child_indent = _indent(lines[pos])
    if child_indent <= parent_indent:
        return None, pos
    if lines[pos][child_indent:].startswith("- "):
        return _parse_list(lines, child_indent, pos)
    return _parse_map(lines, child_indent, pos)


def _parse_block(lines, min_indent, pos):
    n = len(lines)
    while pos < n and _indent(lines[pos]) < min_indent:
        pos += 1
    if pos >= n:
        return None, pos
    first = lines[pos]
    indent = _indent(first)
    content = first[indent:]
    if content.startswith("- "):
        return _parse_list(lines, indent, pos)
    if ":" in content:
        return _parse_map(lines, indent, pos)
    return _parse_scalar(content), pos + 1


def _tokenize(text):
    lines = []
    for raw in text.splitlines():
        s = _strip_comment(raw).rstrip()
        if s.strip() == "":
            continue
        lines.append(s)
    if lines and lines[0].strip() == "---":
        lines = lines[1:]
    return lines


def load(text):
    """解析单份 YAML 文档。"""
    lines = _tokenize(text)
    val, _ = _parse_block(lines, 0, 0)
    return val


def load_all(text):
    """解析多文档 YAML（以 --- 分隔），返回文档列表。"""
    text = text.strip()
    if text.startswith("---"):
        text = text[3:].lstrip("\n")
    docs = [d.strip() for d in text.split("\n---") if d.strip()]
    return [load(d) for d in docs]
