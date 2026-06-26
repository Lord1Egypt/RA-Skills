# 快速上手 — 三层级

> 30 秒 / 5 分钟 / 30 分钟，按你想投入的时间往下读。

## 0. 首次安装后先跑这个

```bash
python3 scripts/doctor.py --quick
```

会告诉你：

- 14 个脚本是否都能 import + 版本是否一致
- 哪些 API key 已配 / 缺哪些（按需）
- Obsidian vault 检测到没
- 持久化资产盘点（characters / sessions / brand_kits / learned_presets）

如果看到 `✗ ANTHROPIC_API_KEY 未设置（必填）`，先：

```bash
export ANTHROPIC_API_KEY=sk-ant-xxx     # 把 sk-ant-xxx 换成你的真实 key
# 或写到 ~/.zshrc / ~/.bashrc
```

---

## 30 秒：第一条命令

```bash
scripts/enhance_prompt.py "一只赛博朋克的猫" -p 赛博朋克 -m Midjourney
```

复制 `✅ 正向提示词` 那段，粘贴到 Midjourney/Discord，回车出图。

完了，就这么简单。

---

## 5 分钟：基础工作流

### Step 1: 选预设（不知道选哪个 → 让 Claude 推荐）

```bash
scripts/enhance_prompt.py "温柔治愈感的画面" --suggest
```

Claude 会从 88 预设里挑 top 3，附评分 + 适合场景。

### Step 2: 出图

```bash
# 基础（自己挑预设）
scripts/enhance_prompt.py "咖啡馆窗边的少女" -p 胶片摄影 -m Midjourney

# 混合两种风格（v3.0 特性）
scripts/enhance_prompt.py "持剑女侠" -p "赛博朋克+水墨" --mix 0.6 -m SDXL

# A/B 测试出 4 个变体（同 seed，不同 mood/composition）
scripts/enhance_prompt.py "夜晚街景" -p 电影感 --variants 4 -j > /tmp/variants.json
```

### Step 3: 保存常用资产

```bash
# 角色卡（跨调用保持一致）
scripts/enhance_prompt.py "银发机甲少女, twin tails, glowing visor" \
    -p 动漫 --character-sheet --save-char silver_mecha

# 后续直接用
scripts/enhance_prompt.py "在霓虹街头" --char silver_mecha
scripts/enhance_prompt.py "在花海中" --char silver_mecha
# → 自动锁 seed，三张图角色一致
```

### Step 4: 看预设示例图

```bash
scripts/enhance_prompt.py --examples 敦煌壁画
# 输出 5 平台搜索 URL（Lexica / Civitai / Pinterest / Google / Unsplash）
```

---

## 30 分钟：完整工作流

### A. 端到端品牌 KV（食谱 1）

```bash
# 1. 导入示例品牌套件
cat examples/brand_kit-song_tea.json | scripts/brand_kit.py --import

# 2. 用品牌套件 + 智能润色 + 闭环迭代
scripts/auto_iterate.py "宋韵茶饮品牌主视觉，一杯热茶，远山轮廓" \
    -p "汉服写真+水墨" \
    --backend dalle \
    --target 7.5 \
    --max-rounds 3
# → Claude Vision 五维评审，分数 < 7.5 自动改 prompt 重出
```

### B. 学习自己喜欢的风格

```bash
# 给 N 张参考图（你自己拍的、收藏的）
scripts/style_learn.py --name 我的小清新 \
    refs/morning_cafe.jpg \
    refs/sunset.jpg \
    refs/quiet_corner.jpg \
    refs/film_kodak.jpg

# 后续用 @ 前缀调用
scripts/enhance_prompt.py "猫咪坐在窗台" -p "@我的小清新"
```

### C. 短片故事板（v3.0 杀手 feature）

```bash
# 输入剧本 → Claude 拆 6 关键帧 + 5 个转场
scripts/storyboard.py < examples/storyboard-cat_rainy_night.txt \
    -p 电影感 --scenes 6 \
    -m Midjourney --video-model Sora \
    --output ./renders/cat_rainy_night
```

输出（在 `./renders/cat_rainy_night/`）：

- `storyboard.json` 完整数据
- `scene-{01-06}-t2i.txt` 6 个关键帧 T2I prompt
- `transition-{xx-to-yy}-t2v.txt` 5 个转场 T2V prompt
- `README.md` 可读总览

