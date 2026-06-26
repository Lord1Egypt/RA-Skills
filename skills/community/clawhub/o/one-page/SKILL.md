---
name: ultimate-horizontal-timeline-architect
description: >-
  当用户要求生成“向上汇报”、“项目一页纸”时触发。
  该技能具备动态提炼模块主题、同色系关键字高亮能力。核心特性：当识别到包含时间节点、里程碑或阶段性计划的内容时，自动将其渲染为现代感十足的【水平时间轴 (Horizontal Timeline)】UI，提供清晰的横向进度视觉。
---

# 核心动作
严格执行以下3个步骤。优先保证信息的逻辑连贯性、准确性以及视觉风格的还原度。

## Step 1: 动态场景识别与逻辑分块 (Dynamic Context & Segmentation)
根据文本内容，**动态划分出 4 到 6 个核心逻辑模块**。
对于每一个模块，提炼：[动态模块标题]、[动态标签]、子模块详情、模块总结。

## Step 2: 语言清洗与同色系关键字高亮 (Language & Highlight)
- **去口语化**：提炼为专业的书面语言。
- **动态色值匹配**：在正文中识别核心业务名词、数据指标，并使用与该模块主题色对应的 HTML 标签进行高亮包裹（如模块为绿色，则关键字高亮必须带绿色背景与文字）。

## Step 3: 视觉渲染与形态切换 (Adaptive Layout & Horizontal Timeline)
将处理后的内容代入下方 HTML 模板。

**🔥🔥 形态切换规则（UI 变体）🔥🔥：**
1. **默认列表态**：对于常规的描述性内容，使用 `<ul><li>` 结构。
2. **水平时间线态 (Horizontal Timeline)**：当你判断某个模块（如“落地计划”、“里程碑”、“排期”）包含明确的**时间节点、日期或先后步骤**时，**禁止使用 `<ul>` 列表**。你必须使用如下的**水平时间轴 HTML 结构**进行渲染，并将圆点与连线的颜色与当前模块主题色对齐。

