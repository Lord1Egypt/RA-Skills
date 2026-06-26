---
name: idea-memos
description: 小龙虾备忘录 — 记录即时想法，让 AI 更好辅助创作
---

# 硅虾备忘录 🦐

轻量级的本地备忘录系统，基于 Node.js + SQLite，提供 Web 管理界面和 CLI 操作。

## 功能

- 📝 添加备忘录（标题 + 内容 + 标签）
- 🗑️ 删除备忘录
- 🏷️ 标签分类
- 🔍 全文搜索
- 🌐 Web 管理界面（http://localhost:8080）
- ⚡ nginx 反向代理
- 🖥️ CLI 命令行操作

## 安装

```bash
# 1. 安装依赖
cd scripts && npm install

# 2. 启动服务
bash scripts/memos.sh start

# 3. 配置 nginx（可选）
cp memos.nginx.conf /etc/nginx/sites-available/memos
ln -sf /etc/nginx/sites-available/memos /etc/nginx/sites-enabled/
systemctl reload nginx
```

## 使用

### Web 界面
打开 http://localhost:8080

### CLI
```bash
node scripts/memo.js list           # 查看所有
node scripts/memo.js add -t 标题 -c 内容 -g 标签1,标签2   # 添加
node scripts/memo.js rm <id>        # 删除
node scripts/memo.js search <关键词> # 搜索
```

### API
```bash
GET    /api/memos          # 获取列表
POST   /api/memos          # 创建
PUT    /api/memos/:id      # 更新
DELETE /api/memos/:id      # 删除
```

## 管理

```bash
bash scripts/memos.sh start    # 启动
bash scripts/memos.sh stop     # 停止
bash scripts/memos.sh restart  # 重启
bash scripts/memos.sh status   # 状态
```

## 数据

数据存储在 `scripts/memos.db`（SQLite），安全可靠。
