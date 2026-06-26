---
name: profind
description: "ProFind macOS 文件搜索技能 — 毫秒级索引搜索、文件内容全文检索、按大小/日期/类型筛选、批量操作"
version: "1.0.0"
author: Steve-Shi-Web
license: MIT
keywords: ["files", "search", "macos", "spotlight", "productivity"]
---

# ProFind 技能

> macOS 文件搜索工具封装 — 支持 AppleScript 自动化、Shell 脚本钩子、URL Scheme 唤起和内置 HTTP API。

**适用场景：** 深度文件搜索、文件名/内容/元数据查询、按大小/日期/类型筛选、批量操作。

---

## 核心概念

ProFind 是 macOS 上的增强搜索工具，同时支持：
- **Spotlight 索引搜索**（毫秒级）
- **文件系统扫描搜索**（覆盖未索引位置）
- **AppleScript 自动化**（与脚本钩子联动）
- **内置 HTTP API**（程序化搜索）
- **URL Scheme**（从其他应用唤起）

### ProFind 安装检查

```bash
if [ -d "/Applications/ProFind.app" ]; then
    echo "ProFind 已安装: $(defaults read /Applications/ProFind.app/Contents/Info.plist CFBundleShortVersionString 2>/dev/null)"
else
    echo "ProFind 未安装，请从 App Store 下载：https://apps.apple.com/app/id1559203395"
fi
```

---

## 功能列表

| 功能 | 说明 |
|------|------|
| `find_files` | 按文件名搜索，支持 glob/正则 |
| `find_content` | 全文件内容搜索（支持 Spotlight 元数据） |
| `find_advanced` | 高级组合搜索（大小/日期/类型/UTI/标签等） |
| `run_script` | 执行 ProFind 脚本钩子处理搜索结果 |
| `open_search_window` | 打开 ProFind 搜索窗口（可预填查询词） |
| `query_api` | 通过 HTTP API 程序化搜索 |

---

## 搜索策略选择

```
用户查询 → 自动判断使用哪种搜索 → 执行
```

| 情况 | 推荐策略 |
|------|---------|
| 找已知名称的文件 | `find_files`（Spotlight，毫秒级） |
| 搜索文件内容/元数据 | `find_content` |
| 需要多条件组合 | `find_advanced` |
| 需要对结果批量操作 | `run_script` |
| 需要 UI 交互 | `open_search_window` |

---

## 功能详解

---

### 1. find_files — 文件名搜索

> 基于 Spotlight 索引，毫秒级返回。

```bash
# 基本搜索
osascript << 'EOF'
tell application "ProFind"
    activate
    open location "profind:search?name=test&path=~/Documents"
end tell
EOF

# 在指定路径搜索（使用 find 命令找 ProFind 窗口内路径）
# ProFind 支持通过 open location 唤起并传入搜索条件
```

**URL Scheme 格式：**
```
profind:search?name=<搜索词>&path=<路径>&scope=<范围>
```

| 参数 | 说明 | 示例 |
|------|------|------|
| `name` | 搜索文件名 | `test.txt`、`*.pdf` |
| `path` | 搜索根路径（可选） | `~/Documents`、`/Users/Admin` |
| `scope` | 搜索范围 | `all`、`home`、`selected`、`hidden` |

---

### 2. find_content — 内容/元数据搜索

> 使用 Spotlight 查询引擎，支持按内容、作者、UTI、元数据搜索。

```bash
osascript << 'EOF'
tell application "ProFind"
    activate
    
    -- 搜索文件名含 "invoice" 且大小 > 1MB 的 PDF
    open location "profind:search?name=invoice&kind=PDF&size=larger:1MB"
    
    -- 搜索内容含关键字（Spotlight 元数据查询）
    open location "profind:search?name=meeting&meta=content:brainstorm"
    
    -- 按修改日期搜索（最近 7 天内）
    open location "profind:search?name=report&date=modified:~week"
    
    -- 按标签搜索
    open location "profind:search?name=doc&label=red"
end tell
EOF
```

