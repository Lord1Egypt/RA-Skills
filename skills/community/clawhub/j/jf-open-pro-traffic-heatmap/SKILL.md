---
name: jf-open-pro-traffic-heatmap
description: 室内人流热力图分析技能。通过杰峰摄像头定时抓拍 + 本地 YOLOv8 头部检测，生成圆形高斯模糊热力图叠加的交互式 HTML 报告。支持 10 分钟粒度流量趋势、空间利用率分析和客流计数统计。
metadata:
  version: 1.4.1
  author: User
  category: analytics
  tags:
    - 热力图
    - 人流分析
    - 杰峰
    - 监控
    - 客流统计
    - 头部检测
    - 定时任务
  triggers:
    - 热力图
    - 人流分析
    - 客流统计
    - 空间利用率
    - 流量报告
    - 热力图报告
    - 人头检测
    - 热力图怎么用
    - 热力图使用指南
  prerequisites:
    - Python 3.8+
    - pip install opencv-python numpy ultralytics matplotlib
    - 已安装杰峰相关技能（jf-open-pro-capture, jf-open-pro-device-status, jf-open-pro-device-list）
---

# Traffic Heatmap — 人流热力图分析

## 技能描述

分析室内空间人流，通过杰峰摄像头抓图 + 本地 YOLOv8m 头部检测模型，生成圆形高斯模糊热力图叠加的交互式 HTML 报告。支持 10 分钟粒度流量趋势、空间利用率分析和客流计数统计。可配合 QoderWork 定时任务实现自动化采集与 IM 推送。

## 触发词

热力图 / 人流分析 / 客流统计 / 空间利用率 / 流量报告 / 人头检测 / 热力图怎么用 / 使用指南

## 依赖技能

本技能依赖以下已有杰峰技能来完成设备操作，**不要自行实现设备通信**：

| 依赖技能 | 用途 |
|----------|------|
| `jf-open-pro-capture` | 设备抓图（单设备/批量） |
| `jf-open-pro-device-status` | 查询设备在线状态 |
| `jf-open-pro-device-list` | 查询已绑定设备列表 |

## 前置条件

### 环境变量

由杰峰技能统一管理（JF_UUID, JF_APP_KEY, JF_APP_SECRET, JF_MOVE_CARD 等），本技能无需额外配置。

### Python 依赖

```bash
pip install opencv-python numpy ultralytics matplotlib
```

注意：不需要 `requests`，设备通信由杰峰技能处理。

### 检测模型

使用 **YOLOv8m 头部检测模型**（`models/head-yolov8m.pt`，约 50MB），基于 SCUT-HEAD 数据集训练，单类别 `{0: 'head'}`。

模型来源：https://github.com/Abcfsa/YOLOv8_head_detector （medium.pt）

**下载地址（如模型文件缺失可手动或自动下载）：**

| 文件 | 大小 | 下载地址 |
|------|------|----------|
| `head-yolov8m.pt` (medium) | ~50 MB | https://github.com/Abcfsa/YOLOv8_head_detector/raw/main/medium.pt |
| `head-yolov8s.pt` (nano) | ~6 MB | https://github.com/Abcfsa/YOLOv8_head_detector/raw/main/nano.pt |

下载后放入 `models/` 目录并重命名为 `head-yolov8m.pt` 或 `head-yolov8s.pt`。`detect.py` 的 `load_model()` 在本地未找到模型时会自动尝试从上述地址下载。

模型查找路径按优先级从高到低：

1. `models/head-yolov8m.pt`
2. `models/head-yolov8s.pt`
3. `data/models/head-yolov8m.pt`
4. `data/models/head-yolov8s.pt`

如无头部模型权重且下载失败，脚本会抛出异常并提示手动下载地址，不会回退到 COCO 检测器。

## 配置文件

`config/cameras.json` 存储本技能使用的摄像头列表和检测参数：

```json
{
  "cameras": [
    {
      "id": "a717e75986337093",
      "name": "办公室-主区域",
      "password": "",
      "grid_cols": 24,
      "grid_rows": 14
    }
  ],
  "settings": {
    "capture_interval_minutes": 5,
    "confidence_threshold": 0.4,
    "image_retention_days": 7
  }
}
```

