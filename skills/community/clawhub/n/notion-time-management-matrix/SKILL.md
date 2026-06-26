---
name: notion-time-management-matrix
description:
  待办事项管理技能，用于通过 exec 调用 Python 脚本完成指定 Notion 数据库的连接，基于四象限法则进行时间管理，支持待办事项的创建、查询、搜索、状态更新、截止日期修改与分析总结。当用户提出"明天要做"或"最近有什么重要的事"或"25号前解决"或"把任务延期到下周五"等涉及时间管理内容时触发。
metadata:
  openclaw:
    requires:
      bins:
        - python3
    version: "1.1.1"
    author: "xt Shawn"
    license: "MIT"
    config:
      api_key_path: "~/.config/notion/api_key"
      database_name_path: "~/.config/notion/database_name"
---

# Notion 四象限任务管理

## 1. 触发条件

当用户输入包含以下意图时，触发本技能：

- **添加任务**：用户表达需要记录、创建或新增待办事项的意图，包含任务内容和时间相关信息
- **查询任务**：用户询问指定时间范围内的待办事项（如今天、接下来几天、特定日期范围等），或希望对任务进行总结、统计分析、四象限分类、了解当前任务的整体情况
- **搜索任务**：用户询问特定任务的相关信息，提供关键词或描述
- **更新任务状态**：用户表示已经完成某项任务、想要将任务标记为已完成/进行中/未开始/已取消等状态，可通过任务标题或备注进行匹配
- **更新任务截止日期**：用户希望修改任务的截止日期，或将任务延期，可通过任务标题或备注进行匹配

由于agent默认优先从记忆文件中查询待办事项，因此首次触发用户需明确输入使用技能。

## 2. 用户配置

### 2.1 API 密钥配置
用户需要提供 API 密钥，执行以下命令存储 API 密钥：
   ```bash
   mkdir -p ~/.config/notion
   echo "your_api_key_here" > ~/.config/notion/api_key
   ```
- 禁止从memory记忆文件或TOOLS.md文件或上下文获取API密钥。

### 2.2 数据库配置
用户需要提供数据库名称，执行以下命令存储数据库名称：
   ```bash
   mkdir -p ~/.config/notion
   echo "your_database_name_here" > ~/.config/notion/database_name
   ```

- 如果数据库名称不存在、Notion 连接失败、或缺少必需字段，则提示用户修正配置。
- 禁止从memory记忆文件或TOOLS.md文件或上下文获取数据库名称。
- 禁止在脚本调用失败时自行调用Notion API。

### 2.3 状态文件
- **初始化**：如果状态文件不存在或不完整，调用get_state创建文件并了解数据库基本情况。
- **存储位置**：脚本notion_quadrant_manager.py所在目录下的 `notion_quadrant_manager_state.json`
- **作用**：缓存数据库连接信息、字段映射和任务数据，提高操作效率
- **注意事项**：确保脚本所在目录有写入权限
- **访问方式**：通过 `get_state` 动作获取状态文件中的数据库相关信息，禁止阅读状态文件

### 2.4 依赖安装
脚本需要以下 Python 依赖：
- `requests`：用于发送 HTTP 请求到 Notion API

安装依赖的命令：
```bash
pip3 install requests
```

## 3. 必要字段

识别数据库中与下列语义对应的字段，不要求完全同名，但必须存在对应的 Notion 属性类型和可用枚举值。
- 待办事项（标题字段）
- 截止时间（日期字段）
- 四象限（select/status/multi_select 字段）
- 状态（status/select 字段）
- 备注（rich_text/title 字段）
- 分类（multi_select/select 字段）

## 4. 调用方式

本技能通过 exec 调用SKILL.md同目录scripts文件夹下的 Python 文件：

```bash
python3 ./scripts/notion_quadrant_manager.py <action> '<json_args>'
```

## 5. 可调用动作

### 5.1 get_state
获取database 的相关信息，用于 AI 理解用户数据库的基本情况，并识别必要字段。

**参数**：
- 无需传递参数

**返回**：
- `tasks_count`：状态文件中的任务数量
- `resolved`：数据库解析信息
- `fields`：字段映射
- `last_task`：最近一次操作的任务
- `bootstrapped`：是否执行了 bootstrap 操作

**示例**：
```bash
python3 ./scripts/notion_quadrant_manager.py get_state '{}'
```
### 5.2 add
创建任务。理解用户意图，归纳总结任务标题、备注、分类，识别对话中的日期、四象限、状态，生成结构化数据输出给脚本执行。

