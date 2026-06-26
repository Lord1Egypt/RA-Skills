# 日志规约

> 来源: Java开发手册（嵩山版）— 二(三) 日志规约

## 【强制】规则

### 1. 使用日志门面 SLF4J/JCL

不可直接使用 Log4j/Logback 的 API。

> **正例**:
> ```java
> import org.slf4j.Logger;
> import org.slf4j.LoggerFactory;
> private static final Logger logger = LoggerFactory.getLogger(Test.class);
> ```

### 2. 日志保存 15 天

当天日志以"应用名.log"保存在 `/home/admin/应用名/logs/` 目录下。历史日志: `{logname}.log.{yyyy-MM-dd}`

### 3. 安全日志保存 6 个月

网络运行状态、安全事件、个人敏感信息操作等记录，留存不少于六个月，多机备份。

### 4. 扩展日志命名

格式: `appName_logType_logName.log`

> **正例**: `mppserver_monitor_timeZoneConvert.log`

### 5. 占位符拼接

字符串变量之间使用 `{}` 占位符，不用 `+` 拼接。

> **正例**: `logger.debug("id: {} and symbol: {}", id, symbol);`

### 6. 日志级别开关

`trace/debug/info` 级别输出必须进行级别判断。

> **正例**:
> ```java
> if (logger.isDebugEnabled()) {
>     logger.debug("Current ID is: {} and name is: {}", id, getName());
> }
> ```

### 7. 避免重复打印

配置文件中设置 `additivity=false`。

> **正例**: `<logger name="com.taobao.dubbo.config" additivity="false">`

### 8. 生产环境禁用 System.out

禁止 `System.out` / `System.err` / `e.printStackTrace()` 输出日志。

### 9. 异常信息包含两类信息

案发现场信息和异常堆栈信息。

> **正例**: `logger.error("inputParams:{} and errorMessage:{}", params, e.getMessage(), e);`

### 10. 日志禁止 JSON 转对象

如果对象中某些 get 方法覆写了会抛异常，影响业务流程。

## 【推荐】规则

### 11. 谨慎记录日志

- 生产环境禁止 debug 日志
- 有选择地输出 info 日志
- warn 日志注意输出量，避免撑爆磁盘

### 12. warn 记录用户参数错误

避免用户投诉时无所适从。非必要时不打 error 级别。

### 13. 英文描述日志错误信息

国际化团队或海外部署使用英文。英文描述不清楚则用中文。
