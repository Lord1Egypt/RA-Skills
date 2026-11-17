# KingbaseES 客体重用

通过在资源申请和释放时清除介质上的残留信息，满足客体重用要求，避免数据泄露。

## 1. 概述

客体重用功能在 KingbaseES 资源释放时销毁残留数据，防止后续用户或进程读取到之前写入的敏感信息。

### 销毁方式

- **共享缓冲区销毁**：全 0 覆盖
- **磁盘文件残留销毁**：置 0 方法

## 2. 配置参数

| 参数名 | 取值范围 | 默认值 | 描述 |
|--------|---------|--------|------|
| sysreuse_residual_data.enable_obj_reuse | on/off | off | 启用客体重用功能 |

该参数为 PGC_SIGHUP 级别，可通过 SELECT sys_reload_conf() 动态生效。

## 3. 配置步骤

### 加载插件

修改 kingbase.conf 中 `shared_preload_libraries` 参数后重启数据库：

```sql
# kingbase.conf
shared_preload_libraries = 'sysreuse_residual_data'
```

### 查看功能状态

```sql
SHOW sysreuse_residual_data.enable_obj_reuse;
-- off
```

### 开启功能

```sql
\c - system

ALTER SYSTEM SET sysreuse_residual_data.enable_obj_reuse = true;
SELECT sys_reload_conf();

SHOW sysreuse_residual_data.enable_obj_reuse;
-- on
```

### 卸载插件

```sql
# kingbase.conf
shared_preload_libraries = ''
```

修改后重启数据库即可卸载。

## 4. 常见问题

### 问题1：开启后性能影响

共享缓冲区全 0 覆盖和磁盘置 0 操作会引入额外 I/O 开销。在性能敏感场景需评估影响。

### 问题2：客体重用功能不生效

**排查**：
- 确认 sysreuse_residual_data 插件已加载到 shared_preload_libraries
- 确认 enable_obj_reuse 参数已设置为 on
- 数据库已重启（插件加载需重启）

## 最佳实践

1. 仅在需要满足客体重用合规要求的场景开启
2. 评估 I/O 性能影响后再决定启用范围
3. 不使用时及时卸载插件以消除性能开销
