---
name: jf-watchdog
description: 杰峰看门狗技能。基于杰峰设备抓图 + AI 视觉分析的通用区域状态监控，支持物品防盗、通道占用检测、人员存在检测等场景。
metadata:
  version: 1.1.0
  author: User
  category: analytics
  tags:
    - 杰峰
    - 看门狗
    - 区域监控
    - 物品防盗
    - 通道占用
    - 智能巡检
  triggers:
    - 看门狗
    - 看门狗巡检
    - 监控巡检
    - 检查一下
    - 巡逻
    - 巡逻一次
    - 添加监控
    - 配置看门狗
    - 设置监控区域
    - 查看监控
    - 定时巡检
    - 自动巡检
  prerequisites:
    - 配置必需的环境变量（JF_UUID, JF_APP_KEY, JF_APP_SECRET, JF_MOVE_CARD）
    - 设备需已完成配网和绑定
    - 设备需在线
    - 已安装依赖技能（jf-open-pro-device-list）
  region:
    - CN: api-cn.jftechws.com (中国大陆)
    - AS: api-as.jftechws.com (亚洲)
    - EU: api-eu.jftechws.com (欧洲)
    - NA: api-na.jftechws.com (北美洲)
---

# jf-watchdog — 杰峰看门狗技能

## 技能描述

通过杰峰监控设备云抓图 + Agent 视觉分析，对监控画面中指定区域进行状态监控：

- **物品防盗/在位监控** — 监控特定位置是否有物品存在（展品、设备、灭火器等），物品消失则报警
- **通道/出入口占用检测** — 监控消防通道、应急出口等区域是否被物品堵塞，有物品出现则报警
- **人员/车辆存在检测** — 监控某个区域是否有人/车辆等目标出现或消失
- **通用区域状态监控** — 用户自定义框选区域并定义"应该有什么"，系统检测是否符合

Agent 先通过视觉分析自动识别画面中的物品和区域，以文字交互方式让用户选择监控目标；也可通过交互式 Widget 手动框选精确区域。系统后续通过抓图对比分析区域变化，发现异常时输出报告。

## 触发词

看门狗 / 看门狗巡检 / 监控巡检 / 检查一下 / 巡逻 / 巡逻一次 / 添加监控 / 配置看门狗 / 设置监控区域 / 查看监控 / 定时巡检 / 自动巡检

## 依赖技能

| 依赖技能 | 用途 | 是否必需 |
|----------|------|----------|
| `jf-open-pro-device-list` | 添加监控设备时查询已绑定设备列表 | 是（添加设备时） |
| `jf-open-pro-device-status` | 添加监控设备时验证设备在线状态 | 可选 |

抓图、下载和裁剪由本技能自带的 `scripts/watchdog.py` 完成。

## 前置条件

### 环境变量

| 变量名 | 说明 | 默认值 | 必需 |
|--------|------|--------|------|
| `JF_UUID` | 开放平台用户 uuid | - | 是 |
| `JF_APP_KEY` | 开放平台应用 appKey | - | 是 |
| `JF_APP_SECRET` | 开放平台应用密钥 | - | 是 |
| `JF_MOVE_CARD` | 移动卡标识（用于签名） | `2` | 是 |
| `JF_ENDPOINT` | API 接入地址 | `api-cn.jftechws.com` | 否 |

### Python 依赖

```bash
pip install requests Pillow
```

Pillow 用于图片裁剪功能。

## 配置文件

`config/monitors.json` 存储所有监控配置：

```json
{
  "monitors": [
    {
      "sn": "设备序列号",
      "name": "展厅A",
      "password": "设备密码",
      "location": "一楼展厅",
      "channel": 0,
      "regions": [
        {
          "id": "region_1",
          "name": "灭火器位置",
          "x": 100,
          "y": 200,
          "width": 300,
          "height": 400,
          "rule": "此区域应该始终有一个红色灭火器",
          "alert_when": "missing",
          "baseline": {
            "image": "baselines/xxx_region_1_baseline.png",
            "description": "画面中有一个红色灭火器，放置在墙角白色区域",
            "captured_at": "2026-06-05T14:30:00+08:00"
          }
        }
      ]
    }
  ],
  "settings": {
    "default_channel": 0,
    "sensitivity": "moderate"
  }
}
```

