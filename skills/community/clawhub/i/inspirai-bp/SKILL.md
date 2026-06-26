---
name: inspirai-bp
description: "最佳实践管理 - 记录验证通过的解决方案，跨项目复用，避免重复踩坑。Triggers: '最佳实践', 'best practice', '经验记录', '解决方案', '踩坑记录', 'bp capture', 'bp apply', 'bp search'."
version: 1.0.0
license: MIT
---

# inspirai-bp - 最佳实践管理

记录验证通过的解决方案，跨项目复用，避免重复踩坑。

## 数据目录

所有最佳实践存储在 `$HOME/.inspirai/best-practices/` 下：

```
$HOME/.inspirai/best-practices/
├── index.json              # 索引文件
├── wechat/
│   ├── scan-login.md
│   └── mini-auth.md
├── typescript/
│   └── strict-config.md
└── k8s/
    └── rolling-update.md
```

---

## bp capture - 记录最佳实践

交互式引导记录新的最佳实践。

### 使用方式

```
bp capture            # 开始交互式记录
```

### 执行步骤

#### Step 1: 初始化数据目录

```bash
BP_DIR="$HOME/.inspirai/best-practices"
INDEX_FILE="$BP_DIR/index.json"

mkdir -p "$BP_DIR"

# 如果 index.json 不存在，创建初始结构
if [ ! -f "$INDEX_FILE" ]; then
    echo '{"version":1,"practices":{}}' > "$INDEX_FILE"
fi
```

#### Step 2: 收集基本信息

使用 AskUserQuestion 依次询问：

**问题 1：标题**
```
请输入最佳实践的标题（简洁描述方案）：
示例：微信扫码登录方案、K8s 滚动更新配置
```

**问题 2：分类**

先读取现有分类：
```bash
cat "$INDEX_FILE" | jq -r '.practices[].category' | sort -u
```

```
请选择分类：
- wechat（已有 3 个实践）
- typescript（已有 2 个实践）
- k8s（已有 5 个实践）
- 新建分类...
```

**问题 3：标签**
```
请输入标签（用逗号分隔，用于搜索匹配）：
示例：登录, 扫码, OAuth, 微信
```

#### Step 3: 收集内容

依次引导填写：

**问题描述：**
```
请简述遇到的问题场景（1-3 句话）：
```

**解决方案：**
```
请描述解决方案的关键步骤（可以是编号列表）：
```

**关键代码（可选）：**
```
请粘贴关键代码片段（可选，直接回车跳过）：
```

**注意事项（可选）：**
```
有什么需要特别注意的坑吗？（可选，直接回车跳过）：
```

**相关链接（可选）：**
```
有参考文档链接吗？（可选，直接回车跳过）：
```

#### Step 4: 生成 ID 和文件

ID 生成规则：`{category}-{slug}`
- slug 从标题生成，取关键词，用连字符连接
- 示例：标题 "微信扫码登录方案" -> ID "wechat-scan-login"

```bash
CATEGORY="wechat"
SLUG="scan-login"
ID="${CATEGORY}-${SLUG}"
FILE_PATH="$BP_DIR/$CATEGORY/$SLUG.md"
DATE=$(date +%Y-%m-%d)

mkdir -p "$BP_DIR/$CATEGORY"
```

#### Step 5: 写入文档

生成 Markdown 文件：

```markdown
---
id: {id}
title: {title}
category: {category}
tags: [{tags}]
created: {date}
updated: {date}
---

## 问题

{problem}

## 解决方案

{solution}

## 关键代码

{code}

## 注意事项

{notes}

## 相关链接

{links}
```

#### Step 6: 更新索引

读取 `index.json`，添加新条目：

```json
{
  "practices": {
    "{id}": {
      "title": "{title}",
      "category": "{category}",
      "tags": ["{tag1}", "{tag2}"],
      "file": "{category}/{slug}.md",
      "created": "{date}",
      "updated": "{date}"
    }
  }
}
```

写回 `index.json`。

#### Step 7: 确认完成

```
已记录最佳实践：

ID: {id}
标题: {title}
分类: {category}
标签: {tags}
文件: {file_path}

使用 bp apply {id} 可随时查看和应用此实践
```

---

## bp apply - 应用最佳实践

读取指定的最佳实践，提供查看或应用选项。

### 使用方式

```
bp apply <id>         # 应用指定 ID 的实践
```

### 执行步骤

#### Step 1: 验证 ID 存在

```bash
BP_DIR="$HOME/.inspirai/best-practices"
INDEX_FILE="$BP_DIR/index.json"

# 读取 index.json，检查 practices[id] 是否存在
# 如果不存在，提示并退出
```

**ID 不存在时：**

```
未找到 ID 为 "xxx" 的最佳实践

使用 bp search <keyword> 搜索
或使用 bp list 浏览所有实践
```

#### Step 2: 读取实践文档

```bash
# 从 index.json 获取文件路径
FILE_PATH="$BP_DIR/{category}/{slug}.md"
cat "$FILE_PATH"
```

#### Step 3: 展示内容并提供选项

展示文档完整内容后，使用 AskUserQuestion 询问：

```
已加载「{title}」

请选择操作：
- 直接开始实现（根据方案步骤指导实现）
- 复制到项目文档（生成到 docs/references/{id}.md）
- 仅查看，稍后再说
```

#### Step 4: 执行用户选择

**直接开始实现：**
- 展示解决方案步骤
- 逐步引导用户实现

**复制到项目文档：**
```bash
mkdir -p docs/references
cp "$FILE_PATH" "docs/references/{id}.md"
echo "已复制到 docs/references/{id}.md"
```

**仅查看：**
- 结束，不做额外操作

---

