---
name: jf-open-algo-assistant
description: 杰峰开放平台通用AI算法调用助手（开发版）。交互式引导用户明确检测场景（如明厨亮灶、安全生产、消防安全、门店巡检、周界安防），从52个免底库算法清单中推荐适配算法（不含需底库的比对类算法），支持对本地图片/图片URL/摄像头设备抓图（配合 jf-open-pro-capture 技能）调用算法分析并输出结构化检测报告。Use when the user mentions 明厨亮灶、AI检测、算法调用、图片分析、摄像头智能分析、口罩/安全帽/烟火/垃圾检测、开放平台算法、jf算法、检测服务。
metadata:
  version: 1.1.0
  author: JFTech
  category: ai
  tags:
    - 杰峰
    - 开放平台
    - AI算法
    - 图片分析
    - 智能检测
  triggers:
    - 明厨亮灶
    - AI检测
    - 算法调用
    - 图片分析
    - 摄像头智能分析
    - 检测服务
  prerequisites:
    - 配置开放平台开发者凭证（uuid / appKey / appSecret / moveCard）
    - 设备抓图分支需安装依赖技能 jf-open-pro-capture
  region:
    - 算法调用统一入口 https://api.jftechws.com（不区分区域）
    - 设备抓图分支（依赖技能）：CN api-cn.jftechws.com / AS api-as.jftechws.com / EU api-eu.jftechws.com / NA api-na.jftechws.com
---

# jf-open-algo-assistant - 杰峰开放平台通用AI算法调用助手（开发版）

## 技能描述

支持杰峰开放平台场景化检测算法调用：

- 场景引导 - 通过对话明确检测场景（明厨亮灶、工地安全、消防、门店巡检、周界安防等）
- 算法推荐 - 结合 [reference.md](reference.md) 算法清单推荐适配算法并说明理由
- 开通调用 - 自动开通（幂等）+ 同步调用算法分析本地图片/图片URL/设备抓图
- 结果解读 - 按平台「检测结果」页格式输出结构化报告，本地图可渲染红框取证图

适用场景：明厨亮灶/后厨监管、工地/车间安全生产、消防安全、周界安防、门店巡检、车辆管理、环卫环境等

> 所有接口调用通过 `scripts/jf_client.py` 完成，**不要手写 HTTP 请求或签名代码**。

## 触发词

明厨亮灶 / AI检测 / 算法调用 / 图片分析 / 摄像头智能分析 / 检测服务等

## 前置条件

### 平台账号

开放平台开发者账号（控制台获取凭证），算法开通即用、按调用计费。

### 凭证配置（技能目录 config.json）

| 配置项 | 说明 | 默认值 | 必需 |
|--------|------|--------|------|
| uuid | 开放平台用户 uuid | - | ✅ |
| appKey | 开放平台应用 appKey | - | ✅ |
| appSecret | 开放平台应用密钥 | - | ✅ |
| moveCard | 移动卡标识（用于签名） | 2 | ✅ |
| endpoint | API 接入地址 | https://api.jftechws.com | ❌ |

```bash
python scripts/jf_client.py config set --uuid xxx --appkey xxx --appsecret xxx [--movecard 2] [--endpoint https://api.jftechws.com]
```

- 签名算法已内置（官方 SDK 移位加密移植，Header: uuid/appKey/timeMillis/signature，脚本自动处理）
- **凭证只写入本地 config.json，不要在对话中回显 appSecret**

### 依赖技能（仅设备抓图分支需要）

`jf-open-pro-capture`（杰峰设备抓图）。获取渠道：

- QoderWork 技能市场：https://qoder.com/marketplace/skill?id=official_g5rUGlI4
- Gitee 源码仓库：https://gitee.com/jftek/jftech-open-skills/tree/main/jf-open-pro-capture
- ClawHub：https://clawhub.ai/jftech/jf-open-pro-capture

## API 接口

