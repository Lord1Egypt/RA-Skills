# 火一五创意生态 — 整合食谱

> v3.0 加入 huo15 创意生态后，huo15-img-prompt 不再是独立工具，而是「创意管线」的核心节点。
> 本文档列出和其他 huo15-openclaw-* 技能的串联用法。

## 火一五创意全家桶

| 技能 | 角色 |
|------|------|
| `huo15-openclaw-design-director` | 选设计方向（5 流派 × 20 哲学 → 3 方向反差对比） |
| `huo15-openclaw-brand-protocol` | 抓品牌规范（Ask/Search/Download/Verify/Codify） |
| `huo15-openclaw-frontend-design` | 高保真 Web UI 落地 + 设计 tokens |
| `huo15-openclaw-design-critique` | 5 维设计评审 + Keep/Fix/Quick Wins |
| **`huo15-img-prompt`** ⭐ | 文生图 + 文生视频 + 闭环迭代 |

---

## 食谱 1：从零到一做品牌 KV（key visual）

```
设计方向 → 品牌规范 → 出图 → 评审 → 落地
```

### Step 1: design-director 选方向

```
> 我要做一个茶饮品牌，希望有东方气质但又年轻
```

→ design-director 给 3 个反差对比方向（如：宋韵极简 / 国潮复古 / 禅意新中式）。

### Step 2: brand-protocol 沉淀品牌规范

选定"宋韵极简"后：

```
> 帮我把这个方向 codify 成 brand kit
```

→ brand-protocol 输出：colors / fonts / visual_keywords / forbidden 元素。

导入 huo15-img-prompt：

```bash
brand-protocol-output.json | brand_kit.py --import
# 或手动创建
brand_kit.py --create song_tea \
    --colors "#2C5F2D, #97BC62, #F7F4EA" \
    --fonts "Songti SC, Source Han Serif" \
    --keywords "宋韵, 极简, 留白, 文人画" \
    --forbidden "modern digital, neon, cyberpunk"
```

### Step 3: img-prompt 出 KV 图

```bash
# 用品牌套件 + 推荐预设
enhance_prompt.py "茶饮品牌主视觉, 一杯热茶, 远山" \
    -p "汉服写真+水墨" \
    --brand-kit song_tea \
    --polish        # Claude 智能润色

# 或闭环迭代到 7.5 分
auto_iterate.py "茶饮品牌主视觉" \
    -p "汉服写真+水墨" \
    --backend dalle \
    --target 7.5
```

### Step 4: design-critique 评审

```
> 用 design-critique 评审这套图
```

→ Keep/Fix/Quick Wins 三分类反馈。

### Step 5: frontend-design 落地

把出图作为 hero 图，调用 frontend-design 生成完整官网：

```
> 用 frontend-design 给这个茶饮品牌做落地页，hero 用上面这张 KV
```

→ 完整 HTML/CSS/JS 原型，沿用 brand kit 的 tokens。

---

## 食谱 2：自学习风格 + 角色一致性 + 视频短片

适合个人 IP / 自媒体内容创作。

### Step 1: style_learn 学习独有风格

收集你喜欢的 5-10 张图（自己拍的、收藏的、参考的）：

```bash
style_learn.py --name 我的小清新 \
    refs/morning_cafe.jpg \
    refs/sunset_seoul.jpg \
    refs/film_kodak.jpg \
    refs/window_light.jpg \
    refs/quiet_corner.jpg
```

→ Claude Vision 综合 5 张图共性 → 生成 learned preset `@我的小清新`。

### Step 2: character 创建固定角色

```bash
enhance_prompt.py "20 岁亚裔女孩, 长直发, 圆框眼镜, 米白毛衣" \
    -p "@我的小清新" \
    --character-sheet \
    --save-char 我的女主
```

### Step 3: storyboard 拆短片剧本

```bash
storyboard.py "女主在咖啡馆度过的下雨午后，从写信到收到回信" \
    -p "@我的小清新" \
    --scenes 6 \
    -m Midjourney \
    --video-model Sora \
    --output ./my_story
```

