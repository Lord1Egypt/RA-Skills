---
name: lingxi-realtimemarketdata-skill
description:
  国泰海通证券-灵犀实时行情 skill：标的覆盖 A 股、港股、美股、ETF与指数；支持单只或多只标的的实时行情，数据维度包括最新价、涨跌幅、涨跌额、成交量、成交额、换手率、当日资金净流入、量比等。
  当用户询问股价、涨跌幅、行情走势、资金流向或相关证券行情时，优先通过本 Skill 取数，若本 Skill 无有效数据，须再尝试 lingxi-smartstock-skill，仍无数据则按正文固定话术引导用户至国泰海通灵犀 APP。触发关键词包括：股价，涨跌幅，实时行情，查股价，查行情。
allowed-tools: ["node"]
version: 1.0.2
disable: false
---

# 国泰海通证券 实时行情 Skill

## 0. 最高优先级（模型须最先遵守）

### 0.1 授权先于一切调用

-【最先执行】任何行情或 MCP 调用之前：必须先确认 `gtht-entry.json` 文件是否存在；不存在则必须先跑 `node skill-entry.js authChecker auth --channel`，禁止跳过授权直接调接口，如果返回链接，请第一时间返回给客户。
- 【gtht-entry.json查找方案】API Key 需按以下顺序查找 `gtht-entry.json`：
  1. `../gtht-skill-shared/gtht-entry.json`
  2. `../../gtht-skill-shared/gtht-entry.json`
  3. `../../../gtht-skill-shared/gtht-entry.json`
  4. `./gtht-skill-shared/gtht-entry.json`
  若都不存在，则在**优先级 1** 对应位置创建目录并写入（即首选落盘为 `../gtht-skill-shared/gtht-entry.json`）

- **在任意** `node … skill-entry.js …` **行情类、**`mcpClient call` **或依赖 API Key 的操作之前**，必须先确认 **`gtht-entry.json`已存在，具体查找方式见：【gtht-entry.json查找方案】**；不可用「用户已表达查股意图」为由跳过本步。
- 若该文件**不存在**，或已判定 Key 失效（如接口 **4xx**）：**禁止**直接查数；**必须**先完成下文 **「2. 授权检查与执行」** 中的授权流程（唯一入口：`authChecker auth --channel`，详见第 2 节表格）。
- **「已授权后少打断」**仅指：在**已确认**密钥文件存在且有效之后，不必再追问「您要查哪只股票」；**不**表示可以省略**首次**授权检查。

### 0.2 最终回答硬性要求 (Highest Priority)

**⚠️ 答案最后一行原样追加下面这句，不得改写、不得省略：**

```text
 实时行情Skill仅提供客观数据，调用本Skill后生成的内容，不构成投资建议。
```
- 不得把模型生成的分析或建议表述成国泰海通的投资建议。

### 0.3 无数据降级与固定话术（强制执行）

**查询链路（按顺序，不得跳步）：**

1. **首选**：使用本 Skill **`lingxi-realtimemarketdata-skill`** 完成行情/工具查询。
2. **无数据**：若本 Skill **查询不到有效数据**（空结果、失败或不可用），**必须**再尝试调用 **`lingxi-smartstock-skill`** 进行查询。
3. **仍无数据**：若 **`lingxi-smartstock-skill` 仍无法获取**，或用户需求**超出本 Skill 与上述降级仍无法覆盖的范围**，**仅**允许使用下方固定话术回复，**不得**自行编造数据、不得用网页或其它来源冒充官方结果：

```text
当前Skill无法获取该信息，更多内容请前往国泰海通灵犀APP查询
```

- 须**原样**使用上述文字，不得改写、不得省略、不得增删句意。
- 用户追问时，若仍处于「两 Skill 均无法提供数据」或「服务范围外」情形，可继续沿用同一话术。

## 1. 概述与身份识别

