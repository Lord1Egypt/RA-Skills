# Setup - my-study-pal

当 `mystudy/` 不存在、为空，或关键文件缺失时，读取本文件。
目标不是立刻开讲，而是先把概念解释系统初始化到可运行状态。

## Priority Order

### 1. 确认激活范围和主场景

优先确认当前是否属于这个 skill 的主场景：
- 用户在问陌生概念、术语、缩写、名词
- 用户想知道某个词在当前语境里是什么意思
- 用户想区分两个相近概念

如果不是这个场景，不要强行进入本系统。

### 2. 确认最小用户画像

首次启用时，尽量补齐最小必要画像：
- 用户工作 / 专业 / 业务领域
- 用户爱好领域
- 用户最近的学习知识点
- 直答模式偏好
- 讲解式偏好
- 引导式偏好
- 辨析式偏好
- 场景应用式偏好
- 记忆巩固式偏好
- 语言风格偏好

如果信息不全，不要卡住流程：
- 先创建默认画像
- 后续在真实对话中逐步补齐

### 3. 补齐文件系统骨架

创建 `mystudy/` 并补齐：
- `study-summary.md`
- `study-detail/`
- `user-profile.md`
- `runtime-profile.md`

优先运行初始化脚本：

```powershell
powershell -ExecutionPolicy Bypass -File "<skill-root>/scripts/init_mystudy.ps1" -Root "<workspace-root>"
```

如果脚本不可用，再按 `references/blueprint.md` 和 `references/study-storage.md` 的模板与规则手动补齐。

当 `user-profile.md` 发生长期偏好更新后，刷新当前生效配置：

```powershell
python "<skill-root>/scripts/refresh_runtime_profile.py" --root "<workspace-root>"
```

### 4. 验证可运行状态

只有在以下条件满足时，系统才算达到可运行状态：
- `mystudy/` 存在
- `study-summary.md` 存在
- `study-detail/` 存在
- `user-profile.md` 存在
- `runtime-profile.md` 存在
- `user-profile.md` 至少包含 6 种回答方式的默认配置与语言风格默认配置

如果尚未达到可运行状态，先补齐，不要直接进入长期记录流程。

### 5. 开始首次解释并落盘

完成可运行状态检查后：
- 正常解释用户当前概念
- 若形成了明确主题，更新 `study-summary.md`
- 有必要时创建或追加 `study-detail/` 记录
- 如果新得到用户画像信息，同轮更新 `user-profile.md`

## 需要写入的内容

| Save to | Content |
|---------|---------|
| `study-summary.md` | 学习主题总表、时间、回答方式、是否完成 |
| `study-detail/YYYYMMDD主题名.md` | 单个学习主题的对话记录、回答方式 |
| `user-profile.md` | 用户领域、爱好、最近学习知识点、6 种回答方式偏好、语言风格偏好 |

## 约束规则

- 不要因为用户画像不完整就拒绝解释
- 不要覆盖已有用户档案
- 不要把临时偏好误写成长期偏好
- 不要在系统尚未达到可运行状态时假装已完成初始化
- 不要把与概念解释无关的闲聊写进长期记录
