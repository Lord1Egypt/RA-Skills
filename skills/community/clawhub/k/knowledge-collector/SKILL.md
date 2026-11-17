---
name: knowledge-collector
description: "Collect and catalogize equipment institute knowledge from group chats, manual entries, or batch i..."
tags: [domain-specific, plc, file-based, template-based, api-integration]
version: 1.0.0

# Knowledge Collector - 装备所知识收集与入�?
## 触发条件

以下情况激活此技能：
- 用户�?记录知识"/"录入知识"/"知识收集"/"导入知识"
- 群聊中出现技术知识分享类消息（关键词自动识别�?- 用户指定文件夹路径要求批量导�?
## 知识分类体系

### 4大方�?| 方向 | 关键词示�?|
|------|-----------|
| 非标自动�?| 装配线、工装、夹具、气缸、PLC、输送、焊�?|
| 物流自动�?| WCS、AGV、堆垛机、输送线、分拣、仓储、调�?|
| 工业视觉 | 缺陷检测、视觉、相机、光源、镜头、OpenCV、Halcon、YOLO |

### 4个层�?| 层级 | 含义 | 内容类型 |
|------|------|---------|
| L1 | 方案�?| 整体方案文档、系统架�?|
| L2 | 设计�?| 详细设计文档、图纸、选型说明 |
| L3 | 代码�?| 可执行代码、脚本、函�?|
| L4 | 经验�?| 踩坑记录、最佳实践、故障排�?|

### 5种知识类�?- **方案�?* �?模板: `templates/solution.md`
- **设计�?* �?模板: `templates/design.md`
- **软件�?* �?模板: `templates/software.md`
- **算法�?* �?模板: `templates/algorithm.md`
- **经验�?* �?模板: `templates/experience.md`

## 收集入口

### 入口1: 群聊自动识别
监听群聊消息，当包含技术关键词（见 `config/keywords.json`）时自动触发�?1. 提取消息文本
2. 调用 `classify()` 自动分类
3. 调用 `extract_metadata()` 提取结构化信�?4. 填充对应模板
5. 入库 + 推送负责人

### 入口2: 主动记录
用户 @AI �?记录一条知�?，然后提供内容：
1. 接收用户输入（可以是自由文本�?2. 自动分类 + 提取
3. 展示预览，用户确�?4. 入库 + 推送负责人

### 入口3: 批量导入
给定文件夹路径：
1. 扫描文件夹（.md/.txt/.py/.st/.cpp/.pdf�?2. 对每个文件执行分�?提取+入库
3. 输出导入报告

## 执行流程

```
输入 �?classify(text) �?extract_metadata(text) �?fill_template() �?save_to_domain_kit() �?notify_reviewer()
```

### Step 1: 自动分类
```python
from scripts.collector import classify
result = classify(text)
# �?{"direction": "非标自动�?, "type": "软件", "level": "L3"}
```

### Step 2: 信息提取
```python
from scripts.collector import extract_metadata
metadata = extract_metadata(text)
# �?{"equipment": ["AM600"], "protocols": ["EtherCAT"], "projects": ["IV2024"]}
```

### Step 3: 模板填充
```python
from scripts.collector import fill_template
markdown = fill_template(classification, metadata, raw_text)
```

### Step 4: 入库
```python
from scripts.collector import save_to_domain_kit
entity_id = save_to_domain_kit(markdown, classification, metadata)
```

### Step 5: 推送审�?```python
from scripts.collector import notify_reviewer
notify_reviewer(research_room, entity_id, title)
```

## 研究室与负责�?
| 研究�?| 负责�?| 方向 |
|--------|--------|------|
| 机电系统研究�?| 待配�?| 非标自动化、机械设计、电气设计、PLC代码 |
| 工业视觉研究�?| 尹德�?| 视觉检测、光学成像、视觉算�?|
| 物流自动化研究室 | 待配�?| 物流方案、WCS系统、调度算�?|

## �?domain-kit 集成

- 存储: `skills/domain-kit/storage/knowledge_store.py` �?`KnowledgeStore`
- ID生成: `skills/domain-kit/utils/id_generator.py` �?`generate_entity_id`
- 实体类型映射:
  - 方案�?�?"BestPractice"（暂用，待扩展）
  - 设计�?�?"BestPractice"（暂用，待扩展）
  - 软件�?�?"CodeTemplate"
  - 算法�?�?"BestPractice"（暂用，待扩展）
  - 经验�?�?"BestPractice"

## 配置

- 关键词词�? `config/keywords.json`
- 负责人配�? `config/reviewers.json`

## 使用示例

```
用户: 记录一条知�?
AI: 请提供知识内容，可以是：
    - 直接粘贴文本
    - 描述一个技术问�?解决方案
    - 指定文件夹路径批量导�?
用户: 我们在IV2024项目上用AM600通过EtherCAT控制IS620N伺服，踩了一个坑�?      周期设太短导致丢步，最后改�?ms才稳定�?
AI: 已自动分类：
    - 方向: 非标自动�?    - 类型: 经验�?    - 层级: L4（经验层�?    - 提取: 设备[AM600, IS620N], 协议[EtherCAT], 项目[IV2024]

    [预览生成的知识卡片]

    确认入库�?Y/修改)
```
