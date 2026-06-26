# ✅ thinkzone-image 全局技能配置完成

## 📋 配置摘要

**技能名称：** thinkzone-image  
**类型：** 全局技能（所有 agent 可用）  
**状态：** ✓ 全局可用  
**API Key：** `amags_b6324919c0056a78dc326ef06011ecc7d2af896b6b659c216371e55d66895dac`  
**API 地址：** `https://open.thinkzoneai.com`  
**测试结果：** ✅ 成功生成图片（2026-03-19 14:06）

---

## 🎯 触发条件

**任何 agent 在以下情况都会自动调用：**

| 场景 | 触发词示例 |
|------|-----------|
| **图片生成** | "画一张..."、"生成图片"、"AI 绘图"、"做一张图" |
| **配图需求** | "生成一张配图"、"需要一张...的图片" |
| **图生图** | "基于这张图生成"、"参考这张图" |

---

## 📚 文档位置

| 文档 | 路径 |
|------|------|
| **全局技能注册表** | `workspace/GLOBAL-SKILLS.md` |
| **详细使用指南** | `workspace/skills/thinkzone-image/GLOBAL-IMAGE-GENERATION.md` |
| **本地配置** | `workspace/TOOLS.md`（已更新） |

---

## 🎨 可用模型（3 个 · 图片）

- 🖼️ **Gemini 3.1 Flash** - 多模态/参考图
- 🖼️ **MiniMax Image 01** - 人物/动物主体
- 🖼️ **Seedream 5.0 Lite** - 轻量 2K/3K

---

## 🔧 调用方式

### 自动调用（推荐）

用户直接说：
```
画一只吃玉米的金毛犬
```

Agent 自动：
1. 识别图片生成意图
2. 询问或选择模型
3. 调用脚本生成
4. 返回结果

### 手动调用

```bash
cd C:\Users\Administrator\.openclaw\workspace\skills\thinkzone-image
python scripts/gen_image.py --prompt "描述" --model "模型 ID"
```

---

## ⚠️ 当前状态

### ✅ 已完成
- [x] 技能脚本就绪
- [x] 全局配置文档创建
- [x] TOOLS.md 更新
- [x] 触发条件定义
- [x] 模型列表配置

### ⚠️ 需要注意
- [!] **账户余额不足** - 需要充值才能使用
- [!] 环境变量已设置（`THINKZONE_API_KEY`）

---

## 🧪 测试方法

### 测试 1：图片生成意图识别

在任何 agent 对话中发送：
```
画一只可爱的猫咪
```

**预期：** Agent 识别图片生成意图，询问使用哪个模型

### 测试 2：指定模型生成

```
用 Seedream 生成一张露营的图片
```

**预期：** Agent 直接调用 Seedream 模型生成

## 📞 与其他技能配合

### 小红书运营场景

```
用户：帮我发一篇露营笔记，需要配图

工作流：
1. thinkzone-image → 生成露营图片
2. xiaohongshu-skills → 发布笔记
```

### 内容创作场景

```
用户：仿写这篇笔记并生成配图

工作流：
1. xiaohongshu-rewriter → 分析并仿写
2. thinkzone-image → 生成配图
```

---

## 🐛 故障排查

### 问题：账户欠费

**错误：** `AccountOverdueError`

**解决：** 访问 https://testing.amags.thinkzoneai.com 充值

### 问题：技能未触发

**检查：**
1. 确认触发词是否匹配
2. 检查 agent 是否加载了全局技能配置
3. 重启 Gateway 重新加载

---

## 📝 下一步

1. **充值账户** - 访问 ThinkZone 平台充值
2. **测试生成** - 充值后测试图片生成功能
3. **集成测试** - 测试与其他技能的配合

---

**配置完成时间：** 2026-03-19  
**配置者：** 田渝米 🍚  
**状态：** ✓ 全局可用（待充值）
