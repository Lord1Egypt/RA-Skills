# pokerclip

自动将长篇扑克比赛视频切割成完整手牌短视频，输出9:16竖屏格式，适合TikTok / YouTube Shorts。

## 功能
- 自动识别每手牌的开始和结束（基于德州扑克手牌结构）
- 完整保留横屏画面（letterbox，黑边上下）
- 自动生成悬念Hook文案叠加在顶部
- 精准字幕固定在底部黑区
- 取最精彩的Top 5手牌输出

## 环境要求
- Python 3.10+
- ffmpeg（需在PATH中）
- `pip install openai-whisper`
- GPU推荐（RTX系列，CPU也可跑但较慢）

## 使用方法

### 通过OpenClaw调用
```
用pokerclip处理这个视频：downloads/xxx.mp4
```

### 手动运行
```bash
# 1. 放视频到 downloads/
# 2. 主流程（转录+检测+切割）
python skills/pokerclip/scripts/poker_clipper.py "downloads/视频名.mp4"
# 3. 生成Hook
python skills/pokerclip/scripts/gen_hooks.py
# 4. 叠加Hook到视频
python skills/pokerclip/scripts/patch_hooks.py
# 5. 查看结果
# clips/ 目录下即为输出
```

## 输出格式
- 分辨率：1080x1920（9:16）
- 编码：H.264 + AAC
- 字幕：ASS格式内嵌，底部固定位置
- Hook：顶部黑区，前3秒显示

## 校准
如果某个clip切割不准确，告诉AI助手：
> "clip X 的第Y分Z秒开始是新的一手牌"

AI会自动找到对应转录词并修正切割逻辑。
