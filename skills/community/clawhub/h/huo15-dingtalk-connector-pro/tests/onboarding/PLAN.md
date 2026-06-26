# onboarding（入驻配置）测试方案

## 1. 目的与覆盖范围

`tests/onboarding` 覆盖钉钉连接器的入驻配置流程，包括状态检查、配置流程、权限策略设置和禁用功能。

主要覆盖（以测试文件实际引用为准）：

- 状态检查：**getStatus**
- 配置流程：**configure**
- 私信策略：**dmPolicy**
- 禁用功能：**disable**

## 2. 用例表（覆盖现有测试）

### 2.1 getStatus

| 序号 | 场景 | 期望 |
|------|------|------|
| 1 | 未配置 | 返回 configured=false，状态包含 "needs app credentials" |
| 2 | 已配置且探测成功 | 返回 configured=true，状态包含 "connected as DingBot" |

### 2.2 configure

| 序号 | 场景 | 期望 |
|------|------|------|
| 3 | 使用环境变量 + allowlist 策略 | 正确配置 clientId、clientSecret、groupPolicy 和 groupAllowFrom |
| 4 | 设置密钥流程 + 探测失败 | 正确配置密钥，并显示连接失败提示 |

### 2.3 dmPolicy

| 序号 | 场景 | 期望 |
|------|------|------|
| 5 | 获取当前策略 | 默认返回 "open" |
| 6 | 设置策略为 open | allowFrom 包含 "*" |
| 7 | 提示输入 allowFrom | 正确合并用户输入的 allowFrom 列表 |

### 2.4 disable

| 序号 | 场景 | 期望 |
|------|------|------|
| 8 | 禁用通道 | 将通道的 enabled 标记为 false |

## 3. 预期正确输出与潜在错误

- **正确**：状态检查正确反映配置状态；配置流程支持环境变量和手动输入；权限策略正确合并 allowFrom 列表；禁用功能正确设置 enabled 标记。
- **潜在错误原因**：环境变量未正确读取；探测失败时未正确提示；allowFrom 列表合并逻辑错误；禁用功能未正确设置 enabled 标记。
