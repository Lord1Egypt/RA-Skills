## 报告导出流程（一键导出，零技术门槛）

### 核心原则：用户只需回复数字，其他全自动

**零技术门槛设计**：
- 用户不需要安装任何软件或依赖
- 用户不需要执行任何命令
- 用户不需要了解Markdown、HTML等技术细节
- 用户只需要回复数字（如"2"或"2,3"），等待3-5秒，文件自动生成

### 触发时机

当完成以下任一诊断输出后，自动触发报告导出询问：
- Skill1-Idea可行性研判完成
- Skill2-MVP精益设计完成
- Skill3-OPC合规落地完成
- Skill4-种子用户冷启动完成
- Skill5-规模化增长完成

### 导出流程（用户视角）

#### 步骤1：诊断完成，自动询问

```
---
📊 **一键导出报告**

诊断完成！是否需要导出文档？

回复数字即可：
• 回复 1 → 导出 Markdown（适合在线查看）
• 回复 2 → 导出 HTML（适合浏览器查看，可打印）
• 回复 1,2 → 全部导出

💡 提示：回复数字后，文件会自动生成到 opc-reports 文件夹

---

💬 **深入探讨**

你也可以继续和我探讨：
• "帮我详细设计[某个方案]"
• "这个阶段我该怎么做"
• "帮我分析[某个具体问题]"
• "我还有其他困惑..."
```

#### 步骤2：用户回复数字

```
用户：2
```

#### 步骤3：自动生成文件（用户等待3-5秒）

```
⏳ 正在生成文档...

✅ 导出成功！

📁 文件已保存到：opc-reports/2026-06-09/

📄 已生成文件：
• OPC智脑诊断报告_社区治理SaaS_2026-06-09.html（HTML文档）

💡 如何使用：
• HTML文档：双击打开，浏览器自动显示，可打印或详细阅读
```

### 导出流程（技术实现）

#### 自动化执行逻辑

用户回复数字后，智能体自动执行以下步骤（用户无感知）：

1. **解析用户选择**：将"2"解析为["html"]

2. **生成Markdown文件**（如果用户选择1）
   - 文件名：OPC智脑诊断报告_{项目名}_{日期}.md
   - 位置：opc-reports/{日期}/
   - 使用write工具直接生成

3. **生成HTML文档**（如果用户选择2）
   - 使用write工具直接生成.html文件
   - 基础格式：标题、段落、列表、表格
   - 无需安装任何依赖

4. **输出成功消息**
   - 告知用户文件位置
   - 提供使用提示

#### 文件生成策略

**策略1：直接生成（推荐）**
- 使用码道IDE的write工具直接生成文件
- 不依赖外部库或工具
- 速度最快，兼容性最好

