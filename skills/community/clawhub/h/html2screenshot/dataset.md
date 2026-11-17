# 📊 html2screenshot 训练集与验证集

> 为 SkillOpt 循环设计的评测数据集，覆盖 html2screenshot 技能的全部核心能力维度。

---

## 一、数据集设计原则

| 原则 | 说明 |
|------|------|
| **多样性** | 覆盖不同 HTML 结构、CSS 特性、页面长度、交互复杂度 |
| **可验证** | 每个任务都有明确的 Pass/Fail 判定标准 |
| **分层递进** | 从简单到复杂，便于定位系统性错误 |
| **真实场景** | 包含实际使用过的 HTML 页面（A股报告、网页长截图等） |
| **独立划分** | 训练集与验证集严格不重叠 |

---

## 二、评测维度（Scorecard）

每个任务截图后，从以下 6 个维度打分（0-5 分）：

| # | 维度 | 评估标准 | 权重 |
|---|------|---------|------|
| **D1** | **完整性** | 页面内容是否全部被捕获，有无遗漏 | 25% |
| **D2** | **清晰度** | 文字是否清晰可读，有无模糊/锯齿 | 20% |
| **D3** | **布局保真** | 元素位置/大小/间距是否与原页面一致 | 20% |
| **D4** | **CSS 渲染** | backdrop-filter、position: fixed、transform、opacity 等高级 CSS 是否正确渲染 | 15% |
| **D5** | **动态内容** | JS 渲染内容、懒加载图片、无限滚动是否完整捕获 | 10% |
| **D6** | **尺寸适配** | viewport 设置是否正确应用，长图是否完整 | 10% |

**总分 = D1×0.25 + D2×0.20 + D3×0.20 + D4×0.15 + D5×0.10 + D6×0.10**

**Pass 阈值**：总分 ≥ 4.0（即 80% 以上）

---

## 三、训练集（15 个任务）

### 基础层（T1-T5）— 验证基本功能

| ID | 场景 | HTML 来源 | 关键评估点 | 预期总分 |
|----|------|-----------|-----------|---------|
| **T1** | 简单静态页面 | 纯 HTML + 内联 CSS | D1 完整性、D2 清晰度 | ≥4.5 |
| **T2** | 带图片的页面 | HTML + 本地图片路径 | D1 完整性、D5 动态内容 | ≥4.0 |
| **T3** | 长页面（>2000px） | A股报告 HTML（约2500行） | D1 完整性、D6 尺寸适配 | ≥4.0 |
| **T4** | 表格密集页面 | 数据表格（10+列 × 20+行） | D3 布局保真、D2 清晰度 | ≥4.0 |
| **T5** | 多列布局 | CSS Grid / Flexbox 三列布局 | D3 布局保真 | ≥4.0 |

### 进阶层（T6-T10）— 验证 CSS 高级特性

| ID | 场景 | HTML 来源 | 关键评估点 | 预期总分 |
|----|------|-----------|-----------|---------|
| **T6** | backdrop-filter 模糊背景 | 带 `backdrop-filter: blur()` 的卡片 | D4 CSS 渲染 | ≥3.5 |
| **T7** | position: fixed 固定元素 | 带固定头部/侧边栏的页面 | D4 CSS 渲染、D1 完整性 | ≥3.5 |
| **T8** | CSS transform 动画 | 带 `transform: scale()` 的元素 | D4 CSS 渲染 | ≥3.5 |
| **T9** | opacity 淡入效果 | 带 `opacity` 动画的页面 | D4 CSS 渲染 | ≥3.5 |
| **T10** | 混合 CSS 特效 | 同时含 backdrop-filter + fixed + transform | D4 CSS 渲染（综合） | ≥3.0 |

### 复杂层（T11-T15）— 验证动态与真实场景

| ID | 场景 | HTML 来源 | 关键评估点 | 预期总分 |
|----|------|-----------|-----------|---------|
| **T11** | JS 动态渲染 | 带 `document.createElement` 的页面 | D5 动态内容 | ≥3.5 |
| **T12** | 懒加载图片 | 带 `loading="lazy"` 的图片 | D5 动态内容、D1 完整性 | ≥3.5 |
| **T13** | 外部 URL 页面 | 东方财富/雪球等财经页面 | D5 动态内容、D1 完整性 | ≥3.0 |
| **T14** | 移动端 viewport | 390×844 mobile viewport | D6 尺寸适配、D3 布局保真 | ≥3.5 |
| **T15** | 完整 A股报告（2026-05-30） | `memory/2026-05-30.md` 渲染的 HTML | 全维度综合 | ≥4.0 |

---

## 四、验证集（10 个任务）

> ⚠️ 验证集必须与训练集严格不重叠，用于 Gate 门控评估。

### 验证集任务

| ID | 场景 | HTML 来源 | 关键评估点 | 预期总分 |
|----|------|-----------|-----------|---------|
| **V1** | 极简单页 | 单 `<div>` + 内联 CSS | D1 完整性、D2 清晰度 | ≥4.5 |
| **V2** | 超长页面（>5000px） | 多页合并的长报告 | D1 完整性、D6 尺寸适配 | ≥3.5 |
| **V3** | 复杂表格 | 合并单元格 + 多级表头 | D3 布局保真 | ≥3.5 |
| **V4** | 嵌套定位 | fixed + absolute + relative 混合 | D4 CSS 渲染 | ≥3.0 |
| **V5** | 渐变 + 阴影 | 复杂 background-gradient + box-shadow | D4 CSS 渲染 | ≥3.5 |
| **V6** | 外部字体 | 使用 Google Fonts / 自定义字体 | D2 清晰度、D3 布局保真 | ≥3.5 |
| **V7** | 视频/媒体嵌入 | `<video>` / `<iframe>` 嵌入 | D5 动态内容 | ≥3.0 |
| **V8** | 暗黑主题 | 深色背景 + 亮色文字 | D2 清晰度、D4 CSS 渲染 | ≥3.5 |
| **V9** | 响应式断点 | 媒体查询切换不同布局 | D6 尺寸适配 | ≥3.5 |
| **V10** | 真实网页（知乎文章） | 知乎长文页面 | 全维度综合 | ≥3.5 |

