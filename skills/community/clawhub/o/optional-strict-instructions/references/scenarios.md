# Detailed Scenarios for Optional Strict Instructions

This file provides concrete examples of how to apply the Optional Strict Instructions skill in various scenarios.

## Scenario 1: File Deletion with Explicit Method

### User Request
"Use sudo to delete /home/user/important.pdf"

### Step-by-Step Response

**Phase 1: Verification**
```
检查文件是否存在：
$ ls -la /home/user/important.pdf
```

**Phase 2: Option Presentation (如果存在)**
```
找到文件：/home/user/important.pdf (2.3MB, 属于user用户)

用户指定使用sudo删除。执行：
sudo rm -f "/home/user/important.pdf"
```

**Phase 3: Execution**
```
执行sudo命令：
$ sudo rm -f "/home/user/important.pdf"
```

**Phase 4: Handling Results**

**Case A: Success**
```
✅ 文件已使用sudo权限永久删除
```

**Case B: Authentication Required**
```
❌ sudo需要密码

请选择：
1. 提供sudo密码继续删除
2. 取消操作
```

**Case C: File Not Found**
```
❌ 文件不存在：/home/user/important.pdf

可能原因：
1. 路径错误
2. 文件已被删除
3. 文件名大小写问题
```

## Scenario 2: System Configuration Change

### User Request
"Edit /etc/nginx/nginx.conf to add gzip compression"

### Step-by-Step Response

**Phase 1: Verification**
```
检查文件：
$ ls -la /etc/nginx/nginx.conf
$ file /etc/nginx/nginx.conf
```

**Phase 2: Option Presentation**
```
找到系统配置文件：/etc/nginx/nginx.conf (requires root)

修改此文件可能影响网站服务。请选择：

1. sudo nano /etc/nginx/nginx.conf (交互式编辑)
2. sudo sed 添加gzip配置 (自动化添加)
3. 先备份再编辑 (推荐)
   sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup
4. 仅显示当前配置
5. 取消操作
```

**Phase 3: Execution Based on Choice**

**如果选择3 (备份后编辑)：**
```
1. 创建备份：
   sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup.$(date +%s)

2. 添加gzip配置：
   sudo sed -i '/http {/a\\    gzip on;\\n    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;' /etc/nginx/nginx.conf

3. 验证语法：
   sudo nginx -t
```

## Scenario 3: Package Installation

### User Request
"Install docker using apt"

### Step-by-Step Response

**Phase 1: Verification**
```
检查docker是否已安装：
$ which docker
$ docker --version 2>/dev/null

检查系统：
$ lsb_release -a
$ cat /etc/os-release
```

**Phase 2: Option Presentation**
```
安装docker需要sudo权限。请选择：

1. 标准安装 (推荐)
   sudo apt update && sudo apt install docker.io

2. 仅更新仓库
   sudo apt update

3. 检查可用版本
   apt-cache policy docker.io

4. 显示安装命令供手动执行
5. 取消安装
```

## Scenario 4: User Account Management

### User Request
"Create a new user named 'deploy'"

### Step-by-Step Response

**Phase 1: Verification**
```
检查用户是否已存在：
$ id deploy 2>/dev/null
$ grep ^deploy: /etc/passwd
```

**Phase 2: Option Presentation**
```
创建系统用户'deploy'需要sudo权限。请选择：

1. 交互式创建 (推荐)
   sudo adduser deploy

2. 非交互式创建
   sudo useradd -m -s /bin/bash deploy
   sudo passwd deploy

3. 创建带特定UID/GID的用户
   sudo useradd -m -u 1500 -g 1500 deploy

4. 仅检查是否可创建
5. 取消创建
```

## Scenario 5: Service Management

### User Request
"Restart the web server"

### Step-by-Step Response

**Phase 1: Verification**
```
确定web服务：
$ systemctl list-units --type=service | grep -i web
$ systemctl list-units --type=service | grep -i apache
$ systemctl list-units --type=service | grep -i nginx
```

**Phase 2: Option Presentation**
```
检测到web服务：nginx

管理服务需要sudo权限。请选择：

1. 重启nginx
   sudo systemctl restart nginx

2. 重新加载配置 (不中断连接)
   sudo systemctl reload nginx

3. 检查服务状态
   systemctl status nginx

4. 查看服务日志
   sudo journalctl -u nginx -n 20

5. 取消操作
```

## Scenario 6: Database Operation

### User Request
"Backup the MySQL database"

### Step-by-Step Response

**Phase 1: Verification**
```
检查MySQL状态：
$ systemctl status mysql
$ which mysqldump

检查数据库：
$ mysql -e "SHOW DATABASES;" 2>/dev/null
```

**Phase 2: Option Presentation**
```
数据库备份需要数据库凭据。请选择：

1. 备份所有数据库 (需要root密码)
   mysqldump --all-databases > backup-$(date +%Y%m%d).sql

2. 备份特定数据库 (需要数据库名和密码)
   mysqldump database_name > backup-database_name-$(date +%Y%m%d).sql

3. 仅显示数据库列表
4. 测试连接
5. 取消备份
```

## Common Response Templates

### Template 1: Simple Choice
```
[操作描述]
找到资源：[路径] ([详细信息])

选项：
1. [方法A - 详细说明]
2. [方法B - 详细说明]
3. [安全选项]
4. 取消

选择 (1-4):
```

### Template 2: Authentication Required
```
执行 [操作] 需要 [权限类型]

需要认证。请选择：
1. 提供密码继续
2. 改用其他方法
3. 取消操作
```

### Template 3: Resource Not Found
```
❌ 资源不存在：[路径]

可能原因：
1. 路径错误
2. 权限不足
3. 已被删除/移动

建议操作：
1. 检查路径拼写
2. 检查权限
3. 搜索类似文件
```

### Template 4: Operation Complete
```
✅ 操作完成

执行：[命令]
结果：[成功/失败详情]
位置：[如有变更]
下一步：[如有需要]
```

## Key Decision Points

### When to Ask vs When to Act
- **Ask**: Multiple valid methods exist, risk is high, user hasn't specified method
- **Act**: User specified exact method, operation is low-risk and unambiguous

### When to Stop vs When to Continue
- **Stop**: Authentication fails, permission denied, resource not found
- **Continue**: All checks pass, user has confirmed choice

### When to Offer Alternatives
- **Always**: When primary method fails or is unavailable
- **Sometimes**: When user might want different approach
- **Never**: When user explicitly said "only do X"