**URL 参数（内容/元数据搜索）：**

| 参数 | 说明 | 示例 |
|------|------|------|
| `kind` | 文件类型 | `PDF`、`image`、`document`、`folder` |
| `meta` | Spotlight 元数据查询 | `content:<词>`、`author:<人>` |
| `size` | 文件大小 | `larger:1MB`、`smaller:100KB`、`equal:5MB` |
| `date` | 日期范围 | `modified:~week`、`created:~month`、`~year`、`~3month` |
| `label` | 标签颜色 | `red`、`orange`、`yellow`、`green`、`blue`、`purple`、`gray` |
| `contains` | 文件内容包含 | `contains:text to find` |

---

### 3. find_advanced — 高级组合搜索

> ProFind 支持的高级搜索条件，通过 AppleScript 脚本直接构建搜索窗口内容。

```bash
osascript << 'EOF'
tell application "ProFind"
    activate
    
    -- 打开搜索窗口
    set queryWin to make new query window with properties {search text:"*.swift"}
    
    -- 设置高级搜索参数（通过 GUI 脚本或直接参数）
    open location "profind:search?name=*.swift&path=/Users&size=larger:0&date=modified:~month&scope=home"
    
end tell
EOF
```

**搜索条件速查：**

| 条件 | URL 值 | 说明 |
|------|--------|------|
| 文件名包含 | `name=test` | 支持 glob `*.pdf`、正则 `file[0-9]+` |
| 隐藏文件 | `scope=all` | 包含隐藏文件 |
| 仅应用 | `kind=application` | 只搜应用 |
| 仅文件夹 | `kind=folder` | 只搜文件夹 |
| 排除文件夹 | `exclude:/Volumes/Network` | 排除指定路径 |
| 正则搜索 | `name=regex:^doc_[0-9]{4}$` | 使用正则表达式 |
| Spotlight 查询 | `kind=spotlightmetadata` | 直接写 mdimporter 查询 |

**常用文件类型（Kind）：**

```
PDF、document、image、movie、music、archive、code、application、folder
```

**Spotlight 元数据类型：**

```
content、author、comment、creator、title、subject、keyword、album、artist
```

---

### 4. run_script — 脚本钩子执行

> ProFind 的"脚本钩子"（Script Actions）功能：搜索完成后对结果文件执行自定义脚本。

**内置脚本钩子（Sample Scripts）：**
```
/Applications/ProFind.app/Contents/Resources/Sample Scripts/
```

| 脚本 | 功能 |
|------|------|
| `Less In Terminal.scpt` | 在 Terminal 用 less 分页查看路径 |
| `Move To Trash.scpt` | 将选中文件移至废纸篓 |
| `Say Paths.scpt` | 朗读文件路径 |
| `Show Strings In Terminal.scpt` | 显示文件的字符串资源 |
| `Open in iTunes.scpt` | 在 iTunes 中打开音频文件 |
| `Word Count.shell` | 统计文件字数 |
| `Print Paths.shell` | 打印文件路径 |
| `mail.scpt` | 发送文件路径邮件 |
| `duckduckgo.scpt` | 用 DuckDuckGo 搜索文件名 |

**通过 ProFind 菜单配置脚本：**
1. 打开 ProFind → **Scripts 菜单**（或右键结果文件）
2. 添加自定义脚本（AppleScript 或 Shell）
3. 脚本接收参数：`fileItem`（当前文件）和 `fileList`（所有选中文件）

**脚本接收的 AppleScript 参数：**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `currentFile` / `fileItem` | POSIX file | 当前选中的文件路径 |
| `fileList` | list of POSIX file | 所有选中的文件路径列表 |
| `args` / `argsWithoutPaths` | text | 用户传入的额外参数（空格分隔） |
| `urlArguments` | text | 解析后的 URL 参数 |
| `numberOfArgs` | integer | 参数个数 |

**自定义脚本示例（Shell — 批量重命名）：**

