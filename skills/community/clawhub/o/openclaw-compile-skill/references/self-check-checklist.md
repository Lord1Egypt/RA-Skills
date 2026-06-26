# 自审清单

## 必跑脚本

```bash
bash {baseDir}/scripts/compile_check.sh \
  "$COMPILE_TRANSIT_DIR/目标文件.md" \
  --vault "$OPENCLAW_VAULT"
```

## 检查分组

### 1. Frontmatter
- type/status/source/author/original/created/compiled_by/tags/keywords/related_wiki
- `compiled_by` 必须带双引号
- `related_wiki` 必须存在，允许空数组 `[]`

### 2. YAML 格式
- frontmatter 首尾闭合
- 无注释残留
- 无非标准字段

### 3. 标题
- H1 与文件名一致
- 英文标题必须带中文副标题

### 4. 正文结构
- `## 概述`
- `对我们的直接价值`
- `## 局限与思考`
- `## 相关文档`
- `## 来源`

### 5. 原材料与图片
- 原材料存在
- 原材料 `compiled_version` 指向有效中转站
- 图片目录和链接有效

## 失败原则

- 任一项 FAIL：停止，不继续收尾
- 修完后重跑，直到 PASS
- 不允许自行解释为“误报”后继续
