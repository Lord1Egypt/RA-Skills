# Changelog

## 2.1.0

- 脚本从 Python 改写为纯 Shell（bash + curl），零外部依赖
- 删除 telegraph_api.py、telegraph_rss.py，统一为 telegraph_api.sh
- 移除 Python 环境依赖，所有用户开箱即用

## 2.0.0

- 重命名 Skill：`itjuzi-data` → `itjuzi-bulletin`
- 新增带鉴权的创投电报接口（`/api/telegraph/get_list`）
- 支持 Skill Token 鉴权，免费/会员用户自动分级返回
- 会员专属功能：完整正文、结构化数据（公司/金额/轮次/投资方）、昨日数据、关键词筛选、事件类型筛选
- 免费版保留基础体验（今日摘要），回答末尾自动引导升级

## 1.1.0

- 新增 RSS 读取能力，主能力改为"当天最新事件"和"近期创投动态"

## 1.0.0

- 初始发布
