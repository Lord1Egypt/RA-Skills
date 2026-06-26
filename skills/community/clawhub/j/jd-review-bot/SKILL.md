---
name: jd-review-bot
description: 京东批量评价自动化。当用户需要自动评价京东待评价商品时使用此技能。触发场景包括但不限于：批量评价京东订单、自动评价京东商品、给京东待评价商品全部好评、京东评价自动化。无论用户是否明确提到"批量"或"自动化"，只要涉及京东商品评价操作都应触发此技能。
---

# 京东批量评价技能

自动登录京东评价页面，批量完成所有待评价商品的五星好评。

## 环境准备

### 安装 browser-use

如果用户尚未安装 browser-use，先执行安装：

```bash
pip install browser-use
browser-use install
```

`browser-use install` 会安装 Chromium 浏览器及系统依赖。安装完成后验证：

```bash
browser-use doctor
```

### 前置条件

- **Chrome 浏览器**: 用户已登录京东账号的真实 Chrome（通过 `--browser real` 复用 cookie）
- **运行模式**: 必须使用 `--real --headed` 参数，让用户可见浏览器操作过程

## 执行流程

### 阶段 0：环境检查

执行任何操作前，先检查 browser-use 是否可用：

```bash
which browser-use || pip install browser-use && browser-use install
```

如果 `browser-use doctor` 报错，根据提示修复。确保 Chrome 浏览器已打开且已登录京东。

### 阶段 1：收集待评价订单

1. 打开京东评价列表页 `https://club.jd.com/myJdcomments/myJdcomment.action`
2. 遍历 1-5 页，从每页用 `browser-use eval` 提取所有"评价"链接的 ruleid
3. 去重汇总所有 ruleid

```javascript
// 提取 ruleid 的 JS
Array.from(document.querySelectorAll('a'))
    .filter(a => a.textContent.trim() === '评价' && a.href.includes('orderVoucher'))
    .map(a => a.href.match(/ruleid=(\\d+)/)[1])
    .filter((v, i, a) => a.indexOf(v) === i)
```

### 阶段 2：逐个评价（关键顺序！）

对每个 ruleid，按以下顺序操作：

#### 2.1 打开评价页

`https://club.jd.com/myJdcomments/orderVoucher.action?ruleid={ruleid}`

#### 2.2 先填评价文字（必须在评分之前！）

> **为什么必须先填文字**: 京东的星级评分交互会清空所有 textarea。如果先评分再填文字，文字会被清空。

1. 找到所有可见 textarea：`document.querySelectorAll('textarea')`
2. 对每个 textarea，依次：
   - 用 `browser-use eval` 聚焦：`ta.focus(); ta.click()`
   - 用 `browser-use type` 命令输入好评文字（**不可用 JS value 赋值，京东的字符计数器和表单校验不认 JS 赋值**）
3. 文字长度 15-26 字，使用以下模板：

```
宝贝收到了质量很好做工精细非常满意的一次购物体验好评
商品不错包装很严实物流也很快好评推荐购买
质量很好价格实惠值得购买五星好评满意
收到货了跟描述一样很满意以后还会再来好评
东西挺好的用着很顺手推荐购买好评
快递很快包装完好产品质量也不错好评推荐
物美价廉性价比很高满意的一次购物体验
用了一段时间了质量没问题好评推荐购买
外观好看做工精致非常满意好评推荐
第二次购买了质量稳定值得信赖好评
物流超快东西也很好用点赞推荐购买
性价比很高质量超出预期推荐好评
服务态度很好物流速度很快整体体验非常满意
安装师傅很专业态度很好非常满意的一次购物
配送速度快包装完好安装服务也很到位好评
```

4. 手动同步计数器：`document.querySelector('.textarea-num b').textContent = ta.value.length`

#### 2.3 再评分

对所有 `.commstar` 评分组件执行五星评分：

