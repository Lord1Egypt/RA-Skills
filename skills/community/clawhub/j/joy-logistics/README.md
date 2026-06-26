# 京东国际物流数据查询技能

> 本项目是京东国际物流数据查询技能，提供物流轨迹追踪、国际供应链运营、跨境小包体验指标查询两大功能模块。

## 项目结构

```
joy-logistics/
├── skills/
│   ├── joy-logistics-indicator/    # 供应链运营指标查询技能
│   └── joy-logistics-trace/        # 国际物流轨迹追踪技能
├── README.md               # 项目说明文档
└── SKILL.md                # 技能详细说明文档
```

## 1. Skills 总览

| # | Skill 名称 | 功能 | 分类 |
|---|-----------|----|----|
| 1 | **joy-logistics-indicator** | 国际供应链运营指标查询技能 | 文档 |
| 2 | **joy-logistics-trace** | 国际物流轨迹追踪技能 | 文档 |

## 2. 前置准备

### 2.1 安装基础工具

```bash
# 安装 ClawHub CLI（用于从 ClawHub 安装 Skills）
npm i -g clawhub
```

### 2. 配置权限

MAC/Linux
```bash
echo 'export token=66Pi3xz*******yzNHvRNJgeJsqtSkn7fcJ4' >> ~/.zshrc && source ~/.zshrc
```

Windows
```powershell
[Environment]::SetEnvironmentVariable("token", "66Pi3xz*******yzNHvRNJgeJsqtSkn7fcJ4", "User")
```

## 3. Skills 安装


```bash
# 登录 ClawHub（需 GitHub 账号）
clawhub login

# 安装单个 skill
clawhub install joy-logistics-indicator --dir ~/.workspace/skills

# 批量安装所有国际物流 skills
for skill in joy-logistics-indicator joy-logistics-trace; do
  clawhub install "$skill" --dir ~/.workspace/skills --force
done
```

### 4. 验证安装

在和openclaw的对话中输入：

```
列出我安装的国际物流相关 skills
```