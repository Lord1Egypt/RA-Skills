# 水产市场上架内容 — minimax-image-gen

**技能名称：** minimax-image-gen
**分类：** 图像生成 / 文生图
**作者：** Mzusama
**价格：** 免费

---

## 标题
MiniMax image-01 文生图工具 — 集成 Token Plan 额度

## 短描述
使用 MiniMax image-01 模型从文字生成图片。支持中国区和国际区双端。Token Plan 套餐每日 50 张免费额度。

## 完整描述

MiniMax image-01 文生图工具，集成到 OpenClaw。

### 功能亮点
- **文生图**：使用 MiniMax image-01 模型，支持中英文 prompt
- **双端支持**：中国区（api.minimax.chat）和国际区（api.minimax.io）自动适配
- **Prompt 自动增强**：短描述自动补充专业光影、构图、画质参数，效果更佳
- **比例控制**：16:9、1:1、9:16、4:3、21:9 等多种比例
- **批量生成**：一次生成最多 9 张候选图
- **Token Plan 额度**：直接消耗你的 Plus 套餐额度（每日 50 张），无需额外付费

### 快速示例
```
你：帮我画一张赛博朋克风格的城市夜景
→ 自动执行：python image_gen.py "赛博朋克城市夜景..." --region cn --aspect 16:9

你：画一只猫
→ 自动执行：python image_gen.py "a cat..." --region cn
```

### 使用前提
- MiniMax API Key（从 MiniMax 开放平台获取）
- 设置环境变量 `MINIMAX_API_KEY`
- Python 环境（需安装 requests 库）

### 区域选择
使用前需指定区域：
- `--region cn`：中国区用户（MiniMax 中国站）
- `--region global`：国际区用户（MiniMax 国际站）

### 模型信息
- **模型：** MiniMax image-01
- **每日额度：** 50 张（Token Plan Plus 套餐）
- **API 地址：** api.minimax.chat（中国区）| api.minimax.io（国际区）

### ⚠️ 每日额度（Token Plan）
| 套餐 | 每日图片额度 | 备注 |
|------|-------------|------|
| Starter | 0 | 不包含图像生成 |
| **Plus** | **50 张/天** | 推荐，默认套餐 |
| Max | 120 张/天 | |
| Ultra | 800 张/天 | |

额度每日零点重置，直接消耗 Token Plan 套餐额度，无需额外付费。

### 模型信息
- **模型：** MiniMax image-01
- **API 地址：** api.minimax.io（国际区）| api.minimax.chat（中国区）

### 作者
**Mzusama**
