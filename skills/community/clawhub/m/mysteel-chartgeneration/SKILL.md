---
name: Mysteel_ChartGeneration
description: 基于文本描述或数据自动生成各类图表（趋势图、对比图、结构图等）；当用户需要创建可视化图表、将数据转化为直观表达、生成分析报告插图时使用
dependency:
  python:
    - requests
---

# AI图表生成 Skill

## 任务目标
- 本 Skill 用于：通过AI自动生成ECharts图表配置并渲染为HTML文件
- 能力包含：文本描述生图、数据可视化、多种图表类型支持、自动标题生成
- 触发条件：用户要求生成图表、可视化数据、创建分析报告插图

## 前置准备

### API密钥配置（必需）

在调用脚本前，需要先配置API密钥：

**步骤1：检查api_key.md文件**
- 检查项目的references目录下是否存在 `api_key.md` 文件
- 如果不存在，提示用户创建并输入密钥

**步骤2：创建/更新api_key.md文件**
```bash
# 在项目的references目录下创建文件
cd /path/to/my-generation/references
echo "api_key: 你的密钥" > api_key.md
```

**文件格式**：
```
api_key: your_api_key_here
```

**注意**：
- api_key.md文件应在**项目的references目录**下
- 脚本会自动从references目录读取该文件
- 密钥信息将用于接口请求头的token字段
- 每次调用前会检查文件是否存在

**项目目录结构**：
```
my-generation/
├── SKILL.md
├── scripts/
│   ├── generate_chart.py
│   └── render_html.py
└── references/
    ├── api_key.md          # API密钥文件（需要创建）
    └── api-parameters.md
```

### 依赖说明
- 使用 Python 内置模块，需要安装 requests 库（见 dependency 字段）

## 操作步骤

### 智能模式选择（由智能体判断）

根据用户需求，智能体应自动选择最合适的生成模式：

#### 1. FREEDOM模式（自由模式）- 默认推荐

**适用场景**：
- 用户通过自然语言描述图表需求
- 数据量较小或数据已包含在描述中
- 快速原型设计或验证
- 不确定使用哪种模式的场景

**判断依据**：
- 用户输入："生成一个销售趋势图"、"画个柱状图"、"帮我做个对比图表"
- 数据内嵌在描述中："数据为：[100, 200, 300]"
- 没有提供结构化数据文件

**使用方式**：
```bash
node scripts/generate_chart.py --task "用户的自然语言描述"
```

---

#### 2. STRICT模式（严格模式）

**适用场景**：
- 用户提供了结构化数据（JSON数组/对象）
- 数据量较大（超过50条记录）
- 需要高性能数据转换
- 有明确的数据结构说明需求

**判断依据**：
- 用户提供了完整的数据文件或JSON数据
- 数据记录数较多（>50条）
- 用户明确说明数据字段含义

**使用方式**：
```bash
node scripts/generate_chart.py \
  --task "转换任务描述" \
  --mode STRICT \
  --data '{"field1": "value1", ...}' \
  --data-example '[{"field1": "value1"}]' \
  --data-description "数据包含字段1和字段2"
```

---

#### 3. TEMPLATE模式（模板模式）

**适用场景**：
- 用户明确指定图表类型（折线图/柱状图/饼图）
- 需要标准格式的图表
- 快速生成常见图表类型
- 对图表样式要求标准化

**判断依据**：
- 用户明确说："生成一个饼图"、"画条形图"、"用折线图展示"
- 图表类型是标准类型之一
- 数据量适中且结构简单

**使用方式**：
```bash
node scripts/generate_chart.py \
  --task "生成图表描述" \
  --mode TEMPLATE \
  --type 折线图 \
  --data '[{"name": "A", "value": 100}]'
```

---

#### 4. AUTO模式（自动模式）

**适用场景**：
- 智能体无法确定最佳模式
- 需要系统自动选择
- 混合场景

**使用方式**：
```bash
node scripts/generate_chart.py --task "用户需求" --mode AUTO
```

---

### 完整执行流程

1. **检查API密钥配置**
   - 检查 `api_key.md` 文件是否存在
   - 如果不存在，提示用户创建并输入密钥
   - 如果存在，读取密钥信息

