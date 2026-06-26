# 🐾 “猫咪塔罗”占卜助手 CLI

这是一个专为 LLM Agent 打造的塔罗占卜命令行动具（CLI）。
它通过标准化的命令行交互，解决塔罗占卜中“随机抽卡”、“牌阵位置映射”以及“Prompt 模板组装”的繁琐过程，让 Agent 能够顺滑地生成专业的占卜文本。

---

## 🚀 安装与依赖

本 CLI 基于 Python 开发，需预先安装核心库 `typer` 和 `pydantic`：

```bash
pip install "typer[all]" pydantic
```

---

## 🛠️ CLI 核心指令集

CLI 主要包含三个核心指令，支持在原生文本模式或对 Agent 友好的 JSON 模式下工作：

- `list`: 枚举当前受支持的所有可用牌阵。
- `draw`: 纯数字占卜模式（自动为你抽取一定数量的塔罗牌）。
- `compose`: 实体伴侣模式（接收你手工录入的牌号组合为解释 Prompt）。

所有产生抽牌结果或 Prompt 组装的指令（`draw` 和 `compose`），都支持加上 `--json` 参数以输出标准 JSON 格式数据。

---

### 1. `list` - 查看所有牌阵清单

列出 `spreads.json` 中配置的所有可用的牌阵信息。这一步通常为 Agent 引导用户选择占卜方式时查询可用选项。

**传参方式：**
```bash
python neko.py list
```

**返回结果示例（纯文本输出）：**
```text
ID: daily_one
名称: 每日一占 (1张)
用途: 用于快速获取今日的能量指引。通过抽取单张卡牌，直击当前核心问题的本质...
----------------------------------------
ID: past_present_future
名称: 时间之流 (3张)
用途: 用于全方位分析事物或关系的发展脉络。通过“过去、现在、未来”三个时间维度...
----------------------------------------
...
```

---

### 2. `draw` - 数字占卜模式 (自动抽卡)

当用户没有实体塔罗牌时，Agent 调用此命令全自动生成随机抽卡结果并组装文本。

**核心传参：**
* `--spread` (必填): 牌阵 ID，例如 `daily_one`, `gain_and_loss`。
* `--no-rev` (可选): 如果带上此标志，抽取的牌组将 100% 只产生正位。
* `--json` (可选): 将最终结果和解析以结构化 JSON 返回，极度适合外挂的 LLM Agent 进行二次解析。

**传参方式：**
```bash
# 基础调用 (自然文本输出提示词)
python neko.py draw --spread daily_one

# 排除逆位，输出 JSON (对 LLM 最友好的调用)
python neko.py draw --spread past_present_future --no-rev --json
```

**返回结果示例 (`--json` 模式)：**

```json
{
  "status": "success",
  "data": {
    "spread_info": {
      "name": "每日一占",
      "count": 1
    },
    "drawn_cards": [
      {
        "pos": "今日指引",
        "name": "战车",
        "rev": false
      }
    ],
    "final_prompt": "呜呜，你是一只既神秘又活泼的“猫咪塔罗牌”占卜解读大师！...\n\n【牌阵名称】：每日一占\n...【位置 1：今日指引】抽到了 战车（正位）。含义提示：正位的战车牌预示着你正处于一个充满胜利和成就的时期。..."
  }
}
```

---

### 3. `compose` - 手动占卜拼接模式 (人工录入)

当用户自己有实体牌或者外部界面已经选好牌时，可以通过这个命令，把外部牌的编号、正逆位信息传给 CLI 来完成专业结构化的拼接。

**核心传参：**
* `--spread` (必填): 牌阵 ID，用于匹配需要的张数（如 `gain_and_loss` 需求 2 张）。
* `--cards` (必填): 逗号分隔的塔罗牌编号（0-77）。编号数量必须与牌阵需求完全一致！
* `--revs` (必填): 逗号分隔的正逆位布尔状态。需与卡牌数量一一对应。
  * `True`, `false`, `1`, `0`, `yes`, `no` 均受支持且忽略大小写。
  * `0` 或 `false` 代表 正位。
  * `1` 或 `true` 代表 逆位。
* `--json` (可选): 以 JSON 返回结构化结果。

**传参方式：**
```bash
# 得失牌阵（需求2张牌），传入 愚者(0)为正位，魔术师(1)为逆位。
python neko.py compose --spread gain_and_loss --cards 0,1 --revs 0,1

# 等效的 JSON 模式
python neko.py compose --spread gain_and_loss --cards 0,1 --revs flase,true --json
```

**异常处理与错误提示 (`--json` 模式下)：**

如果用户的输入有误（如 ID 不存在、数组长度不符）：
```bash
python neko.py compose --spread daily_one --cards 0,1 --revs 0,1 --json
```

**错误回调示例：**
```json
{
  "status": "error",
  "error": "传入的卡牌数量 (2) 与牌阵要求 (1) 不符。"
}
```

---

## 🎨 开发与定制

如果你想更换 Prompt 的系统人设或微调牌阵，你可以随时修改以下文件：
* `tarot.json`: 所有 78 张卡牌的详细定义与释义。
* `spreads.json`: 控制着牌阵和 `shared_prompt_template`（公共 Prompt 模板）。CLI 每次都会动态加载最新数据。
