# 主流房产平台数据源参考

## 平台概览

### 贝壳找房 (ke.com / app.ke.com)
- **覆盖**: 全国300+城市，二手房/新房/租房/成交
- **数据特点**: 房源真实性高（要求业主实名认证），VR看房，小区详情丰富
- **URL模式**: `{city}.ke.com/ershoufang/` (二手房), `{city}.ke.com/chengjiao/` (成交)
- **搜索技巧**: 可拼接筛选参数，如 `{city}.ke.com/ershoufang/pg2/` (第2页)
- **城市代码**: bj(北京), sh(上海), gz(广州), sz(深圳), hz(杭州), cd(成都), nj(南京) 等拼音首字母

### 链家 (lianjia.com)
- **覆盖**: 30+核心城市，以二手/租房为主
- **数据特点**: 房源真实性高，经纪人信息透明，VR看房
- **URL模式**: `{city}.lianjia.com/ershoufang/` (二手房), `{city}.lianjia.com/zufang/` (租房)
- **与贝壳关系**: 贝壳旗下的直营品牌，部分数据互通

### 安居客 (anjuke.com)
- **覆盖**: 全国600+城市，新房/二手房/租房
- **数据特点**: 新房覆盖最广，开发商合作多
- **URL模式**: `{city}.anjuke.com/sale/` (二手房), `{city}.fang.anjuke.com/` (新房)
- **注意**: 部分房源信息可能不够新，需交叉验证

### 房天下 (fang.com)
- **覆盖**: 全国重点城市，新房/二手房/租房
- **数据特点**: 楼盘信息全面（容积率/绿化率/开发商）
- **URL模式**: `{city}.fang.com/` (首页), `{city}.newhouse.fang.com/` (新房)

### 58同城 (58.com)
- **覆盖**: 全国城市，租房为主
- **数据特点**: 租房信息量大，但中介混杂
- **注意**: 虚假房源较多，需谨慎筛选

### 我爱我家 (5i5j.com)
- **覆盖**: 北京/上海/杭州等城市
- **数据特点**: 老牌中介，房源真实性中等

### 诸葛找房 (zhuge.com)
- **覆盖**: 聚合多平台房源
- **数据特点**: 聚合平台，可跨平台比价

## 搜索关键词模板

### 二手房
```
- 贝壳找房 {city} {district} 二手房 {room_count}室 {budget_min}-{budget_max}万
- 链家 {city} {district} 二手房 均价 2026
- {city} {district} 二手房 急售 降价
- {city} {community_name} 二手房 在售
```

### 租房
```
- {city} {district} 租房 {room_count}室 {budget}以内
- 贝壳租房 {city} {district}
- {city} {district} 整租 {room_count}室
```

### 新房
```
- {city} {district} 新楼盘 2026
- 贝壳新房 {city} {developer_name}
- {city} {district} 在售楼盘 价格
```

### 笋盘
```
- {city} 笋盘 降价 急售
- {city} 低于市场价 二手房
- {city} {district} 业主急售
```

### 成交记录
```
- 链家 {city} {community_name} 成交记录
- 贝壳 {city} {community_name} 成交价
- {city} {community_name} 最新成交均价 2026
```

### 小区信息
```
- {city} {community_name} 小区 物业 绿化
- {city} {community_name} 周边配套 地铁 学校
- {city} {community_name} 房价 均价
```

### 学区
```
- {city} {district} 学区划片 2026
- {city} {school_name} 对口小区
- {city} 小学排名 学区房
- {city} 教育局 学区划分 政策
```

## 数据提取注意事项

1. **价格单位**: 贝壳/链家单位为"万"（万元），安居客/房天下可能不同，需统一
2. **面积单位**: 统一为"平米"（平方米）
3. **楼层描述**: "低楼层/中楼层/高楼层" + "共X层"
4. **建成年代**: 部分平台显示"年代"，格式如"2000年建成"
5. **房产证**: "满五唯一"、"满二"等税费相关标签
6. **挂牌时间**: 贝壳/链家显示发布时间

## 区域均价获取策略

当无法直接获取区域均价时:
1. 搜索 "{city} {district} 二手房均价 2026"
2. 搜索 "{city} {district} 房价 参考均价"
3. 从采集到的房源单价中计算中位数作为近似均价
4. 参考多个来源取均值

## 学区信息来源

- 各地教育局官网 (edu.xx.gov.cn)
- 贝壳/链家学区频道
- 本地教育类公众号文章
- 百度百科学校词条
