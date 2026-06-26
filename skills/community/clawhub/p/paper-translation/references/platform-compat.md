# 平台兼容性与踩坑经验

## LaTeX 公式兼容性

| 问题 | 解决方案 |
|------|---------|
| 腾讯文档不支持 `\bm{...}`（bm 宏包） | 全部替换为 `\boldsymbol{...}` |
| `\bold` / `\mathbold` 不兼容 | 统一到 `\boldsymbol` |
| 罕见宏包命令 | 避免使用，仅 `\mathbb{R}` 等标准宏安全 |

**强制流程**：翻译完成后执行 `grep -c '\\bm' file.md`，结果必须为 0。

## 图片跨平台兼容性

| 平台 | 支持 | 不支持 |
|------|------|--------|
| IMA 知识库 | ArXiv 外链 URL、base64 data URI | 本地相对路径（上传后失效） |
| 腾讯文档 | `upload_image` 返回的 image_id | HTTP/HTTPS 外链 |

**标准图片上传流程**：

```bash
# 1. 下载
curl -sL -o x{n}.png https://arxiv.org/html/<paper_id>/x{n}.png

# 2. 腾讯文档：上传拿 image_id
mcporter call tencent-docs upload_image --args '{"file_name":"x1.png","image_base64":"<base64>"}'

# 3. IMA：直接用外链
![Fig](https://arxiv.org/html/<paper_id>/x1.png)
```

**图片 404 排查**：下载后检查文件大小，多个文件大小完全相同通常为 404 垃圾响应，应删除。

## 图表插入位置

图/表插入在**所在章节标题之后、小节正文之前**（与原文顺序一致）。

- Figure 2 应放在 §3.4 章节入口，而非 §3.4.1 之后
- Table 1/2 放在章节标题后即可
- 避免图表打断论证链条

## 腾讯文档 API 踩坑

### 标题长度限制

`create_smartcanvas_by_mdx` 的 `title` 字段**限制 36 字符**（按字符数计算，非字节）。

超长报错：`business 400001: title length exceeds 36 characters`

### mcporter 传大参数

`mcporter call` **不支持 `--args-file`**。可靠写法：

```bash
# 先生成 JSON 文件
jq -n --arg title "$TITLE" --rawfile mdx "$FILE" --arg cf "markdown" \
  '{title:$title, mdx:$mdx, content_format:$cf}' > /tmp/args.json

# 再用 cat 传入
mcporter call tencent-docs create_smartcanvas_by_mdx --args "$(cat /tmp/args.json)"
```

### 授权流程

`setup.sh` 在 CodeBuddy 独立 shell 环境下后台进程会被回收。解决方案：绕开 setup.sh，用同步轮询获取 token：

1. `openssl rand -hex 8` 生成 code
2. 展示授权链接给用户
3. `curl` 同步轮询 token（每 10 秒一次，最多 3 分钟）
4. `mcporter config add` 注册 token

## IMA 知识库 API 踩坑

### add_knowledge 限流

短时间内多次调用返回 `code=220030`（表面"没有权限"，实际是限流）。

**解决方案**：sleep 15 秒后重试，已上传的 cos_key 仍有效，无需重新 create_media。

### 图片不支持直传

`create_media` 的 `media_type=9`（图片）返回 220030。图片只能嵌入 Markdown（base64 data URI 或外链 URL）。

## 翻译内容质量常见问题

| 问题 | 表现 | 预防 |
|------|------|------|
| 简称全称搞错 | TA=Target Attention 错写为 Transformer Aggregator | 首次出现标全称并核对原文 |
| 默认精简原文 | 完整论证压缩成摘要式描述 | 逐段翻译，不做默认精简 |
| 模型解读混入正文 | 评论和翻译混在一起 | 强制 `> **[译注]**：...` 引用块 |
| 事实性错误 | Kunlun 归属错写为百度（实际 Meta） | 元信息必须从原文/搜索确认 |
| PDF 截图文件名搞反 | table1.png 实际是 Table 2 | 保存后按内容核对文件名 |
