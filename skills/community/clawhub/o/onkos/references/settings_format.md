# 设定文件格式规范

## 目录
- [概览](#概览)
- [文件格式](#文件格式)
- [板块定义](#板块定义)
- [完整示例](#完整示例)
- [操作类型](#操作类型)
- [验证规则](#验证规则)

## 概览

设定文件是Markdown格式的结构化文档，用于一次性批量导入小说世界观设定到Onkos系统。支持导入角色、实体（势力/地点/物品）、关系、事实、伏笔和约束规则。

## 文件格式

- 格式: Markdown（UTF-8编码）
- 结构: `## 板块标题` 划分板块，`### 名称` 定义子项，`- 属性: 值` 定义属性
- 大小限制: 建议不超过5000行

## 板块定义

### 角色（## 角色 / ## 人物）

| 属性 | 别名 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| 角色 | 定位/role | string | 是 | protagonist/antagonist/mentor/sidekick/npc |
| 性格 | personality | string | 否 | 性格描述 |
| 说话风格 | speech_style | string | 否 | 语言风格 |
| 核心特质 | core_traits | string | 否 | 逗号分隔，如"勇气,正义,执着" |
| 禁止行为 | forbidden_actions | string | 否 | 逗号分隔，如"背叛朋友,临阵脱逃" |
| 背景 | 背景故事/background | string | 否 | 背景故事 |
| 恐惧 | fears | string | 否 | 逗号分隔 |
| 目标 | goals | string | 否 | 逗号分隔 |

```markdown
## 角色
### 李天
- 角色: protagonist
- 性格: 坚韧不拔重情重义
- 说话风格: 沉稳寡言
- 核心特质: 勇气,正义,执着
- 禁止行为: 背叛朋友,临阵脱逃
- 背景: 孤儿被昆仑派收养
- 恐惧: 失去亲人
```

### 实体（## 势力/地点/物品 / ## 世界设定）

| 属性 | 类型 | 必填 | 说明 |
|------|------|------|------|
| 类型 | type | 否 | faction/location/item/concept（默认concept） |
| 其他属性 | 自由键值对 | 否 | 存入properties |

```markdown
## 势力/地点/物品
### 昆仑派
- 类型: faction
### 天域
- 类型: location
### 天罡剑
- 类型: item
```

### 关系（## 关系）

格式: `来源 → 目标: 关系描述`（箭头支持 → 或 ->）

```markdown
## 关系
- 李天 → 昆仑派: 属于
- 墨渊 → 天剑宗: 曾是长老
- 昆仑派 → 天域: 位于
```

### 事实（## 事实）

格式: `实体.属性=值 (chapter:N, importance:X, valid_from:N, valid_until:N)`

括号内参数可选，chapter默认为0（创世设定），importance默认为permanent。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| chapter | int | 0 | 确立该事实的章节 |
| importance | string | permanent | permanent/arc-scoped/chapter-scoped |
| valid_from | int | chapter | 生效起始章节 |
| valid_until | int | 无 | 失效章节 |
| category | string | 自动推断 | character/world/item/event |

```markdown
## 事实
- 李天.境界=筑基初期 (chapter:1, importance:arc-scoped)
- 李天.门派=昆仑派 (chapter:0, importance:permanent)
- 天域异变.状态=开始 (chapter:1, importance:arc-scoped)
```

### 伏笔（## 伏笔）

格式: `描述 (chapter:N, priority:X, expected_resolve:N)`

括号内参数可选，chapter默认为0。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| chapter | int | 0 | 种埋章节 |
| priority | string | normal | high/normal/low |
| expected_resolve | int | 无 | 预期回收章节 |

```markdown
## 伏笔
- 天域异变的真正原因 (chapter:1, priority:high)
- 赵云的真实目的 (chapter:1)
- 天罡剑最终归属 (chapter:20, priority:high, expected_resolve:50)
```

### 约束规则（## 约束规则 / ## 约束）

约束规则存储在 `project_config.json` 的 `constraints` 字段中，创作章节时通过 `for-creation` 返回给智能体。

格式：`### 规则名称` + `- 键: 值`，每个约束是一个自由键值对的对象，自动附加 `name` 字段。

```markdown
## 约束规则
### 剧情偏移值增长率
- 增长范围: 每章2-5%
- 禁止: 跳跃式增长（如单章暴涨20-30%）

### 章节字数
- 范围: 2000-2500字

### 写作风格
- 风格: 太上布衣沙雕风
- 禁止: 文艺腔、矫情描写
- 参考作品: 最强反套路系统
```

解析后写入 `project_config.json`：
```json
"constraints": {
    "剧情偏移值增长率": {
        "name": "剧情偏移值增长率",
        "增长范围": "每章2-5%",
        "禁止": "跳跃式增长（如单章暴涨20-30%）"
    },
    "章节字数": {
        "name": "章节字数",
        "范围": "2000-2500字"
    },
    "写作风格": {
        "name": "写作风格",
        "风格": "太上布衣沙雕风",
        "禁止": "文艺腔、矫情描写",
        "参考作品": "最强反套路系统"
    }
}
```

- import: 添加约束规则（同名覆盖）
- update: 合并字段（已有约束保留未提及的字段，新字段覆盖）
- delete: 按规则名称删除

## 完整示例

```markdown
# 苍穹破 设定

## 角色
### 李天
- 角色: protagonist
- 性格: 坚韧不拔重情重义
- 说话风格: 沉稳寡言
- 核心特质: 勇气,正义,执着
- 禁止行为: 背叛朋友,临阵脱逃
- 背景: 孤儿被昆仑派收养
- 恐惧: 失去亲人

### 墨渊
- 角色: antagonist
- 性格: 阴险狡诈野心勃勃
- 说话风格: 冷嘲热讽
- 核心特质: 野心,残忍,城府
- 禁止行为: 放过敌人
- 背景: 天剑宗前长老

### 赵云
- 角色: mentor
- 性格: 温润如玉深藏不露
- 说话风格: 循循善诱

### 苏瑶
- 角色: sidekick
- 性格: 活泼开朗古灵精怪
- 说话风格: 俏皮活泼
- 核心特质: 机敏,善良,好奇

## 势力/地点/物品
### 昆仑派
- 类型: faction
### 天剑宗
- 类型: faction
### 天域
- 类型: location
### 昆仑山
- 类型: location
### 天罡剑
- 类型: item
### 天劫
- 类型: concept

## 关系
- 李天 → 昆仑派: 属于
- 墨渊 → 天剑宗: 曾是长老
- 昆仑派 → 天域: 位于
- 天剑宗 → 天域: 位于
- 李天 → 天罡剑: 命定持有

## 事实
- 李天.门派=昆仑派 (importance:permanent)
- 李天.境界=筑基初期 (chapter:1, importance:arc-scoped)
- 墨渊.身份=天剑宗前长老 (importance:permanent)
- 天劫.状态=即将降临 (importance:arc-scoped)

## 伏笔
- 天域异变的真正原因 (chapter:1, priority:high)
- 赵云的真实目的 (chapter:1, priority:high)
- 天罡剑最终归属 (chapter:20, priority:high, expected_resolve:50)

## 约束规则
### 剧情偏移值增长率
- 增长范围: 每章2-5%
- 禁止: 跳跃式增长（如单章暴涨20-30%）
### 章节字数
- 范围: 2000-2500字
### 写作风格
- 风格: 热血爽文
- 禁止: 文艺腔、慢热
```

## 操作类型

设定文件支持三种操作，使用同一Markdown格式，仅包含需要操作的条目即可：

### 导入(import)

创建新条目，角色/实体/关系/事实/伏笔全部写入系统。

```bash
# 命令行
python scripts/settings_importer.py --project-path ./my-novel --action import --path 设定.md
# 通过CommandExecutor
ce.execute("import-settings", {"path": "设定.md"})
```

### 更新(update)

更新已有条目。文件中只需包含要更新的条目和属性（未列出的属性保持不变）：
- 角色: 更新core_traits/speech_style/role等属性
- 实体: 更新type/properties
- 关系: 先删旧边再建新边（可更改关系描述）
- 事实: set_fact的upsert语义，自动supersede旧值
- 伏笔: 更新priority/expected_resolve

```bash
# 命令行
python scripts/settings_importer.py --project-path ./my-novel --action update --path 设定更新.md
# 通过CommandExecutor
ce.execute("update-settings", {"path": "设定更新.md"})
```

### 删除(delete)

删除匹配的条目。文件中只需包含条目的名称/描述即可匹配：
- 角色: 删除角色文件 + 知识图谱character节点
- 实体: 删除节点（级联删除关联边）
- 关系: 按source+target+relation匹配并删除边
- 事实: 按entity+attribute真删除
- 伏笔: 按description匹配open伏笔并abandon

```bash
# 命令行
python scripts/settings_importer.py --project-path ./my-novel --action delete --path 设定删除.md
# 通过CommandExecutor
ce.execute("delete-settings", {"path": "设定删除.md"})
```

### 预览(dry-run)

仅解析不执行，预览解析结果。可在import/update/delete前使用。

```bash
python scripts/settings_importer.py --project-path ./my-novel --action dry-run --path 设定.md
ce.execute("preview-settings", {"path": "设定.md"})
```

## 验证规则

1. 文件必须为UTF-8编码的Markdown格式
2. 板块标题（##）必须是已定义的关键词，未识别的板块将被跳过
3. 角色名称（###）不能为空
4. 关系行必须包含来源、目标和关系描述
5. 事实行必须包含实体.属性=值
6. 伏笔行必须包含描述
7. 重复导入同名角色/节点会覆盖已有数据
8. 事实导入遵循supersede机制，同实体同属性的旧事实会被标记为已替代
9. 约束规则按名称去重，同名约束导入时覆盖，更新时合并字段