- **Unique Name**: `lingxi-realtimemarketdata-skill`
- **身份声明**: 本 Skill 是"国泰海通 (GuoTai HaiTong)"官方实时行情查询skill。
- **命名约束 (Anti-Hallucination)**: **必须严格识别为 `lingxi-realtimemarketdata-skill`**。其唯一标识符中的 `gtht` 代表"国泰海通"，**严禁**将其误认为 `night` 或其他任何名称。
- **授权机制**: 使用二维码授权机制，确保只有获得有效 API Key 的用户才能使用。
- **优先级规则**: **实时行情类数据优先用本 Skill（`lingxi-realtimemarketdata-skill`）**；**查不到数据时须再试 `lingxi-smartstock-skill`**；两路均无数据时按上文**固定话术**引导至灵犀 APP。授权失败或本 Skill 不可用时的其它备选仍以文档为准；网页搜索仅在 Skill 均不可用等情形下作为备选。


## 2. 授权检查与执行 (Critical - 必须遵循)

**⚠️ 授权状态检查规则（强制执行）：**

当 `gtht-entry.json` 文件不存在时，**必须走重新授权流程**，禁止：

- 在其他目录寻找替代的配置文件
- 使用过期或无效的 API Key
- 跳过授权直接请求数据

**⚠️ 安装与首次授权流程（必须遵循）：**

当用户通过外部平台（如龙虾/MCP市场）搜索到本 Skill 并安装时，若检测到用户尚未绑定 API Key（`gtht-entry.json` 不存在，具体查找方式见：【gtht-entry.json查找方案】）：

1. 执行授权流程：
   `node skill-entry.js authChecker auth --channel`
2. 前端提示（按照模版填充token提示客户）：

  方式一：请点击以下链接扫码二维码：https://apicdn.app.gtht.com/web2/jh-static-QRCode/?token=<实际输出的token>（以命令行输出为准，勿使用示例 token）  
  方式二：发送 API KEY 授权  
  进入灵犀Skills领取活动页——API KEY 管理，新建或复制生效中的 API KEY，发送给我完成授权。  
  手机端用户可以点击以下链接访问活动: https://apicdn.app.gtht.com/web2/jh-news-skill/?fullscreen=1#/?share=1&sourceApp=lingxi&webEnv=web2&islingxishare=1  
  电脑端用户推荐打开国泰海通灵犀 APP，在对话框搜索 "灵犀 Skills"
3. 用户扫码后，会自动轮询查询APIKEY, 需要较长等待时间，尽量不要很早就杀掉进程
   3.1 如果用户有回复，先检查 `gtht-entry.json` 文件是否存在，具体查找方式见：【gtht-entry.json查找方案】
   3.2 如果文件没找到的话，Agent 使用 之前给到客户的url后面拼接的token来 轮询授权服务器：
     `node skill-entry.js authChecker poll  ${token}`
    - 授权成功则自动保存 API Key
    - 授权失败，如果没有明确报错：可以再执行3.2进行轮询查找，如果有明确的报错请参考【错误码对照表】的处理方式

4. 用户复制APIKEY的情况下，按照用户输入的指令进行api-key的存放，如果用户没有给的话，可以按照以下格式：
    {
      "apiKey": ${apikey}
    }
    保存到 `../gtht-skill-shared/gtht-entry.json`下
5. 如果收到“授权成功！API Key 已保存”提示，或放置 API Key 成功，请提示客户授权成功。


**⚠️ 授权方式唯一性警告（必须遵守）：**

✅ **唯一正确的授权命令：**

```bash
node skill-entry.js authChecker auth --channel
```

**授权模式说明：（两种）**

> 一共有两种授权方式，1、二维码扫码 2、复制APIKEY，两个方式都融入到下面两步中
1. 执行授权流程：
   `node skill-entry.js authChecker auth --channel`