| 功能 | 地址 | 方法 |
|------|------|------|
| 查询算法列表/开通状态 | /openai/algorithm/application/v3/getAlgoExperienceList | POST |
| 开通算法 | /openai/algorithm/application/v3/open | POST |
| 调用算法（同步） | /openai/algorithm/application/v3/callApp | POST |
| 调用算法（异步推送） | /openai/algorithm/application/v3/pushApp | POST |

## 核心功能：交互流程（严格按顺序执行）

```
任务清单（每轮对话维护）:
- [ ] 1. 明确检测场景
- [ ] 2. 推荐算法并说明理由
- [ ] 3. 用户确认算法清单
- [ ] 4. 检查凭证 + 获取图片/设备序列号
- [ ] 5. 开通并调用算法
- [ ] 6. 解读检测结果
```

### 步骤 1：明确检测场景

询问用户要实现什么场景的检测服务（如"明厨亮灶"、"工地安全"、"消防通道监控"）。
用 AskUserQuestion 给出常见场景选项（参考 reference.md「场景速查」），同时允许用户自由描述。
用户描述模糊时追问：监控对象是什么、想发现什么行为/目标、室内还是室外。

### 步骤 2：推荐算法

先读 [reference.md](reference.md) 的算法清单（52 个，全部免底库），结合场景给出推荐：

- 每个推荐算法给出：名称、appUuid、一句话能力说明
- 不要推荐与场景无关的算法；宁缺毋滥
- 若用户点名要比对类算法（智能门锁/陌生人识别/猫脸识别/多宠识别），说明这些需先在控制台维护底库，不在本技能支持范围

### 步骤 3：等待用户确认

**必须等用户明确选定算法后才能继续**（可多选）。用 AskUserQuestion 多选确认。

### 步骤 4：凭证与检测输入

1. 凭证检查：运行 `python scripts/jf_client.py config show`
   - 已配置 → 运行 `python scripts/jf_client.py test` 验证签名连通性
   - 未配置 → 引导用户提供 uuid / appKey / appSecret / moveCard（开放平台控制台获取，moveCard 默认 2），然后执行 `config set`
   - `test` 返回签名错误时：提示用户核对 moveCard 与凭证是否正确
2. 询问检测输入，二选一：
   - **图片**：本地文件路径或图片 URL → 进入步骤 5
   - **设备序列号（SN）**：走设备抓图分支 ↓

### 步骤 4a：设备抓图分支

1. 检查 `jf-open-pro-capture` 技能是否可用（当前会话的可用技能列表中查找）
2. 未安装 → 告知用户：设备抓图依赖 **jf-open-pro-capture** 技能（从杰峰摄像头抓取实时图片），当前未安装，并列出上文「依赖技能」的三个获取渠道；然后用 AskUserQuestion 让用户选择：
   - **帮我自动下载安装（推荐）** → 执行第 3 步自动安装
   - 我自己安装 → 等待用户装好后告知继续
   - 改用图片方式 → 回到步骤 4 的图片分支
3. 自动安装流程（用户同意后执行）：
   ```bash
   git clone --depth 1 https://gitee.com/jftek/jftech-open-skills.git <临时目录>
   # 把其中 jf-open-pro-capture 子目录复制到 C:\Users\zheng\.qoderworkcn\skills\jf-open-pro-capture
   ```
   - git 不可用时改下 zip：https://gitee.com/jftek/jftech-open-skills/repository/archive/main.zip
   - 复制后校验目标目录存在 SKILL.md；若当前会话技能列表未刷新，直接读取该 SKILL.md 并按其说明继续抓图，无需等待用户操作
4. 已安装 → 按该技能的说明用设备 SN 抓取一张图片，得到本地图片路径后进入步骤 5
   - 抓图前向用户确认：设备 SN、所在区域（默认 CN `api-cn.jftechws.com`，EU/AS/NA 换对应域名）、设备 admin 密码（平台需用它登录设备执行抓图指令）
   - 实测经验：`--password` 本地必填校验可传占位值，但若平台侧设备凭证未同步，抓图会报 `Please re-obtain the DeviceToken and synchronize the device login username and password`，需用户先在控制台重新绑定/同步设备密码
   - token 接口报 `DEV_NOTEXIT` = 该区域平台查无此设备，先核对区域是否选错（token 查询不要求设备在线，可低成本探测区域）

