---
name: podcast-gen
description: "播客生成器 — 根据用户描述，通过搜索引擎抓取最新资讯，生成口语化播客脚本，根据脚本语义自动匹配最合适的讯飞TTS声音，合成时长3分钟内的MP3音频并发送。触发词：生成播客、播客、podcast、帮我做一段音频、做一期节目。"
---

# podcast-gen · 播客生成器

根据用户描述，自动检索信息 → 生成脚本 → 语义匹配声音 → 合成音频 → 发送文件。

## 依赖

本 skill 需要 **xfyun-tts** skill 已安装，且以下环境变量已配置（通过 `openclaw config set` 或系统环境变量注入）：

```
XFYUN_APP_ID
XFYUN_API_KEY
XFYUN_API_SECRET
```

---

## Step 1 — 信息检索

直接用 `web_fetch` 调用搜索引擎 URL 抓取资讯，无需额外 skill。

### 搜索 URL 模版

```
# 国内新闻/热点（近一天）
https://cn.bing.com/search?q={keyword}&ensearch=0&tbs=qdr:d

# 科技/AI（近一周）
https://cn.bing.com/search?q={keyword}+最新进展&ensearch=0&tbs=qdr:w

# 国际新闻
https://duckduckgo.com/html/?q={keyword}+news+today

# 备用
https://www.sogou.com/web?query={keyword}
```

抓取 1–2 个源，提取关键事实和数据点即可。若结果为空或全是广告，换备用引擎重试。

---

## Step 2 — 生成播客脚本

基于检索结果，生成口语化播客脚本。

### 字数控制

| 目标时长 | 字数范围 |
|---------|---------|
| ~2分钟  | 350–420字 |
| ~2.5分钟 | 450–520字 |
| ~3分钟  | 550–600字 |

**上限 600 字**（speed=48 约 2:40）

### 脚本规范

- 结构：开场白 → 主体（2–3个核心信息点）→ 结尾收场
- 口语化，短句优先，避免长难句
- **禁止**：括号舞台指示、Markdown 符号（`**`、`#`）、表情符号
- 数字/英文缩写写成易读形式（"GPT-4" → "GPT四"）
- 段落间可插入 `[p300]` 停顿标记（300ms）

---

## Step 3 — 根据脚本语义选择声音

以下为 xfyun-tts 完整声音列表（`python3 tts.py --list-voices` 输出，共53个）：