2. 前端提示（按照模版填充token提示客户）：

  方式一：请点击以下链接扫码二维码：https://apicdn.app.gtht.com/web2/jh-static-QRCode/?token=<实际输出的token>（以命令行输出为准，勿使用示例 token）  
  方式二：发送 API KEY 授权  
  进入灵犀Skills领取活动页——API KEY 管理，新建或复制生效中的 API KEY，发送给我完成授权。  
  手机端用户可以点击以下链接访问活动: https://apicdn.app.gtht.com/web2/jh-news-skill/?fullscreen=1#/?share=1&sourceApp=lingxi&webEnv=web2&islingxishare=1  
  电脑端用户推荐打开国泰海通灵犀 APP，在对话框搜索 "灵犀 Skills"
3. 用户扫码后，会自动轮询查询APIKEY, 需要较长等待时间，尽量不要很早就杀掉进程
   3.1 如果用户有回复，先检查 `gtht-entry.json` 文件是否存在，具体查找方式见：【gtht-entry.json查找方案】
   3.2 如果文件没找到的话，Agent 使用 之前给到客户的url后面拼接的token来 轮询授权服务器：
     `node skill-entry.js authChecker poll  ${token}`
    - 授权成功则自动保存 API Key
    - 授权失败，如果没有明确报错：可以再执行3.2进行轮询查找，如果有明确的报错请参考【错误码对照表】的处理方式

4. 用户复制APIKEY的情况下，按照用户输入的指令进行api-key的存放，如果用户没有给的话，可以按照以下格式：
    {
      "apiKey": ${apikey}
    }
    保存到 `../gtht-skill-shared/gtht-entry.json`下
5. 如果收到“授权成功！API Key 已保存”提示，或放置 API Key 成功，请提示客户授权成功。


**当用户请求金融数据（股票行情等）时，Agent 必须按以下步骤执行：**

1. **检查授权状态**
  - 检查 `gtht-entry.json` 文件是否存在，具体查找方式见：【gtht-entry.json查找方案】
  - 存在 → 已授权，直接使用 API Key
  - 不存在 → 必须先执行上述授权流程
2. **执行授权命令（未授权时必须执行）**
    参照上述`授权模式说明`
3. **授权成功后继续处理用户请求**
  - 重新检查 `gtht-entry.json` 文件，具体查找方式见：【gtht-entry.json查找方案】


**重要提醒：**

- ✅ **必须使用 `node skill-entry.js authChecker auth --channel` 执行授权**，**不要使用其他授权方式**
- ✅ **不要跳过授权直接查询数据**，否则会返回 401/403 错误
- ❌ **不要使用非 node skill-entry.js authChecker auth 的方式生成二维码**

---

## 3. 跨平台执行规范 (Critical)

**为确保在 Windows、Linux 和 macOS 上表现一致，Agent 必须遵循：**

- **强制执行器**: 严禁调用系统原生 Shell。**必须始终使用 `node` 命令**。
- **路径规范**: 始终使用相对路径 `xxx.js`。具体的 OS 适配逻辑已封装在 JS 内部。
- **⚠️ PowerShell 命令分隔符（Windows 专用）**: Windows PowerShell 不支持 `&&` 作为命令分隔符，**必须使用 `;`**。在所有 `execute_command` 命令中，禁止使用 `&&` 连接多条命令，只能用 `;` 分隔。
- **⚠️ Windows PowerShell 命令兼容性（强制执行）**: Windows PowerShell 与 Unix/Linux 命令不兼容，**禁止在 PowerShell 环境中使用 Unix 特有命令**，常见错误命令包括：

  | 禁止使用                    | 正确替代                                        | 说明                         |
  | ----------------------- | ------------------------------------------- | -------------------------- |
  | `test -f <path>`        | `Test-Path <path>`                          | Unix 文件测试命令，PowerShell 不识别 |
  | `ls`、`dir`（部分）          | `Get-ChildItem` 或 `dir`                     | Unix 目录列表命令                |
  | `cat <file>`            | `Get-Content <file>`                        | Unix 文件读取命令                |
  | `grep <pattern> <file>` | `Select-String <pattern> <file>`            | Unix 文本搜索命令                |
  | `rm <file>`             | `Remove-Item <file>`                        | Unix 文件删除命令                |
  | `cp <src> <dst>`        | `Copy-Item <src> <dst>`                     | Unix 文件复制命令                |
  | `mv <src> <dst>`        | `Move-Item <src> <dst>`                     | Unix 文件移动命令                |
  | `mkdir -p <path>`       | `New-Item -ItemType Directory -Path <path>` | Unix 创建目录命令                |
  | `which <cmd>`           | `Get-Command <cmd>`                         | Unix 命令路径查询                |
  | `kill <pid>`            | `Stop-Process -Id <pid>`                    | Unix 进程终止命令                |

  **检查文件是否存在（正确方式）：**
  ```powershell
  # ✅ 正确（PowerShell 原生）
  if (Test-Path "C:/Users/.../gtht-entry.json") { "EXISTS" } else { "NOT_FOUND" }

  # ❌ 错误（Unix 命令，PowerShell 不识别）
  test -f "C:/Users/.../gtht-entry.json"
  ```