**参数**：
- `title`：任务标题（Agent 归纳总结）
- `due_date`：截止日期（ISO 格式）
- `quadrant`：四象限分类（Agent推断）
- `status`：状态（默认：未开始）
- `category`：分类（Agent 归纳总结，可选）
- `note`：备注（Agent 归纳总结，可选）

**返回**：
- 创建的任务信息

**示例**：
```bash
python3 ./scripts/notion_quadrant_manager.py add '{"title":"去北京","due_date":"2026-03-28","quadrant":"重要紧急","status":"未开始","category":"工作","note":"商务出差"}'
```

### 5.3 query
查询指定时间范围内的任务，支持状态过滤，可选择生成总结。

**参数**：
- `start_date`：开始日期（可选，格式：YYYY-MM-DD）
- `end_date`：结束日期（可选，格式：YYYY-MM-DD）
- `days`：天数（可选，当不提供 start_date 和 end_date 时使用，不传时默认：7）
- `status`：任务状态列表（可选，默认：["未开始", "进行中"]）
- `category`：任务分类（可选）
- `quadrant`：任务四象限（可选，如：重要紧急、紧急不重要、重要不紧急、不重要不紧急）
- `summary`：是否生成总结（当用户要求总结时传true，默认：false）

**返回**：
- 指定时间范围内的任务列表（包含超时任务提醒）
- 如果 summary 为 true，还返回四象限统计、重要紧急任务列表、建议提前完成任务列表、超时任务列表和建议

**示例**：
```bash
# 查询指定日期范围的任务
python3 ./scripts/notion_quadrant_manager.py query '{"start_date":"2026-04-01","end_date":"2026-04-07","status":["未开始", "进行中"]}'

# 查询最近 7 天的任务并生成总结
python3 ./scripts/notion_quadrant_manager.py query '{"days":7,"summary":true}'

# 查询指定分类和四象限的任务
python3 ./scripts/notion_quadrant_manager.py query '{"days":7,"category":"工作","quadrant":"重要紧急"}'
```

### 5.4 search
搜索指定任务。

**参数**：
- `query`：查询关键词

**返回**：
- 所有匹配到的任务（按相似度排序）

**示例**：
```bash
python3 ./scripts/notion_quadrant_manager.py search '{"query":"北京出差"}'
```

### 5.5 update_status
更新任务状态和/或截止日期。优先使用任务标题或备注进行精确匹配，更新失败或不确定具体任务参数就使用search方法和用户确认。

**参数**：
- `title`：任务标题（用于查找任务，必选）
- `note`：任务备注（用于查找任务，可选）
- `status`：任务状态（可选，如：未开始、进行中、完成等）
- `due_date`：任务截止日期（可选，格式：YYYY-MM-DD）

**返回**：
- 更新后的任务信息

**示例**：
```bash
# 通过任务标题更新状态为进行中
python3 ./scripts/notion_quadrant_manager.py update_status '{"title":"去北京","status":"进行中"}'

# 通过任务备注更新截止日期
python3 ./scripts/notion_quadrant_manager.py update_status '{"note":"商务出差","due_date":"2026-04-15"}'

# 同时更新任务状态和截止日期
python3 ./scripts/notion_quadrant_manager.py update_status '{"title":"去北京","status":"进行中","due_date":"2026-04-15"}'
```


## 6. 四象限处理

### 6.1 写入数据时四象限推测规则
- 是否重要：任务内容凡涉及领导、父母等重要关系人，涉及学习、健康、资金处理、晋升，涉及事先承诺的均为重要
- 是否紧急：任务完成日期距今天小于等于2天的均为紧急
- 如判定成功，请在写入数据完成后告知用户写入的四象限分类
- 如无法判定重要性或紧急性，直接询问用户四象限分类

### 6.2 总结分析流程
1. 检查数据库中是否有四象限字段，如有则直接使用该值判定
2. 基于用户不同象限的任务数量，基于减少紧急任务数量、专注重要任务的原则，给出当前任务情况统计和建议

## 7. 超时任务处理

- 识别截止时间早于当前时间的任务
- 在查询和总结时单独列出这些任务
- 使用醒目的方式提醒用户这些任务已超时
- 超时任务优先显示在任务列表顶部

## 8. 输出要求

Python 脚本返回 JSON，至少包含：
- `ok`：操作是否成功
- `action`：执行的动作
- `message`：操作结果消息
- `data`：操作结果数据

Agent 读取 JSON 后，根据回复消息的平台（微信、飞书等），选择合适的排版（列表、表格、分割线、图标等）对齐并罗列任务，组织自然语言回复给用户，保证内容清晰，重点突出。

**微信QQ示例**：
```
⏰ 任务归类 x2
1.title-1
  （进行中/3.28/重要紧急）📚
2.title-2
  （进行中/3.28/重要紧急）💼

```



