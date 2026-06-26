# Poker Clipper Skill

## 用途
将长篇扑克比赛视频自动切割成完整手牌片段，转换为9:16竖屏格式，添加专业字幕和Hook文案，输出适合TikTok/YouTube Shorts的短视频。

## 调用方式
```
/poker-clipper [视频文件路径]
```
或直接说："帮我处理这个扑克视频" / "切割新视频"

## 核心脚本
| 脚本 | 作用 |
|------|------|
| `scripts/poker_clipper.py` | 主流程：转录→手牌检测→切割+字幕 |
| `scripts/gen_hooks.py` | 生成唯一Hook文案 |
| `scripts/patch_hooks.py` | 将Hook叠加到视频顶部黑区 |
| `scripts/fix_hooks.py` | 手动覆盖Hook（出现重复时用） |
| `scripts/analyze_hands.py` | 诊断：显示完整街道/结果时间线 |
| `scripts/check_overlap.py` | 诊断：显示clip时间范围和间隔 |
| `scripts/debug_signals.py` | 诊断：显示转录中出现的结束信号 |

## 标准工作流
```bash
# 1. 放视频到 downloads/
# 2. 运行主流程
python scripts/poker_clipper.py "downloads/视频名.mp4"
# 3. 生成Hook
python scripts/gen_hooks.py
# 4. 叠加Hook
python scripts/patch_hooks.py
# 5. 打开查看
explorer clips
```

## 手牌边界检测原理

### 德州扑克手牌结构（必须理解）
```
Pre-flop → Flop（3张公牌）→ Turn（第4张）→ River（第5张）→ 摊牌/结果
```
每手牌是一个**完整序列**。切割必须从手牌开始到底池归属确认。

### 检测逻辑
1. **扫描转录**，识别街道信号（Flop/Turn/River）和结果信号
2. **结果信号触发手牌结束**，下一手从这里之后开始
3. **20s窗口去重**：同一手牌结束时多个信号合并为一个
4. **评分**：按兴奋关键词密度打分，取Top N手
5. **短片段过滤**：<30s的片段自动丢弃

### 关键教训：哪些词不能做结束信号
- ❌ `flop`、`turn`、`river` — 这是街道词，出现在手牌**中间**
- ❌ `full house`、`four of a kind` — 解说在手牌进行中就会说
- ❌ `all in`、`shoves` — 行动词，不是结果
- ✅ 只有**底池归属**和**玩家离开**才是真正结束

## 结束信号库（HAND_END_SIGNALS）
持续维护，新信号随校准追加：

### 底池归属
- `wins the pot`, `wins the hand`, `takes the pot`, `takes it down`
- `scoops`, `ship it`, `well done`, `nice hand`, `good hand`
- `win a pot worth`, `going to win a pot`, `raked in`, `rakes in`
- `locked up`, `two thirds of the way to scooping`
- `wins a monster`, `wins a massive`, `round one goes to`

### 玩家弃牌/离场
- `eliminated`, `busted`, `knocked out`
- `ronnie's folded`, `going to the cage`
- `folded his hand`, `folds his hand`
- `and he folds`, `and she folds`

### 赛后评论（手牌已结束）
- `phil deserved that`, `show some class`, `you lose the whole lot`
- `shuts me up`, `shut me up`, `locked up at least`

## 画布参数（固定，勿改）
```
画布: 1080x1920（9:16竖屏）
视频区域: 1080x607，垂直居中（letterbox，完整保留横屏画面）
字幕区: SUB_Y=1383（底部黑区），44px字体
Hook区: HOOK_Y=328（顶部黑区），52px字体，前3秒显示
```

## 校准流程
当用户说"X分X秒开始是新的一手牌"：
1. 计算绝对时间：clip开始时间 + 用户报告的分秒
2. 运行 `check_clip5_boundary.py`（或临时脚本）查看该时间点前后转录
3. 找到解说中表示"上一手结束"的词
4. 将该词加入 `HAND_END_SIGNALS`
5. 重跑完整流程验证

## Hook生成原则
- 5个公式轮换（每clip用不同公式）：悬念gap / 反直觉 / 情绪触发 / 部分揭示 / 沉浸感
- `used_hooks` set防止重复
- 金额从转录中提取（>100的数字才算）
- Fallback池保证不重复

## 常见问题

**Q: 某手牌被切成两段**
→ 运行 `analyze_hands.py` 查看时间线，找中间误触发的结束信号，删掉它

**Q: 两手牌被合并成一段**
→ 找两手牌之间的转录词，加入 `HAND_END_SIGNALS`

**Q: Hook重复**
→ 运行 `fix_hooks.py` 手动赋值，然后运行 `patch_hooks.py`

**Q: 字幕位置不对**
→ 调整 `poker_clipper.py` 中的 `SUB_Y`（字幕）或 `HOOK_Y`（Hook）

**Q: Whisper识别错误导致信号丢失**
→ 在诊断脚本中扩大搜索范围，找到实际词汇加入信号库；或升级到 `large-v3` 模型（慢但准）

## 工作目录
```
C:\Users\user\.openclaw\workspace-poker\
├── downloads/     # 放输入视频
├── clips/         # 输出clip + 转录缓存 + JSON报告
└── scripts/       # 所有处理脚本
```