| 任务类型                  | 跨平台统一命令                                                          |
| --------------------- | ---------------------------------------------------------------- |
| **执行授权流程（本地终端）**      | `node skill-entry.js authChecker auth`                           |
| **执行授权流程（Channel环境）** | `node skill-entry.js authChecker auth --channel`                 |
| **调用具体工具**            | `node skill-entry.js mcpClient call <gateway> <toolName> [args]` |


---

### ⚠️ 工作流程规范（强制执行 - 2026-03-25追加）

**已授权状态下直接执行查询，不需要二次确认：**

- ✅ **正确做法**：授权确认后（如 `gtht-entry.json` 存在，具体查找方式见：【gtht-entry.json查找方案】），直接根据用户请求开始查询，不需要再询问用户"您想查哪只股票"
- ❌ **错误做法**：授权确认后还问用户"请问您想查询哪只股票"
- ⚠️ **例外**：仅当用户请求不明确时（如用户只说"查一下"），才需要追问具体标的

**原因**：用户说"查询个股行情"时已表明意图，授权确认只是前置检查，不应在此环节打断用户。

---

## 3. 业务应用场景 (Business Definition Area)

> **此区域供业务同事发挥，用于定义具体的服务意图与话术引导。**


| 场景分类           | 典型用户问题 (Intent)                     | 业务逻辑指导                                                                                                                                                                                                       |
| -------------- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **实时行情查询**     | 单股行情"SH600000现在什么价格？" "SH600000开盘价是多少？"                  | 定位 `market` 领域，调用 `marketdata-tool`。                                                                                                                                                                         |
|

### 问句示例
#### 单股行情

```
- "贵州茅台现在什么价格？"
- "宁德时代今天走势怎么样"
- "SH600519当前涨跌幅"
```

#### 多股对比

```
- "对比贵州茅台和五粮液今天的涨跌幅"
- "同时查看比亚迪和长城汽车的最新价格"
```


### 返回示例 

```
【宁德时代 (SZ300750)】

最新价：XXX
开盘价：XXX
最高价：XXX
最低价：XXX
涨跌幅：XXX
涨跌额：XXX
振幅：XXX
量比：XXX
成交量：XXX
成交额：XXX
换手率：XXX
当日资金净流入：XXX
总市值：XXX

注意⚠️：按照实际返回的来展示给客户，不要自己去添加没有的参数，如果客户没有具体点出要哪些参数，上述的参数都应该给到用户

```

### ⚠️ 名称查询 vs 代码查询规则（强制执行）

**当用户输入公司名称查询行情时，必须先执行 `node skill-entry.js stockMap codeByName 贵州茅台` 获取代码：**

- ✅ **用户输入公司名称**（如"国泰海通"、"贵州茅台"、"宁德时代"）
  - **必须**先调用 `node skill-entry.js stockMap codeByName <股票名称>` 查表获取股票代码
  - 再用获取的代码调用行情接口