```bash
#!/bin/bash
# ProFind Shell Script Hook 示例
# 放在 ~/Library/Scripts/ProFind/ 下即可在 ProFind 中调用

for file in "$@"; do
    echo "处理文件: $file"
    # 替换空格为下划线
    newname=$(echo "$(basename "$file")" | sed 's/ /_/g')
    dir=$(dirname "$file")
    if [ "$newname" != "$(basename "$file")" ]; then
        mv "$file" "$dir/$newname"
        echo "重命名为: $newname"
    fi
done
```

**自定义脚本示例（AppleScript — 发送邮件）：**

```applescript
-- 放在 ~/Library/Scripts/ProFind/MailFilePath.scpt
-- 使用方式：在 ProFind 中选中文件 → Scripts → MailFilePath
-- 参数格式：: mail "收件人" "主题"

on open theFiles
    tell application "Mail"
        set theMessage to make new outgoing message with properties ¬
            {subject:"ProFind 文件", content:"附件文件路径:" & linefeed}
        tell theMessage
            repeat with aFile in theFiles
                set content of theMessage to ¬
                    (content of theMessage) & (POSIX path of aFile) & linefeed
            end repeat
            set visible to true
            activate
        end tell
    end tell
end open
```

**通过 run script 执行（AppleScript 调用）：**

```bash
osascript << 'EOF'
-- 调用 ProFind 的 DuckDuckGo 脚本搜索文件名
tell application "ProFind"
    open location "profind:search?name=macOS Ventura&script=duckduckgo"
end tell
EOF
```

---

### 5. open_search_window — 打开搜索窗口

> 打开 ProFind 主窗口，支持预填充搜索条件。

```bash
# 打开 ProFind（全新窗口）
osascript -e 'tell application "ProFind" to activate'

# 带搜索条件打开
osascript << 'EOF'
tell application "ProFind"
    activate
    open location "profind:search?name=report&kind=PDF&path=~/Documents"
end tell
EOF

# 打开并显示高级搜索面板
osascript << 'EOF'
tell application "ProFind"
    activate
    -- 打开搜索窗口后通过菜单触发高级搜索
    tell process "ProFind"
        keystroke "f" using {command down, option down}
    end tell
end tell
EOF
```

**ProFind 快捷键：**
| 快捷键 | 功能 |
|--------|------|
| `Cmd+F` | 新建搜索 |
| `Cmd+O` | 打开选中文件 |
| `Cmd+Return` | 打开选中项 |
| `Space` | 快速预览（QLGenerator） |
| `Cmd+Shift+G` | 前往路径 |
| `Cmd+,` | 偏好设置 |

---

### 6. query_api — Media Server HTTP API

> ProFind 内置 Media Server（UPnP/DLNA 媒体服务器），运行于 **端口 54812**，支持 SOAP 协议搜索。

**⚠️ 重要说明：** Media Server 是 ProFind 搜索结果的 UPnP 暴露接口，不是独立的文件索引 API。需要先在 ProFind UI 中执行搜索，结果才会出现在 Media Server 中。

**启用方式：** ProFind → 偏好设置 → Media Server → 勾选启用

**协议：** UPnP SOAP（非 REST），需通过 SOAP Action 调用：