### 步骤 5：开通并调用

对用户确认的每个算法依次执行：

```bash
# 1) 开通（幂等，已开通也不会报错）
python scripts/jf_client.py open <appUuid>
# 2) 调用分析（本地图片自动转base64；URL直接传）；输出重定向到文件供步骤6渲染使用
python scripts/jf_client.py call <appUuid> --image <图片路径或URL> --sn <设备SN> [--conf 0.3] > result_<appUuid>.json
```

- 本地图片无真实设备时 `--sn` 可用占位值（如 `local-image`）
- 多个算法逐个调用，结果文件命名 result_<appUuid>.json，最后汇总

### 步骤 6：解读结果（结构化检测报告）

按平台「检测结果」页面的固定结构输出。

**6.1 生成取证图与摘要**（仅本地图片可渲染取证图）：

```bash
python scripts/render_result.py --result result_<appUuid>.json --image <原图路径> \
  --algo-name <算法中文名> --label-cn <业务标签> --sn <设备SN> [--channel 0] --out-dir <输出目录>
```

- 脚本在原图画红色 bbox + 标签 + 置信度生成取证图，并输出结构化摘要 JSON（告警文案/检测结果表/检测信息/取证图路径）
- label-cn 映射规则：行为类 sleeping→疑似睡岗、off duty→疑似离岗、playing_phone→玩手机、eating→进食；合规类 no mask→未戴口罩、no_hardhat→未戴安全帽、no head covering→未戴厨师帽、smoking→吸烟；存在类按中文语义（human→人员、garbage→垃圾）；拿不准时用「算法名+检出」

**6.2 报告模板**（每个检出的算法一份）：

```
## 检测结果
**检出 N 个目标**
> **检出告警**：画面中检测到 N 个「{业务标签}」目标，建议及时关注。

| 检测项 | 结果 |
| --- | --- |
| 行为/目标识别 | {业务标签} |
| 目标数量 | N 个 |
| 最高置信度 | 88% |
| 画面位置 | {左侧/中部/右侧...区域} |
| 分析时间 | YYYY-MM-DD HH:mm:ss |

**检测信息**：设备序列号 {sn} ｜ 通道 {channel} ｜ 检测能力 {算法名}
取证图：![取证图](路径)（可附接口返回的原图链接，24小时有效）
```

多算法同轮调用时：先给汇总告警行（检出哪些项、未检出哪些项），再逐个输出报告。

**6.3 未检出**（data 为空）→ 明确告知未检出目标，不生成取证图；建议：调低置信度（`--conf 0.2`）重试、核对画面是否满足算法要求（如吸烟检测需人体露出2/3以上）

**6.4 `code!=2000`** → 按下方「状态码」与 reference.md「错误处理」定位

## 📊 API 使用规范

| 功能 | 接口 | 关键参数 | 用途 |
|------|------|----------|------|
| 连通性测试 | getAlgoExperienceList | page/rows/lang | 验证签名凭证有效性（lang 必填） |
| 开通算法 | open | algoAppUuid + algoAppVersion | 调用前提，幂等（12537 视为已开通） |
| 同步调用 | callApp | appUuid + image + appConfig | 检测分析，返回 objects/bbox/confidence |
| 异步推送 | pushApp | appUuid + callbackUrl | 告警回调模式（本技能默认同步） |

## 使用示例

### 环境准备

```bash
cd C:\Users\zheng\.qoderworkcn\skills\jf-open-algo-assistant\scripts

# 配置开发者凭证（占位符请替换为实际值）
python jf_client.py config set --uuid "uuidxxxx" --appkey "appkeyxxxx" --appsecret "appsecretxxxx" --movecard 2
```