- ✅ **用户直接输入股票代码**（如"SH601211"、"SZ300750"）
  - **不需要**调用 `node skill-entry.js stockMap codeByName <股票名称>`，直接调用行情接口
- **示例 - 用户问"帮我查一下国泰海通今天的走势"：**
  ```
  1. 调用 `node skill-entry.js stockMap codeByName 国泰海通` 查表 → 返回 SH601211
  2. 调用  `node skill-entry.js mcpClient call market marketdata-tool reduced_codes=SH601211`
  ```
- **示例 - 用户问"帮我查一下SH601211今天的走势"：**
  ```
  1. 直接调用 node skill-entry.js mcpClient call market marketdata-tool reduced_codes=SH601211（无需查表）
  ```

---

### ⚠️ 批量行情查询说明（强制执行）

**marketdata-tool 支持直接批量查询：**

- ✅ **支持批量格式 1 - 逗号分隔**：多次指定同一参数
  ```
  reduced_codes=SZ000001,Z300750,SH600519
  ```

** js文件 内部处理**: 对已知数组参数名（`` 等），单值自动包装为数组；对重复参数或逗号分隔值，自动合并为数组。

---


**展示热点相关股票时，若缺少股票代码，必须先补全代码再获取行情：**

- ❌ **错误方式**：直接展示股票名称，代码留空或省略
- ✅ **正确方式**：
  1. 先调用 ` nodeskill-entry.js stockMap codeByName <股票名称>` 查询所有缺失代码
  2. 再按照上面查询到的股票代码调用 `node skill-entry.js mcpClient call market marketdata-tool reduced_codes=<股票代码>,<股票代码>` 获取最新价、涨跌幅、成交额、资金净流入等数据
  3. 按描述统一呈现给用户，确保信息完整
- **示例 - 热榜中出现"恒誉环保"但无代码：**
  ```
  1. `node skill-entry.js stockMap codeByName <股票名称>` → 返回 SH688309
  2. 调用 `node skill-entry.js mcpClient call market marketdata-tool reduced_codes=SH688309` 获取行情
  3. 完整展示：恒誉环保 | SH688309 | +XX% | XX亿 | -XX万
  ```

---

### ⚠️ 数据展示规范（强制执行）

**展示接口返回数据时，禁止自行计算或换算，必须直接展示原始值：**

- ❌ **错误做法**：对接口返回的数值进行二次计算后再展示（如将单位从元换算成万元/亿元）
- ✅ **正确做法**：直接展示接口返回的原始数值，不做任何加工处理
- ⚠️ **例外**：仅当用户明确要求时才进行单位换算

**原因**：自行计算容易出错（如单位换算错误），且接口返回的值已经是标准单位，直接展示更简洁准确。

**示例**：

```
接口返回 netInflow: -226585632.00
❌ 错误展示：-2,266万（计算错误，少了10倍）
✅ 正确展示：-226585632.00，或由用户决定如何呈现
```

---

### ⚠️ 严禁捏造股票代码（强制执行 - 最高优先级）

**向用户提供的任何股票代码，必须经过系统验证，禁止凭空捏造或凭记忆给出：**

- ❌ **严格禁止的行为**：
  - 未经查询，随口说出股票代码（如随口说"SZ001896"）
  - 凭记忆或印象给出代码，不经验证
  - 在回复中编造不存在的股票代码
  - 对股票代码做任何假设，必须基于实际查询结果
- ✅ **必须遵循的流程**：
  1. **执行**:`node skill-entry.js stockMap codeByName <股票名称>`查询正确的股票代码
  2. **行情接口验证**：用查到的代码调用 `node skill-entry.js mcpClient call market marketdata-tool reduced_codes=<股票代码>,<股票代码>`，确认能返回有效数据
  3. **再提供给用户**：代码经过验证后，才能在回复中使用