| VCN | 名称 | 性别 | 语言 | 场景 |
|-----|------|------|------|------|
| `x5_lingyuzhao_flow` | 聆玉昭 | 成年女 | 中文普通话 | 交互聊天 |
| `x5_lingxiaotang_flow` | 聆小糖 | 成年女 | 中文普通话 | 语音助手 |
| `x5_EnUs_Grant_flow` | Grant | 成年女 | 英文美式口音 | 交互聊天 |
| `x5_EnUs_Lila_flow` | Lila | 成年女 | 英文美式口音 | 交互聊天 |
| `x6_lingxiaoli_pro` | 聆小璃 | 成年女 | 中文普通话 | 交互聊天 |
| `x6_xiaoqiChat_pro` | 聆小琪 | 成年女 | 中文普通话 | 交互聊天 |
| `x6_lingfeiyi_pro` | 聆飞逸 | 成年男 | 中文普通话 | 交互聊天 |
| `x6_feizheChat_pro` | 聆飞哲 | 成年男 | 中文普通话 | 交互聊天 |
| `x6_lingxiaoyue_pro` | 聆小玥 | 成年女 | 中文普通话 | 交互聊天 |
| `x6_lingxiaoxuan_pro` | 聆小璇 | 成年女 | 中文普通话 | 交互聊天 |
| `x6_lingyuyan_pro` | 聆玉言 | 成年女 | 中文普通话 | 交互聊天 |
| `x6_pangbainan1_pro` | 旁白男声 | 成年男 | 中文普通话 | 旁白配音 |
| `x6_pangbainv1_pro` | 旁白女声 | 成年女 | 中文普通话 | 旁白配音 |
| `x6_lingfeihan_pro` | 聆飞瀚 | 成年男 | 中文普通话 | 纪录片 |
| `x6_lingfeihao_pro` | 聆飞皓 | 成年男 | 中文普通话 | 广告促销 |
| `x6_gufengpangbai_pro` | 古风旁白 | 成年男 | 中文普通话 | 旁白配音 |
| `x6_lingyuaner_pro` | 聆园儿 | 成年女 | 中文普通话 | 儿童绘本 |
| `x6_ganliannvxing_pro` | 干练女性 | 成年女 | 中文普通话 | 角色配音 |
| `x6_ruyadashu_pro` | 儒雅大叔 | 成年男 | 中文普通话 | 角色配音 |
| `x6_lingyufei_pro` | 聆玉菲 | 成年女 | 中文普通话 | 时政新闻 |
| `x6_lingxiaoshan_pro` | 聆小珊 | 成年女 | 中文普通话 | 时政新闻 |
| `x6_lingxiaoyun_pro` | 聆小芸 | 成年女 | 中文普通话 | 角色配音 |
| `x6_lingyouyou_pro` | 聆佑佑 | 童年女 | 中文普通话 | 交互聊天 |
| `x6_lingxiaoying_pro` | 聆小颖 | 成年女 | 中文普通话 | 交互聊天 |
| `x6_lingxiaozhen_pro` | 聆小瑱 | 成年女 | 中文普通话 | 直播带货 |
| `x6_lingfeibo_pro` | 聆飞博 | 成年男 | 中文普通话 | 时政新闻 |
| `x6_waiguodashu_pro` | 外国大叔 | 成年男 | 中文普通话（外国人说中文） | 角色配音 |
| `x6_gaolengnanshen_pro` | 高冷男神 | 成年男 | 中文普通话 | 角色配音 |
| `x6_dongmanshaonv_pro` | 动漫少女 | 成年女 | 中文普通话 | 动漫角色 |
| `x6_wennuancixingnansheng_mini` | 温暖磁性男声 | 成年男 | 中文普通话 | 角色配音 |
| `x6_xiaonaigoudidi_mini` | 小奶狗弟弟 | 成年男 | 中文普通话 | 角色配音 |
| `x6_shibingnvsheng_mini` | 士兵女声 | 成年女 | 中文普通话 | 角色配音 |
| `x6_kongbunvsheng_mini` | 恐怖女声 | 成年女 | 中文普通话 | 旁白配音_悬疑恐怖 |
| `x6_yulexinwennvsheng_mini` | 娱乐新闻女声 | 成年女 | 中文普通话 | 娱乐新闻 |
| `x6_wenrounansheng_mini` | 温柔男声 | 成年男 | 中文普通话 | 售后客服 |
| `x6_jingqudaolannvsheng_mini` | 景区导览女声 | 成年女 | 中文普通话 | 景区导览解说 |
| `x6_daqixuanchuanpiannansheng_mini` | 大气宣传片男声 | 成年男 | 中文普通话 | 广告宣传片 |
| `x6_cuishounvsheng_pro` | 催收女声 | 成年女 | 中文普通话 | 催收客服 |
| `x6_yingxiaonv_pro` | 营销女声 | 成年女 | 中文普通话 | 营销客服 |
| `x6_huanlemianbao_pro` | 海绵宝宝 | 童年男 | 中文普通话 | IP模仿 |
| `x6_xiangruiyingyu_pro` | 商务殷语 | 成年男 | 中文普通话 | IP模仿 |
| `x6_taiqiangnuannan_pro` | 台湾腔温柔男声 | 成年男 | 台湾话 | 台湾话 |
| `x6_wumeinv_pro` | 妩媚姐姐 | 成年女 | 中文普通话 | 角色配音 |
| `x6_lingbosong_pro` | 聆伯松 | 成年男 | 中文普通话 | 角色配音 |
| `x6_dudulibao_pro` | 少女可莉 | 童年女 | 中文普通话 | IP模仿 |
| `x6_huajidama_pro` | 滑稽大妈 | 成年女 | 中文普通话 | 角色配音 |
| `x6_huoposhaonian_pro` | 活泼少年 | 成年男 | 中文普通话 | 角色配音 |
| `x6_lingxiaoxue_pro` | 聆小雪 | 成年女 | 中文普通话 | 角色配音 |
| `x6_gufengxianv_mini` | 古风侠女 | 成年女 | 中文普通话 | 角色配音 |
| `x6_wuyediantai_mini` | 午夜电台 | 成年女 | 中文普通话 | 角色配音 |
| `x6_tiexinnanyou_mini` | 贴心男友 | 成年男 | 中文普通话 | 角色配音 |
| `x4_zijin_oral` | 子津 | 成年男 | 天津话 | 交互聊天 |
| `x4_ziyang_oral` | 子阳 | 成年男 | 东北话 | 交互聊天 |

