# 达人数据采集执行协议（Collection Playbook）

> 定位：Step 2「采集与整理证据」中 T4 公开页面取数路径的执行手册。本 skill 不内置采集器，本协议 + `scripts/collect_account.py` 提供可复用的自动化骨架。
> 配套脚本：`scripts/collect_account.py`（Playwright 骨架，输出 works.csv / comments.csv）。

## 0. 何时使用

- 用户没有现成数据，且无法走 T1 官方后台 / T2 开放 API / T3 第三方工具导出时
- 需要评论原文做七维分类与信任资产信号核查（T3 工具拿不到评论原文）时

## 1. 路径选择（按优先级）

| 优先级 | 路径 | 工具 | 说明 |
|--------|------|------|------|
| 1 | 用户已有数据 | — | 校验口径后直接进入 Step 3 |
| 2 | 第三方工具导出 | 蝉妈妈/飞瓜/千瓜导出 Excel/CSV | 作品数据快；无评论原文 |
| 3 | 浏览器自动化 | `scripts/collect_account.py`（或 agent-browser） | T4 主粮：作品 + 评论原文 |
| 4 | Agent-Reach 渠道 | 宿主安装后读取 xiaohongshu/bilibili/twitter | 证据等级同 T4 |
| 5 | 截图/导出解析 | OCR / 表格解析 | 补充性数据块 |

## 2. 浏览器自动化采集步骤

### 2.1 前置检查

1. 确认目标平台与达人主页 URL（Step 1 已定）
2. `pip install playwright && playwright install chromium`
3. 先以 `--headless` 关闭的有头模式跑一次，人工确认页面可访问、登录墙/验证码不阻断公开内容

### 2.2 运行脚本

```bash
# 采集作品列表 + 每条代表作品的可见评论
python scripts/collect_account.py \
  --platform xiaohongshu \
  --url "https://www.xiaohongshu.com/user/profile/xxx" \
  --out ./out \
  --max-works 45 \
  --max-comments 1000
```

输出：
- `works.csv`：作品清单（work_id / platform / url / publish_time / likes / comments / favorites / caption / fetch_time）
- `comments.csv`：评论明细（work_id / content / likes / is_top / fetch_time），已去标识化（不含昵称/头像）

### 2.3 选择器适配（关键）

平台 DOM 持续变动，`SELECTORS` 中的选择器是**占位配置**。采集结果为空或明显缺失时：

1. 有头模式打开目标页面，用 DevTools 定位作品卡片、互动数据、评论节点的实际 class/data 属性
2. 更新 `scripts/collect_account.py` 中 `SELECTORS[平台]` 对应条目
3. 适配记录写入脚本注释（`# 适配日期: YYYY-MM-DD`），便于追溯

**经验参考：**
- 互动数据（点赞/评论/收藏）在不同页面形态下可能是独立 DOM 节点或卡片内联文本，优先选 `data-e2e` / `data-testid` 类稳定属性，其次再选 class
- 评论的"查看更多回复"按钮要点击展开后再翻页，脚本通过滚动触发懒加载，失效时需手动补点击逻辑

### 2.4 批量与控频

- 默认 `--max-works 40`，与 Step 1 样本量自适应标准对齐（高频账号可调大）
- 内置拟人化随机延时；一次跑大量账号时，分批执行并加大延时
- **只采公开可见数据**；遇到登录墙/验证码即停止，如实报告，不绕过

## 3. 结构化整理 Schema（对齐"交付四件套"）

| 交付物 | 来源 | 字段要求 |
|--------|------|---------|
| 作品清单 | works.csv | 含 platform 标记 + 基础数据；置顶/近期/代表作品分档由 Step 3 分析时标注 |
| 评论明细 | comments.csv | 按 work_id 与作品一一对应；内容原文 + 点赞数 |
| 素材文件夹 | 脚本不采图片/视频本体 | 需素材时单独下载封面/视频，按 work_id 归档 |
| 采集说明 | 手动填写 | 口径、时间范围、平台可见性限制、缺失项、选择器适配记录 |

**口径要求（对齐 data-collection.md）：** 不同作品和评论必须按同一套口径对上号；跨平台数据不得混在同一口径下统计。

## 4. 口径校验清单（进入 Step 3 前）

- [ ] works.csv 条数 ≥ Step 1 样本范围要求（否则走降级协议）
- [ ] 每条作品都有 fetch_time 与 platform 标记
- [ ] 评论明细能按 work_id 对回作品，无孤儿评论
- [ ] 评论区是否只采到"可见评论"（排序/折叠/删除影响）——在采集说明中标注
- [ ] 无昵称/头像等个人信息残留（去标识化校验）

## 5. 合规检查点（必须遵守）

- 只采集**公开可见**数据，不碰需登录态的他人私人数据
- 遵守平台服务条款与 robots 协议，控制采集频率（拟人化节奏）
- 评论数据统计前**去标识化**（脚本已默认不采昵称/头像）
- 无法获取的数据如实标注缺口，**禁止用推算值冒充实测值**
- 触发风控/封禁的风险由使用者自担

## 6. 失败降级

| 情况 | 处理 |
|------|------|
| 脚本运行失败 | 改用 agent-browser 人工引导采集，或退回用户已有数据 / T3 导出 |
| 选择器失效导致数据为空 | 按 2.3 适配后重跑；无法适配则如实报告，不编造 |
| 平台登录墙阻断 | 停止采集，在报告「证据边界」声明缺口 |
| 部分作品评论采不全 | 在采集说明记录可见性限制，评论层结论降级为"方向性判断" |
