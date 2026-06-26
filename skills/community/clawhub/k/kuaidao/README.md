# 快导 (KD) - 短视频脚本批量生成

**版本：** 1.1.0（2026年4月更新）

快导(KD)是一个跨平台、跨行业的短视频脚本批量生成与管理工具，支持单次任务执行。

---

## ⚠️ 安装前必读（安全检查清单）

在安装和运行快导之前，请确认以下事项：

### 1. 依赖检查
- [ ] Python 3.7+ 已安装
- [ ] `openpyxl` 已安装 (`pip install openpyxl`)
- [ ] `web_search` skill 可用（用于搜索平台爆款）
- [ ] 可选：`lark-cli`（仅当需要飞书上传功能时）

### 2. 路径配置安全
- [ ] `copy_library_path` 指向你**控制的目录**
- [ ] `rules_path` 指向你**控制的目录**  
- [ ] 避免使用系统关键目录（如 C:\Windows, /usr/bin 等）

### 3. 飞书上传（可选）
- [ ] 了解 `feishu_permissions.json` 中的 36 个权限 scope
- [ ] 仅提供 `LARK_CLI_TOKEN` 如果你**确实需要**上传报告
- [ ] token 将存储在 `lark-cli` 配置中，**不在快导内**

### 4. 示例脚本安全
- [ ] `entry_template.py` 包含**占位符路径**（YOUR_USERNAME）
- [ ] **运行前必须修改**路径配置
- [ ] 首次运行时会提示确认路径

### 5. 网络行为知情
- [ ] `web_search` 会发送搜索查询到外部服务
- [ ] `external_search.auto_collect` 启用时会自动搜索热门
- [ ] 不会自动上传任何数据到第三方服务

**确认以上事项后，再继续安装。**

---

## 项目结构

```
kd/
├── kd.py                          # 主入口文件
├── test_workflow.py               # 工作流测试脚本
├── entry_template.py              # 入口模板示例
├── config/                        # 配置文件目录
│   ├── platforms.json             # 平台参数配置（时长、关键词等）
│   ├── workflow.json              # 工作流配置（10步流程定义）
│   ├── templates.json             # 模板配置（提示词模板）
│   ├── user_config.json           # 用户配置（文案库路径、飞书空间ID等）
│   └── feishu_permissions.json    # 飞书权限配置
├── scripts/                       # 核心模块
│   ├── __init__.py                # 模块初始化，导出核心类
│   ├── config_manager.py          # 配置管理（ConfigManager）
│   ├── excel_manager.py           # Excel操作（ExcelManager）
│   ├── script_generator.py        # 脚本生成（ScriptGenerator）
│   ├── workflow_manager.py        # 工作流管理（WorkflowManager）
│   ├── format_checker.py          # 格式检查（FormatChecker）
│   └── feishu_permission_helper.py # 飞书权限开通助手
├── prompts/                       # 提示词模板
│   ├── step6_generate_scripts.md  # 子任务6：生成脚本提示词
│   └── step7_validate_scripts.md  # 子任务7：合理性检查提示词
├── references/                    # 参考文档
│   ├── platform_rules/            # 平台规则文档（自动生成）
│   │   ├── xiaohongshu_rules.md
│   │   ├── douyin_rules.md
│   │   └── shipinhao_rules.md
│   └── README.md                  # 参考资料说明
├── tests/                         # 测试脚本
│   ├── config_manager_win.py      # Windows配置管理测试
│   ├── excel_manager_win.py       # Windows Excel操作测试
│   ├── format_checker_win.py      # Windows格式检查测试
│   ├── script_generator_win.py    # Windows脚本生成测试
│   ├── __init__.py
│   ├── mac/                       # macOS测试脚本
│   │   ├── config_manager_mac.py
│   │   ├── excel_manager_mac.py
│   │   ├── format_checker_mac.py
│   │   └── script_generator_mac.py
│   └── linux/                     # Linux测试脚本
│       ├── config_manager_linux.py
│       ├── excel_manager_linux.py
│       ├── format_checker_linux.py
│       └── script_generator_linux.py
├── requirements.txt               # Python依赖
├── setup.py                       # 安装配置
├── .gitignore                     # Git忽略配置
├── SKILL.md                       # OpenClaw Skill文档
└── README.md                      # 本文件（用户使用手册）
```

---

## 核心类说明

| 类名 | 文件 | 用途 |
|:---|:---|:---|
| `ConfigManager` | `config_manager.py` | 管理所有配置文件（platforms.json、user_config.json等） |
| `ExcelManager` | `excel_manager.py` | 读写Excel文案库，格式扫描与保持 |
| `ScriptGenerator` | `script_generator.py` | 生成短视频脚本内容 |
| `WorkflowManager` | `workflow_manager.py` | 协调执行10步快导流程 |
| `FormatChecker` | `format_checker.py` | 检查Excel格式、内容合理性 |

---

---

## ⚠️ CRITICAL — 首次使用必读

**用户：**"我要用快导生成小红书脚本"

**我：**好的，使用快导之前，需要先完成几项配置。我来引导你：

---

### 第0步：开通飞书机器人权限（如使用飞书功能）

**用户：**"我需要保存报告到飞书吗？"

**我：**"如果你希望自动上传执行报告到飞书知识库，需要先开通机器人权限。如果只用本地保存，可以跳过这步。"

**开通权限（可选）：**

```bash
# 运行权限开通助手
python scripts/feishu_permission_helper.py
```

或手动开通：
1. 进入飞书开发者后台：https://open.feishu.cn/app
2. 选择你的应用 → 权限管理 → 开通权限
3. 点击"批量导入/导出权限"
4. 粘贴 `config/feishu_permissions.json` 中的内容
5. 申请开通并发布应用

**需要的权限包括：**
- 云文档读写（保存报告）
- 知识库访问（上传到 wiki）
- 消息发送（通知功能）

---

### 第1步：安装依赖

**用户：**"我已经装好了 Python，接下来呢？"

**我：**安装 openpyxl，用于操作 Excel 文案库：

```bash
pip install openpyxl
```

---

### 第2步：配置搜索关键词和主题方向

