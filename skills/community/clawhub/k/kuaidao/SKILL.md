---
name: kd
version: 1.1.0
description: "快导(KD) - 短视频脚本批量生成与管理。当用户需要批量生成多平台短视频脚本、管理文案库时使用。"
metadata:
  requires:
    bins: ["python"]
    pypi_packages: ["openpyxl"]
    skills:
      - "web_search"
    optional:
      bins: ["lark-cli"]
      skills:
        - "lark-doc"
        - "lark-wiki"
    env:
      required: []  # 没有必需的环境变量
      optional:
        - name: "LARK_CLI_TOKEN"
          description: "飞书 CLI 认证 token（仅当使用飞书上传功能时需要）"
          sensitive: true
    files:
      - "config/platforms.json"
      - "config/user_config.json"
  cliHelp: |
    # 查看帮助
    python kd.py --help
    
    # 执行完整快导流程
    python kd.py run --platform xiaohongshu
    
    # 执行单步
    python kd.py step --platform xiaohongshu --step 6
    
    # 规则更新
    python kd.py rules --platform xiaohongshu
    
    # 活动管理（v1.1.0新增）
    python kd.py activity --command "添加活动：春节特惠，关键词：春节、过年"
    python kd.py activity --command "列出所有活动"
  configPaths:
    - "~/.agents/skills/kd/config/"
  configPaths.optional:
    - "~/.agents/skills/kd/references/platform_rules/"
---

# 快导 (KD)

快导(KD)是一个跨平台、跨行业的短视频脚本批量生成与管理工具。

## ⚠️ CRITICAL — 首次使用必读

**使用前必须完成以下配置：**

1. **安装依赖：** `pip install openpyxl`
2. **配置搜索关键词：** 编辑 `config/platforms.json`
3. **设置文案库路径：** 编辑 `config/user_config.json`

详见 [README.md](./README.md) 完整文档。

## 核心功能

| 功能 | 说明 |
|:---|:---|
| **快导系列** | 10步流程生成多平台短视频脚本 |
| **规则更新** | 生成/更新平台运营规则文档 |

## Shortcuts（快速使用参考）

| 用户说 | 我执行 | 说明 |
|:---|:---|:---|
| "快导小红书，生成5条" | 执行完整10步流程 | 自动执行搜索→生成→写入→报告全流程 |
| "快导第6步" | 执行单步生成脚本 | 仅执行Step 6，需前置步骤数据 |
| "配置关键词" | 引导配置 platforms.json | 设置平台搜索关键词池 |
| "配置文案库路径" | 引导配置 user_config.json | 设置Excel文案库保存位置 |
| "配置飞书空间" | 引导配置 report_space_id | 设置报告上传的飞书知识库 |
| "检查文案库格式" | 执行Step 5格式扫描 | 读取Excel实际格式参数 |
| "查看平台规则" | 读取 rules 文档 | 查看已生成的平台运营规则 |
| "更新小红书规则" | 执行规则更新系列 | 搜索最新规则并更新文档 |
| "测试快导" | 运行 test_workflow.py | 快速测试核心功能是否正常 |

## 执行模式

### 自动模式（默认）
```python
from scripts import WorkflowManager
workflow = WorkflowManager('xiaohongshu')
result = workflow.run_full()
```

### 交互模式（每步完成后暂停）
```python
from scripts import WorkflowManager

# 启用交互模式
workflow = WorkflowManager('xiaohongshu', interactive=True)

# 执行，每步完成后返回等待
result = workflow.run_full()
if result.get('paused'):
    print(result['message'])  # "Step X 完成，是否继续？"

# 用户确认后继续
result = workflow.resume()
```

### 回调模式（即时回复每步结果）
```python
def on_step_complete(step_num, result, should_pause):
    print(f"Step {step_num} 完成")  # 即时回复用户

workflow = WorkflowManager('xiaohongshu')
workflow.run_full(callback=on_step_complete)
```

## 核心模块

- `ConfigManager` - 配置管理
- `ScriptGenerator` - 脚本生成
- `ExcelManager` - Excel操作

**详细用法和示例见 [README.md](./README.md)**

## 版本

| 版本 | 日期 | 说明 |
|:---:|:---:|:---|
| 1.1.0 | 2026-04-27 | 新增：智能时长计算、活动管理、详细内容格式、BGM生成、Excel行高100 |
| 1.0.0 | 2026-04-24 | 初始版本，支持3平台 |

---

## v1.1.0 新功能详解

### 1. 智能时长计算

系统会自动计算并调整每个分镜的时间段：
- **台词时长**：字数 × 0.25秒
- **运镜时长**：固定2秒、推拉3秒、摇移4秒、复杂6秒、航拍8秒
- **建议时长**：max(台词, 运镜) + 1秒缓冲
- **自动调整**：使用建议时长更新B列时间段

**配置**（`config/platforms.json`）：
```json
"duration_policy": {
  "xiaohongshu": {
    "auto_adjust": true,  // 开启自动调整
    "calculation_rules": {
      "speech_rate": 0.25,
      "motion_base": { "static": 2, "push_pull": 3, ... },
      "buffer_seconds": 1
    }
  }
}
```

### 2. 活动管理

支持自然语言管理活动：
- 添加活动：`添加活动：春节特惠，关键词：春节、过年`
- 列出活动：`列出所有活动`
- 查询活动：`查询活动：春节`
- 删除活动：`删除活动：春节特惠`

系统会根据脚本主题自动匹配活动，填入L列（关联活动）。

### 3. 详细内容格式

分镜内容现在支持更详细的描述：
- **C列-镜头**：设备/焦段/内容
- **D列-运镜**：方式/轨迹/速度
- **E列-技巧**：光线/ISO/对焦/色调
- **F列-画面**：场景/构图/色彩/氛围

### 4. BGM详细生成

I列BGM现在要求详细格式：
```
音乐名：《稻香》周杰伦
风格：田园治愈、轻快温暖
使用时机：0-30秒前奏，30-60秒主歌，60-90秒副歌
```

### 5. Excel行高统一

数据行统一设置为100，标题行20.4：
```json
"row_height": {
  "title_row": 20.4,
  "data_row": 100
}
```

### 6. 外网搜索自动收集

`user_config.json` 新增 `external_search` 配置：

```json
{
  "external_search": {
    "auto_collect": true,      // 空关键词时自动获取热门
    "collect_count": 20,
    "platforms": ["TikTok", "YouTube"],
    "default_keywords": []       // 备用关键词（可选）
  }
}
```

**三种使用场景：**
1. `external_keywords` 有值 → 使用用户配置的关键词
2. `external_keywords` 为空，`default_keywords` 有值 → 使用默认关键词
3. 两者都为空 + `auto_collect: true` → 调用 web_search 自动获取当前热门

**注意：** 场景3如果搜索失败会直接报错，不使用备用数据。

---

## 联系我们

如有问题或建议，欢迎交流：

- **微信号：** huitouyoujianta
- **用途：** 快导(KD)技能使用咨询、功能建议、技术交流

欢迎加微信交流学习！