**输出模板（横向时间轴增强版）：**
```html
<div style="background-color: #FFFFFF; padding: 24px 30px; border-radius: 16px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #333; max-width: 900px; margin: 15px auto; box-shadow: 0 10px 40px rgba(0,0,0,0.06); border: 1px solid rgba(0,0,0,0.04);">

  <div style="border-bottom: 2px solid #EEE; padding-bottom: 15px; margin-bottom: 18px;">
    <h1 style="font-size: 26px; font-weight: 700; margin: 0 0 6px 0; color: #111; letter-spacing: -0.5px;">[提取的全盘主题]</h1>
    <p style="font-size: 14px; color: #666; margin: 0; font-weight: 400;">[核心目标或会议定性语句]</p>
  </div>

  <div style="background-color: #F7F5FC; padding: 16px 20px; border-radius: 10px; margin-bottom: 15px; border-left: 4px solid #6C5CE7;">
    <h2 style="font-size: 17px; font-weight: 600; color: #6C5CE7; margin: 0 0 12px 0; display: flex; align-items: center;"><span style="background: rgba(108, 92, 231, 0.1); color: #6C5CE7; padding: 3px 8px; border-radius: 4px; font-weight: 700; font-size: 14px; margin-right: 10px;">01</span>[动态模块1标题]<span style="font-size: 11px; color: #999; margin-left: auto; font-weight: normal;">/[动态标签1]/</span></h2>
    <div style="display: flex; gap: 12px;">
      <div style="flex: 1; background: #FFF; border-radius: 6px; padding: 12px 15px; border: 1px solid #EEE;">
        <h3 style="font-size: 13px; color: #333; margin: 0 0 8px 0;">[子模块标题] <span style="background: rgba(108, 92, 231, 0.08); color: #6C5CE7; padding: 2px 6px; border-radius: 4px; font-weight: 600; font-size: 11px; float: right;">[状态]</span></h3>
        <ul style="font-size: 12px; color: #555; margin: 0; padding-left: 16px; line-height: 1.6;">
          <li>[详细描述，包含<strong style="color: #6C5CE7; font-weight: 700; background: rgba(108, 92, 231, 0.08); padding: 1px 5px; border-radius: 4px; margin: 0 2px;">紫色关键字</strong>]</li>
        </ul>
      </div>
    </div>
  </div>

  <div style="background-color: #F8FCF9; padding: 16px 20px; border-radius: 10px; margin-bottom: 15px; border-left: 4px solid #27AE60;">
    <h2 style="font-size: 17px; font-weight: 600; color: #27AE60; margin: 0 0 12px 0; display: flex; align-items: center;"><span style="background: rgba(39, 174, 96, 0.1); color: #27AE60; padding: 3px 8px; border-radius: 4px; font-weight: 700; font-size: 14px; margin-right: 10px;">02</span>[生产环境落地计划 / 进度追踪]<span style="font-size: 11px; color: #999; margin-left: auto; font-weight: normal;">/排期/</span></h2>
    
    <div style="position: relative; padding-top: 10px;">
      <div style="position: absolute; top: 15px; left: 5px; right: 5px; height: 2px; background-color: rgba(39, 174, 96, 0.2); z-index: 1;"></div>
      
      <div style="display: flex; gap: 20px; overflow-x: auto; position: relative; z-index: 2; padding-bottom: 5px;">
        
        <div style="flex: 1; min-width: 160px;">
          <div style="width: 10px; height: 10px; background-color: #27AE60; border-radius: 50%; border: 2px solid #FFF; box-shadow: 0 0 0 1px rgba(39,174,96,0.3); margin-bottom: 12px;"></div>
          <div style="font-size: 13px; font-weight: 600; color: #27AE60; margin-bottom: 6px;">[本周三 14:00] <span style="background: rgba(39, 174, 96, 0.08); color: #27AE60; padding: 1px 6px; border-radius: 4px; font-weight: 600; font-size: 10px; margin-left: 4px;">[已完成]</span></div>
          <div style="font-size: 12px; color: #555; line-height: 1.6;">
            [完成对接配置，包含<strong style="color: #27AE60; font-weight: 700; background: rgba(39, 174, 96, 0.08); padding: 1px 5px; border-radius: 4px; margin: 0 2px;">绿色关键字</strong>]
          </div>
        </div>

        <div style="flex: 1; min-width: 160px;">
          <div style="width: 10px; height: 10px; background-color: #27AE60; border-radius: 50%; border: 2px solid #FFF; box-shadow: 0 0 0 1px rgba(39,174,96,0.3); margin-bottom: 12px;"></div>
          <div style="font-size: 13px; font-weight: 600; color: #27AE60; margin-bottom: 6px;">[下周上线前] <span style="background: rgba(39, 174, 96, 0.08); color: #27AE60; padding: 1px 6px; border-radius: 4px; font-weight: 600; font-size: 10px; margin-left: 4px;">[进行中]</span></div>
          <div style="font-size: 12px; color: #555; line-height: 1.6;">
            [独立API Key分配，包含<strong style="color: #27AE60; font-weight: 700; background: rgba(39, 174, 96, 0.08); padding: 1px 5px; border-radius: 4px; margin: 0 2px;">绿色关键字</strong>]
          </div>
        </div>

        </div>
    </div>
  </div>

  <div style="background-color: #FFFDF9; padding: 16px 20px; border-radius: 10px; margin-bottom: 5px; border-left: 4px solid #E67E22;">
    <h2 style="font-size: 17px; font-weight: 600; color: #E67E22; margin: 0 0 10px 0; display: flex; align-items: center;"><span style="background: rgba(230, 126, 34, 0.1); color: #E67E22; padding: 3px 8px; border-radius: 4px; font-weight: 700; font-size: 14px; margin-right: 10px;">End</span>核心洞察与下一步<span style="font-size: 11px; color: #999; margin-left: auto; font-weight: normal;">/总结/</span></h2>
    <div style="background-color: #FFF; border-radius: 6px; padding: 12px 15px; border: 1px solid rgba(230, 126, 34, 0.15); font-size: 12px; color: #D35400; line-height: 1.6; font-weight: 500;">
      [提炼的一条核心结论，包含<strong style="color: #D35400; font-weight: 700; background: rgba(211, 84, 0, 0.08); padding: 1px 5px; border-radius: 4px; margin: 0 2px;">深橙色关键字</strong>]
    </div>
  </div>

</div>
