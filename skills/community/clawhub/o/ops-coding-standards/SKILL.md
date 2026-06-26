---
name: ops-coding-standards
description: 运维后台（Python/Django）编码规范与最佳实践，适用于 ops_api 等运维系统开发。当要求写ops代码、代码审查、检查编码规范、Python Django开发规范时自动激活。
triggers:
  - (.*) ops (.*) 代码规范 (.*)
  - (.*) 运维后台 (.*) 开发规范 (.*)
  - (.*) django (.*) 编码规范 (.*)
  - (.*) python (.*) 代码审查 (.*)
  - (.*) celery (.*) 事务 (.*)
required_commands: []
required_environment_variables: []
---

# ops运维后台编码规范

> 通用运维后台 Python/Django 编码规范，适用于所有 ops 系统开发。

---

## 一、规范范围

- 所有新代码必须遵循 **PEP8** 编码规范
- PEP8 规范参考：https://pep8.org/

---

## 二、文件头注释（新建 .py 文件时必须）

```python
# -*- coding: utf-8 -*-
"""
@File    : ${NAME}.py
@Desc    : ${DESCRIPTION}
@Author  : ${USER}
@Date    : ${DATE}
"""
```

---

## 三、函数 docstring 规范

### 3.1 代码行数多 → 必须分步说明

```python
def sync_server_data(server_id):
    """
    同步服务器数据

    第一步：校验目标服务器状态
    第二步：执行数据导出
    第三步：数据传输到目标节点
    第四步：更新数据库记录
    第五步：发送通知

    :param server_id: 服务器ID
    :return: bool  是否成功
    """
    pass
```

### 3.2 代码行数少 → 简要注释即可

```python
def get_server_status(server_id):
    """查询游戏服运行状态"""
    return Server.objects.get(id=server_id).status


def disable_user(uid):
    """批量禁用用户"""
    User.objects.filter(id=uid).update(is_active=False)
```

---

## 四、PEP8 代码规范

代码在 PyCharm / IDE 里**应避免出现黄色波浪线**（PEP8 违规提示）。

| 违规 | 错误 | 正确 |
|------|------|------|
| 运算符缺空格 | `a+b` | `a + b` |
| 逗号后缺空格 | `def f(a,b)` | `def f(a, b)` |
| 单行过长 | 超过120字符 | 换行或拆分 |
| import 顺序错误 | 先 import 第三方 | 标准库 → 第三方 → 本地 |

**格式化**：每次完成后用 IDE reformat（Ctrl+Alt+L / Cmd+Option+L），再提交。

---

## 五、Django + Celery 事务规范（高危！）

### 5.1 事务内调用异步任务的坑

`transaction.atomic()` 上下文内的 SQL **不会自动提交**给 Celery 异步任务。异步任务在独立数据库连接中执行，不受当前事务影响。

**❌ 错误**：
```python
with transaction.atomic():
    Task.objects.create(...)
    async_task.delay(...)  # 事务回滚，但任务已在独立连接执行
```

**✅ 正确**：
```python
with transaction.atomic():
    Task.objects.create(...)
# 事务提交后再触发
async_task.delay(...)
```

### 5.2 异步任务路由

```python
@app.task(queue='high_priority')
def critical_task():
    pass

@app.task(queue='default')
def normal_task():
    pass
```

---

## 六、日志轮转规范（防止磁盘撑爆）

所有 Web 服务必须配置日志轮转。

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '/var/log/ops_api/app.log',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 30,
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}
```

---

## 七、Django Admin 命令 vs 离线脚本

| 场景 | 推荐方式 |
|------|---------|
| Web 后台触发的运维动作 | Django Admin 命令（management/commands/） |
| 纯定时任务（crontab） | 离线脚本 |
| 需要版本控制 | Django Admin 命令 |

---

## 八、敏感信息过滤（必须遵守！）

| ❌ 禁止 | ✅ 正确做法 |
|--------|-----------|
| 硬编码密码/密钥/Secret 在代码中 | 使用环境变量 `${VAR}` 或配置文件读取 |
| 在日志中打印敏感字段 | 过滤或脱敏处理 |
| 在错误信息中暴露内部路径/接口 | 返回通用错误信息 |

**示例**：
```python
# ❌ 硬编码
API_KEY = "sk-xxxxx-secret"

# ✅ 环境变量
API_KEY = os.environ.get("API_KEY", "")

# ❌ 日志打印敏感信息
logger.info(f"password={password}")

# ✅ 脱敏打印
logger.info(f"user_id={user_id}, action=login")
```

---

## 九、不要做什么

| ❌ 禁止 | ✅ 正确做法 |
|--------|-----------|
| 事务内直接调用 Celery 异步任务 | 事务提交后再触发 |
| 硬编码密码/密钥在代码中 | 环境变量或安全存储 |
| 不格式化代码就提交 | Ctrl+Alt/L 格式化后提交 |
| 代码有黄色波浪线不处理 | 立即修复 PEP8 违规 |
| 在生产代码中暴露内部接口信息 | 统一错误返回值 |
| 把 `.git` 目录部署到生产 | 部署前删除 |

---

## 十、自检清单

每次提交前检查：

1. ✅ 无 PEP8 黄色/红色波浪线
2. ✅ 每个函数有 docstring
3. ✅ Ctrl+Alt+L 格式化后提交
4. ✅ 事务 + 异步任务场景已考虑
5. ✅ 无硬编码敏感信息
6. ✅ 日志配置了轮转