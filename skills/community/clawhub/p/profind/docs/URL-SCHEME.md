# URL Scheme 速查

## 基础格式

```
profind:search?name=<搜索词>
```

所有参数用 `&` 串联，无空格。

---

## 参数速查表

### 基础参数

| 参数 | 值示例 | 说明 |
|------|--------|------|
| `name` | `test`、`*.pdf`、`^doc_` | 搜索文件名，支持 glob/regex |
| `path` | `~/Documents` | 搜索根路径 |
| `scope` | `all`、`home`、`hidden` | 搜索范围 |

### 文件类型（kind）

```
PDF、document、image、movie、music、audio、archive、
code、application、folder、bookmark
```

### 大小（size）

| 格式 | 示例 |
|------|------|
| 大于 | `size=larger:1MB` |
| 小于 | `size=smaller:100KB` |
| 等于 | `size=equal:5GB` |

支持单位：`B` / `KB` / `MB` / `GB`

### 日期（date）

| 格式 | 说明 |
|------|------|
| `modified:~week` | 最近 7 天内修改 |
| `modified:~month` | 最近 30 天内修改 |
| `modified:~year` | 最近 1 年内修改 |
| `created:~3month` | 最近 3 个月内创建 |

### 标签（label）

```
red、orange、yellow、green、blue、purple、gray
```

### Spotlight 元数据（meta）

| 示例 | 说明 |
|------|------|
| `meta=author:John` | 按作者搜索 |
| `meta=content:report` | 按内容搜索 |
| `meta=keyword:financial` | 按关键词搜索 |

### 其他

| 参数 | 示例 |
|------|------|
| `exclude` | `exclude:/Volumes/Network` |
| `script` | `script=duckduckgo` |

---

## 常用场景模板

### 搜索 Documents 中的 PDF

```
profind:search?name=*.pdf&path=~/Documents
```

### 搜索近一个月修改的大文件

```
profind:search?name=*&date=modified:~month&size=larger:10MB
```

### 搜索隐藏文件

```
profind:search?name=.*&scope=all
```

### 搜索指定类型（排除某路径）

```
profind:search?name=*.xlsx&path=~/Documents&exclude:~/Documents/Archive
```

### 正则搜索

```
profind:search?name=regex:^data_[0-9]{8}\.csv$
```

---

## 调用方式

### AppleScript

```applescript
open location "profind:search?name=report&kind=PDF&date=modified:~month"
```

### Shell

```bash
osascript -e 'tell application "ProFind" to open location "profind:search?name=report"'
```

### Terminal

```bash
open "profind:search?name=*.pdf&path=~/Downloads"
```