```bash
PORT=54812

# ① 获取搜索能力
curl -s --max-time 10 -X POST "http://localhost:$PORT/ContentDirectory/control" \
  -H "Content-Type: text/xml; charset=utf-8" \
  -H 'SOAPACTION: "urn:schemas-upnp-org:service:ContentDirectory:1#GetSearchCapabilities"' \
  -d '<?xml version="1.0" encoding="utf-8"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
  <s:Body>
    <u:GetSearchCapabilities xmlns:u="urn:schemas-upnp-org:service:ContentDirectory:1"/>
  </s:Body>
</s:Envelope>'

# ② 搜索文件（dc:title = 文件名）
curl -s --max-time 15 -X POST "http://localhost:$PORT/ContentDirectory/control" \
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

# ③ 浏览目录结构
curl -s --max-time 10 -X POST "http://localhost:$PORT/ContentDirectory/control" \
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

**SOAP Action 速查：**

| Action | 说明 | 端口 |
|--------|------|------|
| `GetSearchCapabilities` | 获取支持的元数据字段 | 54812 |
| `Search` | 按文件名/元数据搜索 | 54812 |
| `Browse` | 浏览索引目录结构 | 54812 |

---

## 使用模式

### 模式一：Shell 脚本封装（推荐）

所有搜索操作通过 `osascript` + URL Scheme 执行：

```bash
profind_search() {
    local query="$1"
    local kind="${2:-}"
    local path="${3:-}"
    
    local url="profind:search?name=${query}"
    [ -n "$kind" ] && url="${url}&kind=${kind}"
    [ -n "$path" ] && url="${url}&path=${path}"
    
    osascript -e "tell application \"ProFind\" to open location \"$url\"" &
}
```

### 模式二：AppleScript 脚本

处理 ProFind 脚本钩子：

```bash
cat > ~/Library/Scripts/ProFind/MyScript.scpt << 'APPLESCRIPT'
on open theFiles
    repeat with aFile in theFiles
        -- 处理每个文件
        do shell script "echo " & (POSIX path of aFile)
    end repeat
end open
APPLESCRIPT
```

---

## 完整示例

### 示例 1：搜索近一个月修改的 PDF 报告

```bash
profind_search() {
    local query="$1"
    local url="profind:search?name=${query}&kind=PDF&date=modified:~month"
    osascript -e "tell application \"ProFind\" to open location \"$url\""
}
profind_search "report"
```

### 示例 2：搜索大于 10MB 的视频文件

```bash
osascript << 'EOF'
tell application "ProFind"
    activate
    open location "profind:search?name=*&kind=movie&size=larger:10MB&scope=all"
end tell
EOF
```

### 示例 3：搜索代码仓库中的 Swift 文件（排除 node_modules）

```bash
osascript << 'EOF'
tell application "ProFind"
    activate
    open location "profind:search?name=*.swift&path=/Users/Admin/Projects&exclude:/Users/Admin/Projects/node_modules"
end tell
EOF
```

### 示例 4：带脚本钩子的搜索（批量操作）

```bash
# 先用 Spotlight 快速定位，再用脚本批量处理
osascript << 'EOF'
tell application "ProFind"
    activate
    open location "profind:search?name=*.log&size=larger:1MB&path=/Users/Admin"
end tell
EOF
# 用户在 ProFind 界面中选择文件 → Scripts → "Move To Trash" 批量删除
```

---

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `Application isn't running` | ProFind 未安装/启动 | `open /Applications/ProFind.app` |
| `URL could not be opened` | URL Scheme 格式错误 | 检查 `profind:` 参数格式 |
| `Permission denied` | 权限不足 | 系统偏好设置 → 隐私与安全性 → 完全磁盘访问 |
| `No results` | Spotlight 索引为空 | 运行 `mdutil -s /` 重建索引 |
| `Script error` | 脚本钩子执行失败 | 检查脚本语法和参数 |

---

## 系统要求

- **macOS 10.14+**
- **ProFind 1.0+**（App Store 下载）
- **完全磁盘访问权限**（系统偏好设置 → 隐私与安全性 → 完全磁盘访问）
  - ProFind 需要此权限才能搜索系统文件夹

---

## 相关文件路径

| 文件 | 路径 |
|------|------|
| ProFind 应用 | `/Applications/ProFind.app` |
| 示例脚本 | `/Applications/ProFind.app/Contents/Resources/Sample Scripts/` |
| 用户脚本 | `~/Library/Scripts/ProFind/` |
| 偏好设置 | `~/Library/Preferences/com.zeroonetwenty.ProFind.plist` |
| 日志 | `~/Library/Logs/ProFind/` |
| 索引数据库 | `~/.ProFind/` |

---

## 快捷命令（CLI 封装）

```bash
# 在 ~/.zshrc 中添加 alias：
alias profind='open -a ProFind'
alias profind-search='profind_search'  # 见上方函数定义'
```
