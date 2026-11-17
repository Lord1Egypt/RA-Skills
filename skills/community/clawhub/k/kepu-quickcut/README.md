# kepu-quickcut 科普快剪

知识点 → 选叙事模板 → 出 **1080×1920 竖版科普短视频 MP4**。确定性渲染（画面 = `seek(t)` 纯函数），字永远不错、任何帧可精确复现、改哪改哪。

与 [creator-style-kit](https://github.com/threeaus/creator-style-kit) 互补：**它管版式皮肤，本包管叙事结构**——每个模板是一个 10 秒"怎么讲一个知识点"的完整叙事（幕次/节拍/镜头/点破句），主打中文知识垂类。

## 五个叙事模板（均已出过可用成片）

| 模板 | 文件 | 叙事结构 | 适合内容 | 样片 |
|---|---|---|---|---|
| 汉字演变 | `templates/hanzi-evolution.html` | 五幕：古文字形态依次生长→尾屏诗句点破 | 单字字源×诗词 | 《月·一个字的三千年》 |
| 时间线 | `templates/timeline.html` | 镜头沿横轴推进，节点点亮，大年份同步 | 编年史/技术演进 | 《AI 66 年》 |
| 白板手绘 | `templates/whiteboard.html` | A/B 火柴人对比→曲线柱图→红笔圈点破 | 二选一对比/方法论 | 《每天15分钟 vs 周末3小时》 |
| 水彩绘本 | `templates/storybook.html` | 分层错拍开场→主体变换→哲理点破 | 自然现象/温情知识 | 《月亮的脸》 |
| 机制机器 | `templates/machine.html` | 开场先亮骨架→小球沿管道流动、零件逐环点亮→反馈回路（可选）→尾屏点破 | 系统/机制/流程：Agent 工作流、RAG、数据流水线 | 《RAG 是怎么转起来的》 |

样例片源码：`examples/agent-demo.html`——同一模板的 Agent 填槽实例（开 `HAS_FEEDBACK` 演示 ③→② 闭环），只改填槽区即可生成新片。

## 快速开始

```bash
# 1. 抽帧自检（采 3-5 个关键帧目检，见 SKILL.md 工作流）
# 2. 渲染成片（零安装，约 45 秒）
node scripts/capture.js templates/timeline.html frames
python scripts/assemble.py frames out.mp4
```

环境：Playwright 缓存的 Chromium（capture.js 自动发现；无缓存时兜底系统 Chrome）+ Python opencv-python（自带 openh264）。

## 工作流与渲染铁律

见 [SKILL.md](SKILL.md)——五步工作流 + 叙事铁律 + 11 条踩坑换来的渲染铁律。核心原则：**模板引擎，不是自由生成**，只填槽不动架构。

## License

MIT。第三方组件：[rough.js](https://roughjs.com/) v4.6.6（MIT，见 THIRD-PARTY.md）。
