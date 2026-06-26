---
name: orm-weather-routing-nav-voyage-distance
description: ORM 气象导航航次距离计算工具 - 通过 NavOptima 查询港口间航行距离（海里）
homepage: https://ormwx.com
metadata: {"clawdbot":{"emoji":"⚓","requires":{"bins":[]},"install":[]}}
---

# ⚓ ORM WEATHER ROUTING NAV VOYAGE DISTANCE SKILL

**中文名：** ORM 气象导航航次距离计算工具  
**英文名：** ORM WEATHER ROUTING NAV VOYAGE DISTANCE SKILL  
**版本：** 2.4.0（航次增强版）  
**创建时间：** 2026-03-24  
**更新时间：** 2026-03-24 13:14  
**维护人：** ORM 正权海事 - AI 系统

---

## 📋 工具概述

**用途：** 通过 NavOptima 气象导航系统计算全球港口间的航行距离（海里）  
**适用场景：** 航次估算、租船合同、气象导航服务、客户报价、多港口航线规划

**数据源：** NavOptima (https://nop.ormwx.com/voyage/distance) - **公司专业系统**

---

## 🔐 登录配置（已更新）

**NavOptima 账号：**
- **URL:** https://nop.ormwx.com/voyage/distance
- **邮箱:** distance@ormwx.com
- **密码:** 5qzqE9Kt

**✅ 登录测试：** 2026-03-24 11:26 测试成功

**安全提醒：** 此账号为敏感配置，严禁外泄！

---

## 🗺️ 操作流程

### Step 1: 登录 NavOptima

1. 打开 https://nop.ormwx.com/voyage/distance
2. 点击登录按钮
3. 选择 "Account Password"
4. 输入邮箱和密码
5. 勾选协议并登录

### Step 2: 输入港口

#### 基础操作（2 个港口）

1. 点击起点港口输入框
2. 输入港口名称（如 `SHANGHAI`）
3. 从下拉列表选择正确港口（如 `SHANGHAI [CN]`）
4. 点击终点港口输入框
5. 输入港口名称（如 `BERONG`）
6. 从下拉列表选择正确港口（如 `BERONG [PH]`）

#### 高级操作（多港口 - 途经点）

**当港口数超过 2 个时：**

1. 点击 **+** 按钮（红色框）增加途经点
2. 输入途经点港口名称
3. 从下拉列表选择正确港口
4. 可继续点击 **+** 添加更多途经点
5. 点击 **-** 按钮可删除多余的港口

**示例：** 上海→新加坡→鹿特丹（3 个港口）
- 第 1 行：SHANGHAI [CN]
- 第 2 行：SINGAPORE [SG]（途经点）
- 第 3 行：ROTTERDAM [NL]

#### 经纬度设置（精确位置）

**当需要设置具体经纬度时：**

1. 点击港口输入框右侧的 **📍 定位图标**（红色框）
2. 地图进入拖拽模式
3. 用鼠标拖拽地图到目标位置
4. 观察光标显示的经纬度（右下角显示）
5. 根据光标经纬度确定精确位置
6. 点击地图设置途经点
7. 系统自动记录该点经纬度

**适用场景：**
- 非标准港口位置
- 特定锚地坐标
- 自定义航线点
- 精确的装/卸货位置

### Step 3: 选择 AI Route 并查询

1. 点击 **AI Route** 标签（蓝色按钮）
2. 点击 **Confirm** 按钮
3. 等待系统计算（约 3-5 秒）

### Step 4: 获取结果

系统显示：
- **航行距离**（海里，nm）
- **航程时间**（天，days）
- **出发时间**（ETD）
- **预计到达**（ETA）
- **航线图**（地图展示，含气象数据）

### Step 5: 截图并发送（强制）

**1. 调整地图视图（重要）**
```python
# 自动缩放地图，确保始发港和目的港都显示在画面中
# 使用 browser 工具控制 zoom in/out
# 标准：两个港口都在画面内，航线完整可见
# 如果港口距离远 → zoom out
# 如果港口距离近 → zoom in 保持适当比例
```

**2. 截取完整结果图**
```python
# 截取完整结果页面（包含地图和航线）
browser.screenshot(full_page=True, output_path="/tmp/orm-route-result.jpg")

# ⚠️ 重要：保持原始配色
# - 不进行任何渲染/滤镜/调色
# - 使用地图本来配色（默认主题）
# - 不切换深色/浅色模式
# - 保持 NavOptima 默认视觉效果
```

**3. 立即发送到聊天窗口（强制）**
```python
# 无论用户在什么窗口对话，必须发送截图
message.send(
    channel="feishu",  # 或当前对话渠道
    target=用户 ID,
    media="/tmp/orm-route-result.jpg",
    caption="📍 [起点] → [终点] 航线图 - ORM Weather Routing"
)
```

**4. 附加签名信息（强制）**
```markdown
---

### 📞 联系方式

**ORM Weather Routing**  
👤 **Andy**  
📱 **+86 18669863008** (WeChat/WhatsApp)  
📧 **Andy@ormwx.com**
```

---

## 📊 输出格式标准

### 完整输出模板

```markdown
## 📍 [起点港口] → [终点港口]

### 航行距离（NavOptima AI Route）

| 项目 | 数值 |
|------|------|
| **航行距离** | **XXX 海里** |
| 航程时间 | X.X 天 |
| 出发时间 | YYYY-MM-DD HH:MM (UTC +8) |
| 预计到达 | YYYY-MM-DD HH:MM (UTC +8) |
| 航速设定 | XX.X kts |
| 天气系数 | X% |

### 航线截图

![航线图](截图路径)

---

**数据来源：** NavOptima 气象导航系统  
**计算时间：** YYYY-MM-DD HH:MM  
**精度等级：** ⭐⭐⭐⭐⭐（<1% 误差）

---

### 📞 联系方式

**ORM Weather Routing**  
👤 **Andy**  
📱 **+86 18669863008** (WeChat/WhatsApp)  
📧 **Andy@ormwx.com**
```

### ⚠️ 强制要求

**1. 航线截图自动发送**
- ✅ 无论用户在什么窗口对话
- ✅ 查询结束后**立即发送** jpg 格式截图到聊天窗口
- ✅ 使用 `message` 工具或平台原生图片发送功能
- ✅ 截图必须包含完整航线图 + 距离数据

**2. 签名信息（每次必选）**
- ✅ 每次查询结束必须附加联系方式
- ✅ 格式固定如下：

```markdown
---

### 📞 联系方式

**ORM Weather Routing**  
👤 **Andy**  
📱 **+86 18669863008** (WeChat/WhatsApp)  
📧 **Andy@ormwx.com**
```

---

## 📍 常用港口代码

### 中国港口

| 港口 | 显示名称 | 代码 |
|------|----------|------|
| 上海 | SHANGHAI [CN] | CNSHA |
| 青岛 | QINGDAO [CN] | CNTAO |
| 宁波 | NINGBO [CN] | CNNGB |
| 深圳 | SHENZHEN [CN] | CNSZX |
| 广州 | GUANGZHOU [CN] | CNGZH |
| **潮州** | **CHAOZHOU [CN]** | **CNCZH** |
| 厦门 | XIAMEN [CN] | CNXMN |
| 大连 | DALIAN [CN] | CNDLC |
| 天津 | TIANJIN [CN] | CNTXG |

### 东南亚港口

| 港口 | 显示名称 | 代码 |
|------|----------|------|
| **Berong** | **BERONG [PH]** | **PHBRG** |
| 新加坡 | SINGAPORE [SG] | SGSIN |
| 雅加达 | JAKARTA [ID] | IDJKT |
| 马尼拉 | MANILA [PH] | PHMNL |
| 林查班 | LAEM CHABANG [TH] | THLCH |

### 非洲港口

| 港口 | 显示名称 | 代码 |
|------|----------|------|
| 马普托 | MAPUTO [MZ] | MZMPM |
| 德班 | DURBAN [ZA] | ZADUR |
| 开普敦 | CAPE TOWN [ZA] | ZACPT |
| 蒙巴萨 | MOMBASA [KE] | KEMBA |
| 达累斯萨拉姆 | DAR ES SALAAM [TZ] | TZDAR |

### 欧洲港口

| 港口 | 显示名称 | 代码 |
|------|----------|------|
| 鹿特丹 | ROTTERDAM [NL] | NLRTM |
| 汉堡 | HAMBURG [DE] | DEHAM |
| 安特卫普 | ANTWERP [BE] | BEANR |
| 比雷埃夫斯 | PIRAEUS [GR] | GRPIR |

---

## ⚠️ 注意事项

### 1. 精度说明

| 数据源 | 精度 | 误差范围 |
|--------|------|----------|
| **NavOptima** | ⭐⭐⭐⭐⭐ | **<1%** |
| Searoutes API | ⭐⭐⭐⭐ | 1-3% |
| 估算公式 | ⭐⭐⭐ | 5-10% |

### 2. 必须使用 NavOptima 的场景

- ✅ 租船合同航次估算
- ✅ 客户报价
- ✅ 气象导航服务
- ✅ 航次性能分析
- ✅ 正式报告输出
- ✅ 多港口航线规划
- ✅ 需要精确经纬度的场景

### 3. 截图要求

- ✅ 必须包含完整航线图
- ✅ 必须显示距离数值
- ✅ 必须显示 ETA 信息
- ✅ 使用 full_page=True
- ✅ 多港口航线需显示所有途经点

### 4. 安全规则

- ❌ 严禁外泄 NavOptima 账号密码
- ❌ 严禁将截图发送给未授权人员
- ❌ 严禁上传到公开平台
- ✅ 仅限内部使用和客户报价

---

## 🔧 错误处理

### 常见问题

| 问题 | 解决方案 |
|------|----------|
| 登录失败 | 检查账号密码，确认账户有效 |
| 港口找不到 | 尝试使用港口代码或英文名 |
| 结果加载超时 | 增加 wait timeout 到 60 秒 |
| 截图失败 | 检查浏览器权限 |
| AI Route 无响应 | 刷新页面重试，或切换 Experience Route |
| 多港口计算失败 | 检查港口顺序，确保每个港口都有效 |
| 经纬度设置失败 | 确保已点击定位图标，地图已加载 |

### 降级方案

如果 NavOptima 不可用：
1. 尝试刷新页面重新登录
2. 使用 Experience Route 作为备选
3. 降级到 Searoutes API
4. 使用估算公式（需标注误差范围）

---

## 📝 使用示例

### 示例 1：基本查询（2 个港口）

```
用户：查询潮州到 Berong 的距离

→ 调用 orm-weather-routing-nav-distance "Chaozhou" "Berong"
→ 登录 NavOptima
→ 输入 CHAOZHOU [CN] 和 BERONG [PH]
→ 选择 AI Route → Confirm
→ 返回：837 海里 + 截图
```

**输出：**
```markdown
## 📍 CHAOZHOU [CN] → BERONG [PH]

### 航行距离（NavOptima AI Route）

| 项目 | 数值 |
|------|------|
| **航行距离** | **837 海里** |
| 航程时间 | 3.1 天 |
| 出发时间 | 2026-03-24 11:00 (UTC +8) |
| 预计到达 | 2026-03-27 13:24 (UTC +8) |
| 航速设定 | 12.0 kts |
| 天气系数 | 5% |

---

**数据来源：** NavOptima 气象导航系统  
**计算时间：** 2026-03-24 11:09  
**精度等级：** ⭐⭐⭐⭐⭐（<1% 误差）
```

### 示例 2：多港口查询（3 个港口）

```
用户：查询上海→新加坡→鹿特丹的航线距离

→ 调用 orm-weather-routing-nav-distance "Shanghai" "Singapore" "Rotterdam"
→ 登录 NavOptima
→ 输入 SHANGHAI [CN]
→ 点击 + 按钮添加途经点
→ 输入 SINGAPORE [SG]
→ 点击 + 按钮添加终点
→ 输入 ROTTERDAM [NL]
→ 选择 AI Route → Confirm
→ 返回各段距离 + 总距离 + 截图
```

**输出：**
```markdown
## 📍 SHANGHAI [CN] → SINGAPORE [SG] → ROTTERDAM [NL]

### 航行距离（NavOptima AI Route）

| 航段 | 距离 | 时间 |
|------|------|------|
| 上海→新加坡 | 2,450 海里 | 8.5 天 |
| 新加坡→鹿特丹 | 8,350 海里 | 29.0 天 |
| **总计** | **10,800 海里** | **37.5 天** |

---

**数据来源：** NavOptima 气象导航系统  
**精度等级：** ⭐⭐⭐⭐⭐（<1% 误差）
```

### 示例 3：经纬度设置（精确位置）

```
用户：查询上海到某特定锚地（坐标：22.5°N, 114.0°E）的距离

→ 调用 orm-weather-routing-nav-distance "Shanghai" "22.5,114.0"
→ 登录 NavOptima
→ 输入 SHANGHAI [CN]
→ 点击终点右侧的 📍 定位图标
→ 拖拽地图到目标位置
→ 观察右下角经纬度显示（22.5°N, 114.0°E）
→ 点击地图设置该点为终点
→ 选择 AI Route → Confirm
→ 返回距离 + 截图
```

### 示例 4：航次计算

```
用户：潮州到 Berong，速度 12kt，油耗 20t/d

→ 调用 orm-weather-routing-nav-distance 获取距离 837 海里
→ 时间 = 837/12 = 69.75 小时 = 2.9 天
→ 油耗 = 2.9 × 20 = 58 吨
→ 输出完整航次估算
```

---

## 🎯 高级功能说明

### 多港口航线规划

**适用场景：**
- 多港挂靠航次
- 转运航线
- 环球航行
- 复杂贸易航线

**操作要点：**
1. 按顺序输入所有港口
2. 使用 + 按钮添加途经点
3. 确保港口顺序正确
4. 系统自动计算最优航线

### 经纬度精确设置

**适用场景：**
- 非标准港口位置
- 特定锚地/泊位
- 海上作业点
- 自定义航线点

**操作要点：**
1. 点击 📍 定位图标
2. 拖拽地图到目标区域
3. 观察右下角经纬度显示
4. 精确点击目标位置
5. 系统自动记录坐标

---

## 📚 相关文件

| 文件 | 用途 |
|------|------|
| `/Users/andy/.openclaw/workspace/skills/orm-weather-routing-nav-distance/SKILL.md` | Skill 定义文件 |
| `/Users/andy/.openclaw/workspace/工具使用规则.md` | 工具使用规范 |
| `/Users/andy/.openclaw/workspace/TOOLS.md` | 本地配置 |

---

## 🔄 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0.0 | 2026-03-24 | 初始版本，支持基本距离查询 |
| 2.0.0 | 2026-03-24 | 集成 NavOptima，支持 AI Route + 截图 |
| 2.1.0 | 2026-03-24 11:26 | 更新账号为 distance@ormwx.com，测试登录成功 |
| 2.1.1 | 2026-03-24 11:27 | Skill 名称更新为 ORM WEATHER ROUTING NAV DISTANCE SKILL |
| 2.2.0 | 2026-03-24 11:32 | 新增多港口支持（+ 按钮）、经纬度设置（📍 图标）功能 |
| 2.3.0 | 2026-03-24 11:40 | 强制发送截图到聊天窗口、添加签名信息（Andy 联系方式） |
| 2.3.1 | 2026-03-24 11:55 | 地图自动缩放（始发港 + 目的港同框）、保持原始配色（不渲染） |
| **2.4.0** | **2026-03-24 13:14** | **Skill 名称更新：NAV 后增加 VOYAGE（航次增强版）** |

---

## ✅ 执行确认

- [x] 创建 Skill 文件
- [x] 配置 NavOptima 登录（新账号）
- [x] 测试登录成功（2026-03-24 11:26）
- [x] 定义操作流程
- [x] 编写输出格式
- [x] 收录常用港口
- [x] 编写错误处理
- [x] 编写使用示例
- [x] 新增多港口操作说明（+ 按钮）
- [x] 新增经纬度设置说明（📍 图标）
- [x] 更新版本历史（v2.2.0）
- [x] 强制发送截图到聊天窗口（v2.3.0）
- [x] 添加签名信息（Andy 联系方式）（v2.3.0）
- [x] 地图自动缩放（始发港 + 目的港同框）（v2.3.1）
- [x] 保持原始配色（不渲染/无滤镜）（v2.3.1）
- [x] **Skill 名称更新：NAV VOYAGE（v2.4.0）**

---

**维护人：** ORM 正权海事 - AI 系统  
**审核人：** 高总  
**生效时间：** 2026-03-24  
**下次回顾：** 2026-03-31

---

*⚓ ORM WEATHER ROUTING NAV VOYAGE DISTANCE SKILL - 专业航海航次距离计算，NavOptima 精准数据！*