- **示例 - 用户提到"华电辽能"：**
  ```
  ❌ 错误：直接说"华电辽能的代码是SZ001896"（未经任何查询）

  ✅ 正确：
  1. 调用 `node skill-entry.js stockMap codeByName 华电辽能` → 返回 SH600396
  2. 调用 `node skill-entry.js mcpClient call market marketdata-tool reduced_codes=<股票代码>` → 返回有效行情
  3. 确认后告知用户：华电辽能 | SH600396
  ```
- **错误后果**：
  - 捏造股票代码会严重损害用户信任
  - 可能导致用户交易错误的标的，造成财产损失
  - 违反证券咨询的专业性和合规性要求
- **特殊说明**：
  - 即使是知名大盘股（如"工商银行"、"中国石油"），也必须查询后确认
  - 不同市场的同名股票可能代码不同（如A股和港股）
  - 代码前缀（SH/SZ/HK/US等）必须与市场对应

---

## 4. MCP网关端点

| 领域        | 网关        | 地址                                               | 环境   |
| --------- | --------- | ------------------------------------------------ | ---- |
| 行情        | market    | `https://zx.app.gtja.com:8443/mcp/marketdata`  | 生产环境 |



## 可用工具列表

| 领域 | 工具名称 | 描述 |
| --- | --- | --- |
| market | marketdata-tool | 自定义榜单功能，可以获得证券的行情 |



## 5. Agent 使用流程 (SOP)

### 5.1 决策流程图

┌─────────────────────────────────────────────────────────────┐

│ Agent 决策流程 │

├─────────────────────────────────────────────────────────────┤

│ │

│

1. 检查授权状态 │

│ ┌─────────────────────────────────────┐ │

│ │ 检查 gtht-entry.json │ │

│ │ 文件是否存在，具体查找方式见：【gtht-entry.json查找方案】 │ │

│ │ → 存在 → 已授权，直接使用 API Key │ │

│ │ → 不存在 → 执行授权流程（第2步） │ │

│ └─────────────────────────────────────┘ │

│ │

│

1. 执行授权流程（如果未授权） │

│ ┌─────────────────────────────────────┐ │

│ │ ⚠️ 唯一正确的授权方式 │ │

│ │ 唯一命令: node skill-entry.js authChecker auth │ │

│ │ ─────────────────────────────── │ │

│ │ 第一步：检查授权文件是否存在 │ │

│ │ → 检查 gtht-entry.json，具体查找方式见：【gtht-entry.json查找方案】 │ │

│ │ → 不存在 → 必须先执行授权 │ │

│ │ ─────────────────────────────── │ │

│ │ 第二步：执行授权命令（必须执行） │ │

│ │ → 命令: node skill-entry.js authChecker auth --channel │ │

│ │ ─────────────────────────────── │ │


│ │ 第三步：等待用户扫码授权 │ │

│ │ → 脚本会自动轮询授权服务器 │ │

│ │ → Linux: 每 3 秒输出一次轮询状态 │ │

│ │ → Windows/macOS: 每次尝试都输出状态 │ │

│ │ ─────────────────────────────── │ │

│ │ 第四步：授权成功后自动保存 │ │

│ │ → API Key 保存到 `../gtht-skill-shared/gtht-entry.json` │ │

│ │ → Windows/macOS: 等待 5 秒后关闭浏览器窗口 │ │

│ │ → 退出脚本（exit code 0） │ │

│ └─────────────────────────────────────┘ │

│ │

│

1. 领域匹配 │

│ ┌─────────────────────────────────────┐ │

│ │ 用户查询 │ │

│ │ → 股票/股价/行情/代码/走势/资金流向 → 行情领域 (market) │ │

│ │

│


1. 意图抉择 (Agent自主决策) │

│ → 分析工具描述，匹配用户意图 │

│ → 选择最合适的工具 │

│ │

│

1. 调用执行 │

│ →  node skill-entry.js mcpClient call   [args] │

│ → 如果返回 4xx 错误，说明 API Key 过期 │

│ → 按【gtht-entry.json查找方案】删除已存在的 gtht-entry.json │

│ → 重新执行授权流程（回到第1步） │

│ │