### 语义匹配规则

根据脚本主题、语气、受众，从上表中选择场景最匹配的声音：

- **时政新闻 / 国际要闻** → `x6_lingfeibo_pro` 或 `x6_lingyufei_pro`（场景：时政新闻）
- **纪录片 / 军事 / 严肃叙事** → `x6_lingfeihan_pro`（场景：纪录片）
- **旁白 / 解说 / 财经** → `x6_pangbainan1_pro`（场景：旁白配音）
- **科技 / AI / 科学探索** → `x6_lingfeihan_pro` 或 `x6_pangbainan1_pro`
- **娱乐 / 综艺** → `x6_yulexinwennvsheng_mini`（场景：娱乐新闻）
- **广告 / 宣传片** → `x6_daqixuanchuanpiannansheng_mini`（场景：广告宣传片）
- **儿童故事 / 科普** → `x6_lingyuaner_pro`（场景：儿童绘本）
- **武侠 / 历史 / 古风** → `x6_gufengpangbai_pro`（场景：旁白配音，古朴厚重）
- **悬疑 / 恐怖** → `x6_kongbunvsheng_mini`（场景：悬疑恐怖）
- **生活 / 情感 / 故事** → `x5_lingyuzhao_flow`（通用，自然亲切）
- **英文为主** → `x5_EnUs_Lila_flow`（美式英语，温暖自然）
- **方言 / 趣味** → `x4_ziyang_oral`（东北话）或 `x4_zijin_oral`（天津话）
- **默认 / 通用** → `x5_lingyuzhao_flow`

---

## Step 4 — 合成音频

将脚本写入临时文件后调用 xfyun-tts：

```bash
# 1. 定义输出路径（使用系统临时目录 + 时间戳，跨平台兼容）
OUTDIR=$(mktemp -d)
OUTFILE="$OUTDIR/podcast_$(date +%Y%m%d_%H%M%S).mp3"
SCRIPTFILE="$OUTDIR/script.txt"

# 2. 写入脚本
cat > "$SCRIPTFILE" << 'SCRIPT'
<脚本内容>
SCRIPT

# 3. 定位 xfyun-tts 脚本（openclaw skills 安装目录）
TTS_SCRIPT=$(openclaw skills path xfyun-tts 2>/dev/null || find ~/.openclaw -name "tts.py" -path "*/xfyun-tts/*" 2>/dev/null | head -1)

# 4. 合成
python3 "$TTS_SCRIPT" \
  --voice <选定VCN> \
  --output "$OUTFILE" \
  --speed 48 \
  --volume 55 \
  --file "$SCRIPTFILE"

echo "$OUTFILE"
```

环境变量由 OpenClaw 自动注入（通过 `openclaw config set skills.entries.xfyun-tts.env.*`），无需硬编码。

---

## Step 5 — 发送给用户

```python
message(
  action="send",
  filePath="<OUTFILE 路径>",
  caption="🎙️ <标题> · <日期>\n🎤 声音：<声音名称>（<选择理由>）\n⏱️ 约 X 分钟\n📌 <一句话内容简介>"
)
```

发送后确认返回 `messageId` 存在，确保文件真正上传成功。

---

