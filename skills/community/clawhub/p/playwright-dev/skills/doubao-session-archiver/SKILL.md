# Doubao Session Archiver - 豆包会话归档

## 技能描述

自动保存豆包会话内容到本地文件夹，支持序号管理、内容提取、worklog 同步。

## 触发条件

- **自动触发**：消息以"豆包"开头
- **手动触发**：用户说"保存豆包"、"归档会话"

## 核心能力

1. **会话保存** - 自动保存到 `doubao-sessions/` 文件夹
2. **序号管理** - 同一天多次会话自动递增（-1, -2, -3...）
3. **内容提取** - 提取工作内容、会议记录、决策项
4. **worklog 同步** - 自动更新 worklog.txt
5. **项目知识库同步** - 刷新对应项目 workload

## 文件命名规则

**格式：** `YYYY-MM-DD (周*) -N worklog.md`

**示例：**
```
doubao-sessions/
├── 2026-03-06 (周五) -1 worklog.md
├── 2026-03-06 (周五) -2 worklog.md
├── 2026-03-07 (周六) -1 worklog.md
└── ...
```

**序号规则：**
- 同一天第一次会话：-1
- 同一天第二次会话：-2
- 新的一天：重置为 -1

## 成功案例（2026-03-06）

### 豆包自动化工作流

**触发词：** "豆包"开头自动处理

**4 步自动执行：**
1. ✅ worklog.txt 更新
2. ✅ 专家点评 HTML 生成
3. ✅ Chrome 自动打开 HTML
4. ✅ TTS 语音 + 飞书发送 + 本地自动播放

**文件归档：** `doubao-sessions/YYYY-MM-DD (周*) -N worklog.md`

### 感知与行动中心会话

**输入：** 豆包会话（项目立项报告分析）
**输出：**
- `doubao-sessions/2026-03-06 (周五) -1 worklog.md`
- `worklog.txt` 更新（添加 4 项完成工作）
- `tasks/projects/感知与行动中心 - 交付域风险管控.md` 更新
- `expert-review-2026-03-06-xiaomi-auto.html` 生成

---

## 工作流程

### 完整流程

```
1. 识别豆包会话 - 消息以"豆包"开头
2. 生成文件名 - 日期 + 序号
3. 保存原始内容 - doubao-sessions/文件名.md
4. 提取工作内容 - 识别 [完成]/[进行中]/[待办]
5. 更新 worklog.txt - 追加到今日记录
6. 识别项目 - 提取项目名称
7. 同步项目知识库 - 刷新项目 workload
8. 生成专家点评 - expert-review-日期 - 主题.html
9. Chrome 自动打开 - 独立窗口显示
10. TTS 语音生成 - MP3 到 Temp 目录
11. 飞书发送 - 文字 + 语音
12. 本地自动播放 - Start-Process
```

### 序号管理逻辑

```powershell
# 获取今日序号
$today = Get-Date -Format "yyyy-MM-dd"
$weekday = Get-Date -Format "ddd"
$pattern = "$today ($weekday) -*.md"
$existingFiles = Get-ChildItem "doubao-sessions" -Filter $pattern

# 计算下一个序号
$nextNum = $existingFiles.Count + 1
$filename = "$today ($weekday) -$nextNum worklog.md"
```

---

## 内容提取规则

### 工作内容识别

**标记格式：**
- `[完成]` - 已完成的工作
- `[进行中]` - 当前进行的工作
- `[待办]` - 计划要做的工作
- `[规划]` - 未来规划的工作

**示例：**
```markdown
### 2026-03-06 (周五)
- [完成] 小米汽车感知与行动中心 - 交付域立项报告分析
- [完成] 供应链数字化项目：异常感知 - 行动反馈闭环系统
- [进行中] 数据治理（第一优先级）
- [规划] 基于 LCR 的产能监控系统
```

### 项目识别

**关键词：**
- 项目名称（如"感知与行动中心"）
- 项目代号（如"XM-2026-001"）
- 业务领域（如"供应链"、"产能监控"）

**同步规则：**
- 识别到项目 → 读取项目卡片
- 添加本周工作 → 更新「项目进度」章节
- 更新最后时间 → 标记同步时间

---

## 文件结构

```
workspace/
├── doubao-sessions/               # 豆包会话归档
│   ├── 2026-03-06 (周五) -1 worklog.md
│   ├── 2026-03-06 (周五) -2 worklog.md
│   └── ...
├── worklog.txt                    # 工作日志（同步更新）
├── tasks/projects/                # 项目知识库（同步更新）
│   ├── 感知与行动中心.md
│   └── ...
└── expert-review-*.html           # 专家点评（可选生成）
```

## 输出格式

### 归档文件格式