---

## 五、训练集/验证集划分矩阵

```
              训练集          验证集
基础层        T1-T5           V1
进阶层        T6-T10          V4, V5
复杂层        T11-T15         V2, V3, V6-V10
```

**划分说明**：
- 验证集 V1 对应基础层，确保基本功能不回归
- 验证集 V4, V5 对应进阶层，确保 CSS 渲染能力不退化
- 验证集 V2, V3, V6-V10 对应复杂层，确保真实场景能力
- 训练集 T6-T10 专门针对已知失败模式（backdrop-filter/fixed 等），用于主动修复

---

## 六、评分自动化脚本模板

```bash
#!/bin/bash
# evaluate_screenshot.sh
# 用法: ./evaluate_screenshot.sh <html_file> <output_png> <viewport_width> <viewport_height>

HTML_FILE="$1"
OUTPUT_PNG="$2"
VIEWPORT_W="${3:-1280}"
VIEWPORT_H="${4:-800}"

# 1. 截图
NODE_PATH=/Users/zhangyao/.local/lib/node_modules node - <<'SCRIPT'
const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  const html = fs.readFileSync(process.argv[1], 'utf8');
  const OUTPUT = process.argv[2];
  const W = parseInt(process.argv[3]);
  const H = parseInt(process.argv[4]);

  const browser = await puppeteer.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: W, height: H, deviceScaleFactor: 2 });
  await page.setContent(html, { waitUntil: 'load' });

  const dims = await page.evaluate(() => ({
    width: Math.ceil(document.body.scrollWidth),
    height: Math.ceil(document.body.scrollHeight),
  }));

  await page.setViewport({ width: dims.width, height: dims.height, deviceScaleFactor: 2 });
  await page.evaluate(() => window.stop());

  await page.screenshot({ type: 'png', fullPage: true }).then(s => {
    fs.writeFileSync(OUTPUT, s);
    console.log(JSON.stringify({
      success: true,
      width: dims.width,
      height: dims.height,
      fileSizeKB: Math.round(s.length / 1024)
    }));
  });

  await browser.close();
})();
SCRIPT

# 2. 输出结果供人工/LLM 评分
echo "Screenshot saved to: $OUTPUT_PNG"
```

---

## 七、SkillOpt 执行计划

### Phase 1: Baseline（基准测试）
1. 用当前 SKILL.md 在验证集 V1-V10 上跑一遍
2. 记录每个任务的得分和失败模式
3. 计算验证集平均分（baseline score）

### Phase 2: Rollout（训练集执行）
1. 用当前 SKILL.md 在训练集 T1-T15 上执行
2. 收集完整执行轨迹：
   - 使用的 viewport 参数
   - 是否遇到错误/超时
   - 截图文件大小
   - 人工/LLM 评分

### Phase 3: Reflect（反向传播）
1. 分析失败 minibatch（总分 < 4.0 的任务）
2. 识别系统性错误模式：
   - "所有 backdrop-filter 场景都模糊" → 需要添加 `--disable-gpu` 或 `--screenshot-mode=normal` 参数
   - "所有 long page 都截断" → 需要调整 `fullPage` 或 viewport 计算逻辑
   - "JS 渲染内容缺失" → 需要增加 `waitUntil: 'networkidle0'` 或 `waitForSelector`
3. 分析成功 minibatch，确认有效规则

### Phase 4: Edit（有界编辑）
1. 基于反思结果，提出最多 4 次编辑操作
2. 编辑类型：
   - `add`: 添加新的 CSS 渲染修复规则
   - `delete`: 删除无效/冗余的说明
   - `replace`: 替换过时的参数配置

### Phase 5: Gate（验证门控）
1. 在验证集 V1-V10 上评估候选新 SKILL.md
2. 只有严格提升才接受（并列也拒绝）
3. 拒绝则记录到拒绝编辑缓冲区

### Phase 6: 慢更新/元技能
1. 每 epoch 结束做跨 epoch 一致性分析
2. 提炼长期模式写入 SKILL.md 的"保护区域"

---

## 八、已知失败模式记录（用于 Reflect 分析）

| 失败模式 | 触发场景 | 可能原因 | 修复方向 |
|---------|---------|---------|---------|
| backdrop-filter 模糊 | T6, T10 | Chrome GPU 加速问题 | 添加 `--disable-gpu` 或 `--disable-software-rasterizer` |
| position: fixed 不可见 | T7 | 截图时 fixed 元素未渲染 | 确保 `waitUntil: 'load'` 后等待额外时间 |
| 长页面截断 | T3, T15 | viewport 高度计算错误 | 改用 `document.documentElement.scrollHeight` |
| JS 内容缺失 | T11 | 页面未完全渲染 | 增加 `page.waitForSelector()` 或 `page.waitForTimeout()` |
| 图片模糊 | T2 | deviceScaleFactor 未生效 | 确保 `deviceScaleFactor: 2` 在 `setViewport` 中设置 |

---

*数据集版本: v1.0 | 创建时间: 2026-06-02 | 下一步: 执行 Baseline 测试*