- `id`: 摄像头唯一标识（杰峰设备 ID）
- `name`: 用户定义的显示名称
- `grid_cols/grid_rows`: 热力图网格密度（默认 24x14，每格约 80x77 像素，适合 1920x1080 画面）
- `capture_interval_minutes`: 建议采集间隔（仅供 Agent 参考）
- `confidence_threshold`: 头部检测最低置信度（默认 0.4，平衡召回与误检）

## 数据隔离

**每个会话使用独立的数据目录**，避免不同会话的数据互相污染。

通过 `--data-dir` 参数指定会话数据目录，数据库、抓拍图片、报告输出全部存储在该目录下：

```
{data_dir}/
  data/
    traffic_heatmap.db    # 独立的 SQLite 数据库
    captures/             # 独立的抓拍归档
      {YYYYMMDD}/
    outputs/              # 独立的报告输出
      report.html
      summary.txt
```

**使用规则：**

- **Agent 在对话中执行操作时**：使用当前会话的 workspace 目录作为 `--data-dir`，例如 `C:\Users\...\workspace\{session_id}\`。这样每个会话的数据完全隔离。
- **定时任务**：使用定时任务自己的 `contextDirs` 目录作为 `--data-dir`，定时任务的数据与其他会话独立。
- **不指定 `--data-dir` 时**：回退到技能安装目录（向后兼容），所有数据共享。

**脚本调用示例：**

```bash
# detect.py 指定数据目录
python scripts/detect.py --images {data_dir}/data/captures/{YYYYMMDD}/ \
  --config config/cameras.json \
  --db {data_dir}/data/traffic_heatmap.db \
  --data-dir {data_dir}

# run_report.py 指定数据目录
python run_report.py --data-dir {data_dir}
```

配置（`config/cameras.json`）、代码（`scripts/`、`assets/`）和模型（`models/`）始终从技能安装目录共享，不受 `--data-dir` 影响。

## 核心工作流

### 工作流 0: 引导使用（首次对话 / 帮助）

**触发：** 用户说"热力图怎么用"、"帮我配置热力图"、"介绍一下热力图"、"使用指南"，或 Agent 判断用户是首次使用本技能。

**流程：**

Agent 应先做一次环境检查，然后根据当前状态给出针对性的引导，而不是机械地输出固定话术。

#### 第一步：环境检查（静默执行，不要告诉用户"我在检查"）

依次检查以下项目，记录结果：

1. 读取 `config/cameras.json`，看是否已有摄像头配置（cameras 列表是否为空，或只有默认占位数据）。
2. 检查 `models/` 目录下是否有 `head-yolov8m.pt` 或 `head-yolov8s.pt`。
3. 检查当前会话的 `data_dir/data/traffic_heatmap.db` 是否存在（是否有历史数据）。
4. 使用 `qoder_cron` 的 list action 检查是否已有热力图相关的定时任务。

#### 第二步：根据状态引导

根据检查结果，按以下逻辑组织对话：

**情况 A — 全新状态（无摄像头、无模型、无数据）：**

```
你好！我来帮你搭建人流热力图分析系统。

这个系统能做什么：
• 通过杰峰摄像头定时抓拍画面，用 AI 检测人头数量
• 生成空间热力图，直观展示哪些区域人流密集
• 支持定时自动采集，检测结果自动推送到 IM 频道（钉钉等）

搭建只需要 3 步，我来一步步带你完成：

1️⃣ 添加摄像头 — 告诉我你要监控哪个摄像头
2️⃣ 下载检测模型 — 首次使用需要下载 AI 模型（约 50MB，自动完成）
3️⃣ 试跑一次 — 抓图、检测、看效果

我们先从添加摄像头开始，好吗？说"开始"就行。
```

用户确认后，自动进入工作流 1（摄像头配置）。

**情况 B — 有摄像头，但无模型：**

```
已经配置好摄像头了！接下来需要下载头部检测模型。

