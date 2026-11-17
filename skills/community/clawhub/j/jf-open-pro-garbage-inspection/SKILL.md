---
name: jf-garbage-inspection
description: 杰峰垃圾溢出巡检技能。通过杰峰监控设备抓图，Agent 直接看图分析垃圾桶是否溢出，输出结构化巡检报告。支持单设备/批量巡检和定时任务。
metadata:
  version: 1.1.0
  author: User
  category: analytics
  tags:
    - 杰峰
    - 垃圾溢出
    - 巡检
    - 垃圾桶
    - 智能分析
    - 环境卫生
  triggers:
    - 垃圾巡检
    - 垃圾溢出
    - 垃圾桶巡检
    - 巡检怎么用
    - 检查垃圾
    - 垃圾溢出了吗
    - 巡检一次
    - 添加摄像头
    - 定时巡检
    - 自动巡检
  prerequisites:
    - 配置必需的环境变量（JF_UUID, JF_APP_KEY, JF_APP_SECRET, JF_MOVE_CARD）
    - 设备需已完成配网和绑定
    - 设备需在线
    - 已安装依赖技能（jf-open-pro-device-list, jf-open-pro-device-status）
  region:
    - CN: api-cn.jftechws.com (中国大陆)
    - AS: api-as.jftechws.com (亚洲)
    - EU: api-eu.jftechws.com (欧洲)
    - NA: api-na.jftechws.com (北美洲)
---

# jf-garbage-inspection — 杰峰垃圾溢出巡检技能

## 技能描述

通过杰峰监控设备云抓图 + Agent 视觉分析，自动判断垃圾桶是否溢出：

- **抓图分析** — 对摄像头抓图后下载到本地，Agent 直接看图判断垃圾桶状态
- **单设备/批量** — 支持检查单个垃圾桶或多个垃圾桶
- **分级报告** — 输出严重溢出/轻度溢出/正常/无法判断四级巡检报告
- **摄像头管理** — 通过配置文件持久化管理巡检摄像头列表
- **定时巡检** — 支持配置定时任务自动巡检并推送结果

## 触发词

垃圾巡检 / 垃圾溢出 / 垃圾桶巡检 / 巡检怎么用 / 检查垃圾 / 垃圾溢出了吗 / 巡检一次 / 添加摄像头 / 定时巡检 / 自动巡检

## 依赖技能

| 依赖技能 | 用途 |
|----------|------|
| `jf-open-pro-device-list` | 添加摄像头时查询已绑定设备列表 |
| `jf-open-pro-device-status` | 添加摄像头时验证设备在线状态 |

抓图和下载由本技能自带的 `scripts/capture_and_download.py` 完成。

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
pip install requests
```

## 配置文件

`config/cameras.json` 存储巡检摄像头列表和参数：

```json
{
  "cameras": [
    {
      "sn": "设备序列号",
      "name": "A栋1楼垃圾桶",
      "password": "设备密码",
      "location": "A栋1楼大厅"
    }
  ],
  "settings": {
    "overflow_threshold": "moderate",
    "default_channel": 0
  }
}
```

- `sn`：杰峰设备序列号（唯一标识）
- `name`：用户定义的显示名称
- `password`：设备密码（用于自动获取 Token）
- `location`：位置描述（辅助分析报告中提供上下文）
- `overflow_threshold`：分析敏感度（`low` / `moderate` / `high`）
- `default_channel`：默认抓图通道号

## 核心工作流

### 工作流 0: 引导使用（首次对话 / 帮助）

**触发：** 用户说"垃圾巡检"、"垃圾溢出"、"巡检怎么用"、"帮我配置巡检"，或 Agent 判断用户是首次使用。

**流程：**

Agent 先静默检查环境状态，然后根据结果引导用户：

#### 第一步：环境检查（静默执行，不告诉用户"我在检查"）

1. 读取 `config/cameras.json`，检查 cameras 列表是否为空。
2. 检查环境变量 `JF_UUID`、`JF_APP_KEY`、`JF_APP_SECRET` 是否已设置（通过 `echo %JF_UUID%` 或 Bash 命令）。

#### 第二步：根据状态引导

**情况 A — 全新状态（无摄像头、无环境变量）：**

```
你好！我来帮你搭建垃圾溢出巡检系统。

这个系统能做什么：
- 通过杰峰摄像头抓图，用 AI 分析垃圾桶是否溢出
- 自动输出巡检报告，标注严重溢出/轻度溢出/正常
- 支持定时自动巡检，结果推送到 IM 频道

