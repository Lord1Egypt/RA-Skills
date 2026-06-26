# 🤖 豆包会话专家点评系统

**版本：** v1.0  
**创建时间：** 2026-03-06  
**作者：** 阿福（AI 助理）

---

## 📋 功能说明

自动处理豆包会话内容，生成专家级点评 HTML 网页，包含：
- 知识架构图（Mermaid）
- 专家深度洞察
- 对比分析表格
- 行动建议

**核心流程：**
```
豆包会话 → AI 分析 → 专家点评 → HTML 网页 → Chrome 打开 → TTS 语音 → 飞书发送
```

---

## 🚀 快速开始

### 方法 1：使用触发词（推荐）

在飞书聊天中发送：
```
豆包 [粘贴豆包会话内容...]
```

系统会自动执行 4 步流程。

### 方法 2：手动运行脚本

```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\Xiabi\.openclaw\workspace\skills\doubao-expert-review\scripts\process-doubao-session.ps1
```

---

## 📐 用户偏好（已内置）

### 学习偏好
- ✅ 视觉学习者 - 结构化专业图表
- ✅ 不要手绘风格 - 要专业架构图
- ✅ Mermaid 图表 + 知识要点
- ✅ 结合自身业务场景点评

### 语音偏好
- ✅ 自动播放 - TTS 生成后自动播放
- ✅ 文字 + 语音 - 飞书同时发送
- ✅ 0 步操作 - 全自动

### 行文风格
- ✅ 金字塔原理 - 结论先行
- ✅ Critical Thinking - 主动思考
- ✅ 业务价值导向 - 先说价值
- ✅ MECE 法则 - 不重不漏

### 视觉设计
- ✅ 科学杂志风 - Nature 排版
- ✅ 小红书图标 - emoji 点缀
- ✅ 双栏布局 + 侧边栏导航
- ✅ 专业配色

---

## 📁 文件结构

```
doubao-expert-review/
├── SKILL.md                          # 技能定义文件
├── README.md                         # 本文件
├── scripts/
│   ├── process-doubao-session.ps1    # 主处理脚本
│   ├── fetch-doubao-history.ps1      # 豆包历史获取（可选）
│   └── generate-expert-review.ps1    # 专家点评生成（可选）
└── templates/
    └── expert-review-template.html   # HTML 模板
```

---

## 🎨 HTML 输出标准

### 必备章节（按顺序）

1. **专家评分** - 完整性/正确性/缺失项
2. **核心观点** - 结论先行
3. **深度洞察** - ≥3 个大观点
4. **知识架构** - Mermaid 图表
5. **对比分析** - 表格或对比图
6. **行动建议** - 可落地的建议

### 视觉风格

- **字体：** 微软雅黑 (Microsoft YaHei)
- **背景：** 白色背景，深色文字
- **布局：** 双栏布局 + 侧边栏
- **图表：** Mermaid 知识架构图
- **配色：** 学术风格，专业严谨

---

## 📊 示例输出

### 输入
```
豆包
今天学习了小米汽车的感知与行动中心项目：
1. 感知侧已落地，115 家供应商调研完成
2. 工单闭环规划中
3. 6 大核心指标：决策通过 115 家，SBC 签约 75.7%，验收通过率 94%，产能达标率 68%
```

### 输出文件
1. `doubao-sessions/2026-03-06 (周五) -1 worklog.md` - 原始内容
2. `expert-review-2026-03-06-xiaomi-auto.html` - 专家点评 HTML
3. `worklog.txt` - 工作日志更新

### 自动操作
1. ✅ Chrome 打开 HTML 预览
2. ✅ TTS 生成核心内容语音
3. ✅ 飞书发送文字 + 语音
4. ✅ 本地自动播放语音

---

## 🔧 配置选项

### 环境变量（可选）

```powershell
$env:DOUBAO_WORKSPACE = "C:\Users\Xiabi\.openclaw\workspace"
$env:DOUBAO_AUTO_OPEN_CHROME = "true"  # 是否自动打开 Chrome
$env:DOUBAO_AUTO_SEND_FEISHU = "true"  # 是否自动发送飞书
$env:DOUBAO_AUTO_PLAY_VOICE = "true"   # 是否自动播放语音
```

---

## ⚠️ 注意事项

1. **触发词识别** - 必须严格以 "豆包" 开头
2. **序号递增** - 同一天多次会话自动递增
3. **HTML 标准** - 必须包含 6 个必备章节
4. **语音播放** - 需要本地音频播放权限
5. **Chrome 依赖** - 需要安装 Google Chrome

---

## 🐛 故障排查

### 问题 1：Chrome 没有自动打开

**解决：**
```powershell
# 检查 Chrome 是否安装
Get-AppxPackage -Name "Google.Chrome"

# 手动打开
Start-Process "chrome.exe" -ArgumentList "expert-review-*.html"
```

### 问题 2：飞书语音没有自动播放

**解决：**
```powershell
# 检查 play-latest-voice.ps1 脚本
Test-Path "C:\Users\Xiabi\.openclaw\workspace\play-latest-voice.ps1"

# 手动播放
powershell -ExecutionPolicy Bypass -File play-latest-voice.ps1
```

### 问题 3：HTML 格式不符合预期

**解决：**
- 检查 `templates/expert-review-template.html`
- 确保包含 6 个必备章节
- 验证 Mermaid 图表语法正确

---

## 📞 相关资源

- **MEMORY.md** - 长期记忆，包含项目知识库
- **DOUBAO_AUTO_GUIDE.md** - 豆包自动化指南
- **worklog.txt** - 日常工作日志

---

## 🎯 成功标准

- ✅ 豆包会话完整保存
- ✅ worklog.txt 及时更新
- ✅ HTML 符合专家点评格式
- ✅ Chrome 自动打开
- ✅ TTS 语音生成并播放
- ✅ 飞书消息发送成功

---

## 📝 更新日志

### v1.0 (2026-03-06)
- ✅ 初始版本发布
- ✅ 4 步自动化流程实现
- ✅ 专家点评 HTML 模板
- ✅ 用户偏好内置
- ✅ 飞书集成

---

**维护者：** 阿福（AI 助理）  
**最后更新：** 2026-03-06