```javascript
document.querySelectorAll('.commstar').forEach(group => {
    // 逐星 hover，触发京东评分组件的内部状态
    for (let i = 1; i <= 5; i++) {
        const star = group.querySelector('.star.star' + i);
        if (star) {
            star.dispatchEvent(new MouseEvent('mouseenter', { bubbles: true }));
            star.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
        }
    }
    // 点击第5颗星确认评分
    const s5 = group.querySelector('.star.star5');
    if (s5) s5.dispatchEvent(new MouseEvent('click', { bubbles: true }));
});
```

#### 2.4 处理服务印象（如有）

部分订单有"服务印象"标签选择，点击正面标签：

```javascript
const reasonsSection = document.querySelector('.fop-reasons');
if (reasonsSection) {
    const labels = reasonsSection.querySelectorAll('label, span');
    const positiveLabels = Array.from(labels).filter(l => {
        const t = l.textContent.trim();
        return t.includes('态度好') || t.includes('速度快') || t.includes('专业') 
            || t.includes('满意') || t.includes('耐心') || t.includes('及时')
            || t.includes('热情') || t.includes('细心') || t.includes('准时');
    });
    positiveLabels.slice(0, 3).forEach(l => l.click());
}
```

#### 2.5 提交前最终同步

评分操作可能清空 textarea 或重置计数器，提交前必须重新同步：

```javascript
document.querySelectorAll('textarea').forEach(ta => {
    const container = ta.closest('.fop-item');
    const counterB = container?.querySelector('.textarea-num b');
    if (counterB && ta.value.length > 0) {
        counterB.textContent = ta.value.length;
    }
});
```

#### 2.6 点击发表

```javascript
const btn = Array.from(document.querySelectorAll('a'))
    .find(el => el.textContent.trim() === '发表');
if (btn) btn.click();
```

#### 2.7 验证结果

提交后等待 2-3 秒，检查页面是否跳转离开评价页：

```javascript
const body = document.body.innerText;
if (!body.includes('评价订单')) return 'SUCCESS';  // 已跳转，评价成功
if (body.includes('请填写完整的评价内容')) return 'ERROR';  // 校验失败
```

### 阶段 3：确认完成

全部评价完成后，回评价列表页验证所有页的"评价"链接数为 0。

## browser-use CLI 命令参考

> **关键**: 所有命令必须加 `--session <name>` 保持会话状态，否则后续 eval/type/state 会报 `SessionManager not initialized` 错误。

```bash
# 打开页面
browser-use --browser real --headed --session jdreview open "<url>"

# 执行 JavaScript（返回 JSON）
browser-use --browser real --headed --session jdreview --json eval "<js_code>"

# 模拟键盘输入（必须用于 textarea 填文字）
browser-use --browser real --headed --session jdreview type "<text>"

# 查看页面状态
browser-use --browser real --headed --session jdreview state
```

## 常见问题

### SessionManager not initialized

每个 `browser-use` CLI 命令是独立进程，不加 `--session` 无法共享浏览器状态。修复方式：所有命令统一加 `--session <name>` 参数，脚本中在 `run()` 函数统一注入即可。`open` 命令负责创建会话，后续 `eval`/`type`/`state` 复用同一会话。

### 收集到 0 条待评价

通常是 eval 执行失败但被静默吞掉（脚本 `bu_eval` 的 except 分支返回了空字符串）。确认 `run()` 函数中已包含 `--session` 参数。`browser-use` 4.x 版本起强制要求 session 参数。`open` 命令负责创建会话，后续 `eval`/`type`/`state` 复用同一会话。

## 批量脚本

技能目录下的 `scripts/jd_review.py` 是完整的批量评价脚本，可以通过 browser-use CLI 的 Python API 直接执行：

```bash
python3 /Users/huangdq/skills/jd-review-bot/scripts/jd_review.py
```

该脚本封装了上述所有流程，包括：
- 自动收集所有分页的待评价订单
- 多 textarea 订单支持（服务评价 + 商品评价）
- 服务印象标签自动选择
- 计数器同步
- 提交验证
- 进度显示和最终统计