### 1. 验证凭证连通性

```bash
python jf_client.py test
```

### 2. 开通算法

```bash
python jf_client.py open a1000007    # 口罩检测
```

### 3. 调用算法分析

```bash
# 图片 URL
python jf_client.py call a1000007 --image "https://xx.jpg" --sn <设备SN> --conf 0.3

# 本地图片（自动转 base64；无真实设备时 --sn 可占位）
python jf_client.py call a1000007 --image "C:\path\to\image.jpg" --sn local-image > result_a1000007.json
```

### 4. 渲染取证图与结构化摘要

```bash
python render_result.py --result result_a1000007.json --image "C:\path\to\image.jpg" \
  --algo-name 口罩检测 --label-cn 未戴口罩 --sn <设备SN> --out-dir <输出目录>
```

## 参数说明

| 参数 | 取值/默认 | 说明 |
|------|-----------|------|
| appUuid | 如 a1000007 | 算法标识，见 reference.md 清单，所有算法共用 v3 接口 |
| image.url / image.b64 | 二选一 | 图片云链接或 base64，sn 必填（纯图片可占位） |
| appConfig.confThreshold | 默认 0.3 | 置信度阈值：越低结果越多，越高越严格 |
| appConfig.includeAreas/excludeAreas | 可选 | 区域圈选，仅部分算法支持（见清单「区域」列） |
| algoAppVersion | 默认 v1.0 | open 接口的算法版本参数 |

## 状态码

### 平台状态码

| code | 说明 | 处理建议 |
|------|------|----------|
| 2000 | 成功 | - |
| 12537 | 已开通（user already has the permission） | open 时视为成功（脚本已处理） |
| 12505 | 参数缺失（如 lang cannot be null） | getAlgoExperienceList 必须传 lang（zh/en） |
| 28007 | Header 参数错误 | 检查 uuid、appKey、timeMillis、signature（运行 test 排查） |
| 50000 | 服务器内部错误 | 联系杰峰技术支持 |

### 设备抓图分支（依赖技能）

| 现象 | 处理建议 |
|------|----------|
| 40103 无效 Token | deviceToken 过期（有效期 24 小时），重新获取 |
| DEV_NOTEXIT | 该区域平台查无此设备，换区域探测（token 查询不要求设备在线） |
| synchronize the device login username and password | 平台侧设备凭证未同步，需用户在控制台重新绑定/同步设备密码 |

## 注意事项

- 算法范围 - 仅支持 52 个免底库检测类算法；4 个比对类算法（智能门锁/陌生人识别/猫脸识别/多宠识别）需底库与 openSearchId，不在支持范围，遇到时说明并引导用户去开放平台控制台配置
- 统一接口 - 所有算法共用同一套 v3 接口，靠 appUuid 区分；同步 `callApp`、异步 `pushApp`（本技能默认同步）
- 渲染依赖 - `render_result.py` 依赖 Pillow（`pip install pillow`）；缺失时自动降级为仅输出结构化文本报告，不渲染取证图
- 凭证安全 - appSecret 只存本地 config.json，不回显、不写入导出包
- 结果时效 - 接口返回的原图链接 24 小时有效
- 细节参考 - 接口返回结构、场景速查、错误处理等见 [reference.md](reference.md)

## 相关文件

| 文件 | 说明 |
|------|------|
| SKILL.md | 技能文档 |
| reference.md | 算法清单（52个）、场景速查、接口细节、错误处理 |
| algorithms.json | 算法元数据（appUuid/appName/label/场景分组） |
| scripts/jf_client.py | 主客户端（配置/测试/开通/调用，内置官方签名算法） |
| scripts/render_result.py | 取证图渲染 + 结构化摘要（红框/中文标签/置信度） |
| config.json | 本地凭证（运行时生成，导出时必须排除） |

## 参考文档

杰峰开放平台