```markdown
# 豆包会话归档

**日期：** 2026-03-06 (周五)
**序号：** -1
**原始时间：** 2026-03-06 15:30
**会话主题：** 感知与行动中心立项报告分析

---

## 会话内容

[用户粘贴的豆包会话原始内容]

---

## 提取的工作内容

### 完成
- 感知与行动中心立项报告分析
- 供应链数字化项目设计

### 进行中
- 数据治理

### 待办
- 飞书 OAuth 配置

---

## 关联项目

- 感知与行动中心
- 供应链数字化

---

_自动归档于 2026-03-06 15:35_
```

### worklog.txt 更新格式

```markdown
### 2026-03-06 (周五) - 豆包会话
- [完成] 小米汽车感知与行动中心 - 交付域立项报告分析
- [完成] 供应链数字化项目：异常感知 - 行动反馈闭环系统
- [进行中] 数据治理（第一优先级）
- [规划] 基于 LCR 的产能监控系统
```

---

## 技术实现

### 保存会话（PowerShell）

```powershell
param(
    [string]$Content,
    [string]$SessionDate,
    [string]$SessionTopic
)

$today = Get-Date -Format "yyyy-MM-dd"
$weekday = Get-Date -Format "(ddd)"
$archiveDir = "C:\Users\Xiabi\.openclaw\workspace\doubao-sessions"

# 计算序号
$pattern = "$today $weekday -*.md"
$existingFiles = Get-ChildItem $archiveDir -Filter $pattern -ErrorAction SilentlyContinue
$nextNum = $existingFiles.Count + 1

# 生成文件名
$filename = "$today $weekday -$nextNum worklog.md"
$filepath = Join-Path $archiveDir $filename

# 写入内容
$markdown = @"
# 豆包会话归档

**日期：** $today $weekday
**序号：** -$nextNum
**原始时间：** $(Get-Date -Format 'yyyy-MM-dd HH:mm')
**会话主题：** $SessionTopic

---

## 会话内容

$Content

---

_自动归档于 $(Get-Date -Format 'yyyy-MM-dd HH:mm')_
"@

$markdown | Set-Content $filepath -Encoding UTF8
Write-Host "✅ 会话已归档：$filename"
```

### 更新 worklog.txt

```powershell
$worklogPath = "C:\Users\Xiabi\.openclaw\workspace\worklog.txt"
$content = Get-Content $worklogPath -Raw -Encoding UTF8

# 查找今日记录
$today = Get-Date -Format "yyyy-MM-dd"
$weekday = Get-Date -Format "ddd"
$todayHeader = "### $today ($weekday)"

if ($content -match [regex]::Escape($todayHeader)) {
    # 今日记录已存在，追加内容
    $newContent = $content.Replace($todayHeader, "$todayHeader`n- [完成] 新工作内容")
} else {
    # 创建今日记录
    $newSection = @"

$todayHeader
- [完成] 新工作内容

"@
    $newContent = $content + $newSection
}

$newContent | Set-Content $worklogPath -Encoding UTF8
```

---

## 与豆包专家点评 Skill 的区别

| 维度 | 豆包会话归档 | 豆包专家点评 |
|------|-------------|-------------|
| **主要功能** | 保存原始内容 | 生成专家点评 HTML |
| **输出** | doubao-sessions/*.md | expert-review-*.html |
| **触发** | "豆包"开头 | "豆包"开头 |
| **关系** | 基础功能 | 高级功能（包含归档） |

**协作流程：**
```
豆包会话归档 → 保存原始内容
  ↓
豆包专家点评 → 生成 HTML 报告
```

---

## 用户偏好

- ✅ **自动归档** - 无需确认，自动保存
- ✅ **序号管理** - 同一天自动递增
- ✅ **内容提取** - 自动识别工作内容
- ✅ **worklog 同步** - 自动更新工作日志
- ✅ **项目同步** - 刷新项目知识库

---

## 示例用法

**场景 1：豆包会话**
```
用户："豆包 [会议记录...]"
AI: 
1. 保存 → doubao-sessions/2026-03-07 (周六) -1 worklog.md
2. 提取 → worklog.txt 更新
3. 同步 → 项目知识库刷新
4. 点评 → expert-review-2026-03-07.html
```

**场景 2：手动归档**
```
用户："保存刚才的豆包会话"
AI: 读取最近会话 → 保存到 doubao-sessions/
```

**场景 3：查看归档**
```
用户："查看今天的豆包归档"
AI: 列出 doubao-sessions/2026-03-07*.md 文件
```

---

## 注意事项

1. **序号管理** - 同一天多次会话自动递增
2. **内容完整** - 保存原始内容，不删减
3. **worklog 同步** - 只追加，不覆盖
4. **项目识别** - 准确识别项目名称
5. **编码格式** - UTF-8，避免中文乱码

---

## 参考文档

- 豆包专家点评 Skill：`skills/doubao-expert-review/SKILL.md`
- 工作日志：`worklog.txt`
- 归档目录：`doubao-sessions/`

---

_最后更新：2026-03-07 01:10 - 创建 Skill（参考 2026-03-06 成功案例）_