把 6 个 scene prompt 喂 Midjourney，5 个 transition prompt 喂 Sora，剪辑串联即得 ~30 秒短片。

### D. 在 IDE 里直接用（Claude Code / Cursor）

注册到 `~/.claude/mcp.json`：

```json
{
  "mcpServers": {
    "huo15-img-prompt": {
      "command": "python3",
      "args": ["/path/to/huo15-img-prompt/scripts/mcp_server.py"]
    }
  }
}
```

然后在 Claude Code：

```
> @huo15-img-prompt 帮我给落地页做 hero 图，主题是"AI 编程助手"，要科技感但温暖
```

Claude Code 会自动调链路：suggest_presets → polish_prompt → enhance_prompt → review_image。

### E. 本地 Web UI

```bash
python3 scripts/web_ui.py
# 自动开浏览器到 http://127.0.0.1:7155
```

可视化 88 预设、实时 prompt 预览、一键复制。

### F. 把 recipe 沉淀到 Obsidian

```bash
scripts/enhance_prompt.py "..." --obsidian
# 自动写入 ~/knowledge/huo15/图集/ 或 OBSIDIAN_VAULT 指定位置
# 含完整 frontmatter + 复现命令
```

---

## 常见问题

### Q1: 我没有 ANTHROPIC_API_KEY，能用吗？

可以。**80% 功能不依赖 Claude**：
- ✅ enhance_prompt（88 预设 / 五锁 / 混合 / variants / compact）
- ✅ enhance_video（视频提示词）
- ✅ reverse_prompt（参考图反解，metadata 模式）
- ✅ render_prompt（10 后端直出，需要对应后端的 key）
- ✅ safety_lint（红线检测，纯本地词典）
- ✅ character / brand_kit（持久化）
- ✅ web_ui / mcp_server

需要 ANTHROPIC_API_KEY 的：
- ❌ claude_polish（智能润色）
- ❌ image_review（VLM 评审）
- ❌ auto_iterate（闭环迭代）
- ❌ storyboard（剧本拆分）
- ❌ style_learn（风格学习）
- ❌ --suggest 推荐预设

### Q2: 我能在 Anaconda 环境里用吗？

可以，纯标准库，没有第三方依赖。任何 Python 3.8+ 环境都行。

### Q3: 哪些后端最值得配？

- **入门**：DALL-E 3（OPENAI_API_KEY，质量稳定，文字渲染好）
- **省钱**：本地 ComfyUI / SD WebUI（一次性下载模型，永久免费）
- **国产场景**：字节即梦（ARK_API_KEY，中文场景效果好）
- **快速试**：Replicate flux-schnell（REPLICATE_API_TOKEN，4 步出图）

### Q4: 14 个脚本太多，我从哪 3 个开始？

1. `enhance_prompt.py` — 这是核心，所有路径都从它开始
2. `doctor.py` — 出问题先跑这个
3. `web_ui.py` — 不想敲命令的时候用

剩下的按需：要出图 → render_prompt；要短片 → storyboard；要做品牌一致 → brand_kit。

### Q5: 出来的 prompt 太长，SDXL 会截断怎么办？

```bash
scripts/enhance_prompt.py "..." -m SDXL --compact
# 自动压缩到 CLIP 77 token 内
```

### Q6: 我之前的图想改一改，prompt 丢了

```bash
scripts/reverse_prompt.py 你的图.png
# 自动从 PNG metadata 提取 A1111/ComfyUI/NovelAI 三种格式的 prompt
```

如果图没 metadata：

```bash
scripts/reverse_prompt.py 你的图.png --vlm
# 输出标准 VLM 模板，复制给 GPT-4o / Claude Sonnet 4.5 / Gemini 即可
```

---

## 下一步

- 完整 88 预设：`scripts/enhance_prompt.py -l --with-examples`
- 食谱书：[RECIPES.md](RECIPES.md)
- 完整 CLI：每个脚本都有 `-h` / `--help`

有问题先跑 `doctor.py`，再到 [https://clawhub.ai/skills/huo15-img-prompt](https://clawhub.ai/skills/huo15-img-prompt) 看 issue。