**monitors 数组 — 每台监控设备：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `sn` | string | 杰峰设备序列号（唯一标识） |
| `name` | string | 用户定义的设备显示名称 |
| `password` | string | 设备密码（用于自动获取 Token） |
| `location` | string | 位置描述 |
| `channel` | int | 抓图通道号（默认 0） |
| `regions` | array | 该设备下的监控区域列表 |

**regions 数组 — 每个监控区域：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 区域唯一标识（自动生成，格式 `region_{N}`，N 为自增序号） |
| `name` | string | 区域名称（用户定义，如"灭火器位置"） |
| `x` | int | 矩形左上角 X 坐标（像素坐标） |
| `y` | int | 矩形左上角 Y 坐标（像素坐标） |
| `width` | int | 矩形宽度（像素） |
| `height` | int | 矩形高度（像素） |
| `rule` | string | 自然语言规则描述 |
| `alert_when` | string | 报警触发条件：`missing`（应有物品消失）/ `appeared`（不应有物品出现）/ `changed`（状态发生变化）。Agent 以规则文本为主要判断依据，`alert_when` 作为辅助提示 |
| `baseline.image` | string | 基线裁剪图的相对路径 |
| `baseline.description` | string | Agent 生成的基线状态文字描述 |
| `baseline.captured_at` | string | 基线采集时间（ISO 8601） |

**settings 对象：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `default_channel` | int | 默认抓图通道号 |
| `sensitivity` | string | 分析敏感度：`low` / `moderate` / `high` |

## 基线机制

### 基线保存

当区域选择完成后（无论是 Agent 智能识别还是 Widget 手动框选）：

1. 脚本根据区域坐标（x, y, width, height）裁剪原始抓图
2. 裁剪图保存到 `baselines/{sn}_{regionId}_baseline.png`
3. Agent 使用 Read 工具查看基线图片，生成文字描述（描述区域中的物品、颜色、布局等）
4. 裁剪图路径、文字描述、采集时间一起写入 `monitors.json`

### 巡检对比

1. 抓取新的实时图
2. 脚本按区域坐标裁剪当前图片
3. Agent 对每个区域同时查看三样内容：基线图片、当前裁剪图、规则描述
4. Agent 综合判断：当前状态是否与基线一致、是否符合规则

## 核心工作流

### 工作流 0: 引导使用（首次对话 / 帮助）

**触发：** 用户说"看门狗"、"看门狗怎么用"、"配置监控"，或 Agent 判断用户是首次使用。

**流程：**

Agent 先静默检查环境变量（JF_UUID, JF_APP_KEY, JF_APP_SECRET）和 `config/monitors.json` 状态。

#### 第一步：环境检查（静默执行，不告诉用户"我在检查"）

1. 读取 `config/monitors.json`，检查 monitors 列表是否为空。
2. 检查环境变量 `JF_UUID`、`JF_APP_KEY`、`JF_APP_SECRET` 是否已设置（通过 `echo %JF_UUID%` 或 Bash 命令）。

#### 第二步：根据状态引导

**情况 A — 全新状态（无监控点、无环境变量）：**

```
你好！我来帮你搭建看门狗区域监控系统。

这个系统能做什么：
- 通过杰峰摄像头抓图，用 AI 分析指定区域的状态变化
- 支持物品防盗、通道占用检测、人员存在检测等场景
- 自动输出巡检报告，标注异常区域
- 支持定时自动巡检，结果推送到 IM 频道

搭建只需要 2 步：

1. 配置环境变量（JF_UUID, JF_APP_KEY 等）
2. 添加监控设备和区域

我们先从配置环境变量开始，好吗？说"开始"就行。
```

**情况 B — 有环境变量，无监控点：**

```
环境变量已就绪！接下来需要添加监控设备。

说"添加监控"，我会帮你从已绑定的设备中选择并配置监控区域。
```

**情况 C — 有监控点，就绪状态：**

```
一切就绪！当前配置：

监控设备：{列出设备名称}
监控区域：{列出区域数量}
敏感度：{sensitivity}

现在可以：
- "巡逻一次" — 立即对所有监控区域抓图分析
- "检查 展厅A" — 只检查指定设备
- "查看监控" — 管理监控配置
- "定时巡检" — 设置自动巡检

需要做什么？
```

**注意事项：**
- 引导对话要简洁，不要一次输出太多信息
- 如果用户明确说做什么，跳过引导直接进入对应工作流

