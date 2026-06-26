# Joplin CLI 完整命令参考

> 来源：https://joplinapp.org/help/apps/terminal/#shell-mode

## 笔记本命令

### mkbook - 创建笔记本
```bash
joplin mkbook "笔记本名"
```

### use - 切换笔记本
```bash
joplin use "笔记本名"
```
后续操作都在此笔记本内进行。

### ls - 列出内容
```bash
joplin ls /              # 列出所有笔记本
joplin ls                # 列出当前笔记本的笔记
joplin ls -l             # 长格式（含ID、日期、标题）
joplin ls -t n           # 只显示笔记
joplin ls -t t           # 只显示待办
joplin ls -n 10          # 限制数量
joplin ls -s title       # 按标题排序
```

### rmbook - 删除笔记本
```bash
joplin rmbook "笔记本名"
joplin rmbook -f "笔记本名"  # 强制删除，不确认
```

---

## 笔记命令

### mknote - 创建笔记
```bash
joplin mknote "标题"
```

### mktodo - 创建待办
```bash
joplin mktodo "待办事项"
```

### cat - 查看笔记
```bash
joplin cat <id|标题>
joplin cat -v <id>       # 完整信息（含元数据）
```

### set - 设置属性
```bash
joplin set <id> title "新标题"
joplin set <id> body "内容"
joplin set <id> is_todo 1        # 转为待办
joplin set <id> todo_due 1640000000  # 设置截止时间（Unix时间戳）
```

常用属性：
- `title` - 标题
- `body` - 正文
- `parent_id` - 所属笔记本ID
- `is_todo` - 是否为待办（0/1）
- `todo_due` - 待办截止时间
- `todo_completed` - 完成时间

### edit - 编辑笔记
```bash
joplin edit <id>
```
使用配置的编辑器打开（默认自动检测）。

### rmnote - 删除笔记
```bash
joplin rmnote <id|标题>
joplin rmnote -f <id>    # 强制删除
```

---

## 移动和复制

### mv - 移动笔记
```bash
joplin mv <笔记> <目标笔记本>
joplin mv "我的笔记" "工作"
```

### cp - 复制笔记
```bash
joplin cp <笔记> <目标笔记本>
```

### ren - 重命名
```bash
joplin ren <笔记或笔记本> "新名称"
```

---

## 待办操作

### done / undone
```bash
joplin done <id>         # 标记完成
joplin undone <id>       # 标记未完成
```

### todo
```bash
joplin toggle <id>       # 切换完成状态
joplin clear <id>        # 转为普通笔记
```

---

## 标签

### tag - 标签操作
```bash
joplin tag add <标签> <笔记>    # 添加标签
joplin tag remove <标签> <笔记> # 移除标签
joplin tag list                 # 列出所有标签
joplin tag notetags <笔记>      # 列出笔记的标签
```

---

## 同步

### sync - 同步
```bash
joplin sync              # 同步到远程
```

同步目标配置（TUI 模式或命令行）：
```bash
# Nextcloud
joplin config sync.target 5
joplin config sync.5.path "https://example.com/nextcloud/remote.php/webdav/Joplin"
joplin config sync.5.username "用户名"
joplin config sync.5.password "密码"

# WebDAV
joplin config sync.target 6
joplin config sync.6.path "https://webdav.example.com/Joplin"
joplin config sync.6.username "用户名"
joplin config sync.6.password "密码"

# Dropbox
joplin config sync.target 7

# OneDrive
joplin config sync.target 3

# 本地文件系统
joplin config sync.target 2
joplin config sync.2.path "/path/to/sync/dir"
```

---

## 导入导出

### export - 导出
```bash
joplin export /path/to/output --format jex          # JEX 格式
joplin export /path/to/output --format md           # Markdown
joplin export /path/to/output --format md_frontmatter
joplin export /path/to/output --notebook "笔记本名"  # 仅导出指定笔记本
```

### import - 导入
```bash
joplin import /path/to/file.enex     # Evernote
joplin import /path/to/file.jex      # JEX
joplin import /path/to/file.md       # Markdown
```

---

## 配置

### config - 查看/设置配置
```bash
joplin config                    # 查看所有配置
joplin config editor             # 查看特定配置
joplin config editor "vim"       # 设置编辑器
joplin config locale "zh_CN"     # 设置语言
```

常用配置项：
- `editor` - 文本编辑器命令
- `locale` - 语言
- `sync.target` - 同步目标类型
- `sync.interval` - 同步间隔（秒）
- `dateFormat` - 日期格式
- `timeFormat` - 时间格式

---

## 其他

### status - 状态
```bash
joplin status              # 显示笔记和笔记本统计
```

### version - 版本
```bash
joplin version
```

### help - 帮助
```bash
joplin help                # 通用帮助
joplin help all            # 所有命令
joplin help mknote         # 特定命令帮助
```

### attach - 附件
```bash
joplin attach <笔记> /path/to/file
```

### geoloc - 地理位置
```bash
joplin geoloc <笔记>       # 显示笔记的地图链接
```

### batch - 批量执行
```bash
joplin batch /path/to/commands.txt
```
文件中每行一个命令。

---

## 实用技巧

### Cron 定时同步
```bash
*/30 * * * * /usr/local/bin/joplin sync
```

### 通过管道创建笔记
```bash
echo "# 标题\n\n内容" | joplin mknote "标题"
```

### 批量操作
```bash
# 创建笔记本和笔记
joplin mkbook "日记"
joplin use "日记"
joplin mknote "$(date +%Y-%m-%d)"
```