当前摄像头：{列出已配置的摄像头名称}

模型文件约 50MB，从 GitHub 下载，首次运行检测时会自动拉取。
要现在试跑一次看看效果吗？
```

用户确认后，进入工作流 2（采集与检测），模型会在 `load_model()` 中自动下载。

**情况 C — 有摄像头、有模型，但无数据：**

```
一切就绪！你的系统配置如下：

📷 摄像头：{列出名称}
🧠 检测模型：已就绪
⏱️ 定时任务：{已配置 / 未配置}

现在可以做这些事：
• 「采集一次」— 立即抓图并检测人数
• 「生成报告」— 生成热力图 HTML 报告
• 「定时采集」— 设置自动采集和钉钉推送

建议先跑一次采集看看效果，要试试吗？
```

**情况 D — 已有数据（老用户回来）：**

```
欢迎回来！当前状态：

📷 摄像头：{列出名称}
📊 历史数据：{数据条数} 条采集记录
⏱️ 定时任务：{已配置 / 未配置}

需要我做什么？
• 「采集一次」— 立即抓图检测
• 「生成报告」— 查看最新热力图
• 「查看摄像头」— 管理摄像头配置
• 「定时采集」— 配置自动采集推送
```

#### 第三步：执行用户选择的操作

根据用户回复进入对应工作流（1~5），执行完成后回到引导末尾，简短提示下一步可以做什么。

#### 注意事项

- 引导对话要简洁，不要一次输出太多信息
- 环境检查是静默的，不要列出一堆检查步骤给用户看
- 如果用户明确说要做什么（如"帮我添加摄像头"），跳过引导直接进入对应工作流
- 每次完成一个操作后，简短提示用户接下来可以做什么

### 工作流 1: 摄像头配置

**触发：** 用户说"添加摄像头"、"配置摄像头"、"查看摄像头列表"、"删除摄像头"

**流程：**

1. 如果用户说"查看摄像头列表"：读取 `config/cameras.json` 并展示给用户。
2. 如果用户说"添加摄像头"：
   - 使用 `jf-open-pro-device-list` 技能查询可用设备列表
   - 让用户选择要添加的设备（或手动输入设备 ID）
   - 询问用户给摄像头起个名字（如"入口"、"收银台"）
   - 使用 `jf-open-pro-device-status` 验证设备是否在线
   - 将设备信息写入 `config/cameras.json`
3. 如果用户说"删除摄像头"：从 `config/cameras.json` 中移除对应条目。

### 工作流 2: 采集与检测

**触发：** 用户说"采集一次"、"收集数据"、"跑检测"

**流程：**

1. 读取 `config/cameras.json` 获取摄像头列表。
2. **使用 `jf-open-pro-capture` 技能** 对所有摄像头执行批量抓图。
   - 将图片下载到 `{data_dir}/data/captures/{YYYYMMDD}/` 目录
   - 图片命名格式：`{camera_id}_{timestamp}.png`
   - 如果某个摄像头离线，跳过并记录警告
3. 运行头部检测脚本：
   ```bash
   python scripts/detect.py --images {data_dir}/data/captures/{YYYYMMDD}/ \
     --config config/cameras.json \
     --db {data_dir}/data/traffic_heatmap.db \
     --data-dir {data_dir}
   ```
4. 向用户汇报检测结果摘要（每个摄像头检测到多少人）。

### 工作流 3: 生成报告

**触发：** 用户说"生成报告"、"看热力图"、"本周报告"

**流程：**

1. 根据用户意图确定时间范围（默认：当天）。
2. 运行报告生成脚本（自动查找最新背景图）：
   ```bash
   python run_report.py --data-dir {data_dir}
   ```
   `{data_dir}` 为当前会话的数据目录。脚本会从 `{data_dir}/data/` 读取数据库和抓拍图，输出 `report.html` 和 `summary.txt` 到 `{data_dir}/data/outputs/`。
3. 使用 `present_files` 将生成的 HTML 报告呈现给用户。
4. `generate_report()` 返回总结文本，可保存到 `summary.txt` 或直接用于 IM 推送。

### 工作流 4: 单独渲染热力图

**触发：** 用户说"看某个摄像头的热力图"

**流程：**

1. 运行热力图渲染脚本：
   ```bash
   python scripts/heatmap.py \
     --db data/traffic_heatmap.db \
     --camera {camera_id} \
     --start {YYYY-MM-DD} \
     --end {YYYY-MM-DD} \
     --background {background_image_path} \
     --output data/outputs/heatmap_{camera_id}.png \
     --grid-cols 24 --grid-rows 14
   ```
2. 展示生成的热力图 PNG。

### 工作流 5: 定时自动采集与推送

**触发：** 用户说"定时采集"、"每 N 分钟跑一次"、"自动推送报告"

**流程：**

1. **引导用户确认配置（必须，不要假设）：**

   使用 AskUserQuestion 工具询问以下信息：

   - **采集间隔：** 提供选项 5 分钟 / 10 分钟 / 15 分钟 / 30 分钟
   - **推送对象：** 使用 `qoder_list_channel_conversations` 查询当前可用的 IM 会话列表，将会话名称作为选项供用户选择（如"钉钉-陈亮"、"钉钉-运维群"等），如果没有可用会话则提示用户先连接 IM 频道
   - **运行时段：** 提供选项 全天 24 小时 / 仅工作时间 9:00-18:00 / 自定义

2. 使用 `qoder_cron` 工具创建定时任务：
   ```
   schedule: { kind: "cron", expr: "*/{间隔} * * * *", tz: "Asia/Shanghai" }
   payload.message: 自然语言描述完整流水线步骤
   ```
3. 定时任务的 message 应包含完整步骤：
   - 使用杰峰技能抓图
   - 运行 `detect.py --data-dir {data_dir}` 检测头部
   - 运行 `run_report.py --data-dir {data_dir}` 生成报告（自动选择最新抓图作为热力图背景）
   - 读取 `summary.txt`，通过 IM 频道推送给用户选择的接收人

**推送方式：** 统一通过 IM 频道发送消息（使用 `qoder_list_channel_conversations` 查找会话 + `qoder_delegate_to_im` 投递），**不要使用 DWS 等连接器直接发钉钉消息**。

**示例定时任务 message（{用户名} 由用户选择后替换，{data_dir} 为定时任务的数据目录）：**

```
执行以下人流热力图分析任务：