→ 6 个关键帧 + 5 个转场，每个都 prompt 完整可用。

### Step 4: 出图 + 出视频

```bash
# 关键帧用 Midjourney 出
for f in my_story/scene-*-t2i.txt; do
    cat $f | grep -A1 '## Positive' | tail -1
    # 喂给 MJ
done

# 转场用 Sora 出（关键帧作为首帧）
for f in my_story/transition-*.txt; do
    # 喂给 Sora i2v 模式
done

# 剪辑串联即得短片
```

### Step 5: 评审反馈

```bash
image_review.py my_story/renders/*.png --rank
```

不好的轮次让 auto_iterate 自动改。

---

## 食谱 3：电商商品图全套

### Step 1: brand_kit 沉淀品牌色

```bash
brand_kit.py --create my_brand \
    --colors "#FF6B35, #1A1A2E, #FAFAFA" \
    --keywords "清爽, 现代, 高级感"
```

### Step 2: 用变体测试找最优 prompt

```bash
enhance_prompt.py "无线耳机产品图, 白底, 30 度俯视" \
    -p 产品摄影 \
    --brand-kit my_brand \
    --variants 6 \
    --variant-axes mood,composition,lighting

# 出 6 张图后排名
image_review.py renders/variant-*.png --rank
```

### Step 3: 锁定最优 → 系列扩展

最优变体的 seed → 用作角色卡：

```bash
enhance_prompt.py "无线耳机产品图" \
    -p 产品摄影 \
    --brand-kit my_brand \
    --save-char earphone_main \
    --seed <最优 seed>

# 后续所有变体（不同角度、配件、场景）共用
enhance_prompt.py "无线耳机展示图，环境光" --char earphone_main
enhance_prompt.py "无线耳机加包装" --char earphone_main
enhance_prompt.py "无线耳机使用场景" --char earphone_main
```

### Step 4: 沉淀到 Obsidian

```bash
enhance_prompt.py "..." --char earphone_main --obsidian
```

→ 所有 recipe 写入 vault `图集/`，方便后续团队 review。

---

## 食谱 4：Claude Code 工作流（IDE 内调用）

注册 MCP server 到 `~/.claude/mcp.json`：

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

然后在 Claude Code 里：

```
> @huo15-img-prompt 帮我给落地页做一张 hero 图，主题是"AI 编程助手"，要科技感但温暖
```

Claude Code 会：
1. 调 `suggest_presets` 推荐 top-3
2. 调 `polish_prompt` 润色
3. 调 `enhance_prompt` 出 prompt
4. 你出图后调 `review_image` 五维评审
5. 不好让 Claude 改 prompt 重出（闭环）

---

## 食谱 5：和 huo15-openclaw-knowledge-base 联动

把 brand_kit + character_card + learned_preset 沉淀到 huo15 知识库：

```bash
# brand_kit 导出 → 入库
brand_kit.py --export song_tea | jq '.' > raw/song_tea_brand.json
# 然后用 knowledge-base 编译入 wiki

# character 导出 → 入库
character.py --export 我的女主 > raw/heroine.json
```

→ wiki 全局搜索时这些资产可被检索。

---

## 设计原则

1. **每个技能管自己一段**：design-director 选方向，img-prompt 出图，design-critique 评审
2. **数据格式互通**：brand_kit / character / learned_preset 都是标准 JSON，可在技能间传递
3. **Claude 是协调者**：用 Claude Code + MCP 让 Claude 自动选择合适的技能链路
4. **闭环优先**：每一步都有"评审 → 改 → 重做"的能力，不要单步走到底

## 反对的做法

❌ 把所有功能塞到一个技能里（违反"每个 skill 独立模块化"原则）
❌ 在 img-prompt 里复刻 design-director 的方向选择能力（重复造轮子）
❌ 不沉淀 brand_kit / character / learned_preset 到 ~/.huo15/（每次重新生成）
❌ 跳过评审直接发布（v2.5 的闭环迭代是免费的，不用白不用）

---

由 huo15-img-prompt v3.0 发布，后续随生态扩展持续更新。
