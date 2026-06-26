# EXTEND.md 配置 Schema

## 概述

EXTEND.md 是用户偏好设置文件，采用 Markdown 格式，使用 `## 区块名` 分隔各配置区块。

---

## 文件位置

按优先级从高到低：

| 路径 | 范围 |
|------|------|
| `.panda-skills/panda-knowledge-card/EXTEND.md` | 当前项目 |
| `${XDG_CONFIG_HOME:-$HOME/.config}/panda-skills/panda-knowledge-card/EXTEND.md` | XDG 用户目录 |
| `$HOME/.panda-skills/panda-knowledge-card/EXTEND.md` | 用户主目录 |

---

## 完整 Schema

### 设置

```markdown
## 设置
默认风格: auto
默认平台: xhs
默认输出目录: knowledge-cards
默认卡片数量: auto
水印: 关闭
水印内容: @my-account
水印位置: 右下角
语言: auto
```

| 字段 | 类型 | 默认值 | 可选值 |
|------|------|--------|--------|
| `默认风格` | string | `auto` | `auto`, `notion`, `study-notes`, `chalkboard`, `cute`, `bold`, `warm`, `vector-illustration`, `minimal`, `screen-print` |
| `默认平台` | string | `general` | `xhs`, `wechat`, `weibo`, `x`, `douyin`, `instagram`, `general` |
| `默认输出目录` | string | `knowledge-cards` | `knowledge-cards`, `same-dir`, `imgs-subdir` |
| `默认卡片数量` | string | `auto` | `auto`, 或具体数字（如 `5`） |
| `水印` | string | `关闭` | `关闭`, `开启` |
| `水印内容` | string | — | 水印文字 |
| `水印位置` | string | `右下角` | `右下角`, `左下角`, `右上角`, `左上角`, `底部居中` |
| `语言` | string | `auto` | `auto`, `zh`, `en`, `ja` 等 |

### 角色（可选）

```markdown
## 角色
角色图片: ~/.panda-skills/characters/my-avatar.png
角色名称: 小熊猫
角色风格: 可爱卡通
默认融合模式: 讲解者
```

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `角色图片` | string | — | 角色参考图路径 |
| `角色名称` | string | — | 角色名称 |
| `角色风格` | string | `可爱卡通` | `可爱卡通`, `Q版`, `简笔画`, `像素风`, `写实卡通` |
| `默认融合模式` | string | `讲解者` | `讲解者`, `点缀`, `无角色`, `auto` |

角色区块与 panda-article-illustrator 共享相同的格式和字段定义。

### 自定义配色（可选）

```markdown
## 自定义配色
主色: #3B82F6
辅色: #10B981
强调色: #F59E0B
背景色: #FAFAFA
```

---

## 完整示例

```markdown
## 设置
默认风格: notion
默认平台: xhs
默认输出目录: knowledge-cards
默认卡片数量: auto
水印: 开启
水印内容: @hash-panda
水印位置: 右下角
语言: zh

## 角色
角色图片: ~/.panda-skills/characters/panda-avatar.png
角色名称: 小熊猫
角色风格: 可爱卡通
默认融合模式: auto

## 自定义配色
主色: #3B82F6
辅色: #10B981
强调色: #F59E0B
背景色: #FAFAFA
```

---

## 解析规则

1. 以 `## ` 开头的行标识区块名称
2. 区块内每行格式为 `key: value`
3. 空行和非 `key: value` 格式的行被忽略
4. `~` 开头的路径展开为用户主目录
5. 项目级配置优先于用户级