搭建只需要 2 步：

1. 配置环境变量（JF_UUID, JF_APP_KEY 等）
2. 添加巡检摄像头

我们先从配置环境变量开始，好吗？说"开始"就行。
```

**情况 B — 有环境变量，无摄像头：**

```
环境变量已就绪！接下来需要添加巡检摄像头。

说"添加摄像头"，我会帮你从已绑定的设备中选择。
```

**情况 C — 有摄像头，就绪状态：**

```
一切就绪！当前配置：

摄像头：{列出摄像头名称}
敏感度：{overflow_threshold}

现在可以：
- "巡检一次" — 立即对所有摄像头抓图分析
- "检查 A栋 的垃圾桶" — 只检查指定摄像头
- "查看摄像头" — 管理摄像头列表
- "定时巡检" — 设置自动巡检

需要做什么？
```

**注意事项：**
- 引导对话要简洁，不要一次输出太多信息
- 如果用户明确说要做什么，跳过引导直接进入对应工作流

### 工作流 1: 摄像头管理

**触发：** 用户说"添加摄像头"、"删除摄像头"、"查看摄像头"

**流程：**

**查看摄像头：**
读取 `config/cameras.json`，展示已配置的摄像头列表（名称、SN、位置）。

**添加摄像头：**
1. 使用 `jf-open-pro-device-list` 技能查询可用设备列表。
2. 展示设备列表让用户选择（显示 SN 和昵称）。
3. 询问用户：给摄像头起个名字（如"A栋1楼垃圾桶"）、位置描述（如"A栋1楼大厅"）。
4. 使用 `jf-open-pro-device-status` 验证设备是否在线。
5. 将设备信息追加到 `config/cameras.json` 的 cameras 列表中。

**删除摄像头：**
从 `config/cameras.json` 的 cameras 列表中移除对应条目。

### 工作流 2: 执行巡检（核心）

**触发：** 用户说"巡检一次"、"检查垃圾"、"垃圾溢出了吗"、"检查 X 的垃圾桶"

**流程：**

#### 步骤 1 — 确认巡检范围

读取 `config/cameras.json`。如果用户指定了特定摄像头（如"检查 A 栋"），只巡检匹配的设备；否则巡检全部。

#### 步骤 2 — 抓图下载

运行抓图脚本（设置 PYTHONIOENCODING=utf-8）：

```bash
python {skill_dir}/scripts/capture_and_download.py \
  --action inspect-batch \
  --config {skill_dir}/config/cameras.json \
  --output-dir {workspace}/captures/{YYYYMMDD}/ \
  --json
```

如果是单设备巡检：

```bash
python {skill_dir}/scripts/capture_and_download.py \
  --action inspect-single \
  --device-sn {设备SN} \
  --device-name {设备名称} \
  --device-location {位置} \
  --output-dir {workspace}/captures/{YYYYMMDD}/ \
  --json
```

脚本输出 JSON 格式的结果。

#### 步骤 3 — 看图分析

对 JSON 结果中每个 `"success": true` 的设备：

1. 使用 **Read 工具**读取 `results[].file` 指向的本地图片文件。
2. 仔细观察图片内容，按以下维度分析：

**分析维度：**

1. **识别垃圾桶**：在画面中找到垃圾桶，确认其位置和数量。如果画面中没有垃圾桶或看不到垃圾桶，标记为"无法判断 — 画面中未发现垃圾桶"。

2. **判断溢出状态**：
   - 垃圾是否超出桶口边缘
   - 是否有垃圾悬挂在桶沿
   - 桶外地面是否有散落垃圾
   - 桶盖是否能正常关闭

3. **严重程度分级**（参考 `overflow_threshold` 设置）：
   - **正常**（绿）：垃圾未满或刚满，桶口整洁，无外溢
   - **轻度溢出**（黄）：垃圾略超桶口，少量外溢，桶盖可能无法完全关闭
   - **严重溢出**（红）：大量垃圾溢出桶外，地面有明显散落物

4. **敏感度调节**（根据 `overflow_threshold`）：
   - `low`：只有"严重溢出"才标记为异常，轻度溢出视为正常
   - `moderate`（默认）：轻度溢出也标记为异常
   - `high`：垃圾桶接近满（约 80%）即标记为轻度溢出

5. **附加观察**：
   - 画面中如有多个垃圾桶则逐一判断
   - 记录垃圾桶是否倾斜、盖子状态等
   - 如果图片模糊、过暗、角度不佳，标记为"无法判断"并说明原因

#### 步骤 4 — 输出巡检报告

将所有设备的分析结果汇总，按以下格式输出：

```
📋 垃圾溢出巡检报告
━━━━━━━━━━━━━━━━━━━
巡检时间：YYYY-MM-DD HH:mm:ss
巡检设备：N 台 | 成功：X 台 | 失败：Y 台