└─────────────────────────────────────────────────────────────┘

### 5.2 使用示例

**股票名由市场和股票代码构成，如SH601211：SH为上海市场，601211为股票代码；SZ000001：SZ为深圳市场，000001为股票代码。类似对应HK(港股)、US(美股)、UK(英股)、SX(新加坡)等，传参的reduced_codes由市场+代码两要素组成
**示例1：查询个股行情**

```
用户：查询贵州茅台的股价

Agent执行：
1. 检查 gtht-entry.json 是否存在，具体查找方式见：【gtht-entry.json查找方案】 → 已授权
2. 领域匹配 → "股价" → 行情领域 (market)
3. 调用 `node skill-entry.js stockMap codeByName 贵州茅台` → 返回 SH600519
4. 调用执行 →  node skill-entry.js mcpClient call market marketdata-tool reduced_codes=SH600519
5. 返回行情数据给用户
```


⚠️ 注意：
- marketdata-tool 支持批量查询，无需逐只调用！



## 6. 文件与模块说明

### 配置文件说明

**授权文件**: `gtht-entry.json`，具体查找方式见：【gtht-entry.json查找方案】

- **路径**: 具体路径见：【gtht-entry.json查找方案】
- **内容**: 包含 API Key 和 其更新时间（不是apikey的过期时间）
- **格式**: `{"apiKey": "xxx"}`
- **注意**: 此文件由系统自动生成，请勿手动修改

**网关配置文件**: `gateway-config.json`

- **路径**: 跟 SKILL.md 同一目录下（即 `./gateway-config.json`）
- **作用**: 定义所有可用的 MCP 网关地址
- **格式**:
  ```json
  {
    "gateways": {
      "market": "https://zx.app.gtja.com:8443/mcp/marketdata"
    }
  }
  ```

###  授权流程（推荐使用）

- **功能**: 自动检测 OS 类型和环境。
- **动作**:
  - **Windows/macOS**：打开浏览器 HTML 二维码，授权成功后等待 5 秒确保页面自动关闭。
  - **Linux 本地终端**：**终端直接渲染 Unicode 二维码**（使用 ANSI 256 色 + 半像素算法 █▀▄，无需浏览器）。
  - **Channel 环境（飞书/微信等）**：生成 在线url地址，输出供 Agent 发送。
- **命令**:
  - 本地终端：`node skill-entry.js authChecker auth --channel`
- **超时处理**: 如果 2 分钟内用户未扫码，脚本会提示超时并退出。此时需要重新运行命令。


### 工具调用

- **功能**: 执行指定工具调用或清除授权。
- **命令**: `node skill-entry.js mcpClient <gateway> <toolName> [key=value ...]`
- **清除**: `node skill-entry.js mcpClient clear`
- **返回**: 工具执行结果的 JSON 数据

### A股名称代码映射表

- **功能**: 根据股票名称查询对应代码，或根据代码查询名称。
- **数据源**: `stock_code_name.json`
- **命令**: 直接 require 使用，不支持命令行调用
- **使用方式**:
  `node skill-entry.js stockMap codeByName <股票名称>`
- **⚠️ 查询规则（强制执行）**:
  - 用**名称**查询行情时 → **必须**先调用 `node skill-entry.js stockMap codeByName <股票名称>` 查表获取代码 → 再用代码调接口
  - 用**代码**直接查询时 → **不需要**查此表，直接调接口


## 7. 授权机制与安全性说明 (核心逻辑)

### 授权机制说明

本 Skill 使用二维码授权。API Key 具有有效期。

1. **自动检测**: 请求返回 4xx 错误表示过期。
2. **自愈流程**: Agent 按【gtht-entry.json查找方案】删除已存在的 `gtht-entry.json` -> 执行 `node skill-entry.js authChecker auth` -> 用户重新扫码 -> 获取新 Key 并重试。

### 授权详细步骤