### 工作流 1: 配置监控点

**触发：** 用户说"添加监控"、"配置看门狗"、"设置监控区域"

**流程：**

#### 步骤 1 — 查询设备列表

使用 `jf-open-pro-device-list` 技能查询可用设备列表。

#### 步骤 2 — 用户选择设备

展示设备列表让用户选择（显示 SN 和昵称）。询问用户：给设备起个名字（如"展厅A"）、位置描述（如"一楼展厅"）。

#### 步骤 3 — 单设备抓图

运行抓图脚本（设置 PYTHONIOENCODING=utf-8）：

```bash
PYTHONIOENCODING=utf-8 python {skill_dir}/scripts/watchdog.py \
  --action capture-single \
  --device-sn {SN} \
  --device-name {名称} \
  --password {密码} \
  --output-dir {workspace}/captures/ \
  --json
```

脚本输出 JSON 包含抓图 URL 和本地下载路径。

#### 步骤 4 — Agent 智能识别画面内容（推荐模式）

Agent 使用 Read 工具查看抓图（本地路径），对画面进行全面视觉分析：

1. **识别所有可监控的物品和区域**，包括但不限于：
   - 固定物品（灭火器、设备、家具、展品等）
   - 通道和出入口区域
   - 墙面、地面等空白区域
   - 人员可能出现的区域
2. **为每个识别到的目标估计矩形坐标**（像素坐标，基于图片尺寸）
3. **为每个目标生成监控建议**，包括：
   - 序号标记（①②③...）
   - 物品/区域名称
   - 建议的监控规则（自然语言）
   - 建议的报警类型（missing / appeared / changed）

#### 步骤 5 — 文字交互选择区域（主要方式）

Agent 将识别结果以文字交互的方式呈现给用户：

```
我在画面中识别到以下可监控的目标：

① {物品名称} — {位置描述}，{当前状态描述}
   建议规则：「{规则描述}」
   报警类型：{missing/appeared/changed}

② {物品名称} — {位置描述}，{当前状态描述}
   建议规则：「{规则描述}」
   报警类型：{missing/appeared/changed}

③ ...

你可以：
- 选择要监控的区域（多选）
- 说"用交互页面自定义"打开 Widget 手动框选精确区域
- 说"全部都要"监控所有识别到的区域
```

使用 AskUserQuestion 工具让用户多选要监控的区域（multiSelect: true），同时提供"用交互页面自定义"选项。

**如果用户选择"用交互页面自定义"：** 跳转到步骤 5b（Widget 模式）。

**如果用户选择了具体区域：** 进入步骤 6。

#### 步骤 5b — Widget 交互模式（备选）

如果用户选择使用 Widget 自定义，或 Agent 无法准确识别画面内容时：

使用 `show_widget` 渲染交互式区域配置界面：

```
show_widget(
  widget_path='jf-watchdog/assets/watchdog-config-widget.html',
  data={
    "imageUrl": "抓图URL",
    "localPath": "本地抓图路径",
    "deviceSn": "设备SN",
    "deviceName": "设备名称",
    "imageWidth": 1920,
    "imageHeight": 1080,
    "existingRegions": []
  }
)
```

如果是编辑已有设备，将已有区域数据传入 `existingRegions` 供 Widget 回显。

用户在 Widget 中拖拽绘制矩形、设置名称和规则，点击「生成配置」输出 JSON。

#### 步骤 6 — 构建区域配置

**文字交互模式：** 根据用户选择的区域和 Agent 在步骤 4 中估计的坐标，构建区域配置 JSON。Agent 需要对每个选中区域精确估算矩形坐标（x, y, width, height），确保覆盖目标物品/区域。

**Widget 模式：** 直接使用 Widget 输出的 JSON。

区域配置 JSON 格式：

```json
{
  "device_sn": "xxx",
  "device_name": "展厅A",
  "source_image": "本地抓图路径",
  "regions": [
    {
      "id": "region_1",
      "name": "灭火器位置",
      "x": 100, "y": 200, "width": 300, "height": 400,
      "rule": "此区域应该始终有一个红色灭火器",
      "alert_when": "missing"
    }
  ],
  "image_size": { "width": 1920, "height": 1080 }
}
```

#### 步骤 7 — 裁剪基线图片

对每个区域，运行基线裁剪：