技能目录: {skill_dir}
数据目录: {data_dir}

步骤 1 — 抓图
使用杰峰抓图技能对所有摄像头抓图。
环境变量: JF_UUID=xxx, JF_APP_KEY=xxx, JF_APP_SECRET=xxx, JF_MOVE_CARD=xxx
图片保存到 {data_dir}/data/captures/{今天YYYYMMDD}/ 目录，命名格式 {camera_id}_YYYYMMDDHHmmss.png

步骤 2 — 检测
设置 PYTHONIOENCODING=utf-8，运行:
python {skill_dir}/scripts/detect.py --images {data_dir}/data/captures/{今天YYYYMMDD}/ \
  --config {skill_dir}/config/cameras.json \
  --db {data_dir}/data/traffic_heatmap.db \
  --data-dir {data_dir}

步骤 3 — 生成报告
运行: python {skill_dir}/run_report.py --data-dir {data_dir}
生成 {data_dir}/data/outputs/report.html 和 summary.txt（自动选最新图片作背景）

步骤 4 — 推送
读取 {data_dir}/data/outputs/summary.txt，通过 IM 频道发送总结给「{用户名}」
```

## 脚本参考

| 脚本 | 用途 | 调用方式 |
|------|------|----------|
| `scripts/db.py` | SQLite 数据层（库模块） | 被其他脚本导入 |
| `scripts/detect.py` | YOLOv8m 头部检测 + 网格映射 | CLI: `--images --config --db --data-dir` |
| `scripts/heatmap.py` | 圆形高斯热力图渲染 | CLI: `--db --camera --start --end --background --output --grid-cols --grid-rows` |
| `scripts/report.py` | 交互式 HTML 报告生成（含总结生成） | CLI: `--db --config --start --end --output --backgrounds --data-dir`，返回总结文本 |
| `run_report.py` | 报告生成入口（自动选最新背景图） | CLI: `--data-dir --daily`，输出 report.html + summary.txt |

## 检测策略

使用 YOLOv8m 头部检测模型（SCUT-HEAD 训练），专门针对监控场景优化：

- **模型：** `head-yolov8m.pt`，单类别 `head`，medium 规模（约 50MB）
- **锚点：** 头部 bbox 底部中心 `(cx, y2)`，近似颈部/肩膀位置
- **置信度阈值：** 0.4（在召回率和误检率之间取得平衡）
- **适用场景：** 站立、行走、坐姿、背面、后脑勺、半遮挡人头、远距离小目标
- **回退：** 如无头部模型权重且自动下载失败，抛出异常提示手动下载，不回退到 COCO 检测器

## 热力图渲染

采用**圆形高斯模糊渲染**方式，不使用网格线：

- 每个有数据的网格绘制一个圆形色块，半径为格子短边的 40%
- 使用高斯模糊（kernel = radius/2）使圆形边缘柔和
- 颜色映射使用 `YlOrRd` colormap（黄→橙→红），透明度 alpha=0.6
- 无数据区域不绘制，直接显示背景画面

## 报告格式

交互式自包含 HTML 报告，特性包括：

- **摄像头标签切换：** 多摄像头时通过标签页切换
- **统计卡片（6 项）：** 总检测人次、平均检测人次（每轮）、本小时平均人次、高峰时段、最热区域、采集轮次；网格自适应布局
- **左右排版：** 左侧热力图（1.5fr）+ 右侧 10 分钟流量柱状图（1fr）
- **热力图：** base64 嵌入 PNG，圆形色块叠加，带渐变色图例
- **流量图表：** Canvas 柱状图，按 10 分钟粒度聚合，X 轴标签旋转 -30°，峰值高亮
- **本次总结：** 可视化区域下方展示统计总结卡片，包含采集轮次、累计检测人次、高峰时段、最热区域、平均人次和流量趋势（上升/下降/平稳）
- **采集记录摘要：** 每条历史记录附带简要分析（本时段峰值 / 高于平均 / 正常水平 / 低于平均 / 未检测到人员活动）
- **时间预设：** 日/周/月快捷切换按钮

报告生成函数 `generate_report()` 返回总结文本字符串，调用方可将其保存或用于 IM 推送。

## 数据说明

SQLite 数据库 `{data_dir}/data/traffic_heatmap.db` 包含三张表：

- **cameras**: 摄像头配置信息
- **detections**: 每帧检测记录（时间戳、人数、图片路径）
- **grid_heat**: 网格热力累积数据（按摄像头+网格坐标+时间窗口）

报告通过 `query_grid()` 聚合 grid_heat 表生成热力图，通过 `query_time_series()` 按 10 分钟窗口聚合生成流量趋势。

### 关键查询函数

| 函数 | 说明 |
|------|------|
| `query_grid(db, cam_id, start, end)` | 聚合网格数据用于热力图渲染 |
| `query_time_series(db, cam_id, start, end, interval_minutes=10)` | 按 N 分钟窗口聚合流量趋势 |
| `query_stats(db, cam_id, start, end)` | 汇总统计（总量、高峰、最热格子、轮次） |
| `query_history(db, cam_id, start, end)` | 查询检测历史记录（时间戳、人数、图片路径） |

## 错误处理

| 场景 | 处理 |
|------|------|
| 摄像头离线 | 跳过该设备，汇报部分结果 |
| 未找到头部检测模型 | 自动从 GitHub 下载（重试 3 次），失败则抛异常提示手动下载地址 |
| 某帧无检测结果 | 正常行为，不写入 grid_heat 记录 |
| Windows CLI JSON 转义失败 | 改用临时 Python 脚本直接调用函数 |
| 磁盘空间不足 | 建议用户清理旧图片（超过 image_retention_days 的） |
