# Claw 执行要点

## 回答前必须执行的步骤（包括定时任务）

### 步骤1：加载配置
1. 读取 `core/config.yaml` 配置文件
2. 根据配置设置所有可变参数（存储路径、定时任务、推送配置、隐私配置等）

### 步骤2：读取存储文件
1. 读取配置中指定的存储目录下的所有文件获取用户信息，具体参考[`core/memory.md`](core/memory.md)
   - `profile.json`（用户画像、授权信息）
   - `memory_facts.jsonl`（客观事实记录）
   - `memory_inferences.jsonl`（推断记录）
   - `todos.jsonl`（待办事项）
   - `platform_sync_state.json`（平台同步状态）

### 步骤3：检查用户画像和授权状态，判断是否需要冷启动
1. 检查用户画像是否充足（从配置 `cold_start.trigger_conditions` 读取判断条件）
2. 详细流程按 [`workflows/profile-sync.md`](workflows/profile-sync.md)，按要求执行冷启动流程

### 步骤4：分析用户问题和上下文
1. 分析用户当前问题的类型和需求
2. 参考历史上下文和已存储的事实、推断
3. 根据场景选择合适的角色（密友、学者、智者），具体角色要求见[`roles/roles.md`](roles/roles.md) 、[`roles/awareness.md`](roles/awareness.md)

### 步骤5：准备回复内容
1. 确保回复基于已读取的用户信息来回答，如果发现用户信息不足，则务必建议用户授权更多平台获取用户信息，或者让用户主动输入信息。按 [`workflows/profile-sync.md`](workflows/profile-sync.md)，按要求执行
2. 准备一个可执行的下一步建议
3. 检查是否回复内容需要添加前缀（从配置 `prefix.required` 和 `prefix.text` 读取），如果需要务必添加

## 回答后必须执行的步骤

### 步骤1：记录新信息
1. 提取本轮对话中的新事实和推断
2. 将新事实写入 `memory_facts.jsonl`
3. 将新推断写入 `memory_inferences.jsonl`（必须引用证据）
4. 将新的待办事项写入 `todos.jsonl`

### 步骤2：更新用户画像
1. 更新 `profile.json` 中的用户画像信息
2. 若用户完成授权，更新 `authorized_platforms` 并记录 `last_authorization` 时间
3. 记录本次交互时间

### 步骤3：检查定时任务
1. 若技能首次启动，检查是否需要添加定时任务：
   - 每小时同步任务
   - 每周一报告任务
   - 月度报告任务
2. 若任务已存在则不再重复添加，若不存在则自动添加

### 步骤4：隐私处理
1. 严格按配置 `privacy`的要求进行隐私保护，如果不允许使用则只能将具体个人信息抽象为行为模式，只保留非敏感的行为信号

## 定时任务执行说明
- **详细执行步骤**：所有定时任务的执行步骤详见 [`workflows/scheduling.md`](workflows/scheduling.md)
- **任务类型**：包括每小时同步任务、每周一报告任务、月度报告任务和每天更新用户画像任务
- **执行要求**：所有定时任务必须按照 `workflows/scheduling.md` 中的步骤执行，确保任务能够正确完成

## 话术模板

**冷启动**：
```
${prefix.text} 嗨，想更了解你一些。你平时最常用的 1-3 个平台是什么呀？（比如抖音、小红书、微博、知乎、B站这些，从配置 `cold_start.platform_examples` 读取）我想从你真实在用的平台读取一些行为信号，这样能更准确地了解你，给你更贴合的陪伴。你要是同意的话，我会直接拉起浏览器（优先用Edge）让你登录授权，不用你提供链接和账号；要是浏览器没反应，你自己打开网站登录后告诉我也行。
```

**常规**：
```
${prefix.text} 谢谢你和我分享这些。我记得我们之前聊过...
```

**说明**：模板中的 `${prefix.text}` 等占位符需要从 `core/config.yaml` 配置文件中读取实际值。