```bash
PYTHONIOENCODING=utf-8 python {skill_dir}/scripts/watchdog.py \
  --action crop-baselines \
  --source-image {抓图本地路径} \
  --device-sn {SN} \
  --regions-json '{区域配置JSON}' \
  --output-dir {skill_dir}/baselines/ \
  --json
```

裁剪图保存到 `baselines/{sn}_{regionId}_baseline.png`。

#### 步骤 8 — Agent 生成基线描述

对每个区域的基线裁剪图，Agent 使用 Read 工具查看图片，生成文字描述：
- 描述区域中的物品、颜色、布局等视觉特征
- 描述应具体，便于后续巡检时对比（如"画面中有一个红色灭火器，放置在墙角白色区域"）

#### 步骤 9 — 写入配置

将完整配置写入 `config/monitors.json`，包含基线信息：

```json
{
  "sn": "设备SN",
  "name": "展厅A",
  "password": "设备密码",
  "location": "一楼展厅",
  "channel": 0,
  "regions": [
    {
      "id": "region_1",
      "name": "灭火器位置",
      "x": 100, "y": 200, "width": 300, "height": 400,
      "rule": "此区域应该始终有一个红色灭火器",
      "alert_when": "missing",
      "baseline": {
        "image": "baselines/{sn}_region_1_baseline.png",
        "description": "Agent生成的基线描述",
        "captured_at": "ISO 8601 时间"
      }
    }
  ]
}
```

如果 monitors 列表中已有该设备，更新其 regions；如果是新设备，追加到列表中。

**查看监控：**
读取 `monitors.json`，展示所有监控设备和区域的摘要信息。

**删除监控：**
从 `monitors.json` 中移除对应设备或区域，删除对应的基线图片文件。

### 工作流 2: 执行巡检（核心）

**触发：** 用户说"看门狗巡检"、"检查一下"、"巡逻"、"巡逻一次"

**流程：**

#### 步骤 1 — 确认巡检范围

读取 `config/monitors.json`。如果用户指定了特定设备（如"检查 展厅A"），只巡检匹配的设备；否则巡检全部。

#### 步骤 2 — 抓图下载

运行抓图脚本（设置 PYTHONIOENCODING=utf-8）：

```bash
PYTHONIOENCODING=utf-8 python {skill_dir}/scripts/watchdog.py \
  --action capture \
  --config {skill_dir}/config/monitors.json \
  --output-dir {workspace}/captures/{YYYYMMDD}/ \
  --json
```

脚本输出 JSON 格式的结果（设备 SN、本地路径、是否成功等）。

#### 步骤 3 — 区域裁剪

对每台成功抓图的设备，运行区域裁剪：

```bash
PYTHONIOENCODING=utf-8 python {skill_dir}/scripts/watchdog.py \
  --action crop-regions \
  --config {skill_dir}/config/monitors.json \
  --source-image {抓图本地路径} \
  --device-sn {SN} \
  --output-dir {workspace}/crops/{YYYYMMDD}/ \
  --json
```

脚本输出每个区域的裁剪图路径。

#### 步骤 4 — Agent 视觉分析

对每个监控区域，Agent 同时读取三样内容：

1. **基线图片：** `baseline.image` 指向的文件
2. **当前裁剪图：** 步骤 3 输出的裁剪图
3. **规则描述：** `rule` 和 `baseline.description`

**分析维度：**

1. **基线对比：** 基线中描述的关键物品/状态在当前画面中是否仍然存在
2. **规则检测：** 当前画面是否出现规则中描述的异常情况
3. **报警条件：** 结合 `alert_when` 标签判断触发条件
   - `missing`：应有物品是否消失
   - `appeared`：不应有的物品是否出现
   - `changed`：状态是否发生变化

4. **敏感度调节**（根据 `sensitivity` 设置）：
   - `low`：只有明显变化才报异常
   - `moderate`（默认）：中等变化也报
   - `high`：细微变化也报

5. **附加观察：**
   - 如果图片模糊、过暗、角度不佳，标记为"无法判断"并说明原因
   - 记录画面中的其他异常信息

每个区域输出结论：**正常** / **异常** / **无法判断**，以及具体分析描述。

#### 步骤 5 — 标注巡检图片

在完整抓图上为每个监控区域绘制矩形框和状态标签，生成带标注的巡检图片：

