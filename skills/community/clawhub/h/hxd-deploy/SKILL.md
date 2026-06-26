---
name: hxd-deploy
description: 部署霍小钉服务到服务器。自动上传 JAR 文件、备份旧版本、重启服务。
---

# 霍小钉服务部署工具

自动化部署霍小钉 Spring Boot 服务到远程服务器。

## 触发条件

当用户提到以下关键词时自动触发：
- "部署霍小钉"
- "部署 hxd"
- "部署服务"
- "更新霍小钉"
- "发布霍小钉"
- "hxd 部署"
- "霍小钉上线"

## 部署配置

### 服务器信息
- **IP**: 203.170.59.16
- **用户**: root
- **SSH 私钥**: `~/.ssh/id_ed25519`

### 文件路径
- **本地 JAR**: `D:\springboot\hxd\target\hxd-0.0.1-SNAPSHOT.jar`
- **远程目录**: `/hjxz/hxd-api/lib`
- **远程脚本**: `/hjxz/hxd-api/bin/hxd-api`
- **日志文件**: `/hjxz/hxd-api/logs/wrapper.log`

## 部署步骤

### 1. Maven 打包（新增）

在上传 JAR 之前，先执行 Maven 打包命令：

```powershell
cd "D:\springboot\hxd"
mvn clean package -Pprod -DskipTests
```

打包完成后检查生成的 JAR 文件是否存在。

### 2. 检查本地 JAR 文件

```powershell
Test-Path "D:\springboot\hxd\target\hxd-0.0.1-SNAPSHOT.jar"
```

如果文件不存在，检查 Maven 打包是否成功。

### 3. SSH 连接测试

```powershell
ssh -i "$env:USERPROFILE\.ssh\id_ed25519" -o StrictHostKeyChecking=no root@203.170.59.16 "echo 'SSH connection successful'"
```

### 4. 上传 JAR 文件

```powershell
$timestamp = Get-Date -Format "yyyy-MM-dd-HH-mm"
scp -i "$env:USERPROFILE\.ssh\id_ed25519" -o StrictHostKeyChecking=no "D:\springboot\hxd\target\hxd-0.0.1-SNAPSHOT.jar" "root@203.170.59.16:/hjxz/hxd-api/lib/hxd-0.0.1-SNAPSHOT.jar"
```

### 5. 备份旧版本并替换

```powershell
ssh -i "$env:USERPROFILE\.ssh\id_ed25519" -o StrictHostKeyChecking=no root@203.170.59.16 @"
cd /hjxz/hxd-api/lib
mv hxd.jar hxd.jar.bak$timestamp
mv hxd-0.0.1-SNAPSHOT.jar hxd.jar
"@
```

### 6. 重启服务

```powershell
ssh -i "$env:USERPROFILE\.ssh\id_ed25519" -o StrictHostKeyChecking=no root@203.170.59.16 "/hjxz/hxd-api/bin/hxd-api restart"
```

### 7. 验证服务状态

```powershell
# 检查服务状态
ssh -i "$env:USERPROFILE\.ssh\id_ed25519" -o StrictHostKeyChecking=no root@203.170.59.16 "cat /hjxz/hxd-api/bin/hxd-api.status"

# 检查日志（最近 30 行）
ssh -i "$env:USERPROFILE\.ssh\id_ed25519" -o StrictHostKeyChecking=no root@203.170.59.16 "tail -30 /hjxz/hxd-api/logs/wrapper.log"
```

## 输出要求

部署完成后报告：
1. ✅ JAR 文件上传状态
2. ✅ 备份文件名称（带时间戳）
3. ✅ 服务重启状态（PID、状态）
4. ✅ 服务运行状态（从日志确认）
5. ⚠️ 任何警告或错误信息

## 错误处理

### 常见问题

1. **SSH 连接失败**
   - 检查私钥文件是否存在
   - 检查服务器是否可达
   - 提示用户检查网络或 SSH 配置

2. **JAR 文件不存在**
   - 提示用户先执行 Maven 构建：`mvn clean package`
   - 检查构建路径是否正确

3. **服务启动失败**
   - 查看完整日志：`tail -100 /hjxz/hxd-api/logs/wrapper.log`
   - 检查端口占用：`netstat -tlnp | grep 9999`
   - 检查磁盘空间：`df -h`

4. **备份失败**
   - 检查文件权限
   - 检查磁盘空间

## 示例对话

**用户**: 部署一下霍小钉服务

**助手**: 好的，开始部署霍小钉服务...
- ✅ JAR 文件已上传
- ✅ 旧版本备份为 hxd.jar.bak2026-03-25-16-56
- ✅ 服务已重启，PID: 21499，状态：STARTED
- ✅ 服务正常运行，端口 9999

部署完成！🫘

---

## 注意事项

1. **部署时间**: 避免在业务高峰期部署（工作日 9:00-18:00）
2. **备份保留**: 保留最近 2-3 个备份版本，避免磁盘占满
3. **日志检查**: 每次部署后必须检查日志确认服务正常
4. **回滚方案**: 如需回滚，将备份文件改名为 hxd.jar 后重启服务

## 快速回滚命令

```powershell
# 回滚到上一个版本
ssh -i "$env:USERPROFILE\.ssh\id_ed25519" -o StrictHostKeyChecking=no root@203.170.59.16 @"
cd /hjxz/hxd-api/lib
ls -lt hxd.jar.bak* | head -1 | awk '{print \$NF}' | xargs -I {} cp {} hxd.jar
/hjxz/hxd-api/bin/hxd-api restart
"@
```