**用户：**"我是做农家乐的，怎么配置？"

**我：**请告诉我你的搜索关键词和创作主题方向：

- **搜索关键词：** 用于搜索平台爆款视频（例如：农家乐、采摘、成都周边、周末去哪）
- **主题方向：** 你希望创作的内容方向（可选，为空则不限制主题。例如：采摘攻略、亲子游玩、美食探店）

我会帮你配置到 `config/platforms.json` 中。

**示例：**
```json
{
  "platforms": {
    "xiaohongshu": {
      "keywords": ["农家乐", "采摘", "成都周边"],
      "theme_direction": ["采摘攻略", "亲子游玩"]
    }
  }
}
```

**注意：** `theme_direction`（主题方向）可为空，不填则不限制创作主题。

---

### 第3步：设置文案库保存位置

**用户：**"生成的脚本保存在哪里？"

**我：**请告诉我你希望保存到哪个文件夹，例如：

> "保存到 F:\\vlog\\JT\\idea\\ 目录，文件名叫小红书文案库.xlsx"

我会帮你配置到 `config/user_config.json` 中。

**配置项说明：**
| 配置项 | 你要告诉我的内容 | 用途 |
|:---|:---|:---|
| 文案库路径 | "F:\\vlog\\JT\\idea\\小红书文案库.xlsx" | 保存生成的脚本 |
| 飞书空间ID | 你的飞书知识库空间ID（可选）| 自动上传报告到飞书 |
| 规则文档路径 | 留空即可（可选）| 保存平台规则文档 |

---

### 第4步：生成平台规则（可选）

**用户：**"什么是平台规则？需要吗？"

**我：**平台规则包含小红书的运营规范，例如：
- 视频时长要求（2-3分钟）
- 标题字数限制（20字以内）
- 违规内容红线

**你可以选择：**
- ✅ **帮我生成默认规则** — 我基于平台通用规则创建
- ❌ **先跳过** — 后续在生成的脚本中手动调整

如果选择生成，告诉我："帮我生成小红书规则文档"

---

### 完成！现在可以开始使用了

**用户：**"配置好了，开始生成脚本吧"

**我：**好的，执行快导系列任务，告诉我：
1. 目标平台（小红书/抖音/视频号）
2. 生成几条脚本（默认5条）

我们开始吧！

---

## ⚠️ 安全与隐私说明

### 数据存储
- **所有生成的脚本**保存在本地配置的 Excel 文件路径
- **执行报告**默认保存到本地 `reports/` 目录
- **不会自动上传到任何云服务**

### 飞书上传（可选）
- 如需上传报告到飞书知识库，**需手动配置**
- 步骤：
  1. 安装并配置 `lark-cli`（见下方"飞书权限开通"章节）
  2. 手动运行上传命令
- **默认不上传**，仅在用户明确要求时才执行

### 网络访问
- **web_search**：搜索平台爆款时使用（必需）
- **无其他外部网络调用**
- 所有脚本执行在本地完成

### 敏感信息
- 如需配置飞书认证，token 保存在 `lark-cli` 的配置中
- 快导 skill **不存储任何凭证**

---

## 使用说明（重要）

**当前版本状态：**
- ✅ **Python API**：完整可用，推荐通过 Python 代码调用
- 🚧 **CLI 命令行**：框架已搭建，具体功能开发中

**建议使用方式：** 直接导入 Python 模块使用（见下方"Python API 使用"章节）

---

## 快导十步流程说明

### 简略版（默认）

**用户：**"快导的十步分别是什么？"

**我：**快导系列包含10个步骤：

| 步骤 | 名称 | 一句话说明 |
|:---:|:---|:---|
| 1 | 搜索平台爆款 | 搜你行业的爆款视频参考 |
| 2 | 读取平台规则 | 读取平台运营规范 |
| 3 | 搜外网爆款 | 搜TikTok/YouTube灵感 |
| 4 | 查重复 | 避开已有脚本主题 |
| 5 | 查格式 | 扫描Excel实际格式 |
| 6 | 写脚本 | 生成差异化脚本 |
| 7 | 检查 | 检查脚本合理性 |
| 8 | 保存 | 写入Excel文案库 |
| 9 | 验证 | 验证写入结果 |
| 10 | 出报告 | 生成执行报告 |

完整执行就是走这10步，也可以单独执行某一步。

---

### 详细版

**用户：**"详细说说每一步做什么？"

**我：**

**第1步：搜索平台爆款**
- 用你配置的关键词搜小红书/抖音/视频号
- 随机抽3个关键词，各搜20条
- 最终选定4个最优爆款

**第2步：读取平台规则**
- 读取平台运营规范（时长、标题、违规红线等）
- 输出7项关键规则摘要

**第3步：搜外网爆款**
- 搜TikTok/YouTube找灵感
- **三种模式：**
  1. 使用 `external_keywords` 配置的关键词搜索
  2. 使用 `default_keywords` 预设默认关键词搜索  
  3. `auto_collect=true` 时自动获取当前热门视频（无需关键词）
- 最终选定1个外网爆款

**配置方式：** 在 `user_config.json` 中配置 `external_search`

**第4步：查重复**
- 读取你文案库已有脚本
- 确定需避开的主题方向

**第5步：查格式**
- 扫描Excel实际格式（字体、颜色、边框等）
- 记录格式参数，确保写入时格式一致

**第6步：写脚本**
- 基于第1、3步的爆款，生成差异化脚本
- 每个脚本包含完整的分镜、台词、BGM等14列

**第7步：检查**
- 检查时长、内容、场景、台词、格式等合理性
- 发现问题直接修改

**第8步：保存**
- 将脚本写入Excel文案库
- 严格按第5步记录的格式写入

**第9步：验证**
- 用Python读取Excel验证
- 检查格式、内容、位置正确性

**第10步：出报告**
- 生成Markdown执行报告
- 保存到飞书知识库（如配置了空间ID）

---

## 安装

### 方式1：通过 clawhub 安装（推荐）

```bash
# 安装 skill
clawhub install kd

# 进入 skill 目录
cd ~/.agents/skills/kd

# 安装依赖
pip install -r requirements.txt
```