- **正常区域：** 绿色矩形框 + 绿色标签背景 + 黑色文字（如"白色洞洞鞋: 正常"）
- **异常区域：** 红色矩形框 + 红色标签背景 + 白色文字（如"灭火器位置: 异常 — 物品缺失"）
- **无法判断区域：** 灰色矩形框 + 灰色标签背景

Agent 使用 Python PIL/Pillow 编写内联脚本完成标注：

1. 打开完整抓图（步骤 2 的输出）
2. 对每个监控区域，用 `ImageDraw.rectangle` 按坐标 (x, y, x+width, y+height) 绘制矩形框（width=3）
3. 在矩形框上方绘制标签：区域名称 + 状态文字
4. 保存到 `{workspace}/crops/{YYYYMMDD}/patrol_annotated.png`

#### 步骤 6 — 输出巡检报告

将所有区域的检测结论汇总，按以下格式输出：

```
🐕 看门狗巡检报告
━━━━━━━━━━━━━━━━━━━
巡检时间：YYYY-MM-DD HH:mm:ss
监控设备：N 台 | 监控区域：X 个 | 正常：Y 个 | 异常：Z 个

🔴 {设备名称} > {区域名称} (sn: {SN})
   状态：异常 — {异常类型}
   规则：{规则描述}
   分析：{具体分析描述}

🟢 {设备名称} > {区域名称} (sn: {SN})
   状态：正常
   分析：{具体分析描述}

⚫ {设备名称} > {区域名称} (sn: {SN})
   状态：无法判断
   原因：{无法判断的原因}

━━━━━━━━━━━━━━━━━━━
汇总：异常 A 个 / 正常 B 个 / 无法判断 C 个
建议关注：{异常区域列表}
```

**排列顺序：** 异常 → 正常 → 无法判断（按严重程度降序）。

**失败的设备和离线的设备**也需在报告中标注，用"离线"或具体错误原因标注。

**展示标注图片：** 输出文字报告后，必须使用 `present_files` 工具将步骤 5 生成的标注巡检图片展示给用户，让用户在完整画面中看到每个监控区域的位置和状态。如有异常区域，额外展示基线裁剪图与当前裁剪图的对比。示例：

```
present_files([
  {"file_path": "标注巡检图片路径（完整画面+红/绿框）"},
  {"file_path": "异常区域基线裁剪图"},
  {"file_path": "异常区域当前裁剪图"}
])
```

### 工作流 3: 定时巡检

**触发：** 用户说"定时巡检"、"每天巡检"、"自动巡检"

**流程：**

#### 步骤 1 — 确认巡检参数

使用 AskUserQuestion 工具确认：
- **巡检频率：** 每天 1 次（早上 9 点）/ 每天 2 次（9 点和 14 点）/ 自定义 cron 表达式
- **推送方式：** 结果如何推送（IM 频道、消息通知等）

#### 步骤 2 — 生成巡检指令模板

生成以下自包含的巡检指令文本，其中所有变量替换为实际值：

```
执行以下看门狗巡检任务：

技能目录: {skill_dir}
环境变量: JF_UUID={uuid}, JF_APP_KEY={key}, JF_APP_SECRET={secret}, JF_MOVE_CARD={card}

步骤 1 — 抓图：
设置 PYTHONIOENCODING=utf-8
python {skill_dir}/scripts/watchdog.py --action capture --config {skill_dir}/config/monitors.json --output-dir {data_dir}/captures/{YYYYMMDD}/ --json

步骤 2 — 裁剪：
对每台成功抓图的设备运行：
设置 PYTHONIOENCODING=utf-8
python {skill_dir}/scripts/watchdog.py --action crop-regions --config {skill_dir}/config/monitors.json --source-image {抓图路径} --device-sn {SN} --output-dir {data_dir}/crops/{YYYYMMDD}/ --json

步骤 3 — 分析：
对每个监控区域，使用 Read 工具读取基线图片和当前裁剪图，结合规则描述和基线描述判断状态。
判断标准：基线中应有物品是否仍在、是否出现异常物品、画面状态是否符合规则。
每个区域输出结论：正常 / 异常 / 无法判断。

步骤 4 — 标注图片：
在完整抓图上用 PIL/Pillow 为每个监控区域绘制矩形框和状态标签（正常=绿色，异常=红色），保存标注图。

步骤 5 — 报告：
汇总巡检结果，输出看门狗巡检报告，展示标注图片。如有 IM 频道可用，将报告推送给相关人员。
```

