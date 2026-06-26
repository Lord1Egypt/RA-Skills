# Learning Planner - 学习规划师

个人学习管理系统，帮助设定学习目标、制定计划、跟踪进度，并提供间隔重复复习功能。

## 快速开始

```bash
# 安装
cd ~/.openclaw/workspace/skills/learning-planner
pip install -e .

# 初始化数据库
learning data path

# 创建学习目标
learning goal create "Python 编程" --description "掌握 Python 编程语言"

# 创建子目标
learning goal create "Python 基础语法" --parent 1 --priority high
learning goal create "Python 面向对象" --parent 1 --priority high

# 查看目标树
learning goal tree

# 生成今日计划
learning plan today

# 创建复习卡片
learning card create "Python 列表推导式语法" --answer "[x for x in iterable if condition]" --tags python

# 今日复习
learning review today

# 学习统计
learning report stats
```

## 示例数据

```bash
# 创建技能树
learning goal create "Web 开发" --description "全栈 Web 开发技能"
learning goal create "前端开发" --parent 1 --priority high
learning goal create "后端开发" --parent 1 --priority high
learning goal create "HTML/CSS" --parent 2 --priority high
learning goal create "JavaScript" --parent 2 --priority high
learning goal create "Python Web" --parent 3 --priority high
learning goal create "数据库" --parent 3 --priority medium

# 添加学习资源
learning resource add "MDN Web Docs" --url https://developer.mozilla.org --type documentation --tags web
learning resource add "Python 官方教程" --url https://docs.python.org --type documentation --tags python

# 创建复习卡片
learning card create "HTTP 状态码 200 含义" --answer "请求成功" --tags web
learning card create "CSS 盒模型组成" --answer "content, padding, border, margin" --tags css
learning card create "Python 装饰器作用" --answer "在不修改原函数的情况下扩展功能" --tags python

# 开始学习
learning session start 1 --notes "学习 Python 基础"
# ... 学习结束后 ...
learning session stop 1
```

## 测试命令

```bash
# 测试目标管理
learning goal list
learning goal show 1
learning goal progress 1 --percent 50

# 测试计划
learning plan list
learning plan week

# 测试复习
learning card list
learning review stats

# 测试资源
learning resource list
learning resource search python

# 测试统计
learning session time --days 7
learning report stats
```
