# miniprogram-mall-ushopun-skill
基于 Ushopun（优社云AI）官方 miniProgramV2 真实项目构建的微信小程序商城前端，覆盖首页、分类、商品详情、购物车、结算、订单、个人中心等 50+ 页面与完整交易链路。内置 dev.ushopun.com OpenAPI（接口前缀 /api/v2，返回体 code/content/data，guid/token/shopId 鉴权）完整接口对接规范与每个方法的调用示例。当用户需要开发对接 Ushopun 后端（优社云）的微信小程序商城时调用此 Skill。后端接口文档参考同目录 openapi.json（#File ./openapi.json，servers 为 {tenant}.ushopun.com 泛域名模板，开发填 dev，正式替换租户子域名）。