🔴 {摄像头名称} (sn: {设备SN})
   状态：严重溢出
   位置：{位置描述}
   分析：{具体分析描述}

🟡 {摄像头名称} (sn: {设备SN})
   状态：轻度溢出
   位置：{位置描述}
   分析：{具体分析描述}

🟢 {摄像头名称} (sn: {设备SN})
   状态：正常
   位置：{位置描述}
   分析：{具体分析描述}

⚫ {摄像头名称} (sn: {设备SN})
   状态：无法判断
   位置：{位置描述}
   原因：{无法判断的原因}

━━━━━━━━━━━━━━━━━━━
汇总：严重溢出 A 台 / 轻度溢出 B 台 / 正常 C 台 / 无法判断 D 台
建议优先处理：{严重溢出的摄像头名称列表}
```

**排列顺序：** 严重溢出 → 轻度溢出 → 正常 → 无法判断（按严重程度降序）。

**失败的设备和离线的设备**也需在报告中展示，用"离线"或具体错误原因标注。

**展示抓图图片：** 输出文字报告后，必须使用 `present_files` 工具将所有成功抓取的图片文件展示给用户。每台设备对应一张抓图，让用户能直观看到每个摄像头的实时画面。示例：

```
present_files([
  {"file_path": "抓图文件的完整路径"},
  {"file_path": "抓图文件的完整路径"}
])
```

### 工作流 3: 定时巡检

**触发：** 用户说"定时巡检"、"每天巡检"、"自动巡检"

**流程：**

1. 使用 AskUserQuestion 工具确认：
   - **巡检频率：** 每天 1 次（早上 9 点）/ 每天 2 次（9 点和 14 点）/ 自定义 cron
   - **推送对象：** 使用 `qoder_list_channel_conversations` 查询可用 IM 会话列表，让用户选择接收人

2. 使用 `qoder_cron` 创建定时任务，message 示例：

```
执行以下垃圾溢出巡检任务：

技能目录: {skill_dir}
数据目录: {data_dir}

步骤 1 — 抓图
使用以下命令对所有巡检摄像头抓图：
设置 PYTHONIOENCODING=utf-8
python {skill_dir}/scripts/capture_and_download.py --action inspect-batch --config {skill_dir}/config/cameras.json --output-dir {data_dir}/captures/{今天YYYYMMDD}/ --json
环境变量: JF_UUID=xxx, JF_APP_KEY=xxx, JF_APP_SECRET=xxx, JF_MOVE_CARD=xxx

步骤 2 — 分析
对抓图成功的每台设备，使用 Read 工具读取下载的本地图片，分析垃圾桶是否溢出。
判断标准：严重溢出（大量垃圾溢出桶外）、轻度溢出（略超桶口）、正常（未满或刚满）。
如果画面中看不到垃圾桶，标记为"无法判断"。

步骤 3 — 推送
汇总巡检结果，通过 IM 频道发送报告给「{用户名}」。
报告格式包含每台设备的状态（严重溢出/轻度溢出/正常/无法判断）和具体分析。
```

## 错误处理

| 场景 | 处理方式 |
|------|----------|
| 摄像头离线 | 跳过该设备，报告中标记"离线"，计入失败 |
| 抓图 API 错误 | 跳过该设备，报告中标记失败原因 |
| 图片下载失败 | 脚本自动重试一次，仍失败标记"下载失败" |
| 图片无法分析 | Agent 标记"无法判断"，说明原因 |
| 环境变量缺失 | 提示用户配置所需环境变量 |
| 配置文件为空 | 引导用户先添加摄像头 |

## 脚本参考

| 脚本 | 用途 | 调用方式 |
|------|------|----------|
| `scripts/capture_and_download.py` | 抓图 + 下载 | CLI: `--action {inspect-single,inspect-batch} --config --output-dir --json` |
| `scripts/crypto.py` | 签名加密工具 | 被 capture_and_download.py 导入 |

## 相关文件

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能文档 |
| `scripts/capture_and_download.py` | 抓图 + 下载脚本 |
| `scripts/crypto.py` | 签名/时间戳加密工具 |
| `config/cameras.json` | 摄像头配置文件 |

## 参考文档

- [杰峰开放平台](https://docs.jftech.com)