#### 步骤 3 — 配置定时执行

根据当前运行环境的定时任务能力（如 cron 任务、调度系统、外部工具等）配置自动执行。

- 如果平台支持定时任务功能，引导 Agent 使用平台能力创建定时任务，将上述指令模板作为任务内容
- 如果平台不支持定时任务，建议用户通过外部工具（如系统 crontab、任务计划程序等）实现定时执行

## 巡检报告模板

完整的巡检报告格式如下：

```
🐕 看门狗巡检报告
━━━━━━━━━━━━━━━━━━━
巡检时间：YYYY-MM-DD HH:mm:ss
监控设备：N 台 | 监控区域：X 个 | 正常：Y 个 | 异常：Z 个

--- 异常 ---

🔴 {设备名称} > {区域名称} (sn: {SN})
   状态：异常 — {missing/appeared/changed}
   规则：{规则描述}
   基线：{基线描述}
   分析：{具体分析，对比基线和当前画面的差异}

--- 正常 ---

🟢 {设备名称} > {区域名称} (sn: {SN})
   状态：正常
   分析：{具体分析，确认与基线一致}

--- 无法判断 ---

⚫ {设备名称} > {区域名称} (sn: {SN})
   状态：无法判断
   原因：{无法判断的原因，如图片模糊、光线不足、角度变化等}

--- 设备异常 ---

⚫ {设备名称} (sn: {SN})
   状态：抓图失败
   原因：{离线 / API 错误 / 下载失败等}

━━━━━━━━━━━━━━━━━━━
汇总：异常 A 个 / 正常 B 个 / 无法判断 C 个 / 设备异常 D 台
建议关注：{异常区域列表，如有}
```

**报告必须附带标注图片：** 使用 `present_files` 展示完整画面上标注了各区域矩形框和状态的巡检图片。异常区域额外展示基线裁剪图与当前裁剪图的对比。

## 错误处理

| 场景 | 处理方式 |
|------|----------|
| 摄像头离线 | 跳过该设备，报告中标记"离线"，计入失败 |
| 抓图 API 错误 | 跳过该设备，报告中标记失败原因 |
| 图片下载失败 | 脚本自动重试一次，仍失败标记"下载失败" |
| 区域裁剪失败 | 跳过该区域，报告中标记"裁剪失败" |
| Agent 无法判断 | 标记"无法判断"，说明原因 |
| 环境变量缺失 | 提示用户配置所需环境变量 |
| 配置文件为空 | 引导用户先添加监控设备 |
| 基线图片丢失 | 提示用户重新配置该区域的基线 |

## 脚本参考

| 脚本 | 用途 | 调用方式 |
|------|------|----------|
| `scripts/watchdog.py` | 抓图 + 下载 + 裁剪 | CLI: `--action {capture,capture-single,crop-regions,crop-baselines} --config --output-dir --json` |
| `scripts/crypto.py` | 签名加密工具 | 被 watchdog.py 导入 |

**各 action 详细说明：**

| action | 说明 | 必需参数 |
|--------|------|----------|
| `capture` | 批量抓图（从 monitors.json 读取设备列表） | `--config`, `--output-dir` |
| `capture-single` | 单设备抓图（配置阶段用） | `--device-sn`, `--device-name`, `--password`, `--output-dir` |
| `crop-regions` | 区域裁剪（巡检时从抓图裁剪各区域） | `--config`, `--source-image`, `--device-sn`, `--output-dir` |
| `crop-baselines` | 基线裁剪（配置阶段从抓图裁剪基线） | `--source-image`, `--device-sn`, `--regions-json`, `--output-dir` |

所有 action 均支持 `--json` 参数输出 JSON 格式结果。

## 相关文件

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能文档 |
| `scripts/watchdog.py` | 抓图 + 下载 + 裁剪脚本 |
| `scripts/crypto.py` | 签名/时间戳加密工具 |
| `assets/watchdog-config-widget.html` | 交互式区域配置 Widget |
| `config/monitors.json` | 监控配置文件 |
| `baselines/` | 基线图片存储目录 |

## 参考文档

- [杰峰开放平台](https://docs.jftech.com)
- [杰峰云抓拍定价](https://aops.jftech.com/#/pricing?lang=zh&tab=MEDIA_PROCESSING)
