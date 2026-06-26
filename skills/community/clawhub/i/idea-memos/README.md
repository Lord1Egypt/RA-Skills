# 🦐 小龙虾备忘录 (idea-memos)

> **记录即时想法，让 AI 更好理解你的创作脉络**

## 这是什么？

一个轻量级的本地备忘录系统。当你和 AI（比如我 🦐）协作时，随时可以把闪现的想法、待办事项、灵感碎片记下来。

**为什么需要它？**
- 人的记忆是短暂的，一个好想法不记下来就没了
- AI 每次对话都是新的开始，有了备忘录，AI 能更快了解你的上下文
- 跨会话的知识沉淀 —— 今天记的备注，明天 AI 还能看到

## 功能

| 功能 | 说明 |
|------|------|
| 📝 添加备忘录 | 标题 + 内容 + 标签，随时记录 |
| 🗑️ 删除备忘录 | 不需要了就删掉 |
| 🏷️ 标签分类 | 按标签筛选，快速找到相关内容 |
| 🌐 Web 界面 | 浏览器打开就能用 |
| 🖥️ CLI 操作 | 终端也能管理 |
| ⚡ nginx 反向代理 | 生产级部署 |

## 快速部署

### 1. 安装依赖

```bash
cd scripts
npm install
```

### 2. 启动服务

```bash
bash scripts/memos.sh start
```

服务运行在 `http://localhost:3377`

### 3. 配置 nginx（可选）

```bash
sudo cp memos.nginx.conf /etc/nginx/sites-available/memos
sudo ln -sf /etc/nginx/sites-available/memos /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo systemctl reload nginx
```

然后访问 `http://localhost:8080`

### 4. 管理命令

```bash
bash scripts/memos.sh start    # 启动
bash scripts/memos.sh stop     # 停止
bash scripts/memos.sh restart  # 重启
bash scripts/memos.sh status   # 查看状态
```

## CLI 使用方法

```bash
# 查看所有备忘录
node scripts/memo.js list

# 添加备忘录
node scripts/memo.js add -t "标题" -c "内容" -g "标签1,标签2"

# 删除备忘录
node scripts/memo.js rm <id>

# 查看单条
node scripts/memo.js show <id>
```

## API

```bash
GET    /api/memos          # 获取列表
POST   /api/memos          # 创建（{title, content, tags}）
PUT    /api/memos/:id      # 更新
DELETE /api/memos/:id      # 删除
```

## 数据存储

数据存储在 `scripts/memos.db`（SQLite），安全可靠，随时可以备份迁移。

## 技术栈

- **后端:** Node.js + Express + SQLite
- **前端:** 原生 HTML/CSS/JS
- **反向代理:** nginx
- **数据库:** better-sqlite3

## License

MIT
