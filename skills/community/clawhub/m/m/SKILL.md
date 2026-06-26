---
name: m
description: Short alias skill for moving files, directories, or data; also for system management like managing services or packages. Use when relocating or reorganizing content.
---

# m（Move 简写）

这是一个快速"移动/管理" Skill，用字母 **m** 触发。用于文件移动、目录重构，以及系统包和服务的操作。

---

## 适用场景

当你说：
- "移动文件到其他目录"
- "重命名文件"
- "迁移项目"
- "安装/卸载软件"
- "管理服务"
- "reorganize files"

---

## 文件移动

**基础mv**
```bash
mv old.txt new.txt              # 重命名
mv file.txt /path/to/dir/       # 移动到目录
mv *.tmp /trash/                # 移动所有tmp文件
mv -i file.txt backup/          # 交互模式（覆盖前确认）
mv -n file.txt backup/          # 不覆盖已存在
mv -v file.txt backup/          # 显示操作详情
```

**批量移动**
```bash
# 按扩展名移动到子目录
mkdir -p backup && mv *.log backup/

# 移动并保留目录结构
find . -name "*.tmp" -exec mv {} tmp_files/ \;

# 移动并排除某些文件
rsync -av --exclude='*.log' source/ dest/
```

**跨设备移动**
```bash
# mv 原地操作，无法跨设备
# 跨设备需要用cp+rm，或rsync
rsync -avh source/ /mnt/other_disk/backup/
rm -r source/  # 确认后再删
```

---

## 目录重构

```bash
# 创建目录并移动
mkdir -p archives/2025 && mv *.log archives/2025/

# 移动目录自身
mv project /opt/projects/

# 批量创建并移动
for dir in */; do
  mkdir -p "archive/$(date +%Y%m)/$dir"
  mv "$dir" "archive/$(date +%Y%m)/"
done
```

---

## 包管理（m = Manage）

**npm (Node.js)**
```bash
npm install express            # 安装包
npm uninstall lodash          # 卸载包
npm update                    # 更新所有
npm outdated                  # 检查过时
npm audit fix                 # 修复漏洞
npm ci                        # 根据package-lock安装（CI环境）
```

**pip (Python)**
```bash
pip install django            # 安装
pip uninstall numpy           # 卸载
pip list --outdated           # 列出过时
pip freeze > requirements.txt # 导出依赖
pip install -r requirements.txt  # 批量安装
pip check                    # 检查依赖冲突
```

**apt (Ubuntu/Debian)**
```bash
sudo apt update               # 更新索引
sudo apt install nginx        # 安装
sudo apt remove nginx         # 卸载（保留配置）
sudo apt purge nginx          # 完全卸载（含配置）
sudo apt upgrade              # 升级所有
sudo apt autoremove           # 清理无用依赖
```

**yum/dnf (CentOS/RHEL/Fedora)**
```bash
sudo dnf install nodejs       # 安装
sudo dnf remove mysql-server  # 卸载
sudo dnf upgrade              # 升级
sudo dnf autoremove           # 清理
```

**brew (macOS)**
```bash
brew install wget             # 安装
brew uninstall --ignore-dependencies wget  # 卸载
brew upgrade                  # 升级所有
brew cleanup                  # 清理旧版本
brew doctor                   # 健康检查
brew list --versions          # 查看版本
```

**chocolatey (Windows)**
```powershell
choco install git              # 安装
choco uninstall nodejs        # 卸载
choco upgrade all             # 升级所有
choco list --local-only       # 已安装列表
```

---

## 服务管理

**systemd (Linux)**
```bash
sudo systemctl start nginx              # 启动
sudo systemctl stop nginx               # 停止
sudo systemctl restart nginx            # 重启
sudo systemctl reload nginx             # 重载配置（不中断）
sudo systemctl enable nginx             # 开机自启
sudo systemctl disable nginx            # 禁用自启
sudo systemctl status nginx             # 查看状态
sudo systemctl is-active nginx          # 是否运行
sudo systemctl is-enabled nginx         # 是否启用
```

**macOS launchd**
```bash
launchctl list                          # 列出服务
launchctl start /Library/LaunchDaemons/com.example.plist
launchctl stop com.example.service
launchctl unload ~/Library/LaunchAgents/com.example.plist
```

**Windows Service (PowerShell)**
```powershell
Start-Service -Name "Spooler"          # 启动
Stop-Service -Name "Spooler"           # 停止
Restart-Service -Name "W3SVC"          # 重启
Get-Service | Where {$_.Status -eq "Running"}  # 运行中的服务
Set-Service -Name "Spooler" -StartupType Automatic  # 设置自动
```

---

## 数据迁移

**数据库**
```bash
# 备份+恢复
mysqldump -u root -p db > backup.sql
mysql -u root -p new_db < backup.sql

# MongoDB
mongodump --archive > backup.gz
mongorestore --archive < backup.gz

# PostgreSQL
pg_dump db > backup.sql
psql new_db < backup.sql
```

**容器数据**
```bash
docker cp container:/app/data ./local_backup/
docker volumes ls  # 查看卷
docker run --rm -v source:/data -v dest:/backup alpine \
  cp -r /data /backup/
```

---

## 版本迁移

**Git分支移动**
```bash
git branch -m old-name new-name  # 重命名分支
git branch -m branch new-branch # 当前分支重命名
git branch -m main master       # 主分支重命名
```

**标签移动**
```bash
git tag new_tag old_tag         # 复制标签
git tag -d old_tag             # 删除旧标签
git push origin :old_tag new_tag  # 更新远程
```

---

## 实用技巧

**原子移动（避免中断）**
```bash
# 重命名目录（原子操作）
mv temp_dir final_name  # 瞬间完成，用户无感知

# 增量更新（rsync比mv更安全）
rsync -av --delete source/ dest/
```

**移动前验证**
```bash
if [ -d "source" ]; then
  echo "Source exists"
  mv source dest/
else
  echo "Source not found"
fi
```

**跨平台移动脚本**
```bash
#!/usr/bin/env bash
# m 移动文件，支持通配符
src="$1"
dest="$2"

if [ -z "$src" ] || [ -z "$dest" ]; then
  echo "Usage: m <source> <destination>"
  exit 1
fi

if [ ! -e "$src" ]; then
  echo "Error: $src does not exist"
  exit 1
fi

mv "$src" "$dest" && echo "Moved: $src -> $dest"
```

---

| 操作类型 | 推荐命令 | 替代方案 |
|----------|----------|----------|
| 文件移动 | mv | rsync（跨设备） |
| 目录移动 | mv -T | rsync -a |
| 包安装 | 各包管理器 | 手动编译 |
| 服务重启 | systemctl restart | kill + start |

---

> m 技能是组织和管理的主力。 mv 操作请三思：确认目标存在，确认空间足够，确认不会覆盖重要数据。
