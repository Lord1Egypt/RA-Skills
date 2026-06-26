# 自定义脚本示例

## 内置脚本钩子

位于：`/Applications/ProFind.app/Contents/Resources/Sample Scripts/`

| 脚本 | 类型 | 功能 |
|------|------|------|
| `Less In Terminal.scpt` | AppleScript | 在 Terminal 用 less 分页查看文件路径 |
| `Move To Trash.scpt` | AppleScript | 将选中文件移至废纸篓 |
| `Say Paths.scpt` | AppleScript | 朗读选中文件路径 |
| `Show Strings In Terminal.scpt` | AppleScript | 显示文件的字符串资源 |
| `Open in iTunes.scpt` | AppleScript | 在 iTunes 中打开音频文件 |
| `Word Count.shell` | Shell | 统计选中文件的字数 |
| `Print Paths.shell` | Shell | 打印文件路径 |
| `mail.scpt` | AppleScript | 将文件路径发送邮件 |
| `duckduckgo.scpt` | AppleScript | 用 DuckDuckGo 搜索文件名 |

---

## 自定义脚本

自定义脚本放在 `~/Library/Scripts/ProFind/` 目录下。

### Shell 脚本

#### 批量重命名（空格 → 下划线）

```bash
#!/bin/bash
# BatchRename.sh
# 放置路径：~/Library/Scripts/ProFind/BatchRename.sh

for file in "$@"; do
    filename=$(basename "$file")
    dirname=$(dirname "$file")
    newname=$(echo "$filename" | sed 's/ /_/g')
    if [ "$newname" != "$filename" ]; then
        mv "$file" "$dirname/$newname"
        echo "✓ 重命名: $filename → $newname"
    fi
done
```

#### 文件属性报告

```bash
#!/bin/bash
# FileInfo.sh

for file in "$@"; do
    echo "=== $(basename "$file") ==="
    echo "路径: $file"
    echo "大小: $(du -h "$file" | cut -f1)"
    echo "修改: $(stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$file")"
    echo "类型: $(file -b "$file")"
    echo ""
done
```

### AppleScript

#### 发送文件路径邮件

```applescript
-- MailFilePaths.scpt
-- 使用方式：选中文件 → Scripts → MailFilePaths
-- 参数格式（在搜索框输入）：: mail "收件人@example.com" "邮件主题"

on open theFiles
    set fileCount to (count of theFiles)
    if fileCount is 0 then
        display dialog "请先选中文件" buttons {"OK"} default button 1
        return
    end if
    
    set pathList to ""
    repeat with aFile in theFiles
        set pathList to pathList & (POSIX path of aFile) & linefeed
    end repeat
    
    tell application "Mail"
        set theMessage to make new outgoing message with properties ¬
            {subject:"ProFind 文件路径 (" & fileCount & " 个文件)", ¬
             content:"ProFind 文件路径列表:" & linefeed & linefeed & pathList}
        tell theMessage
            set visible to true
            activate
        end tell
    end tell
end open
```

#### 复制路径到剪贴板

```applescript
-- CopyPaths.scpt
-- 选中文件 → 路径复制到剪贴板

on open theFiles
    set pathList to ""
    repeat with aFile in theFiles
        set pathList to pathList & (POSIX path of aFile) & linefeed
    end repeat
    
    tell application "System Events"
        set the clipboard to pathList
    end tell
    
    display notification "已复制 " & (count of theFiles) & " 个路径到剪贴板"
end open
```

#### 用 VS Code 打开文件

```applescript
-- OpenInVSCode.scpt
-- 选中文件 → 在 VS Code 中打开

on open theFiles
    repeat with aFile in theFiles
        set posixPath to POSIX path of aFile
        do shell script "open -a 'Visual Studio Code' " & quoted form of posixPath
    end repeat
end open
```

---

## 脚本参数参考

### AppleScript 脚本接收的参数

```applescript
-- 入口函数：on open(theFiles)
-- theFiles：选中文件列表（alias 列表）

on open theFiles
    -- 文件数量
    set fileCount to count of theFiles
    
    -- 获取每个文件的 POSIX 路径
    repeat with aFile in theFiles
        set aPath to POSIX path of aFile
        -- 处理文件...
    end repeat
end open

-- 命令行参数入口：on run argv
on run argv
    -- argv[1] = 第一个参数
    -- argv[2] = 第二个参数
end run
```

### Shell 脚本接收的参数

```bash
# $@ = 所有文件路径（空格分隔）
# $1, $2, ... = 逐个文件路径

for file in "$@"; do
    echo "$file"
done
```

---

## 调试技巧

### 在 Script Editor 中调试

```applescript
-- 在脚本开头加入日志输出
log "开始处理文件"
try
    -- 脚本逻辑
on error errMsg number errNum
    log "错误: " & errMsg & " (编号: " & errNum & ")"
end try
```

### 查看 ProFind 脚本菜单

1. 在 ProFind 中执行一次搜索
2. 选中结果文件
3. 点击顶部菜单 **Scripts** 查看自定义脚本列表
