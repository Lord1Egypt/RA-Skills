# API 参考

## 1. URL Scheme API

### 基本格式

```
profind:search?name=<keyword>&<param1>=<value1>&<param2>=<value2>
```

所有参数均可自由组合。

### 参数列表

| 参数 | 说明 | 示例 |
|------|------|------|
| `name` | 搜索文件名（支持 glob/regex） | `test`、`*.pdf`、`^doc_[0-9]+` |
| `path` | 搜索根路径 | `~/Documents`、`/Users/Admin` |
| `scope` | 搜索范围 | `all`（含隐藏）、`home`、`selected`、`hidden` |
| `kind` | 文件类型 | `PDF`、`image`、`movie`、`document`、`folder`、`application` |
| `size` | 文件大小 | `larger:1MB`、`smaller:100KB`、`equal:5GB` |
| `date` | 日期范围 | `modified:~week`、`created:~month`、`~year`、`~3month` |
| `label` | 标签颜色 | `red`、`orange`、`yellow`、`green`、`blue`、`purple`、`gray` |
| `meta` | Spotlight 元数据 | `content:<词>`、`author:<人>` |
| `contains` | 文件内容包含 | `contains:text` |
| `exclude` | 排除路径 | `exclude:/Volumes/Network` |
| `script` | 脚本钩子 | `duckduckgo`、`mail` |

### Spotlight 元数据类型

```
content、author、comment、creator、title、subject、keyword、album、artist
```

---

## 2. AppleScript API

### 标准调用

```applescript
tell application "ProFind"
    activate
    open location "profind:search?name=<keyword>"
end tell
```

### 窗口控制

```applescript
tell application "ProFind"
    activate
end tell

tell application "System Events"
    tell process "ProFind"
        -- 新建搜索 Cmd+Opt+F
        keystroke "f" using {command down, option down}
    end tell
end tell
```

---

## 3. Shell 函数封装

```bash
profind_search() {
    local query="$1"
    local kind="${2:-}"
    local path="${3:-}"
    local date="${4:-}"
    
    local url="profind:search?name=${query}"
    [ -n "$kind" ] && url="${url}&kind=${kind}"
    [ -n "$path" ] && url="${url}&path=${path}"
    [ -n "$date" ] && url="${url}&date=${date}"
    
    osascript -e "tell application \"ProFind\" to open location \"$url\"" &
}
```

### 使用方式

```bash
profind_search "report" "PDF" "~/Documents" "modified:~month"
```

---

## 4. Media Server HTTP API（UPnP SOAP）

### 服务信息

| 项目 | 值 |
|------|-----|
| 协议 | UPnP/DLNA SOAP |
| 端口 | 54812（自动分配） |
| 端点 | `/ContentDirectory/control` |
| 支持字段 | `dc:title` |

### SOAP Actions

#### GetSearchCapabilities

```bash
curl -s --max-time 10 -X POST "http://localhost:54812/ContentDirectory/control" \
  -H "Content-Type: text/xml; charset=utf-8" \
  -H 'SOAPACTION: "urn:schemas-upnp-org:service:ContentDirectory:1#GetSearchCapabilities"' \
  -d '<?xml version="1.0" encoding="utf-8"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
  <s:Body>
    <u:GetSearchCapabilities xmlns:u="urn:schemas-upnp-org:service:ContentDirectory:1"/>
  </s:Body>
</s:Envelope>'
```

#### Search

```bash
curl -s --max-time 15 -X POST "http://localhost:54812/ContentDirectory/control" \
  -H "Content-Type: text/xml; charset=utf-8" \
  -H 'SOAPACTION: "urn:schemas-upnp-org:service:ContentDirectory:1#Search"' \
  -d '<?xml version="1.0" encoding="utf-8"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
  <s:Body>
    <u:Search xmlns:u="urn:schemas-upnp-org:service:ContentDirectory:1">
      <ContainerID>0</ContainerID>
      <SearchCriteria>(dc:title contains "keyword")</SearchCriteria>
      <SortCriteria></SortCriteria>
    </u:Search>
  </s:Body>
</s:Envelope>'
```

#### Browse

```bash
curl -s --max-time 10 -X POST "http://localhost:54812/ContentDirectory/control" \
  -H "Content-Type: text/xml; charset=utf-8" \
  -H 'SOAPACTION: "urn:schemas-upnp-org:service:ContentDirectory:1#Browse"' \
  -d '<?xml version="1.0" encoding="utf-8"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
  <s:Body>
    <u:Browse xmlns:u="urn:schemas-upnp-org:service:ContentDirectory:1">
      <ObjectID>0</ObjectID>
      <BrowseFlag>BrowseDirectChildren</BrowseFlag>
      <Filter>*</Filter>
      <StartingIndex>0</StartingIndex>
      <RequestedCount>20</RequestedCount>
      <SortCriteria></SortCriteria>
    </u:Browse>
  </s:Body>
</s:Envelope>'
```

### 目录结构（Browse 返回）

| 容器 ID | 说明 |
|---------|------|
| `0` | 根目录 |
| `Index` | 索引容器 |
| `Recent` | 最近搜索结果 |
| `Series` | 系列/分组 |

---

## 5. 脚本钩子参数

### AppleScript 脚本

| 参数 | 类型 | 说明 |
|------|------|------|
| `currentFile` / `fileItem` | POSIX file | 当前文件路径 |
| `fileList` | list of POSIX file | 所有选中文件路径 |
| `args` / `argsWithoutPaths` | text | 用户额外参数 |
| `urlArguments` | text | URL 解析参数 |
| `numberOfArgs` | integer | 参数个数 |

### Shell 脚本

Shell 脚本通过 `$@` 接收文件路径列表：

```bash
#!/bin/bash
for file in "$@"; do
    echo "处理: $file"
done
```
