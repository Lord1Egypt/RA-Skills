# Nginx Explorer Skill 安装指南

## 安装方法

### 方法1：使用 ClawHub（推荐）
```bash
# 安装到当前工作区
clawhub install nginx-explorer

# 或指定目录
clawhub install nginx-explorer --dir ~/.openclaw/skills
```

### 方法2：手动安装
```bash
# 1. 复制技能目录到 OpenClaw 技能目录
cp -r nginx-explorer ~/.openclaw/skills/

# 或复制到工作区技能目录
cp -r nginx-explorer /path/to/your/workspace/skills/
```

### 方法3：通过 extraDirs 加载
```json5
// 在 ~/.openclaw/openclaw.json 中添加
{
  skills: {
    load: {
      extraDirs: ["/path/to/nginx-explorer"],
      watch: true,
      watchDebounceMs: 250,
    }
  }
}
```

## 配置步骤

### 1. 编辑 OpenClaw 配置文件
```bash
# 如果配置文件不存在，先创建
touch ~/.openclaw/openclaw.json
```

### 2. 添加 nginx-explorer 配置
编辑 `~/.openclaw/openclaw.json`，添加以下内容：

```json5
{
  skills: {
    entries: {
      "nginx-explorer": {
        enabled: true,
        env: {
          NGINX_URL: "http://apt_nginx"  // 你的 nginx 服务器地址
        }
      }
    }
  }
}
```

### 3. 重启 OpenClaw
```bash
# 重启 Gateway 服务
openclaw gateway restart

# 或重启整个 OpenClaw
# （取决于你的安装方式）
```

## 验证安装

### 1. 检查技能是否加载
```bash
# 查看技能状态
openclaw skills list

# 或通过 OpenClaw UI 查看
```

### 2. 测试技能功能
在 OpenClaw 会话中测试：
```
用户：探索 nginx 目录
OpenClaw：应该使用 nginx-explorer 技能来探索 http://apt_nginx/
```

### 3. 检查环境变量
```bash
# 在 OpenClaw 会话中检查环境变量
echo $NGINX_URL
```

## 配置选项

### 必需配置
- `NGINX_URL`: nginx 服务器的基础 URL

### 可选配置
```json5
{
  skills: {
    entries: {
      "nginx-explorer": {
        enabled: true,
        env: {
          NGINX_URL: "http://apt_nginx"
        },
        config: {
          // 启用缓存（默认：true）
          cacheEnabled: true,
          
          // 下载目录（默认：/tmp/nginx-tools）
          downloadDir: "/tmp/nginx-tools",
          
          // 自动清理（默认：true）
          autoCleanup: true,
          
          // 缓存时间（秒，默认：3600）
          cacheTTL: 3600,
          
          // 最大并发请求数（默认：3）
          maxConcurrent: 3
        }
      }
    }
  }
}
```

## 故障排除

### 1. 技能未加载
- 检查 `~/.openclaw/openclaw.json` 语法
- 确认技能目录位置正确
- 查看 OpenClaw 日志：`openclaw gateway logs`

### 2. 环境变量未设置
- 确认配置中的 `env` 部分正确
- 检查技能是否启用（`enabled: true`）
- 重启 OpenClaw 服务

### 3. 无法访问 nginx
- 验证 `NGINX_URL` 是否正确
- 测试网络连接：`curl -I $NGINX_URL`
- 检查防火墙和网络配置

### 4. 权限问题
- 确保 OpenClaw 有权限访问 nginx
- 检查下载目录的写入权限
- 验证 curl 命令可用

## 更新技能

### 通过 ClawHub 更新
```bash
clawhub update nginx-explorer
```

### 手动更新
```bash
# 备份旧版本
cp -r ~/.openclaw/skills/nginx-explorer ~/.openclaw/skills/nginx-explorer.backup

# 复制新版本
cp -r /path/to/new/nginx-explorer ~/.openclaw/skills/
```

## 卸载

### 通过 ClawHub 卸载
```bash
clawhub uninstall nginx-explorer
```

### 手动卸载
```bash
# 移除技能目录
rm -rf ~/.openclaw/skills/nginx-explorer

# 或从工作区移除
rm -rf /path/to/workspace/skills/nginx-explorer

# 从配置中移除
# 编辑 ~/.openclaw/openclaw.json，删除 nginx-explorer 条目
```

## 支持

- 查看技能文档：`cat ~/.openclaw/skills/nginx-explorer/SKILL.md`
- 访问 OpenClaw 文档：https://docs.openclaw.ai
- 加入社区：https://discord.com/invite/clawd