### 方式2：手动下载

```bash
# 下载到本地
cd ~/.agents/skills/
git clone <repository-url> kd

# 安装依赖
cd kd
pip install -r requirements.txt
```

---

## Python API 使用（推荐）

### 快导系列 - 生成脚本

```python
from kd.scripts import ScriptGenerator, ExcelManager, ConfigManager

# 1. 加载配置
config = ConfigManager()
config.load_platform('xiaohongshu')  # 或 'douyin', 'shipinhao'

# 2. 生成脚本
generator = ScriptGenerator(platform='xiaohongshu')
scripts = generator.generate(
    trending_titles=['爆款标题1', '爆款标题2'],  # 子任务1结果
    rules_summary={...},  # 子任务2结果
    avoid_themes=['已有主题1'],  # 子任务4结果
    count=5
)

# 3. 写入文案库
with ExcelManager('path/to/文案库.xlsx') as em:
    format_info = em.scan_format()  # 子任务5
    for script in scripts:
        em.append_script(script)  # 子任务8
```

### 规则更新系列

```python
from kd.scripts import ConfigManager

# 读取平台规则（需用户自行创建规则文档）
config = ConfigManager()
rules = config.load_rules('xiaohongshu')
```

---

## Shortcuts（快速使用参考）

| 用户说 | 我执行 | 对应模块 |
|:---|:---|:---|
| "帮我配置小红书关键词" | 引导配置 platforms.json | config_manager |
| "设置文案库路径" | 引导配置 user_config.json | config_manager |
| "生成小红书规则" | 创建 xiaohongshu_rules.md | rules_update |
| "快导小红书，生成5条" | 执行完整10步流程 | 快导系列 |
| "快导第6步，生成脚本" | 执行单步子任务6 | step6_generate |
| "检查文案库格式" | 执行 step5 格式检查 | excel_manager |
| "验证写入结果" | 执行 step9 验证 | excel_manager |

### 额外问答

**用户：**"快导的十步分别是什么？"

**我：**（提供简略版或详细版，见上方"快导十步流程说明"章节）

---

## 执行模式

### 自动模式（默认）

**说明：** 连续执行所有步骤，完成后一次性返回结果。

```python
from kd.scripts import WorkflowManager

# 创建实例
workflow = WorkflowManager('xiaohongshu')

# 执行完整流程
result = workflow.run_full()

if result['success']:
    print(f"✅ 完成！生成 {len(result['completed_steps'])} 步")
else:
    print(f"❌ 失败：{result.get('error', '未知错误')}")
```

---

### 交互模式

**说明：** 每完成一步后暂停，等待用户确认后再继续。

```python
from kd.scripts import WorkflowManager

# 启用交互模式
workflow = WorkflowManager('xiaohongshu', interactive=True)

# 执行
result = workflow.run_full()

# 如果暂停了，提示用户
if result.get('paused'):
    print(result['message'])
    # 输出示例: "Step 1 完成，是否继续执行 Step 2？"
    
    # 用户回复后继续
    workflow.resume()
```

**用户交互示例：**

| Agent 回复 | 用户回复 | 说明 |
|:---|:---|:---|
| "Step 1 完成，选定4个爆款。继续？" | "继续" / "跳过" / "停止" | 选择继续执行、跳过下一步、或停止 |
| "Step 6 完成，生成5条脚本。继续？" | "继续" | 进入检查和保存阶段 |

---

### 回调模式（即时回复）

**说明：** 每完成一步立即回调，适合需要即时向用户展示进度的场景。

```python
from kd.scripts import WorkflowManager

def on_step_complete(step_num, result, should_pause):
    """每步完成后的回调"""
    print(f"✅ Step {step_num} 完成")
    
    # 如果是关键步骤，展示更多信息
    if step_num == 1:
        trending = result.get('final_selection', [])
        print(f"   选定爆款: {len(trending)} 个")
    elif step_num == 6:
        scripts = result.get('scripts', [])
        print(f"   生成脚本: {len(scripts)} 条")
    
    # 如果需要暂停，提示用户
    if should_pause:
        print("   输入 '继续' 执行下一步")

# 执行，使用回调
workflow = WorkflowManager('xiaohongshu')
result = workflow.run_full(callback=on_step_complete)
```

---

## 详细命令示例

### 示例1：完整快导流程

**用户：**"快导小红书，生成5条脚本"

**我：**执行完整10步流程：

```python
from kd.scripts import ConfigManager, ScriptGenerator, ExcelManager

# Step 1-5: 准备阶段
config = ConfigManager()
platform_config = config.load_platform('xiaohongshu')

# Step 6: 生成脚本
generator = ScriptGenerator(platform='xiaohongshu')
scripts = generator.generate(
    trending_titles=['爆款标题1', '爆款标题2', '爆款标题3', '爆款标题4'],
    external_title='外网爆款标题',
    rules_summary={...},
    avoid_themes=['已有主题'],
    count=5
)

# Step 7: 合理性检查（自动生成时已完成）

# Step 8-9: 写入并验证
with ExcelManager('path/to/文案库.xlsx') as em:
    for script in scripts:
        em.append_script(script)
    em.validate_write()

# Step 10: 生成报告
print(f"✅ 成功生成 {len(scripts)} 条脚本")
```

---

### 示例2：单步执行

**用户：**"快导第6步，生成脚本"

**我：**仅执行脚本生成：

```python
from kd.scripts import ScriptGenerator

generator = ScriptGenerator(platform='xiaohongshu')
scripts = generator.generate(
    trending_titles=[...],  # 用户需提供
    count=5
)
```

---

### 示例3：检查文案库格式

**用户：**"检查文案库格式"

**我：**扫描Excel格式：

```python
from kd.scripts import ExcelManager

with ExcelManager('path/to/文案库.xlsx') as em:
    format_info = em.scan_format()
    print(format_info)
```

---

### 示例4：配置搜索关键词

**用户：**"帮我配置小红书关键词"

**我：**更新 platforms.json：