**策略2：可视化优先（HTML核心优化）**
- HTML首屏采用**左右布局**：左侧条形图，右侧评分+概况
- - 首屏之后才是详细诊断内容
- 整体风格：橙色主色调(#e8792b)，专业简洁

**HTML可视化首屏结构（左右布局，必须放在报告最顶部，紧跟标题之后）**：

**⚠️ 必须使用以下HTML模板，禁止自由调整结构。仅替换{}占位符内容。**

```html
<!-- ====== 首屏仪表盘（禁止修改结构，仅替换{}占位符） ====== -->
<div style="margin-bottom:30px;">
  <!-- 上排：评分卡+条形图 -->
  <div style="display:flex;gap:24px;margin-bottom:20px;">
    <!-- 左：综合评分卡 -->
    <div style="flex:0 0 200px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:28px 20px;background:#fef9f3;border-radius:12px;border:1px solid #fde8cd;">
      <div style="font-size:56px;font-weight:900;color:{scoreColor};line-height:1;">{score}</div>
      <div style="font-size:14px;color:#888;margin-top:6px;margin-bottom:10px;">综合可行度</div>
      <span style="display:inline-block;padding:4px 14px;border-radius:20px;font-size:12px;font-weight:600;color:#fff;background:{scoreColor};">{level}</span>
      <span style="display:inline-block;padding:4px 14px;border-radius:20px;font-size:12px;font-weight:600;color:#fff;background:#e8792b;margin-top:6px;">{stage}</span>
    </div>
    <!-- 右：维度条形图 -->
    <div style="flex:1;display:flex;flex-direction:column;justify-content:center;padding:20px 28px;background:#fff;border-radius:12px;border:1px solid #f0f0f0;">
      <div style="margin-bottom:14px;font-size:14px;font-weight:700;color:#333;">五维度评分</div>
      <div style="display:flex;align-items:center;margin-bottom:10px;font-size:13px;">
        <span style="flex:0 0 80px;text-align:right;padding-right:12px;color:#666;">需求可行性</span>
        <div style="flex:1;height:20px;background:#f5f5f5;border-radius:10px;overflow:hidden;"><div style="height:100%;border-radius:10px;width:{v0}%;background:{c0};"></div></div>
        <span style="flex:0 0 36px;text-align:right;font-weight:700;font-size:14px;color:{c0};">{v0}</span>
      </div>
      <div style="display:flex;align-items:center;margin-bottom:10px;font-size:13px;">
        <span style="flex:0 0 80px;text-align:right;padding-right:12px;color:#666;">市场空间</span>
        <div style="flex:1;height:20px;background:#f5f5f5;border-radius:10px;overflow:hidden;"><div style="height:100%;border-radius:10px;width:{v1}%;background:{c1};"></div></div>
        <span style="flex:0 0 36px;text-align:right;font-weight:700;font-size:14px;color:{c1};">{v1}</span>
      </div>
      <div style="display:flex;align-items:center;margin-bottom:10px;font-size:13px;">
        <span style="flex:0 0 80px;text-align:right;padding-right:12px;color:#666;">个人匹配度</span>
        <div style="flex:1;height:20px;background:#f5f5f5;border-radius:10px;overflow:hidden;"><div style="height:100%;border-radius:10px;width:{v2}%;background:{c2};"></div></div>
        <span style="flex:0 0 36px;text-align:right;font-weight:700;font-size:14px;color:{c2};">{v2}</span>
      </div>
      <div style="display:flex;align-items:center;margin-bottom:10px;font-size:13px;">
        <span style="flex:0 0 80px;text-align:right;padding-right:12px;color:#666;">产品成熟度</span>
        <div style="flex:1;height:20px;background:#f5f5f5;border-radius:10px;overflow:hidden;"><div style="height:100%;border-radius:10px;width:{v3}%;background:{c3};"></div></div>
        <span style="flex:0 0 36px;text-align:right;font-weight:700;font-size:14px;color:{c3};">{v3}</span>
      </div>
      <div style="display:flex;align-items:center;font-size:13px;">
        <span style="flex:0 0 80px;text-align:right;padding-right:12px;color:#666;">合规就绪度</span>
        <div style="flex:1;height:20px;background:#f5f5f5;border-radius:10px;overflow:hidden;"><div style="height:100%;border-radius:10px;width:{v4}%;background:{c4};"></div></div>
        <span style="flex:0 0 36px;text-align:right;font-weight:700;font-size:14px;color:{c4};">{v4}</span>
      </div>
    </div>
  </div>
  <!-- 下排：诊断概况 -->
  <div style="padding:20px 28px;background:#fef9f3;border-radius:12px;border:1px solid #fde8cd;">
    <div style="margin-bottom:14px;font-size:14px;font-weight:700;color:#333;">诊断概况</div>
    <div style="display:flex;gap:20px;">
      <div style="flex:1;"><div style="font-weight:700;color:#e8792b;font-size:13px;margin-bottom:4px;">当前阶段</div><div style="font-size:13px;color:#444;line-height:1.6;">{当前阶段内容}</div></div>
      <div style="flex:1;"><div style="font-weight:700;color:#e8792b;font-size:13px;margin-bottom:4px;">核心卡点</div><div style="font-size:13px;color:#444;line-height:1.6;">{核心卡点内容}</div></div>
      <div style="flex:1;"><div style="font-weight:700;color:#27ae60;font-size:13px;margin-bottom:4px;">最该做的</div><div style="font-size:13px;color:#444;line-height:1.6;">{最该做的内容}</div></div>
      <div style="flex:1;"><div style="font-weight:700;color:#e74c3c;font-size:13px;margin-bottom:4px;">最大风险</div><div style="font-size:13px;color:#444;line-height:1.6;">{最大风险内容}</div></div>
    </div>
  </div>
</div>
<!-- ====== 首屏仪表盘结束 ====== -->

**占位符说明**：
- `{v0}-{v4}`：五维度分值（0-100）
- `{c0}-{c4}`：条形图颜色（≥70用#27ae60，50-69用#f39c12，<50用#e74c3c）
- `{score}`：综合可行度分数
- `{scoreColor}`：分数颜色（80-100用#27ae60，60-79用#f39c12，40-59用#e8792b，0-39用#e74c3c）
- `{level}`：等级文字（高度可行/可行但需突破/有挑战/不可行）
- `{stage}`：当前阶段名称
- `{当前阶段内容}`等：诊断概况4行内容，每行需包含具体可执行信息（2-3句话），禁止空泛描述

**关键约束**：
1. 禁止修改HTML结构（三栏布局、gap、顺序等），仅替换{}占位符
2. 上排：左=综合评分卡，右=维度条形图；下排=诊断概况（四项横排）
3. 诊断概况每行内容必须充实：当前阶段需说明"做什么+为什么"，核心卡点需指出"具体问题+根因"，最该做的需给出"动作+时间"，最大风险需说明"风险+后果"

**五维度分值来源**：
- 需求可行性：Skill1诊断的可行度评分
- 市场空间：Skill1诊断的市场空间评分
- 个人匹配度：Skill1诊断的个人匹配度评分
- 产品成熟度：无产品=0，有Idea=30，有MVP=60，有付费用户=80，有复购=100
- 合规就绪度：均无=0，有主体=40，有主体+合同=70，全部就绪=100

**综合可行度** = 需求可行性×0.4 + 市场空间×0.3 + 个人匹配度×0.3
**等级**：80-100绿灯 / 60-79黄灯 / 40-59橙灯 / 0-39红灯

**策略3：兜底方案**
- 如果HTML生成失败，至少保证Markdown文件生成成功

### 导出文件命名规则

文件名格式：`OPC智脑诊断报告_{项目名}_{日期}.{扩展名}`

示例：
- `OPC智脑诊断报告_智能电蚊拍Idea_2026-06-09.md`
- `OPC智脑诊断报告_社区治理SaaS_2026-06-09.html`

### 导出文件存储位置

默认存储在项目根目录下的 `opc-reports/` 文件夹：
```
opc-reports/
├── 2026-06-09/
│   ├── OPC智脑诊断报告_智能电蚊拍Idea_2026-06-09.md
│   ├── OPC智脑诊断报告_智能电蚊拍Idea_2026-06-09.html
│   ├── OPC智脑诊断报告_社区治理SaaS_2026-06-09.md
│   ├── OPC智脑诊断报告_社区治理SaaS_2026-06-09.html
```

### 异常处理（用户友好）

#### 情况1：用户不选择导出
```
用户：不需要

OPC智脑：好的，报告未导出。您可以随时让我重新诊断并导出。
```

#### 情况2：用户选择无效
```
用户：abc

OPC智脑：请回复数字：
• 1 = Markdown
• 2 = HTML
• 或多个数字，如 1,2
```

#### 情况3：导出失败
```
OPC智脑：⚠️ 导出遇到问题，已为您生成Markdown文件作为备选。

📄 文件位置：opc-reports/2026-06-09/OPC智脑诊断报告_xxx.md

💡 您可以：
1. 用Markdown编辑器打开查看
2. 或用文本编辑器打开查看
```

### 导出工具集成

导出工具位于项目根目录：`opc-report-exporter/`

工具提供以下API：
- `exportReport(markdown, format, options)` - 导出报告
- `exportReportFromFile(filePath, format, options)` - 从文件导出

支持格式：
- `markdown` - Markdown文档（.md）
- `html` - HTML文档（.html）
- `both` - 同时生成Markdown和HTML

### 使用示例（完整流程）

**示例1：首次使用的新手用户**

```
用户：帮我诊断这个Idea：智能电蚊拍+计数器+App

OPC智脑：【阶段判定】当前处于：构思期（第1阶段）
...（完整诊断内容）

---
📊 **一键导出报告**

诊断完成！是否需要导出文档？

回复数字即可：
• 回复 1 → 导出 Markdown（适合在线查看）
• 回复 2 → 导出 HTML（适合浏览器查看，可打印）
• 回复 1,2 → 全部导出

用户：2

OPC智脑：⏳ 正在生成文档...

✅ 导出成功！

� 文件已保存到：opc-reports/2026-06-09/

📄 已生成文件：
• OPC智脑诊断报告_智能电蚊拍Idea_2026-06-09.html（HTML文档）

💡 如何使用：
• HTML文档：双击打开，浏览器自动显示，可打印或详细阅读
```

**示例2：只要HTML文档**

```
用户：2

OPC智脑：⏳ 正在生成HTML文档...

✅ 导出成功！

📄 文件位置：opc-reports/2026-06-09/OPC智脑诊断报告_xxx.html

💡 双击文件即可打开，适合打印或详细阅读。
```

### 约束规则

1. **主动询问原则**：每次诊断完成后必须主动询问是否导出，不等待用户主动提出
2. **自动化原则**：用户选择后自动执行导出，不需要用户手动操作命令
3. **多选支持**：支持用户选择多个格式，一次生成多个文件
4. **错误友好**：导出失败时提供清晰的错误信息和解决方案
5. **文件管理**：按日期自动分类存储，避免文件混乱
6. **AI标识原则**：在Markdown和HTML文档末尾必须添加AI生成标识，格式如下：
   - Markdown：在文档末尾添加 `---\n\n**本报告由OPC智脑（AI）生成**\n\n作者：李屹镒\n\n生成时间：{日期时间}\n\n---`
   - HTML：在页面底部添加醒目的AI生成标识区域，包含"本报告由OPC智脑（AI）生成"、作者信息和生成时间
---

## OPC智脑使用指南

### 快速开始

1. **发起诊断**：直接描述你的创业Idea或当前困惑
2. **等待诊断**：OPC智脑会自动判定阶段并给出建议
3. **导出报告**：回复数字（1或2），自动生成文档

### 常见问题

**Q：我不懂技术，能用吗？**
A：完全可以！你只需要用自然语言描述问题，OPC智脑会自动完成所有分析。导出报告也只需回复数字。

**Q：导出的文件在哪里？**
A：文件自动保存在 `opc-reports/日期/` 文件夹，你可以直接打开使用。

**Q：诊断结果准确吗？**
A：OPC智脑基于五阶段创业模型，所有建议都严格适配"一人创业者"的约束，务实落地可执行。

**Q：可以多次诊断吗？**
A：可以！每次诊断都会独立生成报告，按日期自动分类存储。

### 最佳实践

1. **如实回答**：信息采集时如实回答，诊断会更精准
2. **按阶段推进**：不要跳阶段，每阶段达到毕业条件再进入下一阶段
3. **执行建议**：OPC智脑的建议都是可立即执行的，建议按优先级执行
4. **定期复盘**：每完成一个阶段，导出报告复盘，再进入下一阶段

---

**OPC智脑 - 一人公司全生命周期创业诊断专家**

让每个创业者都能用最低成本、最短路径完成从0到1的商业验证。

---

