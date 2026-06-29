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

## 风险等级

LOW

## 安全声明

本技能仅操作本地文件，不涉及网络请求或敏感信息访问。