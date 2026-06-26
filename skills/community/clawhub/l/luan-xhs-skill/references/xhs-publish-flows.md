# XHS Publish Flows

本文件拆分并细化「发布链路」的操作步骤，供 `SKILL.md` 按需引用。

## 0. 总览

发布类型：
- 视频
- 图文
- 长文

三要素（发布前必须齐全）：
1. 封面
2. 标题
3. 正文

**当前已验证最稳的网页端发布路径：**
- 登录与鉴权：`creator.xiaohongshu.com/new/home`
- 发布入口：`creator.xiaohongshu.com/publish/publish`
- 成功确认：`creator.xiaohongshu.com/new/note-manager`

## 1. 图文发布（推荐默认）

### 1.1 已验证直发链路（优先）
1. 打开 `https://creator.xiaohongshu.com/new/home`，确认不是登录页。
2. 如页面出现“短信登录 / 发送验证码 / 收不到验证码”，先判断是否只是普通短信页。
3. 如页面出现“APP扫一扫登录 / 为保护账号安全 / 请使用已登录该账号的小红书APP扫码登录身份”，停止短信流程，直接改走 `scripts/xhs_login_qr.js`。
4. 普通短信页才继续使用 `scripts/xhs_login_sms.js`。
3. 进入 `https://creator.xiaohongshu.com/publish/publish`。
4. **主动点击「上传图文」**，不要假设默认 tab 正确。
5. 上传首图/多图；如果用户没有给图，先用 `scripts/xhs_make_text_cover.py` 生成兜底封面。
6. 等待标题框 `填写标题会有更多赞哦` 和正文编辑器 `.tiptap.ProseMirror` 出现。
7. 填写标题（建议 <=20 字）。
8. 填写正文。
9. 如需话题，优先通过 UI 选题；少量纯文本标签可放正文末尾。
10. 用户明确要求直发时点击「发布」；若只是预演，则停在发布前。
11. 在把正文写进编辑器前，先把字面量 `\n` 归一化成真实换行，避免正文里出现 `\n`。
12. 发布后进入「笔记管理」，确认目标标题已出现；**只有这一步成功，才算真正发布成功。**

### 1.2 脚本化直发（推荐）

优先使用脚本而非临时拼自动化：

```bash
# 1) 登录（任选其一）
node scripts/xhs_login_sms.js --phone 13xxxxxxxxx
# 如果平台切成强制扫码：
node scripts/xhs_login_qr.js

# 2) 直接发布图文（没有 --image 时会自动生成兜底封面）
node scripts/xhs_publish_with_saved_session.js \
  --title "标题" \
  --body "正文"
```

如需明确指定素材图：

```bash
node scripts/xhs_publish_with_saved_session.js \
  --title "标题" \
  --body "正文" \
  --image /path/to/cover.png
```

如只想演练到发布前，不真正发布：

```bash
node scripts/xhs_publish_with_saved_session.js \
  --title "标题" \
  --body "正文" \
  --dry-run
```

### 1.3 图文-文字配图（备用）
1. 进入「上传图文」。
2. 点击「文字配图」。
3. 输入封面大字报文案。
4. 点击「生成图片」。
5. 在模板页选择样式并点「下一步」。
6. 进入编辑页填写：标题、正文、话题/标签。
7. 校验三要素后停在发布按钮（或在用户明确授权时直接发布）。

### 1.4 图文半程预发（不发布）
满足以下条件即视为“半程预发完成”：
- 已完成封面生成（或上传）
- 已进入编辑页
- 已填写标题与正文
- 仅停在「发布」按钮可见处，未点击发布

## 2. 视频发布

### 2.1 已验证直发链路（优先）
1. 进入 `https://creator.xiaohongshu.com/publish/publish`。
2. 保持在「上传视频」页，直接使用 `input.upload-input` 上传视频文件。
3. **不要把“上传中”或仅出现文件名误判为完成。** 只有出现以下信号，才算真正进入视频编辑页：
   - `视频文件` / `重新上传`
   - `设置封面`
   - `填写标题会有更多赞哦` 输入框
   - `.tiptap.ProseMirror` 正文编辑器
   - 底部 `暂存离开 / 发布` 按钮区
4. 先填标题，再填正文。
5. 若发布按钮是灰的/disabled，优先检查标题和正文是否都已填写；这通常不是上传失败，而是字段未补齐。
6. 校验可见范围与设置。
7. 用户明确要求直发时点击「发布」；否则停在发布前。
8. 发布后进入「笔记管理」，确认标题出现。

### 2.2 推荐脚本

```bash
node scripts/xhs_publish_video.js \
  --video /path/to/video.mp4 \
  --title "标题" \
  --body "正文"
```

可见性参数：

```bash
--visibility public|private|mutual
```

### 2.3 常见失败判断
- 仍停在 `拖拽视频到此或点击上传`：说明还没进编辑页，不要误报发布失败。
- 底部有 `发布` 按钮但按钮灰掉：优先补齐标题和正文。
- 草稿箱看不到视频草稿：网页端草稿是本地浏览器草稿，不保证跨浏览器/跨会话可见。


## 3. 长文发布

1. 进入「写长文」。
2. 新建创作或导入链接。
3. 填写长文标题与正文结构。
4. 若用户目标是图文，避免误走长文链路。

## 4. 常见问题与处理

- 社区首页显示可浏览，但创作后台跳登录：以创作后台为准，重新登录。
- 短信登录脚本报 `QR_REQUIRED`：不是用户操作错了，是平台切成了强制扫码；直接改用 `scripts/xhs_login_qr.js`。
- 默认落在视频上传页：主动切「上传图文」。
- 标题超限：出现 `xx/20` 时立刻压缩。
- 只做了封面没填文案：必须补齐标题与正文。
- `published=true` 但不确定是否成功：进入「笔记管理」确认标题是否出现。
- 网页端详情扫码限制：评论优先在通知页处理，必要时改 App 端。
