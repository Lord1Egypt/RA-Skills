# error-guard - 错误守卫

## 功能
实时监控错误、自动拦截、预防问题

## 核心机制

### 1. 错误分类

#### 致命错误 (立即处理)
- 内存溢出
- 磁盘满
- 认证失效
- 系统崩溃

#### 严重错误 (快速处理)
- API 超时
- 连接失败
- 权限不足

#### 警告 (记录并监控)
- 速率限制
- 临时失败
- 资源紧张

#### 信息 (仅记录)
- 调试日志
- 性能指标

### 2. 错误模式识别
```python
def detect_error_pattern(errors):
    # 检测重复错误
    if len(set(errors[-5:])) == 1:
        return "repeating_error"
    
    # 检测错误累积
    if error_rate() > threshold:
        return "error_accumulation"
    
    # 检测级联错误
    if has_cascade(errors):
        return "cascade_failure"
    
    return "isolated_error"
```

### 3. 自动拦截规则
```
IF 同一错误出现 3 次 THEN
    记录并警告
    暂停相关操作
    进入熔断模式
END

IF 错误率 > 10% THEN
    降低操作频率
    增加重试延迟
    通知管理员
END

IF 致命错误 THEN
    保存完整上下文
    执行优雅关闭
    触发重启
END
```

### 4. 错误预防
```python
# 执行前验证
async def pre_execution_check(command):
    checks = {
        "auth": verify_token(),
        "resources": check_resources(),
        "rate_limit": check_rate_limit(),
        "dependencies": check_services()
    }
    
    if not all(checks.values()):
        raise PreExecutionError("验证失败")
    
    return True
```

### 5. 错误恢复
```python
async def error_recovery(error):
    strategies = {
        "auth_error": refresh_and_retry,
        "timeout_error": retry_with_backoff,
        "rate_limit_error": wait_and_retry,
        "resource_error": free_resources_and_retry
    }
    
    strategy = strategies.get(error.type, default_retry)
    return await strategy(error)
```

---

*🦞 辉仔 - 错误终结者*
