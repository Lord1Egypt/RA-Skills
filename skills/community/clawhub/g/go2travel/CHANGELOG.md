# CHANGELOG — go2Travel

## v1.9.2 (2026-04-01)

### ⚡ 优化
- 新增输出末尾附加提示机制（Step 5）
- 根据行程内容动态展示 4-6 条可进一步了解的信息
- 提示用户可主动触发：审查/验证/行李/拍照/天气/美食等详细报告

## v1.9.1 (2026-04-01)

### ⚡ 优化
- 优化 trip-planner.md 输出精简原则
- 默认不输出行程审查/验证/行李等详细报告
- 核心信息优先：行程概览 + 租车 + 住宿 + 行程 + 费用 + 注意事项
- 详细报告改为用户主动触发（问"审查"/"验证"/"带什么"时才输出）

## v1.9.0 (2026-04-01)

### ✨ 新增
- 新增 📊 预算追踪专家（`roles/budget-tracker.md`）— 实时记账 + 预算预警 + 消费分析
- 新增 🏥 医疗健康专家（`roles/health-expert.md`）— 常备药清单 + 高原预防 + 医疗资源
- SKILL.md 新增 intents：`budget_tracking`, `health_advice`
- SKILL.md 新增 patterns：记账/医疗关键词匹配
- 团队扩展至 26 个角色

## v1.8.0 (2026-04-01)

### ✨ 新增
- 新增 🎯 个性化推荐专家（`roles/personalization-expert.md`）— 用户画像 + 偏好匹配 + 定制推荐
- 新增 🏗️ 多城市行程架构师（`roles/multi-city-architect.md`）— 跨城市行程 + 交通衔接 + 时间优化
- SKILL.md 新增 intents：`personalization`, `multi_city`
- SKILL.md 新增 patterns：人群标签/多城市关键词匹配
- 团队扩展至 24 个角色

## v1.7.0 (2026-04-01)

### ✨ 新增
- 新增 📋 行程审查专家角色（`roles/itinerary-reviewer.md`）— 合理性检查 + 预算审查 + 逻辑检查
- 新增 ✅ 行程验证专家角色（`roles/itinerary-validator.md`）— 可行性验证 + 开放状态 + 天气适配
- 新增 📖 旅行攻略专家角色（`roles/guide-expert.md`）— 目的地攻略 + 行前指南 + 避坑指南
- SKILL.md 新增 intents：`itinerary_review`, `itinerary_validation`, `travel_guide`
- SKILL.md 新增 patterns：审查/验证/攻略关键词匹配
- 团队扩展至 22 个角色

## v1.6.0 (2026-04-01)

### ✨ 新增
- 新增 📸 摄影专家角色（`roles/photography-expert.md`）— 拍照点推荐 + 拍摄时间 + 构图建议
- 新增 🎭 文化体验专家角色（`roles/culture-expert.md`）— 非遗体验 + 民俗活动 + 深度体验
- 新增 🏕️ 露营专家角色（`roles/camping-expert.md`）— 露营地推荐 + 装备清单 + 露营技巧
- SKILL.md 新增 intents：`photography`, `cultural_experience`, `camping`
- SKILL.md 新增 patterns：摄影/文化/露营关键词匹配
- 团队扩展至 19 个角色

## v1.5.0 (2026-04-01)

### ✨ 新增
- 新增 📖 旅行日记专家角色（`roles/diary-expert.md`）— 旅行日记 + 照片配文 + 行程总结
- 新增 🔄 应急专家角色（`roles/emergency-expert.md`）— 行程变更 + 天气预案 + 紧急求助
- SKILL.md 新增 intents：`travel_diary`, `emergency_response`
- SKILL.md 新增 patterns：日记/延误/紧急关键词匹配
- 团队扩展至 16 个角色

## v1.4.0 (2026-04-01)

### ✨ 新增
- 新增 🗺️ 路线专家角色（`roles/route-expert.md`）— 路线规划 + 最优顺序 + 交通建议
- 新增 💱 汇率专家角色（`roles/currency-expert.md`）— 实时汇率 + 换汇建议 + 小费文化
- 新增 📱 实用信息专家角色（`roles/practical-info-expert.md`）— 时差/插座/紧急电话/网络
- SKILL.md 新增 intents：`route_planning`, `currency_exchange`, `practical_info`
- SKILL.md 新增 patterns：路线/汇率/实用信息关键词匹配
- 团队扩展至 14 个角色

## v1.3.0 (2026-04-01)

### ✨ 新增
- 新增 📄 签证专家角色（`roles/visa-expert.md`）— 签证要求 + 材料清单 + 入境政策
- 新增 🛡️ 保险专家角色（`roles/insurance-expert.md`）— 保险推荐 + 保障对比 + 理赔指引
- SKILL.md 新增 intents：`visa_guide`, `travel_insurance`
- SKILL.md 新增 patterns：签证/保险关键词匹配
- 团队扩展至 11 个角色

## v1.2.0 (2026-04-01)

### ✨ 新增
- 新增 🌤️ 天气专家角色（`roles/weather-expert.md`）— 天气预报 + 穿衣建议
- 新增 🧳 行李专家角色（`roles/packing-expert.md`）— 智能行李清单 + 场景适配
- SKILL.md 新增 intents：`weather_check`, `packing_list`
- SKILL.md 新增 patterns：天气/穿衣/行李关键词匹配
- 团队架构图更新，新增天气和行李专家

## v1.1.0 (2026-04-01)

### ✨ 新增
- 新增 💰 省钱专家角色（`roles/budget-expert.md`）
- 新增 🍜 美食专家角色（`roles/food-expert.md`）
- 新增 🚗 租车专家角色（`roles/car-rental-expert.md`）
- 新增 3 个参考文档（`references/budget-expert.md`, `food-expert.md`, `car-rental-expert.md`）
- SKILL.md 新增 intents：`car_rental`, `food_search`, `budget_optimize`
- SKILL.md 新增 patterns：美食/租车/省钱关键词匹配

### 🐛 修复
- 修复 `search-poi` 命令参数错误（需同时提供 `--city-name` 和 `--keyword`）
- 修复 `search-flight` 往返搜索返回 0 条（改为去程/返程分开搜索）
- 修复酒店数据字段映射不一致问题
- 修复 SKILL.md 核心命令表中 `search-poi` 命令过时

### ⚡ 优化
- 所有角色文件新增"错误处理"章节（flyai 超时/空结果/网络异常的降级策略）
- `flight-expert.md` 标记 `--journey-type` 和 `--back-date` 为不推荐
- `hotel-expert.md` 补充 `--check-in-date` / `--check-out-date` 参数说明
- `trip-planner.md` 更新搜索策略（往返航班分开搜索、景点搜索改用 keyword-search）

## v1.0.0 (2026-03-31)

### ✨ 初始版本
- 7 个角色：旅行规划师、机票专家、酒店专家、景点专家、省钱专家、美食专家、租车专家
- 4 个参考文档：keyword-search、search-flight、search-hotel、search-poi
- 基于飞猪 MCP 实时数据的旅行规划能力