```python
from kd.scripts import ConfigManager

config = ConfigManager()
config.set_platform_keywords(
    platform='xiaohongshu',
    keywords=['农家乐', '采摘', '成都周边'],
    theme_direction=['采摘攻略', '亲子游玩']  # 可选
)
```

---

## 常见错误处理

### 配置类错误

**错误1：关键词未配置**
- **用户：**"快导小红书"
- **报错：**`"keywords is empty"`
- **我：**"先告诉我你的搜索关键词，例如：农家乐、采摘、成都周边..."

**错误2：文案库路径未设置**
- **用户：**"开始生成"
- **报错：**`"copy_library_path not set"`
- **我：**"请告诉我文案库保存到哪里，例如：F:\\vlog\\JT\\idea\\小红书文案库.xlsx"

---

### Step 1 错误：搜索平台爆款

**错误1：没有搜索 skill**
- **报错：**`"web_search skill not available"`
- **我：**"当前没有配置搜索功能，请手动提供4个爆款标题，或者安装 web_search skill"

**错误2：搜索返回空结果**
- **报错：**`"no trending videos found"`
- **我：**"用你配置的关键词没搜到爆款，要不要换几个关键词试试？"

---

### Step 2 错误：读取平台规则

**错误1：规则文档不存在**
- **报错：**`"rules file not found: xiaohongshu_rules.md"`
- **我：**"规则文档不存在，要我帮你生成默认规则吗？"

---

### Step 3 错误：搜索外网爆款

**错误1：没有外网搜索 skill**
- **报错：**`"external search not available"`
- **我：**"当前无法搜索外网爆款（需要相应skill），可以继续用平台爆款生成，或者你提供一个外网参考链接？"

**错误2：网络问题**
- **报错：**`"network error: cannot access TikTok/YouTube"`
- **我：**"网络访问受限，搜不到外网爆款。这一步可以跳过，继续用平台爆款生成脚本？"

**错误3：外网关键词未配置**
- **报错：**`"external_keywords is empty"`
- **我：**"没有配置外网搜索关键词，告诉我几个英文关键词，例如：food, farm, family？或者直接跳过这步？"

---

### Step 4 错误：同质化检查

**错误1：文案库文件不存在**
- **报错：**`"copy library file not found"`
- **我：**"文案库文件还没创建，第一次使用吧？直接生成新脚本，不用查重复了"

---

### Step 5 错误：格式检查

**错误1：Excel 格式异常**
- **报错：**`"cannot read Excel format: file corrupted"`
- **我：**"Excel文件读取失败，可能是格式问题。要不要我创建一个新的标准格式文案库？"

---

### Step 6 错误：生成脚本

**错误1：生成超时**
- **报错：**`"script generation timeout"`
- **我：**"生成脚本超时了，可能是网络问题。要不要减少生成数量再试？"

**错误2：内容不合规**
- **报错：**`"generated content violates platform rules"`
- **我：**"生成的内容可能不符合平台规范，需要我调整后再生成吗？"

---

### Step 7 错误：合理性检查

**错误1：时长不达标**
- **报错：**`"total duration mismatch: expected 120-180s, got 90s"`
- **我：**"总时长不够，需要增加分镜或延长单镜时长，要我自动调整吗？"

**错误2：内容同质化**
- **报错：**`"scripts are not differentiated enough"`
- **我：**"脚本差异化不够，重新生成一批？"

---

### Step 8 错误：更新文案库

**错误1：写入失败**
- **报错：**`"failed to write to Excel: permission denied"`
- **我：**"Excel文件被占用了（可能你正在打开），关闭Excel后再试？"

**错误2：格式不匹配**
- **报错：**`"format mismatch with step5 scan result"`
- **我：**"写入格式和扫描的格式不一致，需要我重新扫描再写入？"

---

### Step 9 错误：全面检查对比

**错误1：内容丢失**
- **报错：**`"content validation failed: missing columns"`
- **我：**"验证发现内容有缺失，回退到Step 8重新写入？"

**错误2：位置错误**
- **报错：**`"position mismatch: expected row 15, found row 14"`
- **我：**"写入位置不对，检查后发现偏移了一行，需要修正？"

---

### Step 10 错误：提交报告

**错误1：飞书空间未配置**
- **报错：**`"report_space_id not set"`
- **我：**"没有配置飞书空间ID，报告保存到本地目录可以吗？"

**错误2：保存失败**
- **报错：**`"failed to upload to lark wiki"`
- **我：**"飞书上传失败了，报告已保存到本地，需要手动上传吗？"

---

## v1.1.0 新功能说明（2026年4月更新）

### 1. 智能时长计算（auto_adjust）

**功能：** 根据台词字数自动计算并调整分镜时长

**配置：**
```json
// config/platforms.json
{
  "duration_policy": {
    "xiaohongshu": {
      "target_duration": {"min": 120, "max": 180},
      "segment_duration": {"min": 6, "max": 15},
      "auto_adjust": true,  // 开启自动调整
      "calculation_rules": {
        "speech_rate": 0.25,  // 0.25秒/字
        "motion_base": {...},  // 运镜基础时长
        "buffer_seconds": 1     // 缓冲时间
      }
    }
  }
}
```

**说明：**
- `auto_adjust: true` → 系统自动计算（默认）
- `auto_adjust: false` → 完全手动控制时间段
- 台词时长 = 字数 × speech_rate（0.25秒/字）
- 总时长必须 ≥ 台词时长的60%

---

### 2. 活动配置管理（Activity Manager）

**功能：** 自动匹配脚本关联活动

**配置方式1：自然语言**
```
用户："添加活动：春节特惠，关键词：春节、过年、团圆"
Agent：✓ 活动"春节特惠"已添加，包含3个关键词

用户："列出所有活动"
Agent：当前有2个活动：春节特惠、五一采摘节

用户："删除活动：春节特惠"
Agent：✓ 已删除
```