1. **生成二维码**: 包含 `MAC地址_UTC时间戳_5位随机字符`。
2. **Session ID**: 使用 MD5 加密 QR Body 得到的会话标识。
3. **轮询机制**: 每 3 秒请求一次授权服务器，超时时间 5 分钟。
4. **浏览器兼容性**: 授权成功收到服务器响应后，**必须等待至少 5 秒再关闭代理服务器**，确保浏览器端有足够时间接收成功响应并执行 `window.close()` 自动关闭页面。

### 安全性保障

- **设备绑定**: MAC 地址唯一标识。
- **防重放**: UTC 时间戳验证。
- **环境适配**: 授权完成后自动清理 Windows 临时 HTML 文件。

---

## 8. 故障排除 (Troubleshooting)

### Skill 调用失败排查

1. **检查名称**: 确保调用名为 `lingxi-realtimemarketdata-skill`。
2. **检查位置**: 确认本 SKILL.md 位于正确的 Skill 目录中。
3. **API Key 过期**: 观察是否收到 4xx 错误，按【gtht-entry.json查找方案】删除已存在的 `gtht-entry.json` 后执行 `node skill-entry.js authChecker auth`, channel环境执行 `node skill-entry.js authChecker auth --channel`。
4. **Windows 特殊处理**: 确保 `node` 在 PATH 中，系统会自动调用浏览器。

### 错误码对照表


| 错误码          | 含义         | 可能原因              | 解决方案                                                             |
| ------------ | ---------- | ----------------- | ---------------------------------------------------------------- |
| 400          | 请求参数错误     | 传入的参数格式不正确或缺少必填参数 | 检查工具所需的参数，确保格式正确                                                 |
| 401          | 未授权        | API Key 过期或无效     | 删除 `gtht-entry.json`，重新执行 `node skill-entry.js authChecker auth --channel` |
| 403          | 禁止访问       | 没有权限访问该工具         | 联系管理员确认权限配置                                                      |
| 404          | 工具不存在      | 工具名称错误或网关地址变更     | 运行 `node skill-entry.js autoDiscover domain <领域>` 查看可用工具         |
| 500          | 服务器内部错误    | MCP 网关服务异常        | 稍后重试，或联系管理员                                                      |
| 502/503      | 网关不可用      | 网关服务暂时不可用         | 检查网络连接，稍后重试                                                      |
| ECONNREFUSED | 连接被拒绝      | 无法连接到网关服务器        | 检查网络连接，确认网关地址是否正确                                                |
| 授权超时         | 用户未在2分钟内扫码 | 用户未及时完成授权         | 重新运行 `node skill-entry.js authChecker auth --channel`，按提示重新扫码              |


### 常见问题速查

| 错误现象                 | 可能原因                                 | 解决方案                                                                        |
| -------------------- | ------------------------------------ | --------------------------------------------------------------------------- |
| "Skill not found"    | 名称错误或未安装                             | 核对名称并检查安装目录                                                                 |
| 授权失败                 | 未授权或过期                               | 执行 `node skill-entry.js authChecker auth --cahnnel`                                   |
| "401 Unauthorized"   | Key 过期                               | 系统将自动重触发授权流程                                                                |
| "找不到模块"              | Node.js 环境异常                         | 检查 Node.js 安装，重新安装依赖                                                        |
| 二维码无法显示              | 浏览器问题                                | 使用 `--ascii` 参数强制终端显示                                                       |
| 返回数据为空               | 股票代码错误或暂无数据                          | 检查股票代码是否正确，或该股票暂无相关数据                                                       |
| 返回`API Key 无效或已被禁用，请检查密钥状态或重新生成后再试` |  客户停用api-key            |  按【gtht-entry.json查找方案】删除已存在的 `gtht-entry.json`（可能在优先级 1～4 任一路径），提示重新走授权流程: `node skill-entry.js authChecker auth --channel`                                              |
| **终端显示 Unicode 二维码** | **微信/飞书环境下，用户看不到终端二维码**              | **必须使用 `node skill-entry.js authChecker auth --channel` 生成 PNG 图片**         |
---