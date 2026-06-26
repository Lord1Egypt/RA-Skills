# 配置文件管理

配置文件存储浏览器状态（cookies、历史、本地存储）。

## 创建配置文件

```bash
# 使用新配置文件启动
BRIDGE_PROFILE=~/.pinchtab/work-profile pinchtab &
```

## 配置文件位置

- **macOS/Linux**: `~/.pinchtab/<profile-name>`
- **Windows**: `%USERPROFILE%\.pinchtab\<profile-name>`

## 多配置文件

```bash
# 实例 1 - 工作配置文件
BRIDGE_PROFILE=~/.pinchtab/work BRIDGE_PORT=9867 pinchtab &

# 实例 2 - 个人配置文件
BRIDGE_PROFILE=~/.pinchtab/personal BRIDGE_PORT=9868 pinchtab &
```

## 配置文件隔离

每个配置文件完全隔离：
- Cookies
- 本地存储
- 会话存储
- 浏览器历史
- 保存的密码（如果启用）

## 清理配置文件

```bash
# 删除配置文件
rm -rf ~/.pinchtab/work-profile
```

## 最佳实践

1. **自动化专用** - 为自动化任务创建空配置文件
2. **定期清理** - 定期删除并重建配置文件
3. **不要共享** - 每个用户/任务使用独立配置文件