**配置方式2：直接编辑JSON**
```json
// config/platforms.json
{
  "activities": {
    "list": [
      {
        "id": "spring_festival",
        "name": "春节特惠",
        "keywords": ["春节", "过年", "团圆", "年夜饭"],
        "applicable_platforms": ["xiaohongshu", "douyin"]
      },
      {
        "id": "labor_day",
        "name": "五一采摘节",
        "keywords": ["五一", "采摘", "出游"],
        "applicable_platforms": ["xiaohongshu", "douyin", "shipinhao"]
      }
    ],
    "default": "日常推广"
  }
}
```

**自动匹配规则：**
1. 关键词匹配 → 脚本内容包含活动关键词
2. 时间匹配 → 当前日期在活动有效期内
3. 平台匹配 → 活动适用于当前平台

**无匹配时：** 自动填写"日常推广"

---

### 3. BGM详细生成

**功能：** 生成具体的音乐名称、风格和使用时机

**配置：**
```json
// config/platforms.json
{
  "bgm_library": {
    "categories": {
      "food_display": {
        "name": "美食展示",
        "tracks": [
          {"name": "《小美满》周深", "style": "治愈轻快", "suitable": "全程"}
        ]
      },
      "emotional_narrative": {
        "name": "情感叙事",
        "tracks": [...]
      }
    }
  }
}
```

**输出格式：**
```
I列（推荐音乐/BGM）：
音乐名：《小美满》周深
风格：治愈轻快
使用时机：全程
```

---

### 4. Excel行高统一100

**功能：** 数据行统一设置为100，标题行20.4

**配置：**
```json
// config/platforms.json
{
  "global_settings": {
    "row_height": {
      "title_row": 20.4,
      "data_row": 100
    }
  }
}
```

---

### 5. 外网搜索自动收集（auto_collect）

**功能：** `external_keywords` 为空时，自动获取热门视频

**配置：**
```json
// config/user_config.json
{
  "external_search": {
    "auto_collect": true,      // 开启自动收集
    "collect_count": 20,
    "platforms": ["TikTok", "YouTube"],
    "default_keywords": []       // 为空时自动获取
  }
}
```

**三种使用场景：**
1. **手动配置** → `external_keywords: ["food", "cooking"]` → 使用这些关键词
2. **默认预设** → `default_keywords: ["viral food"]` → 使用预设关键词
3. **完全自动** → 两者都为空 + `auto_collect: true` → 自动获取热门

---

## 参考文档

### references/ 目录说明

`references/` 目录存放快导运行过程中生成的参考文档：

| 子目录 | 用途 | 生成方式 |
|:---|:---|:---|
| `platform_rules/` | 平台运营规则文档 | 规则更新系列生成 |
| `trending/` | 平台爆款缓存 | 快导系列自动保存 |
| `external/` | 外网爆款参考 | 快导系列自动保存 |

**用户：**"references 目录是干什么的？"

**我：**"这是存放规则文档和数据缓存的地方。platform_rules/ 存平台规则，trending/ 存搜到的爆款，external/ 存外网参考。具体说明可以看 references/README.md"

---

### 规则文档位置

**用户：**"平台规则存在哪里？"

**我：**"默认保存在 `references/platform_rules/` 目录，包含：
- `xiaohongshu_rules.md` - 小红书规则
- `douyin_rules.md` - 抖音规则  
- `shipinhao_rules.md` - 视频号规则

可以修改保存路径：
```python
config.set_rules_path("你的自定义路径")
```"

---

## CLI 命令行（开发中）

CLI 功能当前仅作为框架存在，具体功能正在开发中。

```bash
# 查看帮助（可用）
kd --help

# 以下命令框架存在，功能开发中：
kd run --platform xiaohongshu      # 执行完整快导系列
kd step --platform xiaohongshu --step 6  # 执行单步
kd rules --platform xiaohongshu    # 规则更新
kd config show                     # 配置管理
```

**当前推荐使用 Python API 直接调用。**

---

