# 系统架构与详细流程

## 7 阶段管线详解

```
[Step 1] 文件预处理
  输入：原始文件（DOCX/PDF/XLSX/图片/MD/TXT）
  处理：mammoth提取文本 + 视觉LLM替换内嵌图片 + 复杂表格截图识别
  输出：纯文本 Markdown（无 base64 图片）

[Step 2] 价值评估（LLM）
  输入：Markdown 前2000字符
  LLM 输出：{ has_value: bool, score: 0~1, reason: str, suggested_category: str }
  阈值: score >= 0.4 (可配置)
  低于阈值 → 跳过文件，不生成数据集

[Step 3] 智能分类（LLM + MongoDB）
  输入：Markdown 前2000字符 + MongoDB 分类树 JSON
  LLM 输出：{ matched: bool, category_path, confidence, suggest_ga, ga_genre, ga_audience, ... }
  - 匹配现有分类 → 直接归入
  - 不匹配 → 自动创建新分类
  - suggest_ga=true → 启用 GA 多视角增强

[Step 4] 参数确认
  合并所有步骤结果，确认分类路径、GA设置、语言等参数

[Step 5] EasyDataset 管线（7 子步骤）
  5.1 创建项目（名称: JYKG_<文件名>_<时间戳>）
  5.2 配置 LLM 模型
  5.3 上传文件
  5.4 文本分割（.md 用 split API domain_tree_action=keep）
  5.5 GA 对生成（如启用）
  5.6 问题生成（最多重试3次）
  5.7 答案生成（最多重试3次）

[Step 6] 数据集确认与导出
  - 批量确认所有数据集
  - 分批导出 JSON
  - 问题去重（重复问题删整条）
  - COT 字段移除

[Step 7] 数据存储
  - 本地：<datasets_dir>/<分类路径>/<文件名>_alpaca.json
  - MongoDB：ds_<分类slug> 集合（逐条 Q&A 入库）
```

## 知识检索流程

```
用户提问
  ↓
python main.py -q "提取的关键词"
  ↓
关键词拆分（2字中文词组）→ 匹配分类 → ds_*集合 $regex 搜索
  ↓
只保留 answer 字段 → "---" 拼接 → 45000字截断（句号处切割）
  ↓
作为知识凭证融入回答
```

## 文件结构

```
<skill_root>/                    # 用户指定或默认为 D:/knowledge_skill/
├── config.json                  # 系统配置（LLM/EasyDataset/MongoDB连接信息）
├── JY_Knowlgdge_Skill/          # 代码主目录
│   ├── SKILL.md                 # 技能主入口（Model第一阅读对象）
│   ├── main.py                  # 主控脚本
│   ├── easy_dataset_client.py   # EasyDataset API 客户端
│   ├── file_preprocessor.py     # 文件预处理引擎
│   ├── mongo_manager.py         # MongoDB 管理器
│   ├── classifier.py            # LLM 分类器
│   ├── config_manager.py        # 配置管理
│   ├── clean_cot.py             # COT 清洗脚本
│   ├── run.bat                  # Windows 一键运行
│   ├── requirements.txt         # Python 依赖
│   ├── tools/                   # 工具脚本
│   │   ├── check_env.py         # 环境检测
│   │   └── diagnose.py          # 问题诊断
│   └── docs/                    # 详细文档
│       ├── cold_start.md        # 冷启动指南
│       ├── easydataset_deploy.md
│       ├── easydataset_api.md
│       ├── troubleshooting.md
│       └── skill_architecture.md
├── datasets/                    # 数据集输出
├── processed/                   # 预处理缓存
├── uploads/                     # 文件上传临时目录
└── mongo-data/                  # MongoDB 数据卷
```

## 依赖服务拓扑

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│ LLM API     │    │ 视觉 LLM API │    │ MongoDB      │
│ :1234/v1    │    │ :1234/v1     │    │ :27017       │
│ 分类+评估   │    │ 图片分析     │    │ 分类+数据集  │
└──────┬──────┘    └──────┬───────┘    └──────┬───────┘
       │                  │                   │
       └──────────────────┼───────────────────┘
                          │
              ┌───────────▼───────────┐
              │   JY_Knowledge_Skill  │
              └───────────┬───────────┘
                          │
              ┌───────────▼───────────┐
              │   EasyDataset :1717   │
              │   Docker Container    │
              │   文本/图片数据集生成  │
              └───────────────────────┘
```

## EasyDataset 任务类型

| taskType | 说明 | 执行方式 |
|----------|------|----------|
| `file-processing` | 文件处理（分割+领域树） | 异步，通过 poll_task 轮询 |
| `question-generation` | 批量生成问题 | 异步，支持 GA 扩展 |
| `answer-generation` | 批量生成答案 | 异步 |
| `image-question-generation` | 图片问题生成 | 异步 |
| `image-dataset-generation` | 图片数据集生成 | 异步 |
| `data-cleaning` | 数据清洗 | 异步 |

任务状态：0=处理中, 1=已完成, 2=失败, 3=已中断

## 配置文件结构

```json
{
  "llm": {
    "base_url": "LLM API 地址",
    "api_key": "API Key",
    "model": "模型名称",
    "vision_model": "视觉模型名称",
    "vision_concurrency_limit": 10
  },
  "easy_dataset": { "base_url": "http://localhost:1717" },
  "mongo": { "uri": "mongodb://localhost:27017", "database": "knowledge_skill" },
  "output": {
    "processed_dir": "预处理目录",
    "datasets_dir": "数据集输出目录",
    "uploads_dir": "上传目录"
  },
  "dataset_generation": {
    "task_timeout_minutes": 720,
    "include_ga_pairs": true
  },
  "file_filter": { "value_threshold": 0.4 }
}
```
