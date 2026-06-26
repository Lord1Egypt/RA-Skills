# /novel learnings - 记忆系统

## 触发方式

```
/novel learnings add <内容>
/novel learnings list
/novel learnings check
```

或对话式：
```
把这段设定记下来
更新记忆
```

---

## 功能

管理 `.learnings/` 目录，记录角色、地点、情节、世界观等写作过程中的灵感，确保故事前后一致。

---

## 核心文件

```
<项目名>/
└── .learnings/
    ├── characters.md     # 角色新增设定/变化
    ├── locations.md     # 地点场景细节
    ├── plot.md          # 情节新增/转折
    ├── worldbuilding.md # 世界观补充
    └── notes.md         # 其他杂项
```

---

## 使用时机

### 1. track-init 后初始化

```bash
mkdir -p .learnings/
touch .learnings/{characters,locations,plot,worldbuilding,notes}.md
```

---

### 2. 写作中途用户注入新设定

用户提到新设定时，AI 自动追加到对应文件：

```
用户：这章主角有个妹妹，叫林朵，今年8岁
```

→ 自动追加到 `.learnings/characters.md`：
```
## 新增角色：林朵
- 关系：主角妹妹
- 年龄：8岁
- 性格：活泼可爱
- 首次出现：第X章
```

---

### 3. /novel write 前的强制读取

`/novel write` 执行前，必须读取 `.learnings/` 中与本章相关的条目，确保新设定不被遗忘。

---

### 4. 自动引用机制

写作时，如果本章涉及的角色/地点在 `.learnings/` 中有记录，自动引用最新版本：

```
📖 .learnings/characters.md 中的角色林朵：
- 关系：主角妹妹
- 年龄：8岁（首提第3章）
- 性格：活泼可爱

→ 写作时自动引用这些细节
```

---

## 输出格式

### learnings add

```
✅ 已记录到 .learnings/characters.md

## 新增角色：林朵
- 关系：主角妹妹
- 年龄：8岁
- 性格：活泼可爱
- 首次出现：第X章
```

### learnings list

```
📚 .learnings/ 记忆库

characters.md (4条)
  - 林朵 [新增]
  - 老管家 [更新]
locations.md (2条)
  - 明月楼 [新增]
plot.md (1条)
  - 伏笔揭晓点 [更新]
worldbuilding.md (0条)
notes.md (3条)
```

### learnings check

```
📖 写作前记忆检查

发现与本章相关的记忆：
- characters.md: 林朵（第3章新增）
- locations.md: 明月楼（第2章）

本章应引用：
- 林朵正在院子里浇花

✅ 检查通过
```