2. **分析用户需求**（智能体完成）
   - 提取图表类型、数据来源、数据量、复杂度
   - 根据上述规则选择最合适的模式

3. **调用图表生成脚本**
   - 脚本自动从 `api_key.md` 读取密钥
   - 将密钥设置到请求头的 `token` 字段
   - 根据选择的模式调用 `scripts/generate_chart.py`
   - 传递相应参数（task、mode、data、type等）
   - asyncEnable固定为false（仅支持同步模式）

4. **处理结果**
   - 同步模式：直接获取option配置

5. **渲染HTML文件**
   - 调用 `scripts/render_html.py` 将配置转换为HTML
   - 自动读取meta文件中的标题
   - 返回HTML文件路径

---

## 资源索引

- **必要脚本**：
  - [scripts/generate_chart.py](scripts/generate_chart.py)（调用AI图表生成API，仅支持同步模式）
  - [scripts/render_html.py](scripts/render_html.py)（将ECharts配置渲染为HTML文件）
- **领域参考**：
  - [references/api-parameters.md](references/api-parameters.md)（API参数详细说明和使用示例）
  - [references/api_key.md](references/api_key.md)（API密钥配置文件，需用户创建）

## 注意事项

- **API密钥配置**：首次使用前必须在**项目的references目录**下创建 `api_key.md` 文件并填入密钥，格式为 `api_key: your_key`
- **密钥文件位置**：api_key.md文件必须放在项目的references目录下，脚本会自动从references目录读取该文件
- **密钥传递方式**：密钥会自动从references目录的 `api_key.md` 读取并设置到请求头的 `token` 字段
- **仅支持同步模式**：asyncEnable固定为false，不支持异步处理
- **自动标题生成**：脚本会根据用户的task描述自动生成图表标题，并保存到meta文件中
- **标题使用规则**：render_html.py会自动读取meta文件中的标题，如果找不到则使用默认标题
- **模式选择优先级**：FREEDOM > TEMPLATE > STRICT > AUTO（智能体根据场景自动选择）
- **数据内嵌优先**：如果数据已在task描述中，无需额外提供--data参数
- **STRICT模式要求**：必须提供data、dataExample、dataDescription三个参数
- **TEMPLATE模式限制**：仅支持标准图表类型（折线图、柱状图、饼图等）
- **脚本自动生成唯一的requestId，无需手动指定**
- **HTML文件使用ECharts渲染，支持交互操作**

## 使用示例

### 示例1：自然语言生图（FREEDOM模式）

**用户需求**："帮我生成一个展示2024年各月份销售额的折线图，数据为：[1200, 1500, 1800, 2000, 2200, 2500, 2800, 3000, 3200, 3500, 3800, 4000]"

**智能体判断**：
- 自然语言描述 → FREEDOM模式
- 数据已内嵌 → 无需--data参数

**自动生成标题**：
- 原始task："帮我生成一个展示2024年各月份销售额的折线图，数据为：[1200, 1500, ...]"
- 提取标题："2024年各月份销售额"

**执行步骤**：
```bash
# 1. 检查api_key.md文件（如果不存在，提示用户创建）
# 2. 调用生成脚本（同步模式）
node scripts/generate_chart.py --task "帮我生成一个展示2024年各月份销售额的折线图，数据为：[1200, 1500, 1800, 2000, 2200, 2500, 2800, 3000, 3200, 3500, 3800, 4000]"

# 3. 渲染HTML
node scripts/render_html.py --option-file output/req-xxx_option.json --output output/sales_trend.html
```

**注意**：脚本会自动从 `api_key.md` 读取密钥并设置到请求头

---

### 示例2：指定图表类型（TEMPLATE模式）

**用户需求**："生成一个饼图展示市场份额，数据如下：A产品30%，B产品25%，C产品20%"

**智能体判断**：
- 明确指定"饼图" → TEMPLATE模式
- 数据简单且结构清晰 → TEMPLATE模式优先

