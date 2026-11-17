# 基于 skill-standardization 渐进式披露规范的权限说明

本文档由 `skill-standardization` 权限扫描器自动维护。

## 风险等级

**LOW**（实际权重: 0.0）

## 权限总览

| 权限类别 | 涉及项数 | 风险等级 |
|-----------|----------|----------|
| `subprocess_call` | 0 项 | ✅ LOW |
| `file_delete` | 0 项 | ✅ LOW |
| `network_access` | 0 项 | ✅ LOW |
| `sensitive_access` | 0 项 | ✅ LOW |
| `critical_write` | 0 项 | ✅ LOW |

## 高权限操作说明

- 无。所有文件操作均限制在技能独立数据目录内，不涉及系统关键目录、网络监听或外部请求。

## 权限详细说明

### 子进程调用（subprocess）

**无**。


### 文件删除

**无**。


### 网络访问

**无**。


### 敏感信息访问

**无**。


### 关键位置写入

**无**。


## 授权方式说明

- **immediate（即时授权）**：每次执行前需获得用户批准
- **unified（统一授权）**：首次执行前获得用户批准，后续不再询问
- **silent（静默授权）**：无需用户交互，自动执行并记录

<!-- fp:risk=LOW|sensitive=0|critical_write=0|network=0|delete=0|subprocess=0|issues=0 -->
---

# 权限说明

本文档说明 hug-html 技能的权限需求、各操作的权限权重及风险评级。

## 权限权重说明

| 操作 | 权限权重 | 说明 |
|------|----------|------|
| Read（读文件） | LOW | 读取输入文件、模块库、样式预设，无写入操作 |
| Write（写文件） | MEDIUM | 将输出 HTML 文件写入 `../.standardization/hug-html/data/output/`，仅限指定目录 |
| Bash（运行脚本） | MEDIUM | 运行 `scripts/` 目录内的 Python 脚本，不执行系统命令或外部代码 |
| 网络访问 | NONE | 不访问任何外部网络，不发送数据 |

## 风险评级

本技能风险等级：**LOW**

**原因**：
- 所有操作仅限于本地文件读写
- 不访问系统敏感路径（如 `~/.ssh/`、`~/.aws/`）
- 不向外部网络发送任何数据
- 不执行用户 Shell 配置文件（`.bashrc` / `.zshrc`）

## 敏感信息访问声明

本技能：
- **不会**访问系统敏感路径或凭证文件
- **不会**向外部网络发送数据
- **不会**执行用户 Shell 配置文件（`.bashrc` / `.zshrc`）

---

> 本文档遵循 R-15/R-16 权限说明规范，由 `skill-standardization v2.38.6` 生成。