## bp search - 搜索最佳实践

根据关键词在标题和标签中搜索匹配的最佳实践。

### 使用方式

```
bp search <keyword>           # 单关键词搜索
bp search <kw1> <kw2>         # 多关键词搜索（AND 逻辑）
```

### 执行步骤

#### Step 1: 检查数据目录

```bash
BP_DIR="$HOME/.inspirai/best-practices"
INDEX_FILE="$BP_DIR/index.json"

if [ ! -f "$INDEX_FILE" ]; then
    echo "尚未记录任何最佳实践。使用 bp capture 开始记录。"
    exit 0
fi
```

#### Step 2: 读取索引并搜索

读取 `index.json`，对每个实践检查：
1. 标题是否包含关键词
2. 标签数组是否包含关键词

匹配规则：
- 不区分大小写
- 多关键词时，所有关键词都需匹配（AND 逻辑）
- 按匹配度排序（标题匹配 > 标签匹配）

#### Step 3: 格式化输出

**找到匹配时：**

```
搜索 "微信 登录" - 找到 2 个匹配：

1. [wechat-scan-login] 微信扫码登录方案
   标签: 登录, 扫码, OAuth, 微信
   分类: wechat | 更新: 2026-01-28

2. [wechat-mini-auth] 小程序静默登录
   标签: 登录, 小程序, 微信
   分类: wechat | 更新: 2026-01-25

使用 bp apply <id> 查看详情并应用
```

**无匹配时：**

```
搜索 "xyz" - 未找到匹配

建议：
- 尝试更短或不同的关键词
- 使用 bp list 浏览所有分类
```

---

## bp list - 列出最佳实践

列出已记录的最佳实践，支持按分类筛选。

### 使用方式

```
bp list              # 显示分类统计
bp list <category>   # 列出指定分类下的实践
```

### 执行步骤

#### Step 1: 检查数据目录

```bash
BP_DIR="$HOME/.inspirai/best-practices"
INDEX_FILE="$BP_DIR/index.json"

if [ ! -f "$INDEX_FILE" ]; then
    echo "尚未记录任何最佳实践。使用 bp capture 开始记录。"
    exit 0
fi
```

#### Step 2: 读取索引

```bash
cat "$INDEX_FILE"
```

#### Step 3: 格式化输出

**无参数时 - 显示分类统计：**

```
最佳实践统计：

分类          数量
─────────────────
wechat        3
typescript    2
k8s           5
─────────────────
总计          10

使用 bp list <category> 查看具体分类
```

**带参数时 - 列出该分类下的实践：**

```
[wechat] 分类下的最佳实践：

ID                    标题                    更新时间
───────────────────────────────────────────────────────
wechat-scan-login     微信扫码登录方案        2026-01-28
wechat-mini-auth      小程序静默登录          2026-01-25
wechat-pay            微信支付集成            2026-01-20

使用 bp apply <id> 查看详情并应用
```

**分类不存在时：**

```
未找到分类 "xxx"

已有分类：wechat, typescript, k8s

使用 bp list 查看所有分类
```

---

## bp update - 更新最佳实践

加载已有实践，引导更新内容。

### 使用方式

```
bp update <id>        # 更新指定 ID 的实践
```

### 执行步骤

#### Step 1: 验证 ID 存在

```bash
BP_DIR="$HOME/.inspirai/best-practices"
INDEX_FILE="$BP_DIR/index.json"

# 读取 index.json，检查 practices[id] 是否存在
```

**ID 不存在时：**

```
未找到 ID 为 "xxx" 的最佳实践

使用 bp search <keyword> 搜索
或使用 bp list 浏览所有实践
```

#### Step 2: 读取现有内容

```bash
FILE_PATH="$BP_DIR/{category}/{slug}.md"
cat "$FILE_PATH"
```

展示当前内容给用户。

#### Step 3: 询问更新内容

```
当前内容已加载。请描述需要更新的内容：

你可以：
- 补充新的注意事项
- 更新解决方案步骤
- 添加代码片段
- 修正错误信息

请输入更新内容：
```

#### Step 4: 应用更新

根据用户描述，修改文档相应部分。

更新 frontmatter 中的 `updated` 字段：
```yaml
updated: {today}
```

#### Step 5: 更新索引

更新 `index.json` 中对应条目的 `updated` 字段。

#### Step 6: 确认完成

```
已更新「{title}」

更新时间: {date}
文件: {file_path}

使用 bp apply {id} 查看更新后的内容
```

---

## bp delete - 删除最佳实践

确认后删除指定的最佳实践。

### 使用方式

```
bp delete <id>        # 删除指定 ID 的实践
```

### 执行步骤

#### Step 1: 验证 ID 存在

```bash
BP_DIR="$HOME/.inspirai/best-practices"
INDEX_FILE="$BP_DIR/index.json"

# 读取 index.json，检查 practices[id] 是否存在
```

**ID 不存在时：**

```
未找到 ID 为 "xxx" 的最佳实践

使用 bp list 浏览所有实践
```

#### Step 2: 显示实践信息并确认

```
即将删除：

ID: {id}
标题: {title}
分类: {category}
创建时间: {created}

此操作不可恢复！确认删除吗？
- 确认删除
- 取消
```

#### Step 3: 执行删除

**用户确认后：**

```bash
# 删除文档文件
rm "$BP_DIR/{category}/{slug}.md"

# 检查分类目录是否为空，为空则删除
if [ -z "$(ls -A $BP_DIR/{category})" ]; then
    rmdir "$BP_DIR/{category}"
fi
```

从 `index.json` 中移除对应条目，写回文件。

#### Step 4: 确认完成

```
已删除「{title}」
```

**用户取消时：**

```
已取消删除操作
```
