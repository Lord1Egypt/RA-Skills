# Keep Learning Agent

> 持续学习，每天进步一点点
> 
> 统一的知识沉淀和经验固化框架，适合所有 AI Agent 使用

---

## 🎯 与 self-improving-agent 的区别

| 特性 | self-improving-agent | xiaomi-learning-system |
|------|---------------------|----------------------|
| **模板完整性** | 简单（缺少根因分析） | 完整（含 5Why 分析） |
| **索引系统** | 无 | ✅ INDEX.md |
| **自我修复** | 基础 | ✅ 集成 self-repair.ps1 |
| **可复用库** | 无 | ✅ lib/ 模块 |
| **SOP 文档** | 无 | ✅ KNOWLEDGE-SOP.md |
| **经验→模型** | 基础 | ✅ 完整流程 |
| **状态管理** | 简单 | ✅ 完整流转 |
| **Pattern-Key** | ✅ | ✅ |
| **Recurrence-Count** | ✅ | ✅ |

---

## 📦 安装

```bash
# 已本地安装
# 位置：C:\Users\luvzexi\.openclaw\workspace\skills\xiaomi-learning-system\
```

---

## 🚀 使用

### 1. 记录新学习

```bash
# 复制模板
Copy .learnings/templates/learning-template.md

# 填写内容
Edit with your learning details

# 追加到主文件
Append to .learnings/LEARNINGS.md
```

### 2. 运行自我修复

```powershell
# 会话启动自动运行
G:\clawbot\config\self-repair.ps1
```

### 3. 更新索引

```powershell
# 手动更新
Edit .learnings/INDEX.md

# 或等待 Python 脚本（待创建）
python .learnings/update-index.py
```

### 4. 封装可复用模块

```
1. 解决方案验证成功
2. 创建 lib/xxx.py 模块
3. 更新 lib/README.md
4. 标记状态为 resolved
```

---

## 📁 文件说明

| 文件 | 用途 |
|------|------|
| `SKILL.md` | Skill 定义文档 |
| `_meta.json` | Skill 元数据 |
| `.clawhub/origin.json` | ClawHub 注册信息 |
| `README.md` | 本文件 |

---

## 🔄 与全局配置集成

### self-repair.ps1
```powershell
# 位置：G:\clawbot\config\self-repair.ps1
# 功能：检查 pending 学习项，提取 Pattern-Key
```

### autoload-configs.ps1
```powershell
# 位置：G:\clawbot\config\autoload-configs.ps1
# 功能：会话启动加载配置
```

### skills-config.json
```json
{
  "skills": {
    "xiaomi-learning-system": {
      "configured": true,
      "priority": "critical"
    }
  }
}
```

---

## 📊 当前状态

| 指标 | 数值 |
|------|------|
| 总学习数 | 14 条 |
| 已解决 | 9 条 |
| 已提升 | 4 条 |
| 可复用模块 | 1 个 (feishu_api.py) |

---

## 🎓 设计原则

1. **学到的东西必须固化** - 不只存在于临时会话
2. **可复用优先** - 封装成 lib/ 模块
3. **索引快速查找** - INDEX.md 提供多种索引
4. **自动检查** - self-repair 自动检查 pending 项
5. **定期整理** - 每周归档已 promoted 学习

---

*版本：1.0.0*  
*创建时间：2026-03-04*  
*作者：Neo & MiMi*