```bash
node scripts/generate_chart.py \
  --task "生成一个饼图展示市场份额" \
  --mode TEMPLATE \
  --type 饼图 \
  --data '[{"name": "A产品", "value": 30}, {"name": "B产品", "value": 25}, {"name": "C产品", "value": 20}, {"name": "其他", "value": 25}]'

node scripts/render_html.py --option-file output/req-xxx_option.json --output output/market_share.html
```

---

### 示例3：大数据量处理（STRICT模式）

**用户需求**："我有销售数据文件，包含1000条记录，请生成销量排名前10的柱状图。数据结构：product_name, sales_amount, region"

**智能体判断**：
- 数据量1000条 → STRICT模式
- 有明确数据结构 → 提供dataDescription

```bash
node scripts/generate_chart.py \
  --task "将销售数据转换为柱状图，展示销量排名前10的产品" \
  --mode STRICT \
  --data '$(cat sales_data.json)' \
  --data-example '[{"product_name": "产品A", "sales_amount": 12000, "region": "华东"}]' \
  --data-description "数据包含产品名称、销量金额、区域三个字段"

node scripts/render_html.py --option-file output/req-xxx_option.json --output output/top10_sales.html
```

---

### 示例4：对比类图表（FREEDOM模式）

**用户需求**："画个柱状图对比华东、华南、华北三个区域的钢材库存量，数据：华东5000吨，华南4500吨，华北6000吨"

**智能体判断**：
- 自然语言描述 + 数据内嵌 → FREEDOM模式

```bash
node scripts/generate_chart.py --task "画个柱状图对比华东、华南、华北三个区域的钢材库存量，数据：华东5000吨，华南4500吨，华北6000吨"

node scripts/render_html.py --option-file output/req-xxx_option.json --output output/inventory_comparison.html
```

---

### 示例5：趋势分析（FREEDOM模式）

**用户需求**："生成一个钢联螺纹钢价格走势图，展示最近一年的价格变化趋势"

**智能体判断**：
- 自然语言描述，无明确数据 → FREEDOM模式（AI会自动推断或生成数据）

```bash
node scripts/generate_chart.py --task "生成一个钢联螺纹钢价格走势图，展示最近一年的价格变化趋势"

node scripts/render_html.py --option-file output/req-xxx_option.json --output output/price_trend.html
```

---

## 模式选择决策树

```
用户请求
  ├─ 是否明确指定图表类型？（饼图/柱状图/折线图等）
  │   └─ 是 → TEMPLATE模式
  │
  ├─ 是否提供大量结构化数据？（>50条）
  │   └─ 是 → STRICT模式
  │
  └─ 自然语言描述 + 数据量小/内嵌数据
      └─ FREEDOM模式（默认）
```

**注意**：所有模式均为同步处理，asyncEnable固定为false

---

## 推荐执行流程（智能体视角）

1. **接收用户需求**

2. **检查API密钥配置**：
   - 检查 `api_key.md` 文件是否存在
   - 如果不存在，提示用户："请先配置API密钥，创建 api_key.md 文件并填入密钥，格式：api_key: your_key"
   - 如果存在，继续执行

3. **分析需求特征**：
   - 提取关键词（图表类型、数据、复杂度）
   - 判断数据来源（描述内嵌/提供文件/无数据）
   - 评估数据量级

4. **选择生成模式**：根据上述决策树

5. **构建命令参数**：准备task、mode、data等参数

6. **调用脚本执行**（同步模式）：
   - 脚本自动从 `api_key.md` 读取密钥
   - 密钥自动设置到请求头的 `token` 字段
   - asyncEnable固定为false

7. **渲染HTML并返回**

## API密钥配置示例

### 创建api_key.md文件
```bash
# 在项目的references目录下创建文件
cd /path/to/my-generation/references
echo "api_key: your_actual_api_key_here" > api_key.md
```

### 文件内容格式
```
api_key: sk_abc123xyz789
```

### 错误处理
- 如果文件不存在，脚本会提示：`api_key.md 文件不存在。请先在项目的references目录下创建该文件并填入API密钥。文件路径：{项目目录}/references/api_key.md`
- 如果文件为空，脚本会提示：`api_key.md 文件为空，请填入API密钥。文件路径：{项目目录}/references/api_key.md`