| 软件 | 用途 | 安装命令 |
|:---|:---|:---|
| **Python 3.7+** | 运行脚本 | [官网下载](https://www.python.org/downloads/) |
| **lark-cli** | 飞书API操作 | `npm install -g @larksuite/cli` |

### Python依赖包

| 包名 | 用途 | 安装命令 |
|:---|:---|:---|
| **openpyxl** | Excel文件操作 | `pip install openpyxl` |

### 自动安装

如检测到未安装依赖，系统将提示并协助安装：

```bash
# 检查并安装Python依赖
kd setup --check-deps

# 自动安装（需用户确认）
kd setup --install-deps
```

**注意：** 首次使用前请确保已安装Python和lark-cli。

## 系统支持

| 系统 | 支持状态 | 测试脚本位置 |
|:---|:---:|:---|
| **Windows** | ✅ 默认支持 | `tests/` |
| **macOS** | ✅ 支持 | `tests/mac/` |
| **Linux** | ✅ 支持 | `tests/linux/` |

**注意：** Windows版本默认已配置UTF-8编码支持。macOS和Linux用户使用对应目录下的测试脚本。

## 软件依赖

### 必需软件

| 软件 | 用途 | 安装命令 |
|:---|:---|:---|
| **Python 3.7+** | 运行脚本 | [官网下载](https://www.python.org/downloads/) |
| **lark-cli** | 飞书API操作 | `npm install -g @larksuite/cli` |

### Python依赖包

| 包名 | 用途 | 安装命令 |
|:---|:---|:---|
| **openpyxl** | Excel文件操作 | `pip install openpyxl` |

### 自动安装

如检测到未安装依赖，系统将提示并协助安装：

```bash
# 检查并安装Python依赖
kd setup --check-deps

# 自动安装（需用户确认）
kd setup --install-deps
```

**注意：** 首次使用前请确保已安装Python和lark-cli。

## 功能模块

| 模块 | 说明 | 触发命令 |
|:---|:---|:---|
| **快导系列** | 生成多平台短视频脚本（10步流程） | `kd run --platform <平台>` |
| **规则更新系列** | 更新平台运营规则文档 | `kd rules --platform <平台>` |

## 支持平台

| 平台 | 标识 | 总时长 | 分镜数 |
|:---|:---|:---:|:---:|
| 小红书 | `xiaohongshu` | 2-3分钟 | 自动计算 |
| 抖音 | `douyin` | 1分钟内 | 自动计算 |
| 视频号 | `shipinhao` | 1-3分钟 | 自动计算 |

**平台基础信息**（可修改：`config/platforms.json`）
- 小红书：女性、种草决策、攻略型
- 抖音：年轻人、公域流量、快节奏
- 视频号：中老年、私域社交、温情叙事

## 用户配置变量说明

### 配置变量总览

| 变量名 | 用途 | 是否必需 | 为空时的处理 |
|:---|:---|:---:|:---|
| `copy_library_path` | 文案库Excel路径 | ✅ 必需 | 提示用户配置 |
| `report_space_id` | 飞书知识库空间ID | ✅ 必需 | 提示用户配置 |
| `rules_path` | 规则文档保存路径 | ⚠️ 建议配置 | 使用默认值 `references/platform_rules/` |
| `platform_keywords` | 平台搜索关键词池 | ⚠️ 建议配置 | 子任务1终止，提示配置 |
| `external_keywords` | 外网搜索关键词池 | ❌ 可选 | 子任务3跳过（不影响主流程） |
| `theme_direction` | 内容主题方向 | ❌ 可选 | 脚本生成时不限制主题 |

### 变量详细说明

#### 1. copy_library_path（文案库路径）

**用途：** 指定文案库Excel文件的保存位置

**配置方式：**
```bash
# 方式1：命令行
kd config set copy_library_path "F:\\vlog\\JT\\idea\\xiaohongshu_scripts.xlsx"

# 方式2：编辑配置文件
# 编辑 config/user_config.json
{
  "copy_library_path": "F:\\vlog\\JT\\idea\\xiaohongshu_scripts.xlsx"
}

# 方式3：Python脚本
from kd import ConfigManager
config = ConfigManager()
config.set_copy_library_path("F:\\vlog\\JT\\idea\\xiaohongshu_scripts.xlsx")
```

**文件不存在时的处理：**
- 如文件不存在，自动按默认格式创建新的Excel文件
- 默认格式包含14列（A-N），带标题行格式
- 提示用户："文案库不存在，已按默认格式创建"

#### 2. report_space_id（飞书空间ID）

**用途：** 指定执行报告保存的飞书知识库空间

**配置方式：**
```bash
kd config set report_space_id "你的空间ID"
```

**获取方式：**
1. 打开飞书知识库
2. 进入目标空间
3. 空间设置 → 复制空间ID

**为空时的处理：**
- 子任务10提示用户配置
- 可选择保存到本地目录：`reports/`

#### 3. rules_path（规则文档路径）

**用途：** 指定平台规则文档的保存位置

**配置方式：**
```bash
kd config set rules_path "F:\\我的规则\\"
```

**为空时的处理：**
- 使用默认值：`references/platform_rules/`

**规则文档不存在时的处理：**
- 子任务2提示用户先生成规则
- 提供生成命令：`kd rules --platform xiaohongshu`

#### 4. platform_keywords（平台关键词池）

**用途：** 子任务1搜索目标平台爆款时使用

**配置方式：**
```bash
# 方式1：命令行
kd config set-keywords --platform xiaohongshu \
  --keywords "美食,探店,农家菜,采摘,生活,乡村,慢生活,周末"

# 方式2：编辑配置文件
# 编辑 config/platforms.json
{
  "platforms": {
    "xiaohongshu": {
      "keywords": ["美食", "探店", "农家菜", "采摘"]
    }
  }
}
```

**为空时的处理：**
- 子任务1输出警告："关键词池为空，无法进行搜索"
- 终止子任务1
- 提示用户配置关键词池

#### 5. external_keywords（外网关键词池）

**用途：** 子任务3搜索外网平台爆款时使用（可选）

**配置方式：**
```bash
kd config set-external-keywords \
  --keywords "food,cooking,life,vlog,story,family,memory"
```

**为空时的处理：**
- 子任务3输出提示："外网关键词池为空，跳过外网搜索"
- 跳过子任务3，直接执行子任务4
- 不影响主流程执行

#### 6. theme_direction（内容主题方向）

**用途：** 指导脚本生成的主题方向（可选）

**配置方式：**
```bash
# 编辑 config/platforms.json
{
  "platforms": {
    "xiaohongshu": {
      "theme_direction": ["采摘攻略", "美食探店", "慢生活体验"]
    }
  }
}
```

**为空时的处理：**
- 脚本生成时不限制主题方向
- 完全基于爆款和外网参考生成

### 首次使用配置流程

```bash
# 步骤1：设置文案库路径（必需）
kd config set copy_library_path "你的文案库路径"

# 步骤2：设置飞书空间ID（必需）
kd config set report_space_id "你的空间ID"

# 步骤3：配置平台关键词池（建议）
kd config set-keywords --platform xiaohongshu \
  --keywords "关键词1,关键词2,关键词3"

# 步骤4：配置外网关键词池（可选）
kd config set-external-keywords \
  --keywords "food,cooking,life"

# 步骤5：验证配置
kd config validate
```

### 配置验证命令

```bash
# 验证所有配置
kd config validate

# 验证特定平台
kd config validate --platform xiaohongshu

# 查看当前配置
kd config show

# 查看特定平台配置
kd config show --platform xiaohongshu
```

## 首次使用配置

### 1. 设置文案库路径

```bash
kd config set copy_library_path "你的文案库目录"
# 示例：kd config set copy_library_path "D:\\我的文案\\"
```

### 2. 设置飞书报告空间

```bash
kd config set report_space_id "你的空间ID"
# 空间ID在飞书知识库设置中获取
```

### 3. 配置搜索关键词（可选）

编辑 `config/platforms.json` 中对应平台的 `keywords` 字段。

### 4. 设置规则文档路径

```bash
kd config set rules_path "你的规则文档目录"
# 示例：kd config set rules_path "D:\\我的规则\\"
# 默认：references/platform_rules/
```

### 5. 配置搜索关键词（可选）

编辑 `config/platforms.json` 中对应平台的 `keywords` 字段。

### 6. 设置行业场景（可选）

编辑 `config/platforms.json` 中 `industry_templates` 添加你的行业。

## 快速开始

### 执行完整任务链（10步）

```bash
# 执行小红书任务
kd run --platform xiaohongshu --duration "2-3min"

# 执行抖音任务
kd run --platform douyin --duration "1min"
```

### 执行单个子任务

```bash
# 仅执行子任务6：生成脚本
kd step --platform xiaohongshu --step 6

# 仅执行子任务7：合理性检查
kd step --platform xiaohongshu --step 7
```

### 批量生成脚本（仅子任务6）

```python
from kd import ScriptGenerator

gen = ScriptGenerator(
    platform="xiaohongshu",
    duration="2-3min",
    keywords=["采摘", "农家菜", "慢生活"]
)
scripts = gen.generate(count=5)
```

## 完整10步流程

| 步骤 | 名称 | 说明 | 输出 |
|:---:|:---|:---|:---|
| 1 | 搜索目标平台爆款 | 随机抽取关键词，搜索爆款 | 选定的爆款列表 |
| 2 | 读取平台规则 | 读取平台运营规则文档 | 关键规则摘要 |
| 3 | 搜索外网平台 | 搜索TikTok/YouTube爆款 | 外网爆款参考 |
| 4 | 同质化检查 | 检查避免与已有脚本重复 | 需避开主题清单 |
| 5 | 格式检查 | 现场读取Excel实际格式 | 格式确认清单 |
| 6 | 生成脚本 | 生成差异化脚本 | 完整脚本 |
| 7 | 合理性检查 | 多维度检查并修改 | 检查清单+修改记录 |
| 8 | 更新文案库 | 脚本写入Excel | 写入确认清单 |
| 9 | 全面检查对比 | Python验证写入结果 | 验证报告 |
| 10 | 提交报告 | 生成并保存执行报告 | Markdown报告 |

**注意：**
- 步骤1的关键词池：用户配置（`config/platforms.json`）
- 步骤2的平台规则：用户通过"规则更新系列"生成
- 步骤4的已有脚本：从用户配置的文案库路径读取

## 灵动参数配置

### 核心参数

| 参数 | 默认值 | 说明 | 配置位置 |
|:---|:---:|:---|:---|
| `total_duration` | "2-3min" | 总时长 | 命令行参数 |
| `segment_duration` | "3-12s" | 单分镜时长范围 | `config/platforms.json` |
| `segments_count` | 自动计算 | 分镜数量 | 根据时长自动计算 |

### 分镜时长分配模式

根据总时长自动分配，遵循"开头快、中间稳、结尾慢"原则：

**示例（小红书，2-3分钟）：**
- 开场：3-5秒（快速吸引）
- 主体：6-10秒（内容展开）
- 结尾：10-12秒（升华收尾）

### 内容详细度参数

| 参数 | 默认值 | 说明 |
|:---|:---:|:---|
| `shot_min_chars` | 20 | C列-镜头最少字数 |
| `movement_min_chars` | 15 | D列-运镜最少字数 |
| `technique_min_chars` | 15 | E列-技巧最少字数 |
| `scene_min_chars` | 20 | F列-画面最少字数 |
| `line_min_chars` | 30 | G列-台词最少字数 |
| `sound_min_chars` | 15 | H列-音效最少字数 |

**修改位置：** `config/platforms.json` → `content_requirements.columns`

## 文案库文件

**路径设置：** 首次使用需配置

```
你的文案库目录/
├── 小红书文案库.xlsx
├── 抖音文案库.xlsx
└── 视频号文案库.xlsx
```

**配置命令：**
```bash
kd config set copy_library_path "路径"
```

## 飞书报告保存

**空间ID设置：** 首次使用需配置

- **配置命令：** `kd config set report_space_id "你的空间ID"`
- **命名格式：** `YYYY-MM-DD-快导-平台名称`
- **示例：** `2026-04-22-快导-小红书`

**空间ID获取：** 飞书知识库 → 空间设置 → 复制空间ID

## 规则更新系列

**用途：** 生成/更新平台运营规则文档

```bash
# 更新小红书规则
kd rules --platform xiaohongshu

# 更新抖音规则
kd rules --platform douyin

# 更新视频号规则
kd rules --platform shipinhao
```

**规则文档位置：** `references/platform_rules/`

**初始状态：** 已提供3个平台的规则模板，用户可根据实际运营经验更新

### 规则文档说明

每个平台的规则文档包含：
- 平台基础信息（用户画像、内容风格）
- 核心规则（完播率、原创要求、违规红线）
- 文案规范（标题要求、字数要求、语言风格）
- 拍摄建议（画面要求、运镜技巧）

**查看规则：**
```bash
# 查看小红书规则
kd refs show --platform xiaohongshu

# 编辑规则（直接编辑文件）
nano references/platform_rules/xiaohongshu_rules.md
```

## 错误处理

- **单步超时：** 5分钟
- **出错处理：** 立即停止，通知用户错误详情
- **数据安全：** 写入前自动备份

## 跨平台使用说明

### 不同系统测试脚本使用

根据您的操作系统选择对应的测试脚本（文件名与scripts目录核心模块对应）：

| 核心模块 | Windows | macOS | Linux |
|:---|:---|:---|:---|
| `config_manager.py` | `config_manager_win.py` | `config_manager_mac.py` | `config_manager_linux.py` |
| `excel_manager.py` | `excel_manager_win.py` | `excel_manager_mac.py` | `excel_manager_linux.py` |
| `format_checker.py` | `format_checker_win.py` | `format_checker_mac.py` | `format_checker_linux.py` |
| `script_generator.py` | `script_generator_win.py` | `script_generator_mac.py` | `script_generator_linux.py` |

#### 使用步骤

**Windows用户（默认）：**
```bash
cd tests
python config_manager_win.py
python excel_manager_win.py
```

**macOS用户：**
```bash
cd tests
# 从mac目录复制到根目录
cp mac/config_manager_mac.py .
python config_manager_mac.py
```

**Linux用户：**
```bash
cd tests
# 从linux目录复制到根目录
cp linux/config_manager_linux.py .
python config_manager_linux.py
```

### 目录结构

```
tests/
├── config_manager_win.py      # Windows版本（默认）
├── excel_manager_win.py
├── format_checker_win.py
├── script_generator_win.py
├── __init__.py
├── mac/                         # macOS版本
│   ├── config_manager_mac.py
│   ├── excel_manager_mac.py
│   ├── format_checker_mac.py
│   └── script_generator_mac.py
└── linux/                       # Linux版本
    ├── config_manager_linux.py
    ├── excel_manager_linux.py
    ├── format_checker_linux.py
    └── script_generator_linux.py
```

**文件名对应规则：**
- Windows版本: `{模块名}_win.py`
- macOS版本: `{模块名}_mac.py`
- Linux版本: `{模块名}_linux.py`

**使用提示：** 根据系统复制对应版本的测试脚本到根目录即可直接使用。

## 版本历史

| 版本 | 日期 | 更新内容 |
|:---:|:---:|:---|
| 1.0.0 | 2026-04-22 | 初始版本，支持3平台，单次任务模式 |

## 配置文件说明

| 文件 | 用途 | 可修改内容 |
|:---|:---|:---|
| `config/platforms.json` | 平台参数 | 时长、字数、关键词、行业模板 |
| `config/workflow.json` | 流程配置 | 步骤定义、超时设置 |
| `config/templates.json` | 生成模板 | 提示词、时长分配模式 |

## 更多帮助

```bash
# 查看帮助
kd --help

# 查看平台配置
kd config show --platform xiaohongshu

# 验证配置
kd config validate
```

---

## 快速故障排查

| 问题 | 可能原因 | 解决方案 |
|:---|:---|:---|
| 导入错误 `ModuleNotFoundError: No module named 'openpyxl'` | 未安装依赖 | `pip install -r requirements.txt` 或 `pip install openpyxl` |
| 导入错误 `ModuleNotFoundError: No module named 'scripts'` | Python路径问题 | 确保在 `kd/` 根目录运行，或添加 `sys.path.insert(0, r'C:\\Users\\kkk49\\.agents\\skills\\kd')` |
| Excel写入失败 `Permission denied` | Excel文件被占用 | 关闭Excel后再重试 |
| Excel写入失败 `FileNotFoundError` | 目录不存在 | 确保路径存在，或让程序自动创建 |
| 配置未生效 `KeyError: 'copy_library_path'` | 配置文件未初始化 | 运行配置设置命令或检查 `config/user_config.json` 是否存在 |
| 飞书上传失败 `Permission denied` | 权限未开通 | 运行 `python scripts/feishu_permission_helper.py` 开通权限 |
| 飞书上传失败 `Space not found` | 空间ID错误 | 检查 `config/user_config.json` 中的 `report_space_id` 是否正确 |
| 搜索超时 `TimeoutError` | 网络不稳定 | 检查网络连接，或跳过搜索手动提供爆款标题 |
| 生成脚本为空 `scripts is empty` | 提示词参数缺失 | 检查 `config/templates.json` 和 `prompts/` 目录下模板文件是否完整 |
| 格式检查失败 `Format mismatch` | Excel格式变更 | 重新执行 Step 5 格式扫描 |
| 中文乱码 | 编码问题（Windows） | 使用 Python 脚本读取文件，而非直接查看 |
| Python版本不兼容 | Python < 3.7 | 升级到 Python 3.7+ |

### Windows 用户特别提醒

1. **路径分隔符**：使用双反斜杠 `\\` 或原始字符串 `r'C:\path'`
   ```python
   # ❌ 错误
   path = "C:\\Users\\name\\file.xlsx"
   
   # ✅ 正确
   path = r"C:\\Users\\name\\file.xlsx"
   path = "C:\\\\Users\\\\name\\\\file.xlsx"
   ```

2. **中文文件名**：PowerShell 可能显示乱码，使用 Python 脚本读取
   ```python
   import os
   files = os.listdir(r"F:\\vlog\\JT\\idea")
   for f in files:
       print(f)  # 正确显示中文
   ```

3. **Excel被占用**：确保生成脚本时 Excel 文件已关闭

### 调试模式

如需详细输出调试信息，在 Python 代码中添加：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 活动配置（v1.1.0新增）

快导支持通过自然语言管理活动，用于自动匹配脚本关联活动。

### 配置方式

#### 方式1：自然语言命令（推荐）

```python
from scripts.activity_manager import ActivityManager

manager = ActivityManager()

# 添加活动
manager.execute_command(
    manager.parse_natural_language("添加活动：春节特惠，关键词：春节、过年、团圆")
)

# 列出所有活动
manager.execute_command(
    manager.parse_natural_language("列出所有活动")
)

# 查询活动
manager.execute_command(
    manager.parse_natural_language("查询活动：春节")
)

# 删除活动
manager.execute_command(
    manager.parse_natural_language("删除活动：春节特惠")
)
```

#### 方式2：直接编辑配置文件

编辑 `config/platforms.json`，在 `activities` 部分添加：

```json
"activities": {
  "list": [
    {
      "id": "act_1",
      "name": "春节特惠",
      "keywords": ["春节", "过年", "团圆"],
      "applicable_platforms": ["xiaohongshu", "douyin", "shipinhao", "pyq"],
      "note": "春节期间推广活动"
    },
    {
      "id": "act_2", 
      "name": "枇杷采摘季",
      "keywords": ["枇杷", "采摘", "太平镇"],
      "applicable_platforms": ["xiaohongshu", "douyin"],
      "note": "5-6月枇杷采摘活动"
    }
  ],
  "user_configured": true
}
```

### 自动匹配规则

生成脚本时，系统会根据脚本主题自动匹配活动：
- 活动名称匹配：+10分
- 关键词匹配：每个+5分
- 平台不匹配：0分（排除）

得分最高的活动会被自动填入Excel的L列（关联活动）。

### 默认显示

如未配置任何活动，L列显示：
```
日常推广，当前未设置activities
```

---

## 联系我们

如有问题或建议，欢迎交流：

- **微信号：** huitouyoujianta
- **用途：** 快导(KD)技能使用咨询、功能建议、技术交流

欢迎加微信交流学习！
