# Pet-Game 工作流 Skill

> 本 Skill 定义了 Pet-Game 小程序项目的版本控制和工作流规范。
> AI 助手在进行任何文件修改前**必须**遵守以下规则。

---

## 1. 版本控制系统概述

### 备份文件结构
```
pet-game/
├── .qtools/                      # 工具脚本
│   └── backup_wrapper.py        # 备份入口脚本
├── .backups/                     # 备份区
│   ├── baselines/               # 基准快照
│   ├── elements/              # 频繁元素快照
│   └── state.json             # 版本状态
└── skills/
    └── pet-game-workflow/     # 本 Skill
        └── SKILL.md          # 工作流规则
```

### 备份脚本使用方法
```bash
# 备份单个文件（修改前必须执行）
python .qtools\backup_wrapper.py backup <相对路径> [元素名]

# 示例
python .qtools\backup_wrapper.py backup subpk-home/pages/home/home.wxml BGM开关

# Git commit 后清理备份
python .qtools\backup_wrapper.py clean
```

---

## 2. 强制备份规则（AI 必须遵守）

### 规则 1：修改前必须备份 ⚠️
- **触发条件**：任何文件修改（WXML/WXSS/JS/JSON/MD 等）
- **动作**：先执行 `python .qtools\backup_wrapper.py backup <相对路径> [元素名]`
- **违规后果**：主人会生气 😡
- **示例**：
  ```bash
  # 修改 home.wxml 前
  python .qtools\backup_wrapper.py backup subpk-home/pages/home/home.wxml BGM开关
  # 然后才能修改文件
  ```

### 规则 2：时间窗口
- **规则**：5 分钟内同文件只保留第一个备份
- **实现**：`backup_wrapper.py` 自动检查 `.backups\state.json` 中的 `lastBackupTime`
- **AI 无需判断**，脚本自动处理

### 规则 3：元素追踪
- **规则**：同一元素调整超过 3 次 → 自动建元素快照
- **实现**：`backup_wrapper.py` 自动追踪元素调整次数（基于 `[元素名]` 参数）
- **AI 无需判断**，脚本自动处理

### 规则 4：Git Commit 后清理
- **触发条件**：执行 `git commit` 后
- **动作**：执行 `python .qtools\backup_wrapper.py clean`
- **示例**：
  ```bash
  git commit -m "fix: xxx"
  python .qtools\backup_wrapper.py clean
  ```

### 规则 5：禁止跳过备份
- **禁止行为**：跳过备份直接修改文件
- **AI 必须自觉遵守**，不能等主人提醒
- **违规后果**：主人会生气 😡

---

## 3. AI 工作流程

### 标准流程
1. **收到文件修改任务**
2. **立即执行备份**：`python .qtools\backup_wrapper.py backup <相对路径> [元素名]`
3. **等待备份成功**（确认输出 "Backup saved" 或类似信息）
4. **修改文件**
5. **如果修改 >3 次**，备份脚本会自动建元素快照
6. **Git commit 后执行清理**：`python .qtools\backup_wrapper.py clean`

### 禁止行为 ❌
- 跳过备份直接修改文件
- 等主人提醒才备份
- 忘记在 git commit 后执行清理
- 同一元素调整超过 3 次但不建元素快照

---

## 4. 触发条件

本 Skill 在以下场景**自动触发**：

- 任何修改 `pet-game/` 目录下的文件（WXML/WXSS/JS/JSON/MD 等）
- 任何 Git commit 操作后
- 任何元素位置调整、样式修改、功能变更

---

## 5. 相关文件

- 备份脚本：`.qtools/backup_wrapper.py`
- 备份区：`.backups/`
- 元素快照：`.backups/ELEMENT-SNAPSHOTS.md`
- 项目根目录：`C:\Users\marsz\.qclaw\workspace\pet-game`

---

## 6. 注意事项

1. **每次修改前必须备份**，这是最高优先级规则
2. 备份脚本会自动处理时间窗口和元素追踪
3. Git commit 后必须执行���理
4. 如果不确定是否需要备份，**默认执行备份**
5. **禁止跳过任何备份步骤**

---

> ⚠️ **警告**：不遵守本规则将导致主人不满。AI 必须自觉执行备份！